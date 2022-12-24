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

def main(location):
    print("Init Weather")
    W = weather.Weather("Sacramento,CA,US", "imperial")

    print(f"Weather: {W.get_weather()}")

    try:
        logging.info("epd5in65f Demo")
        
        epd = epd5in65f.EPD()
        logging.info("init and Clear")
        epd.init()
        #epd.Clear()
        font24 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 18)
        font40 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 40)
    
        Himage = Image.open(os.path.join(imgdir, '5in65f0.png'))
        Himage = Himage.resize((epd.width, epd.height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(Himage)

        date_msg = date.today().strftime("%A, %d %B %Y")
        w, h = draw.textsize(date_msg, font=font40)
        draw.text(((epd.width-w)/2,0), date_msg, font = font40, fill=epd.BLACK)

        weather_msg = W.get_weather().capitalize()
        w, h = draw.textsize(weather_msg, font=font40)
        draw.text(((epd.width-w)/2,epd.height-h-10), weather_msg, font = font40, fill=epd.BLACK)

        epd.display(epd.getbuffer(Himage))
        #time.sleep(60)
        #epd.Clear()
        #epd.sleep()
        time.sleep(60)
    
        print("Start Loop")
        while True:
            w_dir = '/Misc/'
            W.update_weather()
            print(f"Weather: {W.get_weather()}")
            weather_msg = W.get_weather()
            if 'haze' in weather_msg:
                w_dir = '/Fog/'
            elif 'mist' in weather_msg:
                w_dir = '/Fog/'
            elif 'fog' in weather_msg:
                w_dir = '/Fog/'
            elif 'smoke' in weather_msg:
                w_dir = '/Fog/'
            elif 'dust' in weather_msg:
                w_dir = '/Dust/'
            elif 'sand' in weather_msg:
                w_dir = '/Dust/'
            elif 'ash' in weather_msg:
                w_dir = '/Dust/'
            elif 'thunder' in weather_msg:
                w_dir = '/Thunderstorm/'
            elif 'drizzle' in weather_msg:
                w_dir = '/Rain/'
            elif 'rain' in weather_msg:
                w_dir = '/Rain/'
            elif 'cloud' in weather_msg:
                w_dir = '/Clouds/'
            elif 'clear' in weather_msg:
                w_dir = '/Clear/'
            elif 'snow' in weather_msg:
                w_dir = '/Snow/'

            if random.randint(0,100) > 50:
                w_dir = '/Misc/'

            imgs = os.listdir(imgdir + w_dir)
            print(imgs)
            img = Image.open(imgdir + w_dir +  random.choice(imgs))
            img = img.resize((epd.width, epd.height), Image.ANTIALIAS)
            draw = ImageDraw.Draw(img)

            date_msg = date.today().strftime("%A, %d %B %Y")
            w, h = draw.textsize(date_msg, font=font40)
            draw.text(((epd.width-w)/2,0), date_msg, font = font40, fill=epd.BLACK)

            weather_msg = W.get_weather().capitalize()
            w, h = draw.textsize(weather_msg, font=font40)
            draw.text(((epd.width-w)/2,epd.height-h-10), weather_msg, font = font40, fill=epd.BLACK)

            epd.display(epd.getbuffer(img))
            #epd.sleep()
            time.sleep(60)
    
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()

if __name__ == '__main__':
    main(sys.argv[1])
