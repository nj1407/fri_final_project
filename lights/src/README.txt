How to run:
rosrun lights serialOut

(run the arduino code on arduino ide once before start program to get LEDs to word)

What it does:
Creates a serial connection from the computer/ros to the arduino. Subscribing to five(node with input of state from sphinx package a.k.a pi_speech_tutorial). Telling the arduino what to make the led colors based on the state of the sphinx code. Acts like a state machine telling leds to turn yellow when does basic movements, green when idle, and red when a command isn't recognized.  
