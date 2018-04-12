import argparse
from command_parser import CommandParser
from filehandler import FileHandler


parser = argparse.ArgumentParser(description='Command line task manager')
parser.add_argument('-f', '--file', action='store', 
                    default="task_manager.txt",
                    help="The file where tasks are stored")
args = parser.parse_args()
filename = args.file

fh = FileHandler(filename)
data = fh.parse_file()

cp = CommandParser(data)

while True:
    try:
        command = input(cp.get_prompt())   
        cp.breakout(command)
    except StopIteration:
        break
    
fh.write_to_file(data)