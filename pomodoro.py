#!/usr/bin/python
from phue import Bridge
import random
import time
import winsound, sys
from graphics import *

b = Bridge('192.168.1.112') # Enter bridge IP here.

#If running for the first time, press button on bridge and run with b.connect() uncommented
b.connect()
lights = b.get_light_objects()
desk = [lights[0], lights[1]]
colormaps = {'green':[0, 1], 'red':[1, 0]}

def newMessage(win, xOffset, yOffset, textSize = 10):
	message = Text(Point(win.getWidth()/2 + xOffset, win.getHeight()/2 + yOffset),'')
	message.setSize(textSize)
	return message

def displayTime(remaining):
	def fmt(num):
		if num < 10:
			return "0" + str(num)
		return str(num)

	return fmt(remaining // 60) + ':' + fmt(remaining % 60)

class Pomodoro(object):
	def __init__(self, studyTime, breakTime, studyLights=desk):
		self.studyTime = studyTime
		self.breakTime = breakTime
		self.lights = studyLights
		self.win = GraphWin('Pomodoro', 250, 50)
		self.topMessage = newMessage(self.win, 0, -10)
		self.botMessage = newMessage(self.win, 0, 10)
		self.topMessage.draw(self.win)
		self.botMessage.draw(self.win)
		self.counter = 0

	def countdownTime(self, status, mins):
		secs = int(mins * 60)
		start = int(time.clock())
		remaining = secs
		self.topMessage.setText("Counter: {0}    ".format(self.counter))
		while remaining > 0:
			remaining = secs + start - int(time.clock())
			fmt_time = displayTime(remaining)
			self.botMessage.setText("{0} {1} \r".format(status, fmt_time))
			self.win.setTitle("{0} Pomodoro".format(fmt_time))
			time.sleep(.1)
			if self.win.checkMouse():
				self.win.close()

	def changeColor(self, color):
		for light in self.lights:
			light.xy = colormaps[color]

	def playChime(self):
		sys.stdout.write("\a\r")
		sys.stdout.flush()

	def study(self):
		self.win.setBackground('red')
		self.changeColor('red')
		self.countdownTime('STUDY NOW. Break in', self.studyTime)

	def takeBreak(self):
		self.win.setBackground('green')
		self.changeColor('green')
		self.countdownTime('Break now. Study in', self.breakTime)

	def initializeLights(self):
		for light in self.lights:
			light.transitiontime = 4
			light.brightness = 255

	def main(self):
		self.initializeLights()
		while True:
			self.playChime()
			self.study()
			self.counter += 1
			self.playChime()
			self.takeBreak()

if __name__ == "__main__":
	print('\nEnter work times or press enter for default times: 25:00 study, 5:00 break.')
	studyTime = 25
	breakTime = 5
	try:
		studyTime = float(input("  Study Time (min): "))
		breakTime = float(input("  Break Time (min): "))
	except:
		pass

	curr_pomo = Pomodoro(studyTime, breakTime)
	curr_pomo.main()




