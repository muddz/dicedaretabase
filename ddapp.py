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

import sys
import os
import sqlite3
import random

con = sqlite3.connect('daretabase.db')
cur = con.cursor()

__all__ = []
__version__ = 0.1
__date__ = '2014-04-20'
__updated__ = '2014-04-20'


#The first function that starts
#redirects to the different functions of the program
def main():

    print('''What would you like to do?
    Press 1 to show the different dare groups
    Press 2 to add a dare (not implemented yet)
    Press 3 to export a dare (not implemented yet)
    ''')

    try:
        choice = int(raw_input("What would you like to do?: "))
    except:
        choice = 0
        print("That is hardly a number, now is it?")

    if choice == 1:
        Menu().daremenu()
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    else:
        print("You didn't enter a valid choice, please try again.")
        main()


# class CLIError(Exception):
#     '''Generic exception to raise and log different fatal errors.'''
#     def __init__(self, msg):
#         super(CLIError).__init__(type(self))
#         self.msg = "E: %s" % msg
#
#     def __str__(self):
#         return self.msg
#
#     def __unicode__(self):
#         return self.msg


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# The function that actually throws all the steps on the screen
class ShowDare:

    def show(self, dare):
        print(bcolors.HEADER
              + "So, you are going to do the " + dare[2]
              + " dare. Good choice." + bcolors.ENDC)

        cur.execute("SELECT * FROM steps WHERE dare = (?)", (dare[0],))
        steps = cur.fetchall()

        for step in steps:
            print(step[3])
            raw_input(bcolors.OKGREEN
                      + "Press any key to see what you rolled"
                      + bcolors.ENDC)
            outcome = random.randrange(1, 6)
            print("Ow, you got a {0}!").format(outcome)


class Menu:

    # Info for the dare listing menu
    def daremenu(self):

        #Get all the dare types from the database
        cur.execute("SELECT * FROM 'daretypes'")
        daretypes = cur.fetchall()

        # create a list with dare numbers to check against later.
        #Might be there is a way more elegant solution for this though
        darenumbers = []

        #Print a row for each of the types
        for daretype in daretypes:
            print(bcolors.HEADER
                   + "{0} - {1}"
                   + bcolors.ENDC).format(daretype[0], daretype[1])

            # Add the number of the current type to the list
            darenumbers.append(daretype[0])

        # Get the input from the user
        daretype = raw_input("Choose a type of dare by typing a number: ")
        # Check if the input was actually a number

        try:
            daretype = int(daretype)
        except:
            print("Got shit in your eyes, you did not enter a number")

            sys.exit()

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

            try:
                dares = \
                raw_input("Which dare would you like from this category?: ")
                os.system('cls' if os.name == 'nt' else 'clear')
            except:
                print("Well, that is not really a number, now is it?")
                sys.exit()

            ShowDare().show(dare)

#initiates the __main__ function
if __name__ == "__main__":
    main()


