import time
from playsound import playsound

while True:
    i = input("Timer in seconds")
    try:
        i = int(i)
    except:
        pass
    for loop in range(i):
        print(i - loop)
        time.sleep(1)
    playsound('C:/Windows/Media/Alarm10.wav')


