# 15-112, Summer 2, Term Project 
######################################
# Full name: Aditya Gupta
# Section: C
# Andrew ID: AdityaG3
######################################



from tkinter import messagebox, simpledialog
from tkinter import *
import math
import string 
from math import * 	
import copy 



#######################################################
# Redefining & defining function from the math module #
#######################################################

# Trig Functions:
sin = lambda x: math.sin(x)
cos = lambda x: math.cos(x)
tan = lambda x: math.tan(x)
sec = lambda x: 1/math.cos(x)
csc = lambda x: 1/math.sin(x)
cot = lambda x: 1/math.tan(x)

# Inverse trig
arcsin = lambda x: math.asin(x)
arccos = lambda x: math.acos(x)
arctan = lambda x: math.atan(x)

# Hyperbolic trig functions
sinh = lambda x: math.sinh(x)
cosh = lambda x: math.cosh(x)
tanh = lambda x: math.tanh(x)

# Inverse of hyperbolic trig functions
arcsinh = lambda x: math.asinh(x)
arccosh = lambda x: math.acosh(x)
arctanh = lambda x: math.atanh(x)

# Logarithmic functions 
ln = lambda x: math.log(x)
log = lambda x, base = 10: math.log(x, base)

# other functions to do with exponents
sqrt = lambda x: math.sqrt(x)
exp = lambda x: math.exp(x)
pow = lambda x, y: math.pow(x,y)

# Misc functions
abs = lambda x: x if x >= 0 else -x



# Superclass to input the function
# has methods to evaluate and get points for function 
class InputFunction(object):
	def __init__(self, funct):
		# the constructor for InputFunction
		self.function = funct.lower()
		self.points = []
		return 
    
    # uses eval() to evaluate the function at a point
	def parseEquation(self, x = None, y = None, z = None):
		try:
			answer = eval(self.function)
			return answer 
		except:
			return None 

	# gets a range of the function 
	def getRange(self, data):
		steps = data.steps
		deltaX = abs(data.xMax - data.xMin)
		deltaY = abs(data.yMax - data.yMin)
		rangeStepX = deltaX/steps
		rangeStepY = deltaY/steps
		result = []
		# double for loop to get range of function
		for step in range(steps+1):
			x = data.xMin + rangeStepX*step
			for ystep in range(steps+1):
				y = data.yMin + rangeStepY*ystep
				result.append(tuple([x, y]))
			y = data.yMin 
		return result 

	# gets the points 
	def getPoints(self, data):
		xyVals = self.getRange(data)
		for tup in xyVals:
			x, y = tup
			# parsing the equation to get z coords 
			z = self.parseEquation(x, y)
			self.points.append(tuple([x, y, z]))
		return self.points



# subclass to render in the function and draws
# the wire mesh pattern
class FunctionRender(InputFunction):
	
	def __init__(self, funct):
		# the constructor for FunctionRender
		InputFunction.__init__(self, funct)
		self.color = ()

	# method to draw the lines
	def draw(self, canvas, data):
		colorLst, countNones = [(0, 0, 255), (0, 255, 0), (255, 0, 0)], 0
		steps, counter = data.steps, 0
		print (data.alpha, data.beta)
		for c in range(len(self.points)-1): # draw half of the wire mesh 
			counter += 1
			# because number of dots = steps + 1
			if((counter)%(steps+1) == 0): continue
			if (self.points[c][2] == None or self.points[counter][2] == None):
				continue
			averageZ = (self.points[c][2] + self.points[counter][2]) / 2
			colorTup = valuetoRGB(averageZ, data.realMinZ, data.realMaxZ, colorLst)
			colorHeat = rgbString(colorTup)
			drawLines(self.points[c], self.points[counter], data, canvas, colorHeat)
		for c in range(len(self.points)-1-steps):# draw other part of wire mesh
			if(self.points[c][2] == None or self.points[c + steps + 1][2] == None):
				continue 
			averageZ = (self.points[c][2] + self.points[c + steps + 1][2])/ 2
			cTup = valuetoRGB(averageZ, data.realMinZ, data.realMaxZ, colorLst)
			colorHeat = rgbString(cTup)
			drawLines(self.points[c], self.points[c + steps + 1], 
				data, canvas, colorHeat)
		if (allNone(self.points)): return 1
		elif (hasNone(self.points)): return 2
		else: return 0



