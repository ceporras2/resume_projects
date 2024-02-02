from tabulate import tabulate
from datetime import datetime
from os import system as os_sys, name as os_name
import json, random, string, sys

class InputValidation:

    @staticmethod
    def home_menu_validation(user_input):
        """
        Validates the user input for the home menu.
        Args:
            user_input (str): The user input.  
        Returns:
            int: 0 if the input is valid, 1 otherwise.
        """
        if isinstance(user_input, str) and (user_input == 'm' or user_input == 'e'):
            return 0
        else:
            return 1

    @staticmethod
    def main_menu_validation(user_input):
        """
        Validates the user input for the main menu.       
        Args:
            user_input (int): The user input.      
        Returns:
            int: 0 if the input is valid, 1 otherwise.
        """
        if isinstance(user_input, int) and (1 <= user_input <= 5):
            return 0
        else:
            return 1

    @staticmethod
    def update_menu_validation(user_input):
        """
        Validates the user input for the update menu.       
        Args:
            user_input (int): The user input.     
        Returns:
            int: 0 if the input is valid, 1 otherwise.
        """
        if isinstance(user_input, int) and (1 <= user_input <= 4):
            return 0
        else:
            return 1
  
        
class MenuOptions:
    
    def home_screen(tasks):
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
        random_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        while random_id in self.tasks_dict:
            random_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return random_id

    def add_task_to_dict(self, new_task):
        self.tasks_dict[self.generate_random_id()] = new_task  

    def is_task_valid(self, task):
        if 'date' in task:
            try:
                due_date = datetime.strptime(task['date'], '%m/%d/%y %H:%M:%S')
                current_date = datetime.now()
                if due_date >= current_date:
                    return True
                else:
                    print("Error: Due date has already passed. Task is not valid.")
            except ValueError:
                print("Error: Invalid date format. Task is not valid.")
        else:
            print("Error: 'date' key not found in task dictionary. Task is not valid.")
        return False

    def new_task(self):
        print("""
        NEW TASK INFORMATION
        """)
        print("=====================================")

        description = input("Task Description: ")
        category = input("Task Category: ")
        status = input("Task Status: ")
        print("Due date format should be MM/DD/YY HH:MM")
        date = input("Task Due Date: ") + ":00"

        new_task = {
            "description": description,
            "category": category,
            "status": status,
            "date": date
        }

        if self.is_task_valid(new_task):
            self.add_task_to_dict(new_task)
            print("Added task successfully.")

    def remove_task(self):
        if not self.tasks_dict:
            print("Tasks list is empty.")

        task_id = input("\nEnter the id of the task you want to remove: ")

        if task_id in self.tasks_dict:
            del self.tasks_dict[task_id]
            print("Removed task successfully.")
        else:
            print("Task with the provided id does not exist.")

    def update_task(self):
        task_id = input("\nEnter the id of the task you want to update: ")

        if task_id in self.tasks_dict:
            task_to_update = MenuOptions.update_task_menu()

            if not task_to_update:
                return

            new_task = self.tasks_dict[task_id].copy()

            if task_to_update == 1:
                new_task["description"] = input("New Task Description: ")
            elif task_to_update == 2:
                new_task["category"] = input("New Task Category: ")
            elif task_to_update == 3:
                new_task["status"] = input("New Task Status: ")
            elif task_to_update == 4:
                print("Due date format should be MM/DD/YY HH:MM")
                new_task["date"] = input("New Task Due Date: ") + ":00"

            self.tasks_dict[task_id] = new_task

            print("Task updated successfully.")
        else:
            print("Task with the provided id does not exist.")

    def clear_expired_dates(self):
        current_datetime = datetime.now()

        tasks_to_remove = []

        for task_id, task in self.tasks_dict.items():
            if 'date' not in task:
                print(f"Error: 'date' key not found in task {task_id}. Skipping task.")
                continue

            try:
                due_date = datetime.strptime(task['date'], '%m/%d/%y %H:%M:%S')
                if due_date < current_datetime:
                    tasks_to_remove.append(task_id)
            except ValueError:
                print(f"Error: Invalid date format in task {task_id}. Skipping task.")

        for task_id in tasks_to_remove:
            del self.tasks_dict[task_id]

        print("Expired tasks removed successfully.")

    def load_tasks(self, file_path):
        try:
            with open(file_path, 'r') as json_file:
                loaded_dict = json.load(json_file)
                return loaded_dict
        except FileNotFoundError:
            print(f"File '{file_path}' not found. Creating a new empty dictionary.")
            with open(file_path, 'w') as json_file:
                json.dump({}, json_file)
            return {}
        except json.decoder.JSONDecodeError as e:
            print(f"JSON file is empty or corrupt. Returning an empty dictionary. {e}")
            return {}

    def save_tasks(self, file_path):
        with open(file_path, 'w') as json_file:
            json.dump(self.tasks_dict, json_file, indent=4)
            print("Tasks were successfully saved")
            
    def sort_tasks_by_date(self, tasks):
        return sorted(tasks, key=lambda x: datetime.strptime(x[0]["date"], '%m/%d/%y %H:%M:%S'))

    def print_tasks(self):
        os_sys('cls' if os_name == 'nt' else 'clear')  # Clear terminal command
        print("""
                            SCHOOL TO DO LIST
            """)
        
        headers = ["Task Description", "Category", "Status", "Due Date", "Task ID"]

        completed_tasks = []
        all_other_tasks = []

        for task_id, task in self.tasks_dict.items():
            if task["status"] == 'Completed':
                completed_tasks.append([task, task_id])
            else:
                all_other_tasks.append([task, task_id])

        # Sort tasks by date before creating table data
        sorted_incomplete_tasks = self.sort_tasks_by_date(all_other_tasks)
        sorted_completed_tasks = self.sort_tasks_by_date(completed_tasks)

        incomplete_data = [[task[0]["description"], task[0]["category"], task[0]["status"], task[0]["date"], task[1]]
                        for task in sorted_incomplete_tasks]

        incomplete_table = tabulate(incomplete_data, headers=headers, tablefmt="grid")
        print("In Progress Tasks:")
        print(incomplete_table)

        if sorted_completed_tasks:
            completed_data = [[task[0]["description"], task[0]["category"], task[0]["status"], task[0]["date"], task[1]]
                            for task in sorted_completed_tasks]
            completed_table = tabulate(completed_data, headers=headers, tablefmt="grid")
            print("\nCompleted Tasks:")
            print(completed_table)


if __name__ == "__main__":
    tasks = ToDoList()
    tasks.tasks_dict = tasks.load_tasks("tasks_dict.json")
    tasks.clear_expired_dates()

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

    sys.exit(0)
