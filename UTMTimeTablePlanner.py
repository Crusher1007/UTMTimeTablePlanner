#UTMTimeTablePlanner
#@Author: Christopher Chianelli

#intialization code
import urllib.request
from tkinter import *
import tkinter.ttk
import time

#Constants
_dep = {"Anthropology" : 1, "Astronomy" : 2, "Biology" : 3, "Biomedical Communications" : 51, "Chemistry" : 5, "Cinema Studies" : 46, "Classics" : 6, "Communication, Culture, Infomation, and Technology" : 4, "Computer Science" : 7, "Concurrent Teacher Education" : 48, "Diaspora and Transnational Studies" : 45, "Drama" : 8, "Earth Science" : 13, "Economics" : 9, "English" : 10, "Enviroment" : 11, "Environmental Geoscience" : 54, "Erindale Courses" : 12, "European Studies" : 14, "Fine Art History (FAH)" : 15, "Fine Art Studio" : 16, "Forensic Science" : 18, "French" : 17, "Geography" : 20, "History" : 22, "History of Religions" : 34, "Italian" : 23, "Language Studies" : 49, "Language Teaching and Learning: French and Italian (HBA)" : 53, "Linguistics" : 26, "Management" : 28, "Mathematics" : 27, "Philosophy" : 29, "Physics" : 30, "Political Science" : 31, "Professional Writing and Communication" : 32, "Psychology" : 33, "Science" : 35, "Slavic Language (Croatian)" : 36, "Sociology" : 37, "Statistics" : 38, "utmONE" : 52, "Visual Culture and Communication" : 50, "Women and Gender Studies" : 40}
_year = "2014"#time.strftime("%Y")



