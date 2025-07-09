def singleton(cls):
    """
    A decorator to make a class a singleton by ensuring only one instance
    of the class is created during the program lifetime.

    This implementation stores the singleton instance in a closure variable,
    so each decorated class has its own independent singleton instance.

    Args:
        cls (type): The class to be decorated as a singleton.

    Returns:
        function: A function that returns the singleton instance of the class.
    """
    instance = None  # Holds the singleton instance for this class

    def get_instance(*args, **kwargs):
        """
        Returns the singleton instance of the decorated class. If the instance
        does not exist yet, creates it with the given arguments.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            object: The singleton instance of the class.
        """
        nonlocal instance
        if instance is None:
            # Create and store the singleton instance on first call
            instance = cls(*args, **kwargs)
        return instance

    return get_instance
