from cmath import sqrt
import numpy as np


class Interpolator():

    def __init__(self,band, a = 1,b = 1, num_points = 3):
        self.band = band
        self.a_init = a
        self.b_init = b
        self.num_points = num_points
        self.no_data = band.GetNoDataValue()

        self.arr = band.ReadAsArray()
        self.arr_shape = self.arr.shape
        
        self.interp, self.sdarr = self.create_raster()


    def _in_ellipse(self, px, x, py, y, a, b):
        z = ((px-x)**2)/a**2 + ((py-y)**2)/b**2
        if z < 1: 
            return True
        else:
            return False

    def _edge_case(self, x,y,a,b):
        if((x > a-1 and y > b-1) and (self.arr_shape[0] - x > a and self.arr_shape[1] - y > b)):
            return False
        else:
            return True

    def null_padding(self,a,b):
        out = self.arr
        return np.pad(out, (a, b), 'constant', constant_values=(self.no_data, self.no_data))

    
    def sub_array(self,x,y,a,b):

        if(self._edge_case(x,y,a,b)):
            temp = self.null_padding(a,b)
            sub_arr = temp[x:x+2*a+1,y:y+2*b+1]
        else:
            sub_arr = self.arr[x-a:x+a+1,y-b:y+b+1]
        
        return sub_arr


    def find_valid_points(self,sub_arr,a,b):

        values = []
        indices = []

        xc = int(sub_arr.shape[0]/2)
        yc = int(sub_arr.shape[1]/2)

        for i in range(sub_arr.shape[0]):
            for j in range(sub_arr.shape[1]):
                if (self._in_ellipse(i,xc,j,yc,a,b) and sub_arr[i,j] != self.no_data):
                    values.append(sub_arr[i,j])
                    indices.append((i,j))

        return values,indices,xc,yc


    def find_points(self,x,y):
        a = self.a_init
        b = self.b_init

        points, indices, xc, yc = self.find_valid_points(self.sub_array(x,y,a,b),a,b)
    
        while(len(points) < self.num_points):

            pointsa,indicesa,xca,yca = self.find_valid_points(self.sub_array(x,y,a+1,b),a+1,b)
            pointsb,indicesb,xcb,ycb = self.find_valid_points(self.sub_array(x,y,a,b+1),a,b+1)

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


    def find_shoalest(self,x,y):
        
        points, indices, xc, yc = self.find_points(x,y)
        max_value = max(points)
        max_index = points.index(max_value)

        dist = abs(sqrt(xc - indices[max_index][0])**2 + (yc - indices[max_index][1])**2)
        std = np.std(np.array(points))

        dist = dist/std

        return max_value, dist


    def create_raster(self):

        interp = np.zeros(self.arr_shape)
        sdarr = np.zeros(self.arr_shape)

        for i in range(self.arr_shape[0]):
            for j in range(self.arr_shape[1]):
                
                value,dist = self.find_shoalest(i,j)

                interp[i,j] = value
                sdarr[i,j] = dist

        return interp, sdarr
        


        
        
        





    




