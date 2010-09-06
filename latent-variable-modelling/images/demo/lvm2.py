# Standard library imports
from optparse import OptionParser
import sys

# Major library imports
from numpy import array, linspace, meshgrid, nanmin, nanmax,  pi, zeros

# Enthought library imports
from enthought.chaco.api import ArrayDataSource, ArrayPlotData, ColorBar, ContourLinePlot, \
                                 ColormappedScatterPlot, CMapImagePlot, \
                                 ContourPolyPlot, DataRange1D, VPlotContainer, \
                                 DataRange2D, GridMapper, GridDataSource, \
                                 HPlotContainer, ImageData, LinearMapper, \
                                 LinePlot, OverlayPlotContainer, Plot, PlotAxis
from enthought.chaco.default_colormaps import *
from enthought.enable.component_editor import ComponentEditor
from enthought.chaco.tools.api import LineInspector, PanTool, RangeSelection, \
                                   RangeSelectionOverlay, SimpleZoom
from enthought.enable.api import Window
from enthought.traits.api import Any, Array, Callable, CFloat, CInt, Enum, Event, Float, HasTraits, \
                             Int, Instance, Str, Trait, on_trait_change, Range
from enthought.traits.ui.api import Group, Handler, HGroup, Item, View
from enthought.traits.ui.menu import Action, CloseAction, Menu, \
                                     MenuBar, NoButtons, Separator


import numpy as np
import scipy.stats

class Model(HasTraits):

    #Traits view definitions:
    traits_view = View( Item(name='Oil'),
                        Item(name='Density'),
                        Item(name='Crispy'),
                        Item(name='Fracture'),
                        Item(name='Hardness'),
                        buttons=["OK", "Cancel"]
                        )

    function = Str("tanh(x**2+y)*cos(y)*jn(0,x+y*2)")
    
    Oil = Range(low=14.0,       high=23.0,   value=17.2)
    Density = Range(low=2500.0, high=3200.0, value=2857.6)
    Crispy = Range(low=7.0,     high=15.0,   value=11.520)
    Fracture = Range(low=9.0,   high=33.0,   value=20.860)
    Hardness = Range(low=60.0,  high=200.0,  value=128.180)
    
    A = 2
    N = 50  
    K = 6
    S = np.array([1.741, 1.138])
    SPEXlim = 10.000
    HotT2lim = 10.000
    new_score = Array
    new_observation = Array
    center = Array(value=[17.202, 2857.600,   11.520,   20.860,  128.180])
    scale = Array(value=[1.592007, 124.499980,   1.775571,   5.466073,  31.127578])
    P = Array(value=np.array([[0.45753343, -0.47874550,  0.5323877, -0.5044769,  0.1534026], [-0.37043885,  0.35674997,  0.1976610, -0.2212399,  0.8046661]]).T)
    
    X = Array(value=np.loadtxt('food-texture.csv', skiprows=1, delimiter=','))
    #X_mcuv = (X - self.center) / self.scale
    #scores = Array(value=np.dot(X_mcuv, self.P))

    npts_x = CInt(400)
    npts_y = CInt(200)

    min_x = CFloat(-2*pi)
    max_x = CFloat(2*pi)
    min_y = CFloat(-1.5*pi)
    max_y = CFloat(1.5*pi)

    xs = Array
    ys = Array
    zs = Array

    minz = Float
    maxz = Float

    model_changed = Event

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        self.compute_model()

    def compute_model(self):
        self.new_observation = np.array([self.Oil, self.Density, self.Crispy, self.Fracture, self.Hardness])
        x_mcuv = (self.new_observation - self.center) / self.scale
        self.new_score = np.dot(x_mcuv, self.P)
        self.model_changed = True
        self.npts_x = int(self.Crispy)
        
        self.xs = linspace(self.min_x, self.max_x, self.npts_x)
        self.ys = linspace(self.min_y, self.max_y, self.npts_y)
        x, y = meshgrid(self.xs,self.ys)
        try:
            d = dict(x=x, y=y)
            exec "from scipy import *" in d 
            exec "from scipy.special import *" in d 
            self.zs = eval(self.function, d) 
            self.minz = nanmin(self.zs)
            self.maxz = nanmax(self.zs)
            self.model_changed = True
            self._function = self.function
        except:
            self.set(function = self._function, trait_change_notify=False)

    def _anytrait_changed(self, name, value):
        if name in ['function', 'npts_x', 'npts_y', 
                    'min_x', 'max_x', 'min_y', 'max_y', 'Oil', 'Density', 'Crispy', 'Fracture', 'Hardness']:
            self.compute_model()  


