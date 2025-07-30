""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""

# from nptdms import TdmsFile
import math
import numpy as np
from pathlib import Path
import copy


from .ec_data import EC_Data
from .step_data  import Step_Data

from .method_util.ec_datas_util import EC_Datas_base

from .ec_util.ec_data_util import ENUM_Channel_Names
from .method_util.util_step import step_time_range


from .util import Quantity_Value_Unit as QV
from .util_graph import plot_options,make_plot_2x_1,saveFig,LEGEND,update_plot_kwargs
#from .util_graph import update_legend
from .analysis.analysis_tafel import Tafel
from .analysis.analysis_levich import Levich


STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"

class Step_Datas(EC_Datas_base):
    """# Class to analyze CV datas. 
    Class Functions:
    - .plot() - plot data    
    
    ### Analysis:
    - .Levich() - plot data    
    - .KouLev() - Koutechy-Levich analysis    
    - .Tafel() - Tafel analysis data    
    
    ### Options args:
    "area" - to normalize to area
    
    ### Options keywords:
    legend = "name"
    """

    def __init__(self, paths:list[Path] | Path|None = None, *args,**kwargs):
        EC_Datas_base.__init__(self,*args, **kwargs)
        

        if paths is None:
            return
        if isinstance(paths,Path ):
            path_list = [paths]
        else:
            path_list = paths
        self.datas = [ Step_Data() for i in range(len(path_list))]
        index=0
        for path in path_list:
            ec = EC_Data(path)
            try:
                self.datas[index].conv(ec,**kwargs)
            finally:
                index=index+1 
        #print(index)
        return
    #############################################################################
    def __getitem__(self, item_index:slice|int): 

        if isinstance(item_index, slice):
            step = 1
            start = 0
            stop = len(self.datas)
            if item_index.step:
                step =  item_index.step
            if item_index.start:
                start = item_index.start
            if item_index.stop:
                stop = item_index.stop    
            return [self.datas[i] for i in range(start,stop,step)  ]
        else:
            return self.datas[item_index]
    #############################################################################
    def __setitem__(self, item_index:int, new_Step):
        if not isinstance(item_index, int):
            raise TypeError("key must be an integer")
        self.datas[item_index] = new_Step
  
