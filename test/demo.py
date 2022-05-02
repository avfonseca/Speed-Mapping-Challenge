import numpy as np
from cmath import sqrt
from scipy import interpolate
from osgeo import ogr
from osgeo import gdal
from osgeo import osr
from PIL import Image


#no_data = 0
#arr = np.array([[0,0,0,0,0,0,0,0,0],
#                [0,0,2,0,0,0,0,0,0],
#                [0,0,1,0,0,0,0,0,0],
#                [0,0,0,3,0,0,0,0,0],
#                [0,-6,-5,-3,-0,-1,-2,-3,0],
#                [0,0,0,0,0,3,0,0,0],
#                [0,0,0,4,0,0,32,0,0],
#                [0,0,0,0,0,0,0,0,0],
#                [0,0,0,0,0,0,0,0,0]])
#arr_shape = arr.shape

def _in_ellipse(px, x, py, y, a, b, alpha):

    pa = (np.cos(alpha)*(px-x) + np.sin(alpha)*(py-y))/a
    pb = (np.sin(alpha)*(px-x) + np.cos(alpha)*(py-y))/b

    z = pa**2 + pb**2

    if z <= 1: 
            return True
    else:
        return False

def _edge_case(x,y,a,b):
    if((x > a-1 and y > b-1) and (arr_shape[0] - x > a and arr_shape[1] - y > b)):
        return False
    else:
        return True

def null_padding(arr,x,y):
        return np.pad(arr, (x, y), 'constant', constant_values=(no_data, no_data))

def sub_array(x,y,a,b):

    c = max(a,b)

    if(_edge_case(x,y,c,c)):
        temp = null_padding(arr,c,c)
        sub_arr = np.copy(temp[x:x+2*c+1,y:y+2*c+1])
    else:
        sub_arr = np.copy(arr[x-c:x+c+1,y-c:y+c+1])
        
    return sub_arr

   
def find_valid_points(sub_arr,a,b,alpha):

    values = []

    xc = int(sub_arr.shape[0]/2)
    yc = int(sub_arr.shape[1]/2)

    for i in range(sub_arr.shape[0]):
        for j in range(sub_arr.shape[1]):
            if (_in_ellipse(i,xc,j,yc,a,b,alpha) and sub_arr[i,j] != no_data):
                    values.append(sub_arr[i,j])
            else:
                sub_arr[i,j] = np.nan

    return values


def find_area(x,y):
    
    a = 1
    b = 1

    eps = 1

    phase = np.arange(0,360,8)*np.pi/180

    sub = sub_array(x,y,a,b)
    values = find_valid_points(sub,a,b,0)
    max_len = len(values)
    p_out = 0
    
    passes = 0
    while(max_len < 8 and passes < 3):

        a_ = a + eps
        b_ = b + eps
        
        sub_a = sub_array(x,y,a_,b)
        sub_b = sub_array(x,y,a,b_)

        if(np.count_nonzero(sub_a != no_data) + np.count_nonzero(sub_b != no_data) == 0):
            passes = passes + 1

        else:
            if(a_ == b or a == b_):
                sub = sub_array(x,y,a,b)
                values = find_valid_points(sub,a,b,0)
                max_len = len(values)
                p_out = 0

            else:

                a_list = [find_valid_points(sub_a,a_,b,p) for p in phase]
                a_len = list(map(len,a_list))
                max_a = max(a_len)
                indexa = a_len.index(max_a)
                p_outa = phase[indexa]

            
            
                b_list = [find_valid_points(sub_b,a,b_,p) for p in phase]
                b_len = list(map(len,b_list))
                max_b = max(b_len)
                indexb = b_len.index(max_b)
                p_outb = phase[indexb]


                if(max_a > max_b):
                    sub = sub_a
                    p_out = p_outa
                    a = a_
                    max_len = max_a
                    passes = 0
                else:
                    sub = sub_b
                    p_out = p_outb
                    b = b_
                    max_len = max_b
                    passes = 0      

        
    return sub, a, b, p_out


def interpolate_missing(x,y):

        
    sub, a, b, p = find_area(x,y)

    sub = sub.astype("float")

    xc = int(sub.shape[0]/2)
    yc = int(sub.shape[1]/2)

    if(np.count_nonzero(~np.isnan(sub)) > 3):

        xs = np.arange(0, sub.shape[1])
        ys = np.arange(0, sub.shape[0])

        array = np.ma.masked_invalid(sub)
        xx, yy = np.meshgrid(xs, ys)

        x1 = xx[~array.mask]
        y1 = yy[~array.mask]
        newarr = array[~array.mask]

        GD1 = interpolate.griddata((x1, y1), newarr.ravel(),
                          (xx, yy),
                                method='cubic')

        output = GD1[xc,yc]

        if (output == np.nan):
            output = no_data

    else:
            output = no_data

    return output

    
def create_raster():

    interp = np.zeros(arr_shape)

    for i in range(arr_shape[0]):
        for j in range(arr_shape[1]):   
            if(arr[i,j] == no_data):
                #print(f"interpolating! {i}x{j}")
                interp[i,j] = interpolate_missing(i,j)
            else:
                #print(f"this pixel exists! {i}x{j}")
                interp[i,j] = arr[i,j]

    return interp


def open_raster(file_name, band_number):

    try:
        raster = gdal.Open(file_name)
    except RuntimeError as e:
        print("ERROR: Cannot open raster.")
        print(e)
        return None

    try:
        raster_band = raster.GetRasterBand(band_number)
    except RuntimeError as e:
        print("ERROR: Cannot access raster band.")
        print(e)
        return None
    return raster, raster_band



src, band = open_raster('NONNA10_4840N08920W.tiff',1)
    
no_data = band.GetNoDataValue()
arr = src.ReadAsArray()
arr_shape = arr.shape

np.savetxt("input.txt", arr)
np.savetxt("output.txt", create_raster())