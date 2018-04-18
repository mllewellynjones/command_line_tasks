from collections import namedtuple
from os.path import expanduser

BASE_PATH = expanduser("~") + "\\Dropbox\\CLO Files\\"

ConfigTuple = namedtuple('Config', [
    'task_file',
    'project_file',
    'inbox_file',
    ])

config = ConfigTuple(
    BASE_PATH + 'tasks.db', # task_file
    BASE_PATH + 'projects.db', # project_file
    BASE_PATH + 'inbox.txt', # inbox file
    )