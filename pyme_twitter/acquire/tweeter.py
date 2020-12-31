
import tweepy
import yaml
import os
import time
import numpy as np
import logging
import threading

logger = logging.getLogger(__name__)

class FakeAPI(object):
    def update_status(self, status):
        print('FakeTweet: %s' % status)


class SimpleWellTweeter(object):
    def __init__(self, gen_sample_mdh, credential_filepath=None, safety=True):
        self.safety = safety
        self._gen_sample_mdh = gen_sample_mdh
        self.slide_info = dict()

        # get our keys/tokens
        if credential_filepath is None:
            credential_filepath = os.path.join(os.path.expanduser("~"), 
                                               os.path.join('.PYME, twitter-credentials.yaml'))

        try:
            with open(credential_filepath) as f:
                cred = yaml.safe_load(f)
            # authenticate
            auth = tweepy.OAuthHandler(cred['consumer_key'], cred['consumer_secret'])
            auth.set_access_token(cred['access_token'], cred['access_token_secret'])
            self._t_api = tweepy.API(auth)
        except IOError as e:
            if not safety:
                raise e
            logger.debug('scope tweeter running in debug mode - no tweets will be issued')
            self._t_api = FakeAPI()
        
        
    
    def tweet_slide(self, acquisition_info, sample_info=None):
        if sample_info is None:
            from PYME.IO.MetaDataHandler import DictMDHandler
            mdh = DictMDHandler()
            sample_info = self._gen_sample_mdh(mdh)
        
        slide = sample_info['Sample.SlideRef']
        
        self.slide_info[slide]['n_series'].append(acquisition_info['n_series'])
        # self.slide_info[slide]['protocol'].append(acquisition_info['protocol'])
        # self.slide_info[slide]['max_frames'].append(acquisition_info['max_frames'])
        
        if self.slide_info[slide]['n_wells'] == len(self.slide_info[slide]['n_series']):
            # time to tweet it
            # msg = "{{imager}} imaged {{n_series}} {{protocol}} series across {{n_wells}} wells on slide {{slide}}, made by {{creator}}, {{notes}}"
            msg = "{{imager}} imaged {{n_series}} series across {{n_wells}} wells on slide {{slide}}, made by {{creator}}, {{notes}}"
            info = {
                'imager': sample_info.getOrDefault('AcquiringUser'),
                'n_series': np.sum(self.slide_info[slide]['n_series']),
                'n_wells': self.slide_info[slide]['n_wells'],
                # 'protocol': self.slide_info[slide]['protocol'][0],
                'creator': sample_info.getOrDefault('Sample.Creator'),
                'slide': sample_info.getOrDefault('Sample.SlideRef'),
                'notes': sample_info.getOrDefault('Sample.Notes'),
            }
            for key, value in info.items():
                msg = msg.replace('{{%s}}' % key, str(value))
            
            if not self.safety:
                self._t_api.update_status(msg)
