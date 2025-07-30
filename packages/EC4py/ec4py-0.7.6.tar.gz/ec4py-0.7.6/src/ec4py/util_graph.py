"""
Utility module.

"""

#import math
from scipy.signal import savgol_filter, medfilt
import numpy as np
#from scipy import ndimage, datasets
import matplotlib.pyplot as plt
from collections import namedtuple
#from fractions import Fraction
#import matplotlib.pyplot as plt
from enum import StrEnum
#from .util import Quantity_Value_Unit as Q_V
import copy


NEWPLOT = "new_plot"

NO_PLOT = "no_plot"

SAVEFIG = "savefig"

Figure = namedtuple("Figure", ["fig", "plots"])
"""Tuplet:
    - fig   : a plt.figure() object.
    - plots :  subplots of the figure
"""

ANALYSE_PLOT = "analyse_plot"
DATA_PLOT = "data_plot"
PLOT = "plot"

class ENUM_legend(StrEnum):
    NONE ="_"
    NAME = "legend_name"
    DATE = "legend_date"
    TIME = "legend_time"
    DATETIME = "legend_datetime"
    ROT = "legend_rot"
    RATE = "legend_rate"
    VSTART = "legend_start"
    V1 = "legend_v1"
    V2 = "legend_v2"
    MWE_CH = "legend_MWE"

LEGEND = ENUM_legend

class ENUM_plotKW(StrEnum):
    LABEL = "label"
    LINESTYLE = "linestyle"
    LINEWIDTH = "linewidth"
    COLOR ="color"
    GRID = "grid"
    XLABEL = "xlabel"
    YLABEL = "ylabel"
    ALPHA = "alpha"
    TITLE = "title"
    XLIM = "xlim"
    YLIM = "ylim"
    figheight = "figheight"
    figwidth = "figwidth"



def update_legend(*args,**kwargs):
    loc_args = list(args) 
    #loc_args.insert(0,listargs)
    default_legend=kwargs.get("default_legend",None)
    if default_legend is not None:
         loc_args.insert(0,default_legend)
   
    for arg in loc_args:
        if isinstance(arg,ENUM_legend):
            kwargs["legend"]=str(arg).replace("legend_","")
        if isinstance(arg,str):
            if arg.startswith("legend"):
                kwargs["legend"]=str(arg).replace("legend_","")
    return kwargs


def fig_change(fig,**kwargs):
    """Change the figure size and title.

    Args:
        fig (Figure): Figure object to be changed.
        **kwargs: Keyword arguments for figure properties.

    Returns:
        Figure: Updated figure object.
    """
    fig.set_figheight(kwargs.get(ENUM_plotKW.figheight.value,6))
    fig.set_figwidth(kwargs.get(ENUM_plotKW.figwidth.value,8))
    fig.suptitle(kwargs.get(ENUM_plotKW.TITLE.value,""))
    return fig

def plot_change(ax,**kwargs):
    """Change the plot properties.

    Args:
        ax (Axes): Axes object to be changed.
        **kwargs: Keyword arguments for plot properties.

    Returns:
        Axes: Updated axes object.
    """
    if kwargs.get(ENUM_plotKW.GRID.value,False):
        ax.grid()
    if kwargs.get(ENUM_plotKW.XLIM.value,None) is not None:
        ax.set_xlim(kwargs.get(ENUM_plotKW.XLIM.value,None))
    if kwargs.get(ENUM_plotKW.YLIM.value,None) is not None:
        ax.set_ylim(kwargs.get(ENUM_plotKW.YLIM.value,None))
    return ax

