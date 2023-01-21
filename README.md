PiClock Advanced / Studio Infoscreen
================
Clock / Infoscreen for radiostudios  
Basically this is just a modified and extended Version of this one: (https://github.com/jdgwarren/pirsclockfull)

## Description - what does this thing?

You can see a clock with the typical LED ring for the seconds and some areas for signalisation of different things like mic, phone, door or whatever you want. You can configure the text and the colors the indicators will light up with easily on your own. 

If the mic is open, a talk timer ist counting up. It stops as soon as the mic is closed. If the mic is opened again, the timer will be reset and starts counting up again. Good to avoid those talks from hell ;)  
In the top left corner there is an indicator, that could show which studio or source is currently broadcasting. In our case we get this information from the audio router. If the on air source corresponds with the studio the current infoscreen is associated to, the colour changes from red font on black backgound to white font on red background. But this is configurable. So you see clearly if the Studio you are in is the on air studio. And if not, you see which studio is the on air studio but in a more subtle color.  
On the bottom you can show the song information of the song that ist currently playing, or also something else. You just have to set the right path.
Both information, the onair info and the song info is polled from textfiles. I'm still testing if the constantly reading of the files is a problem. Maybe there is a better solution. Currently those two files are being read multiple times a second. There must be a better solution... ;)<br />
**Update:**<br />
Yes there is a better solution. If you set the variable "useudpbroadcast" to True, the constantly polling of the textfiles is switched off. There is just one poll after startup. After that the script i waiting for UDP broadcast messages. We generate them with a powershell script. You will find it in the repo as well.<br />
Why UDP broadcast? It was the easiest way to get the message to multiple displays. And it runs much more stable that the file polling method. The clock often used to hang. This seems not to happen with the UDP method.

Currently there could also be found an indicator named "Pegel" in the code which is german for "level". In this case audio level of course. It has no function yet and is commented out. Maybe it's possible to get the audio level of the associated studio via a small USB soundcard and let the indicator light up if the audio level is to high. The soundprocessing doesn't like getting driven with too much input level. I haven't looked into that, but would be nice.
But you can also use it as a 4th indicator with one of the GPIs, no problem, the code is still there.

## Some pictures

YAY, I finally made some pictures of the Infoscreen, so you can get an impression of that thingy:

This is the screen in our Studio 2 when it is off air:
![Studio 2 offair](/pictures/infoscreen_offair.jpg)
Current broadcasting source is "Loop/Zara".

This is the screen when Studio 2 is onair:
![Studio 2 onair](/pictures/infoscreen_onair.jpg)
See also the change of the songinfo on the bottom. When the broadcasting source changes, also the source of the songinfo changes. But that is handeled in the audio router, the infoscrren is just showing the result.

Here the mic is on and the mic timer is running:
![Studio 2 Mic on](/pictures/infoscreen_mic.jpg)

Someone is calling on the phone:
![Studio 2 phone ringing](/pictures/infoscreen_tel.jpg)
Here you also can see the stopped mic timer when mic is closed.

The TÜR (door) indicator would light up in blue, but I was too lazy and it was cold outside ;) And the colour is configurable anyway.
Of course all the indicators can light up simultaneuosly.