class App:
    """Runs and contain the GUI of the UTM Timetable Planner"""
    def __init__(self : "App", parent : "Tk"):
        """Set up the Application"""
        #intialize class variables
        self.department = 1
        self.possibles = []
        self.myDep = []
        self.mySessions = []
        currCourse = ""

        #intialize GUI variables
        self.parent = parent
        self.session_value = StringVar()
        self.area_value = StringVar()
        self.course_value = StringVar()
        self.minTime = StringVar()
        self.maxTime = StringVar()
        
        self.monday = IntVar()
        self.tuesday = IntVar()
        self.wednesday = IntVar()
        self.thursday = IntVar()
        self.friday = IntVar()

        #Create Labels
        self.sessionLabel = Label(parent, text="Session")
        self.sessionLabel.grid(column=0, row=0)
        
        self.subjectAreaLabel = Label(parent, text="Subject Area")
        self.subjectAreaLabel.grid(column=0, row=1)
        
        self.coursesLabel = Label(parent, text="Courses")
        self.coursesLabel.grid(column=0, row=2)

        self.tableLable = Label(parent, text="Selected Courses")
        self.coursesLabel.grid(column=0, row=4)

        self.minTimeLabel = Label(parent, text="Earliest Time")
        self.minTimeLabel.grid(column=3, row=4)

        self.maxTimeLabel = Label(parent, text="Latest Time")
        self.maxTimeLabel.grid(column=3, row=5)

        #Create comboboxes for session, department, and courses
        self.session = tkinter.ttk.Combobox(self.parent, textvariable=self.session_value, state="readonly", width=60)
        self.session['values'] = ("Summer-" + _year, "Fall/Winter-" + _year + "/" + str(int(_year) + 1))
        self.session.current(1)
        self.session.grid(column=1, row=0)
        self.session.bind("<<ComboboxSelected>>", self.updateCourses)
        
        self.subjectAreas = tkinter.ttk.Combobox(self.parent, textvariable=self.area_value, state="readonly", width=60)
        self.subjectAreas['values'] = tuple(sorted(_dep.keys()))
        self.subjectAreas.current(0)
        self.subjectAreas.grid(column=1, row=1)
        self.subjectAreas.bind("<<ComboboxSelected>>", self.updateCourses)
        
        self.courses = tkinter.ttk.Combobox(self.parent, textvariable=self.course_value, state="readonly", width=60)
        self.courses['values'] = tuple(getCourses(self.subjectAreas.get(), _year, self.session.get()))
        self.courses.current(0)
        self.courses.grid(column=1, row=2)
        currCourse = self.courses.get()

        #Create a listbox to hold courses
        self.table = Listbox(root, bg="black",fg="white", width=65)
        self.table.grid(column=1,row=4)

        #Create Options
        self.minTimeEntry = Entry(self.parent, textvariable=self.minTime,width=4)
        self.minTimeEntry.grid(column=2,row=4)
        
        self.maxTimeEntry = Entry(self.parent, textvariable=self.maxTime,width=4)
        self.maxTimeEntry.grid(column=2,row=5)

        self.mondayButton = Checkbutton(self.parent, variable=self.monday,text="Mondays Off")
        self.mondayButton.grid(column=4,row=0)

        self.tuesdayButton = Checkbutton(self.parent, variable=self.tuesday,text="Tuesdays Off")
        self.tuesdayButton.grid(column=4,row=1)

        self.wednesdayButton = Checkbutton(self.parent, variable=self.wednesday,text="Wednesdays Off")
        self.wednesdayButton.grid(column=4,row=2)

        self.thursdayButton = Checkbutton(self.parent, variable=self.thursday,text="Thursdays Off")
        self.thursdayButton.grid(column=5,row=0)

        self.fridayButton = Checkbutton(self.parent, variable=self.friday,text="Fridays Off")
        self.fridayButton.grid(column=5,row=1)

        #add buttons
        self.addButton = Button(self.parent, text="Add", command=self.addCourse)
        self.addButton.grid(column=1, row=3)

        self.removeButton = Button(self.parent, text="Remove Selected Course", command=self.removeCourses)
        self.removeButton.grid(column=1, row=5)
        
        self.generateButton = Button(self.parent, text="Generate a Schedule", command=self.generate)
        self.generateButton.grid(column=1, row=6)

        #Create the empty timetable
        self.timetable = Listbox(root, bg="black",fg="white", width=65)
        self.timetable.grid(column=1,row=8)

        #Create a progressbar and label
        self.progressbar = tkinter.ttk.Progressbar(self.parent, orient="horizontal",mode="determinate", length=400)
        self.progressbar.grid(column=1,row=9)

        self.progresslabel = Label(self.parent)
        self.progresslabel.grid(column=1,row=10)



    def addCourse(self : "App"):
        """Adds a course to the timetable"""
        self.table.insert(END, self.courses.get())
        self.myDep.append(self.department)
        self.mySessions.append(self.session.get())

    def removeCourses(self : "App"):
        """Removes a course from the timetable"""
        if len(self.table.curselection()) == 0:
            return
        index = self.table.curselection()
        self.table.delete(ACTIVE)
        del self.myDep[int(index[0])]
        del self.mySessions[int(index[0])]

    def updateCourses(self : "App", event : "<<ComboboxSelected>>"):
        """Changes what courses to display according to the department selected"""
        self.courses['values'] = tuple(getCourses(self.subjectAreas.get(), _year, self.session.get()))
        self.courses.current(0)
        self.department = _dep[self.subjectAreas.get()]

    def generate(self : "App"):
        #Get courses
        self.possibles = []
        lowest = 0
        highest = 0
        
        if self.minTime.get().lower().find("pm") != -1:
            lowest = Session(["AL","00:00", str(12 + int(self.minTime.get()[0:self.minTime.get().lower().find("pm")])).zfill(2) + ":00", "None", "Y"])
                             
        elif self.minTime.get().lower().find("am") != -1:
            lowest = Session(["AL","00:00", str(int(self.minTime.get()[0:self.minTime.get().lower().find("am")])).zfill(2) + ":00", "None", "Y"])
                             
        elif self.minTime.get() == "":
            lowest = Session(["AL","00:00", "00:00", "None", "Y"])

        else:
            lowest = Session(["AL","00:00", self.minTime.get().zfill(2) + ":00", "None", "Y"])


        if self.maxTime.get().lower().find("pm") != -1:
            highest = Session(["AL",str(12 + int(self.maxTime.get()[0:self.maxTime.get().lower().find("pm")])).zfill(2) + ":00","24:00","None", "Y"])
                             
        elif self.maxTime.get().lower().find("am") != -1:
            highest = Session(["AL",str(int(self.maxTime.get()[0:self.maxTime.get().lower().find("am")])).zfill(2)+ ":00","24:00", "None", "Y"])
                             
        elif self.maxTime.get() == "":
            highest = Session(["AL","24:00", "24:00", "None", "Y"])

        else:
            highest = Session(["AL",self.maxTime.get().zfill(2) + ":00", "24:00", "None", "Y"])
                            
        if self.table.size() == 0:
            return
        self.timetable.delete(0,END)
        courseTitles = self.table.get(0, self.table.size())
        courses = []
        self.progressbar.configure(max=len(courseTitles))
        for i in range(len(courseTitles)):
            self.progresslabel.configure(text="Getting " + courseTitles[i] + " class data...")
            self.parent.update_idletasks()
            courses.append(Course(courseTitles[i],getCourseInfo(courseTitles[i],self.mySessions[i],self.myDep[i])))
            self.progressbar.step()

        sessions = []

        #Create conditions
        conditions = [["Conditions", ["C","O","N","D","I","T", "N"]]]
        if lowest != Session(["AL","00:00", "00:00", "None", "Y"]):
            conditions[0][1].append(lowest)
            
        if highest != Session(["AL","24:00", "24:00", "None", "Y"]):
            conditions[0][1].append(highest)

        if self.monday.get() == 1:
            conditions[0][1].append(Session(["MO","00:00", "24:00", "None", "Y"]))

        if self.tuesday.get() == 1:
            conditions[0][1].append(Session(["TU","00:00", "24:00", "None", "Y"]))

        if self.wednesday.get() == 1:
            conditions[0][1].append(Session(["WE","00:00", "24:00", "None", "Y"]))

        if self.thursday.get() == 1:
            conditions[0][1].append(Session(["TH","00:00", "24:00", "None", "Y"]))

        if self.friday.get() == 1:
            conditions[0][1].append(Session(["FR","00:00", "24:00", "None", "Y"]))

        if len(conditions[0][1]) > 7:
            sessions.append(conditions)

        #divide them into seperate groups
        for course in courses:
            sessions.append(course.getLectures())
            sessions.append(course.getTutorials())
            sessions.append(course.getPracticals())

        for i in range(sessions.count([])):
            sessions.remove([])

        #solve for a possible schedule    
        maxIndicies = []
        currIndicies = []
        for s in sessions:
            maxIndicies.append(len(s) - 1)
            currIndicies.append(-1)

        indexNum = 0

        self.progresslabel.configure(text="Calculating a possible schedule...")
        self.progressbar = tkinter.ttk.Progressbar(self.parent, orient="horizontal",mode="indeterminate", length=400)
        self.progressbar.grid(column=1,row=9)
        self.parent.update_idletasks()

        while (indexNum < len(maxIndicies)):
            #check if we didn't try all avaiable, if so, try next
            if currIndicies[indexNum] < maxIndicies[indexNum]:
                currIndicies[indexNum] += 1

            #check if we are not at root
            #if so, go down one level
            elif indexNum > 0:
                currIndicies[indexNum] = -1
                indexNum -= 1
                continue
            
            #else, it is impossible to not have conflicts
            else:
                break

            #assume it is possible
            possible = True

            #cycle through all sessions up to the index number
            for i in range(indexNum):
                #check each date and time and check for conflicts
                for s2 in sessions[i][currIndicies[i]][1][7:]:
                    for s3 in sessions[indexNum][currIndicies[indexNum]][1][7:]:
                        if s2.isConflict(s3):
                            possible = False
                            break
    
                    if not possible:
                        break
                    
            #if it remained possible, this level is good
            if possible:
                indexNum += 1

        else:#success
            for num in range(len(currIndicies)):
                temp = sessions[num][currIndicies[num]][0]
                temp += " "
                for s4 in sessions[num][currIndicies[num]][1:]:
                    for letter in s4[0:7]:
                        temp += letter
                    temp += " "
                    
                self.timetable.insert(END, temp)
                
            self.progresslabel.configure(text="")
            self.progressbar = tkinter.ttk.Progressbar(self.parent, orient="horizontal",mode="determinate", length=400)
            self.progressbar.grid(column=1,row=9)
            self.parent.update_idletasks()        
            return
        
        self.timetable.insert(END, "No possible schedule")
        self.progresslabel.configure(text="")
        self.progressbar = tkinter.ttk.Progressbar(self.parent, orient="horizontal",mode="determinate", length=400)
        self.progressbar.grid(column=1,row=9)
        self.parent.update_idletasks()

        
