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
    def __init__(self):
        self.inbox = Inbox()
        self.switcher = {
            'a': self.inbox.add_to_inbox,
            'd': self.inbox.display,
            'p': self.inbox.process_item,
            'pa': self.inbox.process_all,
            }
        
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
            print(line_number, line)

        return remaining_command

    def process_item(self, position):
        """
        Process a single inbox item
        """
        pass
            
    def process_all(self):
        """
        Process the inbox, from top (oldest) to bottom (newest)
        """
        for line_number, line in enumerate(self.inbox_contents):
            print(line)
            self.process_item(line_number)
            self.inbox_contents.pop(line_number)
    
    def close(self):    
        """
        Closes the inbox by writing current state to file
        """
        self.filehandler.write_to_text_file(self.inbox_contents)
            