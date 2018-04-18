from config import config
from datetime import datetime
from prettytable import PrettyTable
from filehandler import FileHandler
from base import BaseCommandHandler

TASK_FIELDS = ['Description', 'Priority', 'Created', 'Due', 'Blocked',
               'Time estimate', 'Time Spent', 'Projects', 'Contexts']

class TaskCommandHandler():
    """
    Handles commands related to tasks, primarily by invoking the Task Manager
    
    Args:
        None.
        
    Returns:
        None.
    """
    def __init__(self):
        self.task_manager = TaskManager()
        self.switcher = {
            'a':  self.add_new,
            'bu': self.add_to_contexts_current_task,
            'c':  self.set_closed_current_task,
            'co': self.add_to_contexts_current_task,
            'cr': self.set_created_current_task,
            'd':  self.display_current_task,
            'da': self.display_all,
            'dd': self.set_due_date_current_task,
            'e':  self.edit_current_task,
            'p':  self.set_priority_current_task,
            'pr': self.add_to_projects_current_task,             
            'te': self.set_time_estimate_current_task,
            'ts': self.set_time_spent_current_task,
            }
               
    def get_task_manager(self):
        """
        Returns the task manager associated with this task command handler
        
        Args:
            None.
            
        Returns:
            TaskManager(), or None.
        """
        return self.task_manager
        
    ############################################################################
    # Task commands
    ############################################################################
    def add_new(self, details):
        """
        Add a new task to the task manager
        """
        print(details)
        self.task_manager.add_task(details)
        return None
    
    def add_to_blocked_until_current_task(self, new_blocked_until):
        """
        Adds to the blocked until list on the current task
        """
        self.task_manager.modify_attribute_current_task('blocked_until',
                                                        new_blocked_until)
        return None

    def set_closed_current_task(self, remaining_command):
        """
        Sets the state of the current task to closed
        """
        self.task_manager.modify_attribute_current_task('state', 'closed')
        return remaining_command
    
    def set_created_current_task(self, new_created):
        """
        Sets the created date/time on the current task
        """
        self.task_manager.modify_attribute_current_task('create', new_created)       
        return None

    def add_to_contexts_current_task(self, new_context):
        """
        Adds to the contexts list on the current task
        """
        self.task_manager.modify_attribute_current_task('contexts',
                                                        new_context)
    
    def display_current_task(self, remaining_command):
        """
        Displays the current task
        """
        self.task_manager.display_current_task()
        return remaining_command
        
    def display_all(self, remaining_command):
        """
        Displays all tasks in the task manager
        """
        self.task_manager.display_all_tasks()
        return remaining_command

    def set_due_date_current_task(self, new_due_date):
        """
        Sets the due date/time on the current task
        """
        self.task_manager.modify_attribute_current_task('due', new_due_date)

    def edit_current_task(self, remaining_command):
        """
        Edit the current command
        """
        self.task_manager.edit_current_task()
        return remaining_command

    def set_priority_current_task(self, new_priority):
        """
        Sets the priority on the current task
        """
        self.task_manager.modify_attribute_current_task('priority', 
                                                        new_priority)

    def add_to_projects_current_task(self, new_project):
        """
        Adds to the projects list on the current task
        """
        self.task_manager.modify_attribute_current_task('projects',
                                                        new_project)
                      
    def set_time_estimate_current_task(self, time_estimate):
        """
        Sets the time estimate on the current task
        """
        self.task_manager.modify_attribute_current_task('time_estimate',
                                                        time_estimate)

    def set_time_spent_current_task(self, time_spent):
        """
        Sets the time spent on the current task
        """
        self.task_manager.modify_attribute_current_task('time_spent', 
                                                        time_spent)    

class TaskManager():
    """
    A class that handles a list of tasks in aggregate
    
    Args:
        task_list (list): a list of all the current tasks
    """
    def __init__(self):
        self.filehandler = FileHandler(config.task_file)
        self.task_list = self.filehandler.parse_file()
        self.current_task_index = None
        
    def add_task(self, description):
        """
        Adds a task to the manager using the description
        """
        new_task = Task(description=description)
        self.task_list.append(new_task)
        self.current_task_index = -1    
        self.display_current_task()
       
    def display_current_task(self):
        """
        Displays the current task
        """
        self.task_list[self.current_task_index].display()
        
    def display_all_tasks(self, include_closed=False):
        """
        Outputs a table showing all available tasks, sorted by index
        
        Args:
            include_closed (bool): whether to include closed tasks in the output
            
        Returns:
            None.
        """
        if include_closed:
            table = PrettyTable(['Index'] + TASK_FIELDS + ['State'])
               
            for index, task in enumerate(self.task_list):    
                table.add_row([index] + task.attributes_as_list()
                              + [task.state])
        else:
            table = PrettyTable(['Index'] + TASK_FIELDS)
               
            for index, task in enumerate(self.task_list):    
                table.add_row([index] + task.attributes_as_list())
            
        print(table)
        
    def modify_attribute_current_task(self, attribute, value):
        """
        Sets the attribute on the currently active task to value.
        
        Args:
            attribute (str): a string specifying the attribute 
                             to modfy
                             
            value: the new value
        
        Returns:
            None.
        """
        setattr(self.task_list[self.current_task_index],
                attribute,
                value)       
        

