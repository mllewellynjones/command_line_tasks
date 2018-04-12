from tasks import TaskHandler
from projects import ProjectHandler

class CommandParser():
    """
    Handles all the interactions with the command line and input from
    the user

    Args:
        task_list (list) the list of issues to be worked with
    """
    
    def __init__(self, data):
        self.task_handler = TaskHandler(data['tasks'])
        self.project_handler = ProjectHandler(data['projects'])
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
            'd': [self.task_handler.display_all_tasks],
            'a': [self.task_handler.add_task, self.mode_edit],
            'e': [self.task_handler.edit_current_task],
            'q': [self.stop_parsing], 
            }
    
        if type(self.task_handler.current_task_index) == int:
            switcher['edit'] = {
                'd': [self.task_handler.display_current_task],
                'p': ['priority'],
                'c': ['created'],
                'dd': ['due'],
                'bu': ['blocked_until'],
                'te': ['time_estimate'],
                'ts': ['time_spent'],
                'pr': ['projects'],
                'co': ['contexts'],
                'q': [self.mode_main],
                }
        else:
            switcher['edit'] = {}
        
        try:
            handling_result_list = switcher[self.mode][initial_command]
        except KeyError:
            print("Command not found") 
            handling_result_list = []
        
        for handling_result in handling_result_list:
            if callable(handling_result) and remainder:
                handling_result(remainder)
                remainder = None
            elif callable(handling_result):
                handling_result()
            else:
                self.task_handler.modify_attribute_current_task(handling_result,
                                                                remainder)

    def mode_main(self):
        """
        Returns the parser to the main mode
        """
        self.mode = 'main'
        
    def mode_edit(self):
        """
        Switches the parse to edit mode
        """
        self.mode = 'edit'
        
    def stop_parsing(self):
        """
        Leaves the parser
        """
        raise StopIteration
