# Pixelization related function for multi-order coverage maps
# See http://ivoa.net/documents/MOC

import numpy as np
from numpy import array, log2, sqrt, exp

import mhealpy as hp

def uniq2nside(uniq):
    """
    Extract the corresponding nside from a UNIQ numbered pixel

    Args:
        uniq (int or array): Pixel number

    Return:
        int or array
    """

    order = (log2(array(uniq)/4)/2).astype(int) 
    
    return hp.order2nside(order)

def uniq2nest(uniq):
    """
    Convert from UNIQ ordering scheme to NESTED

    Args:
        uniq (int or array): Pixel number

    Return
        (int or array, int or array): nside, npix
    """

    uniq = array(uniq)

    nside = uniq2nside(uniq)
    npix = uniq - 4 * nside * nside

    return nside, npix

def nest2uniq(nside, ipix):
    """
    Convert from from NESTED to UNIQ scheme

    Args:
        nside (int): HEALPix NSIDE parameter
        ipix (int or array): Pixel number in NESTED scheme

    Return:
        int or array
    """

    ipix = array(ipix)

    return 4 * nside * nside + ipix

def nest2range(nside_input, pix, nside_output):
    """
    Get the equivalent range of pixel that correspond to all
    `child pixels` of a map of a greater order.

    Args:
        nside_input (int or array): Nside of input pixel
        pix (int or array): Input pixel.
        nside_output (int): Nside of map with `child pixels`

    Return:
        (int or array, int or array): Start pixel (inclusive) and 
            stop pixel (exclusive) 
    """

    if np.any(nside_input > nside_output):
        raise ValueError("Input order must be greater or equal to output order")

    npix_ratio = nside_output * nside_output // nside_input // nside_input

    pix = array(pix)

    return (pix*npix_ratio, (pix+1)*npix_ratio)


def uniq2range(nside, uniq):
    """
    Convert from a pixel number in NUNIQ scheme to the range of children 
    pixels that it would correspond to in a NESTED map of a given order

    Args:
       order (int): Nside of equivalent single resolution map
       uniq (int or array): Pixel number in NUNIQ scheme

    Return:
        (int or array, int or array): Start pixel (inclusive) and 
            stop pixel (exclusive) 
    """

    pix_nside, pix = uniq2nest(uniq)

    return nest2range(pix_nside, pix, nside)

def range2uniq(nside, pix_range):
    """
    Convert from range of children pixels in a NESTED map of a given order
    to the corresponding uniq pixel number.

    Args:
        nside (int): Nside of equivalent single resolution map
        pix_range (int or array, int or array): Star pixel (inclusive) and 
            stop pixel (exclusive)

    Return:
        int
    """

    npix_ratio = array(pix_range[1]) - array(pix_range[0])

    nside_uniq = nside / sqrt(npix_ratio)

    pix = array(pix_range[0]) / npix_ratio

    if (nside_uniq < 1 or
        any([not float(i).is_integer() for i in array([nside_uniq]).flatten()]) or
        any([not float(i).is_integer() for i in array([pix]).flatten()])):
        raise ValueError("pix_range is malformed for a HEALPix "
                         "map of nside {}".format(nside))

    return nest2uniq(array(nside_uniq).astype(int),
                                 array(pix).astype(int))

