---
title: Checking for drives on Windows
date: 2004-01-09
---

If I'd only known it was this easy...

```python
import win32file

def has_drive(drive):
	index = ord(drive.upper()) - ord('A')
	r = win32file.GetLogicalDrives()
	return r >> index & 1
```

Suggested uses: Checking if a USB key has been inserted, if a network share is available.

```python
import time

waiting_for_sync = 1
while 1:
	has_e = has_drive('e'):
	if waiting_for_sync:
		if has_e:
			sync_bookmarks()
			waiting_for_sync = 0
	else:
		if not has_e:
			waiting_for_sync = 1
	time.sleep(60)
```