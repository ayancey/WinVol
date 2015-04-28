# WinVol
This slick module gives you a list of all running windows playing sound and their executable name. It uses the pywin32 and win32gui modules by the great and powerful Mark Hammond.

# WinFadr
![](http://i.imgur.com/KWED7ZJ.gif)

WinFadr is the reason I made this module. It allows you to crossfade all running apps out while fading in the application you're focused on, and vice versa. Repo coming soon.

# Requirements
* Python 2.7+
* [psutil](https://github.com/giampaolo/psutil)
* [pywin32](http://sourceforge.net/projects/pywin32)
* [fuckit](https://github.com/ajalt/fuckitpy)
* Windows Vista or higher I think

# Example
```python
from winvol import WinVol

for apps in WinVol().audible():
	print(apps[0].decode('ascii', 'ignore') + " running on " + apps[1])
```

![](http://i.imgur.com/PVVrio4.png)
