# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:34:41 2021

@author: jufen
"""


import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1
import matplotlib as mpl


def rotate_coordinates(x, y, theta):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    x_rot = x*cos_theta + y*sin_theta
    y_rot = -x*sin_theta + y*cos_theta
    return x_rot, y_rot


def set_font(size=14, font_type='Times New Roman'):

    mpl.style.use('classic')
    # Latex font
    # Say, "the default sans-serif font is COMIC SANS"
    plt.rcParams['font.sans-serif'] = "Times New Roman"
    # Then, "ALWAYS use sans-serif fonts"
    plt.rcParams['font.family'] = "sans-serif"
    #plt.rcParams['font.family'] = font_type # #'STIXGeneral'
    SMALL_SIZE = size
    MEDIUM_SIZE = size + 2
    BIGGER_SIZE = size + 2

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)    # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title



def add_colorbar(im, aspect=15, pad_fraction=1.0, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)



def plot_2d_contour(array, extent=None, cmap='coolwarm', xlabel=None,
                    ylabel=None, cbar_label=None, title=None,
                    xticks=None, yticks=None,
                    ratio=1.0, cbar_shrink=1, cbar_aspect=20):

    fig, ax = plt.subplots(1, 1)
    im = ax.imshow(np.flipud(array.T), cmap=cmap, extent=extent)

    cbar = None

    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)

    cbar = fig.colorbar(im, shrink=cbar_shrink, aspect=cbar_aspect)
    cbar.set_label(cbar_label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.title(title)
    plt.tight_layout()

    return fig, cbar



def plot_power_ct_curve(ws, power_range, Ct_range, title=None):
    fig, ax1 = plt.subplots()
    ax1.plot(ws, power_range, 'b-')
    ax1.set_xlabel('Wind speed [m/s]')
    ax1.set_ylabel('Power [MW]', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    plt.ylim(0, max(power_range)*1.1)
    
    ax2 = ax1.twinx()
    ax2.plot(ws, Ct_range, 'r-')
    ax2.set_ylabel('Ct [-]', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.ylim(0, 1)

    if title is not None:
        plt.title(title)
    
    plt.tight_layout()

    return fig



def plot_wind_rose(wind_speed, wind_direction, num_bins=12, speed_bins=None,
                   colormap='viridis', title='Wind rose', 
                   legend_label='Wind Speed [m/s]'):
    """
    Plots a wind rose with different wind speed ranges in different colors.

    Parameters:
        wind_speed (array-like): Array of wind speeds.
        wind_direction (array-like): Array of wind directions in degrees.
        num_bins (int): Number of bins for wind direction.
        speed_bins (array-like): Array of wind speed bin edges.
        colormap (string): colormap used in the wind speed legend, like 
            'viridis', 'coolwarm', etc.
        title (string): title of the figure, default: 'wind rose'.
        legend_label (string): title of the wind speed legend.

    Returns:
        fig
    """
    if speed_bins is None:
        speed_bins = [0, 5, 10, 15, 20, 25, np.inf]  # Default speed bins

    # Convert wind direction to radians
    wind_direction_rad = np.deg2rad(wind_direction)

    # Create bins for wind direction
    direction_bins = np.linspace(0, 2 * np.pi, num_bins + 1) - (np.pi/num_bins)
    direction_bin_centers = (direction_bins[:-1] + direction_bins[1:]) / 2

    # Initialize histogram
    hist = np.zeros((len(speed_bins) - 1, num_bins))

    # Populate histogram
    for i in range(len(speed_bins) - 1):
        mask = (wind_speed >= speed_bins[i]) & (wind_speed < speed_bins[i + 1])
        hist[i], _ = np.histogram(wind_direction_rad[mask], 
                                  bins=direction_bins)

    # Plot wind rose
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    cm = eval(f'plt.cm.{colormap}')
    colors = cm(np.linspace(0, 1, len(speed_bins) - 1))

    for i in range(len(speed_bins) - 1):
        if speed_bins[i+1] is np.inf:
            label=f'>={speed_bins[i]} m/s'
        else:
            label=f'{speed_bins[i]}-{speed_bins[i+1]} m/s'

        bars = ax.bar(direction_bin_centers, hist[i], 
                      width=(2 * np.pi / num_bins), 
                      bottom=np.sum(hist[:i], axis=0), color=colors[i], 
                      edgecolor='black', label=label)

    # Add labels and title
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title(title)
    ax.legend(title=legend_label, bbox_to_anchor=(0.92, 1.07), 
              loc='upper left')
    plt.tight_layout()

    return fig



def save_PRNG_state_in_pickle(save_path='.', 
                              file_name='PRNG_state.pkl'):
    state = np.random.get_state()

    state_dict = {
        'algorithm': state[0],
        'keys': state[1],
        'pos': state[2],
        'has_gauss': state[3],
        'cached_gaussian': state[4]}

    with open(os.path.join(save_path, file_name), 
              'wb') as f: 
        pickle.dump(state_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

    return state_dict



def set_PRNG_state_in_pickle(pickle_file='PRNG_state.pkl'):
    with open(pickle_file, 'rb') as f:
        state_dict = pickle.load(f)
    
    state = (state_dict['algorithm'],
             state_dict['keys'],
             state_dict['pos'],
             state_dict['has_gauss'],
             state_dict['cached_gaussian'])
    
    np.random.set_state(state)

    return state



def closestDistanceBetweenLines(
    a0,a1,b0,b1,
    clampAll=True,clampA0=True,clampA1=True,clampB0=True,clampB1=True):

    """ Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
        Return the closest points on each segment and their distance
        
        source: https://stackoverflow.com/questions/2824478/shortest-distance-between-two-line-segments
    """

    # If clampAll=True, set all clamps to True
    if clampAll:
        clampA0=True
        clampA1=True
        clampB0=True
        clampB1=True


    # Calculate denomitator
    A = a1 - a0
    B = b1 - b0
    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)
    
    _A = A / magA
    _B = B / magB
    
    cross = np.cross(_A, _B);
    denom = np.linalg.norm(cross)**2
    
    
    # If lines are parallel (denom=0) test if lines overlap.
    # If they don't overlap then there is a closest point solution.
    # If they do overlap, there are infinite closest positions, but there is a closest distance
    if not denom:
        d0 = np.dot(_A,(b0-a0))
        
        # Overlap only possible with clamping
        if clampA0 or clampA1 or clampB0 or clampB1:
            d1 = np.dot(_A,(b1-a0))
            
            # Is segment B before A?
            if d0 <= 0 >= d1:
                if clampA0 and clampB1:
                    if np.absolute(d0) < np.absolute(d1):
                        return a0,b0,np.linalg.norm(a0-b0)
                    return a0,b1,np.linalg.norm(a0-b1)
                
                
            # Is segment B after A?
            elif d0 >= magA <= d1:
                if clampA1 and clampB0:
                    if np.absolute(d0) < np.absolute(d1):
                        return a1,b0,np.linalg.norm(a1-b0)
                    return a1,b1,np.linalg.norm(a1-b1)
                
                
        # Segments overlap, return distance between parallel segments
        return None,None,np.linalg.norm(((d0*_A)+a0)-b0)
        
    
    
    # Lines criss-cross: Calculate the projected closest points
    t = (b0 - a0);
    detA = np.linalg.det([t, _B, cross])
    detB = np.linalg.det([t, _A, cross])

    t0 = detA/denom;
    t1 = detB/denom;

    pA = a0 + (_A * t0) # Projected closest point on segment A
    pB = b0 + (_B * t1) # Projected closest point on segment B


    # Clamp projections
    if clampA0 or clampA1 or clampB0 or clampB1:
        if clampA0 and t0 < 0:
            pA = a0
        elif clampA1 and t0 > magA:
            pA = a1
        
        if clampB0 and t1 < 0:
            pB = b0
        elif clampB1 and t1 > magB:
            pB = b1
            
        # Clamp projection A
        if (clampA0 and t0 < 0) or (clampA1 and t0 > magA):
            dot = np.dot(_B,(pA-b0))
            if clampB0 and dot < 0:
                dot = 0
            elif clampB1 and dot > magB:
                dot = magB
            pB = b0 + (_B * dot)
    
        # Clamp projection B
        if (clampB0 and t1 < 0) or (clampB1 and t1 > magB):
            dot = np.dot(_A,(pB-a0))
            if clampA0 and dot < 0:
                dot = 0
            elif clampA1 and dot > magA:
                dot = magA
            pA = a0 + (_A * dot)

    
    return pA,pB,np.linalg.norm(pA-pB)
