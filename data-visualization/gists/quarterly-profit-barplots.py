import pandas as pd

pd.options.plotting.backend = "plotly"

labels = ["2008 Q1", "Q2", "Q3", "Q4", "2009 Q1", "Q2", "Q3", "Q4"]
profit = pd.DataFrame(
    data=[45, 32, 67, 23, 42, 56, 64, 92],
    index=labels,
    columns=["Quarterly profit ($ '000)"],
) + 40

# Draw a bar plot.
fig = profit.plot.bar()
fig.update_traces(
    text=profit["Quarterly profit ($ '000)"],
    textposition="outside",
)
fig.update_layout(
    yaxis_title_text="Quarterly profit ($ '000)",
    showlegend=False,
)
fig.show()

# Now rather use a line plot.
fig = profit.plot.line(markers=True)
fig.update_layout(
    yaxis_title_text="Quarterly profit ($ '000)",
    showlegend=False,
)
fig.show()
