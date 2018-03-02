#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import cv2
from PIL import Image
from PIL import ImageDraw
from os.path import join, isfile, isdir, splitext, basename, abspath
from os import walk
from excel_operation import write_excel


def make_regalur_image(img, size=(256, 256)):
    return img.resize(size).convert('RGB')


def split_image(img, part_size=(64, 64)):
    w, h = img.size
    pw, ph = part_size

    assert w % pw == h % ph == 0

    return [img.crop((i, j, i + pw, j + ph)).copy() \
            for i in range(0, w, pw) \
            for j in range(0, h, ph)]


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


def calc_similar(li, ri):
    #	return hist_similar(li.histogram(), ri.histogram())

    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


def calc_similar_by_path(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    return calc_similar(li, ri)


def calculate_his(li, ri):
    # roi is the object or region of object we need to find
    roi = cv2.imread(li, -1)
    # hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # target is the image we search in
    target = cv2.imread(ri, -1)
    # hsvt = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

    # Find the histograms using calcHist. Can be done with np.histogram2d also
    M = cv2.calcHist([roi], [0], None, [256], [0, 256])
    I = cv2.calcHist([target], [0], None, [256], [0, 256])
    print(cv2.compareHist(M, I, 0))


def get_count(num):
    return (num - 1 + 1) * (num - 1) / 2


def do_calculate(path, need_write_excel=None):
    fileArray = list()
    for root, dirs, files in walk(path):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                fileArray.append(join(root, file))
    print("总文件数： ", len(fileArray))
    calculate_times = get_count(len(fileArray))
    calculate_count = 0
    for i in range(len(fileArray)):
        for j in range(i + 1, len(fileArray)):
            similarity_degree = calc_similar_by_path(fileArray[i], fileArray[j])
            calculate_count += 1
            str1 = "\r \r {0}/{1} {2:.3} %".format(calculate_count + 1, calculate_times,
                                                   ((1 + calculate_count) * 100 / calculate_times))
            sys.stdout.write(str1)
            sys.stdout.flush()

            if need_write_excel:
                if similarity_degree == 1:
                    print("%s ** %s : %.3f" % (abspath(fileArray[i]), abspath(fileArray[j]), similarity_degree))
                    write_excel([abspath(fileArray[i])], "Image_similarity_degree.xls", "SOUCE_1")
                    write_excel([abspath(fileArray[j])], "Image_similarity_degree.xls", "SOUCE_2")
                    write_excel([similarity_degree], "Image_similarity_degree.xls", "DEGREE3")
            else:
                print("\n%s ** %s : %.3f" % (abspath(fileArray[i]), abspath(fileArray[j]), similarity_degree))


if __name__ == '__main__':
    # path = './test/'
    do_calculate()

    # test
    # path = r'test/TEST%d/%d.JPG'
    # for i in range(1, 7):
    #     print('test_case_%d: %.3f' % (i, calc_similar_by_path('test/TEST%d/%d.JPG' % (i, 1), 'test/TEST%d/%d.JPG' % (i, 2))))
    # make_doc_data('test/TEST4/1.JPG', 'test/TEST4/2.JPG')

    # test
    # data = ["data3", "data4","data5","data6"]
    # write_excel(data, "test.xls", "degree1")
    # write_excel(data, "test.xls", "degree2")
    # write_excel(data, "test.xls", "degree3")
