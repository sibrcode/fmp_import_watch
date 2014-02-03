#!/usr/bin/python

# 2013-11-30 simon_b: created file
# 2014-02-01 simon_b: added notifications, regular expressions
# 2014-02-02 simon_b: fixed error in regex, not clear out notifications when quitting

import mmap, os, re, sys
from PyObjCTools import AppHelper
import Foundation
import objc
import AppKit
import time
from threading import Timer

from datetime import datetime, date

# objc.setVerbose(1)

class MountainLionNotification(Foundation.NSObject):
	# Based on http://stackoverflow.com/questions/12202983/working-with-mountain-lions-notification-center-using-pyobjc
	
	def init(self):
		self = super(MountainLionNotification, self).init()
		if self is None: return None
		
		# Get objc references to the classes we need.
		self.NSUserNotification = objc.lookUpClass('NSUserNotification')
		self.NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
		
		return self
    
	def clearNotifications(self):
		"""Clear any displayed alerts we have posted. Requires Mavericks."""
    	
		NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
		NSUserNotificationCenter.defaultUserNotificationCenter().removeAllDeliveredNotifications()

	def notify(self, title, subtitle, text, url):
		"""Create a user notification and display it."""
		
		notification = self.NSUserNotification.alloc().init()
		notification.setTitle_(str(title))
		notification.setSubtitle_(str(subtitle))
		notification.setInformativeText_(str(text))
		notification.setSoundName_("NSUserNotificationDefaultSoundName")
		notification.setHasActionButton_(True)
		notification.setActionButtonTitle_("View")
		notification.setUserInfo_({"action":"open_url", "value":url})

		self.NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(self)
		self.NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

		# Note that the notification center saves a *copy* of our object.
		return notification

	# We'll get this if the user clicked on the notification.
	def userNotificationCenter_didActivateNotification_(self, center, notification):
		"""Handler a user clicking on one of our posted notifications."""
		
		userInfo = notification.userInfo()
		if userInfo["action"] == "open_url":
			import subprocess
			# Open the log file with TextEdit.
			subprocess.Popen(['open', "-e", userInfo["value"]])
            
	def userNotificationCenter_shouldPresentNotification_(self, center, notification):
		# We always want our notifications displayed, even if they get a bit repetitive.
		return objc.YES

def stopRunLoop():
	"""Gracefully stop the Cocoa run loop, which also results in script exiting."""

	global gMLNotification
	
	# Remove any notifications we posted.
	gMLNotification.clearNotifications()
	
	# Kill of our run loop since we will no longer be responding to any clicks.
	AppHelper.stopEventLoop()


def main():

	global gMLNotification
	global gImportFullPath

	# Anything to process? Also needed for mmap function.	
	fileSize = os.stat(gImportFullPath).st_size

	if fileSize > 0:
		# Setup our app environment.
		app=AppKit.NSApplication.sharedApplication()
	
		theFile = open(gImportFullPath)
		importData = mmap.mmap(theFile.fileno(), fileSize, access=mmap.ACCESS_READ)

		# Get lines with a non-zero error code, extracting the date, time, error object, and error number
		rePattern = re.compile (r"(\d\d\d\d-\d\d-\d\d) (\d\d\:\d\d:\d\d).*?\t(.*?)\t([123456789]\d*)\t(.*)")

		# Banner notifications stay up for about 6 seconds, but there may be delays posting them.
		# We need to hang around long enough to handle a user clicking on the notification.
		t = Timer(9.0, stopRunLoop)
		t.start()

		allMatches = rePattern.findall (importData)
		print "Found",len (allMatches),"errors"
		hadMatch = False
		matchNum = -1
		n = []
	
		# This should be the last logged error in import log.
		for match in allMatches:
			matchNum += 1
			n.append (None)
			dt = datetime.strptime(match[0] + " " + match[1], "%Y-%m-%d %H:%M:%S")
	
			if (datetime.now() - dt).seconds < 15:
				n[matchNum] = gMLNotification.notify ("FileMaker Import Error",match[2],match[3] + ": " + match[4],gImportFullPath)
				print "notification",matchNum,"added"
				print match
				time.sleep (0.5)
				hadMatch = True
								
		if hadMatch:
			# The timer set up previously will kill the event loop after the notifications have expired.
			AppHelper.runConsoleEventLoop(installInterrupt=True)

		else:
			# There were no matches, and nothing to do, just exit now.
			sys.exit(0)

#
#	r u n
#

if __name__ == '__main__':

	# When using server based files the import log is in the user's Documents folder.
	gImportSubpath = "~/Documents/Import.log"

	# Need to convert the tilde to full path.
	gImportFullPath = os.path.expanduser (gImportSubpath)

	gMLNotification = MountainLionNotification.alloc().init()
	
	main()


