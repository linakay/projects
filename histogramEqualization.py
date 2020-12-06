# Given a PGM file, output a higher contrast PGM with grey level histograms using only
# standard, built-in functionality (without numpy, matplotlib, or external libraries).
# I chose histogram equalization, which transforms pixel intensity values by
# normalizing the cumulative distribution function of the original image. The new
# image will contain more gray values at the dark and light ends of the spectrum.
# Type 'python3 thisfile.py /path/filename.pgm' at the terminal or change the
# pgm variable on ln 62 to '/path/filename.pgm' in a Python console to test.

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
    pixel_counts = count_pixels(pixels)
    # Calculates the cumulative distribution at each gray level
    cdf = [sum(pixel_counts[:i]) for i in range(1,len(pixel_counts)+1)]
    N = max(cdf)-min(cdf)
    # Normalizes the CDF by dividing each value by the range of values
    norm = [round(((x-min(cdf))*max(pixels))/N) for x in cdf]
    # Uses the normalized CDF as an index to adjust pixel gray values
    normalized = [norm[n] for n in pixels]
    return normalized

# Rescales data to generate a 16-bin printable histogram
def hgram(pixels, fname):
    pmin, pmax, width = min(pixels), max(pixels), ceil((max(pixels)-min(pixels))/16)
    pixel_counts = count_pixels(pixels)
    counts = {i:pixel_counts[i] for i in range(min(pixels), max(pixels)+1)}
    bins = {f'{i}-{min(pmax, i+width-1)}':sum(counts[i] for i in range(i, min(i+width, pmax+1))) for i in range(pmin, pmax+1, width)}
    plt = [f"[{k}]\t{round(bins[k]*70/max(bins.values()))*'█'}".expandtabs(10)+f'({bins[k]:,})' for k in bins]
    bars = '\n'.join(plt)
    title = f'Histogram - {fname}\n'
    tablen = max(round((90-len(title))/2), 0)
    title = f'\t{title}'.expandtabs(tablen)
    legend = 'Values \t Bin Counts\n'.expandtabs(39)
    hist = f'{title}{legend}{bars}\n'
    print(hist)
    return hist

try:
    pgm = sys.argv[1]
    with open(pgm) as content:
        parts = re.split(r'\s+',re.sub(r'#.*',r'\n',content.read()))
        fname = pgm[:len(pgm)-4].split('/')[-1]
        content.close()
    parts = [int(n) for n in parts[1:] if n]
    pixels = parts[3:]
    hgram(pixels, f'Pixel Intensity Values: {fname}')
    hgram(cdf_norm(pixels), f'Modified {fname}')

except Exception:
    print(f'''Please enter a valid pgm file path as an argument. For example:
    python3 {sys.argv[0]} /path/file.pgm''')