import numpy as np

from mhealpy import HealpixMap

def find_peaks(m, height = None):
    """
    Get the pixel numbers for all local maxima.

    Args:
        height (float, array, HealpixMap): Required height of peaks. Either a number, 
            None, a map or a 2-element sequence of the former. The first element is 
            always interpreted as the minimal and the second, if supplied, as the 
            maximal required height.

    Return:
        array
    """

    # Standarize min/max height
    if isinstance(height, (list, np.ndarray)):

        if np.len() != 2:
            raise ValueError(f"Wrong height shape {height.shape}")
        
        min_height = height[0]
        max_height = height[1]

    else:

        min_height = height
        max_height = None

    # Rasterize maps if needed
    if isinstance(min_height, HealpixMap):
        min_height = min_height.rasterize(m).data

    if isinstance(max_height, HealpixMap):
        max_height = max_height.rasterize(m).data

    # Standarize None
    if min_height is None:
        min_height = -np.inf

    if max_height is None:
        max_height = np.inf

    # Get pixels within height limits and their neighbors
    height_pix = np.argwhere(np.logical_and(m.data >= min_height,
                                            m.data <  max_height))[:,0]

    height_pix_nb = m.get_all_neighbours(height_pix)
    
    # A pixel is a local maxima is all neighbohrs have a value less than the pixel
    peak_pix = height_pix[np.where(np.all(m[height_pix] >= m[height_pix_nb], axis = 0))]
    
    return peak_pix
