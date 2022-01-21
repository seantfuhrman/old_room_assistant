import speech_recognition as sr
import os, time, random, wave, contextlib, re, pyowm
from gtts import gTTS
from pygame import mixer
from datetime import datetime
from mutagen.mp3 import MP3
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
#from pixel_ring import pixel_ring


r = sr.Recognizer()
mic = sr.Microphone()
language = 'en'
mixer.init()
x = 0.5
PlayingMusic = False
reading = False

MusicDir = "Music"
HomeDir = ""

owm = pyowm.OWM('0370ddfb83dfbb13c6c688d8a2cd5d1c')
observation = owm.weather_at_coords(40.5123,-74.8593)


def listen (): 
    with mic as source:
        audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=2)
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
    time.sleep(sleep_time + 0.1)
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
    return action




while 1: 
    speech = listen()
    response = None
    action = None
    reading = False

    while reading == True:
        action = processText(speech)
        print("*")

    if re.search('mom', str(speech), re.IGNORECASE):
       print("listening")
       reading = True
  
    if action != None:
        reading = False
        if action == 0:
            response = "LightsOn.wav"
        if action == 1:
            response = "LightsOff.wav"
        if action == 2:
            response = "LampOn.wav"
        if action == 3:
            response = "LampOff.wav"
        if action == 4:
            PlayingMusic = True
        if action ==5:
            x += 0.2
            volume == x**2
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
        if action ==9:
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