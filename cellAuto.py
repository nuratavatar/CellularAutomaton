import graphics
import math

def makeGrid(res, numCells):

	#defaults resolutions lower than 300 pixels to 300 pixels
	if(res < 300):
		print("resolution defaulted to 300x300")
		res = 300
	if(res > 1000):
		print("resolution defaulted to 1000,1000")
		res = 1000

	#rounds resolution to hundreds digit
	res -= res%100

	#Creates graphwindow with resolution of res pixels by res pixels and sets easy to work with coordinates
	grid = graphics.GraphWin("caGrid", res, res, autoflush = False)
	grid.setCoords(0, 0, numCells, numCells)
	grid.setBackground('gray92')

	#list to hold rectangle objects that make up the grid
	gridSq = []
	#holds all the logic behind the grid
	logic = []

	#populating our lists and drawing our grid
	for i in range(numCells):
		gridSq.append([])
		logic.append([])
		for j in range(numCells):
			#add a Rectangle graphics object with sidelength 1 to the current row in the grid
			gridSq[i].append(graphics.Rectangle(graphics.Point(i+ 2*numCells/res, j - 2*numCells/res), graphics.Point(i+1 + 2*numCells/res, j+ 1 - 2*numCells/res)))
			gridSq[i][j].draw(grid)

			#filling out the logic array
			logic[i].append(False)

	#toggle the square if it is clicked
	while(1):
		#get the coordinates of the click
		click = grid.getMouse()
		#we can round the coordinates
		x = int(click.getX())
		y = int(click.getY())
		logic[x][y] = not logic[x][y]
		if(logic[x][y]):
			gridSq[x][y].setFill('magenta')
		else:
			gridSq[x][y].setFill('gray92')

def getRule():
	#Creating a graph window where the user can choose their ruleset
	nHood = graphics.GraphWin('Rule Chooser', 300, 300, autoflush = False)
	nHood.setCoords(0, 0, 3, 3)

	cells = []
	logic = []
	#Drawing the neighborhood
	for i in range(0, 3):
		cells.append([])
		logic.append([])
		for j in range(0, 3):
			#drawing squares and stuff
			cells[i].append(graphics.Rectangle(graphics.Point(i+1/50, j-1/50), graphics.Point(i+1+1/50, j+1-1/50)))
			cells[i][j].draw(nHood)
			#filling out the logic array
			logic[i].append(False)
	cells[1][1].setFill('yellow')
	while(1):	
		click = nHood.getMouse()
		x = int(click.getX())
		y = int(click.getY())
		if(x == 1 and y == 1):
			num = ''
			for row in logic:
				for cell in row:
					if(cell):
						num = num + "1"
					else:
						num = num + "0"

			return toOctal(num)
		else:
			cells[x][y].setFill('magenta')
			logic[x][y] = True
	for row in cells:
		digit = row[0]

#simple function to convert from binary to octal
def toOctal(num):
	result = str(oct(int(num, 2)))
	return int(result[2:])
def toBinary(oct):
	oct = str(oct)
	dec = str(int(oct, 8))
	dec = str(bin(int(dec)))
	binary = (dec[2:])
	while(len(binary) < 9):
		binary = "0" + binary
	return binary
	


#print(getRule())
#makeGrid(500, 43)
print(toBinary(751))
