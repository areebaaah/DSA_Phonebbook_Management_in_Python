import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import *


class Contact:
    def __init__(self, fname, lname, mobile_no, tag):
        self.fname = fname
        self.lname = lname
        self.mobile_no = mobile_no
        self.tag = tag

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def add_contact():
    contact = get_contact_details()

    with open("PhoneBook.csv", "a") as fptr:
        fptr.write(f"{contact.fname},{contact.lname},{contact.mobile_no},{contact.tag}\n")

    messagebox.showinfo("Contact Added", "Contact added successfully.")
    clear_screen()

def get_contact_details():
    fname = entry_fname.get()
    lname = entry_lname.get()
    mobile_no = entry_mobile.get()
    tag = entry_tag.get()
    return Contact(fname, lname, mobile_no, tag)

def display_contacts(lines):
    display_text.config(state=tk.NORMAL)
    display_text.delete(1.0, tk.END)

    display_text.insert(tk.END, "---------------------------------------------------------------------\n")
    display_text.insert(tk.END, f"|Total Number of contacts: {len(lines):2d}                  |\n")
    display_text.insert(tk.END, "---------------------------------------------------------------------\n")
    display_text.insert(tk.END, "|%-3s| %-15s%-15s%-20s%-12s|\n" % ("Sno", "First Name", "Last Name", "Contact Number", "Tag"))
    display_text.insert(tk.END, "---------------------------------------------------------------------\n")

    for count, line in enumerate(lines, 1):
        data = line.strip().split(",")
        data.extend([''] * (4 - len(data)))  # Add empty elements if the line doesn't have enough elements

        sno = f"{count} "
        first_name = f"{data[0]:<15}"
        last_name = f"{data[1]:<15}"
        contact_number = f"{data[2]:<20}"
        tag = f"{data[3]:<12}"

        display_text.insert(tk.END, f"|{sno}| {first_name}{last_name}{contact_number}{tag}|\n")

    display_text.insert(tk.END, "---------------------------------------------------------------------\n")
    display_text.config(state=tk.DISABLED)

def display():
    clear_screen()
    mode = display_var.get()
    with open("PhoneBook.csv", "r") as fptr:
        lines = fptr.readlines()
        if mode == 1:
            display_contacts(lines)
        elif mode == 2:
            display_contacts(list(reversed(lines)))
        else:
            messagebox.showerror("Error", "Invalid Selection !!!")

def delete_contact():
    with open("PhoneBook.csv", "r") as fptr:
        lines = fptr.readlines()

    if not lines:
        messagebox.showinfo("No Contacts", "No contacts to delete.")
        return

    choice = delete_var.get()

    if choice == 1:
        mobile_no = entry_delete_mobile.get()
        lines = [line for line in lines if mobile_no not in line.split(",")[2]]
    elif choice == 2:
        fname = entry_delete_fname.get().lower()
        lname = entry_delete_lname.get().lower()
        lines = [line for line in lines if fname not in line.lower() or lname not in line.lower()]
    else:
        messagebox.showerror("Error", "Wrong choice!")
        return

    with open("PhoneBook.csv", "w") as fptr:
        fptr.writelines(lines)

    messagebox.showinfo("Contact Deleted", "Contact deleted successfully.")
    clear_screen()

def search_contact():
    clear_screen()
    c = simpledialog.askinteger("Search Contact", "1. Search by name\n2. Search by Phone number\nEnter your choice:")
    flag = 0

    if c == 1:
        fname = simpledialog.askstring("Search by Name", "Enter first name: ").lower()
        lname = simpledialog.askstring("Search by Name", "Enter last name: ").lower()
        with open("PhoneBook.csv", "r") as fp:
            lines = [line for line in fp if fname in line.lower() and lname in line.lower()]
            flag = display_contacts(lines)

    elif c == 2:
        phone = simpledialog.askstring("Search by Phone Number", "Enter phone number to search: ")
        with open("PhoneBook.csv", "r") as fp:
            lines = [line for line in fp if phone in line.split(",")[2]]
            flag = display_contacts(lines)

    if not flag:
        print("\nSearch not found")

def modify_contact():
    clear_screen()
    with open("PhoneBook.csv", "r") as fptr:
        lines = fptr.readlines()

    found = False
    fname = simpledialog.askstring("Modify Contact", "Enter First Name: ").lower()
    lname = simpledialog.askstring("Modify Contact", "Enter Last Name: ").lower()

    modified_contacts = []

    for line in lines:
        data = line.strip().split(",")
        if data[0].lower() == fname and data[1].lower() == lname:
            found = True
            modify = simpledialog.askstring("Modify Contact", "Modify First Name? (y/n): ").lower()
            if modify == 'y':
                data[0] = simpledialog.askstring("Modify Contact", "Enter New First Name: ")

            modify = simpledialog.askstring("Modify Contact", "Modify Last Name? (y/n): ").lower()
            if modify == 'y':
                data[1] = simpledialog.askstring("Modify Contact", "Enter New Last Name: ")

            modify = simpledialog.askstring("Modify Contact", "Modify Mobile Number? (y/n): ").lower()
            if modify == 'y':
                data[2] = simpledialog.askstring("Modify Contact", "Enter New Mobile Number: ")

            modify = simpledialog.askstring("Modify Contact", "Modify Tag? (y/n): ").lower()
            if modify == 'y':
                data[3] = simpledialog.askstring("Modify Contact", "Enter New Tag: ")

        modified_contacts.append(','.join(data))

    if found:
        with open("PhoneBook.csv", "w") as fptr:
            fptr.write('\n'.join(modified_contacts))
        print("Contact Modified Successfully")
    else:
        print("Contact not found")

    input("\nPress Enter to continue : ")
    clear_screen()