def make_plot_1x(Title:str,**kwargs):
    
    fig = plt.figure()
    fig_change(fig,**kwargs)
    
    plt.suptitle(Title)
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=1.0, hspace=0.8)
    plot1 = fig.subplots()
    plot_change(plot1,**kwargs)
    #if kwargs.get("grid",False):
    #    plot1.grid()
    #if kwargs.get(ENUM_plotKW.XLIM.value,None) is not None:
    #    plot1.set_xlim(kwargs.get(ENUM_plotKW.XLIM.value,None))
    #if kwargs.get(ENUM_plotKW.YLIM.value,None) is not None:
    #    plot1.set_ylim(kwargs.get(ENUM_plotKW.YLIM.value,None))
    return Figure(fig,[plot1])

def make_plot_2x(Title:str,Vertical = False,**kwargs):
    """Vertical?"""
    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(13)
    plt.suptitle(Title)
    if Vertical:
        fig.set_figheight(5)
        fig.set_figwidth(4)
        plot1,plot2 = fig.subplots(2,1)
    else:
        fig.set_figheight(5)
        fig.set_figwidth(13)
        plot1,plot2 = fig.subplots(1,2)
    if kwargs.get(ENUM_plotKW.GRID.value,False):
        plot1.grid()
        plot2.grid()
    return Figure(fig,[plot1,plot2])
    #
    #return plot1, plot2
    
def make_plot_2x_1(Title:str,**kwargs):
    fig = plt.figure()
    fig.set_figheight(4)
    fig.set_figwidth(10)
    plt.suptitle(Title)
    ax_right = fig.add_subplot(122)
    ax_left_top = fig.add_subplot(221)
    ax_left_bottom = fig.add_subplot(223)
    ax_left_bottom.label_outer()
    ax_left_top.label_outer()
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.3)
    #plot1,plot2 = fig.subplots(1,2)
    if kwargs.get(ENUM_plotKW.GRID.value,False):
        ax_right.grid()
        ax_left_top.grid()
        ax_left_bottom.grid()
        
    return Figure(fig,[ax_left_top, ax_left_bottom, ax_right ])
    # return ax_left_top, ax_left_bottom, ax_right


def quantity_plot_fix(s:str):
    list_of_quantities = str(s).strip().split(" ", 100)
    s_out =""
    for single_quantity in list_of_quantities:
        aa = single_quantity.strip().split("^",2)
        nyckel = aa[0]
        if len(aa)>1:                   #if "^" was found.
            nyckel = nyckel + "$^{" + aa[1] + "}$"  
        s_out = s_out +" " + nyckel
    #print("AA", s_out.strip())
    return s_out.strip() 


def should_plot_be_made(*args, **kwargs):
    """Looks in the list of args to see if a plot should be made

    Returns:
        bool: make plot? 
    """
    makePlot = True
    for arg in args:
        a=str(arg)
        if a.casefold() == NO_PLOT.casefold():
            makePlot = False
    return makePlot



def update_plot_kwargs(index, **kwargs):
    """ 

    Returns: kw
        
    """
    plot_kw = [x.value for x in ENUM_plotKW]
    #loc_kwargs = copy.deepcopy(kwargs.copy())
    loc_kwargs = kwargs.copy()
    for key,value in loc_kwargs.items():
        is_list = isinstance(value,list)
        if key in plot_kw and is_list:
            loc_kwargs[key] = value[index]
            # print(key, value[index])
    # print(loc_kwargs)
    return loc_kwargs

