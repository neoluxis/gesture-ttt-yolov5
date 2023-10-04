import cv2 as cv


def take_photo():
    cam = cv.VideoCapture(2)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    img_num = 0
    labels = [
        "stone",
        "scissors",
        "paper"
    ]
    li = 0
    filepath = f"hand/{labels[li]}_"
    while True:
        ret, img = cam.read()
        cv.imshow("test", img)
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite(f'{filepath}{img_num}.jpg', img)
            img_num += 1
            print(f"save {filepath}{img_num}.jpg")
        if k == ord('a'):
            li += 1
            if li >= len(labels):
                li = 0
            filepath = f"hand/{labels[li]}_"
            print(f"Switch to label {labels[li]}")
        if k == ord('q'):
            print(f"Exit\n"
                  f"Total {img_num} images saved")
            break


def get_sets():
    import os
    import random
    import argparse

    parser = argparse.ArgumentParser()
    # xml文件的地址，根据自己的数据进行修改 xml一般存放在Annotations下
    parser.add_argument('--xml_path', default='VOC2012/Annotations/',
                        type=str, help='input xml label path')
    # 数据集的划分，地址选择自己数据下的ImageSets/Main
    parser.add_argument('--txt_path', default='VOC2012/ImageSets/Main/',
                        type=str, help='output txt label path')
    opt = parser.parse_args()

    trainval_percent = 0.80
    train_percent = 1.0
    xmlfilepath = opt.xml_path
    txtsavepath = opt.txt_path
    total_xml = os.listdir(xmlfilepath)
    if not os.path.exists(txtsavepath):
        os.makedirs(txtsavepath)

    num = len(total_xml)
    list_index = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list_index, tv)
    train = random.sample(trainval, tr)

    file_trainval = open(txtsavepath + 'trainval.txt', 'w')
    file_test = open(txtsavepath + 'test.txt', 'w')
    file_train = open(txtsavepath + 'train.txt', 'w')
    file_val = open(txtsavepath + 'val.txt', 'w')

    for i in list_index:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            file_trainval.write(name)
            if i in train:
                file_train.write(name)
            else:
                file_val.write(name)
        else:
            file_test.write(name)

    file_trainval.close()
    file_train.close()
    file_val.close()
    file_test.close()


def voc_label():
    import xml.etree.ElementTree as ET
    import os
    from os import getcwd

    sets = ['train', 'val', 'test']
    classes = ["stone", "scissor", "paper"]
    abs_path = os.getcwd()
    print(abs_path)

    def convert(size, box):
        dw = 1. / (size[0])
        dh = 1. / (size[1])
        x = (box[0] + box[1]) / 2.0 - 1
        y = (box[2] + box[3]) / 2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return x, y, w, h

    def convert_annotation(image_id):
        in_file = open('/home/neolux/Documents/pytorch/gesture/VOC2012/Annotations/%s.xml' % image_id,
                       encoding='UTF-8')
        out_file = open('/home/neolux/Documents/pytorch/gesture/VOC2012/labels/%s.txt' % image_id, 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            # difficult = obj.find('difficult').text
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            b1, b2, b3, b4 = b
            # 标注越界修正
            if b2 > w:
                b2 = w
            if b4 > h:
                b4 = h
            b = (b1, b2, b3, b4)
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    wd = getcwd()
    for image_set in sets:
        if not os.path.exists('/home/neolux/Documents/pytorch/gesture/VOC2012/labels/'):
            os.makedirs('/home/neolux/Documents/pytorch/gesture/VOC2012/labels/')
        image_ids = open(
            '/home/neolux/Documents/pytorch/gesture/VOC2012/ImageSets/Main/%s.txt' % image_set).read().strip().split()
        # list_file = open('%s.txt' % image_set, 'w')
        # for image_id in image_ids:
        #     list_file.write(abs_path + '/VOC2012/images/%s.jpg\n' % (image_id))
        #     convert_annotation(image_id)
        # list_file.close()
        with open(f"VOC2012/ImageSets/Main/{image_set}.txt", 'w') as f:
            for image_id in image_ids:
                convert_annotation(image_id)
                f.write(f"{abs_path}/VOC2012/images/{image_id}.jpg\n")


if __name__ == "__main__":
    get_sets()
    voc_label()
