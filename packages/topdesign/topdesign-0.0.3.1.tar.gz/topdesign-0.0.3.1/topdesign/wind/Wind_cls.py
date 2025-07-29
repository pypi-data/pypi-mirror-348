# -*- coding: utf-8 -*-
"""
First created on in 2021.
Updated in Feb. 2023.
@author: Ju Feng
"""

import numpy as np
from scipy.interpolate import interp1d
from math import gamma


def Sector2Subsector(para, axis=-1, wd_binned=None, interp_method='piecewise'):
    """ Expand para on the wind direction dimension, i.e., increase the nubmer
    of sectors (sectors to subsectors), by interpolating between sectors, using
    specified method.

    Parameters
    ----------
    para : array_like
        Parameter to be expand, it can be sector-wise Weibull A, k, frequency.
    axis : integer
        Denotes which dimension of para corresponds to wind direction.
    wd_binned : array_like
        Wind direction of subsectors to be expanded to.
    inter_method : string
        'piecewise'/'linear'/'spline', based on interp1d in scipy.interpolate,
        'spline' means cubic spline.

    --------------------------------------
    Note: the interpolating method for sector-wise Weibull distributions and
    joint distribution of wind speed and wind direction is referred to the
    following paper:
        Feng, J. and Shen, W.Z., 2015. Modelling wind for wind farm layout
        optimization using joint distribution of wind speed and wind direction.
        Energies, 8(4), pp.3075-3092. [https://doi.org/10.3390/en8043075]
    """
    if para is None:
        return None

    if wd_binned is None:
        wd_binned = np.linspace(0, 360, 360, endpoint=False)
    para = np.array(para)
    num_sector = para.shape[axis]
    wd_sector = np.linspace(0, 360, num_sector, endpoint=False)

    try:
        interp_index = ['piecewise', 'linear', 'spline'].index(interp_method)
        interp_kind = ['nearest', 'linear', 'cubic'][interp_index]
    except ValueError:
        raise ValueError(
            'interp_method={0} not implemeted yet.'.format(interp_method))
    wd_sector_extended = np.hstack((wd_sector, 360.0))
    para_sector_extended = np.concatenate((para, para.take([0], axis=axis)),
                                          axis=axis)
    f_interp = interp1d(wd_sector_extended, para_sector_extended,
                                    kind=interp_kind, axis=axis)
    para_expanded = f_interp(wd_binned % 360)

    return para_expanded



