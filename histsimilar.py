#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2


def calculate_his(li, ri):
    # roi is the object or region of object we need to find
    roi = cv2.imread(li, -1)
    # hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # target is the image we search in
    target = cv2.imread(ri, -1)
    # hsvt = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

    # Find the histograms using calcHist. Can be done with np.histogram2d also
    degree = []
    for i in range(0, 4):
        try:
            hist_roi = cv2.calcHist([roi], [i], None, [256], [0, 256])
            his_target = cv2.calcHist([target], [i], None, [256], [0, 256])
            re = cv2.compareHist(hist_roi, his_target, 0)
            degree.append(re)
            # print("Run %d channel" % i, 'Degree: ', re)
        except:
            continue
            # print('Run error channel: ', i, 'Image : ', li)

    return min(degree)


if __name__ == '__main__':
    # path = './test/'
    calculate_his()

    # test
    # path = r'test/TEST%d/%d.JPG'
    # for i in range(1, 7):
    #     print('test_case_%d: %.3f' % (i, calc_similar_by_path('test/TEST%d/%d.JPG' % (i, 1), 'test/TEST%d/%d.JPG' % (i, 2))))
    # make_doc_data('test/TEST4/1.jpg', 'test/TEST4/2.jpg')

    # test
    # data = ["data3", "data4","data5","data6"]
    # write_excel(data, "test.xls", "degree1")
    # write_excel(data, "test.xls", "degree2")
    # write_excel(data, "test.xls", "degree3")
