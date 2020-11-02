import mido
from collections import deque

class TimeSignature():
    def __init__(self,numerator,denominator):
        self.numerator = numerator
        self.denominator = denominator 

class ScheduleMetaData():
    """
    Object for storing meta data of a note schedule
    """
    key_signature = None
    time_signature = None
    ticks_per_beat = None
    tempo = None
    length = None    

    def __init__(self):
        pass

class Note():
    norm_TPB = 96

    def __init__(self,note,time,velocity):
        self.note = note # integer representation of note
        self.time = time # [time_start, time_stop]
        self.velocity = velocity

    def time_in_seconds(self,TPB,BPM):
        conversion_factor = 60 / (TPB*BPM)
        return [self.time[0]*conversion_factor, self.time[1]*conversion_factor]

    def norm_time(self,TPB):
        conversion_factor = self.norm_TPB / TPB
        time = [t * conversion_factor for t in self.time] 
        return time

    def __lt__(self,other):
        return self.time[0] < other.time[0] 

class NoteSchedule():
    """
    Parses a MIDI file into an object that is easily converted into notes on
    the piano roll.
    """
    schedule_meta_data = ScheduleMetaData()
    note_tracks = []
    channels = {}

    def __init__(self,midi_file_path):
        self.midi_file = mido.MidiFile(midi_file_path)
        self.__scan_meta_data()
        self.__parse_note_tracks()
    
    def __scan_meta_data(self):
        for track in self.midi_file.tracks:
            for msg in track:
                if msg.is_meta:
                    
                    if msg.type == 'time_signature':
                        self.schedule_meta_data.time_signature = TimeSignature(msg.numerator,msg.denominator)
                    
                    elif msg.type == 'set_tempo':
                        self.schedule_meta_data.tempo = msg.tempo

                    elif msg.type == 'key_signature':
                        self.schedule_meta_data.key_signature = msg.key_signature
                    
                    elif msg.type == 'track_name':
                        self.note_tracks.append(track)

        self.schedule_meta_data.length = self.midi_file.length
        self.schedule_meta_data.ticks_per_beat = self.midi_file.ticks_per_beat

    def __parse_note_tracks(self):
        self.channels = {} # Clear channels

        for track in self.note_tracks:
            notes = {}
            time = 0

            for msg in track:
                time += msg.time

                if msg.type == "note_on":
                    #print(msg)
                    
                    if msg.note not in notes:
                        notes[msg.note] = deque()
                    
                    notes[msg.note].append([msg.note, time, msg.velocity])
                
                elif msg.type == "note_off":
                    
                    n, t, v = notes[msg.note].popleft()
                    new_note = Note(n,[t,time],v)
                    
                    if msg.channel in self.channels.keys():
                        self.channels[msg.channel].append(new_note)
                    else:
                        self.channels[msg.channel] = [new_note]
                    
    def get_BPM(self):
        """
        Convert tempo from microseconds per beat to beats per minute
        """
        BPuS_to_BPM = 6*(10**7)
        return round(1 / (self.schedule_meta_data.tempo / BPuS_to_BPM ), 2)

    def set_BPM(self,BPM):
        """
        TODO
        Updates the tempo in the schedule's meta data
        """
        BPuS_to_BPM = 6*(10**7)
        new_tempo = (1 / (BPM / BPuS_to_BPM))

        self.schedule_meta_data.tempo = new_tempo

    def info(self):
        """
        TODO
        Prints meta data and other useful information for debugging etc.
        """
        pass

def main():
    NS = NoteSchedule('../midi_data/test_midi.mid')
    for k,v in NS.channels.items():
        for note in v:
            print(note.time_in_seconds(NS.schedule_meta_data.ticks_per_beat,NS.get_BPM()))

if __name__ == '__main__':
    main()