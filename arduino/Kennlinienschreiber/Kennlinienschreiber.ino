
// check if we compile on an Arduino with DAC
#if !defined(ARDUINO_UNOR4_MINIMA) && !defined(ARDUINO_UNOR4_WIFI)
#error("Code needs a UNO R4 (with DAC) to work")
#endif

void setup() {
  Serial.begin();             // start the serial port
  pinMode(A0, OUTPUT);        // set A0 pin (DAC) as output
  analogReadResolution(14);   // 14bit ADC resolution --> 16384
  analogWriteResolution(12);  // 12bit DAC resolution --> 4096
  pinMode(LED_BUILTIN, OUTPUT);
}

int count=0;

void loop() {

  if (Serial.available()) {                     // check if there is data on the serial port
    String msg = Serial.readStringUntil('\n');  // read a line from the serial port
    msg.trim();                                 // remove leading and trailing white spaces
    boolean command_ok = false;                 // track if a command was received

    // for '?', output help
    if (msg.startsWith("?") || msg.startsWith("h")) {
      command_ok = true;
      
      Serial.println("OK: Kennlinienschreiber");
      Serial.println("# send 'S [value]' to set output voltage");
      Serial.println("# send 'M [#pin]' to read pin voltage");
    }

    // for 'S', set the output
    if (msg.startsWith("S")) {
      command_ok = true;
      int value = msg.substring(2).toInt();
      
      if (value<0||value>4095) {
        Serial.println("ERR: Value out of range [0..4495]: "+String(value));
      } else {
        analogWrite(A0, value);
        Serial.println("OK: Setting output to: "+String(value));
      }

    }

    // for 'M', read the input
    if (msg.startsWith("M")) {
      command_ok = true;
      int pin = msg.substring(2).toInt();
      
      if (pin<1||pin>5) {
        Serial.println("ERR: Can only read pins A1 to A5: A"+String(pin));
      } else {
        // PIN A0 is 14, A1 15, ..., see:
        // https://github.com/arduino/ArduinoCore-renesas/blob/main/variants/MINIMA/pins_arduino.h
        int value = analogRead(pin+14);
        Serial.println("OK: "+String(value));
      }
    }

    // check if we have processed a valid command
    if (!command_ok) {
      Serial.println("ERR: command unknown: "+msg);
    }


  } else {
    // if no data is received, wait 10ms and
    // blink the LED from time to time
    digitalWrite(LED_BUILTIN, ((count++ /50)%2));
    delay(10);
  }

}
