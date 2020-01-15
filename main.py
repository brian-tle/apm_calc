import pynput
from pynput.keyboard import Key, Listener as KeyListener
from pynput.mouse import Listener as MouseListener

import threading
import time

#global
actions = 0
av_apm = []
n = 2.0
cancel_thread = False

#When a key is pressed
def on_press(key):
	global actions

	actions += 1
	print('{0}'.format(key))

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
		print ('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def average_apm():
	global actions, cancel_thread
	#Every n seconds, calculate apm
	thread_apm = threading.Timer(n, average_apm)
	thread_apm.start()

	apm = actions / n
	actions = 0

	print("\nAPM: " + str(apm) + "\n")
	if cancel_thread == True:
		thread_apm.cancel()

# # Collect events until released
with MouseListener(on_click=on_click) as listener:
	with KeyListener(on_press=on_press, on_release=on_release) as listener:
		average_apm()
		listener.join()
		print(actions)