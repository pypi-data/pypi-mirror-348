from matplotlib.projections import register_projection
from matplotlib.transforms import Bbox
from matplotlib.gridspec import SubplotSpec, GridSpec

from astropy.wcs import WCS
from astropy.visualization.wcsaxes import WCSAxes
from astropy.visualization.wcsaxes.frame import EllipticalFrame
from astropy import units as u
from astropy.coordinates import Angle
    
import numpy as np
from numpy import sqrt

import warnings

from copy import deepcopy

class HealpyAxes(WCSAxes):

    def __init__(self, fig, *rect,
                 coord = 'C',
                 flip = 'astro',
                 rot = 0,
                 **kwargs):
        """
        Base class for WCSAxes that behave similar to healpy's projections.

        Args:
            coord (str): Coordinate system. Either ‘G’ (galactic) or 'C' 
                (celestial, aka equatorial). Note: Ecliptic coordinates are 
                currenty not supported by astropy WCS implementation.
            flip (str): Defines the convention of projection : ‘astro’ 
                (default, east towards left, west towards right) or 
                ‘geo’ (east towards roght, west towards left)
            rot (array): Describe the rotation to apply. In the form 
                (lon, lat, psi) (unit: degrees) : the point at longitude lon 
                and latitude lat will be at the center. An additional rotation 
                of angle psi around this direction is applied.
        """
        
        # Get equivalent WCS FITS header
        naxis1,naxis2 = self._get_naxis(fig, *rect)

        if self._autoscale:
            # Gnom specifies the reosolution and the limits are adjusted based
            # on the figure sizes
            # For the others the limits are fixed and the resolution is adjusted
            # by scaling a normalized appropiate resolution
            self._cdelt *= 360/naxis1

        if np.isscalar(rot):
            rot = [rot,0,0]
        
        if flip == "astro":
            flipsgn = -1
        elif flip == "geo":
            flipsgn = 1
        else:
            raise ValueError("Flip can only be 'astro' or 'geo'")

        crpix1 = (naxis1+1)/2 - flipsgn * self._center[0] / self._cdelt
        crpix2 = (naxis2+1)/2 - self._center[1] / self._cdelt
            
        ctype1, ctype2 = self._get_ctype(coord)

        header = { "NAXIS": 2, 
                   "CTYPE1": ctype1,
                   "NAXIS1": naxis1,
                   "CRPIX1": crpix1,
                   "CRVAL1": rot[0], 
                   "CDELT1": flipsgn * self._cdelt,
                   "CUNIT1": 'deg     ',
                   "CTYPE2": ctype2,
                   "NAXIS2": naxis2,
                   "CRPIX2": crpix2,
                   "CRVAL2": rot[1],
                   "CDELT2": self._cdelt,
                   "CUNIT2": 'deg     ',
                   "PV1_1": 0,
                   "PV1_2": 90,
                   "LONPOLE": -rot[2]}
        
        super().__init__(fig, *rect,
                         wcs = WCS(header),
                         xlim = (0, naxis1),
                         ylim = (0, naxis2),
                         aspect = 1,
                         **kwargs)

        # Match healpy's default
        self.coords[0].set_ticks_visible(False)
        self.coords[1].set_ticks_visible(False)
        self.coords[0].set_ticklabel_visible(False)
        self.coords[1].set_ticklabel_visible(False)
        
    def graticule(self, dpar = 30, dmer = 30, grid = True,
                  ticks = False, tick_format = 'd', frame = True, **kwargs):
        """
        Draw axes grid and ticks

        Args:
            dpar (float): Interval for the latitude axis (parallels)
            dmer (float): Interval for the longitude axis (meridians)
            grid (bool): Whether to show the grid
            ticks (bool): Whether to shoe the tick labels
            tick_format ('str'): Tick label formater. e.g. 'dd:mm:ss.s', 
                'hh:mm:ss.s', 'd.d'
            frame (bool): Draw plot frame  
        """
        
        self.grid(grid, **kwargs)
        self.coords[0].set_ticks(spacing=dmer * u.deg)
        self.coords[1].set_ticks(spacing=dpar * u.deg)

        if frame:
            self.coords.frame.set_linewidth(kwargs.get('linewidth', 1))
            self.coords.frame.set_color(kwargs.get('color', 'black'))
        else:
            self.coords.frame.set_linewidth(0)            
            
        self.coords[0].set_ticklabel_visible(ticks)
        self.coords[1].set_ticklabel_visible(ticks)

        self.coords[0].set_major_formatter(tick_format)
        
    def delgraticules(self):
        """
        Do not show grid and ticks
        """
        
        self.graticule(grid = False, ticks = False, frame = False)
        
    def _get_naxis(self, fig, *rect):
        """
        Return approapiate NAXIS1 and NAXIS2 for a given figure and Bbox (or bounds)
            
        aspect = naxis2/naxis1
        """
        if len(rect) == 1:
            if isinstance(rect[0], Bbox):
                rect = rect[0]
            elif isinstance(rect[0], SubplotSpec):
                rect = rect[0].get_position(fig)
            elif np.iterable(rect[0]):
                return self._get_naxis(fig, *rect[0])
            else:
                raise ValueError("rect format not recognized. Fix me!")
        elif len(rect) == 4:
            rect = Bbox.from_bounds(*rect)
        elif len(rect) == 3:
            rect = GridSpec(*rect[:2])[rect[2]-1].get_position(fig)
        else:
            raise ValueError("rect format not recognized. Fix me!")            
            

        naxis1 = fig.get_figwidth() * fig.dpi * rect.width
        naxis2 = fig.get_figheight() * fig.dpi * rect.height

        if self._aspect is not None:
            naxis2 = min(naxis2, naxis1/self._aspect)
            naxis1 = naxis2 * self._aspect
            
        return int(naxis1), int(naxis2)
    
    def _get_ctype(self, coord):
        """
        Coordinate system. Galactic, Ecliptic or Celestial.
        """
        
        if coord == 'G':
            ctype1 = 'GLON-'
            ctype2 = 'GLAT-'
        elif coord == 'E':

            # Remove when this issue is addressed https://github.com/astropy/astropy/issues/6483
            raise ValueError("Ecliptic coordinates are not yet supported by astropy's WCS implementation")

            ctype1 = 'ELON-'
            ctype2 = 'ELAT-'
            
        elif coord == 'C':
            ctype1 = 'RA---'
            ctype2 = 'DEC--'
        else:
            raise ValueError("Coordinate system can only be 'C', 'G' or 'E'.")
        
        ctype1 += self._wcsproj
        ctype2 += self._wcsproj
        
        return ctype1, ctype2

