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
        self.termyearstr = None
        self.termyearid = None

    # Crns are not the same between semester, so must reset list every time
    # Returns if the list of crns need to be reset
    def settermyear(self, termyearstr, termyearid):
        reset = termyearstr != self.termyearstr
        if reset:
            self.crns = []
            self.termyearstr = termyearstr
            self.termyearid = termyearid
        return reset

    # Need to check if return result is none to determine if valid crn
    def addcrn(self, crn):
        crncourse = cc.getclass(crn, self.termyearid)
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
        print("Starting Check")
        browser = cr.WebPage(self.termyearstr)
        while not self.continuecheck.is_set():
            for crn in self.crns:
                print('Checking ' + str(crn))
                if cc.isclassopen(crn, self.termyearid):
                    print('Crn is open ' + str(crn))
                    browser.addcrn(crn)
            browser.clickbutton(browser.find_element_by_id, 'saveButton')
            self.continuecheck.wait(self.delay)
        browser.close()

    def startcheck(self):
        self.continuecheck.clear()
        t1 = Thread(target=self.runcheck)
        t1.setDaemon(True)
        t1.start()

    def endcheck(self):
        self.continuecheck.set()
