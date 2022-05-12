import numpy as np
import scipy.ndimage
from Interpolator import Interpolator
import sys
from utils import shoal_select, open_raster, write_geotiff


def main(input_file, band_number):

    ds, band = open_raster(input_file, band_number)

    #interpolator = Interpolator(band)

    #arr = interpolator.interp

    #img = scipy.ndimage.gaussian_filter(arr, sigma=(2, 2), order=0)

    #write_geotiff(input_file.split('.')[0] + "_filt.tiff", img, ds, interpolator.no_data)

    #np.savetxt('interpolate_output.txt', arr)

    shoal_select('interpolate_output.txt')



if __name__ == '__main__':
    # make standalone
    if len(sys.argv ) < 3:
        print("""
        ERROR: Provide two arguments:
        1) the band number (int) and 2) input raster directory (str)
        """)

    main(str(sys.argv[1]), int(sys.argv[2]))



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