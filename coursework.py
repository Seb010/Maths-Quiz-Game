#!/usr/bin/python

# Author: Seb010
# Title: Quiz version 1.0
# Last Update: 14.08.2023
# Description: Quiz program to test knowledge of quadratic formula
# SQLight reference: https://www.tutorialspoint.com/sqlite/sqlite_python.htm

from tkinter import *
import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import math
import re
import sqlite3
# preparation of the GUI
from tkinter.constants import CENTER


mainUserWindow = tk.Tk()
mainUserWindow.title("Quadratic Formula Quiz")
mainUserWindow.geometry("800x500")
global welcomeframe
global taskframe
global endGameSummaryFrame
global leaderboardFrame
global answerA
global answerB
global firstchoice
firstchoice = 0
global submittedFlag
global resultArray
global currentUser
global usersOnLeaderboard
global conn
global lastUpdate
lastUpdate="2nd February 2020"



# classes OOP

def displayCount():
    print("Total Users %d" % User.userCount)


class User:
    userCount = 0

    def __init__(self, name):
        self.name = name.capitalize()  # Convert first character to uppercase
        self.userPoints = 0
        self.userTotalAnswers = 0
        self.userCorrectAnswers = 0
        self.userIncorrectAnswers = 0

        User.userCount += 1

    def addCorrectAnswer(self):
        self.userPoints += 1  # to be changed depending on how many points to be added on correct answer
        self.userCorrectAnswers += 1
        self.userTotalAnswers += 1

    def addIncorrectAnswer(self):
        self.userPoints -= 1  # to be changed depending on how many points to be subtracted on incorrect answer
        self.userIncorrectAnswers += 1
        self.userTotalAnswers += 1

    def getUserName(self):
        return self.name

    def getUserPoints(self):
        return self.userPoints

    def getUserTotalAnswersGiven(self):
        return self.userTotalAnswers

    def getUserCorrectAnswersGiven(self):
        return self.userCorrectAnswers

    def getUserIncorrectAnswersGiven(self):
        return self.userIncorrectAnswers

    #
    def setPoints(self, points):
        self.userPoints = points

    def setTotalAnswers(self, answers):
        self.userTotalAnswers = answers


# definitions ----------------------------------------------------------------------------
# returns 3 random numbers in array (range 1-20)
def get3RandomNumbers():
    randomNumbersABC = [0, 0, 0]
    i = 0
    while i < 3:
        randomNumbersABC[i] = random.randint(1, 20)
        i = i + 1
    return randomNumbersABC


# array of user objects on leaderboard to be passed
def bubbleSortOnUsersLeaderboard(usersLeaderboardArray):  # will sort descending
    length = len(usersLeaderboardArray) - 1  # -1 as compares with the last integer in array
    sorted = False  # Assumes array is not sorted

    while not sorted:
        sorted = True  # assumes array is sorted
        for i in range(length):
            if usersLeaderboardArray[i].getUserPoints() < usersLeaderboardArray[i + 1].getUserPoints():  # Checks if 1st int is smaller than 2nd
                sorted = False
                usersLeaderboardArray[i], usersLeaderboardArray[i + 1] = usersLeaderboardArray[i + 1], \
                                                                         usersLeaderboardArray[
                                                                             i]  # Order changed around


def opendbconnection():
    global conn
    conn = sqlite3.connect('quadraticFormulaQuiz.db')
    print("Opened database successfully")

#Database containing Users, Userpoints, UserTotalAnswers,UserCorrectAnswers,UserIncorrectAnswers,Time user name was made
def createDbTables():
    conn.execute('''CREATE TABLE if not exists Users
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         NAME TEXT NOT NULL,
         USERPOINTS INT NOT NULL,
         USERTOTALANSWERS INT NOT NULL,
         USERCORRECTANSWERS INT NOT NULL,
         USERINCORRECTANSWERS INT NOT NULL,
         RECORDTIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
         USERNOTES VARCHAR(500));''')
    print("Table created successfully")

def insertUserIntoDB(user):

    conn.execute('INSERT INTO Users (NAME,USERPOINTS,USERTOTALANSWERS,USERCORRECTANSWERS,USERINCORRECTANSWERS) VALUES (?,?,?,?,?)', (user.getUserName(), user.getUserPoints(), user.getUserTotalAnswersGiven(), user.getUserCorrectAnswersGiven(), user.getUserIncorrectAnswersGiven()))
    conn.commit()
    print("Record created successfully")