class PlotUI(HasTraits):

    #Traits view definitions:
    traits_view = View(
        Group(Item('container',
                   editor=ComponentEditor(size=(800,600)),
                   show_label=False)),
        buttons=NoButtons,
        resizable=True)

    plot_edit_view = View(
        Group(Item('num_levels'),
              Item('colormap')),
              buttons=["OK","Cancel"])


    num_levels = Int(15)
    colormap = Enum(color_map_name_dict.keys())

    #---------------------------------------------------------------------------
    # Private Traits
    #---------------------------------------------------------------------------
    
    _image_index = Instance(GridDataSource)
    _image_value = Instance(ImageData)

    _cmap = Trait(jet, Callable)

    #---------------------------------------------------------------------------
    # Public View interface
    #---------------------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        super(PlotUI, self).__init__(*args, **kwargs)
        self.create_plot()

    def create_plot(self):

        # Create the mapper, etc
        self._image_index = GridDataSource(array([]), 
                                          array([]), 
                                          sort_order=("ascending","ascending"))
        image_index_range = DataRange2D(self._image_index)
        self._image_index.on_trait_change(self._metadata_changed, 
                                          "metadata_changed")
        
        self._image_value = ImageData(data=array([]), value_depth=1)
        image_value_range = DataRange1D(self._image_value)



        # Create the contour plots
        self.polyplot = ContourPolyPlot(index=self._image_index, 
                                        value=self._image_value, 
                                        index_mapper=GridMapper(range=
                                            image_index_range), 
                                        color_mapper=\
                                            self._cmap(image_value_range),
                                        levels=self.num_levels)

        self.lineplot = ContourLinePlot(index=self._image_index, 
                                        value=self._image_value, 
                                        index_mapper=GridMapper(range=
                                            self.polyplot.index_mapper.range),
                                        levels=self.num_levels)


        # Add a left axis to the plot
        left = PlotAxis(orientation='left',
                        title= "y",
                        mapper=self.polyplot.index_mapper._ymapper,
                        component=self.polyplot)
        self.polyplot.overlays.append(left)
    
        # Add a bottom axis to the plot
        bottom = PlotAxis(orientation='bottom',
                          title= "x",
                          mapper=self.polyplot.index_mapper._xmapper,
                          component=self.polyplot)
        self.polyplot.overlays.append(bottom)


        # Add some tools to the plot
        self.polyplot.tools.append(PanTool(self.polyplot, 
                                           constrain_key="shift"))
        self.polyplot.overlays.append(SimpleZoom(component=self.polyplot, 
                                            tool_mode="box", always_on=False))
        self.polyplot.overlays.append(LineInspector(component=self.polyplot, 
                                               axis='index_x',
                                               inspect_mode="indexed",
                                               write_metadata=True,
                                               is_listener=False, 
                                               color="white"))
        self.polyplot.overlays.append(LineInspector(component=self.polyplot, 
                                               axis='index_y',
                                               inspect_mode="indexed",
                                               write_metadata=True,
                                               color="white",
                                               is_listener=False))
       
        # Add these two plots to one container
        contour_container = OverlayPlotContainer(padding=20,
                                                 use_backbuffer=True, 
                                                 unified_draw=True)
        contour_container.add(self.polyplot)
        contour_container.add(self.lineplot)


        # Create a colorbar
        cbar_index_mapper = LinearMapper(range=image_value_range)
        self.colorbar = ColorBar(index_mapper=cbar_index_mapper,
                                 plot=self.polyplot,
                                 padding_top=self.polyplot.padding_top,
                                 padding_bottom=self.polyplot.padding_bottom,
                                 padding_right=40,
                                 resizable='v',
                                 width=30)

        self.pd = ArrayPlotData(line_index = array([]),
                                line_value = array([]),
                                scatter_index = array([]),
                                scatter_value = array([]),
                                scatter_color = array([]))

        self.cross_plot = Plot(self.pd, resizable="h")
        self.cross_plot.height = 100
        self.cross_plot.padding = 20
        self.cross_plot.plot(("line_index", "line_value"), 
                             line_style="dot")
        self.cross_plot.plot(("scatter_index","scatter_value","scatter_color"),
                             type="cmap_scatter",
                             name="dot",
                             color_mapper=self._cmap(image_value_range),
                             marker="circle", 
                             marker_size=8)

        self.cross_plot.index_range = self.polyplot.index_range.x_range

        self.pd.set_data("line_index2", array([])) 
        self.pd.set_data("line_value2", array([])) 
        self.pd.set_data("scatter_index2", array([])) 
        self.pd.set_data("scatter_value2", array([])) 
        self.pd.set_data("scatter_color2", array([])) 

        self.cross_plot2 = Plot(self.pd, width = 140, orientation="v", resizable="v", padding=20, padding_bottom=160)
        self.cross_plot2.plot(("line_index2", "line_value2"), 
                             line_style="dot")
        self.cross_plot2.plot(("scatter_index2","scatter_value2","scatter_color2"),
                             type="cmap_scatter",
                             name="dot",
                             color_mapper=self._cmap(image_value_range),
                             marker="circle", 
                             marker_size=8)

        self.cross_plot2.index_range = self.polyplot.index_range.y_range


        
        # Create a container and add components
        self.container = HPlotContainer(padding=40, fill_padding=True,
                                        bgcolor = "white", use_backbuffer=False)
        inner_cont = VPlotContainer(padding=0, use_backbuffer=True)
        inner_cont.add(self.cross_plot)
        inner_cont.add(contour_container)
        self.container.add(self.colorbar)
        self.container.add(inner_cont)
        self.container.add(self.cross_plot2)


    def update(self, model):
        self.minz = model.minz
        self.maxz = model.maxz
        self.colorbar.index_mapper.range.low = self.minz
        self.colorbar.index_mapper.range.high = self.maxz
        self._image_index.set_data(model.xs, model.ys)
        self._image_value.data = model.zs
        self.pd.set_data("line_index", model.xs)
        self.pd.set_data("line_index2", model.ys)
        self.container.invalidate_draw()
        self.container.request_redraw()
 

    #---------------------------------------------------------------------------
    # Event handlers
    #---------------------------------------------------------------------------

    def _metadata_changed(self, old, new):
        """ This function takes out a cross section from the image data, based
        on the line inspector selections, and updates the line and scatter 
        plots."""
        
        self.cross_plot.value_range.low = self.minz 
        self.cross_plot.value_range.high = self.maxz
        self.cross_plot2.value_range.low = self.minz 
        self.cross_plot2.value_range.high = self.maxz
        if self._image_index.metadata.has_key("selections"):
            x_ndx, y_ndx = self._image_index.metadata["selections"]
            if y_ndx and x_ndx:
                self.pd.set_data("line_value", 
                                 self._image_value.data[y_ndx,:])
                self.pd.set_data("line_value2", 
                                 self._image_value.data[:,x_ndx])
                xdata, ydata = self._image_index.get_data()
                xdata, ydata = xdata.get_data(), ydata.get_data()
                self.pd.set_data("scatter_index", array([xdata[x_ndx]]))
                self.pd.set_data("scatter_index2", array([ydata[y_ndx]]))
                self.pd.set_data("scatter_value",
                    array([self._image_value.data[y_ndx, x_ndx]]))
                self.pd.set_data("scatter_value2",
                    array([self._image_value.data[y_ndx, x_ndx]]))
                self.pd.set_data("scatter_color",
                    array([self._image_value.data[y_ndx, x_ndx]]))
                self.pd.set_data("scatter_color2",
                    array([self._image_value.data[y_ndx, x_ndx]]))
        else:
            self.pd.set_data("scatter_value", array([]))
            self.pd.set_data("scatter_value2", array([]))
            self.pd.set_data("line_value", array([]))
            self.pd.set_data("line_value2", array([]))

    def _colormap_changed(self):
        self._cmap = color_map_name_dict[self.colormap]
        if hasattr(self, "polyplot"):
            value_range = self.polyplot.color_mapper.range
            self.polyplot.color_mapper = self._cmap(value_range)
            value_range = self.cross_plot.color_mapper.range
            self.cross_plot.color_mapper = self._cmap(value_range)
            # FIXME: change when we decide how best to update plots using 
            # the shared colormap in plot object
            self.cross_plot.plots["dot"][0].color_mapper = self._cmap(value_range)
            self.cross_plot2.plots["dot"][0].color_mapper = self._cmap(value_range)
            self.container.request_redraw()

    def _num_levels_changed(self):
        if self.num_levels > 3:
            self.polyplot.levels = self.num_levels
            self.lineplot.levels = self.num_levels



