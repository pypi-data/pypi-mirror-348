###############################################################################
# To run this example, you need to have the following library installed:
# 1. matlabengine (https://pypi.org/project/matlabengine/)
#    [check here for more details: 
#          https://www.mathworks.com/help/matlab/matlab-engine-for-python.html]
#
# 2. juliacall (https://pypi.org/project/juliacall/)
#    [check here for more details: 
#          https://juliapy.github.io/PythonCall.jl/stable/juliacall/]

###############################################################################
# This example solves test problem HS15 from the Hock & Schittkowski collection
#
#   min   100 (x2 - x1^2)^2 + (1 - x1)^2
#   s.t.  x1 x2 >= 1
#         x1 + x2^2 >= 0
#         x1 <= 0.5
#
# assuming the objective function is an executable based on Fortran code,
# the 1st constraint is a Julia function and the 2nd constraint is a matlab 
# function and the 3rd constraint is included in the upper bound of x1.
#
# Ref.: W. Hock and K. Schittkowski, Test Examples for Nonlinear Programming
# Codes.  Lecture Notes in Economics and Mathematical Systems, v. 187,
# Springer-Verlag, New York, 1981, p. 38.



import numpy as np
from topdesign import ModelMatlab, ModelJulia, ModelExecutableStdIO
from topdesign.optimizer import RandomSearch, PSO, RealCodedGA



if __name__ == '__main__':


    ###########################################################################
    # 1. objective function model that wraps the executable obj_func.exe stored
    #    in sub_models folder. The original code is written in Fortran.
    obj_func_model = ModelExecutableStdIO(
        executable='sub_models/obj_func.exe',
        input_arg_keys=['x1', 'x2'], 
        output_arg_keys=['obj'])


    ###########################################################################
    # 2. 1st constraint function model that wraps julia function 
    #    (constraint_func1) in 'sub_models/constraint_func1.jl'.
    constraint_func1_model = ModelJulia(
        Julia_func_name='constraint_func1', 
        Julia_script='sub_models/constraint_func1.jl',
        JuliaMain=None,
        input_arg_keys=['x1', 'x2'], 
        output_arg_keys=['constr1'])


    ###########################################################################
    # 3. 2nd constraint function model that wraps the matlab function 
    #    (constraint_func2) in 'sub_models/constraint_func2.m'.
    constraint_func2_model = ModelMatlab(
        matlab_func_name='constraint_func2', 
        matlab_func_folder='sub_models',
        eng=None,
        input_arg_keys=['x1', 'x2'], 
        output_arg_keys=['constr2'])

    input_dict = {'x1': 4.0, 'x2': 5.0}

    print(obj_func_model.evaluate(input_dict))

    print(constraint_func1_model.evaluate(input_dict))

    print(constraint_func2_model.evaluate(input_dict))


    ###########################################################################
    # 4. Optimization using Random Search, PSO, and Real-coded GA.

    def func_obj(x):
        """ Function to calcuate the objective value."""
        input_dict = {'x1': x[0], 'x2': x[1]}
        return obj_func_model.evaluate(input_dict)['obj']


    def func_constr(x):
        """ Function to calcuate the constraint violation degree. """
        input_dict = {'x1': x[0], 'x2': x[1]}
        constr1 = constraint_func1_model.evaluate(input_dict)['constr1']
        constr2 = constraint_func2_model.evaluate(input_dict)['constr2']
        constr_violation = max(0, -constr1) + max(0, -constr2)
        return constr_violation


    def func_obj_combined(x):
        """ Combined objective function and constraint violation function with
        a penalty method. """
        obj = func_obj(x)
        constr_violation = func_constr(x)
        return obj + 1e3 * constr_violation

    # Define the lower and upper bounds of the design variables.
    lower_bounds = np.array([-5, -5])
    upper_bounds = np.array([0.5, 5])


    ###########################################################################
    # Random search optimization.
    rs_opt = RandomSearch(fun_obj=func_obj,
                          lower_bounds=lower_bounds,
                          upper_bounds=upper_bounds,
                          fun_constr=func_constr,
                          num_dim=2,
                          save_path='./RS_results')

    # Initial guess of the design variables.
    x0 = np.array([-2.0, 1.0])

    res = rs_opt.rs_run(x0=x0, max_move_step=5, num_iter=1000)
    print('Optimization using Random Search is done.')
    print(f'Optimized result: x1={res[0][0]}, x2={res[0][1]}, obj={res[1]}')
    print('-----------------------------------------------------------\n\n')

    ###########################################################################
    # PSO optimization.
    pso_opt = PSO(obj_fun=func_obj_combined,
                  num_design_variables=2,
                  lower_bounds=lower_bounds,
                  upper_bounds=upper_bounds,
                  max_gen=100,
                  save_path='./PSO_results')

    res = pso_opt.pso_run()
    print('Optimization using PSO is done.')
    print(f'Optimized result: x1={res[0][0]}, x2={res[0][1]}, obj={res[1]}')
    print('-----------------------------------------------------------\n\n')

    ###########################################################################
    # Real-coded GA optimization.
    rcga_opt = RealCodedGA(obj_fun=func_obj_combined,
                    num_design_variables=2,
                    lower_bounds=lower_bounds,
                    upper_bounds=upper_bounds,
                    max_gen=100,
                    save_path='./RCGA_results')

    res = rcga_opt.ga_run()
    print('Optimization using RCGA is done.')
    print(f'Optimized result: x1={res[0][0]}, x2={res[0][1]}, obj={res[1]}')
    print('-----------------------------------------------------------\n\n')