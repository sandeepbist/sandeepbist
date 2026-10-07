"""Render a pixel battle over the real GitHub contribution calendar."""

from pathlib import Path
from datetime import date
from math import sin, cos, pi, atan2
from random import Random
import argparse
import importlib.util
import json
import os
import re
from urllib.request import Request, urlopen
from PIL import Image, ImageDraw, ImageChops

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location("retro",ROOT/"source/build-retro.py")
retro=importlib.util.module_from_spec(spec)
spec.loader.exec_module(retro)


def validate(payload):
    if payload.get("errors"):
        raise ValueError("GitHub rejected the calendar query")
    calendar=payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks=calendar["weeks"]
    if not 1<=len(weeks)<=54:
        raise ValueError("Invalid contribution calendar length")
    seen=set()
    for week in weeks:
        for day in week["contributionDays"]:
            date.fromisoformat(day["date"])
            if day["date"] in seen or not isinstance(day["contributionCount"],int) or day["contributionCount"]<0:
                raise ValueError("Invalid contribution day")
            if day["weekday"] not in range(7):
                raise ValueError("Invalid calendar weekday")
            seen.add(day["date"])
    return calendar


def fetch(username):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}",username):
        raise ValueError("Invalid GitHub username")
    token=os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Set GH_TOKEN or GITHUB_TOKEN to refresh contributions")
    query='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel weekday}}}}}}'
    request=Request("https://api.github.com/graphql",data=json.dumps({"query":query,"variables":{"login":username}}).encode(),headers={"Authorization":"Bearer "+token,"Content-Type":"application/json","User-Agent":"retro-profile-calendar"})
    with urlopen(request,timeout=30) as response:
        payload=json.load(response)
    validate(payload)
    return payload


def targets(calendar, seed=None):
    cells=[]
    for column,week in enumerate(calendar["weeks"]):
        for day in week["contributionDays"]:
            if day["contributionCount"]:
                cells.append((column,day["weekday"],day))
    if not cells:
        return []
    number=min(16,len(cells))
    random=Random(seed if seed is not None else date.today().isoformat())
    selected=random.sample(cells,number)
    strongest=max(cells,key=lambda item:item[2]["contributionCount"])
    if strongest not in selected:
        selected[-1]=strongest
    random.shuffle(selected)
    return selected


