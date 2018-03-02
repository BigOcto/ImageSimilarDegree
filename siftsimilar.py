import PIL
import numpy
import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from numpy.core.tests.test_mem_overlap import xrange

MIN_MATCH_COUNT = 10


def make_regalur_image(img, size=(256, 256)):
    pil_image = PIL.Image.open(img)
    return cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_BGR2RGB)

def sift_calculate(query_image, train_image):
    # img1 = cv2.imread('/Users/zhangyu/PycharmProjects/histsimilar/imgsearch/test/TEST2/1.JPG', 0)  # queryImage
    # img2 = cv2.imread('/Users/zhangyu/PycharmProjects/histsimilar/imgsearch/test/TEST2/2.JPG', 0)  # trainImage
    img1 = cv2.imread(query_image, -1)  # queryImage
    img2 = cv2.imread(train_image, -1)  # trainImage
    # img1 = make_regalur_image(query_image)  # queryImage
    # img2 = make_regalur_image(train_image)  # trainImage

    print('RGB shape: ', img1.shape)
    print(img1)
    print(img1.dtype)

    if img1 is None:
        print('query image is None')
        return -0.1
    elif img2 is None:
        print('train image is None')
        return -0.1
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    if des1 is None:
        print('query image read kp None')
        return -0.1
    elif des2 is None:
        print('train image read kp None')
        return -0.1
    else:
        print('des1:', len(des1), 'keypoint :', len(kp1))
        print('des2:', len(des2), 'keypoint :', len(kp2))
    if len(kp1) >= 2 and len(kp2) >= 2:
        matches = flann.knnMatch(des1, des2, k=2)
    else:
        return -0.3
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    print('match count :', len(good))
    degree_query = float('%.2f' % (len(good) / len(kp1) * 100))
    degree_train = float('%.2f' % (len(good) / len(kp2) * 100))
    if degree_query > degree_train:
        print('match degree query:', degree_query)
        return degree_query
    else:
        print('match degree query:', degree_train)
        return degree_train

        # if len(good) > MIN_MATCH_COUNT:
        #     src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        #     dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        #
        #     M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        #     matchesMask = mask.ravel().tolist()
        #
        #     h, w = img1.shape
        #     pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        #     dst = cv2.perspectiveTransform(pts, M)
        #
        #     img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
        #
        # else:
        #     print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
        #     matchesMask = None
        #
        # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
        #                    singlePointColor=None,
        #                    matchesMask=matchesMask,  # draw only inliers
        #                    flags=2)
        #
        # img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        # plt.imshow(img3, 'gray'), plt.show()


# matchesMask = [[0, 0] for i in xrange(len(matches))]
#
# # ratio test as per Lowe's paper
# for i, (m, n) in enumerate(matches):
#     if m.distance < 0.7 * n.distance:
#         matchesMask[i] = [1, 0]
# print(len(matchesMask))
# draw_params = dict(matchColor=(0, 255, 0),
#                    singlePointColor=(255, 0, 0),
#                    matchesMask=matchesMask,
#                    flags=0)
#
# img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
#
# plt.imshow(img3, ), plt.show()

if __name__ == '__main__':
    # path = './test/'
    sift_calculate('/Users/zhangyu/PycharmProjects/histsimilar/imgsearch/test-res/TEST6/1.png',
                   '/Users/zhangyu/PycharmProjects/histsimilar/imgsearch/test-res/TEST6/2.png')
