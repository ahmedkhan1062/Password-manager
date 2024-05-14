import random
import string
import pyperclip
import tkinter
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import font
from tkinter import messagebox
import pandas
import json

#Colour pallete
very_dark = "#070A52"
dark= "#D21312"
medium = "#ED2B2A"
light = "#F15A59"

#Create window
window = tkinter.Tk()
window.title("Password Manager")
window.config(padx=75, pady=50, bg = very_dark)
window.minsize(500,500)


#Read in data file otherwise create new file in correct format
try:
        df = pandas.read_csv(r"\Users\Alienware 15\Documents\Udemy Projects\Project 13 - Password manager\accountdata.csv")
except FileNotFoundError:
        df = pandas.DataFrame(columns=["Website","Username", "Password"])



#------------------Functions--------------------#

#Function check if account already exists
def searchAccount():
    key = ib_siteName.get().lower()
    try:
       with open(r"\Users\Alienware 15\Documents\Udemy Projects\Project 13 - Password manager\data.json", "r") as data_file:
                     accountData = json.load(data_file)
    
    except json.decoder.JSONDecodeError:
              accountData = {}
    
    finally:
           if key in accountData:
                  
              #Clear username text box and input the found username
              ib_userName.delete(0, tkinter.END)
              ib_userName.insert(0, accountData[key]["Username"])

              #Clear password text box and input the found password
              ib_pass.delete(0, tkinter.END)
              ib_pass.insert(0, accountData[key]["Password"])
           
           else:
              #Clear password and username text boxes
              ib_userName.delete(0, tkinter.END)
              ib_pass.delete(0, tkinter.END)
              messagebox.showerror("Account Not Found", "This account has not been added")
              


#Function to generate random password
def genPassword():
    
    #Define the character sets for the password
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?~"

    #Combine all character sets
    all_characters = lowercase_letters + uppercase_letters + digits + special_characters

    #Generate a password by selecting characters randomly
    password = ''.join(random.choice(all_characters) for _ in range(12))
    
    #Copy password to clipboard
    pyperclip.copy(password)

    #Clear password text box and input the new password
    ib_pass.delete(0, tkinter.END)
    ib_pass.insert(0, password)


#Function to add newly entered account details to csv file
def addData():

    global df

    siteName_data = ib_siteName.get().lower()
    userName_data = ib_userName.get()
    password_data = ib_pass.get()

    
    if not siteName_data:
           messagebox.showerror("Website name Incomplete!", "Please make sure to enter a website name")
           return
    if not userName_data:
           messagebox.showerror("Username Incomplete!", "Please make sure to enter a username")
           return
    if not password_data:
           messagebox.showerror("Password Incomeplete!", "Please make sure to enter a password")
           return
    
    confirm = messagebox.askokcancel(title = f"Save {siteName_data} account", message = f"Are you sure you would like to add the following details?: \nWebsite: {siteName_data}\nUsername: {userName_data}\nPassword: {password_data}")

    if confirm:
        #Create dictionary entry out of account details entered
        jsonStore = {siteName_data:
                     {  'Username': userName_data,
                        'Password': password_data,
                        }
                     }
        
        #Try to open and load file into dictionary
        try:
              with open(r"\Users\Alienware 15\Documents\Udemy Projects\Project 13 - Password manager\data.json", "r") as data_file:
                     data = json.load(data_file)

        #If file is empty, create empty dictionary
        except json.decoder.JSONDecodeError:
              data = {}

        #Add the new data to the dictionary
        finally:
              data.update(jsonStore)
              
        #Write the updated data to the json file      
        with open(r"\Users\Alienware 15\Documents\Udemy Projects\Project 13 - Password manager\data.json", "w") as data_file:
              json.dump(data,data_file, indent=4)

       

#------------------UI Design--------------------#


#Create background image
img = PhotoImage(file=r"\Users\Alienware 15\Documents\Udemy Projects\Project 13 - Password manager\redlock.png")
canvas = Canvas(width = 250, height=310,highlightthickness=0, bg=  very_dark)
canvas.create_image(125,150,image = img)

#Site name label
l_siteName = tkinter.Label(text="Site name", bg= very_dark, fg=medium, font=font.Font(family="Inter UI", size=14))
l_siteName.grid(column=1,row=2)

#Site name input
frm_siteName = tkinter.Frame( padx=5, pady=10, bg = very_dark)
frm_siteName.grid(column=2,row=2)
ib_siteName = tkinter.Entry(frm_siteName, width= 26, bg= light,font=font.Font(family="Inter UI", size=11))
ib_siteName.pack()

#Search Button
frm_search = tkinter.Frame(padx=5, pady=5, bg = very_dark)
frm_search.grid(column=3,row=2, columnspan=2)
btn_search = tkinter.Button(frm_search, text="(Find)", width= 14, bg= medium, fg=very_dark, highlightthickness=0, relief="flat", command=searchAccount)
btn_search.pack() 

#User name label
l_username = tkinter.Label(text="Username/Email     ", bg= very_dark, fg=medium, font=font.Font(family="Inter UI", size=14))
l_username.grid(column=1,row=3)

#User name input
frm_userName = tkinter.Frame(padx=5, pady=10, bg = very_dark)
frm_userName.grid(column=2,row=3, columnspan= 2)
ib_userName = tkinter.Entry(frm_userName, width=40, bg= light,font=font.Font(family="Inter UI", size=11))
ib_userName.pack()



#password label
l_pass = tkinter.Label(text="Password", bg= very_dark, fg=medium, font=font.Font(family="Inter UI", size=14))
l_pass.grid(column=1,row=4)

#password input
frm_pass = tkinter.Frame(padx=5, pady=10, bg = very_dark)
frm_pass.grid(column=2,row=4)
ib_pass = tkinter.Entry(frm_pass, width=26, bg=light, font=font.Font(family="Inter UI", size=11))
ib_pass.pack()

#Generate Button
frm_gen = tkinter.Frame(padx=5, pady=5, bg = very_dark)
frm_gen.grid(column=3,row=4, columnspan=2)
btn_gen = tkinter.Button(frm_gen, text="Generate", width= 14, bg= medium, fg=very_dark, highlightthickness=0, relief="flat", command=genPassword)
btn_gen.pack() 


#Add Button
frm_add = tkinter.Frame(padx=5, pady=10, bg = very_dark)
frm_add.grid(column=2,row=5, columnspan=2)
btn_add = tkinter.Button(frm_add, text="Add", width= 45, bg= medium, fg=very_dark, highlightthickness=0, relief= "flat", command=addData)
btn_add.pack()

canvas.grid(column=1,row=1, columnspan=3)

window.mainloop()