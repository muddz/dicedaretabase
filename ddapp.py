#!/usr/local/bin/python2.7
# encoding: utf-8
'''
dicedaretabase -- Dice Dare CLI app

dicedaretabase is small CLI application which lets you do different kind of dice dares.

It defines classes_and_methods

@author:     Muddz

@copyright:  2014 Muddz. All rights reserved.

@license:    license

@deffield    updated: 20-4-2014
'''

import xml.etree.ElementTree as ET
import sys
import os
import sqlite3
import random
import collections

con = sqlite3.connect('daretabase.db')
cur = con.cursor()

__all__ = []
__version__ = 0.1
__date__ = '2014-04-20'
__updated__ = '2014-04-20'


#The first function that starts
#redirects to the different functions of the program
def main():

    #Create database if it doesn't exist.
    cur.execute("""CREATE TABLE IF NOT EXISTS daretypes (id INTEGER PRIMARY KEY, name TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS dares(
    id INTEGER PRIMARY KEY, daretype INTEGER, name TEXT, author TEXT,
    FOREIGN KEY (daretype) REFERENCES daretypes(id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS steps(
    id INTEGER PRIMARY KEY, dare INTEGER, stepnr INTEGER, text TEXT,
    FOREIGN KEY (dare) REFERENCES dares(id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS outcomes(
    id INTEGER PRIMARY KEY, dare INTEGER, roll INTEGER, outcome TEXT,
    step INTEGER, FOREIGN KEY (dare) REFERENCES dares(id),
    FOREIGN KEY (step) REFERENCES steps(id))""")



    print('''What would you like to do?
    Press 1 to show the different dare groups
    Press 2 to add a dare
    Press 3 to export a dare
    ''')

    choice = raw_input("What would you like to do?: ")
    choice = toInt(choice)

    if choice == 1:
        Menu().showDares()
    elif choice == 2:
        Menu().addDareMenu()

    elif choice == 3:
        Menu().exportDareMenu()
    else:
        main()

#this function tries to convert a users input to int
#If it does not work it throws an exception, also all the tables.
# (╯°□°）╯︵ ┻━┻
def toInt(i):
    try:
        i = int(i)
    except:
        print("Got shit in your eyes? You did not enter a number, please do.")
    return i


# Colors and stuff
class bcolors:
    # Got rid of the colours as windows gives zero shits about them
    #HEADER = '\033[95m'
    HEADER = ""
    # OKBLUE = '\033[94m'
    OKBLUE = ""
    # OKGREEN = '\033[92m'
    OKGREEN = ""
    # WARNING = '\033[93m'
    WARNING = ""
    # FAIL = '\033[91m'
    FAIL = ""
    # ENDC = '\033[0m'
    ENDC = ""


# This function tries to export dice dares to an XML file
class ExportDare:

    def export(self):
        print("Which dare do you want to export?")
        choice = Menu().chooseTypeMenu()

        cur.execute("SELECT * FROM dares WHERE id = (?)", (choice,))
        d = cur.fetchone()

        cur.execute("SELECT * FROM steps WHERE dare = (?)", (choice,))
        steps = cur.fetchall()

        # Build the XML file

        dare = ET.Element("dare")

        dare.set("name", d[2])
        dare.set("author", d[3])

        for s in steps:
            step = ET.SubElement(dare, "step")
            # stepnr = ET.SubElement(step, str(s[2]))
            step.set("id", str(s[2]))
            # step.text = s[3]
            step.set("text", s[3])

            cur.execute("SELECT * FROM outcomes WHERE dare = (?) and step = (?)",
                        (d[0], s[2]))
            outcomes = cur.fetchall()

            for o in outcomes:
                outcome = ET.SubElement(step, "outcome")
                outcome.text = str(o[3])

                # roll = ET.SubElement(outcome, "roll")
                outcome.set = ("roll", str(o[2]))

                outcome.set = ("step", str(o[4]))

        tree = ET.ElementTree(dare)
        tree.write("dare.xml")


# The function that actually throws all the steps on the screen
class ShowDare:

    def show(self, dare):

        cur.execute("SELECT * FROM steps WHERE dare = (?)", (dare,))
        steps = cur.fetchall()

        for step in steps:
            if step[2] == 1:
                raw_input(bcolors.OKGREEN
                          + "Welcome to this dare, press enter if you are ready"
                          + bcolors.ENDC)
            roll = random.randrange(1, 6)
            cur.execute("SELECT outcome FROM outcomes WHERE dare = (?) and step = (?)",
                        (dare, step[2]))

            outcome = cur.fetchone()


            if "_X_" in step[3]:

                #Replace the _X_ in the step string
                add = step[3].replace('_X_', outcome[0])
                print("""You rolled a {0}
                that means you have to {1}!""")\
                .format(roll, add)
            else:
                #Display the step
                print(step[3])
                print("""You rolled a {0}, that means you got: {1}!""")\
                .format(roll, outcome[0])


            raw_input(bcolors.OKBLUE
                      + "Ready for the next step? lets go!"
                      + bcolors.ENDC)