# class for inputting and drawing points
class DataPoints(object):
	
	def __init__(self, lstPoints):
		# the constructor for DataPoints
		self.lstPoints = lstPoints

	def drawPoint(self, data, canvas, x1, y1, color = "Black"):
		# draws the point, with a radius of 3
		r = 3
		canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill = color)
	
	def draw(self, canvas, data):
		# draws all of the points in the list of points
		for p in self.lstPoints:
			x1, y1 = ThreeDtoTwoD(p, data)
			self.drawPoint(data, canvas, x1, y1)


# Based on rgbString from course notes but modified by me
# I used this same modified rgb string on tetris (HW #5)
def rgbString(tup):
    # deals with color tuples 
    (red, green, blue) = tup
    return "#%02x%02x%02x" % (red, green, blue)



# makes heat-map effect by converting a value to a color on RGB
# Citation: modified version of code from:
# https://stackoverflow.com/questions/20792445/calculate-rgb
#-value-for-a-range-of-values-to-create-heat-map
def valuetoRGB(val, minV, maxV, colors):
	# gets ratio to determine color
	if(maxV == minV):
		return (0, 255, 0)
	ratio = float(val - minV) / float(maxV - minV) 
	colorIndex = ratio * (len(colors) - 1)
	intColorIndex = int(colorIndex)
	delta = colorIndex - intColorIndex
	epsilon = 10**-10 # for float comparison 
	if (delta < epsilon):
		return colors[intColorIndex]
	else:
		(r, g, b) = colors[intColorIndex]
		(rNext, gNext, bNext) = colors[intColorIndex + 1]
		colorR = int(r + delta * (rNext-r))
		colorG = int(g + delta * (gNext-g))
		colorB = int(b + delta * (bNext-b))
		return (colorR, colorG, colorB)



# Converts a 3D point to a 2D point, which can be plotted
# Citation: Based on wikipedia article on isometric projections
# link: https://en.wikipedia.org/wiki/Isometric_projection
def ThreeDtoTwoD(ThreeDpoint, data):
	x, y, z = ThreeDpoint
	# origin of graph 
	x0 = data.x0 
	y0 = data.y0
	# scaling to go from actual data to python graph coords
	multX = data.multX
	multY = data.multY
	multZ = data.multZ
	# beta is the horizonatal rotation angle of the camera 
	# alpha is the vertical rotation angle of the camera
	beta, alpha = data.beta, data.alpha
	try:
		# based on the formula referenced above, modified for python axes convention
		x2D = x0 - x * multX * sin(beta) + y * multY * cos(beta)
		y2D = (y0 + x * multX * cos(beta) * sin(alpha) + y * multY 
			* sin(beta) * sin(alpha) - z * multZ * cos(alpha))
		return x2D, y2D
	except:
		return None, None 


# gets the min and max 
def getMinMaxofZ(ThreeDpoints, data):
	if(hasNone(ThreeDpoints)):
		zMin, zMax = 0, 0
	else:
		zMin, zMax = ThreeDpoints[0][2], ThreeDpoints[0][2]
	for pt in ThreeDpoints:
		x, y, z = pt
		try:
			if (z < zMin):
				zMin = z
			elif (z > zMax):
				zMax = z
		except:
			# in the case of potentially comparing z = none
			pass
	maxDist = max(abs(zMin), abs(zMax))
	return (-1*maxDist), maxDist, zMin, zMax 


# updates the z coords 
# this function is used by the drawStringFunc
def updateZ(data, lst):
	# the updating of z coords below 
	data.zMin, data.zMax, data.realMinZ, data.realMaxZ = getMinMaxofZ(lst, data)
	if (abs(data.zMax-data.zMin)>0):
		data.multZ = data.width/(data.zMax - data.zMin) * data.percentOfScreen


# checks if there are points with None values as Zs
# those points should not be on the graph 
def allNone(lst):
	# checks if any of the z coords are none
	for tup in lst:
		if tup[2] == None:
			continue
		else:
			return False
	return True  

def hasNone(lst):
	# checks if any elements of tuples in a list
	# are equal to None
	for tup in lst:
		for elem in tup:
			if elem == None:
				return True
	return False 


def drawLines(p1, p2, data, canvas, color = "Black",):
	# draws lines in 2D by converting from 3D to 2D
	x1, y1 = ThreeDtoTwoD(p1, data)
	x2, y2 = ThreeDtoTwoD(p2, data)
	canvas.create_line(x1, y1, x2, y2, fill = color)


