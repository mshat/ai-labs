from config import DEBUG


def debug_print(function):
    def wrapper(*args, **kwargs):
        if DEBUG:
            print(f'[DEBUG] {args[0].debug_msg}')
        return function(*args, **kwargs)

    return wrapper


def debug_print_with_arg(msg: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if DEBUG:
                print(f'[DEBUG] {msg}')
            return function(*args, **kwargs)

        return wrapper
    return decorator
