## FileMaker Import Log Watcher
## (fmp_import_watch)

#### Created by Simon Brown
#### First public version February 2, 2014

### PURPOSE

When the FileMaker Pro client imports scripts, layouts, or schema items it will create entries in a file in the user's Documents folder. This system will monitor the log changes, and create Notification Center alerts when there are new errors.

**Note however that when working on local (non-hosted) there is no fixed position for the Import.log file, so these events are not monitored.**

### REQUIREMENTS

Mac OS 10.8 is required for User Notifications feature. One feature, the clearing of old notifications when using the Alert style, requires Mac OS 10.9.

### INSTALLATION

There are two parts, the launchd .plist that sets up the monitoring of changes to the Import.log, and a script file.

The com.sibr.fmp_import_watch.plist must be installed inside ~/Library/LaunchAgents (where the tilde indicates your home directory).

The Python script, fmp_import_watcher.py should be installed inside ~/Library/Application Support/

Log out & back in to load it, make this happen immediately by running this command in Terminal:

> launchctl load ~/Library/LaunchAgents/com.sibr.fmp_import_watch.plist

### LOGGING

Information may be logged to two files, both in /tmp:

* /tmp/fmp_import_watch.log
* /tmp/fmp_import_watch_err.log

