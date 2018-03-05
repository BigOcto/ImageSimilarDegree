from collections import namedtuple

from siftsimilar import sift_calculate
from histsimilar import calculate_his
from histsimilar import calculate_his
from excel_operation import read_excel_data_by_col, write_excel
from os.path import join, isfile, isdir, splitext, basename, abspath
from os import walk
from excel_operation import write_excel
import sys

# Results of calculate two images
DEGREE = namedtuple('DEGREE', ['source', 'target', 'degree'])


def get_count(num):
    return (num - 1 + 1) * (num - 1) / 2


def do_calculate(path, need_write_excel=None):
    file_array = list()
    for root, dirs, files in walk(path):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                file_array.append(join(root, file))
    print(path, "总文件数： ", len(file_array))
    calculate_times = get_count(len(file_array))
    calculate_count = 0
    results = []
    for i in range(len(file_array)):
        for j in range(i + 1, len(file_array)):
            similarity_degree = calculate_his(file_array[i], file_array[j])
            calculate_count += 1
            str1 = "\r \r {0}/{1} {2:.3} %".format(calculate_count + 1, calculate_times,
                                                   ((1 + calculate_count) * 100 / calculate_times))
            sys.stdout.write(str1)
            sys.stdout.flush()

            if need_write_excel:
                if len(results) >= 1000:
                    sour = []
                    tar = []
                    de = []
                    for re in results:
                        sour.append(re.source)
                        tar.append(re.target)
                        de.append(str(re.degree))
                    write_excel(sour, "Image_similarity_degree2.xls", "SOUCE_1")
                    write_excel(tar, "Image_similarity_degree2.xls", "SOUCE_2")
                    write_excel(de, "Image_similarity_degree2.xls", "DEGREE3")
                    results.clear()

                if similarity_degree > 0.99999:
                    print("%s ** %s : %.3f" % (abspath(file_array[i]), abspath(file_array[j]), similarity_degree))
                    results.append(DEGREE(
                        source=abspath(file_array[i]),
                        target=abspath(file_array[j]),
                        degree=similarity_degree
                    ))
            else:
                print("\n%s ** %s : %.3f" % (abspath(file_array[i]), abspath(file_array[j]), similarity_degree))
    if len(results) > 0:
        sour = []
        tar = []
        de = []
        for re in results:
            sour.append(re.source)
            tar.append(re.target)
            de.append(str(re.degree))
        write_excel(sour, "Image_similarity_degree2.xls", "SOUCE_1")
        write_excel(tar, "Image_similarity_degree2.xls", "SOUCE_2")
        write_excel(de, "Image_similarity_degree2.xls", "DEGREE3")
        results.clear()


if __name__ == '__main__':
    do_calculate('/Users/zhangyu/Desktop/QYVideoClient-debug/res', True)
    # do_calculate('/Users/zhangyu/PycharmProjects/ImageSimilarDegree/test-res/TEST8', True)
    # sift_calculate('/Users/zhangyu/PycharmProjects/histsimilar/imgsearch/test-res/TEST4/1.png',
    #                '/Users/zhangyu/Desktop/QYVideoClient-debug/res/drawable-xhdpi-v4/player_land_setting_guide_bg_new.9.png')

    #####
    # image_list = read_excel_data_by_col("SOUCE_1", 0, "Image_similarity_degree.xls")
    # target_list = read_excel_data_by_col("SOUCE_2", 0, "Image_similarity_degree.xls")
    # degree = []
    # for i in range(1, len(image_list)):
    #     print(image_list[i])
    #     print(target_list[i])
    #     degree.append(sift_calculate(image_list[i], target_list[i]))
    # write_excel(degree, "Image_similarity_degree.xls", "DEGREE_BY_SIFT")
