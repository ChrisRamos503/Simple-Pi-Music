from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.properties import StringProperty

from kivy.core.window import Window
#Window.fullscreen = False


import multiprocessing as mp
import PiMusic
import Sound as s

# create Custom Button Class later


class CustomTTTButton(Button):
    def __init__(self, **kwargs):
	super(CustomTTTButton, self).__init__(**kwargs)
	
	self.cb_pressed = False
	#self.symbol = ''


class TicTacToe(BoxLayout): 
   
    def __init__(self, **kwargs):
	super(TicTacToe, self).__init__( **kwargs)

	self.x_pic_location = "pics/x_gold.png"
	self.o_pic_location = "pics/o_gold.png"
	self.button_start = "pics/blue_But_square.png"
	self.reset_exit = "pics/blue_gloss.png"


	self.Xturn = True
        self.buttons_pressed = 0
	self.game_done = False
	
	self.button_layout = GridLayout(cols=3, rows=3)
	self.display = BoxLayout(orientation="vertical")
	
	self.message = Label(text="Player 1's turn")

	exit_button = Button(text="Exit")
	exit_button.background_normal = self.reset_exit
	exit_button.bind(on_press=self.Exit)
	
	reset_button = Button(text="Reset")
	reset_button.background_normal = self.reset_exit
	reset_button.bind(on_press=self.Reset)

	self.display.add_widget(self.message)
	self.display.add_widget(exit_button)
	self.display.add_widget(reset_button)
	
	self.add_widget(self.display)
	

	for x in xrange(9):
	    
	    b = CustomTTTButton(border=[0,0,0,0], background_normal=self.button_start )
	    b.bind(on_press=self.PlayerPokesButton)
	    self.button_layout.add_widget(b)

	#self.button_layout.background_color = [1,0,0,1]
		
	self.add_widget(self.button_layout)

	
	x_sound = s.Mp3File("sms-alert-2-daniel_simon.mp3",3)
	o_sound = s.Mp3File("sms-alert-5-daniel_simon.mp3",3)
	draw_sound = s.Mp3File("Sad_Trombone-Joe_Lamb-665429450.mp3",3)
	victory_sound = s.Mp3File("glass_ping-Go445-1207030150.mp3",3)

	self.x_id = PiMusic.CreateEntry(x_sound)
	self.o_id = PiMusic.CreateEntry(o_sound)
	self.draw_id = PiMusic.CreateEntry(draw_sound)
	self.victory_id = PiMusic.CreateEntry(victory_sound)


    def PlaySound(self, musicID):
	
	proc = mp.Process(target=PiMusic.PlayID, args=[musicID])
	proc.start()
	#PiMusic.PlayID(musicID)

    def CheckVictory(self):
	
	b_l = self.button_layout.children
	

	# checks vertical, then horizontal, then diagonals

	if( ( (b_l[0].background_normal != self.button_start) and (b_l[0].background_normal == b_l[3].background_normal) and (b_l[0].background_normal == b_l[6].background_normal) ) or

	    ( (b_l[1].background_normal != self.button_start) and (b_l[1].background_normal == b_l[4].background_normal) and (b_l[1].background_normal == b_l[7].background_normal) ) or
	
	    ((b_l[2].background_normal != self.button_start) and (b_l[2].background_normal == b_l[5].background_normal) and (b_l[2].background_normal == b_l[8].background_normal) ) or
	
	    ( (b_l[0].background_normal != self.button_start) and (b_l[0].background_normal == b_l[1].background_normal) and (b_l[0].background_normal == b_l[2].background_normal) ) or

	    ((b_l[3].background_normal != self.button_start) and (b_l[3].background_normal == b_l[4].background_normal) and (b_l[3].background_normal == b_l[5].background_normal) ) or


	    ((b_l[6].background_normal != self.button_start) and (b_l[6].background_normal == b_l[7].background_normal) and (b_l[6].background_normal == b_l[8].background_normal) ) or

	    ((b_l[0].background_normal != self.button_start) and (b_l[0].background_normal == b_l[4].background_normal) and (b_l[0].background_normal == b_l[8].background_normal) ) or

	    ((b_l[2].background_normal != self.button_start) and (b_l[2].background_normal == b_l[4].background_normal) and (b_l[2].background_normal == b_l[6].background_normal) ) 
	
	 ):

	    self.DeclareWinner()
	elif(self.buttons_pressed == 9):
            self.PlaySound(self.draw_id)	    

	else:
	    self.SwapTurn()
		
	
	
	# check for 3 symbols in a row

    def PlayerPokesButton(self, instance):
	if( (self.game_done == False) and (instance.cb_pressed == False) ):
	    
	    
	    if(self.buttons_pressed < 9):
		
		self.ChangeSymbol(instance)
		self.buttons_pressed += 1
	        
		#self.SwapTurn()
	
		if(self.buttons_pressed >= 5):
		    self.CheckVictory()
		else:
		    self.SwapTurn()
		
		#if()self.SwapTurn()
	    
	    instance.cb_pressed = True
	    # declare a draw
		
	pass
	# set Symbol

    def ChangeSymbol(self, instance):
	
	symbol = ""
	if(self.Xturn == True):
	    #symbol = "X"
	    #print "X's turn"
	    
	    symbol = self.x_pic_location
	else:         
	    #symbol = "O"

	    symbol = self.o_pic_location
	
	print "button's background_color =", instance.background_color


	instance.background_normal = symbol
	instance.background_color = [0,0,1,1]
	


	#instance.text = symbol

    def SwapTurn(self):
	player_num = 0

	snd_id = 0

	if( self.Xturn == True):
	    self.Xturn = False
	    player_num = 2
	    snd_id = self.x_id
	
	else:
	    self.Xturn = True
	    player_num = 1
	    snd_id = self.o_id

	msg = "Player " + str(player_num) + "'s turn"

	self.message.text = msg
	self.PlaySound(snd_id)

    def DeclareWinner(self):
	player_num = 0

	# this is reversed when turn is swaped before victory is declared
	# thus if self.Xturn == True, then player 2 won
	if(self.Xturn == True):
	    player_num = 1
	else:
	    player_num = 2
	
	msg = "Player " + str(player_num) + " is the victor"

	self.message.text = msg

	self.game_done = True
	
	self.PlaySound(self.victory_id)

    def Reset(self, instance):

	Window.screenshot(name='screenshot{:04d}.png')
	print "\n\n\nnew image\n\n\n"
	
	self.Xturn = True
        self.buttons_pressed = 0
	self.game_done = False

	for kid in self.button_layout.children:
		#kid.text = ""
		kid.cb_pressed = False
		kid.background_normal = self.button_start
		#'atlas://data/images/defaulttheme/button' #makes white background for buttons
		kid.background_color = [1,1,1,1]
	# resets the game\

	self.message.text = "Player 1's turn"

    def Exit(self, instance):
	App.get_running_app().stop()

class TicTacToeApp(App):

    def __init__(self, **kwargs):
	super(TicTacToeApp, self).__init__(**kwargs)

    def build(self):
	return TicTacToe()

if __name__ == "__main__":

    TicTacToeApp().run()
