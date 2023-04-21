##################################################################
# LOG

def log(sentence: str):
    print(f"****** {sentence}")


def log_error(sentence: str):
    print(f"****** ERROR: ****** {sentence}")


def log_error_input(sentence: str):
    print(f"****** ERROR: ===== INPUT ****** {sentence}")


def log_plugin(sentence: str):
    print(f"****** ===== PLUGINS ****** {sentence}")


def log_error_plugins(sentence: str):
    print(f"****** ERROR: ===== PLUGINS ****** {sentence}")


##################################################################

##################################################################
# Exception

class MyException(Exception):
    msg = ""

    def __init__(self, message: str = ""):
        self.msg = message


##################################################################
