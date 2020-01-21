import pynput
from pynput.keyboard import Key, Listener as KeyListener
from pynput.mouse import Listener as MouseListener

import threading
import time

import tkinter as tk
from tkinter import Frame, Button, Label

#global
actions = 0
mouse_clicks = 0
key_clicks = 0
list_apm = []
n = 4.0
cancel_thread = False
apm_av = 0
start_program = True
end_listener = False
length = len(list_apm)

master = tk.Tk()
master.geometry('350x200+500+300')
master.title('APM Calculator')

frame = Frame(master, width=200, height=600)
frame.pack()

#When a key is pressed
def on_press(key):
	global actions, key_clicks, end_listener
	actions += 1
	key_clicks += 1
	print('{0}'.format(key))
	if end_listener == True:
		return False

#When mouse buttons are pressed
def on_click(x, y, button, pressed):
	global actions, mouse_clicks, end_listener
	if pressed:
		actions += 1
		mouse_clicks += 1
		print ('Mouse clicked at ({0})'.format(button))

	if end_listener == True:
		return False

def start_apm():
	with MouseListener(on_click=on_click) as listener:
		with KeyListener(on_press=on_press) as listener:
			get_apm()
			listener.join()

#Temporary termination
def end_apm():
	global cancel_thread, start_program, end_listener
	cancel_thread = True
	end_listener = True
	start_program = False
	apm_results()
	return False

def get_apm():
	global actions, cancel_thread, lbl, start_program
	if start_program == True:
		lbl.config(text="Starting! Type away!")
		start_program = False
		start_apm()

	while cancel_thread == False:
		master.update()
		time.sleep(2)
		apm = actions
		# list_apm.append(apm)
		actions = 0

		if apm != 0:
			list_apm.append(apm)
			print("\nAPM: " + str(apm))
			lbl.config(text="APM: " + str(apm))
	else:
		print("end stream")

def apm_results():
	global list_apm, apm_av, mouse_clicks, key_clicks, start_program, lbl
	start_program = False
	add_apm = 0

	for values in list_apm:
		add_apm += values

	length = len(list_apm)
	if length != 0:
		#list_apm.remove(0)
		length = len(list_apm)
		apm_av = str(round(add_apm / length, 2))
		min_apm = str(min(list_apm))
		max_apm = str(max(list_apm))

		print("\nTotal Key: " + str(key_clicks) + " | Total Mouse: " + str(mouse_clicks) + " | Total Clicks: " +  str(key_clicks + mouse_clicks))
		print("Min APM: " + min_apm)
		print("Max APM: " + max_apm)
		print("Average APM: " + apm_av)
		print("Minutes recorded: " + str(length))
		a = "\nTotal Key: " + str(key_clicks) + " | Total Mouse: " + str(mouse_clicks) + " | Total Clicks: " + str(key_clicks + mouse_clicks)
		b = "\nMin APM: " + min_apm
		c = "\nMax APM: " + max_apm
		d = "\nAverage APM: " + apm_av
		e = "\nMinutes recorded: " + str(length)

		lbl.config(text= a + b + c + d + e)
	else:
		lbl.config(text="No values recorded")

# def reset_values():
# 	global lbl, actions, mouse_clicks, key_clicks, list_apm, cancel_thread, apm_av, start_program
# 	actions = 0
# 	mouse_clicks = 0
# 	key_clicks = 0
# 	list_apm = []
# 	cancel_thread = False
# 	apm_av = 0
# 	start_program = True
# 	lbl.config(text="Values reset")
# 	print("\n\n\n\n\n\n\n")

#thread_apm = threading.Thread(target=get_apm)

startButton = Button(frame, text="Start", command=get_apm)
startButton.pack(side=tk.LEFT)
quitButton = Button(frame, text="Stop", command=end_apm)
quitButton.pack(side=tk.LEFT)

lbl = Label(master)
lbl.pack()

master.mainloop()