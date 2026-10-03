// ==========================================
// 2-LED DIRECTION CONTROL
// ==========================================

// Buttons
const int NORTH_BUTTON = 25;
const int SOUTH_BUTTON = 26;
const int EAST_BUTTON  = 27;
const int WEST_BUTTON  = 14;

// LEDs
const int NS_LED = 18;   // North + South
const int EW_LED = 22;   // East + West


void setup() {

  Serial.begin(115200);

  // Buttons
  pinMode(NORTH_BUTTON, INPUT_PULLUP);
  pinMode(SOUTH_BUTTON, INPUT_PULLUP);
  pinMode(EAST_BUTTON, INPUT_PULLUP);
  pinMode(WEST_BUTTON, INPUT_PULLUP);

  // LEDs
  pinMode(NS_LED, OUTPUT);
  pinMode(EW_LED, OUTPUT);

  // Initially OFF
  digitalWrite(NS_LED, LOW);
  digitalWrite(EW_LED, LOW);

  Serial.println("Smart Ambulance System Started");
}


void loop() {

  int north = digitalRead(NORTH_BUTTON);
  int south = digitalRead(SOUTH_BUTTON);
  int east  = digitalRead(EAST_BUTTON);
  int west  = digitalRead(WEST_BUTTON);


  // ==========================================
  // NORTH / SOUTH
  // ==========================================

  if (north == LOW || south == LOW) {

    digitalWrite(NS_LED, HIGH);
    digitalWrite(EW_LED, LOW);

    if (north == LOW) {
      Serial.println("NORTH");
    }

    if (south == LOW) {
      Serial.println("SOUTH");
    }
  }


  // ==========================================
  // EAST / WEST
  // ==========================================

  else if (east == LOW || west == LOW) {

    digitalWrite(NS_LED, LOW);
    digitalWrite(EW_LED, HIGH);

    if (east == LOW) {
      Serial.println("EAST");
    }

    if (west == LOW) {
      Serial.println("WEST");
    }
  }


  // ==========================================
  // NO BUTTON PRESSED
  // ==========================================

  else {

    digitalWrite(NS_LED, LOW);
    digitalWrite(EW_LED, LOW);
  }


  delay(50);
}