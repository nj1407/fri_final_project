Code modeled form http://www.pirobot.org/blog/0022/
Changed dictionary, language modeling files, (config directory)
Changed voice_nav to use move_base instead of twists and have a buffer of commands

How to Run:

roslaunch pi_speech_tutorial voice_nav_commands.launch
(launches recognizer)
roslaunch pi_speech_tutorial turtlebot_voice_.launch
(launches the command
roslaunch bwi_launch segbot_v2.launch

What it does:
It uses sphinx to recognize words based on a predefined dictionary and language model. Compiled  on http://www.speech.cs.cmu.edu/tools/
lmtool-new.html and uses takes these words and does actions based off of them in voice_nav.py . In voice_nav the code also publishes where
it is in the program (the state of the program) to the node five(named it this since originally had five states). This is done so the node
serialOut in the lights package can subscribe to five and know the state and execute the arduino code based on this.
