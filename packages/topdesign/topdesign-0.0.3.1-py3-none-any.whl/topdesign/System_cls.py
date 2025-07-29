from topdesign import Model



class System(Model):
    def __init__(self, model_dict={}, workflow_graph=[['input', 'output']], 
                 input_arg_keys=['x'], output_arg_keys=['y'], 
                 parameters_dict=None, name='work_flow', info=None):
        super().__init__(func=None, input_arg_keys=input_arg_keys, 
                         output_arg_keys=output_arg_keys, 
                         parameters_dict=parameters_dict,
                         name=name, info=info)

        self.model_dict = model_dict
        self.workflow_graph = workflow_graph


    
