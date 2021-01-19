#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame , sys , math, time, os, codecs
import RPi.GPIO as GPIO
from pygame.locals import *
os.environ['SDL_VIDEODRIVER']="fbcon"

# Setting up the GPIO and inputs with pull up
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, GPIO.PUD_UP)

pygame.init()
bg = pygame.display.set_mode()
mictimer_time = 0
mictimer_started = False
mictimer_starttime = 0
studtext="Studio 2" #define studio, where infoscreen is installed
songfilepath="/mnt/rds/now-onair.txt"
onairstudiofilepath="/mnt/rds/onair-studio.txt"
pygame.mouse.set_visible(False)

# Change colour to preference (R,G,B) 255 max value
bgcolour       = (0,   0,   0  )
clockcolour    = (255, 0,   0  )
ind1colour     = (255, 0,   0  )
ind2colour     = (255, 0,   0  )
ind3colour     = (0,   255, 0  )
ind4colour     = (0,   255, 255)
offcolour      = (15,  15,  15 )
timercolour    = (210, 210, 210)
txtcolour      = (210, 210, 210)
onaircolour    = (255, 0,   0  )

# Scaling to the right size for the display
digiclocksize  = int(bg.get_height()/5)
digiclocksizesec  = int(bg.get_height()/8)
digiclockspace = int(bg.get_height()/6)
dotsize        = int(bg.get_height()/110)
hradius        = bg.get_height()/3
secradius      = hradius - (bg.get_height()/26)
indtxtsize     = int(bg.get_height()/7)
txtsize        = int(bg.get_height()/10)
onairtxtsize   = int(bg.get_height()/10)
infotxtsize   = int(bg.get_height()/15)
indboxy        = int(bg.get_height()/6)
indboxx        = int(bg.get_width()/4)
onairstudboxy  = int(bg.get_height()/9)
onairstudboxx  = int(bg.get_width()/3.5)

# Coords of items on display
xclockpos      = int(bg.get_width()*0.5)
ycenter        = int(bg.get_height()/2)
xtxtpos        = int(bg.get_width()*0.85)
xtxtpos_left   = int(bg.get_width()*0.14)     
xindboxpos     = int(xtxtpos-(indboxx/2))
xindboxpos_left= int(xtxtpos_left-(indboxx/2))
xonairstudtxt  = int (bg.get_width()*0.1)
xonairstudbox  = int(xonairstudtxt-(onairstudboxx/2.9))
yonairstudbox  = int((ycenter*0.14)-(onairstudboxy/2))
ind1y          = int((ycenter*0.4)-(indboxy/2))  #pegel     
ind2y          = int((ycenter*0.8)-(indboxy/2))  #mic
ind3y          = int((ycenter*0.8)-(indboxy/2))  #tel 
ind4y          = int((ycenter*1.2)-(indboxy/2))  #tür
txthmy         = int(ycenter)
txtsecy        = int(ycenter+digiclockspace)
studioposx     = int(bg.get_width()*0.5)
studioposy     = int(bg.get_height()*0.07)
onairstudposx  = int(bg.get_width()*0.014)
onairstudposy  = int(bg.get_height()*0.07)
songposx       = int(bg.get_width()*0.5)
songposy       = int(bg.get_height()*0.94)

# Fonts  
clockfont     = pygame.font.Font(None,digiclocksize)
clockfontsec  = pygame.font.Font(None,digiclocksizesec)
indfont       = pygame.font.Font(None,indtxtsize)
txtfont       = pygame.font.Font(None,txtsize)
onairfont     = pygame.font.Font(None, onairtxtsize)
infofont      = pygame.font.Font(None, infotxtsize)

# Indicator text - edit text in quotes to desired i.e. "MIC" will show MIC on display
doortext = u"TÜR" # umwandlung in utf-8 wegen Umlaut
ind1txt       = indfont.render("PEGEL",True,bgcolour)
ind2txt       = indfont.render("MIC",True,bgcolour)
ind3txt       = indfont.render("TEL",True,bgcolour)
ind4txt       = indfont.render(doortext,True,bgcolour)
timer         = indfont.render(str(mictimer_time),True,timercolour)
studio        = txtfont.render(studtext,True,txtcolour)
onairstudio   = onairfont.render(studtext,True,onaircolour)
songinfo      = infofont.render("test",True,txtcolour)

# Indicator positions
txtposind1 = ind1txt.get_rect(centerx=xtxtpos,centery=ycenter*0.4)
txtposind2 = ind2txt.get_rect(centerx=xtxtpos_left,centery=ycenter*0.8)
txtposind3 = ind3txt.get_rect(centerx=xtxtpos,centery=ycenter*0.8)
txtposind4 = ind4txt.get_rect(centerx=xtxtpos,centery=ycenter*1.2)
timerpos   = timer.get_rect(centerx=xtxtpos_left*0.67,centery=ycenter*1.2)
studiopos  = studio.get_rect(centerx=studioposx,centery=studioposy)
onairstudpos= onairstudio.get_rect(left=onairstudposx,centery=onairstudposy)
songpos    = songinfo.get_rect(centerx=songposx,centery=songposy)

# Parametric Equations of a Circle to get the markers
# 90 Degree ofset to start at 0 seconds marker
# Equation for second markers
def paraeqsmx(smx):
    return xclockpos-(int(secradius*(math.cos(math.radians((smx)+90)))))

def paraeqsmy(smy):
    return ycenter-(int(secradius*(math.sin(math.radians((smy)+90)))))

# Equations for hour markers
def paraeqshx(shx):
    return xclockpos-(int(hradius*(math.cos(math.radians((shx)+90)))))

