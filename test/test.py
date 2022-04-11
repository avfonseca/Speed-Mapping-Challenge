from osgeo import gdal
from osgeo import osr
import numpy as np
import pygmt

# import 

ds = gdal.Open('NONNA10_5300N13170W.bag')
driver = gdal.GetDriverByName('BAG')

#Band with data
band = ds.GetRasterBand(1)
bag = -1*band.ReadAsArray()

#Mask of valid soundings
no_data_val = -1000000.0
valid_mask = np.where(bag == no_data_val,0,1) 




###Color Codes###
A1 = [143.0/255.0, 191.0/255.0, 147.0/255.0]
A2 = [129.0/255.0, 195.0/255.0, 226.0/255.0]
A3 = [129.0/255.0, 195.0/255.0, 226.0/255.0]
A4 = [167.0/255.0, 224.0/255.0, 233.0/255.0]
A5 = [182.0/255.0, 235.0/255.0, 219.0/255.0]
A6 = [216.0/255.0, 244.0/255.0, 225.0/255.0]
A7 = [216.0/255.0, 244.0/255.0, 225.0/255.0]
A8 = [216.0/255.0, 244.0/255.0, 225.0/255.0]
A9 = [161.0/255.0,74.0/255.0,55.0/255.0]


bag_color = np.zeros((*bag.shape,3))

print(bag_color.shape)

bag_color[np.where(bag<=0)] = np.array(A1) # CHM < 0 - Class 1
bag_color[np.where((bag>0) & (bag<=2))] = np.array(A2) # 0m < CHM < 2m - Class 2
bag_color[np.where((bag>2) & (bag<=5))] = np.array(A3) # 2m < CHM < 5m - Class 3
bag_color[np.where((bag>5) & (bag<=10))] = np.array(A4) # 5m < CHM < 10m - Class 4
bag_color[np.where((bag>10) & (bag<=20))] = np.array(A5) # 10m < CHM < 20m - Class 5
bag_color[np.where((bag>20) & (bag<=30))] = np.array(A6) # 20m < CHM < 30m - Class 6
bag_color[np.where((bag>30) & (bag<=50))] = np.array(A7) # 30m < CHM < 50m - Class 7
bag_color[np.where((bag>50) & (bag<=100))] = np.array(A8) # 50m < CHM - Class 8
bag_color[np.where(bag==no_data_val)] = np.array(A9) # no data val - Class 9




# getting projection from source raster
srs = osr.SpatialReference()
srs.ImportFromWkt(ds.GetProjectionRef())
# create layer with projection
out_layer = out_data.CreateLayer(raster_path.split('.')[0], srs)        
new_field = ogr.FieldDefn('field_name', ogr.OFTReal)
out_layer.CreateField(new_field)        
gdal.FPolygonize(bag_color, bag_color, out_layer, 0, [], callback=None)        
source_raster = None





#fig = pygmt.Figure()
#fig.grdcontour(grid=bag)
#fig.savefig("test.png")





#plt.figure(); 
#plt.imsave("test.png",bag_color)
#plt.title('SERC CHM Classification')
#ax=plt.gca(); ax.ticklabel_format(useOffset=False, style='plain') 


#bag[valid_mask==0] = 0 

#Normalize Image for saving
#range = (np.max(bag) - np.min(bag))
#bag = (bag - np.min(bag))/range

#bag = np.expand_dims(bag, axis=2)
#valid_mask = np.expand_dims(valid_mask, axis=2)
#rgb_bag = np.repeat(bag, 3, axis=2)

#output = Image.new(mode="RGBA", size=(bag.shape[0],bag.shape[1]))
#output = np.concatenate((rgb_bag,valid_mask),axis=2)
#output = np.uint8(output*255)

#img = Image.fromarray(output, 'RGBA')            
#img.save('my2.png')
