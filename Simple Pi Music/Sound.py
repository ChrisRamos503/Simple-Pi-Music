from pydub import playback as pb
from pydub import AudioSegment
import subprocess as sp
import time
import fluidsynth

class Sound(object):
    """
    Abstract class for Sound Objects (not to be confused SndObj objects)
    """
    def __init__(self,name="", duration=2):
	self.name = name
	self.duration = duration

    """
    Used to play file
    """
    def Play():
	pass

    def ChangeName():
	pass

class WavFile(Sound):
    """
    wrapper class used to play .wav files
    """
    def __init__(self, name, duration):
	super(WavFile, self).__init__(name,duration)
	
	dur = duration * 1000
	Sound = AudioSegment.from_wav(name)
        self.Sound = Sound[:dur]
    """
    Used to play file
    """
    def Play(self):
	pb.play(self.Sound)
	pass

class Mp3File(Sound):
    """
    wrapper class used to play .mp3 files
    """
    def __init__(self, name, duration):
	super(Mp3File, self).__init__(name,duration)

    """
    Used to play file
    """
    def Play(self):
	pb._play_with_ffplay(self)
	pass

class SoundFont2File(Sound):
    """
    wrapper class used to play .sf2 files
    """
    def __init__(self, name, duration, freq = 0, volume = 127):
	super(SoundFont2File, self).__init__(name, duration)
	
	self.freq = freq
	self.volume = volume

	self.fs = fluidsynth.Synth()#samplerate=11025)
	self.fs.start('alsa')

	sfid = self.fs.sfload(name) 		# loading soundfont
	self.fs.program_select(0, sfid, 0, 0)		

    """
    Used to play file
    """
    def Play(self):
	self.fs.noteon(0, self.freq, self.volume)
	time.sleep(self.duration)
	self.fs.noteoff(0, self.freq)
	pass

    """
    used to change frequency
    """
    def ChangeFreq(self, frequency):
	self.freq = frequency

    """
    used to change volume
    """
    def ChangeVolume(self, volume):
	if volume > 127:
	    volume = 127
	elif volume < 0:
	    volume = 0
	else:
	    pass
	self.volume = volume

    def On(self, freq):
	self.fs.noteon(0, freq, self.volume)
	pass

    def Off(self, freq):
	self.fs.noteoff(0, freq)
	pass

class MidiFile(Sound):
    """
    wrapper class used to play .midi files
    """
    def __init__(self, MidiName, SoundFont2):
	super(MidiFile, self).__init__(MidiName,0)

	self.Midi = MidiName
	self.SoundFont2 = SoundFont2	
	pass

    """
    Used to play file
    """
    def Play(self):

	sp.Popen("fluidsynth --no-shell -a alsa " + self.SoundFont2 + " " + self.Midi , shell=True)
	time.sleep(3)
	

