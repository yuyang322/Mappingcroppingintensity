# -*- coding: utf-8 -*-
"""
@author: Yuyang Huang, yuyanghuang@zju.edu.cn

This script is an example of a pixel for calculating cropping intensity and 
exporting the beginning and end time of soil exposed using the CIbaresoil package
As preparation, you need to download Sentinel-2 L2A images from 2020.01.01 to 
2023.01.01, especially for B2, B3, B4, B8, B11, B12, MSK_CLDPRB, QA60, SCL bands.

The 'demoforsinglecropping.xls' and 'demofordoublecropping.xls' can be used for 
the example.
"""

import pandas as pd
import datetime
import numpy as np
import CIbaresoil

if __name__ == '__main__':
    # demo for using the CIbaresoil package
    pixel_arr_dir = r'E:\huangyuyang\baresoilovertime2\point_demo3.xls'
    pixel_pd = pd.read_excel(pixel_arr_dir)
    pixel_arr = pixel_pd.values
    
    # sort by date
    sorted_idx = np.argsort(pixel_arr[:,0])
    pixel_arr = pixel_arr[sorted_idx]
    
    # bands
    date = pixel_arr[:,0] # the date is the number of days from Jan 1, 1970
    B2 = pixel_arr[:,1]
    B3 = pixel_arr[:,2]
    B4 = pixel_arr[:,3]
    B8 = pixel_arr[:,4]
    B11 = pixel_arr[:,5]
    B12 = pixel_arr[:,6]
    MSK_CLDPRB = pixel_arr[:,7]
    qa_60 = pixel_arr[:,8]
    SCL = pixel_arr[:,9]
    NDVI_thre = 0.25
    NBR2_thre = 0.225
    Test_window = 10
    N_DAYS = 70
    
    # output result array
    # result_arr[0]: the cropping intensity of the pixel
    # result_arr[1]: time of beginning of soil exposure
    # result_arr[2]: time of end of soil exposure
    
    result_arr = CIbaresoil.CIcalculate(pixel_arr, date, B2, B3, B4, B8, B11, B12, MSK_CLDPRB, qa_60, SCL, NDVI_thre, NBR2_thre, Test_window, N_DAYS)
    # print(result_arr[0])
    # print(result_arr[1])
    # print(result_arr[2])
    
    # output to xls
    out_dir = r'E:\huangyuyang\baresoilovertime2\output_demo3.xls'
    result_df = pd.DataFrame(result_arr)
    result_df.to_excel(out_dir, index=False)
    