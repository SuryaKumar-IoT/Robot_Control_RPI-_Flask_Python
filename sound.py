from time import *
from pygame import *
music_time=10
init()

def playsound():
	mixer.music.load('sound.mp3')
	mixer.music.play()
	sleep(music_time)
	mixer.music.fadeout(music_time)

#playsound()