class WindCondition_Weibull(object):
    """ Wind condition class defines a uniform wind resource cefined by
    sector-wise Weibull distributions with wind rose at a reference height.
    
    Can be applied to flat terrain or offshore sites.
    """
    def __init__(self, Weibull_A_l, Weibull_k_l, freq_l, h_ref, alpha_ref=0.17, 
                 ti=0.06, theta_l=None, interp_method='spline'):
        self.Weibull_A_l = Weibull_A_l
        self.Weibull_k_l = Weibull_k_l
        self.freq_l = freq_l
        self.h_ref = h_ref
        self.alpha_ref = alpha_ref
        self.ti = ti
        
        self.num_l = len(self.Weibull_A_l)
        if theta_l is None:
            theta_l = np.linspace(0, 360, self.num_l, endpoint=False)
        self.theta_l = theta_l

        self.theta_l_refined = np.linspace(0, 360, 361, endpoint=True)
        self.Weibull_A_l_refined = Sector2Subsector(
            self.Weibull_A_l, wd_binned=self.theta_l_refined,
            interp_method=interp_method)

        self.Weibull_k_l_refined = Sector2Subsector(
            self.Weibull_k_l, wd_binned=self.theta_l_refined,
            interp_method=interp_method)
            
        self.freq_l_refined = Sector2Subsector(
            self.freq_l, wd_binned=self.theta_l_refined,
            interp_method=interp_method)
        
        d_theta = self.theta_l_refined[1] - self.theta_l_refined[0]
        self.freq_l_refined[:-1] = self.freq_l_refined[:-1] / np.sum(
            self.freq_l_refined[:-1])
        self.freq_l_refined[-1] = self.freq_l_refined[0]
        self.freq_l_refined = self.freq_l_refined/d_theta

        self.interp_Weibull_A = interp1d(
            self.theta_l_refined, self.Weibull_A_l_refined, kind='linear')
        self.interp_Weibull_k = interp1d(
            self.theta_l_refined, self.Weibull_k_l_refined, kind='linear')
        self.interp_freq = interp1d(
            self.theta_l_refined, self.freq_l_refined, kind='linear')


    def get_pdf(self, ws, wd, h=None):
        if h is not None:
            ws = ws * (self.h_ref / h) ** self.alpha_ref

        wd = np.mod(wd, 360)
        Weibull_A = self.interp_Weibull_A(wd)
        Weibull_k = self.interp_Weibull_k(wd)
        freq = self.interp_freq(wd)
        pdf =(Weibull_k / Weibull_A * (ws/Weibull_A)**(Weibull_k - 1) * 
              np.exp(- (ws/Weibull_A)**Weibull_k) * freq)
        return pdf
    
    @classmethod
    def from_time_series(cls, ws_ts, wd_ts, h_ref, num_l=12, alpha_ref=0.17, 
                 ti=0.06, interp_method='linear'):
        
        wd_ts = np.mod(wd_ts, 360)
        theta_l = np.linspace(0, 360, num_l, endpoint=False)
        sector_width = 360.0 / num_l
        Weibull_A_l = np.zeros(num_l)
        Weibull_k_l = np.zeros(num_l)
        freq_l = np.zeros(num_l)

        num_points = len(ws_ts)

        for i in range(num_l):
            theta_min = theta_l[i] - sector_width / 2
            theta_max = theta_l[i] + sector_width / 2

            if num_l == 0:
                index_l = np.where((wd_ts >= 360 + theta_min) | 
                                   (wd_ts < theta_max))[0]
            else:
                index_l = np.where((wd_ts >= theta_min) & 
                                   (wd_ts < theta_max))[0]
                
            ws_l = ws_ts[index_l]
            wd_l = wd_ts[index_l]

            ws_mean_l = np.mean(ws_l)
            ws_std_l = np.std(ws_l)

            Weibull_k_l[i] = (ws_std_l / ws_mean_l) ** (-1.086) 
            Weibull_A_l[i] = ws_mean_l / (gamma(1 + 1 / Weibull_k_l[i]))
            freq_l[i] = len(ws_l) / num_points

        return cls(Weibull_A_l, Weibull_k_l, freq_l, h_ref, alpha_ref, ti,  
                   theta_l, interp_method)    



if __name__ == '__main__':
    from topdesign import plot_2d_contour, set_font

    ##########################################################################
    # Example with the wind resource at Horns Rev 1 site.
    # Data from the following paper:
    #   Feng, J. and Shen, W.Z., 2015. Modelling wind for wind farm layout
    #   optimization using joint distribution of wind speed and wind direction.
    #   Energies, 8(4), pp.3075-3092. [https://doi.org/10.3390/en8043075]
    
    A = [8.89, 9.27, 8.23, 9.78, 11.64, 11.03, 11.50, 11.92, 11.49, 11.08, 
         11.34, 10.76]
    k = [2.09, 2.13, 2.29, 2.30, 2.67, 2.45, 2.51, 2.40, 2.35, 2.27, 2.24, 
         2.19]
    f = [4.82, 4.06, 3.59, 5.27, 9.12, 6.97, 9.17, 11.84, 12.41, 11.34, 11.70, 
         9.69]
    
    f = [x/100.0 for x in f]
    h_ref = 70

    wind_hornsrev = WindCondition_Weibull(A, k, f, h_ref, 
                                          interp_method='spline')

    ws_range = np.linspace(0, 30, 361)
    wd_range = np.arange(361)
    ws, wd = np.meshgrid(ws_range, wd_range,
                        indexing='ij')

    pdf_hornsrev = wind_hornsrev.get_pdf(ws, wd, h=h_ref)

    set_font(21, 'Time New Roman')

    fig, cbar = plot_2d_contour(pdf_hornsrev.T, extent=[0, 360, 0, 30],
                                xlabel=r'$\theta_{wd}$ [$\degree$]',
                                ylabel=r'$u^\infty$ [m/s]',
                                xticks=np.arange(7)*60,
                                cbar_label=r'$pdf$ [-]')

    fig.savefig('WindCondition_hornsrev.png', bbox_inches='tight')
