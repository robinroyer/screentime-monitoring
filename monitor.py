from __future__ import print_function

import pyxhook
import time


def notify_user_activity():
	print (time.time())
	

def kbevent(event):
	global running
	global hookman
	try:
		notify_user_activity()
		if event.Ascii == 32: # space to kill
			unregister_hook_callback(hookman)
			running = False
		else:
			unregister_hook_callback(hookman)
			time.sleep(5)
			hookman = register_hook_callback()
	except Exception as e:
		unregister_hook_callback(hookman)
		time.sleep(5)
		hookman = register_hook_callback()

def unregister_hook_callback(hookman):
	hookman.cancel()

def register_hook_callback():
	#init
	hookman = pyxhook.HookManager()
	#event
	hookman.KeyDown = kbevent
	hookman.KeyUp = kbevent
	hookman.MouseMovement = kbevent
	hookman.MouseAllButtonsUp = kbevent
	hookman.MouseAllButtonsDown = kbevent
	# start & return
	hookman.start()
	return hookman


if __name__ == '__main__':
	hookman = register_hook_callback()

	# Create a loop to keep the application running
	running = True
	while running:
		time.sleep(0.1)

	# Close the listener when we are done (stop the thread)
	unregister_hook_callback(hookman)