import pickle

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
            # File doesn't contain what we're looking for, 
            # start from scratch
            return []

    
    def write_to_file(self, all_tasks):
        """
        Writes all_tasks to the filename associated with this FileHandler
        
        Args:
            all_tasks (list): the tasks to write out
        """
        file_contents = {}
        file_contents['data'] = all_tasks
       
        with open(self.filename, 'wb') as outfile:
            pickle.dump(file_contents, outfile)