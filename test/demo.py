import numpy as np
from cmath import sqrt
from scipy import interpolate


no_data = 0
arr = np.array([[0,0,0,0,0,0,0,0,0],
                [0,0,2,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0],
                [0,0,0,3,0,0,0,0,0],
                [0,-6,-5,-3,-0,-1,-2,-3,0],
                [0,0,0,0,0,3,0,0,0],
                [0,0,0,4,0,0,32,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]])
arr_shape = arr.shape
interp = np.zeros(arr_shape)
sdarr = np.zeros(arr_shape)

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

    num = 0

    xc = int(sub_arr.shape[0]/2)
    yc = int(sub_arr.shape[1]/2)

    for i in range(sub_arr.shape[0]):
        for j in range(sub_arr.shape[1]):
            if (_in_ellipse(i,xc,j,yc,a,b,alpha) and sub_arr[i,j] != no_data):
                    num = num + 1

    return num


def find_area(x,y):
    
    a = 1
    b = 1

    phase = np.arange(0,360,10)*np.pi/180

    sub = sub_array(x,y,a,b)
    max_len = find_valid_points(sub,a,b,0)
    p_out = 0

    
    while(max_len < 5):

        
        sub_a = sub_array(x,y,a+1,b)
        sub_b = sub_array(x,y,a,b+1)
 
        a_list = [find_valid_points(sub_a,a+1,b,p) for p in phase]
        max_a = max(a_list)
        p_outa = phase[a_list.index(max_a)]

             
        b_list = [find_valid_points(sub_b,a,b+1,p) for p in phase]
        max_b = max(b_list)
        p_outb = phase[b_list.index(max_b)]

            
        if(max_a > max_b):
            sub = sub_a
            p_out = p_outa
            a = a + 1
            max_len = max_a
        else:
            sub = sub_b
            p_out = p_outb
            b = b + 1
            max_len = max_b        

        
    return sub, a, b, p_out


def interpolate_missing(x,y):

        
    sub, a, b, p = find_area(x,y)

    sub = sub.astype("float")

    xc = int(sub.shape[0]/2)
    yc = int(sub.shape[1]/2)

    for i in range(sub.shape[0]):
        for j in range(sub.shape[1]):
            if (not _in_ellipse(i,xc,j,yc,a,b,p)):
                sub[i,j] = no_data
            
            if(sub[i,j] == no_data):
                sub[i,j] = np.nan

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

    return GD1[xc,yc]

    
#def create_raster():
#
 #       for i in range(arr_shape[0]):
  #          for j in range(arr_shape[1]):
   #             
    #            value,dist = find_shoalest(i,j)
#
 #               interp[i,j] = value
  #              sdarr[i,j] = dist


print(interpolate_missing(4,4))
