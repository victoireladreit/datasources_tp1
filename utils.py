import collections
import logging
import time

# Decorator to measure execution time 
def execution_time_decorator(func):
    """
    A decorator function to measure the execution time of a wrapped function.

    Args:
        func (function): The function to be wrapped.

    Returns:
        function: A new function that logs the execution time and returns the result of the wrapped function.

    Example:
        @execution_time_decorator
        def my_function():
            # ... your code here ...
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function that measures the execution time of the wrapped function.

        Args:
            *args: Positional arguments passed to the wrapped function.
            **kwargs: Keyword arguments passed to the wrapped function.

        Returns:
            tuple: A tuple containing the result of the wrapped function and the execution time in seconds.
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        # Log the execution time
        logging.info(f'{func.__name__} took {execution_time} seconds to execute.')
        return result, execution_time
    return wrapper

def count_words_with_dict(text):
    """
    Count the occurrences of words in a given text using a dictionary.

    Args:
        text (str): The input text in which to count words.

    Returns:
        dict: A dictionary where keys are unique words and values are their respective counts.

    Example:
        word_counts = count_words_with_dict("This is a sample text. This text contains words.")
    """
    words = text.split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

def count_words_with_counter(text):
    """
    Count the occurrences of words in a given text using a Counter object from the collections module.

    Args:
        text (str): The input text in which to count words.

    Returns:
        collections.Counter: A Counter object where keys are unique words and values are their respective counts.

    Example:
        word_counts = count_words_with_counter("This is a sample text. This text contains words.")
    """
    words = text.split()
    word_count = collections.Counter(words)
    return word_count

@execution_time_decorator
def count_dict(text):
    """
    Measure the execution time of counting words in a text using a dictionary.

    Args:
        text (str): The input text in which to count words.

    Returns:
        tuple: A tuple containing a dictionary with word counts and the execution time in seconds.

    Example:
        result, execution_time = count_dict("This is a sample text. This text contains words.")
    """
    return count_words_with_dict(text)
        
@execution_time_decorator
def count_counter(text):
    """
    Measure the execution time of counting words in a text using a Counter object.

    Args:
        text (str): The input text in which to count words.

    Returns:
        tuple: A tuple containing a Counter object with word counts and the execution time in seconds.

    Example:
        result, execution_time = count_counter("This is a sample text. This text contains words.")
    """
    return count_words_with_counter(text)