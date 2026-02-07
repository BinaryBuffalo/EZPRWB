import sys

def replace_line(filename, keyword, replacement):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        with open(filename, 'w') as file:
            for line in lines:
                if keyword in line:
                    file.write(replacement + '\n')
                else:
                    file.write(line)

        print(f"Lines containing '{keyword}' replaced in {filename}.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")


def get_allowed_hosts():
    while True:
        try:
            user_input = input("How many hosts would you like to add to ALLOWED_HOSTS? (Press Enter for default 2) ")
            num_hosts = int(user_input) if user_input else 2
            if num_hosts <= 0:
                print("Please enter a positive number.")
            elif num_hosts > 20:
                print("The maximum allowed hosts is 20. Please enter a number less than or equal to 20.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")
    if num_hosts == 1:
        host_input = input("Enter the host (e.g., 'example.com'): ")
        allowed_hosts = f"ALLOWED_HOSTS = ['{host_input}']"
    elif num_hosts > 1:
        allowed_hosts = "ALLOWED_HOSTS = ["
        for i in range(num_hosts):
            host_input = input(f"Enter host {i + 1}: ")
            allowed_hosts += f"'{host_input}', "
        allowed_hosts = allowed_hosts[:-2] + "]"  # Remove the trailing comma and space
    else:
        allowed_hosts = "ALLOWED_HOSTS = ['*']"
    return allowed_hosts


name = input("Project Folder name :")
one_content = name + "/" + name.lower() + "/" + "settings.py"
two_content = get_allowed_hosts() # returns allowed domains from user input in list displayed as python string
replace_line(one_content, "ALLOWED_HOSTS", two_content)