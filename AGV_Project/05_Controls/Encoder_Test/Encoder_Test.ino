volatile long encoderCount = 0;

const int pinA = 2;
const int pinB = 3;

unsigned long lastTimeMs = 0;
long lastCount = 0;

const float dt = 0.1f;          // 100 ms sample
const int sampleMs = 100;

// IMPORTANT:
// CPR = counts per revolution (what YOUR code counts per rev).
// Because we count A on CHANGE => 2 edges per A pulse.
// If your encoder is specified as PPR (channel A pulses per rev),
// then CPR = 2 * PPR.
// Put your best current estimate here and update when you find the datasheet.
const float CPR = 1200.0f;      // example: PPR=600 -> CPR=1200 (A CHANGE)

float rpmFilt = 0.0f;
const float alpha = 0.80f;      // closer to 1 = more smoothing

void setup() {
  Serial.begin(115200);

  pinMode(pinA, INPUT_PULLUP);
  pinMode(pinB, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(pinA), handleEncoderA, CHANGE);
  lastTimeMs = millis();
}

void loop() {
  unsigned long now = millis();
  if (now - lastTimeMs >= (unsigned long)sampleMs) {

    long currentCount;
    noInterrupts();
    currentCount = encoderCount;
    interrupts();

    long delta = currentCount - lastCount;

    float cps = delta / dt;                 // counts per second
    float rps = cps / CPR;                  // revolutions per second
    float rpmRaw = rps * 60.0f;

    rpmFilt = alpha * rpmFilt + (1.0f - alpha) * rpmRaw;

    Serial.print("delta=");
    Serial.print(delta);
    Serial.print("  rpmRaw=");
    Serial.print(rpmRaw, 2);
    Serial.print("  rpmFilt=");
    Serial.println(rpmFilt, 2);

    lastCount = currentCount;
    lastTimeMs += sampleMs; // better timing than lastTimeMs = now
  }
}

void handleEncoderA() {
  bool A = digitalRead(pinA);
  bool B = digitalRead(pinB);

  // Direction decode (works for many encoders; if reversed, swap ++/--)
  if (A == B) encoderCount++;
  else        encoderCount--;
}