class HealpyAxesCylindrical(HealpyAxes):

    def __init__(self, *args, rot = 0, **kwargs):
        """
        For cylindrical or pseudocylindrical coordinates whose center is at
        lon,lat = (0,0) instead of (0,90) for zenithal coordinates
        """
        
        # WCSAxis uses a ~ZXZ (see rotation matrix in Eq. B.1 of
        # Representations of celestial coordinates in FITS (Paper II),
        # Calabretta, M. R., and Greisen, E. W., Astronomy & Astrophysics, 395,
        # 1077-1122, 2002) while healpy assumes ZYX.
        # This performs the transformation.
        
        if np.isscalar(rot):
            rot = [rot,0,0]

        rot = np.deg2rad(rot)

        cosr = np.cos(rot)
        sinr = np.sin(rot)

        A33 = cosr[1] * cosr[2]

        if np.isclose(A33, 1):

            # Rotatin around zenith, angles are ambigous.
            
            alpha0 = 0

            delta0 = np.pi/2

            phi0 = np.arctan2(cosr[1] * sinr[0],
                              -cosr[0] * cosr[1])

        else:

            alpha0 = np.arctan2(-cosr[2] * sinr[0] * sinr[1] - cosr[0] * sinr[2],
                                -cosr[0] * cosr[2] * sinr[1] + sinr[0] * sinr[2])

            delta0 = np.arcsin(A33)

            phi0 = np.arctan2(cosr[1] * sinr[2],
                              sinr[1])

        rot = np.rad2deg([alpha0, delta0, -phi0])
        
        super().__init__(*args,
                         rot = rot,
                         **kwargs)
    
class Mollview(HealpyAxesCylindrical):

    name = "mollview"
    _wcsproj = "MOL"
    _aspect = 2
    _cdelt = 2*sqrt(2)/np.pi # Sqrt of pixel size
    _autoscale = True
    _center = [0,0]
    
    def __init__(self, *args, **kwargs):
    
        super().__init__(*args,
                         frame_class = kwargs.pop('frame_class', EllipticalFrame),
                         **kwargs)
        
register_projection(Mollview)

class Orthview(HealpyAxes):

    name = "orthview"
    _wcsproj = "SIN"
    _aspect  = 1
    _center = [0,0]
    
    # Sqrt of pixel area at point of tangency. Sign matches healpy
    _cdelt = -1/np.pi 
    _autoscale = True

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args,
                         frame_class = kwargs.pop('frame_class', EllipticalFrame),
                         **kwargs)

register_projection(Orthview)

class Cartview(HealpyAxesCylindrical):

    name = "cartview"
    _wcsproj = "CAR"

    _autoscale = True
    
    def __init__(self,
                 *args,
                 rot = 0,
                 latra = [-90,90],
                 lonra = [-180,180],
                 **kwargs):
        """
        Args:
           latra (array): Range in latitude
           lonra (array): Range in longitude
        """

        if latra[0] > latra[1] or latra[0] < -90 or latra[1] > 90:
            raise ValueError("Wrong argument lonra or latra. "
                             "Must be lonra=[a,b],latra=[c,d] c<d, c>=-90, d<=+90")

        delta_lat = latra[1] - latra[0]

        lonra = (np.array(lonra) + 180) % 360 - 180

        if lonra[1] < lonra[0]:

            # Plot contains the antimeridian.
            # Plot the opposite lonra and rotate by 180deg instead
            # to avoid being out of the axes limits

            lonra -= 180
            lonra = (np.array(lonra) + 180) % 360 - 180

            if np.isscalar(rot):
                rot += 180
            else:
                rot = deepcopy(rot)
                rot[0] += 180
                rot[1] = -rot[1]
                rot[2] = -rot[2]                

        elif np.isclose(lonra[0], lonra[1]):
            # Full map
            lonra = [-180,180]
                
        delta_lon = lonra[1] - lonra[0]

        self._aspect = delta_lon/delta_lat

        self._center = [lonra[0] + delta_lon/2, latra[0] + delta_lat/2]

        self._cdelt = delta_lon/360
        
        super().__init__(*args, rot = rot, **kwargs)

register_projection(Cartview)

class Gnomview(HealpyAxes):

    name = "gnomview"
    _wcsproj = "TAN"

    _aspect = None # Free
    _autoscale = False # Fixed resolution. Will set _cdelt on init

    _center = [0,0]
    
    def __init__(self, *args, reso = 1.5, **kwargs):
        """
        Args:
            reso (float): Resolution (in arcmin). i.e. pixel size in final image.
        """
        
        self._cdelt = -Angle(reso*u.arcmin).deg
        
        super().__init__(*args, **kwargs)

register_projection(Gnomview)