class Controller(Handler):

    #---------------------------------------------------------------------------
    # State traits
    #---------------------------------------------------------------------------

    model = Instance(Model)
    view = Instance(PlotUI)

    #---------------------------------------------------------------------------
    # Handler interface
    #---------------------------------------------------------------------------

    def init(self, info):
        self.model = info.object.model
        self.view = info.object.view
        self.model.on_trait_change(self._model_changed, "model_changed")


    #---------------------------------------------------------------------------
    # Public Controller interface
    #---------------------------------------------------------------------------

    def edit_model(self, ui_info):
        self.model.configure_traits()

    def edit_plot(self, ui_info):
        self.view.configure_traits(view="plot_edit_view")


    #---------------------------------------------------------------------------
    # Private Controller interface
    #---------------------------------------------------------------------------

    def _model_changed(self):
        if self.view is not None: 
            self.view.update(self.model)

class ModelView(HasTraits):
    
    model = Instance(Model)
    view = Instance(PlotUI)
    traits_view = View(Item('@view', 
                            show_label=False),
                       menubar=MenuBar(Menu(Action(name="Edit Model",
                                                   action="edit_model"),
                                            Action(name="Edit Plot",
                                                   action="edit_plot"),
                                            CloseAction,
                                            name="File")),
                       handler = Controller,
                       title = "Function Inspector", 
                       resizable=True)
    
    @on_trait_change('model, view')
    def update_view(self):
        if self.model is not None and self.view is not None:
            self.view.update(self.model)
        
