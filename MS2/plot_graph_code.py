import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd

data = pd.read_csv("__")

count = 0
x = []
y = []


def draw_graph(i):
    global count
    count += 1
    x.append(count)
    y.append(data['__'][count])

    plt.cla()
    plt.plot(x, y)


anima = animation.FuncAnimation(plt.gcf(), draw_graph, interval=1)

plt.show()