def forgetTheOlderFrames():
    try:
        welcomeframe.pack_forget()
        welcomeframe.destroy()
    except Exception:
        pass
    try:
        taskframe.pack_forget()
        taskframe.destroy()
    except Exception:
        pass
    try:
        endGameSummaryFrame.pack_forget()
        endGameSummaryFrame.destroy()
    except Exception:
        pass
    try:
        leaderboardFrame.pack_forget()
        leaderboardFrame.destroy()
    except Exception:
        pass


def displayTaskToUser(randomNumbersABC, currentUser, imageLabel=None):
    global welcomeframe
    forgetTheOlderFrames()

    global taskframe
    taskframe = tk.Frame(mainUserWindow)
    qFormulaImg = ImageTk.PhotoImage(Image.open('qFormula.png').resize((200, 100), Image.ANTIALIAS))
    formulainfo = "\n" + currentUser.getUserName() + ", please consider:\n\n\n***************************\n Quadratic " \
                                                     "Formula:\n "
    formulalabel = tk.Label(taskframe, text=formulainfo)
    imageLabel = tk.Label(taskframe, image=qFormulaImg)
    imageLabel.image = qFormulaImg
    taskInfo = "\n***************************\n\n\nPlease calculate the result \"x\" based on numbers as below:\n\na= " + str(
        randomNumbersABC[0]) + "\nb= " + str(randomNumbersABC[1]) + "\nc= " + str(randomNumbersABC[2]) + "\n\n"
    taskLabel = tk.Label(taskframe, text=taskInfo)
    formulalabel.pack()
    imageLabel.pack()
    taskLabel.pack()
    taskframe.pack()


# Discriminant = b^2-4ac
# If Discriminant = 0 then there is only 1 answer (when it is zero we get just ONE real solution (both answers are the same))
# If Discriminant = >=1 then there are two answers (we get two Real solutions )
# If Discriminant = <0 there are no answers (when it is negative we get a pair of Complex solutions )
# https://www.mathsisfun.com/algebra/quadratic-equation.html
def getDiscriminant(randomNumbersABC):
    return math.pow(randomNumbersABC[1], 2) - 4 * randomNumbersABC[0] * randomNumbersABC[2]


def calculateQF(randomNumbersABC, discriminant):
    if discriminant < 0:

        result = ["no answer"]
        return result
    elif discriminant >= 1:

##        rounds the answer to 2 decimal places

        result = [0, 0]
        result[0] = round((-randomNumbersABC[1] + (math.sqrt(discriminant))) / (2 * randomNumbersABC[0]), 2)
        result[1] = round((-randomNumbersABC[1] - (math.sqrt(discriminant))) / (2 * randomNumbersABC[0]), 2)
        return result
    elif discriminant == 0:

        result = [0, 0]
        result[0] = round((-randomNumbersABC[1] + (math.sqrt(discriminant))) / (2 * randomNumbersABC[0]), 2)
        result[1] = round((-randomNumbersABC[1] - (math.sqrt(discriminant))) / (2 * randomNumbersABC[0]), 2)
        if result[0] == result[1]:
            print("answer 1 and answer 2 are the same !!")
        return result


def showNextTaskToUser():
    global resultArray
    global currentUser
    global taskframe
    global firstchoice
    global answerA
    global answerB
    firstchoice = 0
    answerA = ""
    answerB = ""
    taskframe.pack_forget()
    randomNumbersABC = get3RandomNumbers()
    # possibly need to forget the previous frame
    displayTaskToUser(randomNumbersABC, currentUser)
    discriminant = getDiscriminant(randomNumbersABC)
    resultArray = calculateQF(randomNumbersABC, discriminant)
    print("discriminant" + str(discriminant))
    print(resultArray)
    getAnswer()  # from the user


def showLeaderboard():
    currentuseranswers = 0

    try:
        currentuseranswers = currentUser.getUserTotalAnswersGiven()
    except:
        print("currentUser.getUserTotalAnswersGiven() error")


    if currentuseranswers != 0:
        endGame()
    else:

        global leaderboardFrame
        forgetTheOlderFrames()


        leaderboardFrame = tk.Frame(mainUserWindow)

        

        leaderboardInfo = "\n\nBeat the Robot with 100 points!  ;) \n\n\n\n TOP 10 players:\n\n\n"

        #get top 10 users from db
        cursor = conn.execute("SELECT NAME, USERPOINTS from Users order by USERPOINTS DESC Limit 10")
        usersOnLeaderboardTmp = [User("robot")]
        usersOnLeaderboardTmp[0].setPoints(100)


        for row in cursor:
            tmpUser=User(row[0])
            tmpUser.setPoints(row[1])
            usersOnLeaderboardTmp.append(tmpUser)

        print("Operation done successfully")

