from hashlib import md5


def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()


if __name__ == '__main__':
    md5_1 = md5_file('/Users/zhangyu/PycharmProjects/ImageSimilarDegree/test-res/TEST8/1.png')
    md5_2 = md5_file('/Users/zhangyu/PycharmProjects/ImageSimilarDegree/test-res/TEST8/2.png')
    if md5_1 == md5_2:
        print("equal")
    else:
        print("not equal")
    
