FileMaker Import Log Watcher
(fmp_import_watch)

Created by Simon Brown
Initial public version February 2, 2014

PURPOSE

When the FileMaker Pro client imports scripts, layouts, or schema items it will create entries in a file in the user's Documents folder. This system will monitor the log changes, and create Notification Center alerts when there are new errors.

INSTALLATION

There are two parts, the launchd .plist that has the system call the Python script when the Import.log file was changed. The com.sibr.fmp_import_watch.plist must be installed inside ~/Library/LaunchAgents (where the tilde indicates your home directory).

The Python script, fmp_import_watcher.py should be installed inside ~/Library/Application Support/

:ogging out & back in should load it. Or, do this in Terminal:

> launchctl load ~/Library/LaunchAgents/com.sibr.fmp_import_watch.plist

