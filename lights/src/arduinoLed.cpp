#include <PololuLedStrip.h>

// Create an ledStrip object and specify the pin it will use.
PololuLedStrip<12> ledStrip;

// Create a buffer for holding the colors (3 bytes per color).
#define LED_COUNT 60
rgb_color colors[LED_COUNT];
char com;
rgb_color color;

void setup()
{
  // Start up the serial port, for communication with the PC.
  Serial.begin(115200);
  Serial.println("Ready to receive colors."); 
}

//Blinks lights in color read over serial connection
void blink()
{
  rgb_color off;
      off.red = 0;
      off.blue = 0;
      off.green = 0;

  delay(200);
  for(uint16_t i = 0; i < LED_COUNT; i++)
  {
    colors[i] = color;
  }
  ledStrip.write(colors, LED_COUNT);
  delay(200);
  for(uint16_t i = 0; i < LED_COUNT; i++)
  {
    colors[i] = off;
  }
  ledStrip.write(colors, LED_COUNT);
  
}

//Chooses two random colors and makes the LED's light up alternating between these colors
void dance2()
{
  rand();
    rgb_color randColor1;
    randColor1.red = rand() % 255 + 20;
    randColor1.green = rand() % 255 + 20;
    randColor1.blue = rand() % 255 + 20;

    rgb_color randColor2;
    randColor2.red = rand() % 255 + 20;
    randColor2.green = rand() % 255 + 20;
    randColor2.blue = rand() % 255 + 20;

    for(uint16_t i = 0; i < LED_COUNT; i++)
    {
      if(i%2 == 0)
          colors[i] = randColor1;
      else
          colors[i] = randColor2;
      delay(5);
    }
    ledStrip.write(colors, LED_COUNT);
}

//Chooses a random light to light up a random color
void dance()
{
    rgb_color randColors;
    randColors.red = rand() % 255;
    randColors.green = rand() % 255;
    randColors.blue = rand() % 255;

    uint16_t index = rand() % LED_COUNT;
    colors[index] = randColors;
    ledStrip.write(colors, LED_COUNT);
}

//5 lights wrap continuously around the LED Strip in color read in over serial
void wrap(rgb_color color)
{
      rgb_color off;
      off.red = 0;
      off.blue = 0;
      off.green = 0;
      
      for(uint16_t i = 5; i < LED_COUNT; i++)
      {
        colors[i-4] = off;
        colors[i] = color;
        ledStrip.write(colors, LED_COUNT);  
        delay(15);
      }
      for(uint16_t j = LED_COUNT - 5; j < LED_COUNT; j++)
      {
        colors[j] = off;
        ledStrip.write(colors, LED_COUNT);  
        delay(15);
      }
}

void loop()
{
  //Does not do anythng until info is available over Serial connection
  if (Serial.available())
  {
    Serial.print("SERIAL AVAILABLE"); //When there is info being sent over serial
    
    com = Serial.read(); //type of command to execute

    //read in the color
    color.red = Serial.parseInt();
    color.green = Serial.parseInt();
    color.blue = Serial.parseInt();
  }
 
      if(com == 'd')
        dance2();
      else if(com == 'e')
        dance();
      else if(com == 'w')
        wrap(color);
      else if(com == 'b')
        blink();
  
}
