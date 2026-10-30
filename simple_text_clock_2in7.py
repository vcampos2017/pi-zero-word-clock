#!/usr/bin/env python3
"""Plain-language and digital clock for Waveshare 2.7-inch e-paper."""
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from lib.waveshare_epd import epd2in7
WORDS=["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
TENS={20:"twenty",30:"thirty",40:"forty",50:"fifty"}
def number(n):
    if n<20:return WORDS[n]
    t=(n//10)*10
    return TENS[t]+("-"+WORDS[n%10] if n%10 else "")
def phrase(now):
    hour=now.hour%12 or 12
    period="in the morning" if 5<=now.hour<12 else "in the afternoon" if 12<=now.hour<17 else "in the evening" if 17<=now.hour<21 else "at night"
    if now.minute==0:return f"It is {number(hour)} o'clock {period}."
    return f"It is {number(hour)} {number(now.minute)} {period}."
def render(now):
    img=Image.new("1",(264,176),1)
    d=ImageDraw.Draw(img)
    large=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",38)
    small=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",18)
    digital=now.strftime("%I:%M %p").lstrip("0")
    d.text((10,10),digital,font=large,fill=0)
    d.line((10,62,254,62),fill=0)
    line=""
    y=72
    for word in phrase(now).split():
        test=(line+" "+word).strip()
        if d.textlength(test,font=small)>244 and line:
            d.text((10,y),line,font=small,fill=0)
            y+=24
            line=word
        else:line=test
    if line:d.text((10,y),line,font=small,fill=0)
    return img
def main():
    epd=epd2in7.EPD()
    epd.init()
    last=None
    try:
        while True:
            now=datetime.now()
            key=(now.year,now.month,now.day,now.hour,now.minute)
            if key!=last:
                epd.display(epd.getbuffer(render(now)))
                last=key
            time.sleep(2)
    finally:epd.sleep()
if __name__=="__main__":main()
