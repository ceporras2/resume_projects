from string import ascii_uppercase, digits
from datetime import datetime
from tabulate import tabulate
from random import choice
from sys import exit
import json

# Constants
HOME_MENU_OPTIONS = ['m', 'e']
MAIN_MENU_OPTIONS = list(range(1, 6))
UPDATE_MENU_OPTIONS = list(range(1, 5))
DUE_DATE_FORMAT = '%m/%d/%y %H:%M:%S'

class InputValidation:

    @staticmethod
    def home_menu_validation(user_input):
        """
        Checks if the user input for the home menu is valid.
        Parameters:
            user_input (str): The user's input for the home menu option.
        Returns:
            int: 0 if the user input is a valid menu option ('m' or 'e'), 1 otherwise.
        """
        return 0 if isinstance(user_input, str) and user_input in HOME_MENU_OPTIONS else 1

    @staticmethod
    def main_menu_validation(user_input):
        """
        Checks if the user input for the main menu is valid.
        Parameters:
            user_input (int): The user's input for the main menu option.
        Returns:
            int: 0 if the user input is a valid menu option (an integer between 1 and 5, inclusive), 1 otherwise.
        """
        return 0 if isinstance(user_input, int) and user_input in MAIN_MENU_OPTIONS else 1

    @staticmethod
    def update_menu_validation(user_input):
        """
        Checks if the user input for the update menu is valid.
        Parameters:
            user_input (int): The user's input for the update menu option.
        Returns:
            int: 0 if the user input is a valid menu option (an integer between 1 and 4, inclusive), 1 otherwise.
        """
        return 0 if isinstance(user_input, int) and user_input in UPDATE_MENU_OPTIONS else 1


class MenuOptions:

    def home_screen(tasks):
        """
        Displays the home screen of the school to-do list application.
        Args:
            tasks (ToDoList): An instance of the ToDoList class.
        Returns:
            str or int: The user's choice as a string if it is 'm' or 'e', or an integer if it is a valid menu option.
                If the user enters an invalid choice, a message is printed and 0 is returned.
        Raises:
            ValueError: If the user enters a non-integer value for the menu option.
        Prints:
            - The school to-do list header.
            - The current tasks in the to-do list.
            - A prompt for the user to choose between going to the main menu or exiting the application.
        """
        print("""
                            SCHOOL TO DO LIST
            """)
        tasks.print_tasks()

        try:
            user_choice = input("Main Menu(m) or Exit(e): ")

            if InputValidation.home_menu_validation(user_choice):
                print("Please enter a valid choice.")
                return 0
            else:
                return user_choice

        except ValueError as err:
            print(f"Error: {err}")
            return 0

    def main_menu():
        """
        Displays the main menu and prompts the user to enter an option.
        The menu options include printing the to-do list, adding a task to the list, removing a task from the list, updating a task, or going back to the home screen.
        Returns:
            int or None: The user's choice as an integer, or None if the user chooses to go back.
                If the user enters an invalid option, a message is printed and 0 is returned.
        Raises:
            ValueError: If the user enters a non-integer value for the menu option.
        """
        print("""
              MAIN MENU
            """)
        print("=====================================")

        print("1) Print to-do list\n"
              "2) Add task to list\n"
              "3) Remove task from list\n"
              "4) Update task\n"
              "5) Home\n")

        try:
            user_choice = int(input("Enter an option: "))

            if InputValidation.main_menu_validation(user_choice):
                print("Please enter a valid integer.")
                return 0
            else:
                return user_choice

        except ValueError as err:
            print(f"Error: {err}")
            return 0

    def update_task_menu():
        """
        Displays the update task menu and prompts the user to enter an option.
        The menu options include updating the task description, category, status, or due date, or going back to the previous menu.
        Returns:
            int or None: The user's choice as an integer, or None if the user chooses to go back.
                If the user enters an invalid option, a message is printed and 0 is returned.
        Raises:
            ValueError: If the user enters a non-integer value for the menu option.
        """
        print("""
            UPDATE TASK
            """)
        print("=====================================")

        print("1) Task Description\n"
              "2) Task Category\n"
              "3) Task Status\n"
              "4) Task Due Date\n"
              "5) Back\n")

        try:
            user_choice = int(input("Enter an option: "))

            if user_choice == 5:
                return

            if InputValidation.update_menu_validation(user_choice):
                print("Please enter a valid integer.")
                return 0
            else:
                return user_choice

        except ValueError as err:
            print(f"Error: {err}")
            return 0


