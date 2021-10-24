import pandas as pd
import matplotlib.pyplot as plt

all_boards = pd.read_csv("http://openmv.net/file/six-point-board-thickness.csv")
boards = all_boards.iloc[0:100, 1:7]

# Look at the start and end of the data
# Examine and summarize your data before
# doing anything else
boards.head()
boards.tail()
boards.describe()
ax = boards.plot.box(fontsize=16)
plt.show()