##        Leaderboard only stores Top 10 results in descening order
        bubbleSortOnUsersLeaderboard(usersOnLeaderboardTmp)
        counter = 1
        for x in usersOnLeaderboardTmp:
            leaderboardInfo += str(counter) + ".  "
            leaderboardInfo += str(x.getUserName())
            leaderboardInfo += ": " + str(x.getUserPoints()) + " points\n\n"
            counter = counter + 1
            if counter == 11:
                break


        leaderboardLabel = tk.Label(leaderboardFrame, text=leaderboardInfo)
        leaderboardLabel.pack()
        leaderboardFrame.pack()
        


def showEndGameSummaryPage(cUser):
    global currentUser
    global usersOnLeaderboard
    global leaderboardFrame
    global endGameSummaryFrame

    welcomeframe.pack_forget()
    taskframe.pack_forget()
    try:
        leaderboardFrame.pack_forget()
    except:
        pass
    endGameSummaryFrame = tk.Frame(mainUserWindow)
    summaryinfo = "\n\n\n Dear " + cUser.getUserName() + ", your score is: " + str(
        cUser.getUserPoints()) + "\n\n\nTotal answers given: " + str(
        cUser.getUserTotalAnswersGiven()) + "\nIncorrect answers: " + str(
        cUser.getUserIncorrectAnswersGiven()) + "\nCorrect answers: " + str(
        cUser.getUserCorrectAnswersGiven()) + "\n\n\nThank you for playing\n\n"
    summarylabel = tk.Label(endGameSummaryFrame, text=summaryinfo)

    newUserButton = tk.Button(endGameSummaryFrame, text="New Player", highlightcolor="red", command=showWelcomePage)
    leaderboardsbutton = tk.Button(endGameSummaryFrame, text="LEADERBOARDS", highlightcolor="red",
                                   command=showLeaderboard)

    summarylabel.pack()
    newUserButton.pack()
    leaderboardsbutton.pack()
    endGameSummaryFrame.pack()
    # usersOnLeaderboard.append(cUser)
    currentUser = User("Temp")
    # print("usersOnLeaderboard " + str(len(usersOnLeaderboard)))
    # for x in usersOnLeaderboard:
    #     print(x.getUserName())


def endGame():
    global currentUser

    msgToUser = " " + currentUser.getUserName() + ", would you like to finish?"
    confirmationToEnd = tk.messagebox.askyesnocancel("End the quiz", msgToUser)
    print(confirmationToEnd)
    if confirmationToEnd == True:
        insertUserIntoDB(currentUser)
        showEndGameSummaryPage(currentUser)
        pass
    elif confirmationToEnd == False:
        pass
    elif confirmationToEnd == None:
        pass
    pass


def endGameforUser():
    currentuseranswers = 0

    try:
        currentuseranswers = currentUser.getUserTotalAnswersGiven()
    except Exception:
        pass

    if currentuseranswers != 0:
        endGame()
    else:
        if tk.messagebox.askyesno("End Game", "No user is playing, would you like to exit the program ?"):
            quit()


def submitAnswer():
    global firstchoice  # number of answers given by user 0 / 1 / 2 ( determinant / user )
    global answerA
    global answerB

    print("Answer submitted.\n")
    if firstchoice == 0:
        print("firstchoice: " + str(firstchoice))
        answerA = ""
        answerB = ""

    elif firstchoice == 1:
        answerA = answerA.get()
        answerB = ""
        print("firstchoice: " + str(firstchoice))
        print("answerA: " + str(answerA))
        

        if answerA != "":

            rule = re.compile(r'^-?\d+(\.\d\d?)?$')
            if not rule.search(answerA):
                tk.messagebox.showinfo("", "Incorrect Form \n"
                                           "Please make sure answer is given to 2 decimal places")
  
                  
        elif len(answerA)==0:
          empty = tk.messagebox.askyesno("Empty String", "Your answer is empty are you sure you want to continue")

            # Code thas will display same set of random numbers until entry is not empty

        

    elif firstchoice == 2:
        answerA = answerA.get()
        answerB = answerB.get()

        # Decimal Point escaped with \.
        # If decimal Point does exist, it must be followed by 1 or 2 digits \d
        # \d and [0-9] are equivalent
        # ^ and $ anchor the endpoints so the whole string must match

        if answerA != "" or answerB != "":

            rule = re.compile(r'^-?\d+(\.\d\d?)?$')
            if not rule.search(answerA) or not rule.search(answerB):
                tk.messagebox.showinfo("", "Incorrect Form \n"
                                           "Please make sure answer is given to 2 decimal places")
        else:
            print("")

        if len(answerA) == 0 or len(answerB) == 0:
            tk.messagebox.askyesno("Empty String",
                                   "One or more of your answers is empty, are you sure you want to continue")

        print("firstchoice: " + str(firstchoice))
        print("answerA :" + str(answerA))
        print("answerB :" + str(answerB))

    # userAnswers :globals firstchoice, answerA, answerB
    calculatePointsForTheUser(resultArray, currentUser)
    showNextTaskToUser()


