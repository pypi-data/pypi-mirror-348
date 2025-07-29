# Object-oriented healpy wrapper with support for multi-resolutions maps
import logging
logger = logging.getLogger(__name__)

import mhealpy as hp

import matplotlib.pyplot as plt

import operator

from copy import copy,deepcopy

from astropy.io import fits
from astropy.table import Table
from astropy.wcs import WCS
from astropy.visualization.wcsaxes import WCSAxes 
from astropy.visualization.wcsaxes.frame import EllipticalFrame
from astropy import units as u
from astropy.units import Quantity, UnitBase

import numpy as np
from numpy import array, log2, sqrt

import collections

from .healpix_base import HealpixBase
import mhealpy.plot.axes
from mhealpy.plot.util import healpy_coord_to_astropy, astropy_frame_to_healpy

class HealpixMap(HealpixBase):
    """
    Object-oriented healpy wrapper with support for multi-resolutions maps 
    (known as multi-order coverage map, or MOC).

    You can instantiate a map by providing either:
    
    * Size (through ``order`` or ``nside``), and a ``scheme`` ('RING' or 'NESTED').
      This will initialize an empty map.
    * A list of UNIQ pixels. This will initialize a MOC map. Providing the 
      values for each pixel is optional, zero-initialized by default.
    * An array (in ``data``) and an a scheme ('RING' or 'NESTED'). This will
      initialize the contents of the single-resolution map.
    * A HealpixBase object. The data will be zero-initialized.

    .. warning::
        The initialization input is not validated by default. Consider calling 
        `is_mesh_valid()` after initialization, otherwise results might be
        unexpected.


    Regardless of the underlaying grid, you can operate on maps using 
    ``*``, ``/``, ``+``, ``-``, ``**``, ``==`` and ``abs``. For binary 
    operations the result always corresponds to the finest grid, so there
    is no loss of information. If any of the operands is a MOC, the result is a
    MOC with an appropiate updated grid.. If both operands have the same NSIDE, 
    the scheme of the result corresponds to the left operand. If you want to 
    preserve the grid for a specific operand, use ``*=``, `/=`, etc. 

    The result of most binary operations have the same density parameter as the
    left-most operand, except the following cases: 1) the product of a 
    density-like maps with a histogram-like results in histogram-like map.
    2) the ratio between two histogram-like maps is a density-like map. 
    Operations with scalars leave the map type unchanged.

    .. warning::
        Information might degrade if you use in-place operators (e.g. ``*=``, `/=`)

    The maps are array-like, that is, the can be casted into a regular numpy 
    array (as used by healpy), are iterable (over the pixel values) and can be
    used with built-in function such as ``sum`` and ``max``.

    You can also access the value of pixels using regular numpy indexing 
    with ``[]``. For MOC maps, no specific pixel ordering is guaranted. For a 
    given pixel number ``ipix`` in the current grid, you can get the 
    corresponding UNIQ pixel number using ``m.pix2uniq(ipix)``.

    Args:
        data (array): Values to initialize map. Zero-initialized it not provided.
            The map NSIDE is deduced from the array size, unless ``uniq`` 
            is specified in which case this is considered a multi-resolution map.
        uniq (array or HealpixBase): List of NUNIQ pixel number to initialize a MOC map. 
        order (int): Order of HEALPix map.
        nside (int): Alternatively, you can specify the NSIDE parameter.
        scheme (str): Healpix scheme. Either 'RING', 'NESTED' or 'NUNIQ'
        base (HealpixBase): Specify the grid using a HealpixBase object
        density (bool): Whether the value of each pixel should be treated as
            counts in a histogram (``False``) or as the value of a [density]
            function evaluated at the center of the pixel (``True``). This affect 
            operations involving the splitting of a pixel. 
        dtype (array): Numpy data type. Will be ignored if data is provided.
        coordsys (BaseFrameRepresentation or str): Intrinsic coordinates of the map.
            Either ‘G’ (Galactic), ‘E’ (Ecliptic) , ‘C’ (Celestial = Equatorial) or any other 
            coordinate frame recognized by astropy.
    """

    def __init__(self,
                 data = None,
                 uniq = None,
                 order = None,
                 nside = None,
                 scheme = 'ring',
                 base = None,
                 density = False,
                 dtype = None,
                 coordsys = None,
                 unit = None):
        """
        Initialize an empty (use either nside or order) or initialized 
        """

        if data is not None:
            # Initializes map contents

            # Initialize base
            if uniq is not None or base is not None:
                #MOC
                
                super().__init__(uniq = uniq, base = base, coordsys = coordsys)

                if len(data) != self.npix:
                    raise ValueError("Data size mismatch.")
                
            else:
                # Single resolution. From array size itself
                
                nside = hp.npix2nside(len(data))

                super().__init__(nside = nside,
                                 scheme = scheme,
                                 coordsys = coordsys)

            # Set data
            if isinstance(data, u.Quantity):

                if unit is not None:
                    data = data.to(unit)
                else:
                    unit = data.unit

            self._data = array(data)

        else:
            # Empty map
            
            super().__init__(uniq = uniq,
                             order = order,
                             nside = nside,
                             scheme = scheme,
                             base = base,
                             coordsys = coordsys)
        
            self._data = np.zeros(self.npix, dtype=dtype)

        # Other properties
        self._density = density

        if unit is not None and unit != "unknown":
            self._unit = u.Unit(unit)
        else:
            self._unit = None

    @property
    def unit(self):
        return self._unit

    def to(self, unit, equivalencies=[], update = True, copy = True):
        """
        Return a map with converted units

        Args:
            unit (unit-like): Unit to convert to.
            equivalencies (list or tuple): A list of equivalence pairs to try if the units are not
                directly convertible.
            update (bool): If ``update`` is ``False``, only the units will be changed without
                updating the contents accordingly
            copy (bool): If True (default), then the value is copied. Otherwise, a copy
                will only be made if necessary.
        """

        # Copy
        if copy:
            new = deepcopy(self)
        else:
            new = self
        
        # If no conversion is needed
        if not update:
            if unit is None:
                new._unit = None
            else:
                new._unit = u.Unit(unit)

            return new
                
        # Compute factor
        if new.unit is None:
            
            if unit is None or unit == u.dimensionless_unscaled:
                factor = 1
            else:
                TypeError("Map without units")

        else:
            
            factor = new.unit.to(unit, equivalencies = equivalencies)

        # Update values
        new *= factor

        # Update units
        new._unit = unit

        return new
        
    @classmethod
    def read_map(cls, filename, field = None, uniq_field = 0, hdu = 1,
                 density = None, ignore_units = False):
        """
        Read a HEALPix map from a FITS file.

        Args:
            filename (Path): Path to file
            field (int): Column where the map contents are. Default: 0 for 
                single-resolution maps, 1 for MOC maps.
            uniq_field (int): Column where the UNIQ pixel numbers are. 
                For MOC maps only. 
            hdu (int): The header number to look at. Starts at 0.
            density (bool): Whether this is a histogram-like or a density-like map.
                Overrides the guess from the map's units. Defaults to False.
            ignore_units (bool): Don't load units from map.

        Return:
            HealpixMap
        """

        with fits.open(filename) as hdul:

            hdu = hdul[hdu]

            scheme = hdu.header["ORDERING"]

            coordsys = None
            if "COORDSYS" in hdu.header:
                coordsys = hdu.header["COORDSYS"]   

            if scheme == 'NUNIQ':
                # Is MOC

                if field is None:
                    field = 1

                uniq = hdu.data.field(uniq_field).ravel()
                contents = hdu.data.field(field).ravel()
                
            else:
                # Sigle resolution

                if field is None:
                    field = 0

                uniq = None
                contents = hdu.data.field(field).ravel()
                

            # Get units and guess density parameter, whether it is
            # per sr or per pixel
            if ignore_units:
                unit = None
            else:
                unit = hdu.columns[field].unit

                if unit is not None:
                    unit = u.Unit(unit)

            if density is None:

                if unit is not None and ((u.sr, -1) in zip(unit.bases, unit.powers) or
                                         (u.rad, -2) in zip(unit.bases, unit.powers) or
                                         (u.deg, -2) in zip(unit.bases, unit.powers)):
                    density = True
                else:
                    density = False
                
            m = cls(data = contents,
                    uniq = uniq,
                    density = density,
                    scheme = scheme,
                    coordsys = coordsys,
                    unit = unit)
                
        return m

    def get_fits_hdu(self,
                     extra_maps = None,
                     column_names = None,
                     ):
        """
        Build HDU needed to store map in  a FITS file

        Args:
            extra_maps (HealpixMap or array): Save more maps in the same file
                as extra columns. Must be conformable.
            column_names (str or array): Name of colums. Must have the same 
                length as the number for maps. Defaults to 'CONTENTSn', where 
                ``n`` is the map number (ommited for a single map). For MOC maps,
                the pixel information is always stored in the first column, called
                'UNIQ'.

        Return:
            astropy.io.fits.BinTableHDU
        """
        # Standarize data for astropy's Table
        if self.is_moc:

            # IVOA specifies pixels must be in ascending UNIQ order
            usort = np.argsort(self._uniq)
            data = [self._uniq[usort], self._data[usort]]

        else:

            data = [self._data]

        units = [self.unit]
            
        # Add extra maps
        if extra_maps is not None:
            
            if isinstance(extra_maps, HealpixMap):
                extra_maps = (extra_maps,)

            for map in extra_maps:

                if not self.conformable(map):
                    raise ValueError("All extra maps must be conformable")

                if map.is_moc:
                    data.append(map._data[usort])
                else:
                    data.append(map._data)

                units.append(map.unit)
                    
        # Column names
        nmaps = len(data) - self.is_moc
        
        if column_names is not None:

            if isinstance(column_names, str):
                column_names = [column_names]
            
            if len(column_names) != nmaps:
                raise ValueError("Colum names must match the number of maps.")
            
        else:

            if nmaps > 1:

                column_names = ["CONTENTS{}".format(i) for i in range(nmaps)]
                
            else:

                column_names = ["CONTENTS"]

        if self.is_moc:

            column_names.insert(0, 'UNIQ')

            units.insert(0, None)
            
        # Header
        header = [('PIXTYPE', 'HEALPIX',
                       'HEALPIX pixelisation'),
                  ('ORDERING', self.scheme,
                       'Pixel ordering scheme: RING, NESTED, or NUNIQ'),
                  ('NSIDE', self.nside,
                       'Resolution parameter of HEALPIX'),
                  ('INDXSCHM', 'EXPLICIT' if self.is_moc else 'IMPLICIT',
                       'Indexing: IMPLICIT or EXPLICIT')]

        coordsys = astropy_frame_to_healpy(self.coordsys)

        if self.coordsys is not None:
            header.extend([('COORDSYS', coordsys,
                            'Celestial (C), Galactic (G) or Ecliptic (E)')])

        if self.is_moc:
            header.extend([('MOCORDER', self.order, 'Best resolution order')])
        
        # Prepare table and write
        table = Table(data, names = column_names, units = units)

        hdu = fits.table_to_hdu(table)

        hdu.header.extend(header)

        return hdu
        
    def write_map(self,
                  filename,
                  extra_maps = None,
                  column_names = None,
                  extra_header = None,
                  overwrite = False):
        """
        Write map to disc.

        Args:
            filename (Path): Path to output file
            extra_maps (HealpixMap or array): Save more maps in the same file
                as extra columns. Must be conformable.
            column_names (str or array): Name of colums. Must have the same 
                length as the number for maps. Defaults to 'CONTENTSn', where 
                ``n`` is the map number (ommited for a single map). For MOC maps,
                the pixel information is always stored in the first column, called
                'UNIQ'.
            extra_header (iterable): Iterable of (keyword, value, [comment]) tuples
            overwrite (bool): If True, overwrite the output file if it exists. 
                Raises an OSError if False and the output file exists. 
        """

        hdu = self.get_fits_hdu(extra_maps = extra_maps,
                                column_names = column_names)

        if extra_header is not None:
            hdu.header.extend(extra_header)
        
        hdulist = fits.HDUList([fits.PrimaryHDU(), hdu])

        hdulist.writeto(filename, overwrite = overwrite)
        
    @classmethod
    def adaptive_moc_mesh(cls, max_nside, split_fun, density = False,
                          dtype = None, coordsys = None, unit = None):
        """
        Return a zero-initialized MOC map, with an adaptive resolution
        determined by an arbitrary function.

        Args:
            max_nside (int): Maximum HEALPix nside to consider
            split_fun (function): This method should return ``True`` if a pixel 
            should be split into pixel of a higher order, and ``False`` otherwise. 
            It takes two integers, ``start`` (inclusive) and ``stop`` (exclusive), 
            which correspond to a single pixel in nested rangeset format for a 
            map of nside ``max_nside``.
            density (bool): Will be pass to HealpixMap initialization.
            dtype (dtype): Data type
            coordsys (BaseFrameRepresentation or str): Assigns a coordinate system to the map

        Return:
            HealpixMap
        """
        
        base = HealpixBase.adaptive_moc_mesh(max_nside, split_fun)

        return cls(data = np.zeros(base.npix, dtype = dtype),
                   uniq = base._uniq,
                   density = density,
                   coordsys = coordsys,
                   unit = unit)
        
    @classmethod
    def moc_from_pixels(cls, nside, pixels, nest = False, density = False,
                        dtype = None, coordsys = None, unit = None):
        """
        Return a zero-initialize MOC map where a list of pixels are kept at a 
        given nside, and every other pixel is appropiately downsampled.
        
        Also see the more generic ``adaptive_moc_mesh()``.

        Args:
            nside (int): Maximum healpix NSIDE (that is, the NSIDE for the pixel order
                list) 
            pixels (array): Pixels that must be kept at the finest pixelation
            nest (bool): Whether the pixels are a 'NESTED' or 'RING' scheme
            density (bool): Wheather the map is density-like or histogram-like
            dtype: Daty type
            coordsys (BaseFrameRepresentation or str): Assigns a coordinate system to the map
        """

        base = HealpixBase.moc_from_pixels(nside, pixels, nest = nest)

        return cls(data = np.zeros(base.npix, dtype = dtype),
                   uniq = base._uniq,
                   density = density,
                   coordsys = coordsys,
                   unit = unit)

    @classmethod
    def moc_histogram(cls, nside, samples, max_value, nest = False, weights = None,
                      coordsys = None, unit = None):
        """
        Generate an adaptive MOC map by histogramming samples. 

        If the number of samples is greater than the number of pixels in a map
        of the input ``nside``, consider generating a single-resolution
        map and then use `to_moc()`.

        Also see the more generic ``adaptive_moc_mesh()``.

        Args: 
            nside (int): Healpix NSIDE of the samples and maximum NSIDE of the 
                output map
            samples (int array): List of pixels representing the samples. e.g.
                the output of `healpy.ang2pix()`.
            max_value: maximum number of samples (or sum of weights) per pixel.
                Note that due to limitations of the input ``nside``, the output
                could contain pixels with a value largen than this
            nest (bool): Whether the samples are in NESTED or RING scheme
            weights (array): Optionally weight the samples. Both must have the
                same size.
            coordsys (BaseFrameRepresentation or str): Assigns a coordinate system to the map

        Return:
            HealpixMap
        """

        # Standarize samples
        if not nest:
            samples = array([hp.ring2nest(nside, pix) for pix in samples])


        if weights:
            samples = np.rec.fromarrays([samples, weights],
                                        names = ['pix', 'wgt'])

        else:
            samples = np.rec.fromarrays([samples],
                                 names = ['pix'])

        samples.sort(order = 'pix')

        # Get empty mesh by reusing adaptive_moc_mesh
        def value_fun(start, stop):

            start_pos, stop_pos = np.searchsorted(samples.pix, [start, stop])

            if weights:
                value = sum(samples.wgt[start_pos:stop_pos])
            else:
                value = stop_pos - start_pos

            return value
                
        if weights:
            dtype = array(weights).dtype
        else:
            dtype = int
        
        moc_map = cls.adaptive_moc_mesh(nside,
                                        lambda i,f: value_fun(i,f) > max_value,
                                        density = False,
                                        dtype = dtype,
                                        coordsys = coordsys,
                                        unit = unit)

        # Fill
        rangesets = moc_map.pix_rangesets(hp.MAX_NSIDE)

        for pix,(start,stop) in enumerate(rangesets):
            
            moc_map[pix] = value_fun(start // moc_map._npix_ratio_max,
                                     stop // moc_map._npix_ratio_max)

        return moc_map

        
    def to_moc(self, max_value):
        """
        Convert a single-resolution map into a MOC based on the maximum value
        a given pixel the latter should have. 

        .. note:: 
            
            The maximum nside of the MOC map is the same as the nside of the 
            single-resolution map, so the output map could contain pixels with 
            a value greater than this.

        If the map is already a MOC map, it will recompute the grid accordingly
        by combining uniq pixels. Uniq pixels are never split. 

        Also see the more generic ``adaptive_moc_mesh()``.

        Args:
            max_value: Maximum value per pixel of the MOC. Whether the map is
                histogram-like or density-like is taken into account.

        Return:
            HealpixMap
        """

        max_value = self._strip_units(max_value)
        
        # Get empty mesh by reusing adaptive_moc_mesh
        if self.is_moc or self.is_ring:
            # MOC map, will work in rangesets

            rs, rs_argsort = self.pix_rangesets(self.nside, argsort = True)

            def _nest2pix(start,stop):
                # Same as nest2pix but avoids recomputing the rangesets and sorting
                
                return  np.searchsorted(rs.start, [start,stop],
                                        sorter = rs_argsort)

                
            def value_fun(start, stop):

                start_pos, stop_pos = _nest2pix(start, stop)

                pix = rs_argsort[start_pos:stop_pos]

                if self._density:
                    # Weighted average
                    value = sum((rs.stop[pix]-rs.start[pix])*self._data[pix]) / pix.size
                else:
                    # Simple sum
                    value = sum(self._data[pix])

                return value
                    
            def split_fun(start,stop):

                start_pos, stop_pos = _nest2pix(start, stop)

                if stop_pos - start_pos == 1:
                    # A single pixel, don't split
                    return False
                else:

                    pix = rs_argsort[start_pos:stop_pos]
                    
                    if self._density:
                        return max(self._data[pix]) > max_value

                    else:
                        return sum(self._data[pix]) > max_value
                    
        else:
            # Single resolution map
            
            def value_fun(start, stop):
                value = sum(self._data[start:stop])

                if self._density:
                    value /= stop-start

                return value

            def split_fun(start, stop):
                if self._density:
                    return max(self._data[start:stop]) > max_value
                else:
                    return value_fun(start,stop) > max_value

        moc_map = self.adaptive_moc_mesh(self.nside,
                                         split_fun,
                                         density = self._density,
                                         dtype = self.dtype,
                                         unit = self.unit)

        # Fill
        rangesets = moc_map.pix_rangesets(self.nside)

        if self.unit is None:
            for pix,(start,stop) in enumerate(rangesets):
                
                moc_map[pix] = value_fun(start, stop)

        else:
            for pix,(start,stop) in enumerate(rangesets):
                
                moc_map[pix] = value_fun(start, stop) * self.unit

        return moc_map

    def density(self, density = None, update = True):
        """
        Switch between a density-like map and a histogram-like map.

        Args:
            density (bool or None): Whether the value of each pixel should be treated as
                counts in a histogram (``False``) or as the value of a [density]
                function evaluated at the center of the pixel (``True``). This affect 
                operations involving the splitting of a pixel. ``None`` will leave 
                this paramter unchanged.
            update (bool): If True, the values of the map will be updated accordingly.
                Otherwise only the density parameter is changed.

        .. note::
        
            The ``updat=True`` the pixels values are divided/multiplied by their
            effective number of pixels rather than their solid angle area. In 
            order to achieve this scale the map by `1/m.pixarea()`

        Return:
            bool: The current density

        """
        if density is not None:

            if self._density != density:

                self._density = density

                if update:

                    if self.is_moc:
                        ranges = self.pix_rangesets(self.nside)
                        factor = ranges.stop - ranges.start
                    else:
                        factor = 1

                    if density:
                        # From histogram-like to density-like
                        self._data = self._data / factor

                    else:
                        # From density-like to histogram-like
                        self._data = self._data * factor

        return self._density

    @property
    def data(self):
        """
        Get the raw data in the form of an array.
        """

        return self._data
        
    @property
    def dtype(self):
        return self._data.dtype
        
    def __eq__(self, other):

        return (self.conformable(other) and
                np.array_equal(self._data, other._data) and
                self._density == other._density and
                self.unit == other.unit)
                
    def __getitem__(self, key):

        if self.unit is None:
            return self._data[key]
        else:
            return self._data[key]*self.unit

    def _strip_units(self, quantity):

        if isinstance(quantity, u.Quantity):

            if quantity.unit == u.dimensionless_unscaled:
                return quantity.value
            
            if self.unit is None:
                return u.UnitConversionError("Map without units")

            return quantity.to_value(self.unit)

        elif isinstance(quantity, u.UnitBase):

            if quantity == u.dimensionless_unscaled:
                # Do no crash is self.unit is None
                return 1

            return quantity.to(self.unit)
        
        else:

            if self.unit is not None:
                raise u.UnitConversionError("Specify units")
            
            return quantity
        
    def __setitem__(self, key, value):

        self._data[key] = self._strip_units(value)
        
    def __imul__(self, other):

        return self._ioperation(other, operator.imul)

    def __mul__(self, other):

        return self._operation(other, operator.mul)

    def __rmul__(self, other):

        return self._roperation(other, operator.mul)

    def __itruediv__(self, other):

        return self._ioperation(other, operator.itruediv)

    def __truediv__(self, other):

        return self._operation(other, operator.truediv)

    def __rtruediv__(self, other):

        return self._roperation(other, operator.truediv)

    def __ifloordiv__(self, other):

        return self._ioperation(other, operator.ifloordiv)

    def __floordiv__(self, other):

        return self._operation(other, operator.floordiv)

    def __rfloordiv__(self, other):

        return self._roperation(other, operator.floordiv)

    def __iadd__(self, other):

        return self._ioperation(other, operator.iadd)

    def __add__(self, other):

        return self._operation(other, operator.add)

    def __radd__(self, other):
            
        return self._roperation(other, operator.add)

    def __isub__(self, other):

        return self._ioperation(other, operator.isub)

    def __sub__(self, other):

        return self._operation(other, operator.sub)

    def __rsub__(self, other):
 
        return self._roperation(other, operator.sub)

    def __ipow__(self, other):

        return self._ioperation(other, operator.ipow)

    def __pow__(self, other):

        return self._operation(other, operator.pow)

    def __neg__(self):

        new = deepcopy(self)

        new._data *= -1

        return new

    def __abs__(self):

        new = deepcopy(self)

        new._data = np.abs(new._data)
        
        return new
    
    def __array__(self):

        return self._data

    def __array_ufunc__(self, ufunc, method, *args, **kwargs):

        # Take care of units. Leave all other classes alone.
        args = tuple([a if not isinstance(a, self.__class__)
                      else self._data if self.unit is None
                      else self._data * self.unit
                      for a in args])

        return getattr(ufunc, method)(*args, **kwargs)
        
    def rasterize(self,
                  nside = None,
                  scheme = 'ring',
                  uniq = None,
                  order = None,
                  npix = None,
                  base = None):
        """
        Convert to map of a given NSIDE and scheme, or any arbitrary MOC mesh.

        Args:
            uniq (array): Explicit numbering of each pixel in an "NUNIQ" scheme.
            Order (int): Order of HEALPix map.
            nside (int): Alternatively, you can specify the NSIDE parameter.
            npix (int): Alternatively, you can specify the total number of pixels.
            scheme (str): Healpix scheme. Either 'RING', 'NESTED' or 'NUNIQ'
            base (HealpixBase): Alternatively, you can copy the properties of another
                HealpixBase object
        
        Return:
            HealpixMap
        """

        base = HealpixBase(uniq = uniq,
                           order = order,
                           nside = nside,
                           npix = npix,
                           scheme = scheme,
                           coordsys = self.coordsys,
                           base = base)

        if self.conformable(base):
            # Same grid, nothing to do
            
            return deepcopy(self)

        else:
            # All other case can be handled with the identity operation
            
            raster = HealpixMap(base = base,
                                density = self._density,
                                unit = self.unit)

            raster._ioperation(self, lambda a,b: b)

            return raster
        
    @staticmethod
    def _density_operation(map0, map1, operation):
        """
        Get the density parameter resulting from a binary operation
        """
            
        if operation in [operator.add, operator.iadd,
                         operator.sub, operator.isub]:
            # +/-

            # Either a well-defined operation between the same density parameter
            # or default to the left-most operand
            
            return map0._density

        elif operation in [operator.mul, operator.imul]:
            # *
            
            if map0._density != map1._density:

                # A histogram times a density is a [weighted] histogram
                
                return False

            else:

                # Both are the same type.
                # Density*density is well defined and result in density
                # Return left-most for ill-deined histogram*histogram

                return map0._density

        elif operation in [operator.truediv, operator.itruediv,
                           operator.floordiv, operator.ifloordiv]:
            # /

            if not (map0._density or map1._density):

                # Ratio of two histogram-like maps is a density
                return True

            else:

                return map0._density

        else:
            # Identity (rasterizer), **, other (?)
            
            # Return left-most.
            return map0._density
                    
                
    def _roperation(self, other, operation):

        if not np.isscalar(other):
            raise ValueError("Operations can only occur between maps or a "
                             "map and a scalar")

        m = deepcopy(self)

        m._data = operation(other, m._data)
        
        return m
        
    def _operation(self, map1, operation):

        # If second is not a map (e.g. scalar or array), we'll keep the grid
        # If any map is MOC, result will be MOC. Grid is updated.
        # If both are single-resolution, result will have the finest grid
        # If both are single resolution and same order, scheme will correspond
        # to first operand
        # If maps are conformable, the output grid remains unchanged

        map0 = self
        
        if np.ndim(map1) == 0:
            # Operation by a scalar

            map0 = deepcopy(map0)

            map0._ioperation(map1, operation)

            return map0

        else:

            # Get the value part of map1 and the new unit the result should have
            map1,new_unit = map0._unit_operation(map1, operation) 
            
            # Cast to HealpixMap if needed. It needs to have the same grid as
            # self for this to work
            if not isinstance(map1, HealpixMap):

                map1 = HealpixMap(data = map1,
                                  base = self,
                                  density = True,
                                  coordsys = self.coordsys)

            # Temporarily disable unit conversion in []
            map1_unit = map1.unit 
            map1._unit = None
            map0._unit = None
                
            # Check coordsys
            if map0.coordsys is None or map1.coordsys is None:
                equiv_coordsys = map0.coordsys is map1.coordsys
            else:
                equiv_coordsys = map0.coordsys == map1.coordsys

            if not equiv_coordsys:
                raise ValueError("All maps must have the same coordinate system")
                
            # Optimize for different cases
            if (map0.is_moc or map1.is_moc) and not map0.conformable(map1):
                
                # Multi-resolution map
                # This will change the underlaying NUNIQ grid

                # Convert pixel numbers to an equivalent sorted list of nested
                # rangeset for highest posible order
                max_nside = max(map0.nside, map1.nside)

                rs0, sort0 = map0.pix_rangesets(max_nside, argsort = True)
                rs1, sort1 = map1.pix_rangesets(max_nside, argsort = True)

                # Initialize new data with highest possible number of pixels,
                # some will be discarded at the end but this is fasten than append
                new_uniq = np.zeros(map0.npix + map1.npix, dtype = int)
                new_data = np.zeros(map0.npix + map1.npix, dtype = map0._data.dtype)

                pos0 = 0
                pos1 = 0

                pix_new = 0

                start = 0 # Rangeset start of new pixel

                while pos0 < map0.npix and pos1 < map1.npix:

                    # Get input values
                    pix0   = sort0[pos0]
                    range0 = rs0[pix0]
                    value0 = map0[pix0] 

                    pix1   = sort1[pos1]
                    range1 = rs1[pix1]
                    value1 = map1[pix1]
                    
                    stop = min(range0[1], range1[1]) # Rangeset stop of new pixel

                    # Handle density maps
                    npix_new = stop - start

                    if not map0._density:
                        npix_ratio0 = npix_new / (range0[1]-range0[0])
                        value0 = value0 * npix_ratio0

                    if not map1._density:
                        npix_ratio1 = npix_new / (range1[1]-range1[0])
                        value1 = value1 * npix_ratio1

                    # Operation
                    value = operation(value0, value1)

                    new_uniq[pix_new] = hp.range2uniq(max_nside,
                                                        (start, stop))
                    new_data[pix_new] = value

                    # Advance to next pixel
                    pix_new += 1

                    if stop == range0[1]:
                        pos0 += 1

                    if stop == range1[1]:
                        pos1 += 1

                    start = stop

                # Update density parameter
                new_density = self._density_operation(map0, map1, operation)

                # Restore units in other
                map1._unit = map1_unit
                
                # Create new map
                return HealpixMap(new_data[:pix_new],
                                  new_uniq[:pix_new],
                                  density = new_density,
                                  coordsys = self.coordsys,
                                  unit = new_unit)
                
            else:

                # Single-resolution or conformable, can reuse in-place operation

                # Compute new density before possible change of left-most operand
                new_density = self._density_operation(map0, map1, operation)
                
                if map1.order > map0.order:
                    map0,map1 = map1,map0

                map0 = deepcopy(map0)
                    
                map0 = map0._ioperation(map1, operation)

                map0.density(new_density, False)

                return map0

    
    def _ioperation(self, map1, operation):

        map0 = self

        # Get the value part of map1 and the new unit the result should have
        map1,new_unit = map0._unit_operation(map1, operation) 

        if np.ndim(map1) == 0:
            # Operation by a scalar

            map0._data = operation(map0._data, map1)

        else:

            # Operation by another map or something that can be turned into a map

            # Cast to HealpixMap if needed. It needs to have the same grid as
            # self for this to work
            if not isinstance(map1, HealpixMap):
                map1 = HealpixMap(data = map1,
                                  base = self,
                                  density = True,
                                  coordsys = self.coordsys)

            # Temporarily disable unit conversion in []
            map1_unit = map1.unit 
            map1._unit = None
            map0._unit = None
                
            # Check coordsys
            if map0.coordsys is None or map1.coordsys is None:
                equiv_coordsys = map0.coordsys is map1.coordsys
            else:
                equiv_coordsys = map0.coordsys == map1.coordsys

            if not equiv_coordsys:
                raise ValueError("All maps must have the same coordinate system")
                
            # Optimize procedure for various situations
            if map0.conformable(map1):
                # Same underlaying grid, so easy operation

                map0._data = operation(map0._data, map1._data)

            elif ((map0.is_moc or map1.is_moc) or
                  ((map0.is_ring or map1.is_ring) and map0.order != map1.order)):

                # There is no clear optimization in this case
                # Will work in the rangeset representation

                max_nside = max(map0.nside, map1.nside)

                rs0, sort0   = map0.pix_rangesets(max_nside, argsort = True)
                pos0  = 0

                rs1, sort1 = map1.pix_rangesets(max_nside, argsort = True)
                pos1  = 0

                while pos0 < map0.npix and pos1 < map1.npix:

                    pix0 = sort0[pos0]
                    range0 = rs0[pix0]
                    len0 = range0[1] - range0[0]

                    pix1 = sort1[pos1]
                    range1 = rs1[pix1]
                    len1 = range1[1] - range1[0]

                    if len0 > len1:
                        # Downgrade pix1 by getting summing over child pixels
                        # (or weighted average, for a density map)

                        value0 = map0[pix0]
                        value1 = 0

                        while True:
                            # Will break when we catch up with map0

                            if map1._density:
                                # Will take the weighted average
                                value1 += len1 * map1[pix1]
                            else:
                                # Simple sum
                                value1 += map1[pix1]

                            if range0[1] == range1[1]:
                                break

                            pos1   += 1
                            pix1   = sort1[pos1]
                            range1 = rs1[pix1]
                            len1   = range1[1] - range1[0]

                        if map1._density:
                            value1 /= len0

                        map0[pix0] = operation(value0, value1)

                    else:

                        # Upgrade pix1 by dividing it up
                        # (or simply getting the value for density)

                        while True:
                            # Will break when we catch up with map1

                            value1 = map1[pix1]

                            if not map1._density:
                                value1 /= len1 // len0

                            value0 = map0[pix0]

                            map0[pix0] = operation(value0, value1)

                            if range0[1] == range1[1]:
                                break

                            pos0   += 1
                            pix0   = sort0[pos0]
                            range0 = rs0[pix0]
                            len0   = range0[1] - range0[0]

                    pos0 += 1
                    pos1 += 1
                
                
            elif map0.order == map1.order:
                # Same order, different scheme, single-resolution

                nside = map0.nside

                if map0.scheme == 'NESTED':
                    # map1 is RING, map0 is NESTED

                    for pix in range(map0.npix):

                        map0[pix] = operation(map0[pix],
                                              map1[hp.nest2ring(nside, pix)])

                else:
                    # map1 is NESTED, map0 is RING

                    for pix in range(map0.npix):

                        map0[pix] = operation(map0[pix],
                                              map1[hp.ring2nest(nside, pix)])

            else:

                # Only possibility left is that both are NESTED with different
                # order, which is easy to handle

                if map1.order > map0.order:
                    # Downgrade map1 by summing or getting the weighted average

                    npix_ratio = int(4**(map1.order - map0.order))

                    for pix in range(map0.npix):

                        value1 = sum(map1._data[pix*npix_ratio:(pix+1)*npix_ratio])

                        if map1._density:
                            value1 /= npix_ratio

                        map0._data[pix] = operation(map0._data[pix], value1)

                else:

                    # Upgrade map1 by splitting the pixel
                    # (or just use the value if density)

                    npix_ratio = int(4**(map0.order - map1.order))

                    for pix in range(map1.npix):

                        value1 = map1._data[pix]

                        if not map1._density:
                            value1 /= npix_ratio

                        pix0_start = pix*npix_ratio
                        pix0_stop = pix0_start + npix_ratio

                        map0._data[pix0_start: pix0_stop] = \
                            operation(map0._data[pix0_start: pix0_stop],
                                      value1)

            # Update density parameter
            new_density = self._density_operation(map0, map1, operation)

            map0.density(new_density, False)

            # Restore units in other
            map1._unit = map1_unit
            
        # Update units
        map0._unit = new_unit
            
        return map0

    def _unit_operation(self, other, operation):
        """
        Get the value part of the other operand and the new unit of the map
        """

        # Separate between value and unit
        if isinstance(other, HealpixMap):
            other_unit = other.unit
            other_value = other # It will be handled as a regular HealpixMap
        elif isinstance(other, Quantity):
            other_unit = other.unit
            other_value = other.value
        elif isinstance(other, UnitBase):
            other_unit = other
            other_value = 1
        else:
            # float, int, array, list
            other_unit = None
            other_value = np.array(other)

        if self.unit is None and other_unit is  None:
            # If neither operand have units, do nothing else
            return other_value, None

        # Adjust other_value and self.unit depending on the operand

        # Standarize dimensionless
        if other_unit is None:
            other_unit = u.dimensionless_unscaled

        old_unit = self.unit
        if old_unit is None:
            old_unit = u.dimensionless_unscaled
        
        # For * and / the conversion factor is stored in the unit itself
        # ** only accepts scalar dimensionaless quantities, it will crash anyway
        # The idencity operator (for the raterizer) doesn't use the other's units
        if operation in [operator.add, operator.iadd,
                         operator.sub, operator.isub]:
            
            # +, -
            # We need to correct the value by the conversion unit
            # No change in units
            other_value = other_value * other_unit.to(old_unit)
            new_unit = old_unit
            
        elif operation in [operator.mul, operator.imul,
                           operator.truediv, operator.itruediv,
                           operator.floordiv, operator.ifloordiv]:

            # *, /
            # The conversion factor is stored in the unit itself
            new_unit = operation(old_unit, other_unit)
                
        elif operation in [operator.ipow, operator.pow]:

            # **
            # The unit is also raised to the same power, including the value
            # Only works with scalar dimensionsless quantities

            new_unit = operation(old_unit, other)

        else:

            # identity (rasterizer), other (?)
            # No change in units.
            # Do not adjust other_value
            new_unit = old_unit
            
        return other_value, new_unit
    
    def get_wcs_img(self,
                wcs,
                coord = None,
                rasterize = True):
        """
        Rasterize map into a set of WCS axes.

        Args:
            wcs (WCS or WCSAxes): Astropy's WCSAxes to plot the map. Either
                an existing instance or the name of a registered projection.
            coord (str): Intrinsic coordinates of the map. Either ‘G’ (Galactic), 
                ‘E’ (Ecliptic) , ‘C’ (Celestial = Equatorial) or any other 
                coordinate frame recognized by astropy. The default is 'C' unless
                ``coordsys`` is defined. This option overrides ``coordsys``
            rasterize (bool): If True, the resulting image is equivalent to 
                having called ``rasterize()`` before plotting. This only affects 
                multi-resolution histogram-like maps.
            
        Return:
           array
        """

        if isinstance(wcs, WCSAxes):
            wcs = wcs.wcs

        if not isinstance(wcs, WCS):
            raise ValueError("Not a WCS or WCSAxes.")
        
        coord = self._default_coordsys(coord)
        
        # Get values
        class rasterizer:
            """
            This is a wrapper around [], that will divide the value of the pixel
            if the map is MOC and histogram-like. This will give the same result 
            as calling rasterize() first and then plotting the equivalent 
            single-resolution map
            """
            
            def __init__(self, map):
                self.map = map
            
            def __getitem__(self, pix):

                if self.map.is_moc and not self.map._density:

                    # Histogram-like MOC, will divide the pixel
                    pix_nside = hp.uniq2nside(self.map._uniq[pix]) 

                    pix_order = log2(pix_nside)
                    
                    npix_ratio = 4 ** (self.map.order - pix_order)

                    return  self.map[pix] / npix_ratio
                    
                else:

                    # Single resolution or density MOC, nothing to do
                    
                    return self.map[pix]

        if rasterize:
            effmap = rasterizer(self)
        else:
            effmap = self

        yind, xind = np.indices(wcs.array_shape)

        ang = wcs.pixel_to_world(xind, yind)

        try:
            ang = ang.transform_to(coord)
        except Exception as e:
            logger.warn(f"Failed to transform from '{coord.name}' to '{ang.frame.name}'. "
                        f"Rasterizing in '{coord.name}' frame. "
                        f"ERROR: {e}")
        
        ang = ang.represent_as('unitspherical')
        
        lon, lat = ang.lon.rad, ang.lat.rad
        
        out_pix = np.logical_and(np.isnan(lat), np.isnan(lon))
        in_pix = np.logical_not(out_pix)
        
        pix = np.empty(wcs.array_shape, dtype = int)
        pix[in_pix] = self.ang2pix(np.pi/2-lat[in_pix], lon[in_pix])
        
        img = np.empty(wcs.array_shape)
        img[out_pix] = np.nan
        img[in_pix] = effmap[pix[in_pix]]

        return img
    
    def plot(self,
             ax = 'mollview',
             ax_kw = None,
             rasterize = True,
             coord = None,
             cbar = True,
             **kwargs):
        """
        Plot map. This is a wrapper for matplotlib.pyplot.imshow

        Args:
            ax (WCSAxes or str): Astropy's WCSAxes to plot the map. Either
                an existing instance or the name of a registered projection.
            ax_kw (dict): Extra arguments if a new axes needs to be created.
                If ``ax`` is a HealpyAxes --e.g. mollview, cartview, orthview-- and
                ``ax_kw['coord']`` is not provided, it will attempt to match the
                intricsic coordinates. This is however only possible for 'C' and 'G',
                and will default to 'C' otherwise.
            rasterize (bool): If True, the resulting image is equivalent to 
                having called ``rasterize()`` before plotting. This only affects 
                multi-resolution histogram-like maps.
            coord (str): Intrinsic coordinates of the map. Either ‘G’ (Galactic), 
                ‘E’ (Ecliptic) , ‘C’ (Celestial = Equatorial) or any other 
                coordinate frame recognized by astropy. The default is 'C' unless
                ``coordsys`` is defined. This option overrides ``coordsys``
            cbar (bool): Whether to plot the colorbar.
            **kwargs: Passed to matplotlib.pyplot.imshow

        Return:
           AxesImage, WCSAxes: The first return value
               corresponds to the output ``imgshow``. The second is the astropy
               WCSAxes object used.
        """

        # Standarize axes, figure, and frame
        fig,ax,coord = self._default_fig_ax_coordsys(ax, ax_kw, coord)
        
        # Plot
        img = self.get_wcs_img(ax, coord = coord, rasterize = rasterize)
        
        plot =  ax.imshow(img, **kwargs)

        if cbar:
            fig.colorbar(plot, ax = ax,
                         orientation = 'horizontal',
                         pad = .05,
                         fraction = .1,
                         shrink = .5,
                         aspect = 25)
        
        return plot, ax
    
    def get_interp_val(self, theta, phi = None, lonlat = False):
        """
        Return the bi-linear interpolation value of a map using 4 nearest neighbours.

        For MOC maps, this is equivalent to rasterizing the map first to the
        highest order.

        Args:
            theta (float, array or SkyCoord): Zenith angle (rad)
            phi (float or array): Azimuth angle (rad)

        Return:
            scalar or array
        """

        pixels,weights = self.get_interp_weights(theta, phi, lonlat = lonlat)

        values = self[pixels]
            
        if self.is_moc and not self._density:
            # Split the pixels up to corresponding maximum order
            
            nside = hp.uniq2nside(self._uniq[pixels])
            
            npix_ratio =  int(4**self.order) / nside / nside
            
            values = values / npix_ratio

        if values.shape == (4,):
            # scalar input
            return np.dot(weights, values)
        return np.einsum('ij,ij->j', weights, values)

    def moc_sort(self):
        """
        Sort the uniq pixels composing a MOC map based on its 
        rangeset representation
        """

        if not self.is_moc:
            return

        rs, rs_argsort = self.pix_rangesets(hp.MAX_NSIDE, argsort = True)

        self._uniq = self._uniq[rs_argsort]
        self._data = self._data[rs_argsort]

        if self._pix_rangesets is not None:
            self._pix_rangesets = self._pix_rangesets[rs_argsort]

        if self._pix_rangesets_argsort is not None:
            self._pix_rangesets_argsort = np.arange(self.npix)
