
from PYME.Acquire.ui.tile_panel import MultiwellProtocolQueuePanel
from pyme_twitter.acquire import tweeter
from PYME.IO.MetaDataHandler import DictMDHandler

class TweetingMultiwellProtocolQueuePanel(MultiwellProtocolQueuePanel, 
                                          tweeter.SimpleWellTweeter):
    def __init__(self, parent, scope, gen_sample_mdh, credential_filepath=None,
                 safety=True):
        MultiwellProtocolQueuePanel.__init__(self, parent, scope)
        tweeter.SimpleWellTweeter.__init__(self, credential_filepath, safety)

    def OnQueue(self, wx_event=None):
        n_x = int(self.n_x.GetValue())
        n_y = int(self.n_y.GetValue())
        n_total = n_x * n_y
        
        MultiwellProtocolQueuePanel.OnQueue(self, wx_event)

        slide = self._gen_sample_mdh(DictMDHandler())['Sample.SlideRef']
        
        self.slide_info[slide] = {
                'n_wells': n_total,
                'n_series': [],
                # 'protocol': [acquisition_info['protocol']],
                # 'max_frames': [acquisition_info['max_frames']]
            }