import threading

def new():
    # method1: use __new__ method to return same instance
    class Single(object):
        _instance = None
        def __new__(cls, *args, **kw):
            print("__new__")
            if cls._instance is None:
                cls._instance = object.__new__(cls, *args, **kw)
            return cls._instance
        def __init__(self):
            print("__init__")
    single1 = Single()
    single2 = Single()
    print(id(single1) == id(single2))

def thread_safe():
    # thread safe singleton
    # https://medium.com/analytics-vidhya/how-to-create-a-thread-safe-singleton-class-in-python-822e1170a7f6
    class SingletonThreadSafe:
        _instance = None
        _lock = threading.Lock()

        def __new__(cls):
            if not cls._instance:  # This is the only difference
                with cls._lock:
                    if not cls._instance:
                        cls._instance = super().__new__(cls)
            return cls._instance


def method_decorator():
    def singleton(cls):
        _instance = {}

        # will recover class __new__ method
        def inner():
            if cls not in _instance:
                _instance[cls] = cls()
            return _instance[cls]
        return inner
        
    @singleton
    class Cls(object):
        def __init__(self):
            pass

    single1 = Cls()
    single2 = Cls()
    print(id(single1) == id(single2))

# metaclass: 
# https://stackoverflow.com/a/6581949
# https://lotabout.me/2018/Understanding-Python-MetaClass/
def metaclass():
    class Singleton(type):
        _instances = {}
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]

    class Cls4(metaclass=Singleton):
        pass

    single1 = Cls4()
    single2 = Cls4()
    print(id(single1) == id(single2))

if __name__ == '__main__':
    singleton_type = "new"
    import sys
    if len(sys.argv) > 1:
        singleton_type = sys.argv[1]
    if singleton_type == "new":
        new()
    elif singleton_type == "decorator":
        method_decorator()
    elif singleton_type == "thread":
        thread_safe()
    elif singleton_type == "metaclass":
        metaclass()