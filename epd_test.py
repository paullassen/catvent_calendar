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

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd5in65f Demo")
    
    epd = epd5in65f.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    font24 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 18)
    font40 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 40)

    Himage = Image.open(os.path.join(imgdir, '5in65f0.png'))
    Himage = Himage.rotate(90)
    Himage = Himage.resize((epd.height, epd.width), Image.ANTIALIAS)
    epd.display(epd.getbuffer(Himage))
    time.sleep(60)
    epd.Clear()
    epd.sleep()


except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in65f.epdconfig.module_exit()
    exit()
