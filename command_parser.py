import sys
import traceback
from tasks import TaskCommandHandler
from projects import ProjectCommandHandler
from inbox import InboxCommandHandler
from filter import FilterCommandHandler

class CommandParser():
    """
    Handles all the interactions with the command line and input from
    the user

    Args:
        task_list (list) the list of issues to be worked with
    """
    
    def __init__(self):
        self.task_command_handler = TaskCommandHandler()
        self.project_command_handler = ProjectCommandHandler()
        self.inbox_command_handler = InboxCommandHandler(self)
        self.filter_command_handler = FilterCommandHandler(
            self.task_command_handler.get_task_manager(),
            self.project_command_handler.get_project_manager()
            )
        
        # Sort out dependencies
        self.project_command_handler.set_task_manager_on_project_manager(
            self.task_command_handler.get_task_manager())
               
        self.mode = 'main'
    
    def get_prompt(self):
        """
        Returns the appropriate prompt for the current mode.
        
        Args:
            None.
        """
        prompts = {
            'main': '>>',
            'task': 't>',
            'proj': 'p>',
            'inbox': 'i>',
            'filt': 'f>',
            }
            
        return (prompts[self.mode] + ' ')
            
    def breakout(self, command):
        """
        Find the appropriate function to handle this command
        
        Args:
            command (str): the command being parsed
        """
        try:
            initial_command, arguments = command.split(maxsplit=1)
        except ValueError:
            # Happens when the command can't be split
            initial_command = command
            arguments = ''
            
        SWITCHER = {
            'p': self.switch_to_project_mode,
            'q': self.exit_program,
            't': self.switch_to_task_mode,
            'i': self.switch_to_inbox_mode,
            'm': self.switch_to_main_mode,
            'f': self.switch_to_filter_mode,
            }
        
        continued_command = ""
        try:
            if self.mode == 'main' or initial_command == 'm':
                handling_result = SWITCHER[initial_command]
                continued_command = handling_result(arguments)
            else:
                continued_command = self.dispatch_to_command_handler(command)
        except KeyError:
            print("Command not found") 
        except StopIteration:
            raise
        except BaseException as err:
            print("That caused an exception: {}".format(err))
            traceback.print_exc(file=sys.stdout)
        
        if continued_command:
            self.breakout(continued_command)
                
    def dispatch_to_command_handler(self, command):
        """
        Finds the appropriate command handler given the mode and sends the 
        command to that handler
        
        Args:
            command (str): the command to dispatch
            
        Returns:
            str: any remaining command that was not consumed by the handler
        """
        handler_dict = {
            'task': self.task_command_handler,
            'proj': self.project_command_handler,
            'inbox': self.inbox_command_handler,
            'filt': self.filter_command_handler,
            }
        
        current_handler = handler_dict[self.mode]
        remaining_command = current_handler.handle_command(command)
        
        return remaining_command
    
    def get_current_mode(self):
        """
        Returns the current mode of this command handler
        """
        return self.mode
    
    def set_mode(self, new_mode):
        """
        Sets the current mode of this command handler
        """
        self.mode = new_mode


    ############################################################################
    # Main commands
    ############################################################################
    def switch_to_project_mode(self, remaining_command=''):
        """
        Switches into project mode
        """
        self.mode = 'proj'
        return remaining_command

    def switch_to_task_mode(self, remaining_command=''):
        """
        Switch into task mode
        """
        self.mode = 'task'
        return remaining_command
    
    def switch_to_inbox_mode(self, remaining_command=''):
        """
        Switch into inbox mode
        """
        self.mode = 'inbox'
        return remaining_command    
    
    def switch_to_filter_mode(self, remaining_command=''):
        """
        Switch into filter mode
        """
        self.mode = 'filt'
        return remaining_command

    def switch_to_main_mode(self, remaining_command=''):
        """
        Switch into main mode
        """
        self.mode = 'main'
        return remaining_command
               
    def exit_program(self, remaining_command=''):
        """
        Shuts down the program
        """
        self.task_command_handler.close()
        self.project_command_handler.close()
        self.inbox_command_handler.close()
        raise StopIteration
