import matplotlib.pyplot as plt


def main_plugin(values: list[float | int]):
    print("DUMMY PLUGIN CALLED")
    show(values=values)


def show(values: list[float | int]):
    print("DUMMY PLUGIN START")
    print("Values:")
    print(values)
    print("DUMMY PLUGIN END")
