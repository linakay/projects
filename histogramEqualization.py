# Given a PGM file, output a higher contrast PGM with grey level histograms using only
# standard, built-in functionality (without numpy, matplotlib, or external libraries).
# I chose histogram equalization, which transforms pixel intensity values by
# normalizing the cumulative distribution function of the original image. The new
# image will contain more gray values at the dark and light ends of the spectrum.
# Type 'python3 thisfile.py /path/filename.pgm' at the terminal or change the
# pgm variable on ln 59 to '/path/filename.pgm' in a Python console to test.

import sys, re
from math import ceil

# Counts the number of pixels at each level of gray
def count_pixels(pixels):
    pixel_counts = [0 for i in range(max(pixels)+1)]
    for n in pixels:
        pixel_counts[n] += 1
    return pixel_counts

# Uses the cumulative distribution function (CDF) to increase image contrast
def cdf_norm(pixels):
    x_dim, y_dim = int(pixels[0]), int(pixels[1])
    pixels = pixels[3:]
    pmin, pmax, rng = min(pixels), max(pixels), max(pixels)-min(pixels)
    if rng > 60:
        pixel_counts = count_pixels(pixels)
        # Calculates the cumulative distribution at each gray level
        cdf = [sum(pixel_counts[:i]) for i in range(1,len(pixel_counts)+1)]
        N = max(cdf)-min(cdf)
        # Normalizes the CDF by dividing each value by the range of values
        norm = [round(((x-pmin)*pmax)/N) for x in cdf]
        # Uses the normalized CDF as an index to adjust pixel gray values
        normalized = [norm[n] for n in pixels]
    # Employs pixel stretching if range is too small for CDF normalization
    else:
        normalized = [round(((x-pmin)/(rng))*255) for x in pixels]
    output = [str(n) for n in normalized]
    output_file = f'{fname}_new.pgm'
    with open(output_file,'w') as target:
        img = f'P2\n{x_dim} {y_dim}\n{pmax}\n'
        img += '\n'.join(output)
        target.write(img)
        target.close()
    return normalized

# Calculates totals and scales data for a 16-bin printable histogram
def hgram(pixel_counts, fname):
    pmax = len(pixel_counts)
    width = round(pmax/16)
    bin_cts = [sum(pixel_counts[i:i+width]) for i in range(0, pmax, width)]
    tot = [f'({x:,})' for x in bin_cts]
    bins = [f'[{i}-{min(i+width-1, pmax-1)}]\t'.expandtabs(10) for i in range(0, pmax, width)]
    plt = ['█'*ceil(70*(n/max(bin_cts))) for n in bin_cts]
    hist = "\n".join('{}{}{}'.format(x,y,z) for x,y,z in zip(bins,plt,tot))
    title = f'Histogram - {fname}\n'
    tablen = max(round((90-len(title))/2), 0)
    title = f'\t{title}'.expandtabs(tablen)
    legend = 'Values \t Bin Counts\n'.expandtabs(39)
    hist = f'{title}{legend}{hist}\n'
    return hist

try:
    pgm = sys.argv[1]
    with open(pgm) as content:
        parts = re.split(r'\s+',re.sub(r'#.*',r'\n',content.read()))
        fname = pgm[:len(pgm)-4].split('/')[-1]
        content.close()
    parts = [int(n) for n in parts[1:] if n]
    pixels = parts[3:]
    print(hgram(count_pixels(pixels), f'Pixel Intensity Values: {fname}'))
    print(hgram(count_pixels(cdf_norm(parts)), f'Modified {fname}'))

except Exception:
    print(f'''Please enter a valid pgm file path as an argument. For example:
    python3 {sys.argv[0]} /path/filename.pgm''')