class plot_options:
    def __init__(self, **kwargs):
        self.fig = None
        self.name = NEWPLOT
        self.x_label="x"
        self.x_unit = "xunit"
        self.y_label = "y"
        self.y_unit = "y_unit"
        self.x_data = []
        self.y_data =[]
        #self.x = tuple(self.x_data,self.x_label,self.x_unit)
        self.options = {
            'x_smooth' : 0,
            'y_smooth' : 0,
            'y_median'   : 0,
            'yscale':None,
            'xscale':None,
            PLOT : NEWPLOT,
            'dir' : "all",
            'legend' : "_",
            ENUM_plotKW.XLABEL.value : None,
            ENUM_plotKW.YLABEL.value : None,
            'style'  : "",
            ENUM_plotKW.TITLE.value  : "",
            ENUM_plotKW.COLOR.value : None,
            ENUM_plotKW.LABEL.value : None,
            ENUM_plotKW.LINESTYLE.value : None,
            ENUM_plotKW.LINEWIDTH.value : None,
            ENUM_plotKW.GRID.value: False,
            ENUM_plotKW.ALPHA.value: None,
            ENUM_plotKW.XLIM.value: None,
            ENUM_plotKW.YLIM.value: None,
            
            
        }

        self.options.update(kwargs)
        return
    
    def set_title(self,title:str = "", override: bool=False):
        if self.options['title'] == "" or override:
            self.options['title'] = title
    
    def set_y_txt(self, label, unit):
        self.y_label = label
        self.y_unit = unit
        
    def set_x_txt(self, label, unit):
        self.x_label = label
        self.x_unit = unit
        
    def get_title(self):
        return self.options['title']       

    def get_y_txt(self):
        return str(self.y_label + " ("+ self.y_unit +")")
    def get_x_txt(self):
        return str(self.x_label + " ("+ self.x_unit +")")
    
    
    def get_legend(self):
        return str(self.options['legend'])
    
    @property
    def legend(self):
        return self.get_legend()

    @legend.setter
    def legend(self, value:str) -> str:
        self.options['legend'] = value
        #return self.get_legend()
    
    def get_x_smooth(self):
        return int(self.options['x_smooth'])
    
    def get_y_smooth(self):
        return int(self.options['y_smooth'])
    
    def get_dir(self):
        return str(self.options['dir'])
    
    def get_plot(self):
        
        
        return self.options[PLOT]
    
    def smooth_y(self, ydata =[]):
        #try:
        y_smooth = self.get_y_smooth()
        # print("SA VALUE")
        # print(y_smooth)
        if(y_smooth > 0) and len(ydata)>2:
            ydata_array= np.isnan(ydata)
            for i in range(len(ydata_array)):
                if ydata_array[i]:
                    ydata[i]=0
            ydata = savgol_filter(ydata, y_smooth+1, 1)
            for i in range(len(ydata_array)):
                if ydata_array[i]:
                    ydata[i]=np.nan
                    
            # print("SA FITER")
    #except:
        #    pass
        return ydata
    
    def median_y(self, ydata =[]):
        try:
            y_median = self.options["y_median"]
            if(y_median>0): 
                if y_median % 2 ==0:
                    y_median +=1           
                ydata_s = medfilt(ydata, y_median)
            else:
                ydata_s = ydata
        except:
            pass
        return ydata_s
    
    def smooth_x(self, xdata):
        try:
            x_smooth = self.get_x_smooth()
            if(x_smooth > 0):
                xdata = savgol_filter(xdata, x_smooth, 1)
        except:
            pass
        return xdata
            
    
    def fig(self, **kwargs):
        try:
            ax = kwargs[PLOT]
        except KeyError("plot keyword was not found"):
            #fig = plt.figure()
            #  plt.subtitle(self.name)
            fig = make_plot_1x(self.options['title'],**kwargs)
            # ax = fig.plots[0]

    def no_smooth(self):
        self.options["y_smooth"]=0
        self.options["x_smooth"]=0
        self.options["y_median"]=0
        return
    
    def exe(self):
        """_summary_

        Returns:
            line, ax: Line and ax handlers
        """
        ax = self.options[PLOT]
        # fig = None
        if ax == NEWPLOT or ax is None:
           # fig = plt.figure()
           # plt.suptitle(self.name)
            self.fig = make_plot_1x(self.options['title'],**self.options)
            ax = self.fig.plots[0]
            if self.options['yscale']:
                ax.set_yscale(self.options['yscale'])
            if self.options['xscale']:
                ax.set_xscale(self.options['xscale'])
        
        
        try:
            y_median = int(self.options['y_median'])
            if y_median > 0:
                if y_median % 2 ==0:
                    y_median +=1 
                #print("median filter Y", y_median)
                self.y_data = medfilt(self.y_data, y_median)
        except:
            pass
        self.y_data = self.smooth_y(self.y_data)
        try:
            yscale = ax.get_yscale()
            if yscale == "log":
                self.y_data=abs(self.y_data)
        except:
            pass
       
        
        try:
            x_smooth = int(self.options['x_smooth'])
            if x_smooth > 0:
                self.x_data = savgol_filter(self.x_data, x_smooth, 1)
            xscale = ax.get_xscale()
            if xscale == "log":
                self.x_data=abs(self.x_data)
        except:
            pass
        line = None
        try:
            line, = ax.plot(self.x_data, self.y_data, self.options['style'])
            # print("COLOR", self.options,self.options[ENUM_plotKW.COLOR.value])
            # print("COLOR", self.options[ENUM_plotKW.COLOR.value])
            # print("COLOR", ENUM_plotKW.COLOR.value,"SS")
            if self.x_data is not None:
                
                if len(self.get_legend())> 0:
                    if self.get_legend()[0] != "_":
                        line.set_label( quantity_plot_fix(self.get_legend()) )
                        ax.legend()
        
                #print("COLOR2", self.options[ENUM_plotKW.COLOR.value],ENUM_plotKW.COLOR.value)
                
                if self.options[ENUM_plotKW.COLOR.value] is not None:
                    #print("COLOR3", self.options[ENUM_plotKW.COLOR.value])
                    line.set_color(self.options[ENUM_plotKW.COLOR.value])
                if self.options[ENUM_plotKW.LABEL.value] is not None:   
                    line.set_label(self.options[ENUM_plotKW.LABEL.value])
                    ax.legend()
                if self.options[ENUM_plotKW.LINESTYLE.value] is not None:   
                    line.set_linestyle(self.options[ENUM_plotKW.LINESTYLE.value])
                if self.options[ENUM_plotKW.LINEWIDTH.value] is not None:   
                    line.set_linewidth(self.options[ENUM_plotKW.LINEWIDTH.value])
                if self.options[ENUM_plotKW.ALPHA.value] is not None:   
                    line.set_alpha(self.options[ENUM_plotKW.ALPHA.value])

        except:  # noqa: E722
       #     print("NO LINE",e)
           pass
        #### X label
        x_label = f'{quantity_plot_fix(self.x_label)} ({quantity_plot_fix(self.x_unit)})'
        if self.options['xlabel'] is not None:
            x_label = self.options['xlabel']
        
        ax.set_xlabel(x_label)
        #### Y label
        y_label = f'{quantity_plot_fix(self.y_label)} ({quantity_plot_fix(self.y_unit)})'
        if self.options['ylabel'] is not None:
            y_label = self.options['ylabel']
        ax.set_ylabel(f'{y_label}')
        
        return line, ax
    
    def render_plot(self):
        ax = self.options[PLOT]
        if ax == NEWPLOT or ax is None:
            return
        else:
            ax.set_xlabel(f'{quantity_plot_fix(self.x_label)} ({quantity_plot_fix(self.x_unit)})')
            
            ylabel = quantity_plot_fix(self.y_label) + " (" + quantity_plot_fix(self.y_unit)+ ")"
            ax.set_ylabel(f'{ylabel}')
        return
    
    def close(self, *args):
        # print("CLOSE:", args)
        for item in args:
            s = str(item).casefold()    
            if s == "noshow".casefold():
                # print("CLOSING")
                plt.close('all')
                break
        return
    
    def saveFig(self,**kwargs):
        #print("fig")
        saveFig(self.fig,**kwargs)
            


def saveFig(fig:Figure,**kwargs):
    if fig is not None:
            name = kwargs.get(SAVEFIG,None)
            if name is not None:
                fig.fig.savefig(name, dpi='figure', format=None, bbox_inches ="tight")
    else:
        # print("fig is non")
        pass