################################################################    
    def plot(self, *args, **kwargs):
        """Plot Steps.
            use args to normalize the data
            - area or area_cm
            - rotation
            - rate
            
            #### use kwargs for other settings.
            
            - legend = "name"
            - x_smooth = 10
            - y_smooth = 10
            
            
        """
        #loc_kwargs =update_legend(*args,**kwargs)
        # print("loc_kwargs",loc_kwargs)
        p = plot_options(**kwargs)
        p.set_title("Steps")
        
        line, data_plot = p.exe()
        legend = p.legend
        datas = copy.deepcopy(self.datas)
        #CVs = [CV_Data() for i in range(len(paths))]
        
        for index, data in enumerate(datas):
            data_kwargs = update_plot_kwargs(index,**kwargs)
            #rot.append(math.sqrt(cv.rotation))
            #for arg in args:
            #    data.norm(arg)
            data_kwargs["plot"] = data_plot
            # data_kwargs["name"] = data.setup_data.name
            #if legend != "_" :
            #    data_kwargs["legend"] = data.setup_data.name
            p = data.plot(*args, **data_kwargs)
        if legend != "_" : 
            data_plot.legend()
        return data_kwargs
    
    #################################################################################################    

    def get_current_at_time(self, time_s_:float, dt_s_:float = 0,*args, **data_kwargs):
        """Get the current at a specific time.

        Args:
            time_s_ (float): _description_
            dt_s_ (float, optional): _description_. Defaults to 0.

        Returns:
            list of QV: _description_
        """
        current = [QV()] * len(self.datas)
        for i in range(len(self.datas)):
            current[i] = self.datas[i].get_current_at_time(time_s_,dt_s_,*args, **data_kwargs)
        return current
   
    def get_voltage_at_time(self, time_s_:float, dt_s_:float = 0,*args, **data_kwargs):
        """_summary_

        Args:
            time_s_ (float): _description_
            dt_s_ (float, optional): _description_. Defaults to 0.

        Returns:
            List of QV: list of voltage values
        """
        voltage = [QV()] * len(self.datas)
        for i in range(len(self.datas)):
            voltage[i] = self.datas[i].get_voltage_at_time(time_s_,dt_s_,*args, **data_kwargs)
        return voltage
    

    def integrate(self,t_start,t_end,step_nr:int = -1, *args, **kwargs):
        s = "Integrate Analysis"
        if(step_nr>-1):
            s = s + f" of step #{step_nr}"
        
        fig = make_plot_2x_1(s)
        data_plot_i = fig.plots[0]
        data_plot_E = fig.plots[1]
        analyse_plot =  fig.plots[2]
        #data_plot_i,data_plot_E, analyse_plot = make_plot_2x_1(s)
        #########################################################
            # Make plot
        data_kwargs = kwargs
        data_kwargs["plot_i"] = data_plot_i
        data_kwargs["plot_E"] = data_plot_E
        data_kwargs["analyse_plot"] = analyse_plot
        p = plot_options(**kwargs)
        charge = [QV()] * len(self.datas)
        #print(data_kwargs)
        for i in range(len(self.datas)):
            #if(step_nr>-1):
            #    step = self.datas[i].get_step(step_nr)
            #else:
            #    step = self.datas[i]
            charge[i] = (self.datas[i].integrate(t_start,t_end,step_nr,*args, **data_kwargs))
        data_plot_i.axvspan(t_start, t_end, color='C0', alpha=0.2)
        p.close(*args)
        saveFig(fig,**kwargs)
        return charge
    
    ##################################################################################################################

    def Tafel(self, *args, **kwargs):
        """Perform a Tafel analysis
    
        Keywords:
        
            - t : float time at which to take the data point. defaults to "last"     
            - dt : float time window to use for the average in seconds. defaults to 0
            or
            - t_min : float minimum time to use for data selection. Use this instead of "t" and "dt"
            - t_max : float maximum time to use for data selection. Use this instead of "t" and "dt"
            
            - Emax:float maximum voltage to use for fitting. defaults to 1000
            - Emin:float minimum voltage to use for fitting. defaults to -1000
            - step_nr (int, optional): _description_. Defaults to -1.
            
        Returns:
            Quantity_Value_Unit Tafel: slope
        """
        #t_lim = kwargs.get("t", "last")
        step_nr = kwargs.get("step_nr", -1)
        E_fit_max = kwargs.get("Emax", 1000)
        E_fit_min = kwargs.get("Emin", -1000)
        #t_lim_max = kwargs.get("t_max", None)
        #t_lim_min = kwargs.get("t_min", None)
        #d_t_s_ = kwargs.get("dt", 0.0)
        t_lims = step_time_range(self.datas,**kwargs)
        #if t_lim_max is not None and t_lim_min is not None:
        #    t_lim = (t_lim_max+t_lim_min)/2.0
        #    d_t_s_ = abs(t_lim_max-t_lim_min)
            
            
        
        #if isinstance(t_lim, str):
        #    if t_lim == "end" or t_lim == "last":
        #        t_lim = max([x.Time[-1] for x in self.datas])-d_t_s_/2.0
        #t_lim_min =  max( t_lim - d_t_s_/2.0,0)
        #t_lim_max =  min(t_lim + d_t_s_/2.0,self.datas[0].Time[-1])
        
        
        #if not isinstance(t_lim, list):
        #    t_lim =[t_lim]
  
            
        s = "Tafel Analysis"
        if(step_nr>-1):
            s = s + f" of step #{step_nr}"

        fig = make_plot_2x_1(s, **kwargs)
        data_plot_i = fig.plots[0]
        data_plot_E = fig.plots[1]
        analyse_plot =  fig.plots[2]
        # data_plot_i,data_plot_E, analyse_plot = make_plot_2x_1(s)
        #data_plot_i.title.set_text("")
        #data_plot_E.title.set_text('')
        analyse_plot.title.set_text('Tafel Plot')

        #########################################################
        # Make plot
        data_kwargs = kwargs
        data_kwargs["plot_i"] = data_plot_i
        data_kwargs["plot_E"] = data_plot_E
        
        self.plot(LEGEND.NONE, x_channel=ENUM_Channel_Names.Time, y_channel=ENUM_Channel_Names.i , *args, plot=data_plot_i,**kwargs)
        self.plot(x_channel=ENUM_Channel_Names.Time,y_channel=ENUM_Channel_Names.E, plot=data_plot_E)

        # Span where data is taken
        data_plot_i.axvspan(t_lims.min, t_lims.max, color='C0', alpha=0.2)
        data_plot_E.axvspan(t_lims.min, t_lims.max, color='C0', alpha=0.2)

        #axvspan_for_steps(data_plot_i, self.datas[0].Time, 0, len(self.datas[0].Time), *args, **kwargs)
        #axvspan_for_steps(data_plot_E, self.datas[0].Time, 0, len(self.datas[0].Time), *args, **kwargs)

        current = self.get_current_at_time(t_lims.t, t_lims.dt, *args, **kwargs)
        voltage = self.get_voltage_at_time(t_lims.t, t_lims.dt, *args, **kwargs)
        x_data_ext=[i.value for i in voltage]
        y_data_ext=[i.value for i in current]

        v_select = []
        i_select = []
        for i in range(len(voltage)):
            # print("voltage", voltage[i].value, "current", current[i].value)
            if voltage[i].value <= E_fit_max and voltage[i].value >= E_fit_min:
                v_select.append(voltage[i])
                i_select.append(current[i])
        return Tafel(v_select, i_select, current[0].unit, current[0].quantity, "b", "",x_data_ext,y_data_ext,"o-", plot=analyse_plot, **kwargs)
    
    
    def Levich(self, *args, **kwargs):
        """_summary_

        Args:
            Time_s_ (float, optional): _description_. Defaults to -1.
            step_nr (int, optional): _description_. Defaults to -1.

        Returns:
            _type_: _description_
        """
        
        t_lims = step_time_range(self.datas,**kwargs)
        step_nr = kwargs.get("step_nr", -1)
        s = "Levich Analysis"
        if(step_nr>-1):
            s = s + f" of step #{step_nr}"
        
        fig = make_plot_2x_1(s, **kwargs)
        data_plot_i = fig.plots[0]
        data_plot_E = fig.plots[1]
        analyse_plot =  fig.plots[2]
        # data_plot_i,data_plot_E, analyse_plot = make_plot_2x_1(s)
        #data_plot_i.title.set_text("")
        #data_plot_E.title.set_text('')
        analyse_plot.title.set_text('Levich Plot')

        #########################################################
        # Make plot
        data_kwargs = kwargs
        data_kwargs["plot_i"] = data_plot_i
        data_kwargs["plot_E"] = data_plot_E
        
        
        # Span where data is taken
        data_plot_i.axvspan(t_lims.min, t_lims.max, color='C0', alpha=0.2)
        data_plot_E.axvspan(t_lims.min, t_lims.max, color='C0', alpha=0.2)
        
        rot, y, E, y_axis_title, y_axis_unit  = plots_for_rotations(self.datas, t_lims.t, step_nr, *args, **data_kwargs)
  
        # Levich analysis
        B_factor = Levich(rot, y, y_axis_unit, y_axis_title, STYLE_POS_DL, "steps", plot=analyse_plot )
        
        print("Levich analysis" )
        #print("dir", "\tpos     ", "\tneg     " )
        print(" :    ",f"\t{y_axis_unit} / rpm^0.5")
        print("slope:", "\t{:.2e}".format(B_factor.value))
        plot_options(**kwargs).close(*args)
        saveFig(fig,**kwargs)
        return B_factor
 

