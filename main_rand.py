import RPi.GPIO as GPIO
import random
import time
from pydub import AudioSegment
from pydub.playback import play


def add_sample(samp, t, n):
    for i in range(n):
        s = random.choices(t)
        if len(samp) == 0:
            samp.extend(s)
        elif len(samp) > 0 and s[0] != samp[-1]:
            samp.extend(s)
        else:
            i -= 1
    return samp


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pins = [26, 16, 6, 5, 25, 23, 27, 17]
pliki = {'c4': 'c4/C4.mp3', 'd4': 'c4/D4.mp3', 'e4': 'c4/E4.mp3', 'f4': 'c4/F4.mp3',
         'g4': 'c4/G4.mp3', 'a4': 'c4/A4.mp3', 'h4': 'c4/B4.mp3', 'c5': 'c4/C5.mp3'}
notes = ['c4', 'd4', 'e4', 'f4', 'g4', 'a4', 'h4', 'c5']
zielona = 2
czerwona = 3
GPIO.setup(zielona, GPIO.OUT)
GPIO.setup(czerwona, GPIO.OUT)
GPIO.output(zielona, 0)
GPIO.output(czerwona, 0)
for i in pins:
    GPIO.setup(i, GPIO.IN, GPIO.PUD_UP)
buttons = [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW]
sample = add_sample([], 5)
out = list()
punkty = 0
print('Playing C4 for scale')
song = AudioSegment.from_mp3('c4/C4.mp3')
play(song)
time.sleep(2.0)
for l in range(1, len(sample)+1):
    print('playing', l, 'notes')
    for i in sample[:l]:
        song = AudioSegment.from_mp3(pliki[i])
        play(song)

    while True:
        for i in range(8):
            buttons[i] = GPIO.input(pins[i])
        for i in range(8):
            if buttons[i] == GPIO.LOW:
                if (len(out) > 0 and out[-1] != notes[i]) or len(out) == 0:
                    song = AudioSegment.from_mp3(pliki[notes[i]])
                    play(song)
                    print(notes[i], 'pressed')
                    out.append(notes[i])

        if len(out) == len(sample):
            break

    if out == sample:
        print('dobrze!')
        GPIO.output(zielona, 1)
        punkty += 1
        sample = add_sample(sample, notes, 1)

    else:
        print('nie tym razem!\nSample: ', ' '.join([str(elem) for elem in sample]),
              '\nPlayed: ', ' '.join([str(elem) for elem in out]))
        GPIO.output(czerwona, 1)
        break

print(punkty)
