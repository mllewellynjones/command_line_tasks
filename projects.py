from prettytable import PrettyTable
from config import config
from tasks import TASK_FIELDS
from filehandler import FileHandler
from base import BaseCommandHandler

PROJECT_FIELDS = ['Description', 'Notes']

class ProjectCommandHandler(BaseCommandHandler):
    """
    Handles commands related to projects, primarily by invoking the Project
    Manager.
    
    Args:
        None.
        
    Returns:
        None.
    """
    def __init__(self):
        self.project_manager = ProjectManager()
        self.switcher = {
            'a':   self.add_new,
            'd':   self.display_current_project,
            'dt':  self.display_current_project_with_tasks,
            'da':  self.display_all,
            'dat': self.display_all_with_tasks,                
            }

    def set_task_manager_on_project_manager(self, task_manager):
        """
        Assigns a task manager to this project manager
        """
        self.project_manager.task_manager = task_manager
        
    def close(self):
        """
        Close the project manager, for when the program exits
        """
        self.project_manager.close()

    ############################################################################
    # Project commands
    ############################################################################
    def add_new(self, details):
        """
        Add a new project to the project manager
        """
        self.project_manager.add_project(details)
        
    def display_current_project(self, remaining_command):
        """
        Displays the current project
        """
        self.project_manager.display_current_project()
        return remaining_command
        
    def display_current_project_with_tasks(self, remaining_command):
        """
        Displays the current project with tasks
        """
        self.project_manager.display_current_project(with_tasks=True)   
        return remaining_command
        
    def display_all(self, remaining_command):
        """
        Display all projects in the project manager
        """
        self.project_manager.display_all_projects()
        return remaining_command
        
    def display_all_with_tasks(self, remaining_command):
        """
        Displays all projects in the project manager with tasks
        """
        self.project_manager.display_all_projects(with_tasks=True)
        return remaining_command
        

class ProjectManager():
    """
    A class that handles a list of projects in aggregate
    
    Args:
        project_list (list): a list of all the current projects
    """
    def __init__(self, task_manager=None):
        self.filehandler = FileHandler(config.project_file) 
        self.project_list = self.filehandler.parse_file()
        self.current_project_index = None
        
        # It is possible for the project manager to perform some basic function 
        # without a task manager, but it's not expected most of the time
        self.task_manager = task_manager
        
    def add_project(self, description):
        """
        Adds a project to the manager using the description
        """
        new_project = Project(description=description)
        self.project_list.append(new_project)
        self.current_project_index = -1
        self.display_current_project()
    
    def display_current_project(self, with_tasks=False):
        """
        Displays the current project
        """
        self.project_list[self.current_project_index].display()
        
        if with_tasks:
            table = PrettyTable(['Index'] + TASK_FIELDS)
            
            for task_index, task in enumerate(self.task_manager.task_list):
                    if (self.project_list[self.current_project_index].description
                            in task.projects):
                        table.add_row([task_index] + task.attributes_as_list())
                        
            print(table) 
    
    def display_all_projects(self, with_tasks=False):
        """
        Outputs a table showing all available projects, sorted by index
        
        Args:
            with_tasks (bool): whether to show the tasks under each project
        
        Returns:
            None.
        """
        if with_tasks:
            table = PrettyTable(['Project Index']
                                + ['P {}'.format(field) 
                                   for field in PROJECT_FIELDS]
                                + ['Task Index']
                                + ['T {}'.format(field)
                                   for field in TASK_FIELDS]
                                )
            
            for project_index, project in enumerate(self.project_list):
                table_row = [project_index] + project.attributes_as_list()
                
                for task_index, task in enumerate(self.task_manager.task_list):
                    if project.description in task.projects:
                        table_row += [task_index] + task.attributes_as_list()  
                
                table.add_row(table_row)
        else:    
            table = PrettyTable(['Index'] + PROJECT_FIELDS + ['State'])
            
            for index, project in enumerate(self.project_list):
                table.add_row([index] + project.attributes_as_list() + 
                              [project.state])            
        
        print(table)
        
    def close(self):
        """
        Closes the project manager by writing the current state to file
        """
        self.filehandler.write_to_file(self.project_list)


class Project():
    """
    A class representing a single project
    
    Args:
        description (str): a high level description of the project
        
        notes (list): a list of notes (of any type) related to the project
        
    """
    def __init__(self, description, notes=None):
        
        self.description = description
        
        if not notes:
            self.notes = []
        else:
            self.notes = notes
            
        self.state = 'None'
        
    def attributes_as_list(self):
        """
        Returns all the attributes of a project as a list, typically for 
        printing so it's important the order matches PROJECT_FIELDS above.
        """
        return [self.description,
                self.notes]
        
    def display(self):
        """
        Prints a project to the screen in a human readable format.
        
        Args:
            None.
            
        Returns:
            None.
        """
        table = PrettyTable(PROJECT_FIELDS)
        table.add_row(self.attributes_as_list())
        print(table)
    