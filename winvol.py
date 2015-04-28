import time
import subprocess
import psutil
import win32process
import win32gui
import win32con
import fuckit

class WinVol:
	verbose = False
	vol_pid = 0
	vol_hwnd = 0
	vol_ready = False
	vol_close = False

	application_captions = []
	mixer_captions = []
	playing_sound = []

	def enumHandler(self, hwnd, param):
		# Saving window titles and PIDs so we can compare those to the sound mixer
		self.application_captions.append([win32gui.GetWindowText(hwnd),win32process.GetWindowThreadProcessId(hwnd)[1]])

		if self.vol_pid == win32process.GetWindowThreadProcessId(hwnd)[1]:
			if win32gui.GetClassName(hwnd) == '#32770':
				self.vol_hwnd = hwnd
				if self.verbose:
					print('Found volume mixer window @ ' + str(self.vol_hwnd))

	def childHandler_Wait(self, hwnd, param):
		if win32gui.GetWindowText(hwnd).replace('\x00','') == 'System Sounds':
			self.vol_ready = True

	def childHandler(self, hwnd, param):
		if win32gui.GetClassName(hwnd) == 'Static':
			if not win32gui.GetWindowText(hwnd).replace('\x00','') == '':
				# This works because there's an ugly other window object that runs hidden and I have no idea what it's for. http://i.imgur.com/FWF35EL.png (shown behind icons)
				if (win32gui.GetWindowRect(hwnd)[2] - win32gui.GetWindowRect(hwnd)[0]) == 102:
					self.mixer_captions.append(win32gui.GetWindowText(hwnd))

	def audible(self, verbose = False):
		self.verbose = verbose

		# Find process ID of volume mixer
		for pid in psutil.pids():
			# Access gets denied when iterating some processes. Fuck it.
			with fuckit:
				if psutil.Process(pid).name() == 'SndVol.exe':
					self.vol_pid = pid
					if verbose:
						print('Found volume mixer @ ' + str(self.vol_pid))

		# http://stackoverflow.com/a/7006424
		# Opens the volume mixer silently
		if self.vol_pid == 0:
			self.vol_close = True
			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			vol = subprocess.Popen('sndvol', startupinfo=si)
			# For some reason this fixes when the module can't spit out a PID fast enough
			time.sleep(0.1)
			self.vol_pid = vol.pid
			if verbose:
				print('Opening volume mixer silently @ ' + str(self.vol_pid))

		# Looks through all windows searching for volume mixer window
		win32gui.EnumWindows(self.enumHandler, None)

		while self.vol_ready == False:
			# Scans volume mixer window until applications are found
			win32gui.EnumChildWindows(self.vol_hwnd, self.childHandler_Wait, None)

		# Grabs applications found in the volume mixer window
		win32gui.EnumChildWindows(self.vol_hwnd, self.childHandler, None)

		# Compares window captions to PIDs and tuples them.
		for appcap in self.application_captions:
			for mixcap in self.mixer_captions:
				if mixcap in appcap[0]:
					self.playing_sound.append([appcap[0],psutil.Process(appcap[1]).name()])

		# Terminates the volume mixer if it was opened by WinVol, so the user doesn't try to open an invisible window
		if self.vol_close:
			subprocess.call('taskkill /F /IM sndvol.exe', creationflags=0x08000000)
			if verbose:
				print('Volume mixer closed')

		return self.playing_sound