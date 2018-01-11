from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import time
import sndobj as so
import soundgen as sg
###############################################################################
#just wanted to note that I had to offset everything by one
#I couldn't see any way around that, so I decided to that
#or at least in Step_Sequencer3.py 
###############################################################################

class CustomButton(Button):
    #@profile
    def __init__ (self, png, freq, **kwargs):
	super(CustomButton, self).__init__(**kwargs)
   #back ground color for buttons
        self.BGC = png
	self.OFreq = freq # to set notes back to original frequency
	self.freq = 0


class StepSequencer(StackLayout):
    """
	NumColumns is the number of columns in the sequencer and the number of
	button in the columns. NumColumns^2 is the number of buttons in the 
	StepSequencer
    """

    #@profile
    def __init__ (self, FL, interval= 0.95, **kwargs):
	super(StepSequencer, self).__init__ ( **kwargs)


	

	# REMEMBER TO CHANGE '==' BACK TO '!='
	if(len( FL) <= 1 or len (FL) >=11):
	    print "length of Frequency List must be between 2 and 10"
	    quit()
	    	
	if(interval < 0.50):
	    print "interval is too small"
	    quit()


	self.blue_but = "pics/blue3-button.png"
	self.yellow_but = "pics/yellow-button2.png"
	self.red_but = "pics/redbutton.png"
	self.green_but = "pics/green-button.png"
	self.dark_but = "pics/Brown-button2.png"

# ----------------------------------------------------------------

	self.chord = sg.TrueChord(duration=(interval -0.07),FreqList=FL)

# ----------------------------------------------------------------

	self.NumColumns = len(FL)
	#current column i.e the greenish-blue one
	self.CurrCol = 0
	#index for synth list
	self.SynthIndex = self.NumColumns
	
	self.Volume = 110

	# frequency the Greenish-blue beam moves
	self.Interval = interval
	Const = float( 1.0 / self.NumColumns)
	Const2 = float( 1.0 / (self.NumColumns + 1))

	self.orientation = ('bt-rl')#, ['lr-tb', 'tb-lr', 'rl-tb', 'tb-rl', 'lr-bt',##'bt-lr', 'rl-bt', 'bt-rl'])

	control = 0
	f = 60   
	ColSQ = self.NumColumns * self.NumColumns

	FL_index = 0
	while control != ColSQ:
	    
	    if(FL_index == len(FL)): # cycle through frequencies again
		FL_index = 0
	    
	    btn0 = CustomButton(self.blue_but, freq=FL[FL_index], size_hint=(Const2, Const), background_normal = self.blue_but , border=[0,0,0,0])
	    btn0.bind(on_press=self.IColorChange)
	    self.add_widget(btn0)
	    
	    FL_index+= 1
	    control+= 1

	ExitButton = Button(text="Exit", size_hint=(Const2, 0.50), background_normal=self.dark_but, border=[0,0,0,0])
        ExitButton.bind(on_press=self.superExit) 
        self.add_widget(ExitButton)

############################################################

    #@profile
    def Change_Color(self, dt):
	
        self.FrequencyChange()

	if self.CurrCol != self.NumColumns -1:
	    for kid in self.children[ (self.CurrCol * self.NumColumns) + 1 : (( self.CurrCol +1) * self.NumColumns) +1  ]:
	        kid.background_normal = kid.BGC
	
	    #print self.CurrCol
	    self.CurrCol += 1
		
	    for kid in self.children[ (self.CurrCol * self.NumColumns) + 1 : (( self.CurrCol +1) * self.NumColumns) +1  ]:
	        kid.background_normal = self.green_but
	else:
		
	    for kid in self.children[ (( self.CurrCol ) * self.NumColumns) + 1 : (( self.CurrCol + 1) * self.NumColumns) + 1 ]:
	        kid.background_normal = kid.BGC
		
	    self.CurrCol = 0

	    for kid in self.children[ 1 : self.NumColumns + 1]:
	        kid.background_normal = self.green_but
		#kid.background_normal = self.green_but

	    
        #self.FrequencyChange()
	self.Play2()
	#self.NoiseOn()
	

    #@profile
    def IColorChange(self, instance):
	#if instance.background_color == self.red_but:
	if instance.freq != 0:
	
	    #back to normal background color
    	    instance.background_normal = self.blue_but
	    instance.BGC = self.blue_but
		
	    instance.freq = 0
	else:
	    # otherwise turn red to signify active 
	    instance.background_normal = self.red_but
	    instance.BGC = self.red_but
	
	    instance.freq = instance.OFreq

#    def callback(self,dt):
#	print "callback"

    #@profile
    def UPstart(self):
    	Clock.schedule_interval(self.Change_Color, self.Interval)


    def FrequencyChange(self):
	num = ((self.CurrCol +1)* self.NumColumns)
	marker = num - self.NumColumns	
	# list of buttons in one column
	#ButtonList = self.children[ (num - self.NumColumns): num]
	
	l = []

	while (num > marker):
	    if( self.children[num].freq != 0):
		# change sound objects for buttons that are active (red)
		#self.Osc_List[(num % self.NumColumns)].SetFreq(self.children[num].OFreq)
		l.append(self.children[num].OFreq)

	    else:
		#self.Osc_List[(num % self.NumColumns)].SetFreq(0)
		l.append(0)
	    num-=1
        
	self.chord.SwapFreqs(l)
		
    
    def ButtonNumber(self, instance):
	print "Button = ", instance.text, "/n instance index in tree = ", self.children.index(instance)

    def Play2(self):
	#self.thread.ProcOn()
	#time.sleep(self.Interval -0.07)
	#self.thread.ProcOff()

	self.chord.Play()
	
    #@profile
    def superExit(self, instance):
        App.get_running_app().stop()

class StepSequencerApp(App):
    #@profile
    def __init__ (self,FL, interval= 0.95, **kwargs):
	super(StepSequencerApp, self).__init__(**kwargs)
	self.sequencer = StepSequencer(FL, interval, **kwargs)

    #@profile
    def build(self):
	self.sequencer.UPstart()
	return self.sequencer

if __name__ == '__main__':

    a = StepSequencerApp( [440,330,550, 660, 770, 880, 990, 1100, 1200, 1300], interval= 0.55)
    a.run()
