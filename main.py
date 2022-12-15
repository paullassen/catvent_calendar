#! /usr/bin/env python3

from lib import weather

def main():
    w = weather.Weather("Sacramento,CA,US", "imperial")
    print(f'{w.get_weather()}')

if __name__ == '__main__':
    main()
