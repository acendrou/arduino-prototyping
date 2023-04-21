import matplotlib.pyplot as plt


def main_plugin(values: list[float]):
    show(values=values)


def show(values: list[float]):
    try:
        plt.style.use('_mpl-gallery')
        # plot
        fig, ax = plt.subplots()
        ax.stem(values, linefmt="-", markerfmt='C0o')
        plt.show(block=False)
        # fig.figsave("fig.png")
        # subprocess.Popen("fig.png")
        # time.sleep(5)
        # time.sleep(3)
        # plt.pause(2)
        # plt.cla()
        # plt.clf()
        # plt.close()
    except:
        print("Undefined error")