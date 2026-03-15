#include <Arduino.h>

const uint8_t DE_PIN = 4;
const uint8_t SLAVE_ID = 0x01;

// ---------------- Modbus Registers ----------------
const uint16_t REG_MODE      = 0x0136;
const uint16_t REG_FAULT     = 0x0076;
const uint16_t REG_RUN       = 0x0066;
const uint16_t REG_SPEED_SET = 0x0056;
const uint16_t REG_SPEED_ACT = 0x005F;
const uint16_t REG_POLEPAIR  = 0x0116;

// ---------------- Pins ----------------
const uint8_t ENCODER_A_PIN = 2;
const uint8_t PG_PIN        = 3;

// ---------------- Measurement constants ----------------
const uint16_t ENCODER_CPR = 600;
const uint16_t POLE_PAIRS = 5;
const uint16_t PG_PULSES_PER_REV = 3 * POLE_PAIRS;   // = 15
const uint32_t WINDOW_MS = 200;

// Optional encoder deglitch filter
const unsigned long MIN_ENCODER_PULSE_US = 30;

// ---------------- Step schedule ----------------
struct StepSeg {
  uint16_t rpm;
  uint32_t dur_ms;
};

StepSeg seq[] = {
  {0,    3000},
  {1000, 5000},
  {1500, 5000},
  {2000, 5000},
  {2500, 5000},
  {0,    5000}
};

const uint8_t N_SEG = sizeof(seq) / sizeof(seq[0]);

// ---------------- Counters ----------------
volatile long encoderCountWindow = 0;
volatile long encoderCountTotal  = 0;
volatile long pgCountWindow      = 0;
volatile long pgCountTotal       = 0;
volatile unsigned long lastEncoderPulseUs = 0;

// ---------------- State ----------------
uint8_t seg = 0;
uint32_t segStart = 0;
uint32_t testStart = 0;

// ---------------- Helpers ----------------
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

void txEnable() {
  digitalWrite(DE_PIN, HIGH);
  delayMicroseconds(20);
}

void txDisable() {
  digitalWrite(DE_PIN, LOW);
  delayMicroseconds(20);
}

void clearRx() {
  while (Serial1.available()) {
    (void)Serial1.read();
  }
}

uint8_t readBytes(uint8_t* buf, uint8_t len, uint16_t timeout_ms) {
  uint8_t got = 0;
  uint32_t t0 = millis();
  while ((millis() - t0 < timeout_ms) && got < len) {
    if (Serial1.available()) {
      buf[got++] = (uint8_t)Serial1.read();
    }
  }
  return got;
}

void sendFrame(uint8_t* frame, uint8_t len) {
  clearRx();
  txEnable();
  Serial1.write(frame, len);
  Serial1.flush();
  delayMicroseconds(120);
  txDisable();
  delay(6); // safe RTU quiet time at 9600
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

  uint8_t echo[8];
  (void)readBytes(echo, 8, 50);

  delay(10);
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

  uint8_t echo[8];
  if (readBytes(echo, 8, 80) != 8) return false;

  uint8_t resp[7];
  if (readBytes(resp, 7, 200) != 7) return false;

  if (resp[0] != SLAVE_ID || resp[1] != 0x03 || resp[2] != 0x02) return false;

  uint16_t rcrc = (uint16_t)resp[5] | ((uint16_t)resp[6] << 8);
  if (crc16(resp, 5) != rcrc) return false;

  val = ((uint16_t)resp[3] << 8) | resp[4];
  return true;
}

static inline float rpm_fromCounts(long counts, uint16_t pulses_per_rev, uint32_t window_ms) {
  return (counts * 60000.0f) / (pulses_per_rev * window_ms);
}

void applySegment(uint8_t i) {
  write06(REG_RUN, 1);
  write06(REG_SPEED_SET, seq[i].rpm);
}