def plots_for_rotations(step_datas: Step_Datas, time_s_: float,step_nr: int =-1, *args, **kwargs):
    rot = []
    y = []
    t = []
    E = []
    
    rot_kwarge = {"dt" :None, "t_end" : None}
    rot_kwarge.update(kwargs)
    
    # Epot=-0.5
    y_axis_title = ""
    y_axis_unit = ""
    datas = copy.deepcopy(step_datas)
    data_kwargs = kwargs
    # x_qv = QV(1, "rpm^0.5","w")
    plot_i = data_kwargs["plot_i"]
    plot_E = data_kwargs["plot_E"]
    line=[]
    t_min = time_s_
    t_max = None
    for data in datas:
        # x_qv = cv.rotation
        rot.append(math.sqrt(data.rotation))
        #for arg in args:
        #    data.norm(arg)
        data_kwargs["legend"] = str(f"{float(data.rotation):.0f}")
        if step_nr>-1:
            data = data[step_nr]
        # l, ax = data.plot(**data_kwargs)
        l_i, ax1 = data.plot(ENUM_Channel_Names.Time, ENUM_Channel_Names.i, plot=plot_i, *args, **data_kwargs)
        ax1.label_outer()
        l_E, ax2 = data.plot(ENUM_Channel_Names.Time, ENUM_Channel_Names.E, plot=plot_E, *args, **data_kwargs)
        ax2.label_outer()
        line.append([l_i,l_E])
        index = data.index_at_time(time_s_)
        index_end = None
        
        data.norm(args)
        data.set_active_RE(args)
        #print("AAAAAAAAAAA", str(data.i_unit))
        if rot_kwarge["t_end"] is not None:
            index_end = data.index_at_time(float(rot_kwarge["t_end"]))
        if rot_kwarge["dt"] is not None:
            index = data.index_at_time(time_s_- float(rot_kwarge["dt"])/2)
            index_end = data.index_at_time(time_s_ + float(rot_kwarge["dt"])/2)
        if index_end is None:
        # print("INDEX",index)
            t.append(data.Time[index])
            E.append(data.E[index])
            y.append(data.get_current_at_time(time_s_))
        else:
            t_min =data.Time[index]
            t_max =data.Time[index_end]
            t.append(np.average(data.Time[index:index_end]))
            E.append(np.average(data.E[index:index_end]))
            y.append(np.average(data.i[index:index_end]))
           
        y_axis_title = str(data.i_label)
        y_axis_unit = str(data.i_unit)
    rot = np.array(rot)
    y = np.array(y)
    if t_max is not None:
         plot_i.axvspan(t_min, t_max, color='C0', alpha=0.2)
    plot_i.plot(t, y, STYLE_POS_DL)
    plot_i.legend()
    plot_E.plot(t, E, STYLE_POS_DL)
    return rot, y, t, y_axis_title, y_axis_unit