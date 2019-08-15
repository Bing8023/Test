# -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
def parse_obj(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    classname1 = []
    for obj in tree.findall('object'):
        classname = {'digger':[], 'pushdozer':[], 'motocrane':[], 'towercrane':[], 'sanddredge':[], 'fire':[], 'smog':[], 'colorbelts':[],
                     'cementmixer':[], 'pilingmachine':[], 'pumpcar':[]}
        bbox = obj.find('bndbox')
        name1 = obj.find('name').text
        classname[name1] = [int(bbox.find('xmin').text),
                          int(bbox.find('ymin').text),
                          int(bbox.find('xmax').text),
                          int(bbox.find('ymax').text)]

        classname1.append(classname)
    return classname1
def read_image(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    size = tree.find('size')
    weight = int(size.find('width').text)
    height1 = int(size.find('height').text)
    return weight, height1
if __name__ == '__main__':
    width = {'digger': [], 'pushdozer': [], 'motocrane': [], 'towercrane': [], 'sanddredge': [], 'fire': [],
                 'smog': [], 'colorbelts': [],'cementmixer': [], 'pilingmachine': [], 'pumpcar': []}
    height = {'digger': [], 'pushdozer':[], 'motocrane':[], 'towercrane':[], 'sanddredge':[], 'fire':[], 'smog':[], 'colorbelts':[],
                     'cementmixer':[], 'pilingmachine':[], 'pumpcar':[]}
    #image_path = '../JPEGImages/'
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
        for classname in recs[name]:
            for i in classname.keys():
                if classname[i]:
                    ob_w = classname[i][2] - classname[i][0]
                    ob_h = classname[i][3] - classname[i][1]
                    w_rate = ob_w / im_w
                    h_rate = ob_h / im_h
                    width[i].append(w_rate)
                    height[i].append(h_rate)
    i = 1
    fig, ax = plt.subplots(figsize=(18, 9))
    parent_categories = [key2 for key2 in width.keys()]
    colors = iter(cm.rainbow(np.linspace(0, 1, len(parent_categories))))
    plt.xlabel('width')
    plt.ylabel('height')
    plt.title('Rate')
    for parent_category in parent_categories:
        ax.scatter(
                x=np.array(width[parent_category]),
                y=np.array(height[parent_category]),
                color=next(colors),
                label=parent_category
            )
    plt.grid(True)
    plt.legend(loc='best')
    i = i+1
plt.show()
