import numpy as np
import scipy.linalg
from tqdm import tqdm


class Interpolator():

    def __init__(self,band, l_init = 4, num_points = 20, interp_min = 5, iter = 5, eps = 0.7):
        
        self.band = band

        self.l_init = l_init
        self.num_points = num_points
        self.interp_min = interp_min
        self.iter = iter
        self.eps = eps
        
        self.no_data = band.GetNoDataValue()

        self.arr = band.ReadAsArray()
        self.type = self.arr.dtype
        self.arr_shape = self.arr.shape
        
        self.interp = self.create_raster()


    def sub_array(self, x,y,size):

        x_init = max(x - size,0)
        x_end = min(x + size, self.arr_shape[0]-1)
        y_init = max(y - size,0)
        y_end = min(y + size, self.arr_shape[1]-1)

        sub_arr = np.copy(self.arr[x_init:x_end,y_init:y_end])
        
        return sub_arr


    def find_valid_points(self,sub_arr):

        sub_arr[sub_arr == self.no_data] = np.nan
        valid = np.count_nonzero(~np.isnan(sub_arr))

        return valid


    def find_area(self,x,y):

        l = self.l_init

        sub = self.sub_array(x,y,l)
        max_len = self.find_valid_points(sub)
    
        i = 0
        while(max_len < self.num_points and i < self.iter):

            l = l + int(np.exp(self.eps*i))
        
            n_sub = self.sub_array(x,y,l)

            n_len = self.find_valid_points(n_sub)

            max_len = n_len
            sub = n_sub

            i = i + 1
        
        return max_len, sub


    def interpolate_missing(self,x,y):

        
        max_len, sub = self.find_area(x,y)
        sub = sub.astype("float")

        xc = int(sub.shape[0]/2)
        yc = int(sub.shape[1]/2)

        if(max_len > self.interp_min):

            xs = np.arange(0, sub.shape[1])
            ys = np.arange(0, sub.shape[0])

            X, Y = np.meshgrid(xs, ys)

            XX = X.flatten()
            YY = Y.flatten()
            ZZ = sub.flatten()

        
            data = np.column_stack((XX,YY,ZZ))
            filtered = data[~np.isnan(data[:,-1])]

    
            A = np.c_[np.ones(filtered.shape[0]), filtered[:,:2], np.prod(filtered[:,:2], axis=1), filtered[:,:2]**2]
            C,r,_,_ = scipy.linalg.lstsq(A, filtered[:,2])
    
            # evaluate it on a grid
            Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)


            output = Z[xc,yc]

        else:
            output = self.no_data

        return output


    def create_raster(self):

        interp = np.zeros(self.arr.shape).astype(self.arr.dtype)

        for i in tqdm(range(self.arr_shape[0])):
            for j in range(self.arr_shape[1]):   
                if(self.arr[i,j] == self.no_data):
                    interp[i,j] = self.interpolate_missing(i,j)
                else:
                    interp[i,j] = self.arr[i,j]

        return interp
        


        
        
        





    




