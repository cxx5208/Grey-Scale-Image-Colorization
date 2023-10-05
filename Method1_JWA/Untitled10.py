#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from PIL import Image
import os, sys
from data_generator import *


path = "F:/mtech/base_implementation/images/val/class/"
dirs = os.listdir( path )
split_data()
def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((256,256), Image.ANTIALIAS)
            imResize.save( 'F:/mtech/base_implementation/images/val1/'+str(item), 'PNG', quality=90)

resize()

