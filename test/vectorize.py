from osgeo import ogr
from osgeo import gdal
from osgeo import osr
import numpy as np
import os
import sys
import rioxarray as rxr
import geopandas as gpd

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


def main(band_number, input_file):
    src, band = open_raster(input_file,band_number)
    
    nodata = band.GetNoDataValue()
    (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = src.GetGeoTransform()


    driver = ogr.GetDriverByName('ESRI Shapefile')        
    out_data = driver.CreateDataSource("test.shp")
    # getting projection from source raster
    srs = osr.SpatialReference()
    srs.ImportFromWkt(src.GetProjectionRef())
    # create layer with projection
    out_layer = out_data.CreateLayer(input_file.split('.')[0], srs)        
    new_field = ogr.FieldDefn('bathymetry', ogr.OFTReal)
    out_layer.CreateField(new_field)        
    gdal.FPolygonize(band, band, out_layer, 0, [], callback=None)        
    out_data.Destroy()
    src = None


if __name__ == '__main__':
    # make standalone
    if len( sys.argv ) < 3:
        print("""
        ERROR: Provide two arguments:
        1) the band number (int) and 2) input raster directory (str)
        """)

    main(int(sys.argv[1]), str(sys.argv[2]))














# ###Color Codes###
# A1 = [143.0/255.0, 191.0/255.0, 147.0/255.0]
# A2 = [129.0/255.0, 195.0/255.0, 226.0/255.0]
# A3 = [129.0/255.0, 195.0/255.0, 226.0/255.0]
# A4 = [167.0/255.0, 224.0/255.0, 233.0/255.0]
# A5 = [182.0/255.0, 235.0/255.0, 219.0/255.0]
# A6 = [216.0/255.0, 244.0/255.0, 225.0/255.0]
# A7 = [216.0/255.0, 244.0/255.0, 225.0/255.0]
# A8 = [216.0/255.0, 244.0/255.0, 225.0/255.0]
# A9 = [161.0/255.0,74.0/255.0,55.0/255.0]


# bag_color = np.zeros((*bag.shape,3))

# bag_color[np.where(bag<=0)] = np.array(A1) # CHM < 0 - Class 1
# bag_color[np.where((bag>0) & (bag<=2))] = np.array(A2) # 0m < CHM < 2m - Class 2
# bag_color[np.where((bag>2) & (bag<=5))] = np.array(A3) # 2m < CHM < 5m - Class 3
# bag_color[np.where((bag>5) & (bag<=10))] = np.array(A4) # 5m < CHM < 10m - Class 4
# bag_color[np.where((bag>10) & (bag<=20))] = np.array(A5) # 10m < CHM < 20m - Class 5
# bag_color[np.where((bag>20) & (bag<=30))] = np.array(A6) # 20m < CHM < 30m - Class 6
# bag_color[np.where((bag>30) & (bag<=50))] = np.array(A7) # 30m < CHM < 50m - Class 7
# bag_color[np.where((bag>50) & (bag<=100))] = np.array(A8) # 50m < CHM - Class 8
# bag_color[np.where(bag==no_data_val)] = np.array(A9) # no data val - Class 9
