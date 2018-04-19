import uuid

def generate_unique_id():
    """
    Generates a unique ID
    
    Args:
        None.
    
    Returns:
        str: the unique identifier as a string
    """
    return str(uuid.uuid4())