def getAnswer():
    global answerWizard
    answerWizard = tk.Frame(taskframe)
    section1 = tk.Frame(answerWizard)
    global section2
    section2 = tk.Frame(answerWizard)
    section3 = tk.Frame(answerWizard)

    # section 1 (on the left)
    v = tk.IntVar()
    v.set(0)  # initializing the choice

    answers = [
        "No answer",
        "1 answer",
        "2 answers"
    ]

    def quadratic_formula_entry(input):
        quadratic_formula_entry = '0123456789.-'
        for i in input:
            if i not in quadratic_formula_entry:
                return False
            return True

    def ShowChoice():
        global answerA
        global answerB
        try:
            answerA
        except NameError:
            print("well,  WASN'T defined yet")
        else:
            print("sure,  was defined.")
            print(type(answerA))
            if 'str' not in str(type(answerA)):
                answerA.pack_forget()
                answerA.destroy()
        try:
            answerB
        except NameError:
            print("well,  WASN'T defined yet")
        else:
            print("sure,  was defined.")
            print(type(answerB))
            if 'str' not in str(type(answerB)):
                answerB.pack_forget()
                answerB.destroy()

        # 0 - no answer
        # 1 - 1 answer
        # 2 - 2 answers
        global firstchoice
        firstchoice = v.get()
        if firstchoice == 1:
            answerA = tk.Entry(section2)
            answerA.pack()
            answerA.focus_set()

            result_entryA = section2.register(quadratic_formula_entry)
            answerA.config(validate="key", validatecommand=(result_entryA, '%S'))

        elif firstchoice == 2:
            answerA = tk.Entry(section2)
            answerB = tk.Entry(section2)
            answerA.pack()
            answerB.pack()
            answerA.focus_set()

            result_entryA = section2.register(quadratic_formula_entry)
            answerA.config(validate="key", validatecommand=(result_entryA, '%S'))

            result_entryB = section2.register(quadratic_formula_entry)
            answerB.config(validate="key", validatecommand=(result_entryB, '%S'))
        print(v.get())

    # tk.Label(section1,
    #          text="Choose your answer:",
    #          justify = tk.LEFT,
    #          padx = 20).pack()

    for val, answer in enumerate(answers):
        tk.Radiobutton(section1,
                       text=answer,
                       indicatoron=0,
                       width=20,
                       padx=20,
                       variable=v,
                       command=ShowChoice,
                       value=val).pack(anchor=tk.W)

    w = tk.Label(section2, text="", fg="black", width=20, padx=20)
    w.pack()
    # w = tk.Label(section3, text="Blue", bg="blue", fg="white")
    # w.pack()

    # section 3
    submitbutton = tk.Button(section3, text="Submit", highlightcolor="red", width=20, padx=20, command=submitAnswer)
    endbutton = tk.Button(section3, text="End", highlightcolor="red", width=20, padx=20, command=endGame)
    submitbutton.pack()
    endbutton.pack()

    section1.pack(side=tk.LEFT)
    section2.pack(side=tk.LEFT)
    section3.pack(side=tk.LEFT)
    answerWizard.pack()


# resultArray - answers calculated by computer: 3 possibilities
# ['no answer']
# [-0.33, -0.33]
# [-0.33, -0.5]