def drawText(p1, data, canvas, msg, colorT, sizeT):
	# draws the text given 3D points 
	x1, y1 = ThreeDtoTwoD(p1, data)
	canvas.create_text(x1, y1, text = msg, fill = colorT, font = ("Arial", sizeT))



# CITATION: Based on barebones for course website, but modified by me
# Link: https://pd43.github.io/notes/notes4-2.html
# MODEL VIEW CONTROLLER (MVC)
####################################
# MODEL:       the data
# VIEW:        redrawAll and its helper functions
# CONTROLLER:  event-handling functions and their helper functions
####################################

# Initialize the data which will be used to draw on the screen.
	# These are the CONTROLLERs.
	# IMPORTANT: CONTROLLER does *not* draw at all!
	# It only modifies data according to the events.

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

	# This is the VIEW
	# IMPORTANT: VIEW does *not* modify data at all!
	# It only draws on the canvas.
def redrawAll(canvas, data):
    # draw in canvas
    # draw parts of the interface
    drawAxes(canvas, data)
    drawUserInterface(canvas, data)
    # draw the function
    try:
    	retVal  = data.f.draw(canvas, data)
    	if (retVal == 1): 
    		throwError(canvas, data)
    	elif (retVal == 2):  # displays warning if some pts out of range
    		displayWarning(canvas, data)
    except:
    	pass
    # draw the points 
    try:
    	data.dataPoints.draw(canvas, data)
    except:
    	pass
  	# draw the statistics part
    drawStats(canvas, data)
    


def drawStats(canvas, data):
	# draws the statistics information that's on the right of the screen
	height, width = data.height, data.width
	StrX = ("Min X: %+4.1f" % data.xMin + "\tMax X:  %+4.1f" 
		% data.xMax) # part for min and max X
	StrY = ("Min Y: %+4.1f" % data.yMin + "\tMax Y:  %+4.1f" 
		% data.yMax) # part for min and max Y
	StrZ = ("Min Z: %+4.1f" % data.realMinZ + "\tMax Z:  %+4.1f" 
		% data.realMaxZ) # part for min and max Z
	canvas.create_text(data.width * 0.85, data.height * 0.76,
		anchor = "c", text = StrX, font = ("Arial", 14),
		fill = "black")
	canvas.create_text(data.width * 0.85, data.height * 0.8,
		anchor = "c", text = StrY, font = ("Arial", 14),
		fill = "black")
	canvas.create_text(data.width * 0.85, data.height * 0.84,
		anchor = "c", text = StrZ, font = ("Arial", 14),
		fill = "black")



   
def displayWarning(canvas, data):
	# displays the warning when some points are out of the range
	width, height = data.width, data.height
	warningMsg = "Some points have not been plotted due to invalid domain"
	canvas.create_text(.83 * width, .18 * height, anchor = "c",
	 text = warningMsg, font = ("Arial", 14), fill = "red")
	


def drawAxes(canvas, data):
	# draws the axes and other of the graphing part
	# first getting the 3D coordinates of min and max values of
	# X Y and Z 
	xTop, xBot, zBot = (data.xMax, 0, 0), (data.xMin, 0, 0), (0, 0, data.zMin)
	yTop, yBot, zTop = (0, data.yMax, 0), (0, data.yMin, 0), (0, 0, data.zMax)
	drawLines(zTop, zBot, data, canvas)
	drawLines(xTop, xBot, data, canvas)
	drawLines(yTop, yBot, data, canvas)
	drawCube(data, canvas)
	labelAxes(data, canvas)
	


def drawCube(data, canvas):
	# define corners of the cube
	topRFCorner, bottomLBCorner = (data.xMax, data.yMax, data.zMax), (data.xMin, data.yMin, data.zMin)
	topRBCorner, bottomRBCorner = (data.xMin, data.yMax, data.zMax), (data.xMin, data.yMax, data.zMin)
	topLBCorner, bottomRFCorner = (data.xMin, data.yMin, data.zMax), (data.xMax, data.yMax, data.zMin)
	topLFCorner, bottomLFCorner = (data.xMax, data.yMin, data.zMax), (data.xMax, data.yMin, data.zMin)

	# draw edges of the cube 
	drawLines(topRFCorner, topRBCorner, data, canvas)
	drawLines(topRFCorner, bottomRFCorner, data, canvas)
	drawLines(topRFCorner, topLFCorner, data, canvas)
	drawLines(bottomLBCorner, bottomLFCorner, data, canvas)
	drawLines(bottomLBCorner, bottomRBCorner, data, canvas)
	drawLines(bottomLBCorner, topLBCorner, data, canvas)
	drawLines(bottomRFCorner, bottomRBCorner, data, canvas)
	drawLines(bottomRFCorner, bottomLFCorner, data, canvas)
	drawLines(topLFCorner, topLBCorner, data, canvas)
	drawLines(topLFCorner, bottomLFCorner, data, canvas)
	drawLines(topRBCorner, bottomRBCorner, data, canvas)
	drawLines(topRBCorner, topLBCorner, data, canvas)
	



