#! /usr/bin/env python3

import sys
import os

imgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'img')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd5in65f
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import date

from lib import weather

def main():
    try:
        logging.info("epd5in65f Demo")
        
        epd = epd5in65f.EPD()
        logging.info("init and Clear")
        epd.init()
        #epd.Clear()
        font24 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 18)
        font40 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 40)
        font80 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 70)
    
        Himage = Image.open(os.path.join(imgdir, 'Start_image.png'))
        Himage = Himage.resize((epd.width, epd.height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(Himage)

        xmas_msg = "Meowy Christmas!"
        w, h = draw.textsize(xmas_msg, font=font80)
        draw.text(((epd.width-w)/2,0), xmas_msg, font = font80, fill=epd.RED)

        ny_msg = "and a Happy New Year!"
        w, h = draw.textsize(ny_msg, font=font40)
        draw.text(((epd.width-w)/2,epd.height-h-20), ny_msg, font = font40, fill=epd.GREEN)

        epd.display(epd.getbuffer(Himage))
        #time.sleep(60)
        #epd.Clear()
        epd.sleep()
    
    
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()

if __name__ == '__main__':
    main()
