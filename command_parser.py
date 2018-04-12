from tasks import TaskHandler
from projects import ProjectHandler

class CommandParser():
    """
    Handles all the interactions with the command line and input from
    the user

    Args:
        task_list (list) the list of issues to be worked with
    """
    
    def __init__(self, data):
        self.task_handler = TaskHandler(data['tasks'])
        self.project_handler = ProjectHandler(data['projects'])
        self.mode = 'main'
    
    def get_prompt(self):
        """
        Returns the appropriate prompt for the current mode.
        
        Args:
            None.
        """
        prompts = {
            'main': '>>',
            'edit': 'e>',
            }
            
        return (prompts[self.mode] + ' ')
            
    def breakout(self, command):
        """
        Find the appropriate function to handle this command
        
        Args:
            command (str): the command being parsed
        """
        try:
            initial_command, remainder = command.split(maxsplit=1)
        except ValueError:
            # Happens when the command can't be split
            initial_command = command
            remainder = ''
        
        switcher = {}
        
        switcher['main'] = {
            'd': self.main_d,
            'a': self.main_a,
            'e': self.main_e,
            'q': self.stop_parsing, 
            }
    
        if type(self.task_handler.current_task_index) == int:
            switcher['edit'] = {
                'd':  self.edit_d,
                'p':  self.edit_p,
                'c':  self.edit_c,
                'dd': self.edit_dd,
                'bu': self.edit_bu,
                'te': self.edit_te,
                'ts': self.edit_ts,
                'pr': self.edit_pr,
                'co': self.edit_co,
                'q': self.mode_main,
                }
        else:
            switcher['edit'] = {}
        
        try:
            handling_result = switcher[self.mode][initial_command]
            handling_result(remainder)
        except KeyError:
            print("Command not found") 

    ############################################################################
    # Main mode functions
    ############################################################################
    def main_a(self, input):
        """
        Handles the (a)dd command in the main mode
        """
        self.task_handler.add_task(input)
        self.mode = 'edit'
        
    def main_d(self, input):
        """
        Handles the (d)isplay command in the main mode
        """
        self.task_handler.display_all_tasks()   

    def main_e(self, input):
        """
        Handles the (e)dit command in the main mode
        """
        self.task_handler.edit_current_task()
        
    ############################################################################
    # Edit mode functions
    ############################################################################
    def edit_d(self, input):
        """
        Handles the (d)isplay command in the main mode
        """
        self.task_handler.display_current_task()
        
    def edit_p(self, input):
        """
        Sets the (p)riotity on the current task
        """
        self.task_handler.modify_attribute_current_task('priority', input)

    def edit_c(self, input):
        """
        Sets the (c)reated date/time on the current task
        """
        self.task_handler.modify_attribute_current_task('create', input)
        
    def edit_p(self, input):
        """
        Sets the (p)riotity on the current task
        """
        self.task_handler.modify_attribute_current_task('priority', input)
        
    def edit_dd(self, input):
        """
        Sets the (d)ue (d)ate/time on the current task
        """
        self.task_handler.modify_attribute_current_task('due', input)
        
    def edit_bu(self, input):
        """
        Adds to the (b)locked (u)ntil list on the current task
        """
        self.task_handler.modify_attribute_current_task('blocked_until', value)
        
    def edit_te(self, input):
        """
        Sets the (t)ime (e)stimate on the current task
        """
        self.task_handler.modify_attribute_current_task('time_elapsed', value)

    def edit_ts(self, input):
        """
        Sets the (t)ime (s)pent on the current task
        """
        self.task_handler.modify_attribute_current_task('time_spent', value)
        
    def edit_pr(self, input):
        """
        Adds to the (pr)ojects list on the current task
        """
        self.task_handler.modify_attribute_current_task('projects', value)
        
    def edit_co(self, input):
        """
        Adds to the (co)ntexts list on the current task
        """
        self.task_handler.modify_attribute_current_task('contexts', value)
        
    ############################################################################
    # General functions
    ############################################################################
    def mode_main(self, input):
        """
        Returns the parser to the main mode
        """
        self.mode = 'main'
               
    def stop_parsing(self, input):
        """
        Leaves the parser
        """
        raise StopIteration