def main_tk():
    while True:
        print("\n1: Create Contact")
        print("2: Display Directory")
        print("3: Display by tags")
        print("4: Modify Contact")
        print("5: Search Contact")
        print("6: Delete Contact")
        print("7: Exit Program")
        operation = int(input("\nChoose Operation: "))

        if operation == 1:
            add_contact()
        elif operation == 2:
            display()
        #elif operation == 3:
         #   display_by_tag()
        elif operation == 4:
            modify_contact()
        elif operation == 5:
            search_contact()
        elif operation == 6:
            delete_contact()
        elif operation == 7:
            exit(0)
        else:
            clear_screen()
            print("\nInvalid Operation!!")
            print("\nEnter 1 to 7 only")
            input("\nPress Enter to continue")
            clear_screen()


# Create main window
root = tk.Tk()
root.title("Contact Manager")

# Create and place widgets

Label(root, text="Phonebook Management", font="comicsansms 13 bold", pady=10).grid(row=0, column=0)

frame = ttk.Frame(root, padding="10")
frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_fname = ttk.Label(frame, text="First Name:")
label_lname = ttk.Label(frame, text="Last Name:")
label_mobile = ttk.Label(frame, text="Mobile Number:")
label_tag = ttk.Label(frame, text="Tag:")

entry_fname = ttk.Entry(frame)
entry_lname = ttk.Entry(frame)
entry_mobile = ttk.Entry(frame)
entry_tag = ttk.Entry(frame)

button_add = ttk.Button(frame, text="Add Contact", command=add_contact)

label_display = ttk.Label(frame, text="Display Order:")
display_var = tk.IntVar(value=1)
radio_asc = ttk.Radiobutton(frame, text="Ascending", variable=display_var, value=1)
radio_desc = ttk.Radiobutton(frame, text="Descending", variable=display_var, value=2)
button_display = ttk.Button(frame, text="Display Contacts", command=display)

button_search = ttk.Button(frame, text="Search Contact", command=search_contact)
label_search=ttk.Label(frame, text="Search for Contact:")

button_modify = ttk.Button(frame, text="Modify Contact", command=modify_contact)
label_modify= ttk.Label(frame, text="Modify your Contact:")

label_delete = ttk.Label(frame, text="Delete Option:")
delete_var = tk.IntVar(value=1)
radio_mobile = ttk.Radiobutton(frame, text="By Mobile Number", variable=delete_var, value=1)
radio_name = ttk.Radiobutton(frame, text="By Name", variable=delete_var, value=2)

label_delete_mobile = ttk.Label(frame, text="Mobile Number:")
entry_delete_mobile = ttk.Entry(frame)

label_delete_fname = ttk.Label(frame, text="First Name:")
entry_delete_fname = ttk.Entry(frame)

label_delete_lname = ttk.Label(frame, text="Last Name:")
entry_delete_lname = ttk.Entry(frame)

button_delete = ttk.Button(frame, text="Delete Contact", command=delete_contact)

label_space = ttk.Label(frame, text=" ")

display_text = tk.Text(frame, height=18, width=50, state=tk.DISABLED)

# Grid layout
label_fname.grid(row=1, column=0, sticky=tk.E)
label_lname.grid(row=2, column=0, sticky=tk.E)
label_mobile.grid(row=3, column=0, sticky=tk.E)
label_tag.grid(row=4, column=0, sticky=tk.E)

entry_fname.grid(row=1, column=1, sticky=tk.W)
entry_lname.grid(row=2, column=1, sticky=tk.W)
entry_mobile.grid(row=3, column=1, sticky=tk.W)
entry_tag.grid(row=4, column=1, sticky=tk.W)

button_add.grid(row=5, column=1, sticky=tk.W)

label_display.grid(row=1, column=2, sticky=tk.E)
radio_asc.grid(row=1, column=3, sticky=tk.W)
radio_desc.grid(row=1, column=4, sticky=tk.W)
button_display.grid(row=2, column=3, sticky=tk.W)

button_search.grid(row=4, column=3, sticky=tk.W)
label_search.grid(row=4, column=2, sticky=tk.E)

button_modify.grid(row=5, column=3, sticky=tk.W)
label_modify.grid(row=5, column=2, sticky=tk.E)

label_delete.grid(row=8, column=0, sticky=tk.E)
radio_mobile.grid(row=8, column=1, sticky=tk.W)
radio_name.grid(row=8, column=2, sticky=tk.W)

label_delete_mobile.grid(row=9, column=0, sticky=tk.E)
entry_delete_mobile.grid(row=9, column=1, sticky=tk.W)

label_delete_fname.grid(row=10, column=0, sticky=tk.E)
entry_delete_fname.grid(row=10, column=1, sticky=tk.W)

label_delete_lname.grid(row=11, column=0, sticky=tk.E)
entry_delete_lname.grid(row=11, column=1, sticky=tk.W)

button_delete.grid(row=12, column=1, sticky=tk.W)

label_space.grid(row=14, column=1)

display_text.grid(row=14, column=1, columnspan=3)

# Start the Tkinter event loop
root.mainloop()
