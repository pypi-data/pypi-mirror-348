# These functions correspond to a standard single-resolution HEALPix implementation
# They are all needed to generalize the standard for multi-resolution maps
# Currently these are trivial wrappers for healpy. These is the only file in
# mhealpy that imports healpy explicitely. The goal with having all of them in
# a single place is to facilitate swapping healpy by some other implementation
# in the future if needed. 

import healpy as hp

import numpy as np

MAX_ORDER = 29
MAX_NSIDE = 536870912
UNSEEN = hp.UNSEEN

# Order/npix/nside conversion
def order2npix(order):
    """
    Get the number of pixel for a map of a given order

    Args:
        order (int or array)

    Return:
        int or array
    """

    return 12*4**np.array(order, dtype=int)

def nside2order(nside):
    return hp.nside2order(nside)

def order2nside(order):
    return hp.order2nside(order)

def nside2npix(nside):
    return hp.nside2npix(nside)

def npix2nside(npix):
    return hp.npix2nside(npix)

def nside2pixarea(nside):
    return hp.nside2pixarea(nside)

# Ang/pix conversion
def pix2ang(nside, ipix, nest = False, lonlat = False):
    return hp.pix2ang(nside, ipix, nest, lonlat = lonlat)

def pix2vec(nside, ipix, nest = False):
    return hp.pix2vec(nside, ipix, nest)

def ang2pix(nside, theta, phi, nest = False, lonlat = False):
    return hp.ang2pix(nside, theta, phi, nest = nest, lonlat = lonlat)

def vec2pix(nside, x,y,z, nest = False):
    return hp.vec2pix(nside, x,y,z, nest)

# Vec/ang conversion
def vec2ang(vectors):
    return hp.vec2ang(vectors)

def ang2vec(theta, phi, lonlat = False):
    return hp.ang2vec(theta, phi, lonlat = lonlat)

# Conversion ring/nest
def nest2ring(nside, ipix):
    return hp.nest2ring(nside, ipix)

def ring2nest(nside, ipix):
    return hp.ring2nest(nside, ipix)

# Convenience methods
def isnpixok(npix):
    return hp.isnpixok(npix)

# Pixel querying
def get_all_neighbours(nside, theta, phi = None, nest = False, lonlat = False):
    return hp.get_all_neighbours(nside, theta, phi, nest = nest, lonlat = lonlat)

def query_disc(nside, vec, radius, inclusive=False, fact=4, nest=False):
    return hp.query_disc(nside, vec, radius, inclusive, fact, nest)

def query_polygon(nside, vertices, inclusive=False, fact=4, nest=False):
    return hp.query_polygon(nside, vertices, inclusive, fact, nest)

def query_strip(nside, theta1, theta2, inclusive=False, nest=False):
    return hp.query_strip(nside, theta1, theta2, inclusive, nest)

def boundaries(nside, pix, step=1, nest=False):
    return hp.boundaries(nside, pix, step, nest)

# Interpolation
def get_interp_weights(nside, theta, phi=None, nest=False, lonlat = False):
    return hp.get_interp_weights(nside, theta, phi, nest, lonlat = lonlat)


