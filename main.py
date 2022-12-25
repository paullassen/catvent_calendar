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
    W = weather.Weather(location, "imperial")

    print(f"Weather: {W.get_weather()}")

    try:
        logging.info("epd5in65f Demo")
        
        epd = epd5in65f.EPD()
        logging.info("init and Clear")
        epd.init()

        font24 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 18)
        font40 = ImageFont.truetype(os.path.join(imgdir, 'Font.ttc'), 40)

        cond = 'Misc'
        file_dict = {}
        for d in os.listdir(imgdir):
            if os.path.isdir(imgdir + '/' + d):
                d_str = imgdir + '/' + d + '/'
                file_dict[d] = [(d_str+f) for f in os.listdir(d_str) if os.path.isfile(d_str+f)]

        print("Start Loop")
        while True:
            W.update_weather()
            print(f"Weather: {W.get_weather()}")
            weather_msg = W.get_weather()
            if 'haze' in weather_msg:
                cond = 'Fog'
            elif 'mist' in weather_msg:
                cond = 'Fog'
            elif 'fog' in weather_msg:
                cond = 'Fog'
            elif 'smoke' in weather_msg:
                cond = 'Fog'
            elif 'dust' in weather_msg:
                cond = 'Dust'
            elif 'sand' in weather_msg:
                cond = 'Dust'
            elif 'ash' in weather_msg:
                cond = 'Dust'
            elif 'thunder' in weather_msg:
                cond = 'Thunderstorm'
            elif 'drizzle' in weather_msg:
                cond = 'Rain'
            elif 'rain' in weather_msg:
                cond = 'Rain'
            elif 'cloud' in weather_msg:
                cond = 'Clouds'
            elif 'clear' in weather_msg:
                cond = 'Clear'
            elif 'snow' in weather_msg:
                cond = 'Snow'

            if random.randint(0,100) > 50:
                if random.randint(0,100) < 80:
                    cond = 'Misc'
                else:
                    cond = 'All'


            r_img = ''
            print(f"Condition: {cond}")
            if cond == 'All':
                imgset = random.choice(list(file_dict.keys()))
                r_img = random.choice(file_dict[imgset])
            else:
                r_img = random.choice(file_dict[cond])
            print(r_img)
            img = Image.open(r_img)
            img = img.resize((epd.width, epd.height), Image.ANTIALIAS)
            draw = ImageDraw.Draw(img)

            date_msg = date.today().strftime("%A, %d %B %Y")
            w, h = draw.textsize(date_msg, font=font40)
            draw.text(((epd.width-w)/2,0), date_msg, font = font40, fill=epd.BLACK, stroke_width=1, stroke_fill=epd.WHITE)

            weather_msg = W.get_weather().capitalize()
            w, h = draw.textsize(weather_msg, font=font40)
            draw.text(((epd.width-w)/2,epd.height-h-10), weather_msg, font = font40, fill=epd.BLACK,stroke_width=1, stroke_fill=epd.WHITE)

            epd.display(epd.getbuffer(img))
            #epd.sleep()
            time.sleep(60)
    
    except IOError as e:
        print(e)
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()

if __name__ == '__main__':
    main(sys.argv[1])
