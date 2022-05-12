import numpy as np
import pandas as pd
import skimage
import scipy as scp
import matplotlib.pyplot as plt
from skimage import feature
from skimage.segmentation import clear_border
from PIL import Image
import os
from osgeo import ogr
from osgeo import gdal
from osgeo import osr


def shoal_select(filename):
    #generate image
    #image = np.zeros((128,128),dtype = float)
    #image[32:-32,32:-32] = 1
    image = np.loadtxt(filename)
    no_data = image[0,0]
    image[image == no_data] = np.nan
    #initial_image = np.array(Image.open('nlcd_changed.tif'))

    #image = scp.ndimage.rotate(image,15,mode = 'constant')
    #image = scp.ndimage.gaussian_filter(image,4)
    #image = skimage.util.random_noise(image,mode = 'speckle',mean = .1)

    #edge detection
    edges = feature.canny(image,3)

    #show them
    #fig, ax = plt.subplots(nrows = 1, ncols = 2)
    #ax[0].imshow(image,cmap = 'gray')
    #ax[0].set_title('Noisey Image')
    #ax[1].imshow(edges,cmap = 'gray')
    #ax[1].set_title('Edge Detection')
    #plt.show()

    #image label on edge Detection
    label_img = skimage.measure.label(edges,8)
    #clear border
    label_brd = clear_border(label_img)
    #plt.imshow(label_brd)
    #plt.show()

    #get region props
    stats = skimage.measure.regionprops(label_brd,intensity_image = image)

    row_start = []
    row_end = []
    col_start = []
    col_end = []
    row_centers = []
    col_centers = []
    min_vals = []
    #make a new image
    image_new = np.zeros(np.shape(image))
    for ii in range(len(stats)):
        #extract centroid
        centroid = stats[ii].centroid
        #bounding box of form (min_row, min_col, max_row, max_col)
        bbox = stats[ii].bbox
        #range of nrows
        row_range = [bbox[0],bbox[2]]
        row_start.append(bbox[0])
        row_end.append(bbox[2])
        #range of columns
        col_range = [bbox[1],bbox[3]]
        col_start.append(bbox[1])
        col_end.append(bbox[3])
        #center row
        row_cent = int(np.floor(row_range[0] + (row_range[1]-row_range[0])/2))
        row_centers.append((row_cent))
        #center col
        col_cent = int(np.floor(col_range[0] + (col_range[1]-col_range[0])/2))
        col_centers.append((col_cent))
        #compute min values
        min_depth = np.nanmin(image[bbox[0]:bbox[2],bbox[1]:bbox[3]])
        min_vals.append(min_depth)
        #place into new image
        image_new[row_cent,col_cent] = min_depth


    #show the new image
    #plt.imshow(image_new,cmap = 'gray', vmin = -30)
    #plt.show()

    #break the image into x parts
    breaks = 10
    y_bound = np.floor(len(image_new[1,:])/breaks)
    x_bound = np.floor(len(image_new)/breaks)
    #new soundings
    image_final = np.zeros((breaks,breaks))
    image_row_cent = np.zeros((breaks,breaks))
    image_col_cent = np.zeros((breaks,breaks))
    #change 0 to nanmin
    row_centers[row_centers == 0 ] = np.nan
    col_centers[col_centers == 0 ] = np.nan
    for kk in range(breaks):
        for jj in range(breaks):
            temp_val = []
            temp_row_cent = []
            temp_col_cent = []
            for ii in range(len(stats)):
                if row_centers[ii] >= kk*y_bound - y_bound and row_centers[ii] <= kk*y_bound:
                    if col_centers[ii] >= jj*x_bound -x_bound and col_centers[ii] <= jj*x_bound:
                        temp_val.append(min_vals[ii])
                        temp_row_cent.append(row_centers[ii])
                        temp_col_cent.append(col_centers[ii])
                        image_final[kk,jj] = np.min(temp_val)
                        min_idx = np.where(temp_val == np.min(temp_val))[0][0]
                        image_row_cent[kk,jj] = temp_row_cent[min_idx]
                        image_col_cent[kk,jj] = temp_col_cent[min_idx]

    #convert selected soundings to geotiff savable array
    selected_soundings = np.zeros(np.shape(image))
    for ii in range(len(image_row_cent)):
        for jj in range(len(image_row_cent)):
            selected_soundings[int(image_row_cent[ii,jj]),int(image_col_cent[ii,jj])] = image_final[ii,jj]

    #save selected_soundings and unique soundings to make svg files
    svg_values = np.unique(selected_soundings)
    #print(selected_soundings)
    np.savetxt('selected_soundings2.txt',selected_soundings)

    ss = np.unique(selected_soundings[selected_soundings!=0])

    # assign directory
    directory = '..\SVGs'

    # iterate over files in
    ext = '.svg'
    file_names = []
    file_names_png = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if filename.endswith(ext):
            write_file = filename.replace('.svg','.png')
            file_names.append(filename)
            #temp_file = cairosvg.svg2png(url = filename,write_to = write_file)
            file_names_png.append(write_file)
        else:
            continue

    #sort the lists
    sort_names = sorted(sorted(set(file_names)),key = len)
    sort_names_png = sorted(sorted(set(file_names_png)),key = len)


    r_idx = []
    c_idx = []
    for ii in range(len(ss)):
        r_idx.append(np.where(selected_soundings==ss[ii])[0])
        c_idx.append(np.where(selected_soundings==ss[ii])[1])
        if len(r_idx[ii]) >1:
            r_idx[ii] = (r_idx[ii][0])
            c_idx[ii] = (c_idx[ii][0])
        else:
            r_idx[ii] = int(r_idx[ii])
            c_idx[ii] = int(c_idx[ii])

    df = pd.DataFrame()
    df['r_idx'] = r_idx
    df['c_idx'] = c_idx
    df['ss_depth'] = ss
    df['filename'] = pd.Series(sort_names)
    df['filename_png'] = pd.Series(sort_names_png)
    df.to_csv('row_col2.csv')

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

def write_geotiff(filename, arr, in_ds, no_data):
    if arr.dtype == np.float32:
        arr_type = gdal.GDT_Float32
    else:
        arr_type = gdal.GDT_Int32

    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(filename, arr.shape[1], arr.shape[0], 1, arr_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    band = out_ds.GetRasterBand(1)
    band.WriteArray(arr)
    band.SetNoDataValue(no_data)
    band.FlushCache()