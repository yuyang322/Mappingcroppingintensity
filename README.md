## Code for "Mapping Cropping Intensity by Identifying Bare Soil Occurrence from Sentinel-2 Time Series"
### Contact details: yuyanghuang@zju.edu.cn; su.ye@zju.edu.cn

### 1. Using CIbaresoil to calculate cropping intensity
**'CIcalculate'** is the function to calculate cropping intensity based on bare soil occurrence in [CIbaresoil.py](https://github.com/yuyang322/Mappingcroppingintensity/blob/main/CIbaresoil.py):  
```python
from CIbaresoil import CIcalculate  
return_arr = CIcalculate(pixel_arr, date, B2, B3, B4, B8, B11, B12, MSK_CLDPRB, qa_60, SCL, NDVI_thre, NBR2_thre, Test_window, N_DAYS)
```

The input parameters and the return of the function:   
```python
    """
    Parameters
    ----------
    pixel_arr : np.ndarray
        a two-dimensional array containing values from different dates and different bands.
    date : np.ndarray
        an array containing values of days from Jan 1, 1970.
    B2 : np.ndarray
        an array containing values of blue band.
    B3 : np.ndarray
        an array containing values of green band.
    B4 : np.ndarray
        an array containing values of red band.
    B8 : np.ndarray
        an array containing values of NIR band.
    B11 : np.ndarray
        an array containing values of SWIR1 band.
    B12 : np.ndarray
        an array containing values of SWIR2 band.
    MSK_CLDPRB : np.ndarray
        an array containing values of MSK_CLDPRB band.
    qa_60 : np.ndarray
        an array containing values of QA60 band.
    SCL : np.ndarray
        an array containing values of SCL band.
    NDVI_thre : float
        the threshold of NDVI to extract bare soil.
    NBR2_thre : float
        the threshold of NBR2 to extract bare soil.
    Test_window : int
        the temporal window for testing the ephemeral bare soil.
    N_DAYS : int
        the lower limit of crop growth period.

    Returns
    -------
    result_arr : np.ndarray
        result_arr[0]: the cropping intensity of the pixel.
        result_arr[1]: beginning time of soil exposure.
        result_arr[2]: end time of soil exposure.

    """
```

### 2. Preparation and operation
* Downloading Sentinel-2 L2A images of required bands.
* Adding the date band:
  ```python
  from datetime import datetime
  origin_date = datetime.strptime('19700101', '%Y%m%d')
  target_date = datetime.strptime(time_str, '%Y%m%d')
  date = (target_date - origin_date).days + 1
  ```
* A demo for calculation of one pixel: [demo_main.py](https://github.com/yuyang322/Mappingcroppingintensity/blob/main/demo_main.py)  
  [demoforsinglecropping.csv](https://github.com/yuyang322/Mappingcroppingintensity/blob/main/demoforsinglecropping.csv) and [demofordoublecropping.csv](https://github.com/yuyang322/Mappingcroppingintensity/blob/main/demofordoublecropping.csv) can be used as the input of the demo

