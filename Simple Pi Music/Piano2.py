#!/usr/bin/python
#kivy.require('1.0.6') # replace with your current kivy version !
import time
import fluidsynth 	# to play the notes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

class CustomButton(Button):
    """
    A custom button used to store arguments that are used 
    to generate the correct frequency.
    """
    def __init__(self, mystery, frequency, volume, **kwargs):
	super(CustomButton, self).__init__(**kwargs)

#################################################
	self.mystery = mystery
	self.freq = frequency
	self.vol = volume
##################################################
	self.background_normal = ''
	self.background_color = [1,1,1,1] #self.background_color_normal	

    def Turn_On(self,FsSynth):
	FsSynth.noteon(self.mystery, self.freq, self.vol)

    def Turn_Off(self, FsSynth):
	FsSynth.noteoff(self.mystery, self.freq)

class Piano(FloatLayout):
# dont forget to divide button space by 11 
    """
    This Class creates a Piano object, but must be launched with 
    the PianoApp Class.
    """
    
    def __init__ (self, sf2_File, **kwargs):
	super(Piano, self).__init__ ( **kwargs)
	self.size=(300, 300)
	self.Dim = 0.09090
	self.ButtonHeight = 0.3
#	new edition 11-29-15
#	Frequency
	freq = 58

        exitconst = 1-self.Dim
        ExitButton = Button(text="exit", size_hint=(self.Dim-0.0009, self.Dim -0.0009),pos_hint={"x":exitconst, "y":exitconst})
        ExitButton.bind(on_press=self.superExit)
        
        self.add_widget(ExitButton)

# White Piano keys
	btn0 = CustomButton(0, freq + 2, 110, text="", size_hint=(self.Dim-0.0009, 2*self.ButtonHeight),pos_hint={"x":0.0, "y":0.0})
	btn1 = CustomButton(0, freq + 4,110 ,text="", size_hint=(self.Dim-0.0015, 2*self.ButtonHeight),pos_hint={"x":self.Dim, "y":0.0})#0.2
	btn2 = CustomButton(0, freq + 6, 110, text="", size_hint=(self.Dim-0.0009, 2*self.ButtonHeight),pos_hint={"x":(2*self.Dim - .001), "y":0.0})#0.4
	btn3 = CustomButton(0, freq + 7, 110, text="", size_hint=(self.Dim-0.0009, 2*self.ButtonHeight),pos_hint={"x":(3*self.Dim), "y":0.0})#0.2 
	btn4 = CustomButton(0, freq + 9, 110, text="", size_hint=(self.Dim-0.0009, 2*self.ButtonHeight),pos_hint={"x":(4*self.Dim), "y":0.0})
	btn5 = CustomButton(0, freq + 11, 110, text="", size_hint=(self.Dim-0.0015, 2*self.ButtonHeight),pos_hint={"x":(5*self.Dim), "y":0.0})
	btn6 = CustomButton(0, freq + 13, 110, text="", size_hint=(self.Dim-0.0009, 2*self.ButtonHeight),pos_hint={"x":(6*self.Dim), "y":0.0})
	btn7 = CustomButton(0, freq + 14, 110, text="", size_hint=(self.Dim-0.0009, 2*self.ButtonHeight),pos_hint={"x":(7*self.Dim), "y":0.0})
	btn8 = CustomButton(0, freq + 16, 110, text="", size_hint=(self.Dim-0.0015, 2*self.ButtonHeight),pos_hint={"x":(8*self.Dim), "y":0.0})
	btn9 = CustomButton(0, freq + 18, 110, text="", size_hint=(self.Dim-0.0009, 2*self.ButtonHeight),pos_hint={"x":(9*self.Dim - .001), "y":0.0})
	btn10 = CustomButton(0, freq + 19, 110, text="", size_hint=(self.Dim-0.0009, 2*self.ButtonHeight),pos_hint={"x":(10*self.Dim), "y":0.0})
        
	btn1.bind(on_press=self.btn_pressed)
	btn1.bind(on_release=self.btn_released)

# White Piano key bindings
	btn0.bind(on_press=self.btn_pressed)
	btn0.bind(on_release=self.btn_released)
	btn1.bind(on_press=self.btn_pressed)
	btn1.bind(on_release=self.btn_released)
	btn2.bind(on_press=self.btn_pressed)
	btn2.bind(on_release=self.btn_released)
	btn3.bind(on_press=self.btn_pressed)
	btn3.bind(on_release=self.btn_released)
	btn4.bind(on_press=self.btn_pressed)
	btn4.bind(on_release=self.btn_released)
	btn5.bind(on_press=self.btn_pressed)
	btn5.bind(on_release=self.btn_released)
	btn6.bind(on_press=self.btn_pressed)
	btn6.bind(on_release=self.btn_released)
	btn7.bind(on_press=self.btn_pressed)
	btn7.bind(on_release=self.btn_released)
	btn8.bind(on_press=self.btn_pressed)
	btn8.bind(on_release=self.btn_released)
	btn9.bind(on_press=self.btn_pressed)
	btn9.bind(on_release=self.btn_released)
	btn10.bind(on_press=self.btn_pressed)
	btn10.bind(on_release=self.btn_released)
	
