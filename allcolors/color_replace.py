import argparse
from datetime import datetime
from collections import namedtuple
import math
from operator import itemgetter
from PIL import Image
import random
from sortedcontainers import SortedListWithKey
import sys
import time

MAX_COLOR_DEPTH = 2**8  # bit depth of the input image - TODO: compute automatically

Color = namedtuple('Color', ['r', 'g', 'b', 'avg'])

def avg(l):
    return float(sum(l))/len(l) if len(l) > 0 else float('nan')

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

def find_closest_color(color, palette, max_tries):
    """
        max_tries limits number of iterations to try.
        Assumes palette is SortedListWithKey, sorted by avg
    """
    if not palette:
        raise Exception('Palette empty - Ran out of colors; is input image too big ?')

    color = Color(r=color[0], g=color[1], b=color[2], avg=avg(color))
    idx = (palette.bisect_right(color) - palette.bisect_left(color)) / 2

    # look at max_tries colors closest to avg
    idx = max(0, idx - (max_tries / 2))
    sub_palette = palette[idx : idx + max_tries]

    best_color = sub_palette[0]
    best_delta = sys.maxint
    tries = 0
    for cur_color in sub_palette:
        if tries >= max_tries:
            return best_color
        cur_delta = compute_delta(color.r, color.g, color.b, \
                                  cur_color.r, cur_color.g, cur_color.b)
        if cur_delta < best_delta:
            best_color = cur_color
            best_delta = cur_delta
        tries += 1
    return best_color

def create_palette(color_depth=8):
    """ Create palette of all colors for color_depth bit rate.  """
    palette = SortedListWithKey(load=1000, key=lambda c: c.avg)
    scale = (MAX_COLOR_DEPTH / 2**color_depth)

    for x in range(0, 2**color_depth):
        for y in range(0, 2**color_depth):
            for z in range(0, 2**color_depth):
                r = x*scale
                g = y*scale
                b = z*scale
                palette.add( Color(r=r, g=g, b=b, avg=int(avg([r,g,b]))) )

    return palette

def do_replace(im, palette, max_tries):
    start_time = time.time()

    pixels_to_do = []
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            pixels_to_do.append( (x, y) )

    while (pixels_to_do):
        x, y = random.choice(pixels_to_do)  # Randomly select next pixel to replace
        new_color = find_closest_color(im.getpixel((x, y)), palette, max_tries)
        im.paste( (new_color.r, new_color.g, new_color.b), box=((x, y, x+1, y+1)))
        palette.remove(new_color)
        pixels_to_do.remove((x, y))

        if (len(pixels_to_do) % 1000 == 0):
            print '%s pixels to go. Last paste: %s Elapsed time: %d secs' %\
                (len(pixels_to_do), new_color, time.time() - start_time)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create an AllRGB version of a given image')
    parser.add_argument('input_image', type=str, nargs=1, help='Input image')
    parser.add_argument('--max_tries', dest='max_tries', default=20000, type=int,
                        help='Maximum number of colors to look at per pixel.')
    args = vars(parser.parse_args())
    in_filename = args['input_image'][0]

    print 'Starting...'
    print 'max_tries: %s' % args['max_tries']
    im = Image.open(in_filename)
    print 'Read file %s' % in_filename

    # Compute palette size based on size of image.
    num_pixels = im.size[0] * im.size[1]
    depth = math.log(num_pixels, 2) / 3.0
    if depth != round(depth, 0) or depth < 3 or depth > 32:
        raise Exception('Unsupported image size: %s x %x\n' % (im.size[0], im.size[1]) +\
                        'Number of pixels must be a power of 2 between 3-32.')
    palette = create_palette(int(depth))

    print 'Using palette with %s colors' % len(palette)

    do_replace(im, palette, max_tries=args['max_tries'])

    print 'Finished.  %s colors left in palette.' % len(palette)
    out_filename = in_filename[:-4] + '_out_%s.png' % datetime.now().strftime('%Y-%m-%d_%H%M')
    im.save(out_filename)
    print 'Wrote %s' % out_filename

