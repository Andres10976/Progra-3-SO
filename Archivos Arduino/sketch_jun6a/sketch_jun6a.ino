#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Keypad.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const int ROWS = 4; // Número de filas del keypad
const int COLS = 3; // Número de columnas del keypad

char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};

byte rowPins[ROWS] = {3, 4, 5, 6};      // Pines digitales conectados a las filas
byte colPins[COLS] = {A0, A1, A2}; // Pines analógicos conectados a las columnas

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  //keypad
  Serial.begin(9600);

  // Inicializar la comunicación I2C en el Arduino Mega
  Wire.begin();
  // Inicializar el display SSD1306
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  // Limpiar el buffer del display
  display.clearDisplay();
  // Mostrar un texto en el display
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("¡Hola, Arduino!");
  // Mostrar el contenido del buffer en el display
  display.display();
}

void loop() {
  char key = keypad.getKey();
  
  if (key) {
   	Serial.println(key);
	display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextSize(1);
    display.print("Digitado: ");
    display.println(key);
    display.display();
  }
}
