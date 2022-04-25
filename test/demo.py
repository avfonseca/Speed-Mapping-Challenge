import numpy as np
from cmath import sqrt
import gdal



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


no_data = 0
arr = np.array([[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,-6,-5,-3,-23,-1,-2,-3,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]])
arr_shape = arr.shape
interp = np.zeros(arr_shape)
sdarr = np.zeros(arr_shape)

def _in_ellipse(px, x, py, y, a, b):
        z = ((px-x)**2)/a**2 + ((py-y)**2)/b**2
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

    if(_edge_case(x,y,a,b)):
        temp = null_padding(arr,a,b)
        sub_arr = temp[x:x+2*a+1,y:y+2*b+1]
    else:
        sub_arr = arr[x-a:x+a+1,y-b:y+b+1]
        
    return sub_arr

   
def find_valid_points(sub_arr,a,b):

    values = []
    indices = []

    xc = int(sub_arr.shape[0]/2)
    yc = int(sub_arr.shape[1]/2)

    for i in range(sub_arr.shape[0]):
        for j in range(sub_arr.shape[1]):
            if (_in_ellipse(i,xc,j,yc,a,b) and sub_arr[i,j] != no_data):
                values.append(sub_arr[i,j])
                indices.append((i,j))

    return values,indices,xc,yc


def find_points(x,y):
    a = 1
    b = 1

    points, indices, xc, yc = find_valid_points(sub_array(x,y,a,b),a,b)
    
    while(len(points) < 5):

        pointsa,indicesa,xca,yca = find_valid_points(sub_array(x,y,a+1,b),a+1,b)
        pointsb,indicesb,xcb,ycb = find_valid_points(sub_array(x,y,a,b+1),a,b+1)

        if(len(pointsa) > len(pointsb)):
            points = pointsa
            indices = indicesa
            xc,yc = xca,yca
            a = a+1
        else:
            points = pointsb
            indices = indicesb
            xc,yc = xcb,ycb
            b = b+1

    return points, indices, xc, yc


def find_shoalest(x,y):
        
    points, indices, xc, yc = find_points(x,y)
    max_value = max(points)
    max_index = points.index(max_value)

    print(xc,yc,indices[max_index])

    dist = abs(sqrt(xc - indices[max_index][0])**2 + (yc - indices[max_index][1])**2)
    std = np.std(np.array(points))

    norm_dist = dist/std

    return max_value, dist, norm_dist

    
def create_raster():

        for i in range(arr_shape[0]):
            for j in range(arr_shape[1]):
                
                value,dist = find_shoalest(i,j)

                interp[i,j] = value
                sdarr[i,j] = dist

        
print(find_shoalest(4,4))
