import traceback
import sys

class BaseCommandHandler():
    """
    Base class for all Command Handlers
    """    
    
    def __init__(self):
        self.switcher = {}
        
    def handle_command(self, command):
        """
        Parses and dispatches a command
        
        Args:
            command (str): the command to be parsed
            
        Returns:
            str: the remaining command that wasn't consumed
        """
        try:
            initial_command, remainder = command.split(maxsplit=1)
        except ValueError:
            # Happens when the command can't be split
            initial_command = command
            remainder = ''
        
        try:
            handling_result = self.switcher[initial_command]
            remainder = handling_result(remainder)
        except KeyError:
            print("Command not found") 
        except StopIteration:
            raise
        except BaseException as err:
            print("That caused an exception: {}".format(err))
            traceback.print_exc(file=sys.stdout)
        
        return remainder