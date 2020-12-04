# Function to convert grayscale PNG files to PGM format
import matplotlib.pyplot as plt

def png_to_pgm(file):
    img = plt.imread(file)
    dimension = img.shape
    img_flat = list(img.flatten())
    depth = round(max(img_flat)*255)
    pixels = [round(n*255) for n in img_flat]
    pixels_str = [str(n) for n in pixels]
    pgm = '\n'.join(pixels_str)
    header = f'P2\n{dimension[0]} {dimension[1]}\n{depth}\n'
    fname = file.split(sep='/')[-1]
    fname = fname.split(sep='.')[0]+'.pgm'
    with open(fname, 'w') as target:
        target.write(header+pgm)
        target.close()
    # return pixels