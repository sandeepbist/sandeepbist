"""Build the GitHub profile assets. Run with Python and Pillow."""

from math import sin, pi
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DARK = (9, 11, 16)
WHITE = (238, 241, 235)
MINT = (183, 255, 205)
FRAMES = 96


def font(size, bold=False):
    face = ImageFont.truetype(str(ROOT / "source/SpaceGrotesk.ttf"), size)
    face.set_variation_by_name("Bold" if bold else "Regular")
    return face


def glow(size, center, color, radius):
    image = Image.new("RGB", size)
    x, y = center
    ImageDraw.Draw(image).ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)
    return image.filter(ImageFilter.GaussianBlur(radius*.7))


def background(size, center):
    image = ImageChops.add(Image.new("RGB", size, DARK), glow(size, center, (22, 12, 45), 140))
    draw = ImageDraw.Draw(image)
    for x in range(22, size[0], 28):
        for y in range(20, size[1], 28):
            draw.point((x, y), fill=(22, 25, 31))
    draw.rounded_rectangle((1, 1, size[0]-2, size[1]-2), radius=23, outline=(39, 42, 51))
    return image


def monogram(image, phase, center):
    size = 440
    layer = Image.new("RGB", (size, size), DARK)
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle((45, 45, 394, 394), radius=55, fill=(13, 17, 25), outline=(50, 54, 68), width=1)
    draw.rounded_rectangle((57, 57, 382, 382), radius=47, outline=(28, 34, 42), width=1)
    mask = Image.new("L", (size, size))
    ImageDraw.Draw(mask).text((220, 205), "SB", font=font(217, True), anchor="mm", fill=255)
    aura = mask.filter(ImageFilter.GaussianBlur(26))
    intensity = .4 + .12*sin(phase)
    aura = aura.point(lambda value: int(value*intensity))
    layer.paste(Image.new("RGB", layer.size, (75, 80, 120)), (0, 0), aura)
    shadow = Image.new("L", layer.size)
    shadow.paste(mask, (7, 10))
    layer.paste(Image.new("RGB", layer.size, (29, 43, 43)), (0, 0), shadow)
    face = Image.new("RGB", layer.size)
    surface = ImageDraw.Draw(face)
    for y in range(size):
        amount = max(0, min(1, (y-112)/185))
        highlight = .12+.14*sin(phase+y*.009)
        top, bottom = (209, 235, 244), (139, 214, 186)
        color = tuple(min(250, int(a*(1-amount)+b*amount+highlight*12)) for a,b in zip(top,bottom))
        surface.line((0,y,size,y), fill=color)
    layer.paste(face, (0,0), mask)
    shine = Image.new("L", layer.size)
    light = ImageDraw.Draw(shine)
    position = int(-120+(phase/(2*pi))*(size+240))
    light.polygon(((position,0),(position+54,0),(position-90,size),(position-144,size)), fill=100)
    shine = ImageChops.multiply(shine.filter(ImageFilter.GaussianBlur(16)), mask)
    layer.paste(Image.new("RGB", layer.size, (240,255,247)), (0,0), shine)
    draw = ImageDraw.Draw(layer)
    for index in range(15):
        x = 80 + index*20
        height = 3 + int(12*(sin(phase+index*.52)+1)/2)
        draw.line((x,348,x,348-height), fill=(57,85,75), width=3)
    draw.line((84,91,117,91), fill=MINT, width=2)
    draw.line((84,91,84,124), fill=MINT, width=2)
    draw.line((322,349,355,349), fill=(168,151,226), width=2)
    draw.line((355,316,355,349), fill=(168,151,226), width=2)
    for trail in range(100):
        distance = ((phase/(2*pi))*1200-trail)%1200
        side = int(distance//300)
        offset = distance%300
        if side == 0:
            x,y = 70+offset,47
        elif side == 1:
            x,y = 392,70+offset
        elif side == 2:
            x,y = 370-offset,392
        else:
            x,y = 47,370-offset
        brightness = (1-trail/100)**2
        color = tuple(int(39+(channel-39)*brightness) for channel in MINT)
        draw.point((x,y),fill=color)
    image.paste(layer,(int(center[0]-size/2),int(center[1]-size/2)))
    return image


def save(frames, name):
    frames[0].save(ASSETS / f"{name}.png")
    samples = Image.new("RGB", (frames[0].width*4, frames[0].height))
    for i in range(4):
        samples.paste(frames[i*len(frames)//4], (i*frames[0].width, 0))
    palette = samples.quantize(colors=250)
    encoded = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    encoded[0].save(ASSETS / f"{name}.gif", save_all=True, append_images=encoded[1:], duration=70, loop=0, optimize=True)


def hero(mobile=False):
    size = (720, 880) if mobile else (1200, 480)
    center = (360, 600) if mobile else (948, 243)
    base = background(size, center)
    draw = ImageDraw.Draw(base)
    x = 44 if mobile else 58
    letter_x = x
    for letter in "HEY, I'M":
        draw.text((letter_x, 34), letter, font=font(16), fill=(162, 169, 175))
        letter_x += draw.textlength(letter, font=font(16))+4
    draw.ellipse((size[0]-61, 41, size[0]-55, 47), fill=MINT)
    draw.line((size[0]-49, 44, size[0]-31, 44), fill=(77, 86, 88))
    title = font(112 if mobile else 126, bold=True)
    draw.text((x-5, 65 if mobile else 93), "sandeep", font=title, fill=WHITE)
    draw.text((x-5, 171 if mobile else 214), "bist", font=title, fill=WHITE)
    dot_x = x-5+draw.textlength("bist", font=title)+8
    dot_y = 265 if mobile else 320
    draw.rounded_rectangle((dot_x, dot_y, dot_x+17, dot_y+17), radius=4, fill=MINT)
    if not mobile:
        draw.line((x, 386, 676, 386), fill=(35, 39, 46))
    draw.text((x, 316 if mobile else 407), "I make all sorts of things.", font=font(24), fill=(163, 172, 177))
    name_mask = Image.new("L", size)
    mask_draw = ImageDraw.Draw(name_mask)
    mask_draw.text((x-5, 65 if mobile else 93), "sandeep", font=title, fill=255)
    mask_draw.text((x-5, 171 if mobile else 214), "bist", font=title, fill=255)
    frames = []
    for i in range(FRAMES):
        phase = i*2*pi/FRAMES
        frame = monogram(base.copy(), phase, center)
        light = Image.new("L", size)
        light_draw = ImageDraw.Draw(light)
        light_x = int(-100+i*(size[0]+200)/FRAMES)
        light_draw.polygon(((light_x, 0), (light_x+55, 0), (light_x-65, 380), (light_x-120, 380)), fill=65)
        light = light.filter(ImageFilter.GaussianBlur(24))
        mask = ImageChops.multiply(light, name_mask)
        frame.paste(Image.new("RGB", size, (173, 243, 217)), (0, 0), mask)
        frames.append(frame)
    save(frames, "hero-mobile-v3" if mobile else "hero-v3")


def card(label, name, accent):
    frames = []
    for i in range(48):
        image = Image.new("RGB", (400, 124), DARK)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((1, 1, 398, 122), radius=17, fill=(15, 18, 24), outline=(43, 48, 57))
        draw.text((27, 31), label, font=font(43), fill=WHITE)
        shift = 2*sin(i*2*pi/48)
        draw.line((338+shift, 76-shift, 363+shift, 51-shift), fill=accent, width=3)
        draw.line((343+shift, 51-shift, 363+shift, 51-shift, 363+shift, 71-shift), fill=accent, width=3)
        brightness = .55+.45*(sin(i*2*pi/48)+1)/2
        draw.line((26, 111, 82, 111), fill=tuple(int(c*brightness) for c in accent), width=2)
        for trail in range(72):
            position = (i*796/48-trail)%796
            if position < 398:
                px, py = position, 2
            else:
                px, py = 795-position, 121
            fade = (1-trail/72)**2
            draw.point((px, py), fill=tuple(int(35+(c-35)*fade) for c in accent))
        frames.append(image)
    save(frames, name+"-v2")


def divider():
    frames = []
    for i in range(FRAMES):
        image = Image.new("RGB", (1200, 22), DARK)
        draw = ImageDraw.Draw(image)
        draw.line((0, 11, 1200, 11), fill=(37, 41, 49))
        for segment in range(110):
            x = int((i*1200/FRAMES-segment)%1200)
            fade = (1-segment/110)**2
            draw.line((x, 10, x, 12), fill=tuple(int(37+(c-37)*fade) for c in MINT))
        frames.append(image)
    save(frames, "divider-v2")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    hero()
    hero(mobile=True)
    card("Portfolio", "portfolio", MINT)
    card("LinkedIn", "linkedin", (186, 171, 255))
    card("Email", "email", (151, 202, 255))
    divider()
    for path in ASSETS.glob("*.gif"):
        with Image.open(path) as image:
            assert image.n_frames > 1 and image.info.get("loop") == 0
            assert image.size == Image.open(path.with_suffix(".png")).size
            image.seek(image.n_frames-1)
            image.load()
            assert path.stat().st_size < 10_000_000
        print(path.name, round(path.stat().st_size/1024), "KB")
