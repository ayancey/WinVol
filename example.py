from winvol import WinVol

for apps in WinVol().audible():
	print(apps[0].decode('ascii', 'ignore') + " running on " + apps[1])