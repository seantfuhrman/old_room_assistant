This is a voice activated assistant to be run on Raspberry Pi. 
It utilizes a mic array connected to the Raspberry Pi as audio input, and speakers connected through USB as audio output.
It is capable of: 
    - Turning on/off lights
    - Turning on/off my lamp
    - Playing Music
    - Adjusting Volume
    - Reciting the weather 

It also includes and AddMusic executable that is used to automatically add music to the directory of the raspberry pi through a GUI. It takes a youtube link as input and converts the audio to MP3 and uploads it to the Pi.

Turning on/off of lights is done through an RF signal to an Arduino capable of changing the lights through a servo motor
Turning on/off the lamp is done similarly but with an Arduino connected to a relay. 

NEXT VERSION IMPROVEMENTS: 
 - Use Spotify API Library/ WEB SDK as Music Player
 - Use GOVEE API to change LED strip lights