def labelAxes(data, canvas):
	# getting coords of relevant part
	xTopH, xBotL = (data.xMax + data.stepSizeX*2, -data.stepSizeY, 0), (data.xMin - data.stepSizeX*2, -data.stepSizeY, 0)
	yTopH, yBotL = (data.stepSizeX, data.yMax + data.stepSizeY*2, 0), (data.stepSizeX, data.yMin - data.stepSizeY*2, 0)
	zTopH, zBotL = (data.stepSizeX, 0, data.zMax + data.stepSizeZ), (data.stepSizeX, 0, data.zMin - data.stepSizeZ)
	xTopR, xBotR = (data.xMax, data.stepSizeY, 0), (data.xMin, data.stepSizeY, 0)
	yTopR, yBotR = (-data.stepSizeX, data.yMax, 0), (-data.stepSizeX, data.yMin, 0)
	zTopR, zBotR = (-data.stepSizeX, 0, data.zMax), (-data.stepSizeX, 0, data.zMin)
	# label the axis X Y and Z
	drawText(xTopH, data, canvas, "X", "Red", 18)
	drawText(yTopH, data, canvas, "Y", "Red", 18)
	drawText(zTopH, data, canvas, "Z", "Red", 18)
	# label mins and maxes on X Y and Z axes
	drawText(xTopR, data, canvas, '%+4.1f'%data.xMax, "black", 12)
	drawText(yTopR, data, canvas, '%+4.1f'%data.yMax, "black", 12)
	drawText(zTopR, data, canvas, '%+4.1f'%data.zMax, "black", 12)
	drawText(xBotR, data, canvas, '%+4.1f'%data.xMin, "black", 12)
	drawText(yBotR, data, canvas, '%+4.1f'%data.yMin, "black", 12)
	drawText(zBotR, data, canvas, '%+4.1f'%data.zMin, "black", 12)

	
 # draws the user interface 
def drawUserInterface(canvas, data):
	# draws the user interface 
	startX = data.width - data.height//1.7
	restX = data.width - startX
	canvas.create_rectangle(startX, 5, data.width, data.height, fill = None, )



# draws the entered function
def drawStringFunc(funct, data, canvas):
	data.f = FunctionRender(str(funct))
	# gets list of the points
	lst = data.f.getPoints(data)
	updateZ(data, lst)
	# then redraws 
	canvas.delete(ALL)
	redrawAll(canvas, data)
	canvas.update()  


def drawPointsFunc(str1, str2, str3, str4, data, canvas):
	#draws the (upto) four points needed
	ptLst = [str1, str2, str3, str4]
	points, lst, count = [], [], 0
	for pt in ptLst:
		if (len(pt) >= 5):
			pt = pt[1:-1]
			print(pt)
			lst, lst2 = pt.split(","), []
			for item in lst:
				num = float(item)
				lst2.append(num)
			lst2 = tuple(lst2)
			points.append(lst2)
	print(points)
	data.dataPoints = DataPoints(points)
	print(data.dataPoints, "I am in drawPointsFunc")
	canvas.delete(ALL)
	redrawAll(canvas, data)
	canvas.update()


# dialog info from here:
# http://www.kosbie.net/cmu/spring-17/15-112/notes/dialogs-demo1.py
def throwError(data, canvas):
	# error dialogue for an invalid function 
	msgPartOne = "This is not a valid function! Please re-enter a valid one.\n"
	message = msgPartOne + "Click the question mark box for help."
	title = "Invalid Function"
	# shows the popup 
	messagebox.showwarning(title, message)
	


def inputUp(data, canvas):
	# for click of the up button 
	data.alpha -= data.alphaShift
	canvas.delete(ALL)
	redrawAll(canvas, data)
	canvas.update()


def inputDown(data, canvas):
	# for click of the down button 
	data.alpha += data.alphaShift
	canvas.delete(ALL)
	redrawAll(canvas, data)
	canvas.update()
	

