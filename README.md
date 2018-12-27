# Virginia Tech Course Adder #
An automated way to add classes to your virginia tech class schedule
This program is similar [course pickle](https://coursepickle.com/), but also adds 
the class to your schedule instead of just notifying you.
![CourseAdder GUI overview](https://github.com/ryant18/CourseAdder/blob/master/images/overview.PNG)
# Installation #
This program was developed on python 3.7.

First, copy the repository

    git clone https://github.com/ryant18/CourseAdder.git
    
It is recommended to install all the dependicies into a virtaul enviroment
    
    virtualenv venv
    source venv/bin/activate
    
Install all requirements
    
    pip install -r requirements.txt
    
Download the latest version of [Firefox geckodriver](https://github.com/mozilla/geckodriver/releases) and place the executable into `venv/Scripts/`

Start the application

    python gui.py

# How to Use #
Select the semester you want to register for
![Select semester](https://github.com/ryant18/CourseAdder/blob/master/images/termselect.jpg)

Add all the crns that you want to add. If your classes are not showing up correctly, make sure you have the right semester selected.
![Add crns](https://github.com/ryant18/CourseAdder/blob/master/images/startinginput.jpg)

Click on a crn to delete the row

![Delete a crn](https://github.com/ryant18/CourseAdder/blob/master/images/deleterow.jpg)

Set the delay that you want to application to check on. This is the amount of time that the program 
will wait before checking the timetable again. This is done to reduce load on your internet connection
and Virginia Tech's servers. The default value is 30 seconds and can be set from 1 to 3600 seconds.
![Change delay timing](https://github.com/ryant18/CourseAdder/blob/master/images/bottombarbuttons.jpg)

To start the check, click the start check button on the bottom. This will disable all features on the gui
and will open a new window. To stop the check click on the start check button again and you will be allowed to edit
your classes.
![Disabled gui](https://github.com/ryant18/CourseAdder/blob/master/images/disabledgui.jpg)


In the new window you will need to login through the Virginia Tech login portal. That is the only
action required in the browser. You can minimize all the windows, but they do need to remain open for 
the program to work.
![VT login](https://github.com/ryant18/CourseAdder/blob/master/images/vtlogin.jpg)


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
