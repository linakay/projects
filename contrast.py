# Given a PGM file, output a higher contrast PGM with grey level histograms using only
# standard, built-in functionality (without numpy, matplotlib, or external libraries).
# If the original is already equalized, take the square root of gray values.
# Otherwise, use histogram equalization, which transforms pixel intensity values by
# normalizing the cumulative distribution function of the original image. The new
# image will contain more gray values at the dark and light ends of the spectrum.
# Type 'python3 thisfile.py /path/filename.pgm' at the terminal or change the
# pgm variable on ln 82 to '/path/filename.pgm' in a Python console to test.

import re, sys, makepgm
from math import ceil
from statistics import stdev, mean

# Counts the total pixels at each level of gray
def count_pixels(pixels):
    rng = max(pixels)+1
    pixel_counts = [0 for i in range(rng)]
    for n in pixels:
        pixel_counts[n] += 1
    return pixel_counts

# Calculate negative (and positive) square roots without errors
def root(x):
    if x >= 0:
        return x**(1/2)
    else:
        return -(-x)**(1/2)

# Convert values between 0 and 1
def normalize(vals):
    mx, mn = max(vals), min(vals)
    return [(x - mn)/(mx - mn) for x in vals]

# Make gray values between -1 and 1 & take the square root
def sqrt_contrast(pixels):
    normalized = normalize(pixels)
    betweenones = [2*x - 1 for x in normalized]
    roots = [root(x) for x in betweenones]
    norm_roots = normalize(roots)
    mx = max(pixels)
    return [round(mx*x) for x in norm_roots]

# Uses the cumulative distribution function (CDF) to increase image contrast
def cdf_norm(pixels):
    pixel_counts = count_pixels(pixels)
    cdf = [sum(pixel_counts[:i]) for i in range(1,len(pixel_counts)+1)]
    norm = normalize(cdf)
    mx = max(pixels)
    normalized = [round(mx*x) for x in norm]
    return [normalized[p] for p in pixels]

def make_bins(pixel_counts, mn, mx):
    width = ceil((mx-mn)/16)
    counts = {i:pixel_counts[i] for i in range(mn, mx+1)}
    labels = [f'{i}-{min(mx, i+width-1)}' for i in range(mn, mx+1, width)]
    bns = [sum(counts[i] for i in range(i, min(i+width, mx+1))) for i in range(mn, mx+1, width)]
    return labels, bns

# Now display histograms for the original and enhanced images
def hgram(bins, labels, fname):
    bmx = max(bins)
    bars = [f"{round(x*70/bmx)*'█'}"+f'({x:,})' for x in bins]
    plt = [f'[{labels[i]}]\t{bars[i]}'.expandtabs(10) for i in range(len(bars))]
    plt = '\n'.join(plt)
    title = f'Histogram - {fname}\n'
    tablen = max(round((90-len(title))/2), 0)
    title = f'\t{title}'.expandtabs(tablen)
    legend = 'Values \t Bin Counts\n'.expandtabs(39)
    hist = f'{title}{legend}{plt}\n'
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
    pixel_counts = count_pixels(pixels)
    bins = make_bins(pixel_counts, min(pixels), max(pixels))[1]
    labels = make_bins(pixel_counts, min(pixels), max(pixels))[0]
    if len(set(pixel_counts)) < 10 or mean(bins)>(5*stdev(bins)):
        new_pixels = sqrt_contrast(pixels)
    else:
        new_pixels = cdf_norm(pixels)
    new_bins = make_bins(count_pixels(new_pixels), min(new_pixels), max(new_pixels))[1]
    new_labels = make_bins(count_pixels(new_pixels), min(new_pixels), max(new_pixels))[0]
    hgram(bins, labels, f'Pixel Intensity Values: {fname}')
    hgram(new_bins, new_labels, f'Modified {fname}')
    makepgm.writepgm(new_pixels, parts[0], parts[1], fname)

except Exception:
    print(f'''Please enter a valid pgm file path as an argument. For example:
    python3 {sys.argv[0]} /path/filename.pgm''')