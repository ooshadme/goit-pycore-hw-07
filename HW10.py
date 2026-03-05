from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date_obj)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        self.phones.remove(phone_obj)
        self.phones.append(Phone(new_phone))

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        raise ValueError("Phone not found.")

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Birthday is already set.")
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        birthday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday
            else "Not set"
        )
        return f"Name: {self.name.value}, Phones: {phones}, Birthday: {birthday}"


class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []

        for record in self.records.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(
                        year=today.year + 1
                    )

                delta = (birthday_this_year - today).days

                if 0 <= delta <= 7:
                    congratulation_date = birthday_this_year

                    # если выпадает на выходной — переносим на понедельник
                    if congratulation_date.weekday() >= 5:
                        congratulation_date += timedelta(
                            days=7 - congratulation_date.weekday()
                        )

                    upcoming.append(
                        {
                            "name": record.name.value,
                            "date": congratulation_date.strftime("%d.%m.%Y"),
                        }
                    )

        return upcoming


def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0].lower()
    return command, parts[1:]


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
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."


@input_error
def phone_contact(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    phones = ", ".join(p.value for p in record.phones)
    return phones if phones else "No phones found."


@input_error
def show_all(book):
    if not book.records:
        return "No contacts."
    return "\n".join(str(record) for record in book.records.values())


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Birthday not set."


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(
        f"{item['name']} — {item['date']}" for item in upcoming
    )


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

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
            print(show_all(book))

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