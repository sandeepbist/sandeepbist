"""Render original pixel animation layers and composite them with FFmpeg."""

from pathlib import Path
from math import sin, cos, pi
from random import Random
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FRAMES = ROOT / "source/retro-frames"
COUNT = 192
FPS = 12
PALETTE = {"ink": "#091020", "blue": "#377dbb", "light": "#8edfff", "skin": "#eec1a6", "hair": "#c9e0e6", "orange": "#ff876b", "white": "#faf0df"}


def font(size):
    face = ImageFont.truetype(str(ROOT / "source/PixelifySans.ttf"), size)
    face.set_variation_by_name("Bold")
    return face


def text(draw, position, value, size, color="#faf0df"):
    x, y = position
    draw.text((x+2, y+3), value, font=font(size), fill="#091020")
    draw.text((x, y), value, font=font(size), fill=color)


def fighter(draw, x, y, step):
    """Original blue-jacket runner: 29 by 33 native pixels."""
    def box(bounds, color):
        a,b,c,d = bounds
        draw.rectangle((x+a,y+b,x+c,y+d), fill=PALETTE.get(color,color))
    bob = step % 2
    y += bob
    # Coat tail and legs have four distinct running poses.
    draw.polygon([(x+5,y+13),(x-2,y+19),(x+5,y+19),(x+12,y+16)], fill=PALETTE["blue"])
    poses = ((3,25,12,29,11,29,18,32), (7,25,11,32,16,24,20,28), (5,24,13,28,0,29,7,32), (6,24,9,29,15,27,23,31))
    a,b,c,d,e,f,g,h = poses[step%4]
    box((a,b,c,d),"ink");box((e,f,g,h),"ink")
    box((a,b,c,b+2),"blue");box((e,f,g,f+2),"blue")
    box((c-3,d,c+2,d+1),"light");box((g-3,h,g+2,h+1),"light")
    box((6,12,17,24),"ink");box((7,13,16,22),"blue")
    box((8,13,10,21),"light");box((7,23,17,25),"ink")
    box((10,3,19,12),"ink");box((11,5,18,11),"skin")
    box((9,2,18,5),"hair");box((10,1,16,2),"hair")
    box((11,6,19,7),"orange");box((3,7,10,8),"orange")
    box((17,8,18,8),"ink")
    box((14,14,23,17),"skin");box((13,13,18,16),"blue")
    box((20,12,31,15),"ink");box((22,12,32,13),"light")
    box((21,16,23,19),"ink")


def drone(draw, x, y, phase):
    draw.rectangle((x-15,y-2,x+15,y+1),fill="#172b47")
    draw.rectangle((x-9,y-7,x+9,y+7),fill="#0b1426")
    draw.rectangle((x-7,y-5,x+7,y+4),fill="#6d6d91")
    draw.rectangle((x-4,y-3,x+4,y+2),fill="#fc8579")
    draw.rectangle((x-2,y-2,x+2,y),fill="#ffdcc4")
    draw.rectangle((x-11,y+5,x-8,y+10),fill="#b3c8db")
    draw.rectangle((x+8,y+5,x+11,y+10),fill="#b3c8db")
    flame = 3+int(2*(sin(phase)+1))
    draw.rectangle((x-4,y+8,x+4,y+8+flame),fill="#51c5d4")
    draw.rectangle((x-1,y+8,x+1,y+10+flame),fill="#d2f6fc")


