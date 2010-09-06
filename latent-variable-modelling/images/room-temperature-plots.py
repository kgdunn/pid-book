import numpy as np
from matplotlib.dates import DayLocator, DateFormatter
from matplotlib.figure import Figure
import datetime

np.random.seed(21)

days = DayLocator()
dayFmt = DateFormatter('%a')
T_low = 295
T_range = 3

# Generate the temperature data
# -------------------------------
time = np.arange(0, 3, 1/48.0) # 30 minute increments
N = time.shape[0]

base_temp = (np.sin(time * np.pi * 2)  + np.cos(time * np.pi * 2))  * T_range/2 + T_low  
base_temp = base_temp.reshape(N,1)
base_temp = np.append(base_temp, base_temp,  axis=1)
base_temp = np.append(base_temp, base_temp,  axis=1)

dates = time + datetime.date.toordinal(datetime.date.today()) - 1.5
base_temp[:,0] += np.random.normal(loc=0.0, scale=T_range/6.0, size=N)
base_temp[:,1] += np.random.normal(loc=0.0, scale=T_range/6.0, size=N)
base_temp[:,2] += np.random.normal(loc=0.0, scale=T_range/6.0, size=N)
base_temp[:,3] += np.random.normal(loc=0.0, scale=T_range/6.0, size=N)

# Add a dip:
dipper = np.zeros(N)
slope = -1/5.0
start_pt = 40
end_pt = 50
bias = -start_pt * slope
dipper[start_pt:end_pt] += np.arange(start_pt, end_pt) * slope + bias
dipper[end_pt:end_pt+end_pt-start_pt] += np.arange(end_pt, end_pt+end_pt-start_pt) * -slope - 2*bias + 1/3.0
base_temp[:,0] += dipper + np.random.normal(loc=0.0, scale=T_range/6.0, size=N)
base_temp[:,1] += dipper + + np.random.normal(loc=0.0, scale=T_range/6.0, size=N)

# Add a spike:
base_temp[N-39,2] -= 4.0

# Round everything
base_temp = np.round(base_temp,1)

# Record to disk
#np.savetxt('room-temperature.csv', base_temp, fmt='%5.1f', delimiter=',')

# Load the data
base_temp = np.loadtxt('room-temperature.csv', delimiter=',', skiprows=1)


# Plot the results
# -------------------------------
fig = Figure(figsize=(8, 5))

def format_ax(ax, ylabel):
    """ Make some additional axis formatting """
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(dayFmt)
    ax.autoscale_view()
    ax.fmt_xdata = DateFormatter('%a')
    ax.grid(True)
    
    y_ticklabels = [290, 295, 300]
    ax.text(dates[2], 290.5, ylabel, color="blue", va='bottom')
    ax.set_ylim([290, 300])
    ax.yaxis.set_ticks(y_ticklabels)
    tick_items = []
    for entry in y_ticklabels:
        tick_items.append(str(int(entry)))
    ax.yaxis.set_ticklabels(tick_items)
    
ax1 = fig.add_subplot(411)
ax1.plot_date(dates, base_temp[:,0], 'k-', )
ax1.set_title("Temperature of a room, measured at the 4 corners")
format_ax(ax1, "Front left")

ax2 = fig.add_subplot(412)
ax2.plot_date(dates, base_temp[:,1], 'k-')
format_ax(ax2, "Front right")

ax3 = fig.add_subplot(413)
ax3.plot_date(dates, base_temp[:,2], 'k-')
format_ax(ax3, "Back left")

ax4 = fig.add_subplot(414)
ax4.plot_date(dates, base_temp[:,3], 'k-')
format_ax(ax4, "Back right")


fig.autofmt_xdate()
from matplotlib.backends.backend_agg import FigureCanvasAgg
canvas=FigureCanvasAgg(fig)
fig.savefig('room-temperature-plots.png', dpi=300, facecolor='w', edgecolor='w', orientation='landscape', papertype=None, format=None, transparent=True)

