## Code for "Mapping Cropping Intensity by Identifying Bare Soil Occurrence from Sentinel-2 Time Series"
### Contact details: yuyanghuang@zju.edu.cn; su.ye@zju.edu.cn
'CIbaresoil.py' is the script of the package of calculating cropping intensity based on bare soil occurrence.  

The input parameters of the package include:   

pixel_arr: a two-dimensional array containing values from different dates and different bands  
date: an array containing values of days from Jan 1, 1970  
B2: an array containing values of blue band  
B3: an array containing values of green band  
B4: an array containing values of red band  
B8: an array containing values of NIR band  
B11: an array containing values of SWIR1 band  
B12: an array containing values of SWIR2 band  
MSK_CLDPRB: an array containing values of MSK_CLDPRB band  
qa_60: an array containing values of QA60 band  
SCL: an array containing values of SCL band  
NDVI_thre: the threshold of NDVI to extract bare soil  
NBR2_thre: the threshold of NBR2 to extract bare soil  
Test_window: the temporal window for testing the ephemeral bare soil  
N_DAYS: the lower limit of crop growth period  

'main.py' is the script of an example to calculate the cropping intensity using the 'CIbaresoil' package.  

The 'demoforsinglecropping.xls' and 'demofordoublecropping.xls' can be used for the example.
