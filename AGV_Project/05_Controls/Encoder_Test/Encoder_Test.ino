volatile long encoderCount = 0;

const int pinA = 2;
const int pinB = 3;

unsigned long lastTimeMs = 0;
long lastCount = 0;

const float dt = 0.1f;          // 100 ms sample
const int sampleMs = 100;


const float CPR = 1200.0f;      // PPR=600 -> CPR=1200 

float rpmFilt = 0.0f;
const float alpha = 0.80f;      //higher == smoother

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

  // Direction decode 
  if (A == B) encoderCount++;
  else        encoderCount--;
}