class Course:
    """Contains the lectures, tutorials, and practical sessions for a course"""
    
    def __init__(self : "Course", courseName : str, courseData : str):
        """Creates a course given the course's name and the decoded
           xml file for the course
        """
        self._name = courseName
        sections = []

        #Get every section for the course
        for i in range(0, len(courseData), 5):
            sections.append(courseData[i])

        #sections are double counted in year courses since they
        #are composed of both the Fall and Winter Session
        if courseName[8] == "Y":
            sections = sections[:int(len(sections)/2)]

        #Add each section's infomation
        self._sections = []
        count = []
        i = 0
        j = 0
        while(i < len(sections)):
            self._sections.append(list(sections[i]))
            count.append(sections.count(sections[i]))
            i += count[j]
            j += 1

        #Create the sessions for the course
        sessions = []

        for j in range(1, len(courseData), 5):
            sessions.append(Session(courseData[j:j + 4] + list(courseName[8])))

        #Combine dublicate sessions
        i = 0
        for j in range(len(self._sections)):
            self._sections[j].extend(sessions[i: i + count[j]])
            i += count[j]
        #end __init__

    def getLectures(self : "Course"):
        """getLectures() -> list
           returns all the lectures for the course
        """
        lectures = []
        for section in self._sections:
            if section[0] == "L":
                for lec in lectures:
                    if (lec[len(lec) - 1][7] == section[7]):
                        lec.append(section)
                        break

                else:
                    lectures.append([self._name, section])

        return lectures

    def getTutorials(self : "Course"):
        """getTutorials() -> list
           returns all the tutorials for the course
        """
        tutorials = []
        for section in self._sections:
            if section[0] == "T":
                for tut in tutorials:
                    if (tut[len(tut) - 1][7] == section[7]):
                        tut.append(section)
                        break

                else:
                    tutorials.append([self._name, section])
           
        return tutorials

    def getPracticals(self : "Course"):
        """getPracticals() -> list
           returns all the practicals for the course
        """
        practicals = []
        for section in self._sections:
            if section[0] == "P":
                for prac in practicals:
                    if (prac[len(prac) - 1][7] == section[7]):
                        prac.append(section)
                        break

                else:
                    practicals.append([self._name, section])

        return practicals


    def __str__(self : "Course"):
        """Returns the course's name and all its sessions"""
        temp = self._name + "\n"
        for section in self._sections:
            for letter in section[0:7]:
                temp += letter

            temp += "\n"
            for session in section[7:]:
                temp += "\t" + session.__str__() + "\n"
            
            
        return temp



