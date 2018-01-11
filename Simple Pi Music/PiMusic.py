#//////////////////////////////////////start of code//////////////////////////////////////////#
import subprocess as sp
import multiprocessing as mp
import time
import soundgen
import Sound

SoundDict = {}
CurrentID = 0
UnknownName = 0


def GetNewSoundID():

    "Prepares a new ID for a Sound object"
    
    if(SoundDict.keys() != []):
        prevKey = SoundDict.keys()[0]
	print "first key =",prevKey
	
        for keys in SoundDict.keys():
		    
	    if( (prevKey + 1) != keys and prevKey != keys):
		return prevKey + 1
	    prevKey = keys
        
	return prevKey + 1 
    
    else:
	print "there are no entries in the Sound Dictionary"
	return 0

def SelectFiles():
    """
    prints a list of sounds organized by modification time
    """
    sp.Popen("ls -t *.wav *.mp3 *.sf2 *.mid", shell=True)
    pass

def SelectSound():
    """
    returns a list of sound ID's and Names of respective sounds
    """

    for keys in SoundDict.keys():
	print "ID:", keys, " Name:", SoundDict[keys][0]
##########################################################################################

def CreateEntry(Sound):
    """    
	Creates an entry in SoundDictionary
	of format:
		  key : (name, sound)

    """
    if(Sound.name == ""):
	Sound.name = "UnNamed_Sound_" + str(UnknownName)
	UnknownName += 1

    ID = GetNewSoundID()
    SoundDict[ID] = (Sound.name, Sound)

    return ID

def PlayID(ID):
    """
	plays music or sound that has been put 
	in the sound dictionary with ID
    """
    try:    
        SoundDict[ID][1].Play()
    except KeyError:
	print "KeyError:\nthis Key does not exist\ntry using PiMusic.SelectSound()\nto find a sound clip to create a sound object or make a SoundGen"
    except TypeError as te:
	#raise Exception("this function accepts one integer argument\ni.e PiMusic.PlayID(0)") from te
	raise TypeError("WTF")
	print "this function accepts one integer argument\ni.e PiMusic.PlayID(0)"    

def PlaySequenceIDs(IDs=[]):
    """
	   play notes in a sequence via IDs
    """
    try:
	for i in IDs:
	    i.Play()
    except KeyError:
	print "this Key does not exist\n try using PiMusic.SelectSound()"
    except TypeError: 
	print "this function accepts a list of integers\ni.e PiMusic.PlayID([0,1,2,3])"    

def PlayMultipleIDs(IDs=[]):

    try:
	procs = []
	#first_key = SoundDict.keys()[0]	
	#first_duration = SoundDict[first_key][1].duration

	for i in IDs:
	    sound = SoundDict[i][1]
	    #if( isinstance(sound, soundgen.SoundGen))):
	#	print "SoundGen"
		
	    procs.append(mp.Process(target=sound.Play, args=[ ]))
	    print "ID =",i

	[proc.start() for proc in procs]

    except KeyError:
	print "this Key does not exist\n try using PiMusic.SelectSound()"
    except TypeError: 
	print "this function accepts a list of integers\ni.e PiMusic.PlayID([0,1,2,3])"    

def FreeMemory(ID): # -> clears memory
    """
	deletes an entry in the sound dictionary
    """
    try:
        print "clearing sound entry"
        del SoundDict[ID]
    except KeyError:
	print "KeyError:\nthis Key does not exist\ntry using PiMusic.SelectSound()"
    except TypeError: 
	print "this function accepts one integer argument\ni.e PiMusic.FreeMemory(0)" 
   
def FreeSoundDictMemory():
    """
    clears the SoundDictionary

    """
   
    print "clearing SoundDictionary"
    for item in SoundDict.keys():
        del SoundDict[item]
    #SoundDict = None

def SetVolume(volume): 
    
    """
    trying to use the following command -> amixer set PCM 10 <-
    does not set the volume to 10dBs, but instead sets it to 96% of max volume
	
    however you can add or subtract volume to get a desired volume. 
    volume = -106 = mute (effectively)
    volume = 106 = Max volume
    """
    
    if(type(volume) is int or type(volume) is float):
	Vol = int(volume)
  
        sign = "+"
        Arg_String = "amixer -q set PCM "

        if(Vol < 0):
       	    sign = "-"

        Arg_String += volume + "dB" + sign
    
        sp.Popen(Arg_String, shell=True)

    else:
	print "this method only accepts integers and floats"
     
   # sp.Popen("amixer set PCM 106dB+", shell=True)
  
    pass

def Exit():
    """
	Exits the program and frees memory 
	by deleteing SoundDictionary
    """

    #print "I quit()"
    freeMemory()
    quit()
    pass

def IsFile(Name):
    """
	Determines the type of file and 
	returns respective code 
    """

    file = 0
    NameStr = Name[-4:len(Name)]
    
    if(NameStr == '.wav'):
	print "file is wav"
	file = 4
    
    elif(NameStr == '.mp3'):
	print "file is mp3"
	file = 3

    elif(NameStr == '.sf2'):
	print "file is sound font 2 "
	file = 2

    elif(NameStr == '.mid'):
	print "file is midi"
	file = 1
    
    else:
	print "unknown type of sound"
	file = 0

    return file


def SoundFromFileCode(name, duration):
	
	SoundFile = NULL

	filecode = IsFile(name)	

	if(filecode == 4):
		SoundFile = Sound.WavFile(name, duration)
	
	elif(filecode == 3):
		SoundFile = Sound.Mp3File(name, duration)

	elif(filecode == 2):
		SoundFile = Sound.SoundFont2File(name, duration)
	
	elif(filecode == 1):
		SoundFile = Sound.MidiFile(name, duration)
	else:
	        pass

	return SoundFile

#////////////////////////////////////End of Class/////////////////////////////////////////////#

