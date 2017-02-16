import numpy as np
import scipy.ndimage


def gaussian_kernel(M,sigma):
    for i in range(len(M[0,0])):
        M[:,:,i]=scipy.ndimage.filters.gaussian_filter(M[:,:,i],sigma)
    return M


                                                       
