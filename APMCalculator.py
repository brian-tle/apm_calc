import pynput
from pynput.keyboard import Key, Listener as KeyListener
from pynput.mouse import Listener as MouseListener

import threading
import time

import tkinter as tk
from tkinter import Frame, Button, Label

import os.path
from os import path

from datetime import datetime

#Global variables
n = 4.0
actions = 0
mouse_clicks = 0
key_clicks = 0
apm_av = 0
list_apm = []
length = len(list_apm)

start_program = True
cancel_program = False
end_listener = False

time_start = datetime.now()
timestamp = time_start.strftime("%B %d, %Y Started: %H:%M:%S")

#Start program
master = tk.Tk()
master.geometry('350x200+500+300')
master.title('APM Calculator')

frame = Frame(master, width=200, height=600)
frame.pack()

#When a key is pressed
def on_press(key):
	global actions, key_clicks, end_listener
	if end_listener != True:
		actions += 1
		key_clicks += 1
		#print('{0}'.format(key))
	else:
		return False

#When mouse buttons are pressed
def on_click(x, y, button, pressed):
	global actions, mouse_clicks, end_listener
	if end_listener != True:
		if pressed:
			actions += 1
			mouse_clicks += 1
			#print ('Mouse clicked at ({0})'.format(button))
	else:
		return False

#Begins listeners
def start_apm():
	global end_listener
	print("Stream start")
	if end_listener == True:
		return False
	else:
		with MouseListener(on_click=on_click) as listener:
			with KeyListener(on_press=on_press) as listener:
				get_apm()
				listener.join()

#Ends the listener and displays the results
def end_apm():
	global end_listener, cancel_program, start_program
	end_listener = True
	cancel_program = True
	start_program = False
	apm_results()
	return False

#Listens to the keys pressed, adds the amount to a list, displays current, and resets
def get_apm():
	global actions, start_program, end_listener, cancel_program, lbl
	if start_program == True:
		lbl.config(text="Recording! Type away!\nYou will have to wait til the end of the timer for results ):")
		start_program = False
		start_apm()

	if cancel_program == True:
		return False

	while cancel_program != True:
		if end_listener != True:
			master.update()
			time.sleep(n)
			apm = actions
			#Reset actions
			actions = 0

			if apm != 0:
				#Add actions to list
				list_apm.append(apm)
				print("\nAPM: " + str(apm))
				lbl.config(text="APM: " + str(apm))
	else:
		print("\nStream end")
		return False

#Displays the results from the recording
def apm_results():
	global start_program, list_apm, apm_av, mouse_clicks, key_clicks, lbl
	start_program = False
	add_apm = 0

	#Values have to exist for calculations
	length = len(list_apm)
	if length != 0:
		for values in list_apm:
			add_apm += values

		length = len(list_apm)
		apm_av = str(round(add_apm / length, 2))
		min_apm = str(min(list_apm))
		max_apm = str(max(list_apm))

		# print("\nTotal Key: " + str(key_clicks) + " | Total Mouse: " + str(mouse_clicks) + " | Total Actionss: " +  str(key_clicks + mouse_clicks))
		# print("Min APM: " + min_apm)
		# print("Max APM: " + max_apm)
		# print("Average APM: " + apm_av)
		# print("Minutes recorded: " + str(length))
		a = "\nTotal Key: " + str(key_clicks) + " | Total Mouse: " + str(mouse_clicks) + " | Total Clicks: " + str(key_clicks + mouse_clicks)
		b = "\nMin APM: " + min_apm
		c = "\nMax APM: " + max_apm
		d = "\nAverage APM: " + apm_av
		e = "\nMinutes recorded: " + str(length)
		result_string = a + b + c + d + e

		lbl.config(text=result_string)

		saveButton = Button(frame, text="Save", command=save_results(result_string))
		saveButton.pack(side=tk.LEFT, padx=10)
		return False
	else:
		lbl.config(text="No values were recorded")

#Option to save the results to a file
def save_results(res):
	global timestamp

	get_time = datetime.now()
	timestamp = get_time.strftime("%B %d, %Y Started: %H:%M:%S")

	if (path.exists("apm_log.txt")):
		#a to write to existing file
		with open("apm_log.txt", "a") as f:
			f.write('\n====================\n')
			f.write(timestamp)
			f.write(res)
			f.write('\n====================\n')
	else:
		#w to create then write
		with open("apm_log.txt", "w") as f:
			f.write('\n====================\n')
			f.write(timestamp)
			f.write(res)
			f.write('\n====================\n')

# def reset_values():
# 	global lbl, actions, mouse_clicks, key_clicks, list_apm, cancel_program, apm_av, start_program
# 	actions = 0
# 	mouse_clicks = 0
# 	key_clicks = 0
# 	list_apm = []
# 	cancel_program = False
# 	apm_av = 0
# 	start_program = True
# 	lbl.config(text="Values reset")
# 	print("\n\n\n\n\n\n\n")

startButton = Button(frame, text="Start", command=get_apm)
startButton.pack(side=tk.LEFT)
quitButton = Button(frame, text="Stop", command=end_apm)
quitButton.pack(side=tk.LEFT)

lbl = Label(master)
lbl.pack()

master.mainloop()
