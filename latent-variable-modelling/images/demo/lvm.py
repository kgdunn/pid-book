# Kevin Dunn, ConnectMV, Inc., May 2010.
from enthought.traits.api import HasTraits, Instance, Range, Array, Property
from enthought.traits.ui.api import View, Item, HGroup
from enthought.traits.ui.menu import OKButton, RevertButton
from enthought.chaco.api import Plot, ArrayPlotData
from enthought.enable.component_editor import ComponentEditor
import numpy as np

class Model(HasTraits):
    container = Instance(Plot)
        
    Oil = Range(low=14.0,       high=23.0,   value=17.2)
    Density = Range(low=2500.0, high=3200.0, value=2857.6)
    Crispy = Range(low=7.0,     high=15.0,   value=11.520)
    Fracture = Range(low=9.0,   high=33.0,   value=20.860)
    Hardness = Range(low=60.0,  high=200.0,  value=128.180)
    
    # Dimensions of the multivariate model
    A = 2
    N = 50  
    K = 6
    # Loadings:
    P = Array(value=np.array([[0.45753343, -0.47874550,  0.5323877, -0.5044769,  0.1534026], [-0.37043885,  0.35674997,  0.1976610, -0.2212399,  0.8046661]]).T)
    S = np.array([1.741, 1.138])  # Score standard deviations (not used in this demo)

    center = Array(value=[17.202, 2857.600,   11.520,   20.860,  128.180])
    scale = Array(value=[1.592007, 124.499980,   1.775571,   5.466073,  31.127578])

    new_score = Property(Array, depends_on=['new_observation'])
    new_observation = Property(dtype=np.float, shape=(K, 1), depends_on=['Oil', 'Density', 'Crispy', 'Fracture', 'Hardness'])
    
    traits_view = View( Item('container', editor=ComponentEditor(), show_label=False),
                        Item(name='Oil'),
                        Item(name='Density'),
                        Item(name='Crispy'),
                        Item(name='Fracture'),
                        Item(name='Hardness'),
                        resizable=True,
                        buttons = [RevertButton, OKButton],
                        title='Interactive score plot',
                        width=900, height=800
                      )

    def __init__(self):
        super(Model, self).__init__()
        X = np.loadtxt('food-texture.csv', skiprows=1, delimiter=',')
        X_mcuv = (X - self.center) / self.scale
        self.scores = np.dot(X_mcuv, self.P) # T = XP
        
        self._run_plot()
        self.on_trait_change(self._run_plot, 'Oil')
        self.on_trait_change(self._run_plot, 'Density')
        self.on_trait_change(self._run_plot, 'Crispy')
        self.on_trait_change(self._run_plot, 'Fracture')
        self.on_trait_change(self._run_plot, 'Hardness')
        
        

    def _get_new_observation(self):
        return np.array([self.Oil, self.Density, self.Crispy, self.Fracture, self.Hardness])
    
    def _get_new_score(self):
        x_new = (self.new_observation - self.center) / self.scale
        return np.dot(x_new, self.P)
        
    def _run_plot(self):
        x = self.scores[:,0]
        y = self.scores[:,1]
        th_new = np.array([self.new_score[0]])
        tv_new = np.array([self.new_score[1]])
        x_hat = np.dot(self.new_score, self.P.T) # x_predicted = TP'
        e = x_hat - (self.new_observation - self.center) / self.scale # E = X_predicted - X_actual
        SPE = np.sum(e*e)
        
        plotdata = ArrayPlotData(x=x, y=y, x_new=th_new, y_new=tv_new)
        plot = self.plot = Plot(plotdata)
        plot.plot(("x", "y"), type="scatter", color="black")
        plot.plot(("x_new", "y_new"), type="scatter", color="red", marker = "circle", marker_size = 6,) 
        plot.bgcolor = 'white'
        plot.index_axis.title = 't1'
        plot.index_axis.title_font = "modern 16"
        plot.value_axis.title = 't2'
        plot.value_axis.title_font = "modern 16"
        plot.title = "Score plot (SPE for red point = " + str(round(SPE,2)) + ')'
        plot.title_font = "modern 20"
        value_range =  plot.plots.values()[0][0].value_mapper.range
        value_range.low = -2.6
        value_range.high = 2.6
        index_range =  plot.plots.values()[0][0].index_mapper.range
        index_range.low = -4.4
        index_range.high = 4.4
        self.container = plot
 
if __name__ == "__main__":
    Model().configure_traits()