class ToDoList:

    def __init__(self):
        self.tasks_dict = {}

    def generate_random_id(self):
        """
        Generates a random alphanumeric id that is not already in use as a task_id.
        Returns:
            str: A unique random alphanumeric id.
        """
        # Generate a random id
        random_id = ''.join(choice(ascii_uppercase + digits) for _ in range(6))

        # Ensure the generated id is unique by checking against existing task_ids
        while random_id in self.tasks_dict:
            random_id = ''.join(choice(ascii_uppercase + digits) for _ in range(6))
        return random_id

    def add_task_to_dict(self, new_task):
        """
        Adds a new task to the tasks_dict dictionary.
        Args:
            new_task (dict): Dictionary containing information about the new task.
        Returns:
            str: The task ID assigned to the new task.
        """
        # Generate a unique task ID
        new_task_id = self.generate_random_id()

        # Add the new task to the tasks_dict with the generated task ID as the key
        self.tasks_dict[new_task_id] = new_task

        # Return the assigned task ID
        return new_task_id

    def is_task_valid(self, task):
        """
        Checks if a task is valid.
        Args:
            task (dict): Dictionary containing task information.           
        Returns:
            bool: True if the task is valid, False otherwise.           
        Prints error messages if the task is not valid, indicating reasons such as
        an invalid date format, a missing 'date' key, or a due date that has already passed.
        """
        if 'date' in task:
            try:
                # Parse the due date from the task and convert it to a datetime object
                due_date = datetime.strptime(task['date'], DUE_DATE_FORMAT)
                current_date = datetime.now()

                # Check if the due date is in the future (not already passed)
                if due_date >= current_date:
                    return True
                else:
                    # Print an error message if the due date has already passed
                    print("Error: Due date has already passed. Task is not valid.")
            except ValueError as e:
                # Print an error message if there is an issue parsing the due date
                print(f"Error: {e}")
                return False
        else:
            # Print an error message if the 'date' key is not present in the task dictionary
            print("Error: 'date' key not found in task dictionary. Task is not valid.")

        # Return False if any validation checks fail
        return False

    def new_task(self):
        """
        Creates a new task and adds it to the tasks_dict dictionary.
        Prompts the user for task details including description, category, status, and due date.
        The due date should be in the format MM/DD/YY HH:MM:SS.
        Args:
            self (ToDoList): The ToDoList instance.   
        Returns:
            None   
        Prints a success message with the generated task ID if the new task is valid and added successfully.
        """
        # Display information for creating a new task
        print("""
        NEW TASK INFORMATION
        """)
        print("=====================================")

        # Prompt user for task details
        description = input("Task Description: ")
        category = input("Task Category: ")
        status = input("Task Status: ")
        
        # Prompt user for due date in the specified format
        print("Due date format should be MM/DD/YY HH:MM:SS")
        date = input("Task Due Date: ")

        # Create a new task dictionary with user-provided information
        new_task = {"description": description,
                    "category": category,
                    "status": status,
                    "date": date}

        # Check if the new task is valid
        if self.is_task_valid(new_task):
            # Add the new task to the dictionary and obtain the generated task ID
            task_id = self.add_task_to_dict(new_task)
            
            # Display success message with the generated task ID
            print(f"Added task successfully. Task ID: {task_id}")

    def remove_task(self):
        """
        Removes a task from the tasks dictionary based on the provided task_id.
        Prints a success message if the task is removed, or an error message if the task_id does not exist.
        """
        # Check if the tasks dictionary is empty
        if not self.tasks_dict:
            print("Tasks list is empty.")

        # Prompt user for the task_id to be removed
        task_id = input("\nEnter the id of the task you want to remove: ")

        # Check if the task_id exists in the tasks dictionary
        if task_id in self.tasks_dict:
            # Remove the task if the task_id matches
            del self.tasks_dict[task_id]
            print("Removed task successfully.")
        else:
            # Print an error message if the task_id does not exist
            print("Task with the provided id does not exist.")

    def update_task(self):
        """
        Updates a task in the tasks_dict dictionary based on the provided task_id.
        Args:
            task_id (str): The ID of the task to be updated.
        Returns:
            None
        Note: The method assumes that the tasks_dict dictionary is already populated with tasks.
        """
        # Prompt user for the task_id to be updated
        task_id = input("\nEnter the id of the task you want to update: ")

        # Check if the task_id exists in the tasks_dict
        if task_id in self.tasks_dict:
            # Get the field to update from the user
            task_to_update = MenuOptions.update_task_menu()

            # Check if the user chose to go back
            if not task_to_update:
                return

            # Create a copy of the current task to modify
            new_task = self.tasks_dict[task_id].copy()

            # Update the chosen field based on user input
            if task_to_update == 1:
                new_task["description"] = input("New Task Description: ")
            elif task_to_update == 2:
                new_task["category"] = input("New Task Category: ")
            elif task_to_update == 3:
                new_task["status"] = input("New Task Status: ")
            elif task_to_update == 4:
                print("Due date format should be MM/DD/YY HH:MM:SS")
                new_task["date"] = input("New Task Due Date: ")

            # Update the task in-place in the tasks_dict
            self.tasks_dict[task_id] = new_task

            print("Task updated successfully.")
        else:
            print("Task with the provided id does not exist.")

    def load_tasks(self, file_path):
        """
        Loads tasks from a JSON file into the tasks_dict dictionary.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The loaded tasks dictionary.

        Raises:
            FileNotFoundError: If the file is not found, a new empty dictionary is created and returned.
            ValueError: If the loaded data is not a dictionary or if any loaded task is not valid.

        Notes:
            - The method attempts to open and read the JSON file.
            - If the file is found, the method tries to load the tasks from the JSON file into a dictionary.
            - Each loaded task is validated using the is_task_valid method.
            - If any loaded task is not valid, a ValueError is raised and an empty dictionary is returned.
            - If the file is not found, a new empty dictionary is created, saved to the file, and returned.
            - If the JSON file is empty or corrupt, an empty dictionary is returned.
        """
        try:
            # Attempt to open and read the JSON file
            with open(file_path, 'r') as json_file:
                # Try to load tasks from the JSON file into a dictionary
                loaded_dict = json.load(json_file)

                # Check if the loaded data is a dictionary
                if isinstance(loaded_dict, dict):
                    # Validate each task in the loaded dictionary
                    for task_id, task in loaded_dict.items():
                        if not self.is_task_valid(task):
                            # Raise an error if any loaded task is not valid
                            raise ValueError("Loaded tasks are not valid. Returning an empty dictionary.")

                    # Print success message and return the loaded dictionary
                    print("Tasks were successfully loaded")
                    return loaded_dict
                else:
                    # Raise an error if the loaded data is not a dictionary
                    raise ValueError("Loaded data is not a dictionary. Returning an empty dictionary.")

        except FileNotFoundError:
            # If the file is not found, create a new empty dictionary and return it
            print(f"File '{file_path}' not found. Creating a new empty dictionary.")
            with open(file_path, 'w') as json_file:
                json.dump({}, json_file)
            return {}

        except json.decoder.JSONDecodeError as e:
            # If the JSON file is empty or corrupt, return an empty dictionary
            print(f"JSON file is empty or corrupt. Returning an empty dictionary. {e}")
            return {}

    def save_tasks(self, file_path):
        """
        Saves the tasks dictionary to a JSON file.
        Args:
            file_path (str): The file path where the tasks will be saved.
        Notes:
            - The method writes the tasks dictionary to the JSON file.
            - The tasks dictionary is saved with an indentation of 4 spaces.
            - If the file already exists, it will be overwritten.
            - If the file does not exist, it will be created.
        Raises:
            IOError: If there is an error while writing to the file.
        """
        # Write the dictionary to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(self.tasks_dict, json_file, indent=4)
            print("Tasks were successfully saved")

    def print_tasks(self):
        """
        Prints the tasks in the tasks_dict dictionary in a formatted table, sorted by the due date.
        Note: The table is printed to the console.
        """
        # Define headers for the table
        headers = ["Task Description", "Category", "Status", "Due Date", "Task ID"]

        # Sort tasks by due date before creating the table
        sorted_tasks = sorted(self.tasks_dict.items(), key=lambda x: datetime.strptime(x[1]['date'], DUE_DATE_FORMAT))

        # Create a list of lists containing sorted task information for tabulation
        data = [[task[1]["description"], task[1]["category"], task[1]["status"], task[1]["date"], task[0]]
                for task in sorted_tasks]

        # Use the tabulate library to format the data into a table
        table_data = tabulate(data, headers=headers, tablefmt="grid")

        # Print the formatted table
        print(table_data)


if __name__ == "__main__":
    tasks = ToDoList()
    tasks.tasks_dict = tasks.load_tasks("tasks_dict.json")

    while True:
        home_choice = MenuOptions.home_screen(tasks)

        if home_choice == 'm':
            while True:
                menu_choice = MenuOptions.main_menu()

                while not menu_choice:
                    menu_choice = MenuOptions.main_menu()

                if menu_choice == 1:
                    tasks.print_tasks()
                elif menu_choice == 2:
                    tasks.new_task()
                elif menu_choice == 3:
                    tasks.remove_task()
                elif menu_choice == 4:
                    tasks.update_task()
                elif menu_choice == 5:
                    tasks.save_tasks("tasks_dict.json")
                    break
        elif home_choice == 'e':
            break

    exit(0)
