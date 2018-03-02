from siftsimilar import sift_calculate
from histsimilar import do_calculate
from histsimilar import calculate_his
from excel_operation import read_excel_data_by_col, write_excel

if __name__ == '__main__':
    # do_calculate('/Users/zhangyu/PycharmProjects/histsimilar/imgsearch/test-res/TEST6')
    calculate_his('/Users/zhangyu/PycharmProjects/histsimilar/imgsearch/test-res/TEST5/1.jpg',
                  '/Users/zhangyu/PycharmProjects/histsimilar/imgsearch/test-res/TEST5/2.jpg')
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