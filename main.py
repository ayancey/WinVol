import os
import psutil
import fuckit
import win32process
import win32process as process
import win32gui
import sys
import win32con
import ctypes
import subprocess

# http://stackoverflow.com/a/7006424
# Opens the volume mixer silently
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
subprocess.Popen('sndvol', startupinfo=si)

vol_pid = 0
vol_hwnd = 0
vol_ready = False

# Find process ID of volume mixer
for pid in psutil.pids():
	# Access gets denied when iterating some processes. Fuck it.
	with fuckit:
		if psutil.Process(pid).name() == 'SndVol.exe':
			vol_pid = pid
			print 'Found volume mixer @ ' + str(vol_pid)

# http://stackoverflow.com/a/4427960
def GetText(hwnd):
    buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
    buffer = win32gui.PyMakeBuffer(buf_size)
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buffer)
    return buffer[:buf_size]

def enumHandler(hwnd, lParam):
	global vol_hwnd
	if vol_pid in win32process.GetWindowThreadProcessId(hwnd):
		if win32gui.GetClassName(hwnd) == '#32770':
			vol_hwnd = hwnd
			print 'Found volume mixer window @ ' + str(vol_hwnd)

def childHandler_Wait(hwnd, param):
	global vol_ready
	if GetText(hwnd).replace('\x00','') == 'System Sounds':
		vol_ready = True

def childHandler(hwnd, param):
	if win32gui.GetClassName(hwnd) == 'Static':
		if not GetText(hwnd).replace('\x00','') == '':
			# This works because there's an ugly other window object that runs hidden and I have no idea what it's for. http://i.imgur.com/FWF35EL.png (shown behind icons)
			if (win32gui.GetWindowRect(hwnd)[2] - win32gui.GetWindowRect(hwnd)[0]) == 102:
				print GetText(hwnd)

win32gui.EnumWindows(enumHandler, None)

while vol_ready == False:
	win32gui.EnumChildWindows(vol_hwnd, childHandler_Wait, None)

win32gui.EnumChildWindows(vol_hwnd, childHandler, None)

# Terminates the volume mixer so the user doesn't try to open an invisible window
subprocess.call('taskkill /F /IM sndvol.exe', creationflags=0x08000000)