def burst(draw, x, y, age, size=1):
    """Local impact particles; no full-screen flashing."""
    for spoke in range(12):
        angle=spoke*pi/6
        radius=(3+age*2)*size
        px,py=x+radius*cos(angle),y+radius*sin(angle)*0.7
        edge=max(1,4-age//4)
        draw.rectangle((px,py,px+edge,py+edge),fill="#ffc78a" if spoke%2 else "#8bdadb")
    if age<5:
        draw.rectangle((x-5+age,y-5+age,x+5-age,y+5-age),fill="#fff1cb")


def pickup(draw, x, y, phase):
    y+=int(2*sin(phase))
    draw.polygon(((x,y-10),(x+11,y),(x,y+10),(x-11,y)),fill="#13273b",outline="#8bdadb")
    text(draw,(x-5,y-8),"S",13,"#ffd199")
    for offset in (-4,0,4):
        draw.line((x+15,y,x+21,y+offset),fill="#8bdadb")


def boss(draw, x, y, phase, hit=False):
    """Original armored mech, 90 by 63 pixels, facing the player."""
    armor="#b3c8db" if hit else "#53617c"
    dark="#111c31"
    # Rear exhaust, legs, armored shoulders, cannon, and exposed reactor.
    draw.rectangle((x+65,y+16,x+81,y+37),fill=dark)
    draw.rectangle((x+76,y+20,x+84,y+33),fill="#8bdadb")
    for leg in (24,55):
        draw.rectangle((x+leg,y+43,x+leg+12,y+58),fill=dark)
        draw.rectangle((x+leg+2,y+44,x+leg+9,y+54),fill=armor)
        draw.rectangle((x+leg-5,y+57,x+leg+17,y+62),fill="#233651")
        draw.line((x+leg-4,y+59,x+leg+15,y+59),fill="#8bdadb")
    draw.polygon(((x+18,y+10),(x+35,y+3),(x+65,y+7),(x+76,y+21),(x+70,y+48),(x+23,y+48),(x+13,y+31)),fill=dark)
    draw.polygon(((x+23,y+12),(x+37,y+7),(x+63,y+11),(x+69,y+23),(x+64,y+43),(x+25,y+43),(x+19,y+29)),fill=armor)
    draw.rectangle((x+25,y+1,x+47,y+18),fill=dark)
    draw.rectangle((x+28,y+5,x+44,y+14),fill="#687a97")
    draw.rectangle((x+27,y+8,x+41,y+10),fill="#ff876b")
    draw.rectangle((x+35,y+20,x+56,y+37),fill=dark)
    draw.rectangle((x+39,y+24,x+52,y+33),fill="#ff876b")
    draw.rectangle((x+43,y+26,x+48,y+31),fill="#ffd199")
    draw.rectangle((x+3,y+20,x+29,y+38),fill=dark)
    draw.rectangle((x+6,y+22,x+26,y+33),fill=armor)
    draw.rectangle((x-7,y+26,x+19,y+32),fill="#233651")
    draw.line((x-5,y+27,x+17,y+27),fill="#8bdadb")
    if int(phase*3)%2:
        draw.line((x+84,y+22,x+90,y+24),fill="#ffc78a")
        draw.line((x+84,y+30,x+92,y+28),fill="#8bdadb")


def combat_state(index):
    index%=COUNT
    for end,state in ((40,"drone"),(54,"drone-down"),(72,"pickup"),(84,"warning"),(102,"boss-enter"),(164,"boss-fight"),(180,"boss-down"),(192,"clear")):
        if index<end:
            return state


def boss_health(index):
    return max(0,min(1,(164-index)/62))


def rain(draw, index, offset=0):
    random = Random(17)
    for _ in range(64):
        x = random.randrange(6,600)
        y = int((random.randrange(200)+index*400/COUNT)%200)
        if x < 307 and y < 120:
            continue
        draw.line((x,y+offset,x-2,y+5+offset),fill=(117,171,211,48),width=1)


def scene(index, mobile=False):
    offset = 235 if mobile else 0
    image = Image.new("RGBA",(600,470) if mobile else (600,200))
    draw = ImageDraw.Draw(image)
    rain(draw,index,offset)
    phase=index*2*pi/COUNT
    runner_x = 95 + int(9*sin(phase))
    fighter(draw,runner_x,122+offset,index//3)
    state=combat_state(index)
    if state=="drone":
        enemy_x=474+int(12*sin(phase))
        enemy_y=136+int(4*cos(phase*2))+offset
        drone(draw,enemy_x,enemy_y,phase*4)
        for shot in range(3):
            progress=(index/12+shot/3)%1
            x=runner_x+36+progress*(enemy_x-runner_x-46)
            draw.line((x,137+offset,x+8,137+offset),fill="#fff1cb",width=2)
        if index%12<3:
            draw.polygon(((runner_x+33,134+offset),(runner_x+42,137+offset),(runner_x+33,141+offset)),fill="#ffbd72")
            burst(draw,enemy_x-12,enemy_y,index%12)
        draw.rectangle((455,112+offset,499,115+offset),fill="#233651")
        draw.rectangle((455,112+offset,455+max(0,44-index*44//40),115+offset),fill="#ffab98")
    elif state=="drone-down":
        burst(draw,481,136+offset,index-40,1.4)
        text(draw,(453,104+offset),"KO",16,"#ffd199")
    elif state=="pickup":
        progress=(index-54)/17
        pickup(draw,470+(runner_x-470)*progress,124+offset,phase*6)
        text(draw,(355,91+offset),"SPREAD SHOT",13,"#8bdadb")
    elif state=="warning":
        text(draw,(390,99+offset),"BOSS INBOUND",17,"#ffab98")
        draw.line((390,96+offset,548,96+offset),fill="#ffab98")
    elif state in ("boss-enter","boss-fight"):
        entry=max(0,(102-index)/18)
        bx=447+int(entry*190)
        by=94+offset
        hit=state=="boss-fight" and index%8==4
        boss(draw,bx,by,phase,hit)
        text(draw,(390,63+offset),"IRON WARDEN",13,"#ffab98")
        draw.rectangle((390,83+offset,553,89+offset),fill="#111c31",outline="#53617c")
        hp=boss_health(index)
        if hp>0:
            draw.rectangle((392,85+offset,392+int(159*hp),87+offset),fill="#ffab98" if hp>.3 else "#ffc78a")
        if state=="boss-fight":
            for shot in range(3):
                progress=(index/10+shot/3)%1
                x=runner_x+35+progress*(bx-runner_x-37)
                for spread in (-1,0,1):
                    y=137+offset+spread*progress*15
                    draw.line((x-6,y-spread,x+3,y),fill="#fff1cb" if spread==0 else "#8bdadb",width=2)
            if index%8<2:
                draw.polygon(((runner_x+33,132+offset),(runner_x+44,137+offset),(runner_x+33,142+offset)),fill="#ffc78a")
            if hit:
                burst(draw,bx+4,126+offset,2)
            # Slow hostile energy shots stay within the stage.
            progress=((index-102)%24)/24
            ex=bx-10-progress*(bx-runner_x-35)
            ey=121+offset+int(4*sin(progress*pi))
            draw.rectangle((ex-3,ey-2,ex+3,ey+2),fill="#ff876b")
            draw.rectangle((ex-1,ey-1,ex+1,ey+1),fill="#ffd199")
            text(draw,(102,164+offset),"S",11,"#8bdadb")
    elif state=="boss-down":
        age=index-164
        for x,y in ((474,120),(501,134),(459,144)):
            burst(draw,x,y+offset,age,1.2)
        text(draw,(413,77+offset),"BOSS DEFEATED",15,"#ffd199")
    else:
        text(draw,(408,106+offset),"STAGE CLEAR",18,"#8bdadb")
        for particle in range(10):
            x=410+particle*15
            y=135+offset+(index+particle*7)%20
            draw.rectangle((x,y,x+1,y+2),fill="#ffd199" if particle%2 else "#8bdadb")
    if mobile:
        text(draw,(34,19),"hey, i'm",23,"#99c1cc")
        text(draw,(28,50),"SANDEEP",86)
        text(draw,(28,131),"BIST.",86)
    else:
        text(draw,(24,13),"hey, i'm",12,"#a8cbd3")
        text(draw,(21,32),"SANDEEP",45)
        text(draw,(21,74),"BIST.",45)
    return image


def run(args):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",*args],check=True,cwd=ROOT)


def render(mobile=False):
    name="hero-mobile-retro" if mobile else "hero-retro"
    directory=FRAMES/("mobile" if mobile else "desktop")
    directory.mkdir(parents=True,exist_ok=True)
    for index in range(COUNT):
        scene(index,mobile).save(directory/f"{index:03}.png")
    background="[0:v]scale=600:200:force_original_aspect_ratio=increase:flags=neighbor,crop=600:200"
    if mobile:
        background+=",pad=600:470:0:235:color=0x090d1d"
    background+="[background];[background][1:v]overlay=shortest=1,scale=1200:-1:flags=neighbor"
    inputs=["-loop","1","-framerate",str(FPS),"-i",str(ROOT/"source/retro-city.png"),"-framerate",str(FPS),"-i",str(directory/"%03d.png")]
    run(inputs+["-filter_complex",background+",split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=none","-frames:v",str(COUNT),"-loop","0",str(ASSETS/f"{name}.gif")])
    still_inputs=["-i",str(ROOT/"source/retro-city.png"),"-i",str(directory/"126.png")]
    run(still_inputs+["-filter_complex",background,"-frames:v","1",str(ASSETS/f"{name}.png")])


def save_native(frames,name):
    frames=[frame.resize((frame.width*3,frame.height*3),Image.Resampling.NEAREST) for frame in frames]
    frames[0].save(ASSETS/f"{name}.png")
    palette=frames[0].quantize(colors=64)
    encoded=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
    encoded[0].save(ASSETS/f"{name}.gif",save_all=True,append_images=encoded[1:],duration=80,loop=0,optimize=True)


def cards():
    for label,name,accent in (("Portfolio","portfolio","#8bdadb"),("LinkedIn","linkedin","#baa6ec"),("Email","email","#ffab98")):
        frames=[]
        for i in range(48):
            image=Image.new("RGB",(200,56),"#090d1d")
            draw=ImageDraw.Draw(image)
            draw.rectangle((1,1,198,54),fill="#0f192c",outline="#30405b")
            draw.line((4,3,25,3),fill=accent)
            draw.line((4,3,4,10),fill=accent)
            draw.line((174,52,195,52),fill=accent)
            text(draw,(12,10),label,26)
            shift=int(2*sin(i*2*pi/48))
            for row in range(5):
                draw.rectangle((174+shift+row,23+row,175+shift+row,23+row),fill=accent)
                draw.rectangle((174+shift+row,31-row,175+shift+row,31-row),fill=accent)
            start=int(i*180/48)
            draw.line((10+start,53,18+start,53),fill=accent)
            frames.append(image)
        save_native(frames,name+"-retro")
    frames=[]
    for i in range(48):
        image=Image.new("RGB",(400,8),"#090d1d")
        draw=ImageDraw.Draw(image)
        draw.line((0,4,400,4),fill="#30405b")
        x=int(i*400/48)
        draw.line((x,3,x+13,3),fill="#8bdadb")
        draw.line((x,4,x+7,4),fill="#c5f4f0")
        frames.append(image)
    save_native(frames,"divider-retro")


if __name__=="__main__":
    assert [combat_state(i) for i in (0,40,54,72,84,102,164,180,192)]==["drone","drone-down","pickup","warning","boss-enter","boss-fight","boss-down","clear","drone"]
    assert boss_health(102)==1 and boss_health(164)==0
    assert all(boss_health(i+1)<=boss_health(i) for i in range(102,164))
    render()
    render(mobile=True)
    cards()
    for name in ("hero-retro","hero-mobile-retro"):
        path=ASSETS/f"{name}.gif"
        with Image.open(path) as image:
            assert image.info["loop"]==0 and image.n_frames==COUNT
            first=image.convert("RGB")
            image.seek(COUNT//2)
            assert ImageChops.difference(first,image.convert("RGB")).getbbox()
            for index in range(COUNT):
                image.seek(index);image.load()
            duration=sum(image.seek(index) or image.info["duration"] for index in range(COUNT))
            assert abs(duration-COUNT/FPS*1000)<=100, duration
            assert path.stat().st_size<10_000_000
        print(name,round(path.stat().st_size/1024),"KB;",COUNT,"animation frames verified")
