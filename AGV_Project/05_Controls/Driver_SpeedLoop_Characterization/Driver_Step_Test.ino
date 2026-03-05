#include <Arduino.h>

const uint8_t DE_PIN = 4;
const uint8_t SLAVE_ID = 0x01;

// Registers
const uint16_t REG_MODE      = 0x0136;
const uint16_t REG_FAULT     = 0x0076;
const uint16_t REG_RUN       = 0x0066;
const uint16_t REG_SPEED_SET = 0x0056;

const uint16_t REG_SPEED_ACT = 0x005F;
const uint16_t REG_CURRENT   = 0x00B6;

// Manual: 25 counts = 1A
static inline float currentA_fromRaw(uint16_t raw) { return raw / 25.0f; }

// ---- Modbus helpers ----
uint16_t crc16(const uint8_t *buf, uint8_t len) {
  uint16_t crc = 0xFFFF;
  for (uint8_t i = 0; i < len; i++) {
    crc ^= buf[i];
    for (uint8_t j = 0; j < 8; j++) {
      if (crc & 1) crc = (crc >> 1) ^ 0xA001;
      else crc >>= 1;
    }
  }
  return crc;
}

void txEnable() { digitalWrite(DE_PIN, HIGH); delayMicroseconds(20); }
void txDisable(){ digitalWrite(DE_PIN, LOW);  delayMicroseconds(20); }
void clearRx()  { while (Serial1.available()) (void)Serial1.read(); }

uint8_t readBytes(uint8_t* buf, uint8_t len, uint16_t timeout_ms) {
  uint8_t got = 0;
  uint32_t t0 = millis();
  while ((millis() - t0 < timeout_ms) && got < len) {
    if (Serial1.available()) buf[got++] = (uint8_t)Serial1.read();
  }
  return got;
}

// Single RTU transaction boundary + quiet time
void sendFrame(uint8_t* frame, uint8_t len) {
  clearRx();
  txEnable();
  Serial1.write(frame, len);
  Serial1.flush();
  delayMicroseconds(120);
  txDisable();
  delay(6); // RTU quiet time (safe at 9600)
}

void write06(uint16_t reg, uint16_t val) {
  uint8_t frame[8];
  frame[0] = SLAVE_ID;
  frame[1] = 0x06;
  frame[2] = (reg >> 8) & 0xFF;
  frame[3] = reg & 0xFF;
  frame[4] = (val >> 8) & 0xFF;
  frame[5] = val & 0xFF;

  uint16_t c = crc16(frame, 6);
  frame[6] = c & 0xFF;
  frame[7] = (c >> 8) & 0xFF;

  sendFrame(frame, 8);

  // consume echo (RE always enabled)
  uint8_t echo[8];
  (void)readBytes(echo, 8, 50);

  delay(10); // driver processing margin
}

bool readHolding1_echo(uint16_t reg, uint16_t &val) {
  uint8_t req[8];
  req[0] = SLAVE_ID;
  req[1] = 0x03;
  req[2] = (reg >> 8) & 0xFF;
  req[3] = reg & 0xFF;
  req[4] = 0x00;
  req[5] = 0x01;

  uint16_t c = crc16(req, 6);
  req[6] = c & 0xFF;
  req[7] = (c >> 8) & 0xFF;

  sendFrame(req, 8);

  // discard echo
  uint8_t echo[8];
  if (readBytes(echo, 8, 80) != 8) return false;

  // response: 01 03 02 hi lo crc crc
  uint8_t resp[7];
  if (readBytes(resp, 7, 200) != 7) return false;

  if (resp[0] != SLAVE_ID || resp[1] != 0x03 || resp[2] != 0x02) return false;

  uint16_t rcrc = (uint16_t)resp[5] | ((uint16_t)resp[6] << 8);
  if (crc16(resp, 5) != rcrc) return false;

  val = ((uint16_t)resp[3] << 8) | resp[4];
  return true;
}

// ---- Step schedule ----
struct StepSeg { uint16_t rpm; uint32_t dur_ms; };

StepSeg seq[] = {
  {0,    2000},
  {500,  4000},
  {1500, 4000},
  {2500, 4000},
  {3000, 4000},
  {1500, 4000},
  {0,    4000},
};
const uint8_t N = sizeof(seq)/sizeof(seq[0]);

// ---- State ----
uint32_t t0;
uint8_t seg = 0;
uint32_t segStart;

bool readSpeedNext = true;
uint16_t lastSpeed = 0;
uint16_t lastCurRaw = 0;

void applySegment(uint8_t i) {
  write06(REG_RUN, 1);
  write06(REG_SPEED_SET, seq[i].rpm);
}

void setup() {
  pinMode(DE_PIN, OUTPUT);
  txDisable();

  Serial.begin(115200);
  Serial1.begin(9600); // 8N1 (your verified setting)
  delay(500);

  Serial.println("t_ms,seg,cmd_rpm,speed_raw,curr_raw,curr_A");

  // init sequence
  write06(REG_MODE, 1);        // internal mode
  write06(REG_FAULT, 0);       // clear faults
  write06(REG_RUN, 0);         // stop
  write06(REG_SPEED_SET, 0);   // speed 0
  delay(200);

  // start test
  t0 = millis();
  seg = 0;
  segStart = millis();
  applySegment(seg);

  delay(300); // let motor start responding
}

void loop() {
  uint32_t now = millis();

  // Segment advance
  if (now - segStart >= seq[seg].dur_ms) {
    seg++;
    if (seg >= N) seg = 0;            // loop forever (good for repeated captures)
    segStart = now;
    applySegment(seg);
  }

  // Refresh command occasionally (robustness)
  static uint32_t lastCmdRefresh = 0;
  if (now - lastCmdRefresh >= 2000) {
    write06(REG_RUN, 1);
    write06(REG_SPEED_SET, seq[seg].rpm);
    lastCmdRefresh = now;
  }

  // Log at 10 Hz
  static uint32_t lastLog = 0;
  if (now - lastLog >= 100) {
    lastLog = now;

    // cycle-read (5 Hz per channel)
    if (readSpeedNext) {
      uint16_t spd;
      if (readHolding1_echo(REG_SPEED_ACT, spd)) lastSpeed = spd;
    } else {
      uint16_t cur;
      if (readHolding1_echo(REG_CURRENT, cur)) lastCurRaw = cur;
    }
    readSpeedNext = !readSpeedNext;

    Serial.print(now - t0); Serial.print(",");
    Serial.print(seg);      Serial.print(",");
    Serial.print(seq[seg].rpm); Serial.print(",");
    Serial.print(lastSpeed);    Serial.print(",");
    Serial.print(lastCurRaw);   Serial.print(",");
    Serial.println(currentA_fromRaw(lastCurRaw), 3);
  }
}