# user answers: firstchoice ,  answerA, answerB
def checkIfUserAnswerIsCorrect(resultArray):
    global answerA
    global answerB

    if firstchoice == 0 and len(resultArray) == 1:
        return True
    elif firstchoice == 1 and len(resultArray) == 2:
        # to catch a rare case when a variable is a string and cannot be a float
        try:
            if resultArray[0] == round(float(answerA), 2) and resultArray[1] == round(float(answerA), 2):
                return True
        except:
            return False

        else:
            return False
    elif firstchoice == 2 and len(resultArray) == 2:
        try:
            if (resultArray[0] == round(float(answerA), 2) or resultArray[0] == round(float(answerB), 2)) and (
                            resultArray[1] == round(float(answerA), 2) or resultArray[1] == round(float(answerB), 2)):
                return True
        except:
            return False

        else:
            return False
    else:
        return False


def calculatePointsForTheUser(resultArray, currentUser):
    if checkIfUserAnswerIsCorrect(resultArray):
        currentUser.addCorrectAnswer()
        print("correct answer")
    else:
        currentUser.addIncorrectAnswer()
        print("not correct answer")


def playQuadraticFormula():
    global welcomeframe
    global submittedFlag
    global resultArray
    welcomeframe.pack_forget()

    global currentUserNameEntry
    print(currentUserNameEntry.get())

    # Checks currentUserNameEntry is between 3 - 15 characters long and is not an empty string
    if len(currentUserNameEntry.get()) == 0:
        tk.messagebox.showinfo("Invalid Name", "No Name Entered, Please enter your name\n"
                                               "Make sure your name is between 3 - 15 characters long")
        showWelcomePage()

    elif len(currentUserNameEntry.get()) < 3:
        tk.messagebox.showinfo("Invalid Name", "Name Entered Is Too Short\n"
                                               "Make sure your name is between 3 - 15 characters long")
        showWelcomePage()

    elif len(currentUserNameEntry.get()) > 15:
        tk.messagebox.showinfo("Invalid Name", "Name Entered Is Too Long\n"
                                               "Make sure your name is between 3 - 15 characters long")
        showWelcomePage()



    else:
        global currentUser
        currentUser = User(currentUserNameEntry.get())
        # messagebox.showinfo("QuadraticFormula", "Good Luck "+str(currentUser.getUserName()))
        randomNumbersABC = get3RandomNumbers()
        # test cases
        # randomNumbersABC=[1,4,3]
        # randomNumbersABC=[1,3,-4] # ==>  x = 1, x = –4
        # randomNumbersABC=[25,-30,9] # ==>  x = 3/5
        # randomNumbersABC=[2,-4,-3] # ==>   x = 2.58, x = –0.58 rounded to two decimal places
        # randomNumbersABC=[5,6,1] # ==>  x = −0.2 or −1

        displayTaskToUser(randomNumbersABC, currentUser)
        discriminant = getDiscriminant(randomNumbersABC)
        resultArray = calculateQF(randomNumbersABC, discriminant)
        print("discriminant" + str(discriminant))
        print(resultArray)
        getAnswer()  # from the user




def printtext():
    global userNameEntry
    string = userNameEntry.get()
    print(string)


def name_characters(input):
    name_allowed_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    for i in input:
        if i not in name_allowed_chars:
            return False
        return True

def showCredits():

    tk.messagebox.showinfo(title="Credits",message="GAME DESIGN\n"
                                                   "\n"
                                                   "Created by Sebastian Mills\n"
                                                   "Made by Math Game Quizes Ltd\n"
                                                   "All rights reserved\n"
                                                   "Feel free to check out our other games at:\n"
                                                   "www.MathGameQuizes/OtherGames.co.uk")
                           
    
def about():
    tk.messagebox.showinfo(title="About", message="Last Release Date: 4th February 2020\n"

                                                  "Version: Version 1.0\n"

                                                  "Program Name: Quadratic Formula Quiz\n"

                                                  "Author: Seb010\n"

                                                  "Contact Info: programmer@yahoo.co.uk\n"

                                                  "Contact Info: 123 456 789")


def how_to_play():
    global HowToPlayFrame

    HowToPlayFrame = Toplevel(mainUserWindow)

    HowToPlayFrame.geometry("600x400")

    HowToPlayFrame.title("How To Play")

    labelfont = ("times", 18, "bold")

    title = Label(HowToPlayFrame, text="RULES")

    title.config(font=labelfont)

    title.config(height=5, width=12)

    title.place(y=5, x=250)

    Label(HowToPlayFrame, text="Hello User,").place(y=80, x=20)

    Label(HowToPlayFrame, text="Welcome To The Program, for more information about the quadratic formula please visit:").place(y=120, x=20)
    
    Label(HowToPlayFrame, text = "https://www.purplemath.com/modules/quadform.htm").place(y=140,x=20)
    

    Players = Label(HowToPlayFrame, text="Players:", font=("times", 13, "bold")).place(y=170, x=20)

    Label(HowToPlayFrame, text="1").place(y=200, x=20)

    Label(HowToPlayFrame, text="Goal:", font=("times", 13, "bold")).place(y=230, x=20)

    Label(HowToPlayFrame, text="Acheive As Many Questions Correct As You Can").place(y=260, x=20)

    Label(HowToPlayFrame, text="Setup:", font=("times", 13, "bold")).place(y=290, x=20)

    Label(HowToPlayFrame,
          text="Points Added For Correct Answers[+1]    ||   Points Taken Away For Incorrect Answers[-1]").place(y=320,
                                                                                                                 x=20)


