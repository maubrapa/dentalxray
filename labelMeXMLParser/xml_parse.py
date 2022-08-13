# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 11:51:49 2022

@author: maubrapa
"""

import xml.etree.ElementTree as et
import glob
import os
from PIL import Image, ImageDraw

#  --------------------------------------------
def parsePolygon(etelem):
    points = []
    for pt in etelem.findall('pt'):
        num = pt.find('x').text
        if '.' in num: 
            tx = int(float(num))
        else:
            tx = int(num)
        num = pt.find('y').text
        if '.' in num:
            ty = int(float(num))
        else:
            ty = int(num)
        points.append(tx)
        points.append(ty)
    return points

def getImg(imageDir, imgFileName):
    # imagePath = os.path.join(imageDir) + '/*.jpg'
    imgFullPath = os.path.join(imageDir) + imgFileName
    img = Image.open(imgFullPath)
    #image size
    width = img.size[0]
    height = img.size[1]
    return img, width, height

def parseLabeledObjects(root, maskDir, maskVizDir, imageDir):
    file_name = root.findall('filename')[0].text
    polygon = []
    name_list = []

    for lmobj in root.findall('object'):
        # deleted = lmobj.find('deleted').text.encode('utf-8').strip()
        deleted = lmobj.find('deleted').text.strip()
        if deleted=='1':
            continue

        nameobj = lmobj.find('name')
        if nameobj.text is None:
            continue

        # inserted by maubrapa - mai 23th
        if nameobj.text != 'tooth':
        # if nameobj.text == 'restoration':
            name = nameobj.text
            name_list.append(name)
            
            properties = {}
            for attrib in lmobj.findall('attributes'):
                if not attrib.text: break
                properties[ attrib.text.encode('utf-8').strip() ] = ''
            polygon.append( parsePolygon( lmobj.find('polygon') ))
        else:
            continue
        
    [myimg, sx, sy] = getImg(imageDir, file_name)

    # set mask values for train
    color_background = 'black'
    color_outline = color_background
    
    img = Image.new("RGB", [sx, sy], color_background )
    imgViz = Image.new("RGB", [sx, sy], color_background )

    for poly,name in zip(polygon,name_list):
        print(name)
        labelColor = getIndex(labels, name) # get index to set mask value and imgviz color
        # print("labelColor: ", labelColor)
        label_color=(labelColor,labelColor,labelColor)
        # print("label color", label_color)

        if (len(poly) < 3): continue

        # create mask
        ImageDraw.Draw(img).polygon(poly, outline=color_outline, fill=label_color)
        
        # create maskviz
        color = colors[labelColor]
        ImageDraw.Draw(imgViz).polygon(poly, outline=color, fill=color)

    if len(name_list) != 0:
        # save image mask
        file_name1 = maskDir + file_name
        gray_scale = img.convert("L")
        gray_scale.save(file_name1.replace('.jpg','.png'), "PNG")

        # save imageviz mask
        file_name2 = maskVizDir + file_name
        imgViz.save(file_name2.replace('.jpg','.png'), "PNG")

def parseFolder( localDir, maskDir, maskVizDir, imageDir):
    fsAnnotPath = os.path.join(localDir) + '/*.xml'
    print(fsAnnotPath)                  
    for fsAnnotFullpath in glob.glob( fsAnnotPath ):
        print(fsAnnotFullpath)
        # parse the XML file on the file system
        tree = et.parse( fsAnnotFullpath )
        root = tree.getroot()
        print(root)
        if not (os.path.exists(maskDir)):
            os.mkdir(maskDir)
        if not (os.path.exists(maskVizDir)):
            os.mkdir(maskVizDir)
        parseLabeledObjects(root, maskDir, maskVizDir, imageDir)

def combineMaskImage(maskDir,imageDir,maskImageComb):
    maskPath = os.path.join(maskDir) + '/*.png'
    imagePath = os.path.join(imageDir) + '/*.jpg'
    print('>>> Combined mask <<<')

    for maskFullPath, imageFullpath in zip(glob.glob( maskPath ), glob.glob( imagePath ) ):
        maskImg = Image.open(maskFullPath)
        name = maskFullPath.replace(maskDir, imageDir )
        name = name.replace('.png','.jpg')
        origImg = Image.open(name) 

        maskImg = maskImg.convert("RGBA")
        origImg = origImg.convert("RGBA")

        new_img = Image.blend(origImg,maskImg, 0.4)
        
        if not (os.path.exists(maskImageComb)):
            os.mkdir(maskImageComb)            

        file_name = maskFullPath.replace(maskDir,maskImageComb )
        # file_name = file_name.replace('.png','.jpg')
        print(file_name)
        new_img.save(file_name)

def getIndex(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
            return i+1
    return -1

# ------------------------------------------------------
maskDir = './outputMasks/'
maskVizDir = './outputMaskviz/'
maskImageComb = './outputCombined/'

xmlFolder='./inputAnnotations/'
inputImgs = './inputImages/'


labels = ['root canal treatment', 'restoration', 'crown', 'dental implant']
#labels = ['restoration','background']
colors = ["green", "tomato", "blue", "yellow", "purple", "orange", "white"]

# -------------------------------------

if __name__ == "__main__":
    parseFolder(xmlFolder, maskDir, maskVizDir, inputImgs)
    combineMaskImage(maskVizDir, inputImgs, maskImageComb)