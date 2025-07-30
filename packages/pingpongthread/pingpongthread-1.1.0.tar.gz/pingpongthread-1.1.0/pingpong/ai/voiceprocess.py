import uuid
import os
import gtts
import playsound
import pyaudio
import speech_recognition
import pingpong.ai.Cp949ToUniTable as Cp949ToUniTable

class VoiceProcess():
    def __init__(self):
        pass

    # ValueError("Unable to find token seed!") 오류 해결해야 함.
    @staticmethod
    def tts_ko(text, is_print=False) -> None:
        tts = gtts.gTTS(text=text, lang='ko')
        name = str(uuid.uuid1()) + ".mp3"
        with open(name, 'wb+') as f:
            tts.write_to_fp(f)
        playsound.playsound(name)
        os.remove(name)
        if is_print:
            print(text)
 
    # https://kcal2845.tistory.com/34
    # https://github.com/curioustorvald/cp-949-to-utf-8
    # MIT License
    @staticmethod
    def get_audio_list() -> list:
        p = pyaudio.PyAudio()
        try:
            audio_list = []
            for i in range(p.get_device_count()):
                name = p.get_device_info_by_index(i).get('name')
                i = 0
                device = ""
                while True:
                    if(i == len(name)): 
                        break
                    if(Cp949ToUniTable.uni_conv_table[ord(name[i])] == 'LEAD'):
                        device += chr(Cp949ToUniTable.uni_conv_table[ord(name[i])*0x100+ord(name[i+1])])
                        i+=1
                    else:
                        device += chr(Cp949ToUniTable.uni_conv_table[ord(name[i])])
                    i+=1
                audio_list.append(device)
        except KeyError:
            audio_list = []
            for i in range(p.get_device_count()):
                name = p.get_device_info_by_index(i).get('name')
                audio_list.append(name)
        except Exception as error:
            raise error
        return audio_list

    @staticmethod
    def voice_recognize_ko(audio_input_index=0) -> str:
        r = speech_recognition.Recognizer()
        mic = speech_recognition.Microphone(device_index=audio_input_index)
        audio = None
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            result = r.recognize_google(audio, language='ko-KR')
        except speech_recognition.UnknownValueError:
            result = "Voice recognition failed."
        except Exception as error:
            raise error
        return result
