A Python script that transforms an Xbox gamepad into a full mouse replacement, allowing you to control your cursor without touching a physical mouse.

Note: All button names (A, B, LB, Select) refer to the Xbox controller layout!

## How It Works:
The script uses pygame to read gamepad input and pyautogui to translate that input into mouse actions on your system. It runs in a continuous loop, checking the gamepad state 120 times per second for smooth, responsive control.
## Installation!!!(NECESSARY):
Open Powershell and Install pygame and pyautogui in the script folder:
	cd "path/to/the/folder" (like C:\Users\Desktop\CursorForGamepad)
	pip install pygame pyautogui
	python cursor.py

## Features:
* Cursor Mode Toggle:
	Select/View button — switches cursor control on and off
	When disabled, the gamepad stops controlling the mouse, so you can use the controller normally without interference

* Smooth Cursor Movement:
	Left stick — moves the mouse cursor
	Uses a non-linear response curve: small stick movements give precise control, while pushing the stick further increases speed
	Includes a deadzone to prevent cursor drift from stick imprecision
	Floating-point position tracking ensures fluid, pixel-accurate movement

* Page Scrolling:
	Right stick (vertical axis) — scrolls up and down
	Same smooth acceleration curve as cursor movement
	Automatically disabled during text selection to avoid conflicting gestures

* Click Actions:
	A button — left click
	B button — right click (opens context menus)

* Text Selection:
	LB (hold) — simulates holding the left mouse button down
	Move the left stick while holding LB to select text, drag files, etc.
	Release LB to finish the selection
	Scrolling and clicking are automatically disabled while dragging to prevent accidental interruptions

Also free to change settings for yourself!
