import sys
import numpy as np
from topdesign import System



class WFEvalSystem(System):
    """ 
    Reference of the concept:
        Feng, J. and Sørensen, J.N., 2024, June. Towards a general tool chain 
        integration platform for multi-disciplinary analysis and optimization 
        in wind energy. In Journal of Physics: Conference Series (Vol. 2767, 
        No. 8, p. 082014). IOP Publishing. 
        [https://doi.org/10.1088/1742-6596/2767/8/082014]
    """
    def __init__(self, model_dict={}, workflow_graph=None, 
                 input_arg_keys=['layout_x', 'layout_y'], 
                 output_arg_keys=['obj'],
                 wf_model_type='floris',
                 penalty_weighting=1000.0, 
                 parameters_dict=None, name='work_flow', info=None):
        super().__init__(model_dict=model_dict, workflow_graph=workflow_graph,
                         input_arg_keys=input_arg_keys, 
                         output_arg_keys=output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)
        self.wf_model_type = wf_model_type
        self.penalty_weighting = penalty_weighting
        self.current_AEP = None


    def evaluate(self, input_dict, recording=True):
        viol_boundary_dict = self.model_dict['boundary'].evaluate(input_dict)
        viol_spacing_dict = self.model_dict['spacing'].evaluate(input_dict)

        viol_dict = viol_boundary_dict | viol_spacing_dict

        viol_tot_degree = np.sum(viol_dict['viol_boundary']) + np.sum(
            viol_dict['viol_spacing'])
    
        recalculated_AEP = False 

        if viol_tot_degree <= 0 or self.current_AEP is None:
            if self.wf_model_type == 'floris':
                AEP_dict = self.model_dict['wf_model_floris'].evaluate(
                    input_dict)
                recalculated_AEP = True
            elif self.wf_model_type == 'pywake':
                AEP_dict = self.model_dict['wf_model_pywake'].evaluate(
                    input_dict)
                recalculated_AEP = True
            else:
                raise NotImplementedError
            
            self.current_AEP = AEP_dict['AEP']
        else:
            AEP_dict = {'AEP': self.current_AEP + 0.0}

        output_dict = {'obj': self.cal_obj(AEP_dict['AEP'], viol_tot_degree),
                       'recalculated_AEP': recalculated_AEP}
        output_dict = output_dict | viol_dict | AEP_dict

        if recording:
             self.record_current_run(input_dict, output_dict)
        
        return output_dict


    def cal_obj(self, AEP, viol_tot_degree):
        return -AEP + self.penalty_weighting * viol_tot_degree

        