class AddDare:

    def addDare(self):
        print(bcolors.HEADER
              + "What kind of dare do you want to add?"
              + bcolors.ENDC)

        # Asks for the list of dare types and displays the menu.
        darenumbers = Menu().listDareTypes()
        choice = raw_input("I choose number:")
        choice = toInt(choice)
        if choice in darenumbers:
            print("You choose number {0}, lets get started shall we?") \
            .format(choice)
        else:
            print("You didn't enter a valid choice, please do next time.")
            self.addDare()
        darename = raw_input("And how would you want to call the dice dare?: ")
        nickname = raw_input("And what is your (nick)name?: ")
        cur.execute("INSERT INTO dares VALUES (NULL, ?, ?, ?)",
                    (choice, darename, nickname))
        dareid = cur.lastrowid

        print(
              """We are going to go through each step of the dice dare,
              For each step I will ask you how to call the step and
              What the possible outcomes are.
              Right now, every step needs 6 outcomes.""")

        # declare a bool to check if there are any more steps coming after this
        stop = False

        stepnr = 1
        while not stop:
            print(
            """If you want to include a number in the dare, type _X_
            So ex: 'Run around for _X_ KM'
            If you do so, remember to only give outcomes that fit the scentence
            """)
            steptext = raw_input("For this step, the dare-y needs to: ")

            cur.execute("INSERT INTO steps VALUES (NULL, ?, ?, ?)",
                        (dareid, stepnr, steptext))

            print("Great idea! And what are the outcomes going to be?")
            for i in range(1, 7):
                text = raw_input("What does the dare-y have to do when rolling a {0}: ".format(i))

                cur.execute("INSERT INTO outcomes VALUES (NULL, ?, ?, ?, ?)",
                        (dareid, i, text, stepnr))

            cont = raw_input(
            """If this was the last step, type 'q' without quotes,
            If you want to continue adding steps, press any other key.""")

            if cont == "q":
                stop = True
            else:
                stepnr += 1
        con.commit()



class Menu:

    #Lists the current dare types and returns a list with ints corresponding
    #the types in de daretabase.
    def listDareTypes(self):

        #Get all the dare types from the database
        cur.execute("SELECT * FROM 'daretypes'")
        daretypes = cur.fetchall()

        #Create a list with dare numbers to check against.
        #Might be there is a way more elegant solution for this though
        darenumbers = []

        #Print a row for each of the types
        for daretype in daretypes:
            print(bcolors.HEADER
                   + "{0} - {1}"
                   + bcolors.ENDC).format(daretype[0], daretype[1])

            # Add the number of the current type to the list
            darenumbers.append(daretype[0])

        return darenumbers

    # Info for the dare listing menu
    def chooseTypeMenu(self):

        # Asks for the list of dare types and displays the menu.
        darenumbers = self.listDareTypes()

        # Get the input from the user
        daretype = raw_input("Choose a type of dare by typing a number: ")
        # Check if the input was actually a number
        #try to convert to int
        daretype = toInt(daretype)

        if daretype in darenumbers:
            # Clear the screen again and display the different dare types

            os.system('cls' if os.name == 'nt' else 'clear')
            cur.execute(
                        "SELECT * FROM dares WHERE daretype = (?)",
                        (daretype,))
            dares = cur.fetchall()
            for dare in dares:
                print(bcolors.HEADER
                      + "{0} - {1}"
                      + bcolors.ENDC).format(dare[0], dare[2])

            dare = raw_input("Which dare would you like from this category?: ")
            dare = toInt(dare)
            return dare

    def showDares(self):

        dare = Menu.chooseTypeMenu(self)
        ShowDare().show(dare)

    def addDareMenu(self):
        print("""So you want to add a new dare to the daretabase? Great!
If you like to share your dare afterwards, you can do so by exporting
it to a file and emailing or PMing it to me.
""")
        AddDare().addDare()

    def exportDareMenu(self):

        ExportDare().export()



#initiates the __main__ function
if __name__ == "__main__":
    main()