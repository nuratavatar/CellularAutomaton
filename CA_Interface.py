#Tarun Mandalapu 2017

try:
	import Tkinter as tk
	import ttk
except ImportError: #for python 3.3
	import tkinter as tk
	from tkinter import ttk

# (R)ushy (P)anchal modified Zelle's graphics library
# to support GraphWins within frames
import RP_graphics as graphics

import math
from random import randint
from time import sleep



class IteratedFunctionSystemsApp:

   
	# constructor for App class, which implements an App to
	def __init__(self, master):
		self.master = master
		self.gettingRule = False
		#Variables
		self.pause = True
		self.generation = 0
		self.tempLogic = []
		self.numCells = 9
		self.inputting = True
		self.gridSq = [] #list to hold rectangle objects that make up the grid
		self.logic = [] #holds all the logic behind the grid
		self.tempLogic = []
		self.rules = []
		self.rule = 0
		self.currentRow = self.numCells - 1
		#Container Frame
		self.frame = tk.Frame(self.master, background = 'gray11')

		#Graph frame
		self.drawFrame = tk.Frame(self.frame, bg = "gray15")
		self.drawFrame.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = tk.N)

		#Frame holding controls
		self.controlFrame = tk.Frame(self.frame, bg = 'gray15')
		self.controlFrame.grid(row = 1, column = 2, padx = 10, pady = [10,100], sticky = tk.N + tk.S)

		#Frame holding rule interface
		self.ruleFrame = tk.LabelFrame(self.controlFrame, bg = 'gray15', fg = 'white')
		self.ruleFrame.configure(text = "Rule Interface")
		self.ruleFrame.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 15)

		#Frame holding state space editor
		self.ssEditor = tk.LabelFrame(self.controlFrame, bg = 'gray15', fg = 'white')
		self.ssEditor.configure(text = "State Space Editor")
		self.ssEditor.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 15)

		#Frame holding program controls
		self.progContFrame = tk.LabelFrame(self.controlFrame, bg = 'gray15', fg = 'white')
		self.progContFrame.configure(text = "Program Controls")
		self.progContFrame.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 15)

		#Creating the grid
		self.grid = graphics.GraphWin(self.drawFrame, 700, 700, autoflush = False)
		self.grid.grid(row = 1, column = 1, padx = 10, pady = 10)
		self.grid.setCoords(0, 0, self.numCells, self.numCells)
		self.grid.setBackground('gray92')

		self.isDrawn = False
		if(not self.isDrawn):
			#populating our lists and drawing our grid
			for i in range(self.numCells):
				self.gridSq.append([])
				self.logic.append([])
				self.tempLogic.append([])
				for j in range(self.numCells):
					#add a Rectangle graphics object with sidelength 1 to the current row in the grid
					self.gridSq[i].append(graphics.Rectangle(graphics.Point(i+ 2*self.numCells/700, j - 2*self.numCells/700), graphics.Point(i+1 + 2*self.numCells/700, j+ 1 - 2*self.numCells/700)))
					self.gridSq[i][j].draw(self.grid)

					#filling out the logic array
					self.logic[i].append(False)
					self.tempLogic[i].append(False)
			self.isDrawn = True
		#padding arrays
		#self.logic = ([False] * (self.numCells)) + self.logic + ([False] * (self.numCells))
		#self.tempLogic = ([False] * (self.numCells)) + self.tempLogic + ([False] * (self.numCells))
		#for x in range(self.numCells):
		#	self.logic[x] = [False] + self.logic[x] + [False]
		#	self.tempLogic[x] = [False] + self.tempLogic[x] + [False]
		#self.numCells += 2
		#Creating the controls
		#Creating a graph window where the user can choose their ruleset
		self.nHood = graphics.GraphWin(self.ruleFrame, 200, 200, autoflush = False)
		self.nHood.grid(row = 1, column = 0, columnspan = 2, padx = 20, pady = 5)
		self.nHood.setCoords(0, 0, 3, 3)
		self.cells = []
		self.log = []

		#Drawing the neighborhood
		for i in range(0, 3):
			self.cells.append([])
			self.log.append([])
			for j in range(0, 3):
				#drawing square and stuff
				self.cells[i].append(graphics.Rectangle(graphics.Point(i+6/200, j-6/200), graphics.Point(i+1+6/200, j+1-6/200)))
				self.cells[i][j].draw(self.nHood)
				#filling out the logic array
				self.log[i].append(False)
		self.cells[1][1].setFill('yellow')

		#Buttons for rules
		self.getRuleButton = ttk.Button(self.ruleFrame, text = "GET", command = lambda: self.getRule())
		self.getRuleButton.grid(row = 2, column = 0, padx = 5, pady = 5)

		self.addRuleButton = ttk.Button(self.ruleFrame, text = "ADD", command = lambda: self.addRule())
		self.addRuleButton.grid(row = 2, column = 1, padx = 5, pady = 5)

		#State Space Buttons
		self.setButton = ttk.Button(self.ssEditor, text = "SET", command = lambda: self.setInitialCondition())
		self.setButton.grid(row = 0, column = 0, padx = 5, pady = 5)

		self.randomizeButton = ttk.Button(self.ssEditor, text = "RANDOMIZE", command = lambda: self.randomIC())
		self.randomizeButton.grid(row = 0, column = 1, padx = 5, pady = 5)

		#Program Controls
		self.runButton = ttk.Button(self.progContFrame, text = "RUN", command = lambda: self.run())
		self.runButton.grid(row = 0, column = 0, padx = 5, pady = 5)

		self.pauseButton = ttk.Button(self.progContFrame, text = "PAUSE", command = lambda: self.Pause())
		self.pauseButton.grid(row = 0, column = 1,  padx = 5, pady = 5)

		self.stepButton = ttk.Button(self.progContFrame, text = "STEP", command = lambda: self.step())
		self.stepButton.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5)

		self.frame.pack()

	def step(self):
		cunter = 0
		print("Generation: " + str(self.generation))

		#for rows in self.logic:
			#for cellz in rows:
				#if(cellz):
					#cunter += 1
		#print(cunter)

		for i in range(1, self.numCells - 1):
			for j in range(1, self.numCells -1):
				num = ''
				neighborhood = [[self.logic[i-1][j-1], self.logic[i-1][j], self.logic[i-1][j+1]], [self.logic[i][j-1], False, self.logic[i][j+1]], [self.logic[i+1][j-1], self.logic[i+1][j], self.logic[i+1][j+1]]]
				for row in neighborhood:
					for cell in row:
						if(cell):
							num = num + "1"
						else:
							num = num + "0"
				
				for rule in self.rules:
					#if(int(num) != 0):
						#print(num)
						#print(rule + "-")
					if(rule == num):
						self.tempLogic[i][j] = True
		self.generation += 1

		
		#Updating the grid and transfering the logic
		for x in range(1, self.numCells -1):
			for y in range(1, self.numCells -1):
				if(self.tempLogic[x][y]):
					self.gridSq[x][y].setFill('magenta')
				else:
					self.gridSq[x][y].setFill('gray92')

		#Transferring logic
		self.logic = self.tempLogic
		#print(self.logic)
		for m in range(self.numCells):
					for n in range(self.numCells):
						self.tempLogic[m][n] = False
	def run(self):
		self.pause = False
		while(not self.pause):
			self.step()
			self.grid.update()
			sleep(.5)

	def Pause(self):
		self.pause = True
	def randomIC(self):
		for i in range(self.numCells):
			for j in range(self.numCells):
				rand = randint(0, 1)
				if(rand == 1): #I feel like the == 1 is redundant but I'm just making sure that 0/1's outputted from randint function don't work as booleans
					self.logic[i][j] = True
					print("1")
				else:
					self.logic[i][j] = False
					print("0")
		for x in range(self.numCells):
			for y in range(self.numCells):
				print(self.logic[x][y])
				if(self.logic[x][y]):
					self.gridSq[x][y].setFill('magenta')
				else:
					self.gridSq[x][y].setFill('gray92')

	def setInitialCondition(self):
		if(self.generation == 0):
			while(1):
				#Get the coordinates of the click
				click = self.grid.getMouse()
				#We can round them down
				x = int(click.getX())
				y = int(click.getY())
				#print( str(x) + ", " + str(y))
				self.logic[x][y] = not self.logic[x][y]
				if(self.logic[x][y]):
					self.gridSq[x][y].setFill('magenta')
				else:
					self.gridSq[x][y].setFill('gray92')
		generation = 1
		print("Generation: " + self.generation)

	def getRule(self):
		while(1):
			click = self.nHood.getMouse()
			x = int(click.getX())
			y = int(click.getY())
			#print( str(x) + ", " + str(y))
			if(x == 1 and y == 1):
				True
			else:
				self.cells[x][y].setFill('magenta')
				self.log[x][y] = True

	def addRule(self):
		num = ''
		for row in self.log:
			for cell in row:
				if(cell):
					num = num + "1"
				else:
					num = num + "0"
		self.rule = num
		#resetting the grid
		for i in range(3):
			for j in range(3):
				self.cells[i][j].setFill("gray92")
				self.log[i][j] = False
		self.cells[1][1].setFill('yellow')
		#adding the rule
		self.rules.append(self.rule)

	#simple function to convert from binary to octal
	def toOctal(self, num):
		result = str(oct(int(num, 2)))
		return int(result[2:])

#    def toBinary(self, oct):
#    	oct = str(oct)
#    	dec = str(int(oct, 8))
#		dec = str(bin(int(dec)))
#		binary = (dec[2:])
#		while(len(binary) < 9):
#			binary = "0" + binary
#		return binary
		

	def erase(self):
		self.graph.clear()

	def shutDown(self):
		self.root.quit()	
