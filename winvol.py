import time
import subprocess
import psutil
import win32process
import win32gui
import win32con
import fuckit

vol_pid = 0
vol_hwnd = 0
vol_ready = False
vol_close = False

application_captions = []
mixer_captions = []
playing_sound = []

# Find process ID of volume mixer
for pid in psutil.pids():
	# Access gets denied when iterating some processes. Fuck it.
	with fuckit:
		if psutil.Process(pid).name() == 'SndVol.exe':
			vol_pid = pid
			print 'Found volume mixer @ ' + str(vol_pid)

# http://stackoverflow.com/a/7006424
# Opens the volume mixer silently
if vol_pid == 0:
	vol_close = True
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	vol = subprocess.Popen('sndvol', startupinfo=si)
	# For some reason this fixes when the module can't spit out a PID fast enough
	time.sleep(0.1)
	vol_pid = vol.pid
	print 'Opening volume mixer silently @ ' + str(vol_pid)

# http://stackoverflow.com/a/4427960
def GetText(hwnd):
    buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
    buffer = win32gui.PyMakeBuffer(buf_size)
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buffer)
    return buffer[:buf_size]

def enumHandler(hwnd, param):
	global vol_hwnd
	application_captions.append([GetText(hwnd),win32process.GetWindowThreadProcessId(hwnd)[1]])
	if vol_pid == win32process.GetWindowThreadProcessId(hwnd)[1]:
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
				mixer_captions.append(GetText(hwnd))
				#application_captions.append(GetText(hwnd))

# Looks through all windows searching for volume mixer window
win32gui.EnumWindows(enumHandler, None)

while vol_ready == False:
	# Scans volume mixer window until applications are found
	win32gui.EnumChildWindows(vol_hwnd, childHandler_Wait, None)

# Grabs applications found in the volume mixer window
win32gui.EnumChildWindows(vol_hwnd, childHandler, None)

# Compares window captions to PIDs and tuples them.
for appcap in application_captions:
	for mixcap in mixer_captions:
		if mixcap in appcap[0]:
			playing_sound.append([appcap[0],psutil.Process(appcap[1]).name()])

# Terminates the volume mixer if it was opened by WinVol, so the user doesn't try to open an invisible window
if vol_close:
	subprocess.call('taskkill /F /IM sndvol.exe', creationflags=0x08000000)

for stuff in playing_sound:
	print stuff[1]

