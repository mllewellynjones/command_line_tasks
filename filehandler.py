import pickle
from logging import FileHandler

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
                return file_contents['data']
            
        except FileNotFoundError:
            # File doesn't exist, start from scratch
            return []
        
        except EOFError:
            # File doesn't contain what we're looking for, start from scratch
            return []

    def parse_text_file(self):
        """
        Parses the contents of a plaintext files associated with this
        filehandler and returns it
        
        Args:
            None.
        
        Returns:
            list: the contents of the plain text file, broken up into a list of
                  lines
        """
        try:
            with open(self.filename, 'r') as infile:
                file_contents = infile.readlines()
                return file_contents
            
        except FileNotFoundError:
            # File doesn't exist, start from scratch
            return []                
    
    def write_to_file(self, data):
        """
        Writes data to the filename associated with this FileHandler
        
        Args:
            data (list): all the data to write to file
            
        Returns:
            None.
        """      
        with open(self.filename, 'wb') as outfile:
            file_contents = {}
            file_contents['data'] = data
            pickle.dump(file_contents, outfile)
            
    def write_to_text_file(self, data):
        """
        Writes a list to the filename associated with this FileHandler
        
        Args:
            data (list): the data to write to the file
        
        Returns:
            None.
        """
        with open(self.filename, 'w') as outfile:
            for line in data:
                outfile.write(line)
        