class MusicOperationUtils():
    ###  정수 체크
    def integer_check(self, number, option=None) -> None:
        if not isinstance(number, int):
            is_integer = False
        else:
            is_integer = True
        if not is_integer:
            if option:
                raise ValueError("Please enter integer number, or \"" + str(option) + "\"!")
            else:
                raise ValueError("Please enter integer number!")
    
    ### 큐브 ID 처리
    def process_cube_ID(self, cube_ID, connection_number):
        if isinstance(cube_ID, str) and cube_ID.lower() == "all":
            cube_ID = 0xFF
        else:
            self.integer_check(cube_ID, "all") # 정수 체크
            cube_ID = int(cube_ID) # 정수로 변환 
            if not (1 <= cube_ID and cube_ID <= 8):
                raise ValueError("Cube ID must be between 1 to 8.")
            elif cube_ID > connection_number:
                raise ValueError("Cube ID must be less than or equal to connection number.")
            cube_ID -= 1 # (1 to 8 -> 0 to 7)
        return cube_ID

    ### key 매핑
    def get_music_map(self):
        pitch_map = {
            "A3": 37,
            "A#3": 38, "Bb3": 38,
            "B3": 39,
            "C4": 40, 
            "C#4": 41, "Db4": 41,
            "D4": 42, 
            "D#4": 43, "Eb4": 43,
            "E4": 44,
            "F4": 45,
            "F#4": 46, "Gb4": 46,
            "G4": 47,
            "G#4": 48, "Ab4": 48,
            "A4": 49,
            "A#4": 50, "Bb4": 50,
            "B4": 51, 
            "C5": 52,
            "C#5": 53, "Db5": 53,
            "D5": 54,
            "D#5": 55, "Eb5": 55,
            "E5": 56,
            "F5": 57,
            "F#5": 58, "Gb5": 58,
            "G5": 59,
            "G#5": 60, "Ab5": 60,
            "A5": 61,
            "A#5": 62, "Bb5": 62,
            "B5": 63,
            "C6": 64
        }
        doremi_map = {
            "Do": 40, "Re": 42, "Mi": 44, "Fa": 45, "Sol": 47, "La": 49, "Ti": 51,
            "do": 40, "re": 42, "mi": 44, "fa": 45, "sol": 47, "la": 49, "ti": 51, 
            "DO": 40, "RE": 42, "MI": 44, "FA": 45, "SOL": 47, "LA": 49, "TI": 51
        }
        pitch_map.update(doremi_map)
        return pitch_map
    
    ### tempo 매핑
    def get_tempo_map(self):
        # metronome: BPM?
        tempo_map = {
            60: {
                "Whole": 200, "whole": 200,
                "Half": 100, "half": 100,
                "Dotted Half": 150, "dotted half": 150,
                "Quarter": 50, "quarter": 50,
                "Dotted Quarter": 75, "dotted quarter": 75,
                "Eighth": 25, "eighth": 25,
                "Sixteenth": 12, "sixteenth": 12
            },
            100: {
                "Whole": 120, "whole": 120,
                "Half": 60, "half": 60,
                "Dotted Half": 90, "dotted half": 90,
                "Quarter": 30, "quarter": 30,
                "Dotted Quarter": 45, "dotted quarter": 45,
                "Eighth": 15, "eighth": 15,
                "Sixteenth": 7, "sixteenth": 7
            },
            150: {
                "Whole": 80, "whole": 80,
                "Half": 40, "half": 40,
                "Dotted Half": 60, "dotted half": 60,
                "Quarter": 20, "quarter": 20,
                "Dotted Quarter": 30, "dotted quarter": 30,
                "Eighth": 10, "eighth": 10,
                "Sixteenth": 5, "sixteenth": 5
            }
        }
        return tempo_map
    
    ### rest 계산 (확실하지는 않음. 실험이 필요.)
    def get_rest(self, sec):
        # min 0.1s, max 4s
        return int(sec*50) 

    ### music key 체크
    def check_music_map(self, music_key):
        # 60, 100, 150
        music_map = self.get_music_map()
        if music_key not in music_map.keys():
            raise ValueError("Not available musical note key.")
    
    ### tempo key 체크
    def check_tempo(self, metronome, tempo):
        tempo_map = self.get_tempo_map()
        if metronome not in tempo_map.keys():
            raise ValueError("Not available metronome tempo.")
        elif tempo not in tempo_map[60].keys():
            raise ValueError("Not available metronome note.")

    ### rest 체크 (확실하지는 않음. 실험이 필요.)
    def check_rest(self, sec):
        if sec < 0 or 4 < sec:
            raise ValueError("Not rest duration.")

    ### list 길이 체크
    def check_list_len_eq(self, *lists):
        if len(lists) == 1:
            return None
        for i in range(1, len(lists)):
            if len(lists[0]) != len(lists[i]):
                raise ValueError("Length of lists are not all the same.")

    @staticmethod
    def proc_group_id(self_group_id, group_id):
        if group_id == None:
            return self_group_id # None or int
        else:
            return group_id # Not None, int
            
            
    