allcolors
=========

# Background

At a coding night, code golf came up and @andrew311 mentioned he had been
playing with this problem:

http://codegolf.stackexchange.com/questions/22144/images-with-all-colors

which is to make images in which each possible color is used exactly once.


# The Game

I thought it would be interesting to write a program which took an image as
input and recreating it using every possible color once.  This is the result.  

color_replace.py will take an input image which has N number of pixels where
N is a power of 2 between 3 and 32 inclusive (2^3, 2^4, ..., 2^32).  It will
use the appropriate palette based on the image size.

For example, if you give it a 64x64 pixel image, it will use a palette with
4096 different colors.  Images don't have to be square (256x128 works fine),
but do have to a power of 2.


# Examples

## 64x64
![64x64 Input](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_64x64.png)

![64x64 Output](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_64x64_out.png)


## 256x128
![256x128 Input](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_256x128.png)

![256x128 Output](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_256x128_out.png)

