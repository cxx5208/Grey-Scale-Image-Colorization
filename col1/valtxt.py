#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import random
from random import shuffle

from PIL import Image
import os, sys
def split_data():
    names = [f for f in os.listdir('F:/mtech/col1/dataset/train/')]
    
    num_valid_samples = len(names)
    print(num_valid_samples)

    
    valid_names = random.sample(names, num_valid_samples)
    
    with open('valid_names.txt', 'w') as file:
        file.write('\n'.join(valid_names))


if __name__ == '__main__':
    split_data()