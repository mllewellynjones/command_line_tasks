from config import config
from filehandler import FileHandler
from base import BaseCommandHandler

class InboxCommandHandler(BaseCommandHandler):
    """
    Handles commands related to the inbox, primarily by calling methods on the
    inbox itself
    
    Args:
        None.
        
    Returns:
        None.
    """
    def __init__(self, command_parser):
        self.inbox = Inbox()
        self.switcher = {
            'a': self.inbox.add_to_inbox,
            'd': self.inbox.display,
            'p': self.inbox.process_item,
            'pa': self.inbox.process_all,
            }
        self.inbox.command_parser = command_parser
               
    def close(self):
        """
        Close the inbox, for when the program exits
        """
        self.inbox.close()

class Inbox():
    """
    The inbox for unprocessed tasks
    """
    def __init__(self):
        self.filehandler = FileHandler(config.inbox_file)
        self.inbox_contents = self.filehandler.parse_text_file()
        self.command_parser = None

    ############################################################################
    # Inbox commands
    ############################################################################
    def add_to_inbox(self, description):
        """
        Add something to the inbox
        """
        self.inbox_contents.append(description)
        
    def display(self, remaining_command):
        """
        Display the contents of the inbox on the screen
        """
        for line_number, line in enumerate(self.inbox_contents):
            print(line_number, line.rstrip())

        return remaining_command

    def process_item(self, position):
        """
        Process a single inbox item
        """
        previous_mode = self.command_parser.get_current_mode()
        self.command_parser.switch_to_main_mode()

        while True:
            try:
                command = input(self.command_parser.get_prompt())   
                self.command_parser.breakout(command)
            except StopIteration:
                # Item processed
                break
            
        self.command_parser.set_mode(previous_mode)
                
    def process_all(self, remaining_command):
        """
        Process the inbox, from top (oldest) to bottom (newest)
        """
        for line_number, line in enumerate(self.inbox_contents):
            print("Item to process: " + line.rstrip())
            self.process_item(line_number)
            
        self.inbox_contents = []    
            
        return remaining_command
    
    ############################################################################
    
    def close(self):    
        """
        Closes the inbox by writing current state to file
        """
        self.filehandler.write_to_text_file(self.inbox_contents)