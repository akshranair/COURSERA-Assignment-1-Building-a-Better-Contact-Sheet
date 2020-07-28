#!/usr/bin/env python
# coding: utf-8

# In[1]:


import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np
from PIL import ImageDraw
from IPython import display
from zipfile import ZipFile
from PIL import Image
from IPython.display import display
# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!


# In[16]:


images_name=[]
with ZipFile('readonly/images.zip', 'r') as zipObj:
    listOfiles = zipObj.infolist()
    for i in listOfiles:
        images_name.append(i.filename)
        print("done",i.filename)


# In[17]:


big_list=[] #list that contain another which contains the string extracted from each image in images list
for eachimage in images_name:
    small_list=[] #a list which contains the list of strings extracted using pytesseract
    
    small_list.append(eachimage)#adding the name of the file
    
    small_list.append(pytesseract.image_to_string(eachimage).replace('\n',''))
    
    big_list.append(small_list)
    print('done',eachimage)


# In[39]:


def get_faces(image_name):
    img=np.array(image_name)#converting into numpy array
    faces = face_cascade.detectMultiScale(img,1.35,4)#scale factor =1.35 and min neighbours =4
    faces=faces.tolist()
    return faces


# In[37]:


def lookup(text):
    for small_list in big_list:
        if text in small_list[1]:                           #checking if the provided text is in the small list
            print('Results found in file',small_list[0])   
            image_name=small_list[0]                        #if true then the name of the image is stored

            pil_img=Image.open(image_name)
            try:
                face=get_faces(pil_img)                        #calling the function get_faces
                each_face=[]
                for x,y,w,h in face:
                    each_face.append(pil_img.crop((x,y,x+w,y+h)))
                    contact_sheet = Image.new(pil_img.mode, (550,110*int(np.ceil(len(each_face)/5)))) #layout of contact sheet 
                    x = 0
                    y = 0
                    for face in each_face:
                        face.thumbnail((110,110)) #converting cropped faces into thumbnail
                        contact_sheet.paste(face, (x, y))
                        if x+110 == contact_sheet.width:
                            x=0
                            y=y+110
                        else:
                            x=x+110
                display(contact_sheet)       
            except:
                print("No face detected") #if faces are not detected


# In[40]:


lookup("Mark")


# In[25]:


lookup("Christopher")

