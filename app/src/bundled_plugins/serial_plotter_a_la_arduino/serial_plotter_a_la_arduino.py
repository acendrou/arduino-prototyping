import matplotlib.pyplot as plt


def main_plugin(values: list[int]):
    show(values=values)


def show(values: list[int]):
    try:
        plt.style.use('_mpl-gallery')
        # plot
        fig, ax = plt.subplots()
        ax.stem(values, linefmt="-", markerfmt='C0o')
        plt.show(block=False)

    except:
        print("Undefined error")