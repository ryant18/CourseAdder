from threading import Thread
from threading import Event
import course_catalog as cc
import class_registration as cr

STARTING_DELAY = 30


class App:
    # Must set the termyear before doing anything else
    def __init__(self):
        self.crns = []
        self.continuecheck = Event()
        self.delay = STARTING_DELAY
        self.termyear = None

    # Crns are not the same between semester, so must reset list every time
    # Returns if the list of crns need to be reset
    def settermyear(self, newtermyear):
        reset = newtermyear != self.termyear
        if reset:
            self.crns = []
            self.termyear = newtermyear
        return reset

    # Need to check if return result is none to determine if valid crn
    def addcrn(self, crn):
        crncourse = cc.getclass(crn, self.termyear)
        if crncourse is not None:
            self.crns.append(crn)
        return crncourse

    def removecrn(self, crn):
        if crn in self.crns:
            self.crns.remove(crn)

    def setdelaytime(self, delay):
        self.delay = delay

    # Not to be called by outside functions
    def runcheck(self):
        browser = cr.WebPage(self.termyear)
        while not self.continuecheck.is_set():
            for crn in self.crns:
                if cc.isclassopen(crn, self.termyear):
                    browser.addcrn(crn)
            self.continuecheck.wait(self.delay)
        browser.close()

    def startcheck(self):
        self.continuecheck.clear()
        t1 = Thread(target=self.runcheck)
        t1.setDaemon(True)
        t1.start()

    def endcheck(self):
        self.continuecheck.set()
