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
import random

from lib import weather

def main():
    print("Init Weather")

    try:
        logging.info("epd5in65f Demo")
        
        epd = epd5in65f.EPD()
        logging.info("init and Clear")
        epd.init()

        dirs = [('/'+d+'/') for d in os.listdir(imgdir) if os.path.isdir(imgdir + '/' + d)]
        for d in dirs:
            idir = imgdir + d
            for i in os.listdir(idir):
                print(idir+i)
                img = Image.open(idir+i)
                img = img.resize((epd.width, epd.height), Image.ANTIALIAS)
                epd.display(epd.getbuffer(img))
                time.sleep(30)

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()

if __name__ == '__main__':
    main()
