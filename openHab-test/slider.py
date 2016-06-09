import uinput
import time

device = uinput.Device([
	uinput.KEY_LEFT,
	uinput.KEY_RIGHT
	])

if __name__ == "__main__":
	device.emit_click(uinput.KEY_RIGHT)
	