def quit_frame():
    OptionToQuit = tk.messagebox.askyesno("Quit", "Are You Sure You Want To Quit")
    if OptionToQuit == True:
        quit()


# Welcome Frame for users / start page component

def showWelcomePage():
    global welcomeframe
    global currentUser

    currentuseranswers = 0

    try:
        currentuseranswers = currentUser.getUserTotalAnswersGiven()
    except:
        print("currentUser.getUserPoints() error")

    if currentuseranswers != 0:
        endGame()
    else:

        try:

            welcomeframe
        except NameError:
            print("well, welcomeframe WASN'T defined yet")
        else:
            print("sure, welcomeframe was defined.")
            welcomeframe.pack_forget()
            welcomeframe.destroy()

        try:
            endGameSummaryFrame.pack_forget()
            endGameSummaryFrame.destroy()
        except:
            print("endGameSummaryFrame not defined yet")
        forgetTheOlderFrames()

        welcomeframe = tk.Frame(mainUserWindow)
        

        global taskframe
        try:
            taskframe
        except NameError:
            print("well, taskframe WASN'T defined yet")
        else:
            print("sure, taskframe was defined.")
            taskframe.pack_forget()
            taskframe.destroy()

        welcomeinfo = "\n\n\n***************************\n\n Welcome into the Quadratic Formula Quiz\nTo begin please " \
                      "enter your name below and press the \"PLAY\" button \n\n*************************** "
        welcomelabel = tk.Label(welcomeframe, text=welcomeinfo)
        global currentUserNameEntry
        currentUserNameEntry = tk.Entry(welcomeframe)

        welcomelabel.pack()
        currentUserNameEntry.pack()
        currentUserNameEntry.focus_set()

        # name_characters checks that name can only contain upper and lower case letters

        name = welcomeframe.register(name_characters)
        currentUserNameEntry.config(validate="key", validatecommand=(name, '%S'))

        separatorlabel = tk.Label(welcomeframe, text="\n")
        separatorlabel.pack()

        playbutton = tk.Button(welcomeframe, text="PLAY", highlightcolor="red", command=playQuadraticFormula)
        howtoplaybutton = tk.Button(welcomeframe, text="HOW TO PLAY", highlightcolor="red", command=how_to_play)
        leaderboardsbutton = tk.Button(welcomeframe, text="LEADERBOARDS", highlightcolor="red", command=showLeaderboard)
        creditsbutton = tk.Button(welcomeframe, text="CREDITS", highlightcolor="red",command=showCredits)
        quitbutton = tk.Button(welcomeframe, text="QUIT", highlightcolor="red", command=quit)

        playbutton.pack()
        howtoplaybutton.pack()
        leaderboardsbutton.pack()
        creditsbutton.pack()
        quitbutton.pack()

        # b = tk.Button(welcomeframe,text='okay',command=printtext)
        # b.pack(side='bottom')
        welcomeframe.pack()

opendbconnection()
createDbTables()
robot = User("Robot")
robot.setPoints(100)
robot.setTotalAnswers(100)
usersOnLeaderboard = [robot]  # init, default user on the leaderboard
menubar = tk.Menu(mainUserWindow)
infomenu = tk.Menu(menubar, tearoff=0)
infomenu.add_command(label="New Game", command=showWelcomePage)
infomenu.add_command(label="End Game", command=endGameforUser)

infomenu.add_separator()
infomenu.add_command(label="Leaderboards", command=showLeaderboard)
infomenu.add_command(label="Credits",command=showCredits)

infomenu.add_separator()
infomenu.add_command(label="Quit", command=quit_frame)

menubar.add_cascade(label="Start", menu=infomenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="How to play", command=how_to_play)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)
showWelcomePage()
mainUserWindow.config(menu=menubar)
mainUserWindow.mainloop()
