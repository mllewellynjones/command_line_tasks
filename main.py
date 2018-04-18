from command_parser import CommandParser

cp = CommandParser()

while True:
    try:
        command = input(cp.get_prompt())   
        cp.breakout(command)
    except StopIteration:
        break