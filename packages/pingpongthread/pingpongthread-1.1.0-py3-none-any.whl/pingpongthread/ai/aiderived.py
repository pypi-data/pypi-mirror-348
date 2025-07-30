# numpy, tensorflow, cv2 

from ai.voiceprocess import VoiceProcess
from ai.classification import Classification
from ai.getwebcam import GetWebcam

class AiDerived(Classification, GetWebcam, VoiceProcess):
    def __init__(self, tensorflow_no_warnings=True):
        Classification.__init__(self, tensorflow_no_warnings)
        GetWebcam.__init__(self)
        VoiceProcess.__init__(self)
