class TooManyArgsError(Exception):
    pass

class ContactDataAbsentError(Exception):
    pass

class ContactNameAbsentError(Exception):
    pass

class ContactAbsentError(Exception):
    pass

class ContactPresentError(Exception):
    pass

class ContactListEmptyError(Exception):
    pass

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ContactDataAbsentError:
            return "Name or phone not present, please try again."
        except ContactNameAbsentError:
            return "No name entered, please try again."
        except TooManyArgsError:
            return "Too many parameters, please try again."
        except ContactAbsentError:
            return "Contact is not found, use \"add\" command to add it."
        except ContactPresentError:
            return "Contact is already present, use \"change\" command to overwrite the phone."
        except ContactListEmptyError:
            return "Contacts list is empty."

    return inner

@input_error
def add_contact(args, contacts):
    if len(args) < 2:
        raise ContactDataAbsentError
    if len(args) > 2:
        raise TooManyArgsError
    
    name, phone = args
    
    if name in contacts:
        raise ContactPresentError

    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) < 2:
        raise ContactDataAbsentError
    if len(args) > 2:
        raise TooManyArgsError

    name, phone = args

    if name not in contacts:
        raise ContactAbsentError

    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    if len(args) < 1:
        raise ContactNameAbsentError
    if len(args) > 1:
        raise TooManyArgsError
    
    name = args[0]
    
    if name not in contacts:
        raise ContactAbsentError

    return contacts[name]

@input_error
def show_all(contacts):
    if len(contacts) == 0:
        raise ContactListEmptyError
    
    rows = []
    
    for item in contacts.items():
        name, phone = item
        rows.append(f"{name}: {phone}")
    
    return '\n'.join(rows)

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        
        if not user_input:
            print("No command entered.")
            continue
        
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()