def inputLeft(data, canvas):
	# for click of the left button 
	data.beta += data.betaShift
	canvas.delete(ALL)
	redrawAll(canvas, data)
	canvas.update()
	

def inputRight(data, canvas):
	# for click of the right button 
	data.beta -= data.betaShift
	canvas.delete(ALL)
	redrawAll(canvas, data)
	canvas.update()
	

def resetGraph(data, canvas):
	# resets the graph if click on the circle/center button
	data.beta = -math.pi/2 + math.pi*2/3 
	data.alpha = math.pi*1/6
	canvas.delete(ALL)
	redrawAll(canvas, data)
	canvas.update()


def startDrag(data, event):
	# starts the dragging
   	data.lastX = event.x
   	data.lastY = event.y
   

def mouseDrag(data, event, canvas):
	# function to make the mouse dragging functionality 
	changeX = event.x - data.lastX
	changeY = event.y - data.lastY
	if (abs(changeX)>=abs(changeY)): # if change in x direction
   		if (changeX > 0): 
   			data.beta -= data.betaShift
   		elif (changeX <0):
   			data.beta += data.betaShift
	else: # if change is y direction 
   		if (changeY > 0): 
   			data.alpha += data.alphaShift
   		elif (changeY <0):
   			data.alpha -= data.alphaShift	
	if (abs(changeX) > 0 or abs(changeY)>0):
   		canvas.delete(ALL)
   		redrawAll(canvas, data)
   		canvas.update()

	

def displayHelp(data, canvas):
	# displays the help dialogue
	msg1 = ("Type the function, in terms of x and y, on the widget on the ")
	msg2 = ("right of the screen. Most functions are accepted. ") 
	msg2a = ("Use pow, exp or ** for exponents and sqrt for square roots. ")
	msg2b = ("You'll be notified about invalid inputs. ")
	msg3 = ("Use the arrow keys to rotate the cube and the center key ")
	msg4 = ("to go back to the orignial position. You can also drag mouse to ")
	msg5 = ("rotate the cube. The function will display min's and max's. Inp")
	msg6 = ("ut points (x, y, z) to see where they lie relative to the curve.")
	msg7 = (" The range for x and y is -10 to +10 in the graph.")
	message = msg1 + msg2 + msg2a + msg2b + msg3 + msg4 + msg5 + msg6 + msg7
	title = "Instructions:"
	messagebox.showinfo(title, message)



def getFunctionInput(root, data, canvas):
	# labels for showing where to enter input
	label1 = Label(root, text="Enter a function of x and y:")
	labelZ = Label(root, text="Z =")
	labelR = Label(root, text="Rotate the Graph:")
	E1 = Entry(root, bd = 1.5)
	# submit the input
	submit = Button(root, text ="Submit", command = lambda: drawStringFunc(str(E1.get()), data, canvas))
	# make the buttons for rotating the graph
	upB = Button(root, text ="⇧", command = lambda: inputUp(data, canvas))
	downB = Button(root, text ="⇩", command = lambda: inputDown(data, canvas))
	leftB = Button(root, text ="⇦", command = lambda: inputLeft(data, canvas))
	rightB = Button(root, text ="⇨", command = lambda: inputRight(data, canvas))
	resetB = Button(root, text ="◎", command = lambda: resetGraph(data, canvas))
	# place those widgets
	label1.place(relx=.85, rely=.04, anchor="c")
	labelZ.place(relx=.77, rely=.07, anchor="c")     
	E1.place(relx=.85, rely=.07, anchor="c") # for eq
	labelR.place(relx=.85, rely=.25, anchor="c") 
	upB.place(relx = 0.85, rely = 0.30, anchor="c")
	downB.place(relx = 0.85, rely = 0.40, anchor="c")
	leftB.place(relx = 0.80, rely = 0.35, anchor="c")
	rightB.place(relx = 0.90, rely = 0.35, anchor="c")
	resetB.place(relx = 0.85, rely = 0.35, anchor="c")
	submit.place(relx=.85, rely=.12, anchor="c")



