# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 10:24:15 2024

@author: jufen
"""

##############################################################################
# Make sure you have py_wake and floris (v4.x) installed

import numpy as np
import matplotlib.pyplot as plt
from py_wake.site import UniformWeibullSite
from py_wake.site.shear import PowerShear
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.literature.gaussian_models import Bastankhah_PorteAgel_2014
from floris import WindRose, FlorisModel
from floris.turbine_library import TurbineInterface
import pandas as pd
import time

import os
import shutil

from topdesign.wind_farm import WFModel_Floris, WFModel_PyWake, WFEvalSystem
from topdesign.wind_farm import CircularBoundary, MinimalSpacing
from topdesign.optimizer import RandomSearch
from topdesign import plot_power_ct_curve, \
    save_PRNG_state_in_pickle, set_PRNG_state_in_pickle




def plot_layout(x, y, wt_pywake, aep_per_turbine, aep_tot,
                x_boundary=None, y_boundary=None, dpi=300):
    
    fig, ax = plt.subplots(dpi=dpi)
    ax.axis("equal")
    wt_pywake.plot(x, y, ax=ax)
    c = ax.scatter(x, y, c=aep_per_turbine)
    if x_boundary is not None:
        plt.plot(x_boundary, y_boundary, 'r--')

    plt.colorbar(c, label="AEP [GWh]")
    plt.title(f"Total AEP: {aep_tot:.2f} GWh")
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    
    return fig


if __name__ == '__main__':
    ###########################################################################
    # Handle pseudo random number generator state
    
    # set True if want to reproduce and 'PRNG_state.pkl' is there,
    # otherwise set False
    use_save_PRNG_state = True 

    if use_save_PRNG_state:
        set_PRNG_state_in_pickle('PRNG_state.pkl')
    else:
        save_PRNG_state_in_pickle(save_path='./', 
                                  file_name='PRNG_state.pkl')

    ##########################################################################
    # Wind condition based on Horns Rev 1 data
    Weibull_A = np.array([8.89, 9.27, 8.23, 9.78, 11.64, 11.03, 
                        11.50, 11.92, 11.49, 11.08, 11.34, 10.76])
    
    Weibull_k = np.array([2.09, 2.13, 2.29, 2.30, 2.67, 2.45,
                        2.51, 2.40, 2.35, 2.27, 2.24, 2.19])

    freq = np.array([4.82, 4.06, 3.59, 5.27, 9.12, 6.97, 
                    9.17, 11.84, 12.41, 11.34, 11.70, 9.69])/100
    
    ti = 0.1
    alpha = 0.12
    h_ref = 62 

    h_hub = 150.0

    # upscale Weibull_A to the hub height level
    Weibull_A = Weibull_A * (h_hub/h_ref)**alpha

    #specifying the necessary parameters for the UniformWeibullSite object
    site = UniformWeibullSite(p_wd = freq,      # sector frequencies
                            a = Weibull_A,    # Weibull scale parameter
                            k = Weibull_k,    # Weibull shape parameter
                            ti = ti,          # turbulence intensity, optional
                            shear=PowerShear(h_ref=h_hub, alpha=alpha))

    ws = np.arange(30) * 1.0
    wd = np.arange(360) * 1.0

    P_ilk = site.local_wind(x=[0], y=[0], h=h_hub, wd=wd, ws=ws)['P_ilk']

    freq_list = []

    for k in range(len(ws)):
        for l in range(len(wd)):
            freq_list.append([ws[k], wd[l], P_ilk[0, l, k]])

    # make folder for outputs
    if not os.path.isdir('outputs'):
        os.mkdir('outputs')
            
    df = pd.DataFrame(data = freq_list, columns=['ws', 'wd', 'freq_val'])
    df.to_csv('outputs/wind_rose_horns_rev.csv', index=False)

    # Read in the wind rose using the class
    wind_rose = WindRose.read_csv_long(
        "outputs/wind_rose_horns_rev.csv", wd_col="wd", ws_col="ws", 
        freq_col="freq_val", ti_col_or_value=ti)

    # Show the wind rose
    fig_wind = wind_rose.plot(wd_step=15)
    plt.savefig('outputs/wind_rose.png', dpi=300)
    plt.close()


    # ##############################################################################
    # # Wind turbine object of IEA 15MW reference turbine
    wt_floris = TurbineInterface.from_library("internal", "iea_15MW.yaml")
    D = wt_floris.turbine.rotor_diameter

    power_range = wt_floris.power_curve(ws)[1]
    Ct_range = wt_floris.thrust_coefficient_curve(ws)[1]

    wt_pywake = WindTurbine(name='iea-15MW',
                            diameter=D,
                            hub_height=h_hub,
                            powerCtFunction=PowerCtTabular(
                                ws, power_range, 'MW', Ct_range))

    wt_rated_power = 15 # 15 MW

    fig_wt = plot_power_ct_curve(ws, power_range, Ct_range, 
                                 title='IEA 15MW reference turbine')
    plt.savefig('outputs/wind_turbine.png', dpi=300)
    plt.close(fig_wt)


    ###########################################################################
    # Wind farm models with PyWake and Floris
    wf_obj_pywake = Bastankhah_PorteAgel_2014(site, wt_pywake, k=0.0324555)

    parameters_dict = {'wd': wd, 'ws': ws}

    wf_model_pywake = WFModel_PyWake(wf_obj=wf_obj_pywake,
                                    parameters_dict=parameters_dict)

    # Load the FLORIS object
    wf_obj_floris = FlorisModel("inputs/gch.yaml")
    wf_obj_floris.set(wind_data=wind_rose)

    wf_model_floris = WFModel_Floris(wf_obj=wf_obj_floris)

    
    ###########################################################################
    # Initial layout of 9 wts
    layout_x = np.array(
        [0.0, 5, 10, 0.0, 5, 10, 0.0, 5, 10]) * D *1.5
    layout_y = np.array(
            [0.0, 0.0, 0.0, 5.0, 5.0, 5.0, 10.0, 10.0, 10.0]) * D *1.5

    input_dict = {'layout_x': layout_x,
                  'layout_y': layout_y}


    ###########################################################################
    # Define constraints
    x_cen = layout_x[4]
    y_cen = layout_y[4]
    radius = np.sqrt(7.5**2 + 7.5**2) * D
    wf_boundary = CircularBoundary(x_cen, y_cen, radius)

    mini_spacing = 4 * D
    wf_spacing = MinimalSpacing(mini_spacing)


    ###########################################################################
    # Define wind farm evaluation system
    wf_model_type = 'pywake'

    wf_eval_system = WFEvalSystem(
        model_dict={'boundary': wf_boundary,
                    'spacing': wf_spacing,
                    'wf_model_floris': wf_model_floris,
                    'wf_model_pywake': wf_model_pywake},
        wf_model_type=wf_model_type)
    
    wf_eval_system_floris = WFEvalSystem(
        model_dict={'boundary': wf_boundary,
                    'spacing': wf_spacing,
                    'wf_model_floris': wf_model_floris,
                    'wf_model_pywake': wf_model_pywake},
        wf_model_type='floris')


    ###########################################################################
    # Define optimization problem

    # function to parse design vector to x and y cooridnates
    def parse_design_vector(x):
        num_wt = len(x) // 2
        x_i = x[:num_wt]
        y_i = x[num_wt:]
        return x_i, y_i
            
    # objective function
    def fun_obj(x):
        x_i, y_i = parse_design_vector(x)
        input_dict = {'layout_x': x_i,
                'layout_y': y_i}
        output_dict = wf_eval_system.evaluate(input_dict)
        return output_dict['obj']
    
    # objective function with floris
    def fun_obj_floris(x):
        x_i, y_i = parse_design_vector(x)
        input_dict = {'layout_x': x_i,
                'layout_y': y_i}
        output_dict = wf_eval_system_floris.evaluate(input_dict)
        return output_dict['obj']

    # lower/upper bounds based on the circular boundary
    lower_bounds = np.array([x_cen - radius, y_cen - radius])
    upper_bounds = np.array([x_cen + radius, y_cen + radius])

    # Define optimization problem
    rs_opt = RandomSearch(fun_obj=fun_obj, lower_bounds=lower_bounds, 
                          upper_bounds=upper_bounds, fun_constr=None,
                          num_dim=2, save_path='outputs')
    
    
    
    #######################################################################
    # run optimization

    num_wt = len(layout_x)
    num_iter = 2000
    max_move_step = 6000.0
    num_runs = 3

    for i_run in range(num_runs):
        tic = time.time()

        save_path = f'outputs/{num_wt}wt_{num_iter}iter_run{i_run}_RS'

        rs_opt.make_save_path(save_path)

        res = rs_opt.rs_run(x0=np.hstack((layout_x, layout_y)), 
                            num_iter=num_iter,
                            max_move_step=max_move_step, disp_every_step=True)
        
        toc = time.time()

        cpu_time_RS = toc-tic

        print('Optimization took: {:.2f}s'.format(cpu_time_RS))

        cf = -res[1]/(num_wt*15*8760/1000)
        print(res[1])
        print(f'capacity factor = {cf*100:.2f} %')
        print(wf_eval_system.model_dict['wf_model_floris'].num_eval)
        print(wf_eval_system.model_dict['wf_model_pywake'].num_eval)
        num_AEP_calculations = wf_eval_system.model_dict[
            'wf_model_pywake'].num_eval + 0
        
        ##############################################################################
        # Post-processing

        x_opt = res[0][:num_wt]
        y_opt = res[0][num_wt:]

        evol_hist = np.vstack(res[-1])

        last_row = evol_hist[-1, :]
        
        if last_row[0] < num_iter-1:
            last_row[0] = num_iter - 1
            evol_hist = np.vstack((evol_hist, last_row))

        fig = plt.figure(dpi=300)
        plt.plot(evol_hist[:, 0], -evol_hist[:, -1])
        plt.xlabel('Iteration [-]')
        plt.ylabel('AEP [GWh]')
        plt.title('Evolutionary history of optimization\n')
        plt.tight_layout()
        plt.savefig(os.path.join(rs_opt.save_path,'evolution_history.png'))
        plt.close(fig)

        # Get boundary points
        x_boundary, y_boundary = wf_boundary.generate_boundary_points()

        # Plot out original layout
        sim_res = wf_obj_pywake(layout_x, layout_y)
        aep = sim_res.aep(normalize_probabilities=False)
        aep_per_turbine = aep.sum(["wd", "ws"])
        aep_init = np.sum(aep_per_turbine)

        fig_init = plot_layout(layout_x, layout_y, wt_pywake, aep_per_turbine,
                               aep_init, x_boundary=x_boundary, 
                               y_boundary=y_boundary)
        plt.savefig(os.path.join(rs_opt.save_path, 'original_layout.png'))
        plt.close(fig_init)

        # Plot out optimized layout
        sim_res = wf_obj_pywake(x_opt, y_opt)
        aep = sim_res.aep(normalize_probabilities=False)
        aep_per_turbine = aep.sum(["wd", "ws"])
        aep_opt = np.sum(aep_per_turbine)

        fig_RS = plot_layout(x_opt, y_opt, wt_pywake, aep_per_turbine,
                             aep_opt, x_boundary=x_boundary, 
                             y_boundary=y_boundary)
        plt.savefig(os.path.join(rs_opt.save_path, 'optimized_layout.png'))
        plt.close(fig_RS)

        # Recaculating with floris model
        evol_hist_recalculated = evol_hist + 0.0

        for i in range(len(evol_hist_recalculated[:, 0])):
            evol_hist_recalculated[i, -1] = fun_obj_floris(
                evol_hist_recalculated[i, 1:-1])

        # Plot out evolutionary histories
        fig = plt.figure(dpi=300)
        plt.plot(evol_hist[:, 0], -evol_hist[:, -1],
                 evol_hist_recalculated[:, 0], -evol_hist_recalculated[:, -1])
        plt.legend(['PyWake', 'FLORIS'])
        plt.xlabel('Iteration [-]')
        plt.ylabel('AEP [GWh]')
        plt.title('Evolutionary history of optimization\n')
        plt.tight_layout()
        plt.savefig(os.path.join(rs_opt.save_path,'evolution_history_both.png'))
        plt.close(fig)


        # Summary text
        full_aep = wt_rated_power * num_wt * 8760 / 1000

        summary_str = []
        summary_str.append('Summary of results\n')

        summary_str.append(f'i_run = {i_run}')
        summary_str.append(f'cpu_time = {cpu_time_RS:.4f} s')
        summary_str.append(f'save_path: {save_path}')

        summary_str.append(f'num_wt = {num_wt}')
        summary_str.append(f'num_iter = {num_iter}')
        summary_str.append(f'num_AEP_calculations = {num_AEP_calculations}')
        summary_str.append(f'max_move_step = {max_move_step}\n')
        
        # %% Calculate ideal AEP (without wake loss)

        xy_single_turbine = np.array([layout_x[0], layout_y[0]])

        summary_str.append('\n------------PyWake------------------')
        aep_single = - fun_obj(xy_single_turbine)
        aep_ideal = aep_single * num_wt 

        wake_loss_init = (1 - aep_init/aep_ideal) * 100
        wake_loss_opt = (1 - aep_opt/aep_ideal) * 100
        imp_pct = (aep_opt/aep_init - 1) * 100

        summary_str.append(f'AEP_gross = {aep_ideal:.4f} GWh')
        summary_str.append(f'AEP_initi = {aep_init:.4f} GWh, CF = {aep_init/full_aep*100:.2f} %')
        summary_str.append(f'AEP_optim = {aep_opt:.4f} GWh, CF = {aep_opt/full_aep*100:.2f} %')
        summary_str.append(f'wake_loss_initi = {wake_loss_init:.4f} %')
        summary_str.append(f'wake_loss_optim = {wake_loss_opt:.4f} %')
        summary_str.append(f'AEP increase percentage = {imp_pct:.4f} %')


        summary_str.append('\n------------Floris------------------')
        aep_single = - fun_obj_floris(xy_single_turbine)
        aep_ideal = aep_single * num_wt 

        aep_init = -evol_hist_recalculated[0, -1]
        aep_opt = -evol_hist_recalculated[-1, -1]

        wake_loss_init = (1 - aep_init/aep_ideal) * 100
        wake_loss_opt = (1 - aep_opt/aep_ideal) * 100
        imp_pct = (aep_opt/aep_init - 1) * 100

        summary_str.append(f'AEP_gross = {aep_ideal:.4f} GWh')
        summary_str.append(f'AEP_initi = {aep_init:.4f} GWh, CF = {aep_init/full_aep*100:.2f} %')
        summary_str.append(f'AEP_optim = {aep_opt:.4f} GWh, CF = {aep_opt/full_aep*100:.2f} %')
        summary_str.append(f'wake_loss_initi = {wake_loss_init:.4f} %')
        summary_str.append(f'wake_loss_optim = {wake_loss_opt:.4f} %')
        summary_str.append(f'AEP increase percentage = {imp_pct:.4f} %')


        print('\n'.join(summary_str))

        with open(os.path.join(rs_opt.save_path, 'results_summary.txt'), 'w') as f:
            f.write('\n'.join(summary_str))
        
        # copy the current script to the result saving path
        shutil.copy(__file__, os.path.join(rs_opt.save_path, 
                                           'main_script_for_this_run.py')) 