import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
        timeout = time.time() + 60 * 5
        while True:
            if time.time() > timeout:
                self.close()
            try:
                findbutton(buttonid).click()
                break
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

    # Adds the crn to the class schedule
    # has to deal with if the class has already been added before
    def addcrn(self, crn):
        pass
