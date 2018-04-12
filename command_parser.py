from tasks import Task, TASK_FIELDS
from prettytable import PrettyTable

class CommandParser():
    """
    Handles all the interactions with the command line and input from
    the user

    Args:
        task_list (list) the list of issues to be worked with
    """
    
    def __init__(self, task_list):
        self.task_list = task_list
        self.current_task_index = None
        self.mode = 'main'
    
    def get_prompt(self):
        """
        Returns the appropriate prompt for the current mode.
        
        Args:
            None.
        """
        prompts = {
            'main': '>>',
            'edit': 'e>',
            }
            
        return (prompts[self.mode] + ' ')
            
    def breakout(self, command):
        """
        Find the appropriate function to handle this command
        
        Args:
            command (str): the command being parsed
        """
        try:
            initial_command, remainder = command.split(maxsplit=1)
        except ValueError:
            # Happens when the command can't be split
            initial_command = command
            remainder = ''
        
        switcher = {}
        
        switcher['main'] = {
            'd': self.display_all_tasks,
            'a': self.add_task,
            'e': self.edit_current_task,
            'q': self.stop_parsing, 
            }
    
        if type(self.current_task_index) == int:
            switcher['edit'] = {
                'd': self.task_list[self.current_task_index].display,
                'te': 'time_estimate',
                'q': self.return_to_main,
                }
        else:
            switcher['edit'] = {}
        
        try:
            handling_result = switcher[self.mode][initial_command]
        except KeyError:
            print("Command not found") 
            handling_result = None
        
        if callable(handling_result) and remainder:
            handling_result(remainder)
        elif callable(handling_result):
            handling_result()
        else:
            self.modify_attribute_current_task(handling_result,
                                               remainder)

    def add_task(self, description):
        """
        Parses a single 'add task' command and adds to the list
        """
        new_task = Task(description=description)
        self.task_list.append(new_task)
        self.current_task_index = -1    
        self.edit_current_task()

        return
        
    def edit_current_task(self):
        """
        Displays a task and then parses edit commands for that task
        """       
        self.task_list[self.current_task_index].display()
        self.mode = 'edit'          
            
    def return_to_main(self):
        """
        Returns the parser to the main mode
        """
        self.mode = 'main'
        
    def stop_parsing(self):
        """
        Leaves the parser
        """
        raise StopIteration
            
    def display_all_tasks(self):
        """
        Outputs a table showing all available tasks, sorted by index
        
        Args:
            all_tasks (list): a list of all tasks to display
            
        Returns:
            None.
        """
        table = PrettyTable(['Index'] + TASK_FIELDS)
           
        for index, task in enumerate(self.task_list):    
            table.add_row([index] + task.attributes_as_list())
            
        print(table)
        
    def modify_attribute_current_task(self, attribute, value):
        """
        Sets the attribute on the currently active task to value.
        
        Args:
            attribute (str): a string specifying the attribute 
                             to modfy
                             
            value: the new value
        
        Returns:
            None.
        """
        setattr(self.task_list[self.current_task_index],
                attribute,
                value)
