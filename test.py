import threading

def printthread():
	n = 2.0
	x = threading.Timer(2.0, printthread).start()
	print("n sec timer")


printthread()