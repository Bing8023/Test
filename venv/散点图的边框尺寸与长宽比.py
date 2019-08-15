# -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from PIL import Image
def parse_obj(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    return objects
def read_image(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    size = tree.find('size')
    weight = int(size.find('width').text)
    height1 = int(size.find('height').text)
    return weight, height1
if __name__ == '__main__':
    width = []
    height = []
    xml_path = '../Annotations/'
    filenames = os.listdir(xml_path)
    recs = {}
    ims_info = {}
    obs_shape = {}
    for i, name in enumerate(filenames):
        recs[name] = parse_obj(xml_path, name)
        ims_info[name] = read_image(xml_path, name)
    for name in filenames:
        im_w = ims_info[name][0]
        im_h = ims_info[name][1]
        for object in recs[name]:
            ob_w = object['bbox'][2] - object['bbox'][0]
            ob_h = object['bbox'][3] - object['bbox'][1]
            w_rate = ob_w / im_w
            h_rate = ob_h / im_h
            width.append(w_rate)
            height.append(h_rate)
    x = np.array(width)
    y = np.array(height)
    fig = plt.figure(0)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('The rate of Border Size and Length')
    plt.scatter(x, y, c='red', alpha=1, marker='.', label=u'样本')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()
