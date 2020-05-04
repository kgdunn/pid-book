import pandas as pd
import matplotlib.pyplot as plt

labels = ["2008 Q1", "Q2", "Q3", "Q4", "2009 Q1", "Q2", "Q3", "Q4"]
profit = (
    pd.DataFrame(
        data=[45, 32, 67, 23, 42, 56, 64, 92],
        index=labels,
        columns=["Quarterly profit ($ '000)"]
    )
    + 40
)

# # Draw a bar-plot
ax = profit.plot.bar()
ax.set_ylabel("Quarterly profit ($ '000)")
plt.show()

# Now rather use a line plot.
ax = profit.plot.line(marker="o")
ax.set_ylabel("Quarterly profit ($ '000)")
plt.show()
