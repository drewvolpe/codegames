allcolors
=========

# Background

At a coding night, code golf came up and [@andrew311](http://www.twitter.com/andrew311) mentioned he had been
playing with this problem:

http://codegolf.stackexchange.com/questions/22144/images-with-all-colors

which is to make images in which each possible color is used exactly once.


# The Game

I thought it would be interesting to write a program which, instead of creating
a new image from scratch, would take an image as input and create a version 
of that image using every color once.  This is my first attempt at it.

color_replace.py will take an input image which has N number of pixels where
N is a power of 2 between 3 and 32 inclusive (2^3, 2^4, ..., 2^32).  It will
use the appropriate palette based on the image size and create 

For example, if you give it a 64x64 pixel image, it will use a palette with
4096 different colors.  Images don't have to be square (256x128 works fine),
but do have to a power of 2.

It can be run with: 
> python color_replace.py input_image.png



# Examples

### Tasty 64x64
![64x64 Input](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_64x64.png)

![64x64 Output](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_64x64_out.png)


### Tasty 256x128
![256x128 Input](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_256x128.png)

![256x128 Output](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_256x128_out.png)


### Mercat 256x128
![256x128 Input](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/mercat_128x256.png)

![256x128 Output](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/mercat_128x256_out.png)


### Tasty 512x512
![512x512 Input](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_512x512.png)

![512x512 Output](https://raw.github.com/drewvolpe/codegames/master/allcolors/images/tasty_512x512_out.png
)



