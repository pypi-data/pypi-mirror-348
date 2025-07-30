from protocols.generateprotocol import GenerateProtocol
from operations.music.musicoperationutils import MusicOperationUtils
import time

class MusicOperation():
    def __init__(self, number, group_id, robot_status, start_check, write):
        self._GenerateProtocolInstance = GenerateProtocol(number, group_id)
        self._robot_status = robot_status
        self._start_check_copy = start_check
        self._write_copy = write

    ### robot_status 얻기
    def _get_robot_status(self, group_id, status, variable):
        return eval("self._robot_status[{}].{}.{}".format(group_id, status, variable))

    ### robot_status 설정
    def _set_robot_status(self, group_id, status, variable, value):
        exec("self._robot_status[{}].{}.{} = {}".format(group_id, status, variable, value))

    ### music 재생
    def play_music(self, cube_ID, note_list, tempo_list, rest_list=None, metronome=100, group_id=None):
        group_id = MusicOperationUtils.proc_group_id(self._GenerateProtocolInstance._group_id, group_id)
        ### start 체크
        self._start_check_copy()
        ### 연결 개수
        connection_number = self._robot_status[group_id].controller_status.connection_number
        ### cube ID 처리
        cube_ID = MusicOperationUtils().process_cube_ID(cube_ID, connection_number)
        # note_list, tempo_list list화 처리
        if type(note_list) != list:
            note_list = [note_list]
        if type(tempo_list) != list:
            tempo_list = [tempo_list]
        ### rest 처리
        if rest_list == None:
            rest_list = [0]*len(note_list)
        elif type(rest_list) != list:
            rest_list = [rest_list]
        ### list 길이 동일성 체크
        MusicOperationUtils().check_list_len_eq(note_list, tempo_list, rest_list)
        ### note_list 체크 & 변환
        note_list_conv = []
        for music_key in note_list:
            MusicOperationUtils().check_music_map(music_key)
            note_list_conv.append(MusicOperationUtils().get_music_map()[music_key])
        ### tempo_list 체크 & 변환
        tempo_list_conv = []
        for tempo_key in tempo_list:
            MusicOperationUtils().check_tempo(metronome, tempo_key)
            tempo_list_conv.append(MusicOperationUtils().get_tempo_map()[metronome][tempo_key])
        ### rest 체크 & 변환
        rest_list_conv = []
        for rest_key in rest_list:
            MusicOperationUtils().check_rest(rest_key)
            rest_list_conv.append(MusicOperationUtils().get_rest(rest_key))
        ### 바이트 쓰기
        sending_bytes = self._GenerateProtocolInstance.SetMusicNotesInAction_SetMusicNotes_bytes(cube_ID, note_list_conv, tempo_list_conv, rest_list_conv)
        self._write_copy(sending_bytes) 
        ### sleep
        time.sleep(0.2)

    