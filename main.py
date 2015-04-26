import os
import psutil
import fuckit
import win32process
import win32process as process
import win32gui
import sys
import win32con
import ctypes

vol_pid = 0

# Find process ID of Volume Mixer
for pid in psutil.pids():
	with fuckit:
		if psutil.Process(pid).name() == 'SndVol.exe':
			vol_pid = pid
			print 'Found Volume Mixer @ ' + str(vol_pid)



def GetText(hwnd):
    buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
    buffer = win32gui.PyMakeBuffer(buf_size)
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buffer)
    return buffer[:buf_size]

# while True:
# 	print GetText(2165752)

vol_hwnd = 0

def enumHandler(hwnd, lParam):
	global vol_hwnd
	if win32gui.IsWindowVisible(hwnd):
	 if vol_pid in win32process.GetWindowThreadProcessId(hwnd):
		vol_hwnd = hwnd
		print 'Found Volume Mixer window @ ' + str(vol_hwnd)
		print GetText(vol_hwnd)

def childHandler(hwnd, param):
	print GetText(hwnd)
	#print hwnd

win32gui.EnumWindows(enumHandler, None)
win32gui.EnumChildWindows(vol_hwnd, childHandler, None)

#print win32gui.GetClassName(1904276)

# def windowEnumerationHandler(hwnd, resultList):
#     resultList.append((hwnd, win32gui.GetWindowText(hwnd), getClassName(hwnd)))

# def getClassName(hwnd):
# 	resultString = ctypes.c_string("\000" * 32)
# 	ctypes.windll.user32.GetClassNameA(hwnd, resultString, len(resultString))
# 	return resultString.value

# def findTopWindow(wantedText=None, wantedClass=None):
#     topWindows = []
#     win32gui.EnumWindows(windowEnumerationHandler, topWindows)
#     for hwnd, windowText, windowClass in topWindows:
#         if wantedText and not windowText.startswith(wantedText):
#             continue
#         if wantedClass and not windowClass == wantedClass:
#             continue
#         return hwnd

# def findControl(topHwnd, selectionFunction):

#     def searchChildWindows(currentHwnd):

#         childWindows = []

#         try:

#             win32gui.EnumChildWindows(currentHwnd, windowEnumerationHandler, childWindows)

#         except win32gui.error, exception:

#             # This seems to mean that the control does *cannot* have child windows

#             return

#         for childHwnd, windowText, windowClass in childWindows:

#             # print "Found ", childHwnd, windowText, windowClass

#             if selectionFunction(childHwnd, windowText, windowClass):

#                 return childHwnd

#             else:

#                 descendentMatchingHwnd = searchChildWindows(childHwnd)

#                 if descendentMatchingHwnd:

#                     return descendentMatchingHwnd

#         return

#     return searchChildWindows(topHwnd)

    

# topWindows = []
# win32gui.EnumWindows(windowEnumerationHandler, topWindows)


# def enumHandler(hwnd, lParam):
#     if win32gui.IsWindowVisible(hwnd):
#         if 'Stack Overflow' in win32gui.GetWindowText(hwnd):
# 			win32gui.MoveWindow(hwnd, 0, 0, 760, 500, True)
# 			buffer = win32gui.PyMakeBuffer(20)
# 			length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, 20, buffer)
# 			result = buffer[:length]
# 			print result

# 			win32gui.EnumChildWindows(hwnd,childHandler,None)

# def childHandler(hwnd, lParam):
# 	buffer = win32gui.PyMakeBuffer(20)
# 	length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, 20, buffer)
# 	result = buffer[:length]
# 	print result

# win32gui.EnumWindows(enumHandler, None)
# MAIN_HWND = 0

# def is_win_ok(hwnd, starttext):
#     s = win32gui.GetWindowText(hwnd)
#     if s.startswith(starttext):
#             print s
#             global MAIN_HWND
#             MAIN_HWND = hwnd
#             return None
#     return 1


# def find_main_window(starttxt):
#     global MAIN_HWND
#     win32gui.EnumChildWindows(0, is_win_ok, starttxt)
#     return MAIN_HWND


# def winfun(hwnd, lparam):
#     s = win32gui.GetWindowText(hwnd)
#     if len(s) > 3:
#         print("winfun, child_hwnd: %d   txt: %s" % (hwnd, s))
#     return 1

# def main():
# 	hwnd = 1838204
# 	print hwnd
# 	if hwnd < 1:
# 	    hwnd = find_main_window(main_app)
# 	print hwnd
# 	if hwnd:
# 	    win32gui.EnumChildWindows(hwnd, winfun, None)

# main()

# #for i in range(1, 100):
    #os.system('nircmd changeappvolume Firefox.exe -0.05')
			#for pid in processes:
				#print pid
				#if not 'iTunes.exe' in pid:
					#print pid
					#os.system('nircmd changeappvolume ' + pid + ' -0.05'

#def callback(hwnd, procid):
    #if procid in  win32process.GetWindowThreadProcessId(hwnd):
       #w win32gui.SetForegroundWindow(hwnd)

# procid = raw_input()
# win32gui.EnumWindows(callback, procid)

# PORTABLE_APPLICATION_LOCATION = "C:\\Windows\\system32\\notepad.exe"
# processHandler = -1

# def get_hwnds_for_pid (pid):
#   def callback (hwnd, hwnds):
# 	found_pid = win32process.GetWindowThreadProcessId(hwnd)
# 	if found_pid == pid:
# 		hwnds.append (hwnd)
# 	return True
    
#   hwnds = []
#   win32gui.EnumWindows (callback, hwnds)
#   return hwnds

  
# for hwnd in get_hwnds_for_pid (raw_input()):
#     print hwnd, "=>", win32gui.GetWindowText (hwnd)
#     win32gui.SendMessage (hwnd, win32con.WM_CLOSE, 0, 0)


# def show_window_by_process(procid):
#     win32gui.EnumWindows(callback, procid)


# def runProgram():
#     global processHandler
#     #don't run a process more than once
#     if (isLiveProcess(processHandler)):
#         #Bring focus back to running window!
#         show_window_by_process(processHandler)
#         return;
#     try:
#         startObj = process.STARTUPINFO()
#         myProcessTuple = process.CreateProcess(PORTABLE_APPLICATION_LOCATION,None,None,None,8,8,None,None,startObj)
#         processHandler = myProcessTuple[2]
#     except:
#         print(sys.exc_info[0])

# def isLiveProcess(processHandler): #Process handler is dwProcessId
#     processList = process.EnumProcesses()
#     for aProcess in processList:
#         if (aProcess == processHandler):
#             return True
#     return False

#runProgram()