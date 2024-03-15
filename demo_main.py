# -*- coding: utf-8 -*-
"""
@author: Yuyang Huang, yuyanghuang@zju.edu.cn

This script is an example of a pixel for calculating cropping intensity 
using the 'CIcalculate' function in the 'CIbaresoil' package.

As preparation, you need to download Sentinel-2 L2A images from 2020.01.01 to 
2023.01.01, especially for B2, B3, B4, B8, B11, B12, MSK_CLDPRB, QA60, SCL bands.

The 'demoforsinglecropping.csv' and 'demofordoublecropping.csv' can be used for 
the demo.

"""

import pandas as pd
import datetime
import numpy as np
from CIbaresoil import CIcalculate

if __name__ == '__main__':
    
    # demo for using the 'CIcalculate' function
    
    pixel_arr_dir = r'E:\huangyuyang\baresoilovertime2\demoforsinglecropping.csv'
    pixel_pd = pd.read_csv(pixel_arr_dir)
    pixel_arr = pixel_pd.values
    
    # sort by date
    sorted_idx = np.argsort(pixel_arr[:,0])
    pixel_arr = pixel_arr[sorted_idx]
    
    # bands
    date, B2, B3, B4, B8, B11, B12, MSK_CLDPRB, qa_60, SCL = pixel_arr[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]].T
    NDVI_thre = 0.25
    NBR2_thre = 0.225
    Test_window = 10
    N_DAYS = 70
    
    # output result array
    result_arr = CIcalculate(pixel_arr, date, B2, B3, B4, B8, B11, B12, MSK_CLDPRB, qa_60, SCL, NDVI_thre, NBR2_thre, Test_window, N_DAYS)
    print(result_arr[0]) # result_arr[0]: the cropping intensity of the pixel
    print(result_arr[1]) # result_arr[1]: beginning time of soil exposure
    print(result_arr[2]) # result_arr[2]: end time of soil exposure

    