import re

def readpgm(pgm):
    with open(pgm) as content:
        parts = re.split(r'\s+',re.sub(r'#.*',r'\n',content.read()))
        content.close()
    parts = [int(n) for n in parts[1:] if n]
    pixels = parts[3:]
    content.close()
    return parts

def writepgm(pixels, x, y, fname):
    pixel_str = [str(p) for p in pixels]
    new_pixels = '\n'.join(pixel_str)
    header = f'P2\n{x} {y}\n{max(pixels)}\n'
    with open('newpgm.pgm', 'w') as new_image:
        new_image.write(header+new_pixels)
        new_image.close()