class Session:
    """Contains infomation for a signal lecture, tutorial, and practical session"""
    def __init__(self : "Session", sessionInfo : list):
        """Session(sessionInfo) -> Session
           creates a new session given the session's infomation
        """
        self._day = sessionInfo[0]
        self._startTime = Time(sessionInfo[1])
        self._endTime = Time(sessionInfo[2])
        self._room = sessionInfo[3]
        self._session = sessionInfo[4]

    def isConflict(self : "Session", other : "Session"):
        """isConflict(other) -> bool
           returns if this session is conflicting with
           another session
        """
        #Check if they are in the same session. If not, return False
        if self._session != "Y" and other._session != "Y" and self._session != other._session:
            return False
        #Check if they are on the same day. If not, return False
        if self._day != "AL" and other._day != "AL":
            if self._day != other._day:
                return False

        #Check if either are indepenent research. If so, return False                      
        if (self._startTime == _noTime or other._startTime == _noTime):
            return False
        #return if one starts before another ends
        return (self._startTime < other._endTime and other._startTime <= self._startTime) or (other._startTime < self._endTime and self._startTime <= other._startTime)

    def __eq__(self : "Session", other : "Session"):# a == b?
        return self._startTime == other._startTime and self._endTime == other._endTime and self._day == other._day and self._session == other._session

    def __str__(self):
        return self._day + " " + self._startTime.__str__()  + " to " + self._endTime.__str__() + " at " + self._room

