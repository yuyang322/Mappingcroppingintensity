# -*- coding: utf-8 -*-
"""
@author: Yuyang Huang, yuyanghuang@zju.edu.cn

It is the script of the package of calculating cropping intensity based on bare soil occurrence.
This script has 5 steps: 1) add a doy (day of year) band according to date band;
2) use quality control bands to remove the effect of clouds and other invalid values;
3) extract bare soil using GEOS3 method; 4) modify time series of bare soil occurrence 
with two steps; 5) calcute the cropping intensity and export the beginning and end time 
of soil exposed.
The package is uesd for pixel by pixel calculation.

"""

import pandas as pd
import datetime
import numpy as np


def CIcalculate(
        pixel_arr: np.ndarray,
        date: np.ndarray,
        B2: np.ndarray,
        B3: np.ndarray,
        B4: np.ndarray,
        B8: np.ndarray,
        B11: np.ndarray,
        B12: np.ndarray,
        MSK_CLDPRB: np.ndarray,
        qa_60: np.ndarray,
        SCL: np.ndarray,
        NDVI_thre: float,
        NBR2_thre: float,
        Test_window: int,
        N_DAYS: int,
        ):
    
    # add day of year(doy) band
    doy_list = []
    for d in date:
        date_d = datetime.datetime(1970,1,1) + datetime.timedelta(days=int(d))
        doy = date_d.timetuple().tm_yday
        doy_list.append([doy])
    doy = np.array(doy_list)

    
    # mask clouds
    mask1 = MSK_CLDPRB < 30
    qa_60 = qa_60.astype(int)
    opaqueclouds = 1 << 10
    cirrusclouds = 1 << 11
    mask2 = (qa_60 & opaqueclouds == 0) & (qa_60 & cirrusclouds == 0)
    clouds_mask = mask1 & mask2
    
    # SCL select
    defective = 1
    shadow = 3
    cirrus = 10
    snow = 11
    darkArea = 2
    water = 6
    scl_mask = ~(np.logical_or.reduce([SCL == defective, SCL == shadow, SCL == cirrus, SCL == snow, SCL == darkArea, SCL == water]))
    
    # extract bare soil with GEOS3 method
    ndvi = (B8 - B4) / (B8 + B4)
    nbr2 = (B11 - B12) / (B11 + B12)
    optical1 = B3 - B2
    optical2 = B4 - B3
    baresoil_mask = (ndvi < NDVI_thre) & (nbr2 < NBR2_thre) & (optical1 > 0) & (optical2 > 0)
    
    # obtain baresoil stack
    n = B2.shape[0]
    barevalue_list = []
    for i in range(n):
        if(~clouds_mask[i] | ~scl_mask[i]):
            bare_value = 0
        if(clouds_mask[i] & scl_mask[i]):
            if(baresoil_mask[i]):
                bare_value = 2
            else:
                bare_value = 1
        barevalue_list.append([bare_value])
    
    bare_arr = np.array(barevalue_list).astype(int)
    date_arr = date.reshape(-1,1).astype(int)
    doy_arr = doy.reshape(-1,1).astype(int)
    baresoil_stack = np.hstack((bare_arr,date_arr,doy_arr))
    
    
    # CIcalculate
    or_value = baresoil_stack[:,0]
    or_date = baresoil_stack[:,1]
    or_doy = baresoil_stack[:,2]

    mask0 = baresoil_stack[:,0] != 0
    value = or_value[mask0]
    date = or_date[mask0]
    doy = or_doy[mask0]

    if value.shape[0] >= 3:
        # temporal sieving filter
        for i in range(1, value.shape[0] - 1):
            if value[i] == 1 and value[i - 1] == 2 and value[i + 1] == 2:
                value[i] = 2
        # ephemeral soil test
        for i in range(1, value.shape[0] - 1):
            if value[i] == 2 and value[i - 1] == 1 and value[i + 1] == 1:
                doy_i = doy[i]
                year = date[i] // 366
                for j in range(0, value.shape[0]):
                    if value[j] == 2 and (doy[j] >= doy_i - Test_window or doy[j] <= doy_i + Test_window) and (date[j] // 366) != year:
                        value[i] = 2
                    else:
                        value[i] = 1
        # growth cycle number
        value_shift = np.roll(value,1)
        value_shift[0] = value[0]
        value_diff = value_shift - value
        value_partition = np.split(value, np.where(value_diff != 0)[0])
        date_partition = np.split(date, np.where(value_diff != 0)[0])
        cycle_number = 0
        for i in range(len(value_partition)):
            if (np.unique(value_partition[i]) == 1) and (date_partition[i][-1] - date_partition[i][0] >= N_DAYS):
                cycle_number += 1
        ci = cycle_number / 3
        output_ci = 0
        if 0<ci<=1:
            output_ci = 1
        elif 1<ci<=2:
            output_ci = 2
        elif 2<ci<=3:
            output_ci = 3
        # soil exposed time
        if output_ci != 0:
            bare_start_idx = np.where(value_diff == -1)[0]
            bare_start_list = list(date[bare_start_idx])
            bare_end_idx = np.where(value_diff == 1)[0] - 1
            bare_end_list = list(date[bare_end_idx])
        else:
            bare_start_list = [0]
            bare_end_list = [0]
        
    else:
        output_ci = 0
        bare_start_list = [0]
        bare_end_list = [0]
    
    output_ci_list = [output_ci]
    result_arr = np.array([
        output_ci_list,
        bare_start_list,
        bare_end_list
        ],dtype=object)
    return result_arr