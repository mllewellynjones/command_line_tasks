from base import BaseCommandHandler

class FilterCommandHandler(BaseCommandHandler):
    """
    Handles commands related to filters, primarily by calling methods on the 
    Filter Manager
    
    Args:
        None.
        
    Returns:
        None.
    """
    def __init__(self, task_manager, project_manager):
        self.filter_manager = FilterManager(task_manager, project_manager)
        self.switcher = {
            'act': self.display_all_active_tasks,
            }
        
    def display_all_active_tasks(self, remaining_command):
        """
        Displays all active tasks from the task manager
        """
        self.filter_manager.all_active_tasks()
        return remaining_command
        
class FilterManager():
    """
    Handles requests for filters by printing relevant output to the screen.
    
    The filter manager is stateless.
    """
    def __init__(self, task_manager, project_manager):
        self.task_manager = task_manager
        self.project_manager = project_manager
        
    def all_active_tasks(self):
        """
        Returns all tasks that can current be acted on, in index order
        """
        self.task_manager.display_list_of_tasks_by_index(
            self.task_manager.filter(only_active=True))