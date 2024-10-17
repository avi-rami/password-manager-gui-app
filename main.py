from tkinter import *
from tkinter import messagebox
from random import randint,choice,shuffle
import pyperclip
import json

def search():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)  # try to open file and read old data
            messagebox.showinfo(title=f"{website}",message=f"Email: {data[website]["email"]}\nPassword: {data[website]["password"]}")
    except KeyError:
        messagebox.showwarning(title="Error",message=f"The website is not in your data.")
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message=f"No data file found.")
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0,END)
    password_entry.insert(0,password)
    # copies the password to clipboard for immediate use
    pyperclip.copy(password)
    return password


def save_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) <= 0 or len(email) <= 0 or len(password) <= 0:
        messagebox.showwarning(title="Oops",message="Please fill out all of the fields.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}\nPassword: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", mode="r") as data_file:
                    data = json.load(data_file) # try to open file and read old data
                    data.update(new_data) # update old data with new data
                with open("data.json", mode="w") as data_file:
                    json.dump(data, data_file, indent=4) # write the updated data
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4) # create new file and write new data
            website_entry.delete(0,END)
            password_entry.delete(0,END)

window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

# logo row
canvas = Canvas(width=200, height=200, highlightthickness=0)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, columnspan=3)

# website entry row
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_entry = Entry(width=20)
website_entry.focus()
website_entry.grid(row=1, column=1)
search_button = Button(text="Search", command=search, width=10)
search_button.grid(row=1, column=2)

# email entry row
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
email_entry = Entry(width=35)
email_entry.insert(0,"ramiavi2@gmail.com") # currently holds my most commonly used email
email_entry.grid(row=2, column=1, columnspan=2)

# password entry / generation row
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_entry = Entry(width=20)
password_entry.grid(row=3, column=1)
generate_button = Button(text="Generate Password", command=generate_password, width=10)
generate_button.grid(row=3, column=2)

# add button row
add_button = Button(text="Add", command=save_data, width=33)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
