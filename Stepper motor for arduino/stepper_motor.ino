#define ENABLE 8
#define X_STEP 2
#define Y_STEP 3
#define Z_STEP 4
#define A_STEP 12
#define X_DIR  5
#define Y_DIR  6
#define Z_DIR  7
#define A_DIR  13
int incomingByte;

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
char axisFromPC[numChars] = {0};
int directionFromPC = 0;
float speedFromPC = 0.0;
int dir;
int stp;
int spd = 0;
int shutterDelay = 1500;
bool shutter = false;
unsigned long shutterTimeStamp;
bool light = false;
bool motor = false;
bool osa = false;
unsigned long timeStamp;

boolean newData = false;


void setup() {
  // nastavení směrů pro všechny piny
  pinMode(X_STEP, OUTPUT);
  pinMode(Y_STEP, OUTPUT);
  pinMode(Z_STEP, OUTPUT);
  pinMode(A_STEP, OUTPUT);
  pinMode(X_DIR,  OUTPUT);
  pinMode(Y_DIR,  OUTPUT);
  pinMode(A_DIR,  OUTPUT);
  pinMode(ENABLE, OUTPUT);
  // povolení řízení pro všechny drivery
  digitalWrite(ENABLE, HIGH);
  Serial.begin(9600);
  digitalWrite (A_DIR, false);
  shutterTimeStamp = 0;
//  digitalWrite(ENABLE, LOW);
//    motor = true;
//    timeStamp = millis();
//    spd = 5000;
}


void turnMotor() {

    if (strcmp(axisFromPC, "X") == 0)
    {
      dir = X_DIR;
      stp = X_STEP;
      motor = true;
    }
    if (strcmp(axisFromPC, "Y") == 0)
    {
      dir = Y_DIR;
      stp = Y_STEP;
      motor = true;
    }
    if (strcmp(axisFromPC, "Z") == 0)
    {
      
      dir = Z_DIR;
      stp = Z_STEP;
      motor = true;
    }
  
    if (motor)
    {
    digitalWrite(ENABLE, LOW);
    if (directionFromPC == 1)
    {
    osa = true;
    }
    if (directionFromPC == 0)
    {
    osa = false;
    }
    digitalWrite (dir, osa);
    timeStamp = millis();
    spd = (int) speedFromPC;
    }

    if (strcmp(axisFromPC, "A") == 0)
    {
      shutterTimeStamp = millis();
      if (directionFromPC == 1)
      {
      shutter = true;   
      }
      if (directionFromPC == 0)
      {
      shutter = false;       
      }
    }
}

void loop() {


   if (shutter && ((shutterTimeStamp + shutterDelay) > millis()) && millis()>1500)
   {
    digitalWrite(A_DIR, HIGH);
    delayMicroseconds(100);
    digitalWrite(A_DIR, LOW);
   }

   if (!shutter && ((shutterTimeStamp + shutterDelay) > millis()) && millis()>1500)
   {
    digitalWrite(A_DIR, HIGH);
    delayMicroseconds(2000);
    digitalWrite(A_DIR, LOW);
   }
   
    if (light){
    digitalWrite(A_STEP, HIGH);
    }

    if (motor)
    {
      digitalWrite(stp, HIGH);
    }
    delayMicroseconds (100);

    if (light){
    digitalWrite(A_STEP, LOW);
    }

    if (motor)
    {
      digitalWrite(stp, LOW);
    }
    delayMicroseconds (100);

    if ((timeStamp + spd) < millis())
    {
      motor = false;
    }

    if (!motor && !light)
    {
      motor = false;
      light = false;
      digitalWrite(ENABLE, HIGH); 
    }




    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        turnMotor();
        newData = false;
    }

}

void pohybOsy(boolean smer, byte dirPin, byte stepPin, int kroky) {
  // zápis směru na příslušný pin DIR
  digitalWrite (dirPin, smer);
  delay(50);
  // smyčka pro provedení předaného množství kroků
  for (int i = 0; i < kroky; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds (800);
    digitalWrite(stepPin, LOW);
    delayMicroseconds (800);
  }
}


void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    strcpy(axisFromPC, strtokIndx); // copy it to axisFromPC
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    directionFromPC = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    speedFromPC = atof(strtokIndx);     // convert this part to a float

}

//============