# White Piano keys added
	self.add_widget(btn0)
	self.add_widget(btn1)
	self.add_widget(btn2)
	self.add_widget(btn3)
	self.add_widget(btn4)
	self.add_widget(btn5)
	self.add_widget(btn6)
	self.add_widget(btn7)
	self.add_widget(btn8)
	self.add_widget(btn9)
	self.add_widget(btn10)

# Black Piano keys
	Bbtn0 = CustomButton(0, freq + 3, 110, text="", size_hint=( 0.8*self.Dim, self.ButtonHeight),pos_hint={"x":(0.5*self.Dim), "y":.3})
	Bbtn1 = CustomButton(0, freq + 5, 110, text="", size_hint=( 0.8*self.Dim, self.ButtonHeight),pos_hint={"x":(1.5*self.Dim), "y":.3})
	Bbtn2 = CustomButton(0, freq + 8, 110, text="", size_hint=( 0.8*self.Dim, self.ButtonHeight),pos_hint={"x":(3.5*self.Dim), "y":.3})
	Bbtn3 = CustomButton(0, freq + 10, 110, text="", size_hint=( 0.8*self.Dim, self.ButtonHeight),pos_hint={"x":(4.5*self.Dim), "y":.3})
	Bbtn4 = CustomButton(0, freq + 12, 110, text="", size_hint=( 0.8*self.Dim, self.ButtonHeight),pos_hint={"x":(5.5*self.Dim), "y":.3})
	Bbtn5 = CustomButton(0, freq + 15, 110, text="", size_hint=( 0.8*self.Dim, self.ButtonHeight),pos_hint={"x":(7.5*self.Dim), "y":.3})
	Bbtn6 = CustomButton(0, freq + 17, 110, text="", size_hint=( 0.8*self.Dim, self.ButtonHeight),pos_hint={"x":(8.5*self.Dim), "y":.3})

# Black Piano key bindings

	Bbtn0.bind(on_press=self.btn_pressed)
	Bbtn0.bind(on_release=self.btn_released)
	Bbtn1.bind(on_press=self.btn_pressed)
	Bbtn1.bind(on_release=self.btn_released)
	Bbtn2.bind(on_press=self.btn_pressed)
	Bbtn2.bind(on_release=self.btn_released)
	Bbtn3.bind(on_press=self.btn_pressed)
	Bbtn3.bind(on_release=self.btn_released)
	Bbtn4.bind(on_press=self.btn_pressed)
	Bbtn4.bind(on_release=self.btn_released)
	Bbtn5.bind(on_press=self.btn_pressed)
	Bbtn5.bind(on_release=self.btn_released)
	Bbtn6.bind(on_press=self.btn_pressed)
	Bbtn6.bind(on_release=self.btn_released)

	Bbtn0.background_color = [0,0,0,1]
	Bbtn1.background_color = [0,0,0,1]
	Bbtn2.background_color = [0,0,0,1]
	Bbtn3.background_color = [0,0,0,1]
	Bbtn4.background_color = [0,0,0,1]
	Bbtn5.background_color = [0,0,0,1]
	Bbtn6.background_color = [0,0,0,1]

# Adding Black piano keys

	self.add_widget(Bbtn0)
	self.add_widget(Bbtn1)
	self.add_widget(Bbtn2)
	self.add_widget(Bbtn3)
	self.add_widget(Bbtn4)
	self.add_widget(Bbtn5)
	self.add_widget(Bbtn6)

	self.fs = fluidsynth.Synth()
        self.fs.start('alsa')			# starting fluidsynth
	
        #sfid = self.fs.sfload("fs.sf2") 		# loading soundfont
        sfid = self.fs.sfload(sf2_File) 
        self.fs.program_select(0, sfid, 0, 0)

    def btn_pressed(self, instance):#, pos):
	instance.Turn_On(self.fs )
        print ("what bros?")

    def btn_released(self, instance):
	instance.Turn_Off(self.fs )
        print ("Did I do something funny?")

    """
    exiting just got super!
    """
    def superExit(self, instance):
        App.get_running_app().stop()

class PianoApp(App):
    """
    The PianoApp Class is used to render a Piano object onto the screen.
    All applications that use Kivy must have an app Class that inherits 
    from Kivy's App class. Using the inherited app class' run() method
    you can launch an app or in this case a Piano. 
    Don't scoff, that's just how Kivy works.

    try it:
	
    obj = PianoApp("SomeName.sf2")
    obj.run()
    """
    def __init__(self, sf2, **kwargs):
	super(PianoApp, self).__init__(**kwargs)
	self.piano = Piano(sf2)

    """
    This method is not supposed to be invoked directly by the user.
    """
    def build(self):
	#return Piano("p2.sf2")
	return self.piano


if __name__ == "__main__":
			
    #PianoApp().run()
    a = PianoApp("p2.sf2")
    a.run()
					# app finishes
    time.sleep(1.0)

