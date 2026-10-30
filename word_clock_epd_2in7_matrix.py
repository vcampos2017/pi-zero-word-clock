#!/usr/bin/env python3
"""10x11 word clock for Waveshare 2.7-inch monochrome e-paper."""
import time
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from lib.waveshare_epd import epd2in7

GRID=["ITLISASTIME","ACQUARTERDC","TWENTYFIVEX","HALFBTENFTO","PASTERUNINE","ONESIXTHREE","FOURFIVETWO","EIGHTELEVEN","SEVENTWELVE","TENSEOCLOCK"]
POS={"IT":(0,0,2),"IS":(0,3,2),"A":(0,5,1),"QUARTER":(1,2,7),"TWENTY":(2,0,6),"FIVE_M":(2,6,4),"HALF":(3,0,4),"TEN_M":(3,5,3),"TO":(3,9,2),"PAST":(4,0,4),"NINE":(4,7,4),"ONE":(5,0,3),"SIX":(5,3,3),"THREE":(5,6,5),"FOUR":(6,0,4),"FIVE_H":(6,4,4),"TWO":(6,8,3),"EIGHT":(7,0,5),"ELEVEN":(7,5,6),"SEVEN":(8,0,5),"TWELVE":(8,5,6),"TEN_H":(9,0,3),"OCLOCK":(9,5,6)}
HOURS={1:"ONE",2:"TWO",3:"THREE",4:"FOUR",5:"FIVE_H",6:"SIX",7:"SEVEN",8:"EIGHT",9:"NINE",10:"TEN_H",11:"ELEVEN",12:"TWELVE"}
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
def words_for_time(now):
    rounded=now+timedelta(minutes=2)
    minute=(rounded.minute//5)*5
    hour=rounded.hour%12 or 12
    next_hour=hour%12+1
    words=["IT","IS"]
    if minute==0: return words+[HOURS[hour],"OCLOCK"]
    if minute==15: return words+["A","QUARTER","PAST",HOURS[hour]]
    if minute==30: return words+["HALF","PAST",HOURS[hour]]
    if minute==45: return words+["A","QUARTER","TO",HOURS[next_hour]]
    amount=minute if minute<30 else 60-minute
    pieces={5:["FIVE_M"],10:["TEN_M"],20:["TWENTY"],25:["TWENTY","FIVE_M"]}[amount]
    return words+pieces+(["PAST",HOURS[hour]] if minute<30 else ["TO",HOURS[next_hour]])
def render(now):
    lit=set()
    for word in words_for_time(now):
        row,col,n=POS[word]
        lit.update((row,i) for i in range(col,col+n))
    img=Image.new("1",(264,176),1)
    draw=ImageDraw.Draw(img)
    font=ImageFont.truetype(FONT,17)
    for row,line in enumerate(GRID):
        for col,char in enumerate(line):
            x=8+col*22
            y=6+row*16
            if (row,col) in lit:
                draw.text((x,y),char,font=font,fill=0)
            else:
                # Dither inactive letters for a faint appearance.
                mask=Image.new("1",(22,16),1)
                ImageDraw.Draw(mask).text((0,0),char,font=font,fill=0)
                pixels=mask.load()
                for yy in range(16):
                    for xx in range(22):
                        if pixels[xx,yy]==0 and (xx+yy)%3==0:
                            draw.point((x+xx,y+yy),fill=0)
    return img
def main():
    epd=epd2in7.EPD()
    epd.init()
    last=None
    try:
        while True:
            now=datetime.now()
            rounded=now+timedelta(minutes=2)
            bucket=(rounded.year,rounded.month,rounded.day,rounded.hour,rounded.minute//5)
            if bucket!=last:
                epd.display(epd.getbuffer(render(now)))
                last=bucket
            time.sleep(5)
    finally:
        epd.sleep()
if __name__=="__main__":
    main()
