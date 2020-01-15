import pynput
from pynput.keyboard import Key, Listener as KeyListener
from pynput.mouse import Listener as MouseListener

import threading
import time

#global
actions = 0
list_apm = []
n = 5.0
cancel_thread = False
apm_av = 0

#When a key is pressed
def on_press(key):
	global actions

	actions += 1
	#print('{0}'.format(key))

#Temporary termination
def on_release(key):
	global actions, cancel_thread
	if key == Key.esc:
		actions -= 1
		cancel_thread = True
		return False

#When mouse buttons are pressed
def on_click(x, y, button, pressed):
	global actions
	if pressed:
		actions += 1
		#print ('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def get_apm():
	global actions, cancel_thread, list_apm
	#Every n seconds, calculate apm
	thread_apm = threading.Timer(n, get_apm)
	if cancel_thread == False:
		thread_apm.start()

		apm = actions
		list_apm.append(apm)
		actions = 0

		print("\nAPM: " + str(apm))
	elif cancel_thread == True:
		thread_apm.cancel()

def apm_results():
	global list_apm, apm_av
	list_apm.remove(0)
	length = len(list_apm)
	add_apm = 0

	for values in list_apm:
		add_apm += values

	apm_av = add_apm / length

	min_apm = str(min(list_apm))
	max_apm = str(max(list_apm))
	print("Min APM: " + min_apm)
	print("Max APM: " + max_apm)
	print(apm_av)

# Collect events until released
with MouseListener(on_click=on_click) as listener:
	with KeyListener(on_press=on_press, on_release=on_release) as listener:
		get_apm()
		listener.join()

apm_results()