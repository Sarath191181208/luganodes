def remove_null_values(d):
    """
    Remove keys with None values from a dictionary.
    
    Args:
        d (dict): The dictionary to process.
    
    Returns:
        dict: A new dictionary with keys having None values removed.
    """
    res = {k: v for k, v in d.items() if v is not None}
    print(res)
    return res
