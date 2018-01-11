import sndobj as so
import time
import Sound

# I thought of a cool name for the Music Library
# Pie-clectic
# as pi eclectic
EnvTab =so.EnvTable()
HarmTab =so.HarmTable()

class SoundGen(Sound.Sound):
	"""	
	Basic Sound Generator with activatable modulator (self.mod)
	"""
	def __init__(self, name="", duration=1, Table=so.EnvTable(), freq=440, amp=16000):
		super(SoundGen, self).__init__(name,duration)

		self.mod = so.Oscili(Table, 0, 44)
		self.osc = so.Oscili(Table, freq, amp, self.mod)	
		
		self.output = so.SndRTIO(1)
		self.output.SetOutput(1, self.osc)

		self.Prepare()
	
	"""
	Starts SNDThread or think of it as turning on the SoundGen
	"""
	def Start(self):
	    self.thread.ProcOn()
	    print "Starting"

	"""
	Similar to Start() except it turns off after a certain duration
	"""
	def Play(self):
	    self.thread.ProcOn()
	    time.sleep(self.duration)
	    self.thread.ProcOff()
	
	def PlayTime(self, freq=0, duration=1):
	    self.ChangeOscFreq(freq)
	    time.sleep(.02)
	    self.thread.ProcOn()
	    time.sleep(duration)
	    self.thread.ProcOff()

	"""
	Used to turn off SoundGen
	"""
	def Off(self):
	    self.thread.ProcOff()

	"""
	Prepares SoundGen
	"""
	def Prepare(self):
	    self.thread = so.SndThread()
	    self.thread.AddObj(self.mod)
	    self.thread.AddObj(self.osc)
	    self.thread.AddObj(self.output,  so.SND_OUTPUT)

	"""
	Changes Osciliator Table
	"""
	def ChangeOscTable(self, Table):
	    self.osc.SetTable(Table)

	"""
	Changes Modulator Table
	"""
	def ChangeModTable(self, Table):
	    self.mod.SetTable(Table)

	"""
	Changes Osciliator frequency
	"""
	# remember to look at this again
	# check and see if python has overloading
	def ChangeOscFreq(self,freq, Oscili=0):
	
	    if(Oscili == 0):
		    self.osc.SetFreq(freq)	
		    #self.thread_set = False
		   # print "no oscili"
	    else:
		    self.osc.SetFreq(freq)
		   # print "inserted oscili object into chain"	
	    #self.thread_set = False

	"""
	Changes Modulator frequency
	"""
	def ChangeModFreq(self,freq):
	    self.mod.SetFreq(freq)	

	"""
	Changes Osciliator amperage
	"""
	def ChangeOscAmp(self,amp):
	    self.osc.SetAmp(amp)	

	"""
	Changes Modulator amperage
	"""
	def ChangeModAmp(self,amp):
	    self.mod.SetAmp(amp)	

	"""
	Changes modulator Table, frequency, and amperage
	"""
	def ChangeOsc(self, Table, freq, amp):
	    self.ChangeOscTable(Table)
	    self.ChangeOscAmp(amp)
	    self.ChangeOscFreq(freq) 	

	"""
	Changes Osciliator Table, frequency, and amperage
	"""
	def ChangeMod(self, Table, freq, amp):
	    self.ChangeModTable(Table)
	    self.ChangeModAmp(amp)
	    self.ChangeModFreq(freq) 	

class Chord(Sound.Sound):
    def __init__(self, name="", duration=1, FreqList=[]):
	super(Chord, self).__init__(name , duration)

	if len(FreqList) > ChordManager.GetChordLimit():
	    self.FreqList = FreqList[0: ChordManager.GetChordLimit()]
	    print "number of notes has exceeded note limit", ChordManager.GetChordLimit()
	else:
	    self.FreqList = FreqList
	
    def AddFreq(self, freq):
	if(len(FreqList) < ChordManager.GetChordLimit()):
	    self.FreqList.append(freq)
	else:
	    print "you have reached the limit of frequencies you may have for a chord"	
	pass

    def SubtractFreq(self, freq):
	self.FreqList.remove(freq)
	# need to put value error exception
	pass

    def PrintFreq(self):
	for freq in self.FreqList:
	    print "index =", self.FreqList.index(freq), ", frequency =", freq 
    
    def Play(self):
	#ChordManager.ChangeFreqs(self.FreqList)
	ChordManager.Play(self.FreqList, self.duration)