def cell_position(column,row,mobile=False):
    if mobile:
        group=column//14
        return 82+(group%2)*144+(column%14)*8,56+(group//2)*87+row*8
    return 150+column*8,61+row*10


def base(calendar,mobile=False):
    image=Image.new("RGBA",(360,280) if mobile else (600,200))
    draw=ImageDraw.Draw(image)
    draw.rectangle((0,0,359 if mobile else 599,239 if mobile else 153),fill=(9,13,29,230))
    retro.text(draw,(13 if mobile else 22,11),"CONTRIBUTIONS",16 if mobile else 21)
    count=f'{calendar["totalContributions"]:,}'
    count_width=draw.textlength(count,font=retro.font(18 if mobile else 23))
    retro.text(draw,((345 if mobile else 578)-count_width,10),count,18 if mobile else 23,"#8bdadb")
    if mobile:
        for group in range(4):
            x,y=cell_position(group*14,0,True)
            draw.rectangle((x-5,y-5,x+111,y+58),fill=(11,21,37,255),outline="#30405b")
            weeks=calendar["weeks"][group*14:(group+1)*14]
            if weeks:
                first=date.fromisoformat(weeks[0]["contributionDays"][0]["date"])
                last=date.fromisoformat(weeks[-1]["contributionDays"][-1]["date"])
                retro.text(draw,(x,y-17),first.strftime("%b").upper()+" - "+last.strftime("%b").upper(),8,"#8ca5ba")
    else:
        draw.rectangle((143,54,585,134),fill=(11,21,37,255),outline="#30405b")
    month=None
    for column,week in enumerate(calendar["weeks"]):
        for day in week["contributionDays"]:
            x,y=cell_position(column,day["weekday"],mobile)
            amount=day["contributionCount"]
            color="#1e3045" if amount==0 else "#2d6175" if amount<3 else "#489da8" if amount<8 else "#9a88d2" if amount<25 else "#ffb391"
            draw.rectangle((x,y,x+5,y+(5 if mobile else 6)),fill=color)
        if week["contributionDays"] and not mobile:
            value=date.fromisoformat(week["contributionDays"][0]["date"])
            if value.month!=month:
                retro.text(draw,(150+column*8,40),value.strftime("%b").upper(),8,"#8ca5ba")
                month=value.month
    retro.text(draw,(14 if mobile else 23,185 if mobile else 44),"P1",11,"#8bdadb")
    retro.text(draw,(13 if mobile else 22,252 if mobile else 177),"DAILY CONTRIBUTIONS = DAMAGE",8 if mobile else 9,"#9bb6c7")
    return image


def render(calendar,chosen,mobile=False):
    count=max(1,len(chosen))*12
    directory=ROOT/"source/retro-frames"/("battle-mobile" if mobile else "battle")
    directory.mkdir(parents=True,exist_ok=True)
    backdrop=base(calendar,mobile)
    for index in range(count):
        image=backdrop.copy()
        draw=ImageDraw.Draw(image)
        retro.fighter(draw,13 if mobile else 48,210 if mobile else 123,index//3)
        origin_x,origin_y=(47,224) if mobile else (82,137)
        upgraded=index>=48
        if 36<=index<48:
            progress=(index-36)/11
            retro.pickup(draw,origin_x+50*(1-progress),origin_y-13,index*pi/6)
        if upgraded:
            retro.text(draw,(17 if mobile else 54,197 if mobile else 107),"S",10,"#8bdadb")
        if chosen:
            column,row,day=chosen[index//12]
            tick=index%12
            tx,ty=cell_position(column,row,mobile)
            tx+=2;ty+=3
            # Projectile hits the same day whose exact count becomes damage.
            if tick<=5:
                progress=tick/5
                x,y=origin_x+(tx-origin_x)*progress,origin_y+(ty-origin_y)*progress
                draw.line((x-5,y+1,x+3,y-1),fill="#fff1cb",width=2)
                # Side bolts fade before reaching cells; only the center hit has damage.
                if upgraded and tick<4:
                    angle=atan2(ty-origin_y,tx-origin_x)
                    length=((tx-origin_x)**2+(ty-origin_y)**2)**.5*progress
                    for spread in (-.15,.15):
                        sx=origin_x+cos(angle+spread)*length
                        sy=origin_y+sin(angle+spread)*length
                        draw.line((sx-cos(angle+spread)*5,sy-sin(angle+spread)*5,sx,sy),fill="#8bdadb",width=2)
                if tick<2:
                    draw.polygon(((origin_x-1,origin_y-3),(origin_x+7,origin_y),(origin_x-1,origin_y+4)),fill="#ffbd72")
            else:
                draw.rectangle((tx-2,ty-3,tx+4,ty+4),fill="#ffc08c" if tick<8 else "#8ed6d4")
                radius=2+(tick-5)*1.5
                for spoke in range(8):
                    angle=spoke*pi/4
                    x,y=tx+radius*cos(angle),ty+radius*sin(angle)
                    draw.rectangle((x,y,x+1,y+1),fill="#ffbe86")
                damage=str(day["contributionCount"])
                width=draw.textlength(damage,font=retro.font(16 if mobile else 19))
                x=max(79 if mobile else 149,min((342 if mobile else 576)-width,tx-width/2))
                retro.text(draw,(x,ty-20-(tick-6)*2),damage,16 if mobile else 19,"#ffd199")
            label=f'{day["date"]} / {day["contributionCount"]}'
            width=draw.textlength(label,font=retro.font(8 if mobile else 9))
            retro.text(draw,((345 if mobile else 578)-width,266 if mobile else 177),label,8 if mobile else 9,"#ffbea3")
        else:
            retro.text(draw,(190,142),"No contributions in this calendar yet",12,"#8ca5ba")
        image.save(directory/f"{index:03}.png")
    inputs=["-loop","1","-framerate","12","-i",str(ROOT/"source/retro-city.png"),"-framerate","12","-i",str(directory/"%03d.png")]
    composition="[0:v]scale=360:120:force_original_aspect_ratio=increase:flags=neighbor,crop=360:120,pad=360:280:0:150:color=0x090d1d" if mobile else "[0:v]scale=600:200:force_original_aspect_ratio=increase:flags=neighbor,crop=600:200"
    composition+="[background];[background][1:v]overlay=shortest=1,scale="+("720:560" if mobile else "1200:400")+":flags=neighbor"
    name="contributions-mobile-retro" if mobile else "contributions-retro"
    # The PNG shows a real hit and count as a useful reduced-motion alternative.
    retro.run(["-i",str(ROOT/"source/retro-city.png"),"-i",str(directory/"006.png" if chosen else directory/"000.png"),"-filter_complex",composition,"-frames:v","1",str(ROOT/"assets"/f"{name}.png")])
    retro.run(inputs+["-filter_complex",composition+",split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none","-frames:v",str(count),"-loop","0",str(ROOT/"assets"/f"{name}.gif")])
    with Image.open(ROOT/"assets"/f"{name}.gif") as image:
        assert image.n_frames==count and image.info["loop"]==0
        first=image.convert("RGB")
        image.seek(min(6,count-1))
        assert ImageChops.difference(first,image.convert("RGB")).getbbox() or count==1
        for index in range(count):
            image.seek(index);image.load()
        duration=sum(image.seek(index) or image.info["duration"] for index in range(count))
        assert abs(duration-count/12*1000)<=100, duration
    return [{"date":day["date"],"damage":day["contributionCount"]} for _,_,day in chosen]


def self_check():
    payload=json.loads((ROOT/"source/contributions.json").read_text())
    calendar=validate(payload)
    actual={day["date"]:day["contributionCount"] for week in calendar["weeks"] for day in week["contributionDays"]}
    chosen=targets(calendar,"check-a")
    assert all(day["contributionCount"]==actual[day["date"]]>0 for _,_,day in chosen)
    assert chosen==targets(calendar,"check-a")
    assert len({day["date"] for _,_,day in chosen})==len(chosen)
    assert max(day["contributionCount"] for _,_,day in chosen)==max(actual.values())
    if len(actual)>16:
        assert chosen!=targets(calendar,"check-b")
    assert len(targets({"weeks":[{"contributionDays":[]}]}))==0
    for column,week in enumerate(calendar["weeks"]):
        for day in week["contributionDays"]:
            x,y=cell_position(column,day["weekday"],True)
            assert 0<=x<x+5<360 and 0<=y<y+5<240
    assert len({cell_position(column,day["weekday"],True) for column,week in enumerate(calendar["weeks"]) for day in week["contributionDays"]})==len(actual)
    invalid=json.loads(json.dumps(payload))
    invalid["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"][0]["contributionDays"][0]["contributionCount"]=-1
    try:
        validate(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid counts accepted")
    print("Calendar validation, seeded target shuffle, exact damage, and empty-calendar checks passed")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--username",default="sandeepbist")
    parser.add_argument("--refresh",action="store_true")
    parser.add_argument("--check",action="store_true")
    options=parser.parse_args()
    if options.check:
        self_check()
    else:
        payload=fetch(options.username) if options.refresh else json.loads((ROOT/"source/contributions.json").read_text())
        calendar=validate(payload)
        seed=date.today().isoformat()
        chosen=targets(calendar,seed)
        hits=render(calendar,chosen)
        assert render(calendar,chosen,mobile=True)==hits
        # Save fetched data only after rendering succeeds.
        if options.refresh:
            (ROOT/"source/contributions.json").write_text(json.dumps(payload,indent=2)+"\n")
        (ROOT/"source/battle-hits.json").write_text(json.dumps({"username":options.username,"totalContributions":calendar["totalContributions"],"shuffleSeed":seed,"weaponUpgradeAfterHits":4,"hits":hits},indent=2)+"\n")
        print(f'Rendered {len(hits)} hits from {calendar["totalContributions"]:,} real contributions')