class Task():
    """
    A class representing a single task
    
    Args:
        description (str): the subject of the task
        
        created (datetime): the date and time the task was created, defaults to
                            now
                            
        due (datetime): the date and time the task is due
        
        blocked_until (list): a list of other tasks blocking this one, possibly
                              also including a start date, defaults to an 
                              empty list
                              
        time_estimate (str): the estimated time required for this task, defaults
                             to None
        
        time_spent (str): the time already spent on this task, defaults to None
        
        projects (str): a list of projects for which this task is an action, 
                        defaults to an empty list
                        
        contexts (str): a list of contexts for this task, defaults to an empty
                        list
    """
    def __init__(self, description, priority=3, created=None, due=None,
                 blocked_until=None, time_estimate=None, time_spent=None,
                 projects=None, contexts=None, state='open'):
                     
        self.description = description
        
        self._priority = priority
        
        if not created:
            self._created = datetime.now()
            
        self._due = due
        
        if not blocked_until:
            self._blocked_until = []
            
        self._time_estimate = time_estimate
        
        self._time_spent = time_spent
        
        if not projects:
            self._projects = []
        else:
            self._projects = projects
        
        if not contexts:
            self._contexts = []
        else:
            self._contexts = contexts
            
        self._state = state
            
    @staticmethod
    def date_as_string(date_object):
        """
        Returns a given date object as a formatted string, or 'None'
        if there is no object.
        
        Args:
            date_object (datetime): the datetime object to convert
            
        Returns:
            str: the object converted into a string            
        """
        if date_object:
            return date_object.strftime("%a %d %b %Y")
        else:
            return 'None'
            
    @staticmethod
    def list_as_string(list_object):
        """
        Returns a given list object as a formatted comma separated string,
        or 'None' if the list is empty
                
        Args:
            list_object (list): the lsit to convert
            
        Returns:
            str: the object converted into a string            
        """
        if list_object:
            return ",".join(list_object)
        else:
            return 'None'                    
      
    @staticmethod
    def string_to_datetime(datetime_string):
        """
        Converts the specified string into a datetime object
        
        Args:
            datetime_string (str): the string to convert        
        """
        datetime_formats = ["%d %b %y",
                           ]
        
        for dt_format in datetime_formats:
            try:
                value = datetime.strptime(datetime_string, dt_format)
                return value
            except ValueError:
                continue
                
        print("Value could not be parsed")                
        return 'None'

    ############################################################################    
    # Priority
    ############################################################################
    @property
    def priority(self):
        return str(self._priority)
     
    @priority.setter
    def priority(self, value):
        self._priority = int(value)
        
    ############################################################################    
    # Created
    ############################################################################
    @property
    def created(self):
        return self.date_as_string(self._created)
        
    @created.setter
    def created(self, value):
        self._created = self.string_to_datetime(value)

    ############################################################################    
    # Due
    ############################################################################
    @property
    def due(self):
        return self.date_as_string(self._due)

    @due.setter
    def due(self, value):
        self._due = self.string_to_datetime(value)      
        
    ############################################################################    
    # Blocked until
    ############################################################################   
    @property
    def blocked_until(self):
        return self.list_as_string(self._blocked_until)

    @blocked_until.setter
    def blocked_until(self, value):
        if type(value) == list:
            self._blocked_until.extend(value)
        else:
            self._blocked_until.append(value)
            
    def remove_blocked_until(self, value):
        if value in self._blocked_until:
            self._blocked_until.remove(value)
    
    ############################################################################    
    # Time estimate
    ############################################################################  
    @property
    def time_estimate(self): 
        return str(self._time_estimate)
        
    @time_estimate.setter
    def time_estimate(self, value):
        self._time_estimate = value
        
    ############################################################################    
    # Time spent
    ############################################################################
    @property
    def time_spent(self):
        return str(self._time_spent)
    
    @time_spent.setter
    def time_spent(self, value):
        self._time_spent = value

    ############################################################################    
    # Projects
    ############################################################################
    @property
    def projects(self):
        return self.list_as_string(self._projects)
            
    @projects.setter
    def projects(self, value):
        if type(value) == list:
            self._projects.extend(value)
        else:
            self._projects.append(value)
            
    def remove_project(self, value):
        if value in self._projects:
            self._projects.remove(value)
            
    ############################################################################    
    # Contexts
    ############################################################################
    @property
    def contexts(self):
        return self.list_as_string(self._contexts)
        
    @contexts.setter
    def contexts(self, value):
        if type(value) == list:
            self._contexts.extend(value)
        else:
            self._contexts.append(value)
            
    def remove_context(self, value):
        if value in self._contexts:
            self._contexts.remove(value)

    ############################################################################    
    # State
    ############################################################################
    @property
    def state(self):
        return self.state
        
    @state.setter
    def state(self, value):
        if value in ['open', 'closed']:
            self._state = value

    ############################################################################    

    def attributes_as_list(self):
        """
        Returns all the attributes of the task as a list, typically for 
        printing so it's important the order matches TASK_FIELDS above.      
        """
        return [self.description,
                self.priority,
                self.created,
                self.due,
                self.blocked_until,
                self.time_estimate,
                self.time_spent,
                self.projects,
                self.contexts]

    def display(self):
        """
        Prints a task to the screen in a human readable format.
        
        Args:
            None.
            
        Returns:
            None.
        """
        table = PrettyTable(TASK_FIELDS)
        table.add_row(self.attributes_as_list())
        print(table)

