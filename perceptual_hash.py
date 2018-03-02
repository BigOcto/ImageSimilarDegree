#!/usr/bin/python

import glob
import os
import sys

from PIL import Image
from functools import reduce
from excel_operation import read_excel_data_by_col
from excel_operation import write_excel

EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'


def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((16, 16), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    return reduce(lambda x, y_z: x | (y_z[1] << y_z[0]),
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                  0)


def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    print("hanming res :", h)
    return h


def do():
    image_list = read_excel_data_by_col("SOUCE_1", 0, "Image_similarity_degree.xls")
    target_list = read_excel_data_by_col("SOUCE_2", 0, "Image_similarity_degree.xls")
    # for i in range(1, len(image_list)):
    #     calculate(image_list[i], target_list[i])
    calculate("1.JPG", "2.JPG")


def calculate(im, wd):
    h = avhash(im)
    print(h)

    seq = []
    # prog = int(len(images) > 50 and sys.stdout.isatty())
    # for f in images:
    #     if prog:
    #         perc = 100. * prog / len(images)
    #         x = int(2 * perc / 5)
    #         print('\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']'),
    #         print('%.2f%%' % perc, '(%d/%d)' % (prog, len(images))),
    #         sys.stdout.flush()
    #         prog += 1
    hash = avhash(wd)
    print(hash)
    haming = hamming(hash, h)

    # if prog:print
    # print(haming)
    # s = "%d\t%s" % (h, haming)
    # write_excel([haming], "Image_similarity_degree.xls", "DEGREE_BY_HASH")


if __name__ == '__main__':
    do()
    # if len(sys.argv) <= 1 or len(sys.argv) > 3:
    #     print("Usage: %s image.jpg [dir]" % sys.argv[0])
    # else:
    # im, wd = "1.JPG", "2.JPG"
    # h = avhash(im)
    # # os.chdir(wd)
    # images = []
    # # for ext in EXTS:
    # images.extend(glob.glob('*%s' % wd))
    # seq = []
    # prog = int(len(images) > 50 and sys.stdout.isatty())
    # for f in images:
    #     print("____________", f)
    #     seq.append((f, hamming(avhash(f), h)))
    #
    #     if prog:
    #         perc = 100. * prog / len(images)
    #         x = int(2 * perc / 5)
    #         print('\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']'),
    #         print('%.2f%%' % perc, '(%d/%d)' % (prog, len(images))),
    #         sys.stdout.flush()
    #         prog += 1
    #
    # # if prog:print
    # for f, ham in sorted(seq, key=lambda i: i[1]):
    #     print("%d\t%s" % (ham, f))
