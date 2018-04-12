from datetime import datetime
from prettytable import PrettyTable

TASK_FIELDS = ['Description', 'Created', 'Due', 'Blocked',
               'Time estimate', 'Time Spent', 'Projects', 'Contexts']

class Task():
    
    def __init__(self, description, created=None, due=None, blocked_until=None,
                 time_estimate=None, time_spent=None, projects=None,
                 contexts=None):
                     
        self.description = description
        
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

    def attributes_as_list(self):
        """
        Returns all the attributes of the task as a list, typically for 
        printing so it's important the order matches TASK_FIELDS above.      
        """
        return [self.description,
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

