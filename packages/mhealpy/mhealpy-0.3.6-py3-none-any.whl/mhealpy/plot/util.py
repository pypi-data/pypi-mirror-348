
import matplotlib.pyplot as plt

from astropy.visualization.wcsaxes import WCSAxes
from astropy.coordinates import ICRS, Galactic, BarycentricMeanEcliptic, BaseCoordinateFrame, frame_transform_graph

def healpy_coord_to_astropy(coord):

    if isinstance(coord, str):

        # Transform for common HEALPix coordsys when possible
        # If unrecognized, return as input so astropy looks in
        # it registered coord frames
        
        coord = coord.lower() 
        
        if coord == 'c':
            coord = 'icrs'
        elif coord == 'g':
            coord = 'galactic'
        elif coord == 'e':
            coord = 'barycentricmeanecliptic'

    return coord

def astropy_frame_to_healpy(coord):

    if coord is None:
        return None
    
    if not isinstance(coord, BaseCoordinateFrame):
        coord = frame_transform_graph.lookup_name()

    # Use common HEALPix coordsys when possible, and default
    # to using the coordinate frame name
    if isinstance(coord, ICRS):
        return 'c'
    elif isinstance(coord, Galactic):
        return 'g'
    elif isinstance(coord, BarycentricMeanEcliptic):
        return 'e'
    elif hasattr(coord, 'name'):
        return coord.name
    else:
        return None
