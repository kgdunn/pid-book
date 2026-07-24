# HAMILTON A: total annual snowfall and the average of the monthly
# mean temperature, 2000 to 2008, against the 1971 to 2000 normals.
import pandas as pd
import plotly.graph_objects as go

weather = pd.DataFrame({
    "Year": range(2000, 2009),
    "Snowfall": [170.9, 94.1, 138.0, 166.2, 175.8, 218.4, 56.6, 182.4, 243.2],
    "Temperature": [7.6, 8.8, 8.8, 7.3, 7.7, 8.2, 9.1, 8.2, 7.7],
})
normals = {"Snowfall": 161.8, "Temperature": 7.6}
titles = {"Snowfall": "Snowfall (cm)",
          "Temperature": "Average annual temperature (°C)"}

for column, title in titles.items():
    fig = go.Figure()
    fig.add_scatter(x=weather["Year"], y=weather[column], mode="lines+markers")
    fig.add_hline(y=normals[column], line_dash="dash",
                  annotation_text="Averaged over 1971 to 2000 data")
    fig.update_layout(xaxis_title_text="Year", yaxis_title_text=title,
                      showlegend=False)
    fig.show()
