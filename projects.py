
class ProjectHandler():
    """
    A class that handles a list of projects in aggregate
    
    Args:
        project_list (list): a list of all the current projects
    """
    def __init__(self, project_list):
        self.project_list = project_list
    

class Project():
    """
    A class representing a single project
    
    Args:
        
        
    """
    def __init__(self, description, notes=None):
        
        self.description = description
        
        self.notes = notes
        
    