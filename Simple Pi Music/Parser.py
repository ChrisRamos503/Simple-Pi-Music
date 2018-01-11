import math as m
import soundgen as sg
import sndobj as so
import PiMusic


ScaleDict = {}
ScaleDict['M'] = (0,2,2,1,2,2,2,1) 
ScaleDict['m'] = (0,2,1,2,2,1,2,2) 

RootNoteDict = {}
RootNoteDict['C'] = 32.7032
RootNoteDict['C#'] = 34.6478
RootNoteDict['D'] = 36.7081 
RootNoteDict['D#'] = 38.8909
RootNoteDict['E'] = 41.2034
RootNoteDict['F'] = 43.6535
RootNoteDict['F#'] = 46.2493
RootNoteDict['G'] = 48.9994
RootNoteDict['G#'] = 51.9131
RootNoteDict['A'] = 55.0
RootNoteDict['A#'] = 58.2705
RootNoteDict['B'] = 61.7354
RootNoteDict['R'] = 0.0
RootNoteDict[0] = 0.0

MusicMeterDict = {}
MusicMeterDict[1] = 'w'
MusicMeterDict[2] = 'h'
MusicMeterDict[4] = 'q'
MusicMeterDict[8] = 'e'
MusicMeterDict[16] = 's'
MusicMeterDict[32] = 't'
MusicMeterDict[64] = '64'

MusicCodeDict = {}
MusicCodeDict['w'] = 0
MusicCodeDict['h'] = 0
MusicCodeDict['q'] = 0
MusicCodeDict['e'] = 0
MusicCodeDict['w'] = 0
MusicCodeDict['t'] = 0
MusicCodeDict['64'] = 0

# w = whole
# h = half
# q = quarter
# e = eighth
# s = sixteenth
# t = 32th

# noteList = [('A3', 'e'),('A3', 'e'),('A3', 'e'), ('B3', 'e')]
#              ('A#3' , 'e')

MajorChordDict = {}

MajorChordDict['M'] = (0,4,3)
MajorChordDict['Madd4'] = (0,4,1,2)
MajorChordDict['M6'] = (0,4,3,2)
MajorChordDict['M6/9'] = (0,4,3,2,5)
MajorChordDict['M7'] = (0,4,3,4)
MajorChordDict['M9'] = (0,4,3,4,3)
MajorChordDict['M7#11'] = (0,4,3,4,6)
MajorChordDict['Mf5'] = (0,4,2)


MinorChordDict = {}
MinorChordDict['m'] = (0,3,4)
MinorChordDict['mad4'] = (0,3,2,2)
MinorChordDict['m6'] = (0,3,4,1)
MinorChordDict['m7'] = (0,3,4,3)
MinorChordDict['madd9'] = (0,3,4,7)
MinorChordDict['m6/9'] = (0,3,4,1,6)
MinorChordDict['m9'] = (0,3,4,3,4)
MinorChordDict['m/M7'] = (0,3,4,4)
MinorChordDict['m/M9'] = (0,3,4,4,3)
MinorChordDict['m7f5'] = (0,3,3,4)

#
#
#
#

def AssignDurations(time_per_beat, note_type):
    count = 0
    while (count <= 6):
        MusicCodeDict[ MusicMeterDict[note_type] ] = time_per_beat
        if(note_type == 64):
            note_type = 1
            time_per_beat *= 64.0
        else:
            note_type *= 2
            time_per_beat /= 2.0
        count += 1
    pass


def ParseNoteList(NoteList=[], meter='4/4', bpm=120):
    """
    parses a list and returns frequencies
    """
    
    mult = 1		# multiplier
    rnote = ''		# reference note
    freq = 0		# frequency
    dur = 1.0   	# duration
      
    # splits meter in to list
    time_list = meter.split('/')
    
    num_note_type = int (time_list[0])
    note_type = int (time_list[1])

    time_per_meter = float (num_note_type) / float (bpm)
    
    # time per meter in seconds
    time_per_meter *= 60

    time_per_note_type = time_per_meter / note_type

    AssignDurations(time_per_note_type, note_type)

    # list of note frequencies
    FreqList = []

    for note in NoteList:
	mult = float ( note[0][len(note[0]) - 1: len(note[0])] )
	rnote = note[0][0: len(note[0]) -1] 
	freq = RootNoteDict[rnote]

        dur = MusicCodeDict[ note[1] ]

        # appends freq and duration in tuple
	FreqList.append( (freq * m.pow(2, mult - 1), dur) )

    return FreqList

