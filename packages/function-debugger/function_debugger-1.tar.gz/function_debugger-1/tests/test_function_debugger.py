import inspect

def logger(text = "") :
    stack = inspect.stack()
    caller = stack[1].function
    print(caller + text)
    return caller

def test() :
    logger()

test()