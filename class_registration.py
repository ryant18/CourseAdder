import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

registration_url = 'https://apps.es.vt.edu/StudentRegistrationSsb/ssb/classRegistration/classRegistration'


# Extends the selenium driver to work specifically with the virginia tech
class WebPage(webdriver.Firefox):
    # Creates the empty webpage, does nothing else
    def __init__(self, termyear):
        super(WebPage, self).__init__()
        self.login(termyear)

    # Tries to click the given button until it is loaded
    # Deals with the webpage loading slow and when the
    # button is loaded but not in view to be clicked
    def clickbutton(self, findbutton, buttonid):
        timeout = time.time() + 60
        while True:
            if time.time() > timeout:
                self.close()
                return
            try:
                findbutton(buttonid).click()
                return
            except (selenium.common.exceptions.NoSuchElementException,
                    selenium.common.exceptions.ElementNotInteractableException,
                    selenium.common.exceptions.ElementClickInterceptedException):
                time.sleep(1)

    # Starts the login process in the geckodriver browser
    # Returns the browser so other methods can be called on it
    def login(self, termyear):
        self.get(registration_url)
        # Wait until login is finished by user
        self.clickbutton(self.find_element_by_id, 'registerLink')
        # Select the term year
        self.clickbutton(self.find_element_by_id, 's2id_txt_term')
        self.find_element_by_id('s2id_autogen1_search').send_keys(termyear)
        time.sleep(1)
        self.find_element_by_id('s2id_autogen1_search').send_keys(Keys.RETURN)
        self.clickbutton(self.find_element_by_id, 'term-go')
        # Close out of pop up
        self.clickbutton(self.find_element_by_class_name, 'notification-flyout-item')
        # Shift to crn tab
        self.clickbutton(self.find_element_by_id, 'enterCRNs-tab')

    def addnewcrn(self, crn):
        self.find_element_by_id('txt_crn1').send_keys(crn)
        self.clickbutton(self.find_element_by_id, 'addCRNbutton')
        time.sleep(0.5)
        self.clickbutton(self.find_element_by_id, 'saveButton')

    def addexistingcrn(self, dataid):
        buttoncss = "[data-id='" + str(dataid) + "'][data-property='actionItem']"
        self.clickbutton(self.find_element_by_css_selector, buttoncss)
        dropdownadd = self.find_element_by_css_selector("[class='select2-results-"
                                                        "dept-0 select2-result select2-"
                                                        "result-selectable'][role='option']")
        ActionChains(self).move_to_element(dropdownadd).click().perform()
        time.sleep(0.5)
        self.clickbutton(self.find_element_by_id, 'saveButton')

    def getexistingclasses(self):
        addedclasses = self.find_elements_by_class_name('odd')
        addedclasses += self.find_elements_by_class_name('even')
        return addedclasses

    # Adds the crn to the class schedule
    # checks if the class is in the dropdown menu
    def addcrn(self, crn):
        addedclasses = self.getexistingclasses()
        for row in addedclasses:
            if str(crn) in row.text:
                self.addexistingcrn(row.get_attribute('data-id'))
                return
        self.addnewcrn(crn)


a = WebPage("spring")
print('second')
a.addcrn(14277)
print('done')
