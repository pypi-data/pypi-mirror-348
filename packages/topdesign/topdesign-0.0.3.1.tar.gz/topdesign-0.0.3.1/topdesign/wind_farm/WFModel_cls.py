# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:28:19 2024

@author: Ju Feng (jufen@dtu.dk)
"""

import numpy as np
from topdesign import Model
from topdesign import rotate_coordinates



class WFModel(Model):
    def __init__(self, wf_obj,
                 input_arg_keys=['layout_x', 'layout_y'], 
                 output_arg_keys=['AEP'], 
                 parameters_dict=None, name='wf_model', info=None):
        super().__init__(func=None, input_arg_keys=input_arg_keys, 
                         output_arg_keys=output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
        self.wf_obj = wf_obj



class WFModel_Floris(WFModel):
    """ Wind farm model using the FLORIS model (work with floris 4, 
    floris v4.2.2 has been used in the example run).
    """
    def __init__(self, wf_obj,
                 input_arg_keys=['layout_x', 'layout_y'], 
                 output_arg_keys=['AEP'], 
                 parameters_dict=None, name='wf_model_floris', info=None):
        super().__init__(wf_obj, input_arg_keys, output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
    
        
    def func(self, input_dict):
        layout_x = input_dict['layout_x']
        layout_y = input_dict['layout_y']

        self.wf_obj.set(
            layout_x = layout_x,
            layout_y = layout_y
        )

        # Compute the AEP (GWh) using the default settings
        self.wf_obj.run()
        aep = self.wf_obj.get_farm_AEP() / 1.0e9
        
        output_dict = {'AEP': aep}
        return output_dict



class WFModel_PyWake(WFModel):
    """ Wind farm model using the PyWake model.
    """
    def __init__(self, wf_obj,
                 input_arg_keys=['layout_x', 'layout_y'], 
                 output_arg_keys=['AEP'], 
                 parameters_dict=None, name='wf_model_pywake', info=None):
        super().__init__(wf_obj, input_arg_keys, output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
    
        
    def func(self, input_dict):
        layout_x = input_dict['layout_x']
        layout_y = input_dict['layout_y']

        if self.parameters_dict is None:
            sim_res = self.wf_obj(x=np.array(layout_x), 
                                  y=np.array(layout_y))     # wind turbine positions
        
        else:
            wd = self.parameters_dict['wd']
            ws = self.parameters_dict['ws']
            sim_res = self.wf_obj(x=np.array(layout_x), 
                                  y=np.array(layout_y),
                                  wd=wd, ws=ws) 

        # Compute the AEP (GWh) using the default settings
        aep = sim_res.aep(normalize_probabilities=False)
        aep_tot = aep.values.sum()
        
        output_dict = {'AEP': aep_tot}
        return output_dict



class RectangularBoundary(Model):
    def __init__(self, x_cen, y_cen, width, height, rotation_in_deg=0.0,
                 input_arg_keys=['layout_x', 'layout_y'], 
                 output_arg_keys=['viol_boundary'], 
                 parameters_dict=None, name='rectangular_boundary', info=None,
                 viol_buffer=1e-3):
        super().__init__(func=None, input_arg_keys=input_arg_keys, 
                         output_arg_keys=output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
        self.x_cen = x_cen
        self.y_cen = y_cen
        self.width = width
        self.height = height
        self.rotation_in_deg = rotation_in_deg
        self.viol_buffer = viol_buffer


    def cal_viol_degree(self, x, y):
        x_list = np.asarray(x).ravel()
        y_list = np.asarray(y).ravel()
        viol_degree = np.zeros_like(x_list) + 0.0

        x_adjusted, y_adjusted = rotate_coordinates(
            x_list - self.x_cen, y_list - self.y_cen, 
            np.deg2rad(self.rotation_in_deg))

        for i in range(len(x_list)):
            x_adj = x_adjusted[i]
            y_adj = y_adjusted[i]

            dist2x = max(0.0, x_adj - self.width/2.0, -self.width/2.0 - x_adj)
            dist2y = max(0.0, y_adj - self.height/2.0, -self.height/2.0 - y_adj)
            viol_degree[i] = np.sqrt(dist2x**2 + dist2y**2)

            # Do not consider the violation if it is within the buffer range
            if viol_degree[i] > 0 and viol_degree[i] <= self.viol_buffer:
                viol_degree[i] = 0.0
        
        if np.isscalar(x):
            return viol_degree[0]
        elif isinstance(x, np.ndarray):
            return viol_degree.reshape(x.shape)
        else:
            return  [viol_degree[i] for i in range(len(x_list))]

    
    def func(self, input_dict):
        x = input_dict['layout_x']
        y = input_dict['layout_y']

        viol_degree = np.sum(self.cal_viol_degree(x, y))

        output_dict = {'viol_boundary': viol_degree}

        return output_dict


    def generate_boundary_points(self):
        x_boundary = np.array([self.x_cen - self.width/2, 
                               self.x_cen + self.width/2, 
                               self.x_cen + self.width/2, 
                               self.x_cen - self.width/2,
                               self.x_cen - self.width/2])
        y_boundary = np.array([self.y_cen - self.height/2, 
                               self.y_cen - self.height/2, 
                               self.y_cen + self.height/2, 
                               self.y_cen + self.height/2,
                               self.y_cen - self.height/2])
        x_boundary_rot, y_boundary_rot = rotate_coordinates(
            x_boundary, y_boundary, 
            -np.deg2rad(self.rotation_in_deg))
        
        return x_boundary_rot, y_boundary_rot

    


class CircularBoundary(Model):
    def __init__(self, x_cen, y_cen, radius,
                 input_arg_keys=['layout_x', 'layout_y'], 
                 output_arg_keys=['viol_boundary'], 
                 parameters_dict=None, name='circular_boundary', info=None,
                 viol_buffer=1e-3):
        super().__init__(func=None, input_arg_keys=input_arg_keys, 
                         output_arg_keys=output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
        self.x_cen = x_cen
        self.y_cen = y_cen
        self.radius = radius
        self.viol_buffer = viol_buffer


    def cal_viol_degree(self, x, y):
        
        x_list = np.asarray(x).ravel()
        y_list = np.asarray(y).ravel()

        dist2cen = np.sqrt((x_list - self.x_cen)**2 + (y_list - self.y_cen)**2)
        viol_degree = np.where(dist2cen - self.viol_buffer > self.radius, 
                               dist2cen - self.radius, 
                               0.0)
        
        if np.isscalar(x):
            return viol_degree[0]
        elif isinstance(x, np.ndarray):
            return viol_degree.reshape(x.shape)
        else:
            return  [viol_degree[i] for i in range(len(x_list))]
    

    def generate_boundary_points(self, num_points=100):
        theta_range = np.linspace(0.0, np.pi*2, num=num_points, endpoint=True)
        x_boundary = self.x_cen + self.radius * np.cos(theta_range)
        y_boundary = self.y_cen + self.radius * np.sin(theta_range)
        return x_boundary, y_boundary
    
    
    def func(self, input_dict):
        x = input_dict['layout_x']
        y = input_dict['layout_y']

        viol_degree = np.sum(self.cal_viol_degree(x, y))

        output_dict = {'viol_boundary': viol_degree}

        return output_dict
    


class MinimalSpacing(Model):
    def __init__(self, minimal_spacing,
                 input_arg_keys=['layout_x', 'layout_y'], 
                 output_arg_keys=['viol_spacing'], 
                 parameters_dict=None, name='circular_boundary', info=None):
        super().__init__(func=None, input_arg_keys=input_arg_keys, 
                         output_arg_keys=output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
        self.minimal_spacing = minimal_spacing

    
    def cal_viol_degree(self, x, y):
        x_list = np.asarray(x).ravel()
        y_list = np.asarray(y).ravel()
        viol_degree = np.zeros_like(x_list) + 0.0

        for i in range(len(x_list)):
            dist2turbines = np.sqrt((x_list[i] - x_list)**2 +
                                    (y_list[i] - y_list)**2)
            
            viol_degree_list = np.where(dist2turbines < self.minimal_spacing,
                         self.minimal_spacing - dist2turbines, 0.0)
            
            viol_degree_list[i] = 0 # distance to itself not considered

            viol_degree[i] = np.sum(viol_degree_list)
        
        if np.isscalar(x):
            return viol_degree[0]
        elif isinstance(x, np.ndarray):
            return viol_degree.reshape(x.shape)
        else:
            return  [viol_degree[i] for i in range(len(x_list))]
        
    
    def func(self, input_dict):
        x = input_dict['layout_x']
        y = input_dict['layout_y']

        viol_degree = np.sum(self.cal_viol_degree(x, y))

        output_dict = {'viol_spacing': viol_degree}

        return output_dict
    


if __name__ == '__main__':

    def square(x):
        y = x**2
        return y
    
    def square_decorated(input_dict):
        x = input_dict['x']
        y = square(x)
        output_dict = {'y': y}
        return output_dict
    
    model_square = Model(func=square_decorated,
                         input_arg_keys=['x'],
                         output_arg_keys=['y'],
                         parameters_dict=None)
    





        
    