def getPointInputAndShowStats(root, data, canvas):
	# labels for the point interface
	instructions = Label(root, text="Enter point to graph in form (x, y, z):")
	labelP1 = Label(root, text="Point 1:")
	labelP2 = Label(root, text="Point 2:")
	labelP3 = Label(root, text="Point 3:")
	labelP4 = Label(root, text="Point 4:")
	# place the labels 
	instructions.place(relx=0.85, rely=0.46, anchor="c")
	labelP1.place(relx=0.75, rely=0.5, anchor="c")
	labelP2.place(relx=0.75, rely=0.54, anchor="c")
	labelP3.place(relx=0.75, rely=0.58, anchor="c")
	labelP4.place(relx=0.75, rely=0.62, anchor="c")
	# make the display for the statistics
	titleS = Label(root, text="Statistics:")
	EP1, EP2 = Entry(root, bd = 1.5), Entry(root, bd = 1.5)
	EP3, EP4 = Entry(root, bd = 1.5), Entry(root, bd = 1.5)
	EP1.place(relx=.85, rely=.50, anchor="c")
	EP2.place(relx=.85, rely=.54, anchor="c")
	EP3.place(relx=.85, rely=.58, anchor="c")
	EP4.place(relx=.85, rely=.62, anchor="c")
	titleS.place(relx=.85, rely=.72, anchor="c")
	
	submitPoints = Button(root, text ="Submit Points",
	 command = lambda: drawPointsFunc(str(EP1.get()),
	 str(EP2.get()), str(EP3.get()), str(EP4.get()), data, canvas))
	submitPoints.place(relx=.85, rely=.68, anchor="c") 



# initialize parameters used for graphing
def init(data):
    data.steps = 50
    # percent of screen is effects the size of the graph 
    data.percentOfScreen = 0.3
    #-pi/2 there to adjust for an error caused by just
    # using the formula
    data.beta = -math.pi/2 + math.pi*2/3 
    data.alpha = math.pi*1/6
    data.betaShift = math.pi/12
    data.alphaShift = math.pi/12
    data.x0 = data.height//2
    data.y0 = data.height//2
    data.xMin, data.xMax = -5, 5
    data.yMin, data.yMax = -5, 5
    data.zMin, data.zMax = -5, 5
    data.realMinZ, data.realMaxZ = 0, 0
    data.stepSizeX = (data.xMax - data.xMin)/data.steps
    data.stepSizeY = (data.yMax - data.yMin)/data.steps
    data.stepSizeZ = (data.zMax - data.zMin)/data.steps
    data.multX = data.width/(data.xMax - data.xMin) * data.percentOfScreen
    data.multY = data.width/(data.yMax - data.yMin) * data.percentOfScreen
    data.multZ = data.width/(data.yMax - data.yMin) * data.percentOfScreen #initialize to same as multY
    data.points = []



# run function 
def run(width=300, height=300):

	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	#data.timerDelay = 100 # milliseconds
	init(data)
	root = Tk()
	canvas = Canvas(root, width=data.width, height=data.height)
	# initialize the screen 
	redrawAll(canvas, data)
	# Get the function input:
	getFunctionInput(root, data, canvas)
	# Get point input and show the statistics 
	getPointInputAndShowStats(root, data, canvas)
	# Make the help button
	helpButton = Button(root, text = "?", command = lambda: displayHelp(data, canvas))
	helpButton.place(relx=.94, rely=.06, anchor="c")
	canvas.pack()
	
   	# set up mouse drag events 
	root.bind("<ButtonPress-1>", lambda event: startDrag(data, event))
	root.bind("<ButtonRelease-1>", lambda event: mouseDrag(data, event, canvas))
	root.mainloop()  # blocks until window is closed

	print("bye!")


run(1400, 800)




######################################################################
# Test Cases Below: 
######################################################################



def testAllNone():
	# testing allNone
	print("Testing allNone")
	tup = tuple([1, 2, 3])
	lst = []
	lst.append(tup)
	lst2 = []
	assert(allNone(lst) == False)
	tup2 = tuple([1, 2, None])
	lst.append(tup2)
	assert(allNone(lst) == False)
	tup3 = tuple([None, None, None])
	lst2.append(tup3)
	assert(allNone(lst2) == True)
	print("Passed!")


def testHasNone():
	# testing hasNone
	print("Testing hasNone")
	tup = tuple([1, 2, 3])
	lst = []
	lst.append(tup)
	lst2 = []
	assert(allNone(lst) == False)
	tup2 = tuple([1, 2, None])
	lst.append(tup2)
	assert(hasNone(lst) == True)
	tup3 = tuple([None, None, None])
	lst2.append(tup3)
	assert(hasNone(lst2) == True)

	print("Passed!")


testAllNone()
testHasNone()