def PlayNoteList(NoteList=[], meter='4/4', bpm=120):

    #HarmTab =so.HarmTable()
    player = sg.SoundGen("", 2, sg.HarmTab)
    
    
    FreqList = ParseNoteList(NoteList, meter, bpm)

    for notes in FreqList:
	# sends in freq and duration respectfully
	player.PlayTime(notes[0], notes[1])
    pass


def ScaleToNotes(scale, rnote, mult):
    # distance to travel from previous notes
    steps = ScaleDict[scale]
    count = 0
    lp_cnt = 0

    FreqList = []
    #noteList = RootNoteDict.keys()
    noteList = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

    print noteList

    for keys in noteList:
	if(keys != rnote):
	    count +=1
#	elif(count > len(RootNoteDict) ):
#	    print "you must a enter a proper key"
	else:# keys == rnote 
	    break

############################################## insert a better 
############################################## way to exit

    if(count >= 13):
	print "this is an invalid key"
	quit()

    while(lp_cnt < 8):

	print "count =", count
	#print "mult =", mult
	# traversing scale in whole or half steps
	count += steps[lp_cnt]
	print "count =", count

	if(count >= ( len(RootNoteDict.keys()) - 2)):
	    count = count - ( len(RootNoteDict.keys()) - 2)
	    print count
	    print len(RootNoteDict.keys())
	    mult += 1
	print "note =", noteList[count]
	note = RootNoteDict[ noteList[count]]
	
	print note
	# calculate frequency
	FreqList.append( note * m.pow(2.0, mult - 1)  )

	lp_cnt += 1
    
    return FreqList

# Major C starting at C4
def PlayScale(key='MC4', duration=1):
    
    scale = key[0]
    mult = float ( key[len(key) - 1: len(key)] )
    rnote = key[1: len(key) -1]
    
    FreqList = ScaleToNotes(scale, rnote, mult)

    print FreqList

    player = sg.SoundGen("", 2, sg.HarmTab)

    for notes in FreqList:
	# sends in freq and duration respectfully
	player.PlayTime(notes, duration)

def CreateChord(chordname, note):
    """
    creates a standard chord
    from one of the chord
    dictionaries 
    """
    chord_steps = 0
	
    if(chordname[0] == 'M'):
	chord_steps = MajorChordDict[ chordname]
    else:
	chord_steps = MinorChordDict[ chordname]

    count = 0
    lp_cnt = 0
    mult = 0.0

    FreqList = []

    #noteList = RootNoteDict.keys()
    noteList = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

    print noteList

    for keys in noteList:
	if(keys != note):
	    count +=1
#	elif(count > len(RootNoteDict) ):
#	    print "you must a enter a proper key"
	else:# keys == rnote 
	    break

    if(count >= 13):
	print "this is an invalid key"
	quit()


    while(lp_cnt < len(chord_steps)):

	print "count =", count
	#print "mult =", mult
	# traversing scale in whole or half steps
	count += chord_steps[lp_cnt]
	print "count =", count

	if(count >= ( len(RootNoteDict.keys()) - 2)):
	    count = count - ( len(RootNoteDict.keys()) - 2)
	    print count
	    print len(RootNoteDict.keys())
	    mult += 1
	print "note =", noteList[count]
	note = RootNoteDict[ noteList[count]]
	
	print note
	# calculate frequency
	FreqList.append( note * m.pow(2.0, mult - 1)  )

	lp_cnt += 1
    
    created_chord = sg.Chord( chordname + "Chord", 1, FreqList)
    PiMusic.CreateEntry(created_chord)

def CreateCustomChord(NoteList):
    
    mult = 1
    root = ""
    freq = 0.0
    FreqList = []

    for note in NoteList:
	mult = float ( note[len(note) - 1: len(note)] )
	root = note[0: len(note) -1] 
	freq = RootNoteDict[root]
	
	FreqList.append( freq * m.pow(2.0, mult - 1)  )

    created_chord = sg.Chord("Custom Chord", 1, FreqList)
    PiMusic.CreateEntry(created_chord)

