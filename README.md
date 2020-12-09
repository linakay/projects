# projects
# Contrast Enhancement
The primary method of manipulating contrast is histogram equalization. However, if the 
original image is already equalized, the resulting image will be similar or identical.
My code groups pixel grayscale values into sixteen bins. If the standard deviation of 
total pixels in each bin is substantially lower than the overall mean, the code employs
a modifiied square root method of contrast manipulation instead of histogram equalization.