class Time:
    """A representation of 24-hour time that can be manipulated"""
    def __init__(self : "Time", time : str):
        """Time(time) -> Time
           Creates a time object from a String in 24 hour time,
           zero-filled to 5 chars
           >>>t = Time("01:50")
           >>>str(t)
              "01:50"
        """
        #Express time as an int for easy data manipulation
        if (time != ""):
            self._time = 60*int(time[:2]) + int(time[3:])
        else:
            self._time = -1


    def __lt__(self : "Time", other : "Time"):# a < b?
        return self._time < other._time
    def __le__(self : "Time", other : "Time"):# a <= b?
        return self._time <= other._time
    
    def __gt__(self : "Time", other : "Time"):# a > b?
        return self._time > other._time
    def __ge__(self : "Time", other : "Time"):# a >= b?
        return self._time >= other._time
    
    def __eq__(self : "Time", other : "Time"):# a == b?
        return self._time == other._time
    def __ne__(self : "Time", other : "Time"):# a != b?
        return self._time != other._time

    def __str__(self : "Time"):
        """__str__() -> str
           returns a string representing this time in military time
        """
        return str(int(self._time/60)).zfill(2) + ":" + str(self._time%60).zfill(2)
            

#Module methods
def findAll(string : str, substring : str):
    """findAll(string, substring) -> list
       returns all the indices of occurances of
       substring in string

       >>>findAll("Billy Bob pass the Bill to Bill","Bill")
          [0, 19, 27]
    """
    found = []
    start = 0
    while (string.find(substring, start) != -1):
        start = string.find(substring, start)
        found.append(start)
        start += 1

    return found

def getCourses(department : str, year : str, session : str):
    """getCourses(department, year, session) -> list
       returns all the courses offered by a department in a given
       year and session
    """
    u = urllib.request.urlopen("http://m.utm.utoronto.ca/course_list.php?dep_id=" + str(_dep.get(department)) + "&id=" + year + "9&type=1&sessionNm=" + session + "&header=")
    data = u.read().decode()
    u.close()
    courseIndexs = findAll(data, "header=\'>")
    courses = []
    for i in courseIndexs:
        courses.append(data[i + 9:data.find("</a>",i)])
                            
    return courses

def getCourseInfo(course : str, session : str, depID : int):
    """getCourseInfo(course, session, depID) -> list
       returns all lectures, tutorial, and practical data for a course
    """
    courseID = course[:course.find(" -")]
    u = urllib.request.urlopen("http://m.utm.utoronto.ca/course_timetable.php?id=" + _year + "9&course_id=" + courseID[:8]  + "&dep_id=" + str(depID) + "&type=1&sessionNm=" + session + "&sectionCd=" + courseID[8:] + "&header=")
    data = u.read().decode()
    u.close()
    infoStartIndexs = findAll(data, "<td>")
    infoEndIndexs = findAll(data, "</td>")
    courses = []
    for i in range(len(infoStartIndexs)):
        courses.append(data[infoStartIndexs[i] + 4:infoEndIndexs[i]])
    return courses

#Main method    
if __name__ == "__main__":
    #Create the application
    root = Tk()
    _noTime = Time("")
    root.title("UTM Course Scheduler")
    root.geometry("1200x600")
    app = App(root)
    tkinter.mainloop()
    
