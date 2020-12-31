
from PYME.recipes.base import register_module, OutputModule
from PYME.recipes.traits import Input, CStr, Float, Int
import requests
import json
import numpy as np

class QueueMultiwellTweet(OutputModule):
    input_positions = Input('input')
    action_server_url = CStr('http://127.0.0.1:9393')
    timeout = Float(np.finfo(float).max)
    max_duration = Float(np.finfo(float).max)
    nice = Int(100)
    def save(self, namespace, context={}):
        """
        Parameters
        ----------
        namespace : dict
            The recipe namespace
        context : dict
            Information about the source file to allow pattern substitution to 
            generate the output name. At least 'basedir' (which is the fully 
            resolved directory name in which the input file resides) and 
            'file_stub' (which is the filename without any extension) should be 
            resolved.
        """
        inp = self.input_positions
        dest = self.action_server_url + '/queue_action'
        session = requests.Session()
        args = {
            'function_name': 'tweeter.tweet_slide', 
            'args': {
                'acquisition_info': {
                    'n_series': len(inp['x'])
                }
            }, 
            'timeout': self.timeout, 'nice': self.nice, 
            'max_duration': self.max_duration}
        session.post(dest, data=json.dumps(args), 
                        headers={'Content-Type': 'application/json'})