// ---------------- ISRs ----------------
void encoderISR() {
  unsigned long nowUs = micros();
  if ((unsigned long)(nowUs - lastEncoderPulseUs) >= MIN_ENCODER_PULSE_US) {
    encoderCountWindow++;
    encoderCountTotal++;
    lastEncoderPulseUs = nowUs;
  }
}

void pgISR() {
  pgCountWindow++;
  pgCountTotal++;
}

void setup() {
  pinMode(DE_PIN, OUTPUT);
  txDisable();

  pinMode(ENCODER_A_PIN, INPUT);
  pinMode(PG_PIN, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENCODER_A_PIN), encoderISR, RISING);
  attachInterrupt(digitalPinToInterrupt(PG_PIN), pgISR, RISING);

  Serial.begin(115200);
  Serial1.begin(9600);
  delay(500);

  uint16_t polePairsReg = 0;
  if (readHolding1_echo(REG_POLEPAIR, polePairsReg)) {
    Serial.print("# pole_pairs_reg=");
    Serial.println(polePairsReg);
  } else {
    Serial.println("# pole_pairs_reg=ERR");
  }

  Serial.print("# min_encoder_pulse_us=");
  Serial.println(MIN_ENCODER_PULSE_US);

  Serial.println("t_ms,segment,cmd_rpm,driver_rpm,pg_rpm,encoder_rpm,pg_counts,enc_counts,pg_total,enc_total");

  // Drive init
  write06(REG_MODE, 1);
  write06(REG_FAULT, 0);
  write06(REG_RUN, 0);
  write06(REG_SPEED_SET, 0);
  delay(200);

  testStart = millis();
  segStart = millis();
  seg = 0;
  applySegment(seg);

  delay(300);
}

void loop() {
  uint32_t now = millis();

  // Segment advance
  if (now - segStart >= seq[seg].dur_ms) {
    seg++;
    if (seg >= N_SEG) {
      // stop motor and halt logging sequence
      write06(REG_RUN, 0);
      write06(REG_SPEED_SET, 0);
      Serial.println("# test_complete");
      while (true) {
        delay(1000);
      }
    }
    segStart = now;
    applySegment(seg);
  }

  // Refresh command occasionally
  static uint32_t lastRefresh = 0;
  if (now - lastRefresh >= 2000) {
    write06(REG_RUN, 1);
    write06(REG_SPEED_SET, seq[seg].rpm);
    lastRefresh = now;
  }

  // Synchronized measurement/logging
  static uint32_t lastWindow = millis();
  if (now - lastWindow >= WINDOW_MS) {
    noInterrupts();
    long encCounts = encoderCountWindow;
    long pgCounts  = pgCountWindow;
    long encTotal  = encoderCountTotal;
    long pgTotal   = pgCountTotal;
    encoderCountWindow = 0;
    pgCountWindow = 0;
    interrupts();

    uint16_t driverSpeedRaw = 0;
    bool speedOk = readHolding1_echo(REG_SPEED_ACT, driverSpeedRaw);

    float encoderRPM = rpm_fromCounts(encCounts, ENCODER_CPR, WINDOW_MS);
    float pgRPM      = rpm_fromCounts(pgCounts, PG_PULSES_PER_REV, WINDOW_MS);

    Serial.print(now - testStart);       Serial.print(",");
    Serial.print(seg);                   Serial.print(",");
    Serial.print(seq[seg].rpm);          Serial.print(",");
    if (speedOk) Serial.print(driverSpeedRaw);
    else         Serial.print("ERR");
    Serial.print(",");
    Serial.print(pgRPM, 2);              Serial.print(",");
    Serial.print(encoderRPM, 2);         Serial.print(",");
    Serial.print(pgCounts);              Serial.print(",");
    Serial.print(encCounts);             Serial.print(",");
    Serial.print(pgTotal);               Serial.print(",");
    Serial.println(encTotal);

    lastWindow = now;
  }
}