import pickle
from collections import defaultdict

class FileHandler():
    """
    Responsible for reading and writing to a pickle file
    
    Args:
        filename (str): the file for this filehandler to use
    """
    
    def __init__(self, filename):
        self.filename = filename

    def parse_file(self):
        """
        Parses the contents of the associated file and returns it.
        
        Args:
            None.
            
        Returns:
            list: everything under the 'data' key in the file, assumed
                  to be a list
        """
        try:
            with open(self.filename, 'rb') as infile:
                file_contents = pickle.load(infile)
                return file_contents
            
        except FileNotFoundError:
            # File doesn't exist, start from scratch
            return defaultdict(list)
        
        except EOFError:
            # File doesn't contain what we're looking for, 
            # start from scratch
            return defaultdict(list)

    
    def write_to_file(self, data):
        """
        Writes data to the filename associated with this FileHandler
        
        Args:
            data (dict): all the data to write to file
        """      
        with open(self.filename, 'wb') as outfile:
            pickle.dump(data, outfile)