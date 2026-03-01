from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Name:
    def __init__(self, name):
        self.name = name

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_birthday(self, birthday):
        if self.birthday is None:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Birthday is already set.")
    
    def add_phone(self, phone):
        self.phones.append(phone)

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name.name == name:
                return record
        return None

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.records:
            if record.birthday:
                if today <= record.birthday.value < today + timedelta(days=7):
                    upcoming_birthdays.append(record.name.name)
        return upcoming_birthdays

def parse_input(user_input):
    parts = user_input.split()
    command = parts[0]
    return command, parts[1:]

def validate_phone(phone):
    if not re.match(r'^\d{10}$', phone):
        raise ValueError("Phone number must contain exactly 10 digits.")

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Incorrect number of arguments."
    return wrapper

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    try:
        record.add_birthday(birthday)
        return f"Birthday for {name} added."
    except ValueError as e:
        return str(e)

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    if record.birthday:
        return f"Birthday of {name} is {record.birthday.value.strftime('%d.%m.%Y')}."
    return f"No birthday information for {name}."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays next week."
    return "Upcoming birthdays next week: " + ", ".join(upcoming)

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        validate_phone(phone)
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    if old_phone not in record.phones:
        return f"Phone {old_phone} not found for {name}."
    validate_phone(new_phone)
    record.phones.remove(old_phone)
    record.add_phone(new_phone)
    return f"Phone for {name} updated."

@input_error
def phone_contact(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"Contact {name} not found."
    return f"Phones for {name}: " + ", ".join(record.phones)

@input_error
def show_all_contacts(book):
    if not book.records:
        return "No contacts in the address book."
    return "\n".join([record.name.name for record in book.records])

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(phone_contact(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()