class ChordManager():
    StringList = [ SoundGen("string1", 1, EnvTab, 440, 16000 )
    ,SoundGen("string2", 1, EnvTab, 440, 16000 ) ,SoundGen("string3", 1, EnvTab, 440, 16000 )
    ,SoundGen("string4", 1, EnvTab, 440, 16000 ) ,SoundGen("string5", 1, EnvTab, 440, 16000 )
    ,SoundGen("string6", 1, EnvTab, 440, 16000 ) ]

    __chord_limit = 6

    @classmethod
    def Play(cls, FreqList=[], duration=1):
	ChordManager.ChangeFreqs(FreqList)

	temp_list = ChordManager.StringList[0:len( FreqList)]

	for snd in temp_list: #ChordManager.StringList:
	    snd.thread.ProcOn()
#	cnt = 0
	time.sleep(duration)
		
	for snd in temp_list: #ChordManager.StringList:
	    snd.thread.ProcOff()

    @classmethod
    def ChangeFreqs(cls, FreqList=[]):
	count = 0
	for freq in FreqList:
	    ChordManager.StringList[count].ChangeOscFreq(freq)
	    count +=1

    @classmethod
    def ChangeTables(cls, Table):
	for snd in ChordManager.StringList:
	    snd.ChangeOscTable(Table)

    @classmethod
    def ChangeAmps(cls, amp):
	for snd in ChordManager.StringList:
	    snd.ChangeOscAmp(amp)

    @classmethod
    def GetChordLimit(cls):
	return ChordManager._ChordManager__chord_limit

    @classmethod
    def SetChordLimit(cls):
	pass


# potentially better chord class

class TrueChord(Sound.Sound):

    def __init__(self,name='', duration=1, FreqList=[440] ):
	super(TrueChord, self).__init__(name, duration)
	
	self.limit = 10

	if(len(FreqList) > self.limit ):
	    # keep first 8 frequencies
	    self.FreqList = FreqList[0 : self.limit]
	    print "only first,", self.limit  ,"frequencies will be used"
	else:	
	    self.FreqList = FreqList
		
	TrueChordManager.PrepareTrueChordManager()

    def PrintFreqs(self):
	index = 0
	for Freq in self.FreqList:
		print "Freq ", index, ":", Freq
		index+=1

    def SubtractFreq(self, freq):
	if(len(self.FreqList) > 0):
	    for f in self.FreqList:
		if (f == freq): 
		    self.FreqList.remove(freq)
		    print freq, " removed"
		    break
	else:
	    print "you need to add more frequencies"
	    

    def AddFreq(self, freq):
	if(len(self.FreqList) < self.limit):
	    self.FreqList.append(freq)
	else:
	    print "you have reached the limit of frequencies you can have"

    def SwapFreqs(self, FL):
	if(len(FL) >= self.limit):
	    self.FreqList = FL[0:self.limit]
	else:
	    self.FreqList = FL

    def Play(self):
	TrueChordManager.SetChordFreqs(self)
	TrueChordManager.PlayChord(self)

class TrueChordManager():
	

    limit = 10
    
    # for preparing chord manager
    prepared = False

    # for outputing to speakers
    output = so.SndRTIO(1)

    # for combining signals
    mixer = so.Mixer()

    #
    Osc_List = []

    # function table for Oscili objects
    Tab =so.HarmTable()
	
    # sound thread object
    thread = so.SndThread()

    @classmethod
    def PrepareTrueChordManager(cls):

	if(TrueChordManager.prepared == False):

		amp = 16000/ TrueChordManager.limit

		for x in xrange( TrueChordManager.limit):
		    # Create Oscili Object
		    # with appropriate args
			
		    osc = so.Oscili(TrueChordManager.Tab, 0, amp )	
		    TrueChordManager.Osc_List.append(osc)
		    # add object to Osc_List	

	
		    TrueChordManager.thread.AddObj(osc)
		    TrueChordManager.mixer.AddObj(osc)
		    # add object to Mixer object
		    
		TrueChordManager.output.SetOutput(1, TrueChordManager.mixer)

		TrueChordManager.thread.AddObj(TrueChordManager.mixer)
		TrueChordManager.thread.AddObj(TrueChordManager.output,  so.SND_OUTPUT)
		TrueChordManager.prepared = True
	else:
	        print "TrueChordManager is already initialized"

    @classmethod
    def SetChordFreqs(cls, TrueChord):
	
	OSC_iter = 0
	
	for freq in TrueChord.FreqList:
    	    TrueChordManager.Osc_List[OSC_iter].SetFreq(freq)
	    OSC_iter+=1

	if(OSC_iter != TrueChordManager.limit):
		while(OSC_iter != TrueChordManager.limit):
		    TrueChordManager.Osc_List[OSC_iter].SetFreq(0)
		    OSC_iter+=1
	
    @classmethod
    def PlayChord(cls, TrueChord):	
#	print "should hear something now"
	TrueChordManager.thread.ProcOn()
	time.sleep(TrueChord.duration)
	TrueChordManager.thread.ProcOff()

#	    AAAAA	
#	    |^_^|
#	    |___|
