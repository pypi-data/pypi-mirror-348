import logging
logger = logging.getLogger(__name__)

import mhealpy as hp
from mhealpy.plot.util import healpy_coord_to_astropy
from mhealpy.plot.axes import HealpyAxes
from astropy.coordinates import Galactic, ICRS

import numpy as np
from numpy import array, log2, sqrt

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.projections import get_projection_class

from collections import deque

from astropy.coordinates import (UnitSphericalRepresentation, SkyCoord,
                                 BaseRepresentation, CartesianRepresentation,
                                 BaseCoordinateFrame, frame_transform_graph)
import astropy.units as u
from astropy.units import cds
from astropy.visualization.wcsaxes import WCSAxes 

# I couldn't find a public method to do this
from astropy.coordinates.sky_coordinate_parsers import _get_frame_class

class HealpixBase:
    """
    Basic operations related to HEALPix pixelization, for which the map
    contents information is not needed. This class is conceptually very similar 
    the the Healpix_Base class of Healpix_cxx.

    Single resolution maps are fully defined by specifying their order 
    (or NSIDE) and ordering scheme ("RING" or "NESTED"). 

    Multi-resolution maps follow an explicit "NUNIQ" scheme, with each pixel 
    identfied by a _uniq_ number. No specific is needed nor guaranteed.

    .. warning::
        The initialization input is not validated by default. Consider calling 
        `is_mesh_valid()` after initialization, otherwise results might be
        unexpected.


    Args:
        uniq (array): Explicit numbering of each pixel in an "NUNIQ" scheme.
        Order (int): Order of HEALPix map.
        nside (int): Alternatively, you can specify the NSIDE parameter.
        npix (int): Alternatively, you can specify the total number of pixels.
        scheme (str): Healpix scheme. Either 'RING', 'NESTED' or 'NUNIQ'
        coordsys (BaseFrameRepresentation or str): Instrinsic coordinates of the map.
            Either ‘G’ (Galactic), ‘E’ (Ecliptic) , ‘C’ (Celestial = Equatorial) or any other 
            coordinate frame recognized by astropy.
        base (HealpixBase): Alternatively, you can copy the properties of another
            HealpixBase object
    """

    def __init__(self,
                 uniq = None,
                 order = None,
                 nside = None,
                 npix = None,
                 scheme = 'ring',
                 coordsys = None,
                 base = None):

        # Cache of rangeset representation and order.
        # Make some calculations faster
        self._pix_rangesets = None
        self._pix_rangesets_argsort = None
        
        if base is not None:
            # Copy another HealpixBase
            
            self._uniq = base._uniq
            self._scheme = base._scheme
            self._order = base._order
            self._coordsys = base._coordsys

            self._pix_rangesets = base._pix_rangesets
            self._pix_rangesets_argsort = base._pix_rangesets_argsort
            
        elif uniq is not None:
            # MOC map
            
            self._uniq = array(uniq, dtype = int)
            
            # Scheme and order are implicit
            self._scheme = "NUNIQ"
            
            self._order = hp.nside2order(hp.uniq2nside(max(uniq)))
            
            self.coordsys = coordsys
        
        else:
            # Single resolution map

            self._uniq = None
            
            # User specified nside instead of order
            if order is not None:

                self._order = order

            elif nside is not None:

                self._order = hp.nside2order(nside)

            elif npix is not None:

                self._order = hp.nside2order(hp.npix2nside(npix))

            else:

                raise ValueError("Specify nside, order or npix")
                
            if scheme is None:
                    raise ValueError("Specify scheme")

            self._scheme = scheme.upper()

            if self._scheme not in ['RING','NESTED', 'NUNIQ']:
                raise ValueError("Scheme can only be 'ring', 'nested' or 'NUNIQ'")

            self.coordsys = coordsys
            
        # Cache the ratio between the number of pixels in this maps and
        # that of a map with the highest possible order
        self._npix_ratio_max = hp.MAX_NSIDE * hp.MAX_NSIDE // self.nside // self.nside
            
    def __eq__(self, other):

        return self.conformable(other)

    @property
    def coordsys(self):
        return self._coordsys

    @coordsys.setter
    def coordsys(self, coordsys):

        if coordsys is None:
            self._coordsys = None
        elif isinstance(coordsys, BaseCoordinateFrame):
            self._coordsys = coordsys 
        else:
            self._coordsys = _get_frame_class(healpy_coord_to_astropy(coordsys))()
        
    @classmethod
    def adaptive_moc_mesh(cls, max_nside, split_fun, coordsys = None):
        """
        Return a MOC mesh with an adaptive resolution
        determined by an arbitrary function.

        Args:
            max_nside (int): Maximum HEALPix nside to consider
            split_fun (function): This method should return ``True`` if a pixel 
            should be split into pixel of a higher order, and ``False`` otherwise. 
            It takes two integers, ``start`` (inclusive) and ``stop`` (exclusive), 
            which correspond to a single pixel in nested rangeset format for a 
            map of nside ``max_nside``.
            coordsys (BaseFrameRepresentation or str): Assigns a coordinate system to the map

        Return:
            HealpixBase
        """

        map_uniq = deque()

        max_order = hp.nside2order(max_nside)
        order_list = array(range(max_order+1))
        nside = 2**order_list
        npix_ratio = 4 ** (max_order - order_list)
        uniq_shift = 4 * nside * nside
        npix_ratio = 4 ** (max_order - order_list)

        start_buffer = np.zeros((max_order+1, 4), dtype=int)
        cursor = -np.ones((max_order+1), dtype=int)

        for base_pix in range(12):

            order = 0
            start_buffer[order][0] = base_pix * npix_ratio[order]
            cursor[order] = 0

            while order >= 0:

                if cursor[order] < 0:
                    order -= 1
                    continue

                start = start_buffer[order][cursor[order]]
                stop  = start + npix_ratio[order]

                cursor[order] -= 1

                if order < max_order and split_fun(start, stop):
                    # Split

                    order += 1

                    split_shift = array(range(4))*npix_ratio[order]
                    start_buffer[order] = start + split_shift

                    cursor[order] = 3

                else:
                    # Add to map

                    uniq = (start / npix_ratio[order] + uniq_shift[order]).astype(int) 

                    map_uniq.append(uniq)

        return cls(map_uniq, coordsys = coordsys)

    @classmethod
    def moc_from_pixels(cls, nside, pixels, nest = False, coordsys = None):
        """
        Return a MOC mesh where a list of pixels are kept at a 
        given nside, and every other pixel is appropiately downsampled.
        
        Also see the more generic ``adaptive_moc()`` and ``adaptive_moc_mesh()``.

        Args:
            nside (int): Maximum healpix NSIDE (that is, the NSIDE for the pixel
                list) 
            pixels (array): Pixels that must be kept at the finest pixelation
            nest (bool): Whether the pixels are a 'NESTED' or 'RING' scheme
            coordsys (BaseFrameRepresentation or str): Assigns a coordinate system to the map
        """

        # Always work in nested
        if not nest:
            pixels = array([hp.ring2nest(nside, pix) for pix in pixels])
            
        # Auxiliary function so we can reuse adaptive_moc_mesh()
        pixels.sort()
        
        def pix_list_range_intersect(start, stop):

            start_index,stop_index = np.searchsorted(pixels, [start,stop])

            return start_index < stop_index

        # Get the grid        
        return cls.adaptive_moc_mesh(nside,
                                     pix_list_range_intersect,
                                     coordsys = coordsys)

    def conformable(self, other):
        """
        For single-resolution maps, return ``True`` if both maps have the same
        nside, scheme and coordinate system.

        For MOC maps, return `True` if both maps have the same list of UNIQ 
        pixels (including the ordering)
        """

        # astropy's baseframe crashes with ==None...
        if self.coordsys is None or other.coordsys is None:
            equiv_coordsys = self.coordsys is other.coordsys
        else:
            equiv_coordsys = self.coordsys.is_equivalent_frame(other.coordsys)
            
        if self.is_moc:
            return (np.array_equal(self._uniq, other._uniq) and
                    equiv_coordsys)
        else:
            return (self._order == other._order and 
                    self._scheme == other._scheme and
                    equiv_coordsys)

    @property
    def npix(self):
        """
        Get number of pixels.

        For multi-resolutions maps, this corresponds to the number of utilized 
        UNIQ pixels.

        Return:
            int
        """

        if self.is_moc:   
            return len(self._uniq)
        else:
            return int(12 * 4**self._order)

    @property
    def order(self):
        """
        Get map order

        Return:
            int
        """
        
        return self._order

    @property
    def nside(self):
        """
        Get map NSIDE

        Return:
            int
        """

        return int(2**self.order)
        
    @property
    def scheme(self):
        """
        Return HEALPix scheme
        
        Return:
            str: Either 'NESTED', 'RING' or 'NUNIQ'
        """

        return self._scheme

    @property
    def is_nested(self):
        """
        Return true if scheme is NESTED or NUNIQ
        
        Return
            bool
        """

        return self._scheme == "NESTED" or self._scheme == 'NUNIQ'
        
    @property
    def is_ring(self):
        """
        Return true if scheme is RING
        
        Return
            bool
        """

        return self._scheme == "RING"

    @property
    def is_moc(self):
        """
        Return true if this is a Multi-Dimensional Coverage (MOC) map 
        (multi-resolution)

        Return:
            bool
        """

        return self._uniq is not None

    def pix_rangesets(self, nside = None, argsort = False):
        """
        Get the equivalent range of `child pixels` in nested scheme for a map 
        of equal or higher nside

        Args:
            nside (int or None): Nside of output range sets. If None, the map
                nside will be used. nside = mhealpy.MAX_NSIDE returns the 
                cached result
            argsort (bool): Also return also the indices that would sort the array.

        Return:
            recarray: With columns named 'start' (inclusive) and 
                'stop' (exclusive) 
        """

        if nside is None:
            nside = self.nside

        # Ranges
        if self._pix_rangesets is None:

            # No cache, compute from scratch
            start,stop = self.pix2range(hp.MAX_NSIDE, range(self.npix))

            self._pix_rangesets = np.rec.fromarrays([start,stop], names = ['start', 'stop'])
            
        # Use cache
        if nside == hp.MAX_NSIDE:

            rs = self._pix_rangesets

        else:
            
            npix_ratio =  hp.MAX_NSIDE * hp.MAX_NSIDE // nside // nside

            rs = np.rec.fromarrays([self._pix_rangesets.start // npix_ratio,
                                    self._pix_rangesets.stop // npix_ratio],
                                   names = ['start', 'stop'])

        # Argsort
        if argsort:

            if self._pix_rangesets_argsort is None:

                # No cache, compute from scratch
                self._pix_rangesets_argsort = np.argsort(rs.start)

            # Use cache
            rs_argsort = self._pix_rangesets_argsort
                            
            return rs, rs_argsort

        else:

            return rs

    def pix_order_list(self):
        """
        Get a list of lists containing all pixels sorted by order

        Return:
           (list, list): (``pix_per_order``, ``nest_pix_per_order``)
               Each list has a size equal to the map order. 
               Each element is a list of all pixels whose order
               matches the index of the list position.
               The first output contains the index of the pixels, while the
               second contains their coresponding pixel number in a nested scheme.
        """

        pix_per_order = [[] for _ in range(self.order+1)]
        nest_pix_per_order = [[] for _ in range(self.order+1)]

        for pix in range(self.npix):

            nside, nest_pix = hp.uniq2nest(self.pix2uniq(pix))

            order = hp.nside2order(nside)

            pix_per_order[order].append(pix)
            nest_pix_per_order[order].append(nest_pix)

        return pix_per_order,nest_pix_per_order
    
    def pix2range(self, nside, pix):
        """
        Get the equivalent range of `child pixels` in nested scheme for a map 
        of equal or higher nside
        
        Args:
            nside (int): Nside of output range sets
            pix (int or array): Pixel numbers
            
        Return:
            (int or array, int or array): Start pixel (inclusive) and 
                stop pixel (exclusive) 
        """
        
        if self.is_moc:

            return hp.uniq2range(nside, self._uniq[pix])

        else:

            if self.is_ring:
                pix = hp.ring2nest(self.nside, pix)
                
            return hp.nest2range(self.nside, pix, nside)

    def pixarea(self, pix = None):
        """
        Return area of a pixel

        Args:
            pix (int or array): Pixel number. Only relevant for MOC maps.
                Default: All pixels for MOC, a single value for single
                resolution
        
        Return:
            Quantity
        """

        if pix is None:
            if self.is_moc:
                pix = np.arange(self.npix)
            else:
                pix = 0
        
        if self.is_moc:

            ranges = self.pix_rangesets(hp.MAX_NSIDE)[pix]

            area = 3.6331963520923245e-18 * (ranges.stop - ranges.start)

        else:

            area = 1.047197551196597746 / self.nside / self.nside

            area = np.broadcast_to(area, np.shape(pix))
            
        return area * u.sr
        
    def pix2ang(self, pix, lonlat = False):
        """
        Return the coordinates of the center of a pixel
        
        Args:
            pix (int or array)

        Return:
            (float or array, float or array)
        """

        if self.is_moc:

            nside, pix = hp.uniq2nest(self.pix2uniq(pix))

            return hp.pix2ang(nside, pix, nest = True, lonlat = lonlat)
            
        else:
            return hp.pix2ang(self.nside, pix, nest = self.is_nested, lonlat = lonlat)

    def pix2vec(self, pix):
        """
        Return a vector corresponding to the center of a pixel
        
        Args:
            pix (int or array)

        Return:
            array: Size (3,N)
        """

        if self.is_moc:

            nside, pix = hp.uniq2nest(self.pix2uniq(pix))

            return hp.pix2vec(nside, pix, nest = True)
            
        else:
            return hp.pix2vec(self.nside, pix, nest = self.is_nested)

    def pix2skycoord(self, pix):
        """
        Return the sky coordinate for the center of a given pixel
        
        Args:
            pix (int or array): Pixel number
        
        Return:
            SkyCoord
        """

        if self.coordsys is None:
            raise ValueError("Undefined coordinate system")
        
        lon,lat = self.pix2ang(pix, lonlat = True)

        skycoord = SkyCoord(lon*u.deg, lat*u.deg, frame = self.coordsys)

        return skycoord

    def _standarize_theta_phi_lonlat(self, theta, phi, lonlat):

        if isinstance(theta, (SkyCoord, BaseRepresentation)):
            # Support astropy
            
            if isinstance(theta, SkyCoord):

                if self.coordsys is None:
                    raise ValueError("Undefined coordinate system")
                
                theta = theta.transform_to(self.coordsys)
        
            coord = theta.represent_as(UnitSphericalRepresentation)

            theta,phi = coord.lon.deg, coord.lat.deg

            lonlat = True

        return theta,phi,lonlat
    
    def ang2pix(self, theta, phi = None, lonlat = False):
        """
        Get the pixel (as used in []) that contains a given coordinate

        Args:
            theta (float, array or SkyCoord): Zenith angle
            phi (float or arrray): Azimuth angle
      
        Return:
            int or array
        """

        theta, phi, lonlat = self._standarize_theta_phi_lonlat(theta, phi, lonlat)

        pixels = hp.ang2pix(self.nside, theta, phi,
                            nest=self.is_nested, lonlat = lonlat)
        
        if self.is_moc:
            pixels = self.nest2pix(pixels)
            
        return pixels
    
    def vec2pix(self, x, y, z):
        """
        Get the pixel (as used in []) that contains a given coordinate

        Args:
            x (float or array): x coordinate
            y (float or array): y coordinate
            z (float or array): z coordinate
        
        Return:
            int or array
        """

        pixels = hp.vec2pix(self.nside, x, y, z, nest=self.is_nested)

        if self.is_moc:
            pixels = self.nest2pix(pixels)
            
        return pixels
        
    def pix2uniq(self, pix):
        """
        Get the UNIQ representation of a given pixel index.

        Args:
            pix (int): Pixel number in the current scheme (as used for [])
        """

        if self.is_moc:

            return self._uniq[pix]

        else:

            if self.scheme == 'RING':
                pix = hp.ring2nest(self.nside, pix)

            return hp.nest2uniq(self.nside, pix)

    @property    
    def uniq(self):
        """
        Get an array with the NUNIQ numbers for all pixels
        """

        if self.is_moc:
            return self._uniq
        else:
            return self.pix2uniq(range(self.npix))
        
    def nest2pix(self, pix):
        """
        Get the corresponding pixel in the current grid for a pixel in NESTED
        scheme. For MOC map, return the pixel that contains it. 

        Args:
            pix (int or array): Pixel number in NESTED scheme. Must correspond 
                to a map of the same order as the current.

        Return:
            int or array
        """

        if self.is_moc:

            # Work with rangesets for maximum order,
            # then find pixel number for this order,
            # and then find the rangesets that contain these pixels

            pix = np.array(pix)
            
            rangesets, rs_argsort = self.pix_rangesets(hp.MAX_NSIDE, argsort = True)
            
            ipix = np.searchsorted(rangesets.stop, pix * self._npix_ratio_max,
                                   side = 'right',
                                   sorter = rs_argsort)

            opix = rs_argsort[ipix]

            # Follow healpy convention for null pix
            if np.ndim(opix) == 0:
                if pix == -1:
                    opix = -1
            else:
                opix[pix == -1] = -1
                
            return opix
            
        else:
            
            if self.is_nested:
                return pix
            else:
                return hp.nest2ring(self.nside, pix)
            
    
    def get_interp_weights(self, theta, phi = None, lonlat = False):
        """
        Return the indices of the 4 closest pixels on the two rings above and
        below the given location(s) and the corresponding weights. Weights
        are provided for bilinear interpolation along latitude and longitude.

        For MOC maps, these pixel numbers might repeat.

        The output arrays have shapes (4,) if ``theta`` and ``phi`` are
        scalars, or (4,``N``) if they are arrays of length ``N``.

        Args:
            theta (float or array): Zenith angle (rad)
            phi (float or array): Azimuth angle (rad)
 
        Return:
            pixels (array): pixel indices.
            weights (array): weights of the corresponding pixels.
        """

        theta, phi, lonlat = self._standarize_theta_phi_lonlat(theta, phi, lonlat)

        pixels,weights = hp.get_interp_weights(self.nside, theta, phi,
                                               nest = self.is_nested,
                                               lonlat = lonlat)

        if self.is_moc:
            pixels = self.nest2pix(pixels)

        return (pixels, weights)
            
    def get_all_neighbours(self, theta, phi = None, lonlat = False):
        """
        Return the 8 nearest pixels. For MOC maps, these might repeat, as this
        is equivalent to raterizing the maps to the highest order, getting the 
        neighbohrs, and then finding the pixels tha contain them.

        Args:
            theta (float or int or array): Zenith angle (rad). If phi is 
                ``None``, these are assummed to be pixels numbers. 
            phi (float or array or None): Azimuth angle (rad)

        Return:
            array: pixel number of the SW, W, NW, N, NE, E, SE and S neighbours,
                shape is (8,) if input is scalar, otherwise shape is (8, N) if 
                input is of length N. If a neighbor does not exist (it can be 
                the case for W, N, E and S) the corresponding pixel number will 
                be -1.
        """

        theta, phi, lonlat = self._standarize_theta_phi_lonlat(theta, phi, lonlat)

        if self.is_moc and phi is None:
            theta,phi = self.pix2ang(theta, lonlat = lonlat)
        
        neighbors = hp.get_all_neighbours(self.nside, theta, phi,
                                          nest = self.is_nested,
                                          lonlat = lonlat)

        if self.is_moc:
            neighbors = self.nest2pix(neighbors)

        return neighbors
 
    def is_mesh_valid(self):
        """
        Return ``True`` if the map pixelization is valid. For
        single resolution this simply checks that the size is a valid NSIDE value.
        For MOC maps, it checks that every point in the sphere is covered by
        one and only one pixel.
        
        Return:
            True
        """

        if self.is_moc:

            # Work in rangesets, and check that there is no gap in between them
            rs, rs_argsort = self.pix_rangesets(hp.MAX_NSIDE, argsort = True)

            rs = rs[rs_argsort]

            return (rs.start[0] == 0 and
                    rs.stop[-1] == hp.nside2npix(hp.MAX_NSIDE) and
                    np.array_equal(rs.start[1:], rs.stop[:-1]))
            
        else:
                
            return hp.isnpixok(self.npix)

    def _pix_query_fun(self, fun):
        """
        Return a wrapper for healpy's pix querying routines

        Args:
            fun (function): Healpy's query_* functions
        
        Return:
            function: With apprpiate grid, passes rest of arguments to fun
        """

        def wrapper(*args, **kwargs):

            if self.is_moc:

                # We'll do it order by order

                pix_per_order, nest_pix_per_order = self.pix_order_list()
                
                query_pix = np.zeros(0, dtype = int)

                for order in range(self.order+1):

                    pixels = fun(hp.order2nside(order), nest = True,
                                 *args, **kwargs)

                    query_bool = np.isin(nest_pix_per_order[order], pixels)

                    order_pix = array(pix_per_order[order], dtype=int)

                    query_pix = np.append(query_pix,
                                          order_pix[query_bool])

                return np.sort(query_pix)
                        
            else:

                return fun(self.nside, nest = self.is_nested,
                           *args, **kwargs)

        return wrapper                

    def query_polygon(self, vertices, inclusive=False, fact=4):
        """
        Returns the pixels whose centers lie within the convex polygon defined 
        by the vertices array (if inclusive is False), or which overlap with 
        this polygon (if inclusive is True).

        Args:
            vertices (float): Vertex array containing the vertices of the 
                polygon, shape (N, 3).
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.
            fact (int): Only used when inclusive=True. The overlapping test 
                will be done at the resolution fact*nside. For NESTED ordering, 
                fact must be a power of 2, less than 2**30, else it can be any 
                positive integer. Default: 4.
            
        Return:
            int array: The pixels which lie within the given polygon.
        """
        
        fun = self._pix_query_fun(hp.query_polygon)

        return fun(vertices, inclusive=inclusive, fact=fact)

    def query_disc(self, vec, radius, inclusive=False, fact=4):
        """

        Args:
            vec (float, sequence of 3 elements, SkyCoord): The coordinates of unit vector 
                defining the disk center.
            radius (float): The radius (in radians) of the disk
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.
            fact (int): Only used when inclusive=True. The overlapping test 
                will be done at the resolution fact*nside. For NESTED ordering, 
                fact must be a power of 2, less than 2**30, else it can be any 
                positive integer. Default: 4.
        
        Return:
            int array: The pixels which lie within the given disc.
        """

        if isinstance(vec, (SkyCoord, BaseRepresentation)):

            if isinstance(vec, SkyCoord) and self.coordsys is not None:
                vec = vec.transform_to(self.coordsys)
            
            vec = vec.represent_as(CartesianRepresentation).xyz.value
        
        fun = self._pix_query_fun(hp.query_disc)

        return fun(vec, radius, inclusive=inclusive, fact=fact)

    def query_strip(self,  theta1, theta2, inclusive=False):
        """
        Returns pixels whose centers lie within the colatitude range defined by 
        theta1 and theta2 (if inclusive is False), or which overlap with this 
        region (if inclusive is True). If theta1<theta2, the region between 
        both angles is considered, otherwise the regions 0<theta<theta2 and 
        theta1<theta<pi.

        Args:
            theta (float): First colatitude (radians)
            phi (float): Second colatitude (radians)
            inclusive (bool): f False, return the exact set of pixels whose 
                pixels centers lie within the region; if True, return all 
                pixels that overlap with the region.

        Return:
            int array: The pixels which lie within the given strip.
        """
        
        fun = self._pix_query_fun(hp.query_strip)

        return fun(theta1, theta2, inclusive=inclusive)
    
    def boundaries(self, pix, step = 1):
        """
        Returns an array containing vectors to the boundary of the nominated pixel.

        The returned array has shape (3, 4*step), the elements of which are the 
        x,y,z positions on the unit sphere of the pixel boundary. In order to 
        get vector positions for just the corners, specify step=1.
        """
        
        if self.is_moc:

            def single_pix_bounds(pix):

                nside, nest_pix = hp.uniq2nest(self._uniq[pix])
    
                return hp.boundaries(nside, nest_pix, step = step, nest = True)

            moc_bounds = np.vectorize(single_pix_bounds)
            
            return moc_bounds(pix)

        else:

            return hp.boundaries(self.nside, pix, step, nest = self.is_nested)

    def _default_coordsys(self, coord):
        if coord is None:
            coord = self.coordsys
            
            if coord is None:
                coord = 'C'

        coord = healpy_coord_to_astropy(coord)

        if not isinstance(coord, BaseCoordinateFrame):
            coord = frame_transform_graph.lookup_name(coord)()
        
        return coord
        
    def _default_fig_ax_coordsys(self, ax = 'mollview', ax_kw = None, coord = None):

        # Intrinsic coordinates
        coord = self._default_coordsys(coord)
        
        # Plotting coordinates
        if isinstance(ax, mpl.axes.Axes):

            # Fully user defined
            
            fig = ax.get_figure()

        else:

            # Default
            fig = plt.figure(figsize = [4,4], dpi = 150)        

            if ax_kw is None:
                ax_kw = {}
            
            if (issubclass(get_projection_class(ax), HealpyAxes) and
                'coord' not in ax_kw):

                # Handle ICRS and Galactic special cases
                if isinstance(coord, ICRS):
                    ax_kw['coord'] = 'C'
                elif isinstance(coord, Galactic):
                    ax_kw['coord'] = 'G'
                else:
                    logger.warn(f"Could not determine default ax_kw['coord']. WCSAxes do not support intricsic coordinates {coord}. Fallling back to plotting onto ICRS coodinates")
                    ax_kw['coord'] = 'C'

            ax = fig.add_axes([0,0,1,1],
                              projection  = ax,
                              **ax_kw)

        if not isinstance(ax, WCSAxes):
            raise ValueError("Axes is not a valid WCSAxes")

        return fig,ax,coord


    def plot_grid(self,
                  ax = 'mollview',
                  ax_kw = None,
                  step = 32,
                  coord = None,
                  **kwargs):
        """
        Plot the pixel boundaries of a Healpix grid

        Args:
            ax (WCSAxes or str): Astropy's WCSAxes to plot the map. Either
                an existing instance or the name of a registered projection.
            ax_kw (dict): Extra arguments if a new axes needs to be created.
                If ``ax`` is a HealpyAxes --e.g. mollview, cartview, orthview-- and
                ``ax_kw['coord']`` is not provided, it will attempt to match the
                intricsic coordinates. This is however only possible for 'C' and 'G',
                and will default to 'C' otherwise.
            step (int): How many points per pixel side
            coord (str): Instrinsic coordinates of the map. Either ‘G’ (Galactic), 
                ‘E’ (Ecliptic) , ‘C’ (Celestial = Equatorial) or any other 
                coordinate frame recognized by astropy. The default is 'C' unless
                ``coordsys`` is defined. This option overrides ``coordsys``
            **kwargs: Passed to matplotlib.pyplot.plot()
        
        Return:
            matplotlib.lines.Line2D list, WCSAxes: The first return value
               corresponds to the output ``pyplot.plot()`` for one of the pixels. 
               The second is the astropy WCSAxes object used.        
        """

        # Standarize axes, figure, and frame
        fig,ax,coord = self._default_fig_ax_coordsys(ax, ax_kw, coord)
        
        wcs = ax.wcs
        
        # Every line should have the same color
        if 'c' in kwargs:
            color = kwargs.pop('c')
        else:
            color = kwargs.pop('color', 'black')
        
        # Plot boundaries as lines
        lines = []
        for pix in range(self.npix):

            # Get boundaries
            vec = self.boundaries(pix, step = step)

            # Close loop
            vec = np.append(vec, vec[:,0].reshape(-1,1), axis = 1)

            # Project
            theta,phi = hp.vec2ang(np.transpose(vec))
            x,y = wcs.world_to_pixel(SkyCoord(phi, np.pi/2 - theta,
                                              unit = 'rad', frame = coord))

            # Remove discontinuities
            dx = np.abs(np.diff(x))
            dy = np.abs(np.diff(y))
            dist = sqrt(dx*dx + dy*dy)

            if all(np.isnan(dist)):
                # Supress warning
                continue
            
            jumps = dist > 10*np.nanmedian(dist)
            jumps = np.append(jumps, False)

            if any(jumps):

                ijumps = np.nonzero(jumps)[0]+1

                x = np.insert(x, ijumps, np.nan)
                y = np.insert(y, ijumps, np.nan)

            # Plot
            lines += ax.plot(x, y, color = color, **kwargs)

        return lines, ax
        
    def moc_sort(self):
        """
        Sort the uniq pixels composing a MOC map based on its 
        rangeset representation
        """

        if not self.is_moc:
            return

        rs, rs_argsort = self.pix_rangesets(hp.MAX_NSIDE, argsort = True)

        self._uniq = self._uniq[rs_argsort]

        if self._pix_rangesets is not None:
            self._pix_rangesets = self._pix_rangesets[rs_argsort]

        if self._pix_rangesets_argsort is not None:
            self._pix_rangesets_argsort = np.arange(self.npix)
        
