import speech_recognition as sr
import os, time, random, wave, contextlib, re, pyowm, vw, pigpio
from gtts import gTTS
from pygame import mixer
from mutagen.mp3 import MP3
from fuzzywuzzy import fuzz

r = sr.Recognizer()
mic = sr.Microphone()
language = 'en'

mixer.init()
x = 0.5
PlayingMusic = False
reading = False

MusicDir = "/home/pi/Home/Music//"
HomeDir = "/home/pi/Home//"

TX = 21
pi = pigpio.pi()
BPS = 2000
tx = vw.tx(pi, TX, BPS) # Specify Pi, tx GPIO, and baud.


owm = pyowm.OWM('0370ddfb83dfbb13c6c688d8a2cd5d1c')
observation = owm.weather_at_coords(40.5123,-74.8593)



def listen (duration): 
    with mic as source:
        audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        words = r.recognize_google(audio)
        return words
    except sr.RequestError:
        print ("API Not Avaliable")
        return None
    except sr.UnknownValueError:
        return None
        

def respond(file): 
    if ".wav" in file:   
        with contextlib.closing(wave.open(HomeDir + file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        mixer.music.pause()    
        sound = mixer.Sound(HomeDir + file)
        mixer.Sound.play(sound)
        time.sleep(duration)
        mixer.music.unpause()    
    elif ".mp3" in file:
        mp3_file = MP3(file)
        duration = mp3_file.info.length
        mixer.music.stop()
        mixer.music.load(file)
        mixer.music.play()
        
    return duration
        
def find_weather():
    w = observation.get_weather()
    weather_dict = w.get_temperature('fahrenheit')
    weather_dict["status"] = w.get_detailed_status()
    weather_dict["temp"] = round(weather_dict["temp"])
    return weather_dict        
    
    
def play_answer(text):
    language = "en"   
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("temp.mp3")
    sleep_time = respond("temp.mp3")
    time.sleep(sleep_time)
    mixer.music.load("empty.mp3")
    os.remove("temp.mp3")    

def processText(text):
    commands = ["lights on", "lights off", "lamp on", "lamp off", "play music", "volume up", "volume down", "stop music", "exit script", "weather"]
    maxScore = 0
    z = 0
    for command in commands:
        score = fuzz.ratio(text, command)
        if score >= maxScore:
            maxScore = score
            action = z
        z=z+1
    print(action, maxScore)
    if maxScore > 0:
        return action
    else:
        return None    
        

play_answer("ready")

while 1: 
    response = None
    action = None
    if reading == False:
        speech = listen(0.5)

    if re.search('mom', str(speech), re.IGNORECASE):
       reading = True

    
    if reading == True:
        tempVolume = mixer.music.get_volume()
        mixer.music.set_volume(0.1)
        pi.write(26,1)
        speech = listen(1)
        mixer.music.set_volume(tempVolume)
        action = processText(speech)
        pi.write(26,0)
        reading = False
        if action == None:
            play_answer("Sorry I did not understand")
  
    if action != None:
        if action == 0:
            response = "LightsOn.wav"
            tx.put("l")
        if action == 1:
            response = "LightsOff.wav"
            tx.put("l")
        if action == 2:
            response = "LampOn.wav"
            tx.put("o")
        if action == 3:
            response = "LampOff.wav"
            tx.put("o")
        if action == 4:
            PlayingMusic = True
        if action == 5:
            x += 0.2
            volume = x**2
            mixer.music.set_volume(volume)
        if action == 6:
            x -= 0.2
            volume = x**2
            mixer.music.set_volume(volume)
        if action == 7:
            PlayingMusic = False
            mixer.music.stop()
        if action == 8:
            exit()
        if action == 9:
            wr = find_weather()
            play_answer("The temperature is {0} and the weather is {1}".format(wr["temp"], wr["status"])) 
            
    if response != None:
        respond(response)
    if speech != None:
        print(speech)        

    if PlayingMusic == True and mixer.music.get_busy() == False:
        songs = [f for f in os.listdir(MusicDir) if not f.startswith('desk')]
        random.shuffle(songs)
        firstSong = songs[0]
        mixer.music.load(os.path.join(MusicDir, firstSong))
        mixer.music.play()
        for song in songs:
            if song == firstSong:
                continue
            mixer.music.queue(os.path.join(MusicDir, song))
            mixer.music.play() 