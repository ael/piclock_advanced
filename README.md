### PiClock Advanced
Clock / Infoscreen for radiostudios  
Basically this is just a modified and extended Version of this one: (https://github.com/jdgwarren/pirsclockfull)

You can see a clock with the typical LED ring for the seconds and some areas for signalisation of different things like mic, phone, door or whatever you want. You can configure the text and the colors the indicators will light up with easily on your own. 

If the mic is open, a talk timer ist counting up. It stops as soon as the mic is closed. If the mic is opened again, the timer will be reset and starts counting up again. Good to avoid those talks from hell ;)  
In the top left corner there is an indicator, that could show which studio or source is currently broadcasting. In our case we get this information from the audio router. If the on air source corresponds with the studio the current infoscreen is associated to, the colour changes from red font on black backgound to white font on red background. But this is configurable. So you see clearly if the Studio you are in is the on air studio. And if not, you see which studio is the on air studio but in a more subtle color.  
On the bottom you can show the song information of the song that ist currently playing, or also something else. You just have to set the right path.
Both information, the onair info and the song info is polled from textfiles. I'm still testing if the constantly reading of the files is a problem. Maybe there is a better solution. Currently those two files are being read multiple times a second. There must be a better solution... ;)

Currently there could also be found an indicator named "Pegel" in the code which is german for "level". In this case audio level of course. It has no function yet and is commented out. Maybe it's possible to get the audio level of the associated studio via a small USB soundcard and let the indicator light up if the audio level is to high. The soundprocessing doesn't like getting driven with too much input level. I haven't looked into that, but would be nice.
But you can also use it as a 4th indicator with one of the GPIs, no problem, the code is still there.


