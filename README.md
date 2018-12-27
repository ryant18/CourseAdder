# Virginia Tech Course Adder #
An automated way to add classes to your virginia tech class schedule
This program is similar [course pickle](https://coursepickle.com/), but also adds 
the class to your schedule instead of just notifying you.
![CourseAdder GUI overview](https://github.com/ryant18/CourseAdder/blob/master/images/overview.PNG)
# Introduction #
This program was developed on python 3.7.

First, copy the repository

'''
git clone https://github.com/ryant18/CourseAdder.git
'''
It is recommended to install all the dependicies into a virtaul enviroment
![Input each crn into the textbox]()

# Requirements #
# How to Use #

# TODO / Future changes #
* Stop adding a crn from blocking the gui
    * The problem is that the gui can only be accessed from the main thead
      so there needs to be a way to get the result from the request into the main 
      thread without blocking other inputs
* Make course selector work with independent study classes
* Turn the backend app into singleton so that some methods do not have to be called from the app object
* Figure out way to added classes other than going through selnium
* Figure out better way to deal with vt login system
* Add way to import / save crn lists
* Remove delay from requesting the termyears at startup
* Bug where typing fewer than 5 digits in crn box, the crn has 0's appended to end
