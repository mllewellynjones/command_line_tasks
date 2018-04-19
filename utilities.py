import uuid

def generate_unique_id(text):
    """
    Generates a unique ID from a string
    
    Args:
        text (str): the input string to use when forming the unique ID
    
    Returns:
        str: the unique identifier as a string
    """
    return str(uuid.uuid4())