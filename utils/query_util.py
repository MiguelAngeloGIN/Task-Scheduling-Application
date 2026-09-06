def query_handling(func, *args, error=None, ):
    """
    A utility function to handle database queries and exceptions.

    Args:
        func (callable): The function to execute.
        *args: Arguments to pass to the function.
        error (str, optional): Custom error message to raise as ValueError.

    Returns:
        The result of the function call.
    """
    try:
        return func(*args)
    except Exception as e:
        if error:
            raise ValueError(error) from e
        raise



   