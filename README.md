# projects
# Contrast Enhancement
The primary method of manipulating contrast is histogram equalization (contrast.py). 
My code groups pixel grayscale values into sixteen bins. If the standard deviation of 
total pixels in each bin is substantially lower than the overall mean, the 
original image is already equalized. So the resulting image will be similar or identical.
A modified square root method of contrast manipulation can be used to increase contrast instead of histogram equalization.<br><br>
<img src='Histogram.png' alt='Before and after histogram with original and output image'>
<br><br>Portions of the image contrast enhancement code were adapted and modified from the following sources:
https://medium.com/hackernoon/histogram-equalization-in-python-from-scratch-ebb9c8aa3f23 by Tory Walker
https://fog.ccsf.edu/~abrick/notes/231-15.pdf by Aaron Brick
