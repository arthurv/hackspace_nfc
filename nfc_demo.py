import nxppy
import time
import sys
import signal
import pygame
from pygame.locals import *

import os

mifare = nxppy.Mifare()

f = open("user_list.csv",'r')

user_hash = {}

for line in f:
    user_hash[line.split(',')[0]] = line.split(',')[1].strip()
f.close()
def signal_term_handler(signum = None, frame = None):
    sys.stderr.write("Terminated.\n")
    f.close()
    sys.exit(0)

for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]: 
    signal.signal(sig, signal_term_handler)

screen = None;

#"Ininitializes a new pygame screen using the framebuffer"
# Based on "Python GUI in Linux frame buffer"
# http://www.karoltomala.com/blog/?p=679
disp_no = os.getenv("DISPLAY")
if disp_no:
    print "I'm running under X display = {0}".format(disp_no)

# Check which frame buffer drivers are available
# Start with fbcon since directfb hangs with composite output
drivers = ['fbcon']
found = False
for driver in drivers:
    # Make sure that SDL_VIDEODRIVER is set
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True
    break

if not found:
    raise Exception('No suitable video driver found!')

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print "Framebuffer size: %d x %d" % (size[0], size[1])
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
# Clear the screen to start
screen.fill((0, 0, 255))        
# Initialise font support
pygame.font.init()
# Render the screen
pygame.display.update()


uid = None
# Get a font and use it render some text on a Surface.
font = pygame.font.Font(None, 80)
while 1:
    for event in pygame.event.get():
        try:
            if event.key == K_ESCAPE:
                sys.exit()
        except AttributeError:
            pass
    #clear the screen
    pygame.mouse.set_visible(False) #hide the mouse cursor
    screen.fill((255, 255, 255))
    # Render the hackspace logo at 400,160
    logo = pygame.image.load('logo1.1_300_trans.png').convert()
    screen.blit(logo, (400, 160))     
    # Render some text with a background color
    datestr = time.strftime("%A, %d %b %Y", time.localtime())
    text_surface = font.render(datestr,
        True, (0, 0, 0))
    # Blit the text
    screen.blit(text_surface, (10, 30))            
    timestr = time.strftime("%H:%M:%S", time.localtime())
    text_surface = font.render(timestr,
        True, (0, 0, 0))
    # Blit the text
    screen.blit(text_surface, (20, 90))
    # Update the display
    pygame.display.update()
    try:
        uid = mifare.select()
    except nxppy.SelectError:
        pass
    if uid is not None:
        #print "Card detected:", uid
        if uid in user_hash.keys():
            text_surface = font.render("Hello",
                True, (0, 0, 0))
            screen.blit(text_surface, (20, 210))                    
            text_surface = font.render(user_hash[uid],
                True, (0, 0, 0))
            screen.blit(text_surface, (20, 270))
        else:
            text_surface = font.render("Unknown card",
                True, (0, 0, 0))
            screen.blit(text_surface, (20, 210))                    
            text_surface = font.render("Please register",
                True, (0, 0, 0))
            screen.blit(text_surface, (20, 270))
        uid = None #reset uid to None
        pygame.display.update()
        time.sleep(1) #pause for 1 seconds
    time.sleep(1)
#get out of full screen
#size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
pygame.quit()




