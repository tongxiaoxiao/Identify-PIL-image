#coding:utf-8

import os
from PIL import Image
import math
#将图片转换成L模式且黑白像素图片，
def convert_image(image):
    image=image.convert('L')
    image2=Image.new('L',image.size,255)
    for x in range(image.size[0]):#原长
        for y in range(image.size[1]):#原宽
            pix=image.getpixel((x,y))
            if pix<120:
                image2.putpixel((x,y),0)#在image2指定位置(x,y)处画一像素0
    return image2#黑白

def cut_image(image):
    inletter=False#数字开始
    foundletter=False#结束
    letters=[]#五个切割图的坐标
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

    images=[]#五个切割后图像
    for letter in letters:
        img=image.crop((letter[0],0,letter[1],image.size[1]))#(x0,y0,x1,y1)
        images.append(img)
    return images

def buildvector(image):
    result={}#result字典存储每个切割后的图片的每个像素点的颜色值
    i=0
    for data in image.getdata():
        result[i]=data
        i+=1
    return result

class CaptchaRecognize:
    def __init__(self):
        self.letters=['0','1','2','3','4','5','6','7','8','9']
        self.loadSet()

    def loadSet(self):
        self.imgset=[]
        for letter in self.letters:
            temp=[]
            for img in os.listdir('./data/%s'%(letter)):
                temp.append(buildvector(Image.open('./data/%s/%s'%(letter,img))))
            self.imgset.append({letter:temp})

    #计算向量大小
    def cal(self,vect):
        total = 0
        '''
        y = 0
        n = 0
        o = 0
        '''
        for count,col in vect.items():
        #col是每个像素点的颜色值,每个颜色值看成是一维向量，在被分割的图片中，是160/140/120维向量
        #count是被分割的图片中像素点的个数
            total += col ** 2 #平方和:x1^2+x2^2+x3^2+......xn^2
        '''
           if col == 255:
                y = y + 1
            elif col == 0:
                n = n + 1
            else:
                o = o + 1
        print(y + n)
        print(y)
        print(n)
        print(o)
        print(y + n + o)
        print math.sqrt(total)
        '''
        return math.sqrt(total)#sqrt(x1^2+x2^2+x3^2+......xn^2)

    #计算矢量之间的 cos 值,cos值可以用来计算二者相似度
    def cos(self,vect1, vect2):
        relevance = 0
        topvalue = 0
        for count, i in vect1.items():#count是图片中像素点的个数
            if count in vect2:
                topvalue += i * vect2[count]#两个向量点积:x1y1+x2y2+......+xnyn
        ans = topvalue / (self.cal(vect1) * self.cal(vect2))
        #ans是一个cos值，非常接近1(0.9～)，ans越接近1，表示夹角越接近0度cos0=1
        return ans
    #进行识别
    def recognise(self,image):
        image=convert_image(image)
        images=cut_image(image)
        vectors=[]#每一张切割后的图片都是n维向量，vectors存储n维向量形式
        for img in images:
            vectors.append(buildvector(img))
        result=[]#(pro,letter)
        for vector in vectors:
            pro=[]#pro字符可能性大小序列，存储可能字符的概率大小
            for image in self.imgset:
            #imgset是0～9的每个切割图片的像素点颜色值记录字典{0:[0:,1:,2:,......119:,/139:,/159:]}
                for letter,temp in image.items():
                    #temp是每个图片像素点颜色值记录[0:,1:,2:,......119:,/139:,/159:]
                    relevance=0
                    num=0
                    for img in temp:#固定一个letter，循环的次数是gailetter有几个对比已切割图片
                        #img是固定letter下不同切割对比图片的像素点值
                        relevance+=self.cos(vector,img)#计算矢量之间的 cos 值
                        num+=1
                        #num进行比较的被分割图片模板的数量，
                    relevance=relevance/num
                    pro.append((relevance,letter))
            pro.sort(reverse=True)
            result.append(pro[0])
        return result

#循环验证并输出结果
if __name__ == '__main__':
    imageRecognize=CaptchaRecognize()
    for i in range(3, 4):
        image = Image.open('test%s.jpeg' % i)
        result = imageRecognize.recognise(image)
        string = [''.join(item[1]) for item in result]
        print(string)
