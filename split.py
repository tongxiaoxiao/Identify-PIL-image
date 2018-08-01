#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PIL import Image
import uuid

def convert_image(image):
    image=image.convert('L')
    image2=Image.new('L',image.size,255)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if pix<120:
                image2.putpixel((x,y),0)
    return image2

def cut_image(image):
    inletter=False#每个数字开始位置
    foundletter=False#结束位置

    letters=[]#存储坐标，存储五个坐标letters[0]...letters[4]
    start=0
    end=0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if(pix==0):
                inletter=True
        if foundletter==False and inletter ==True:
            foundletter=True
            start=x
        if foundletter==True and inletter==False:
            end=x
            letters.append((start,end))
            foundletter=False
        inletter=False

    images=[]#存储切割后的图像,其中有五张图片，分别为五个字符
    for letter in letters:
        img=image.crop((letter[0],0,letter[1],image.size[1]))#image.crop(x0,y0,x1,y1)
        images.append(img)
    for image in images:
        new_image_filename = './new/' + str(uuid.uuid4()) + '.jpeg'
        image.save(new_image_filename)
    return images

if __name__ == '__main__':
    for i in range(0,500):
        image = Image.open('./image/%s.jpg' % i)
        image = convert_image(image)
        images = cut_image(image)
    #for i in images:
        #image.save('./new/%s.jpg' % i)
'''
def main():
    for filename in os.listdir('image'):
        current_file = 'image/' + filename
        if os.path.isfile(current_file):
            convert_image(current_file)
            cut_image(current_file)
            print 'split file:%s'%current_file

if __name__ == '__main__':
    main()
'''