def paraeqshy(shy):
    return ycenter-(int(hradius*(math.sin(math.radians((shy)+90)))))


def readsonginfo():
    try:
        #songfile=codecs.open(songfilepath, "r", "utf-8")
        songfile=open(songfilepath, 'r', encoding='utf-8-sig')
        contents = songfile.read()
        songfile.close()
    except IOError:
        contents = "Kann Songinfo-File nicht lesen!"    
    return contents.strip('\n')

def readonairstudio():
    try:
        #onairstudfile=codecs.open(onairstudiofilepath, "r", "utf-8")
        onairstudfile=open(onairstudiofilepath, "r")
        contents = onairstudfile.read()
        onairstudfile.close()
    except IOError:
        contents = "Kann OnAir-Studio-File nicht lesen!"
    return contents.strip('\n')

# This is where pygame does its tricks
while True :
    pygame.display.update()

    bg.fill(bgcolour)

    # Retrieve seconds and turn them into integers
    sectime = int(time.strftime("%S",time.localtime(time.time())))

    # To get the dots in sync with the seconds
    secdeg  = (sectime+1)*6

    # Draw second markers
    smx=smy=0
    while smx < secdeg:
        pygame.draw.circle(bg, clockcolour, (paraeqsmx(smx),paraeqsmy(smy)),dotsize)
        smy += 6  # 6 Degrees per second
        smx += 6

    # Draw hour markers
    shx=shy=0
    while shx < 360:
        pygame.draw.circle(bg, clockcolour, (paraeqshx(shx),paraeqshy(shy)),dotsize)
        shy += 30  # 30 Degrees per hour
        shx += 30

    # Retrieve time for digital clock
    retrievehm    = time.strftime("%H:%M",time.localtime(time.time()))
    retrievesec   = time.strftime("%S",time.localtime(time.time()))

    digiclockhm   = clockfont.render(retrievehm,True,clockcolour)
    digiclocksec  = clockfontsec.render(retrievesec,True,clockcolour)

    # Align it
    txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)
    txtpossec     = digiclocksec.get_rect(centerx=xclockpos,centery=txtsecy)

    # Function for the indicators
   # if GPIO.input(11): #pegel currently not used
    #    pygame.draw.rect(bg, offcolour,(xindboxpos, ind1y, indboxx, indboxy))
    #else:
     #   pygame.draw.rect(bg, ind1colour,(xindboxpos, ind1y, indboxx, indboxy))

    if GPIO.input(12): #mic
        pygame.draw.rect(bg, offcolour,(xindboxpos_left, ind2y, indboxx, indboxy))
        mictimer_started = False # stop mictimer
    else:
        pygame.draw.rect(bg, ind2colour,(xindboxpos_left, ind2y, indboxx, indboxy))
        if  mictimer_started == False: # if mictime is not running get current time and set mictimer running
                mictimer_starttime = pygame.time.get_ticks()
                mictimer_started = True
        

    if GPIO.input(13): #tel
        pygame.draw.rect(bg, offcolour,(xindboxpos, ind3y, indboxx, indboxy))
    else:
        pygame.draw.rect(bg, ind3colour,(xindboxpos, ind3y, indboxx, indboxy))

    if GPIO.input(15): #tür
        pygame.draw.rect(bg, offcolour,(xindboxpos, ind4y, indboxx, indboxy))
    else:
        pygame.draw.rect(bg, ind4colour,(xindboxpos, ind4y, indboxx, indboxy))
    
    # Mictimer countup if started (current time minus starttime)
    if mictimer_started:
        mictimer_time = pygame.time.get_ticks() - mictimer_starttime

    # Write timer and convert from ms in s, and from s in mm:ss
    timer = indfont.render(time.strftime('%M:%S', time.gmtime(mictimer_time/1000)),True,timercolour)

    # Update songinfo
    songinfo = infofont.render(str(readsonginfo()),True,txtcolour)
    songpos    = songinfo.get_rect(centerx=songposx,centery=songposy)

    # Update onairstudio and change backgound and font colours according to onairstudio
    onairinfo = str(readonairstudio())
    if onairinfo == studtext:
        pygame.draw.rect(bg, onaircolour,(xonairstudbox, yonairstudbox, onairstudboxx, onairstudboxy))
        onairstudio = onairfont.render(onairinfo + " OnAir",True,txtcolour)
    else:
        pygame.draw.rect(bg, bgcolour,(xonairstudbox, yonairstudbox, onairstudboxx, onairstudboxy))
        onairstudio = onairfont.render(onairinfo + " OnAir",True,onaircolour)

    
    # Render the text
    bg.blit(digiclockhm, txtposhm)
    bg.blit(digiclocksec, txtpossec)
    #bg.blit(ind1txt, txtposind1) #pegel currently not used
    bg.blit(ind2txt, txtposind2) #mic
    bg.blit(ind3txt, txtposind3) #tel
    bg.blit(ind4txt, txtposind4) #tür
    bg.blit(timer, timerpos)
    bg.blit(studio, studiopos)
    bg.blit(onairstudio, onairstudpos)
    bg.blit(songinfo, songpos)
    
    time.sleep(0.04)
    pygame.time.Clock().tick(25)
    for event in pygame.event.get() :
        if event.type == QUIT:
            pygame.quit()
            GPIO.cleanup()
            sys.exit()
        # Pressing q+t to exit
        elif event.type == KEYDOWN:
            if event.key == K_q and K_t:
                pygame.quit()
                GPIO.cleanup()
sys.exit()
