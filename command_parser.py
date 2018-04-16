import sys
import traceback
from tasks import TaskManager
from projects import ProjectManager

class CommandParser():
    """
    Handles all the interactions with the command line and input from
    the user

    Args:
        task_list (list) the list of issues to be worked with
    """
    
    def __init__(self, data):
        self.task_manager = TaskManager(data['tasks'])
        self.project_manager = ProjectManager(data['projects'],
                                              self.task_manager)
        self.mode = 'main'
    
    def get_prompt(self):
        """
        Returns the appropriate prompt for the current mode.
        
        Args:
            None.
        """
        prompts = {
            'main': '>>',
            'task': 't>',
            'proj': 'p>',
            }
            
        return (prompts[self.mode] + ' ')
            
    def breakout(self, command):
        """
        Find the appropriate function to handle this command
        
        Args:
            command (str): the command being parsed
        """
        try:
            initial_command, arguments = command.split(maxsplit=1)
        except ValueError:
            # Happens when the command can't be split
            initial_command = command
            arguments = ''
        
        switcher = {}
        
        switcher['main'] = {
            'p': self.main_p,
            'q': self.stop_parsing,
            't': self.main_t,
            }
    
        switcher['task'] = {
            'a':  self.task_a,
            'bu': self.task_bu,
            'c':  self.task_c,
            'co': self.task_co,
            'cr': self.task_c,
            'd':  self.task_d,
            'da': self.task_da,
            'dd': self.task_dd,
            'e':  self.task_e,
            'p':  self.task_p,
            'pr': self.task_pr,             
            'te': self.task_te,
            'ts': self.task_ts,
            'q':  self.mode_main,
            }
        
        switcher['proj'] = {
            'a':   self.proj_a,
            'd':   self.proj_d,
            'dt':  self.proj_dt,
            'da':  self.proj_da,
            'dat': self.proj_dat,
            'q':   self.mode_main,
            }
        
        continued_command = ""
        try:
            handling_result = switcher[self.mode][initial_command]
            continued_command = handling_result(arguments)
        except KeyError:
            print("Command not found") 
        except StopIteration:
            raise
        except BaseException as err:
            print("That caused an exception: {}".format(err))
            traceback.print_exc(file=sys.stdout)
        
        if continued_command:
            self.breakout(continued_command)
                

    ############################################################################
    # Main mode functions
    ############################################################################
    def main_p(self, continued_command):
        """
        Handles the (p)roject command in the main mode
        """
        self.mode = 'proj'
        return continued_command

    def main_t(self, continued_command):
        """
        Handles the (t)ask command in the main mode
        """
        self.mode = 'task'
        return continued_command

    ############################################################################
    # Task mode functions
    ############################################################################
    def task_a(self, command_input):
        """
        Handles the (a)dd command in the task mode
        """
        self.task_manager.add_task(command_input)
    
    def task_bu(self, command_input):
        """
        Adds to the (b)locked (u)ntil list on the current task
        """
        self.task_manager.modify_attribute_current_task('blocked_until',
                                                        command_input)

    def task_c(self, continued_command):
        """
        Sets the state of the current task to (c)losed
        """
        self.task_manager.modify_attribute_current_task('state', 'closed')
        return continued_command
    
    def task_cr(self, command_input):
        """
        Sets the (cr)eated date/time on the current task
        """
        self.task_manager.modify_attribute_current_task('create', command_input)       

    def task_co(self, command_input):
        """
        Adds to the (co)ntexts list on the current task
        """
        self.task_manager.modify_attribute_current_task('contexts',
                                                        command_input)
    
    def task_d(self, continued_command):
        """
        Handles the (d)isplay command in the task mode
        """
        self.task_manager.display_current_task()
        return continued_command
        
    def task_da(self, continued_command):
        """
        Handles the (d)isplay (a)ll command in the task mode
        """
        self.task_manager.display_all_tasks()
        return continued_command

    def task_dd(self, command_input):
        """
        Sets the (d)ue (d)ate/time on the current task
        """
        self.task_manager.modify_attribute_current_task('due', command_input)

    def task_e(self, continued_command):
        """
        Handles the (e)dit command in the task mode
        """
        self.task_manager.edit_current_task()
        return continued_command

    def task_p(self, command_input):
        """
        Sets the (p)riotity on the current task
        """
        self.task_manager.modify_attribute_current_task('priority', 
                                                        command_input)

    def task_pr(self, command_input):
        """
        Adds to the (pr)ojects list on the current task
        """
        self.task_manager.modify_attribute_current_task('projects',
                                                        command_input)
                      
    def task_te(self, command_input):
        """
        Sets the (t)ime (e)stimate on the current task
        """
        self.task_manager.modify_attribute_current_task('time_elapsed',
                                                        command_input)

    def task_ts(self, command_input):
        """
        Sets the (t)ime (s)pent on the current task
        """
        self.task_manager.modify_attribute_current_task('time_spent', 
                                                        command_input)
        
    ############################################################################
    # Project mode functions
    ############################################################################
    def proj_a(self, command_input):
        """
        Handles the (a)dd command in project mode
        """
        self.project_manager.add_project(command_input)
        
    def proj_d(self, continued_command):
        """
        Handles the (d)isplay command in project mode
        """
        self.project_manager.display_current_project()
        return continued_command
        
    def proj_dt(self, continued_command):
        """
        Handles the (d)isplay with (t)asks command in project mode
        """
        self.project_manager.display_current_project(with_tasks=True)   
        return continued_command   
        
    def proj_da(self, continued_command):
        """
        Handles the (d)isplay (a)ll command in project mode
        """
        self.project_manager.display_all_projects()
        return continued_command
        
    def proj_dat(self, continued_command):
        """
        Handles the (d)isplay (a)ll with (t)asks command in project mode
        """
        self.project_manager.display_all_projects(with_tasks=True)
        return continued_command
        
    ############################################################################
    # General functions
    ############################################################################
    def mode_main(self, continued_command):
        """
        Returns the parser to the main mode
        """
        self.mode = 'main'
        return continued_command
               
    def stop_parsing(self, _):
        """
        Leaves the parser
        """
        raise StopIteration
