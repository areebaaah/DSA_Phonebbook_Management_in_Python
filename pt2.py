import os

class Contact:
    def __init__(self, fname, lname, mobile_no, tag):
        self.fname = fname
        self.lname = lname
        self.mobile_no = mobile_no
        self.tag = tag

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_contact_details():
    fname = input("Enter First Name: ")
    lname = input("Enter Last Name: ")
    mobile_no = input("Enter Mobile Number: ")
    tag = input("Enter Tag (Enter 'Other' for nothing): ")
    return Contact(fname, lname, mobile_no, tag)

def add_contact():
    clear_screen()
    contact = get_contact_details()
    
    with open("PhoneBook.csv", "a") as fptr:
        fptr.write(f"{contact.fname},{contact.lname},{contact.mobile_no},{contact.tag}\n")

    input("Contact added. Press Enter to continue.")
    clear_screen()

def directory_info():
    with open("PhoneBook.csv", "r") as fptr:
        return sum(1 for _ in fptr)

def tag_info(tag):
    with open("PhoneBook.csv", "r") as fptr:
        return sum(1 for line in fptr if tag.lower() in line.lower().split(",")[-1])

def display_contacts(lines):
    lines_list = list(lines)  # Convert the iterator to a list
    print("---------------------------------------------------------------------")
    print(f"|Total Number of contacts : {len(lines_list):2d}                  |")
    print("---------------------------------------------------------------------")
    print("|%-3s| %-15s%-15s%-20s%-12s|" % ("Sno", "First Name", "Last Name", "Contact Number", "Tag"))
    print("---------------------------------------------------------------------")

    for count, line in enumerate(lines_list, 1):
        data = line.strip().split(",")
        data.extend([''] * (4 - len(data)))  # Add empty elements if the line doesn't have enough elements

        sno = f"{count} "
        first_name = f"{data[0]:<15}"
        last_name = f"{data[1]:<15}"
        contact_number = f"{data[2]:<20}"
        tag = f"{data[3]:<12}"

        print(f"|{sno}| {first_name}{last_name}{contact_number}{tag}|")

    print("---------------------------------------------------------------------")
    input("\n\nPress Enter to continue : ")
    clear_screen()

def display():
    clear_screen()
    mode = int(input("1: View by Time Created (Ascending)\n2: View by Time Created (Descending)\nChoose Display Mode: "))
    n = directory_info()

    with open("PhoneBook.csv", "r") as fptr:
        lines = fptr.readlines()
        if mode == 1:
            display_contacts(lines)
        elif mode == 2:
            display_contacts(list(reversed(lines)))
        else:
            print("Invalid Selection !!!")

def display_by_tag():
    clear_screen()
    tag = input("Enter Tag: ").lower()
    with open("PhoneBook.csv", "r") as fptr:
        lines = [line for line in fptr if tag in line.lower().split(",")[-1]]
        display_contacts(lines)

def search_contact():
    clear_screen()
    c = int(input("1. Search by name\n2. Search by Phone number\nEnter your choice: "))
    flag = 0

    if c == 1:
        fname = input("Enter first name: ").lower()
        lname = input("Enter last name: ").lower()
        with open("PhoneBook.csv", "r") as fp:
            lines = [line for line in fp if fname in line.lower() and lname in line.lower()]
            flag = display_contacts(lines)

    elif c == 2:
        phone = input("Enter phone number to search: ")
        with open("PhoneBook.csv", "r") as fp:
            lines = [line for line in fp if phone in line.split(",")[2]]
            flag = display_contacts(lines)

    if not flag:
        print("\nSearch not found")

def delete_contact():
    clear_screen()
    with open("PhoneBook.csv", "r") as fptr:
        lines = fptr.readlines()

    if not lines:
        print("No contacts to delete.")
        input("Press Enter to continue:")
        clear_screen()
        return

    with open("helper.csv", "w") as fptr1:
        choice = int(input("1. Deletion through mobile number\n2. Deletion through name\nEnter your choice: "))

        if choice == 1:
            mobile_no = input("Enter CONTACT's mobile_no: ")
            lines = [line for line in lines if mobile_no not in line.split(",")[2]]

        elif choice == 2:
            fname = input("Enter CONTACT's fname: ").lower()
            lname = input("Enter CONTACT's lname: ").lower()
            lines = [line for line in lines if fname not in line.lower() or lname not in line.lower()]

        else:
            print("Wrong choice!")
            input("Press Enter to continue")
            clear_screen()
            return

        with open("PhoneBook.csv", "w") as fptr:
            fptr.writelines(lines)

        print("Contact(s) Deleted Successfully")

    input("Press Enter:")
    clear_screen()


def modify_contact():
    clear_screen()
    with open("PhoneBook.csv", "r") as fptr:
        lines = fptr.readlines()

    found = False
    fname = input("Enter the name of Contact to modify:\nEnter First name: ").lower()
    lname = input("Enter Last name: ").lower()

    modified_contacts = []

    for line in lines:
        data = line.strip().split(",")
        if data[0].lower() == fname and data[1].lower() == lname:
            found = True
            modify = input("Modify First Name? <y/n>: ").lower()
            if modify == 'y':
                data[0] = input("Enter New First name: ")

            modify = input("Modify Last Name? <y/n>: ").lower()
            if modify == 'y':
                data[1] = input("Enter New Last name: ")

            modify = input("Modify Mobile Number? <y/n>: ").lower()
            if modify == 'y':
                data[2] = input("Enter New Mobile Number: ")

            modify = input("Modify Tag? <y/n>: ").lower()
            if modify == 'y':
                data[3] = input("Enter New Tag: ")

        modified_contacts.append(','.join(data))

    if found:
        with open("PhoneBook.csv", "w") as fptr:
            fptr.write('\n'.join(modified_contacts))
        print("Contact Modified Successfully")
    else:
        print("Contact not found")

    input("\nPress Enter to continue : ")
    clear_screen()


def main():
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
        elif operation == 3:
            display_by_tag()
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

if __name__ == "__main__":
    main()
