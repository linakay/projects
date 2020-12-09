# Alternative to histogram equalization, which uses square roots of grayscale
# values to increase contrast for images that are already equalized.

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