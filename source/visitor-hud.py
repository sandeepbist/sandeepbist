"""Build an animated arcade frame around the existing live visitor counter."""

from pathlib import Path
from math import sin, pi
import importlib.util
from PIL import Image, ImageDraw, ImageChops

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location("retro",ROOT/"source/build-retro.py")
retro=importlib.util.module_from_spec(spec)
spec.loader.exec_module(retro)


def header():
    frames=[]
    for i in range(48):
        image=Image.new("RGB",(400,42),"#090d1d")
        draw=ImageDraw.Draw(image)
        draw.line((7,4,393,4),fill="#30405b")
        draw.line((7,4,7,36),fill="#30405b")
        draw.line((393,4,393,36),fill="#30405b")
        label="VISITORS"
        width=draw.textlength(label,font=retro.font(24))
        retro.text(draw,((400-width)/2,6),label,24)
        for j in range(3):
            brightness=.4+.6*(sin(i*2*pi/48-j*.7)+1)/2
            color=tuple(int(channel*brightness) for channel in (255,184,142))
            x=40+j*10
            draw.rectangle((x,17,x+3,20),fill=color)
            draw.rectangle((397-x,17,400-x,20),fill=color)
        x=int(i*380/48)+10
        draw.line((max(10,x-15),4,x,4),fill="#8bdadb")
        frames.append(image)
    retro.save_native(frames,"visitors-hud-retro")


def guards():
    for name in ("visitor-player-retro","visitor-drone-retro"):
        frames=[]
        for i in range(48):
            image=Image.new("RGB",(64,64),"#090d1d")
            draw=ImageDraw.Draw(image)
            if name=="visitor-player-retro":
                retro.fighter(draw,15,15,i//3)
                if i%12<3:
                    draw.polygon(((49,27),(56,30),(49,33)),fill="#ffc58a")
                draw.line((7,53,55,53),fill="#30405b")
                draw.line((14,54,41,54),fill="#223c4d")
            else:
                retro.drone(draw,32,31+int(3*sin(i*2*pi/48)),i*2*pi/48)
                for j in range(3):
                    x=24+j*8
                    draw.point((x,53-(i+j*5)%12),fill="#53acbb")
            frames.append(image)
        retro.save_native(frames,name)


if __name__=="__main__":
    header()
    guards()
    for name in ("visitors-hud-retro","visitor-player-retro","visitor-drone-retro"):
        path=ROOT/"assets"/f"{name}.gif"
        with Image.open(path) as image:
            assert image.info["loop"]==0 and image.n_frames>1
            first=image.convert("RGB")
            changed=False
            for i in range(image.n_frames):
                image.seek(i);image.load()
                changed=changed or bool(ImageChops.difference(first,image.convert("RGB")).getbbox())
            assert changed
        print(name,round(path.stat().st_size/1024),"KB; animation verified")
