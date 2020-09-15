import mido

file = mido.MidiFile('../midi_data/test_midi.mid')
#file = mido.MidiFile('../midi_data/lo_hi_test.mid')

for i, track in enumerate(file.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

print(file.length)