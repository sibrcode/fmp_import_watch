## FileMaker Import Log Watcher
#### (fmp_import_watch)

### PURPOSE

When the FileMaker Pro client imports scripts, layouts, or schema items it will create entries in a file in the user's Documents folder. This system will monitor the log changes, and create Notification Center alerts when there are new errors.

**Note however that when working on local (non-hosted) files there is no fixed position for the Import.log file, so these events are not monitored.**

### REQUIREMENTS

Mac OS 10.8 is required for User Notifications feature. One feature, the clearing of old notifications when using the Alert style, requires Mac OS 10.9.

### INSTALLATION

There are two files that must be copied into different locations on your system.

The first is a launchd .plist that sets up the monitoring of changes to the Import.log. Copy the com.sibr.fmp_import_watch.plist inside the following folder (where the tilde indicates your home directory):
> ~/Library/LaunchAgents 

The Python script, fmp_import_watcher.py should be installed inside:
> ~/Library/Application Support/

Log out & back in to activate the monitoring, or to make this happen immediately, run this command in Terminal:

> launchctl load ~/Library/LaunchAgents/com.sibr.fmp_import_watch.plist

### LOGGING

Information may be logged to two files, both in /tmp:

* /tmp/fmp_import_watch.log
* /tmp/fmp_import_watch_err.log

### HISTORY

**Created by Simon Brown **
**First public version February 2, 2014 **
