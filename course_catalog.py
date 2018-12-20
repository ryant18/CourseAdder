import requests
from bs4 import BeautifulSoup

timetable_url = 'https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest'


class Course:
    def __init__(self, crn, coursenumber, name, instructor,
                 days, starttime, endtime, location):
        self.crn = crn
        self.coursenumber = coursenumber
        self.name = name
        self.instructor = instructor
        self.days = days
        self.starttime = starttime
        self.endtime = endtime
        self.location = location


# Get the semesters that are currently open for viewing in the timetable
def gettermyear():
    req = requests.get(timetable_url).content
    opentermselector = BeautifulSoup(req, "html5lib").find("select", {"name": "TERMYEAR"})
    openterms = {}
    for term in opentermselector.findAll("option"):
        if term.get_text() != 'Select Term':
            openterms[term.get_text()] = term['value']
    return openterms


# Get the information of the class from the timetable
# Returns none if the crn does not exist in the given term
def getclass(crn, termyear):
    postdata = {
        'CAMPUS': '0',
        'CORE_CODE': 'AR%',
        'crn': crn,
        'TERMYEAR': termyear,
        'BTN_PRESSED': 'FIND class sections',
    }
    opencourse = None

    req = requests.post(timetable_url, postdata).content
    rows = BeautifulSoup(req, 'html5lib').select('table.dataentrytable tbody tr')
    if len(rows) > 1:
        cells = list(map(lambda x: x.get_text(), rows[1].select('td')))
        crn = cells[0].strip()
        coursenumber = cells[1].strip()
        name = cells[2].strip()
        instructor = cells[6].strip()
        days = cells[7].strip()
        starttime = cells[8].strip()
        endtime = cells[9].strip()
        location = cells[10].strip()

        opencourse = Course(crn, coursenumber, name, instructor,
                            days, starttime, endtime, location)
    return opencourse


# Determines if the class is currently open
def isclassopen(crn, termyear):
    postdata = {
        'CAMPUS': '0',
        'TERMYEAR': termyear,
        'CORE_CODE': 'AR%',
        'crn': crn,
        'open_only': 'on',
        'BTN_PRESSED': 'FIND class sections',
    }

    req = requests.post(timetable_url, postdata).content
    rows = BeautifulSoup(req, 'html5lib').select('table.dataentrytable tbody tr')
    return len(rows) > 1

