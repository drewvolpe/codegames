
import math
from PIL import Image
import random
import sys
import time

INPUTFILENAME = './images/mercat_128x256.png' # 'tasty_256x128.png'
OUTFILENAME = INPUTFILENAME[:-4] + '_out.png'
MAX_COLOR = 2**8  # bit depth of the input image - TODO: compute automatically


def compute_delta(r1, g1, b1, r2, g2, b2):
    """ Returns a score of how different color 1 is from color 2, with
        0 being a perfect match.
    """
    # TODO - Replace with better algorithm

    # basic alg: basic distance + sum
    sum1 = r1 + g1 + b1
    sum2 = r2 + g2 + b2
    return (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2 + \
        (sum1 - sum2)**2


def find_closest_color(color, palette):
    if not palette:
        raise Exception('Palette empty - Ran out of colors; is input image too big ?')
    best_color = None
    best_delta = sys.maxint
    for x, y, z in palette:
        cur_delta = compute_delta(color[0], color[1], color[2], x, y, z)
        if cur_delta < best_delta:
            best_color = (x, y, z)
            best_delta = cur_delta
    return best_color


def create_palette(color_depth=8, max_color_depth=8):
    """ Create palette of all colors for color_depth bit rate.  """
    palette = []
    scale = (max_color_depth / 2**color_depth)

    for x in range(0, 2**color_depth):
        for y in range(0, 2**color_depth):
            for z in range(0, 2**color_depth):
                palette.append( (x*scale, y*scale, z*scale) )
    return palette


def do_replace_simple(im, palette):
    # Simple, greedy version
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            new_color = find_closest_color(im.getpixel((x, y)), palette)
            im.paste(new_color, box=((x, y, x+1, y+1)))
            palette.remove(new_color) # only use each color once
        print 'Row %s of %s   last paste: %s - Elapsed: %s' %\
            (x, im.size[0], new_color, time.time() - start_time)



def do_replace_random(im, palette):
    # Randomly select next pixel to replace
    start_time = time.time()
    pixels_to_do = []
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            pixels_to_do.append( (x, y) )
    
    while (pixels_to_do):
        x, y = random.choice(pixels_to_do)
        new_color = find_closest_color(im.getpixel((x, y)), palette)
        im.paste(new_color, box=((x, y, x+1, y+1)))
        palette.remove(new_color)
        pixels_to_do.remove((x, y))

        if (len(pixels_to_do) % 1000 == 0):
            print '%s pixels to go. Last paste: %s Elapsed time: %d secs' %\
                (len(pixels_to_do), new_color, time.time() - start_time)


if __name__ == "__main__":

    print 'Starting...'
    im = Image.open(INPUTFILENAME)
    print 'Read file %s' % INPUTFILENAME

    # Compute palette size based on size of image.
    num_pixels = im.size[0] * im.size[1]
    depth = math.log(num_pixels, 2) / 3.0
    if depth != round(depth, 0) or depth < 3 or depth > 32:
        raise Exception('Unsupported image size: %s x %x\n' % (im.size[0], im.size[1]) +\
                        'Number of pixels must be a power of 2 between 3-32.')
    palette = create_palette(int(depth), MAX_COLOR)
    print 'Using palette with %s colors' % len(palette)

    do_replace_random(im, palette)

    print 'Finished.  %s colors left in palette.' % len(palette)
    im.save(OUTFILENAME)
    print 'Wrote %s' % OUTFILENAME