options_dict = {'colormap' : "jet", 
                'num_levels' : 15,
                'function' : "tanh(x**2+y)*cos(y)*jn(0,x+y*2)"}
model=Model(**options_dict)
view=PlotUI(**options_dict)
popup = ModelView(model=model, view=view)

def show_plot(**kwargs):
    model = Model(**kwargs)
    view = PlotUI(**kwargs)
    modelview=ModelView(model=model, view=view)
    modelview.configure_traits()

def main(argv=None):

    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage, version="%prog 1.0")

    parser.add_option("-c", "--colormap",
                  action="store", type="string", dest="colormap", default="jet",
                  metavar="CMAP", help="choose a default colormapper")

    parser.add_option("-n", "--nlevels",
                  action="store", type="int", dest="num_levels", default=15,
                  help="number countour levels to plot [default: %default]")

    parser.add_option("-f", "--function",
                  action="store", type="string", dest="function", 
                  default="tanh(x**2+y)*cos(y)*jn(0,x+y*2)",
                  help="function of x and y [default: %default]")

    opts, args = parser.parse_args(argv[1:])

    if len(args) > 0:
        parser.error("Incorrect number of arguments")
        
    show_plot(colormap=opts.colormap, num_levels=opts.num_levels,
              function=opts.function)

if __name__ == "__main__":
    sys.exit(main())
