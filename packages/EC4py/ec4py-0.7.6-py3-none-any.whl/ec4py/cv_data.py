""" Python module for reading TDMS files produced by LabView and specifically form EC4 DAQ.

    This module contains the public facing API for reading TDMS files produced by EC4 DAQ.
"""
from __future__ import annotations
import math
import numpy as np
# from scipy import integrate
from scipy.signal import savgol_filter 

import copy

from .ec_data import EC_Data
from .ec_util import EC_Channels

from .lsv_data import LSV_Data

from .util import extract_value_unit     
from .util import Quantity_Value_Unit as QV
from .method_util.util_voltammetry import Voltammetry,create_Tafel_data_analysis_plot,POS,NEG,AVG,DIF,find_vertex
#from .method_util.util_voltammetry import OFFSET_AT_E_MIN, OFFSET_AT_E_MAX, OFFSET_LINE

from .method_util.util_data import get_IR
from .util_graph import plot_options, saveFig, should_plot_be_made,ANALYSE_PLOT,DATA_PLOT
#from .analysis import diffusion_limit_corr

STYLE_POS_DL = "bo"
STYLE_NEG_DL = "ro"


class CV_Data(Voltammetry):
    """# Class to analyze a single CV data. 
    Class Functions:
    - .plot() - plot data    
    - .bg_corr() to back ground correct.
    
    ### iR- Correction
    - add keyword IRCORR = "R" for using the real-part of the impedance
    - add keyword IRCORR = "Rmed" for using the median real-part of the impedance
    - add keyword IRCORR = "Z" for using the absolute impedance
    - add keyword IRCORR = "Zmed" for using the median absolute impedance
    - add keyword IRCORR = 1.0 for manual ir compensation
    
    ### Analysis: 
    - .Tafel() - Tafel analysis data    
    
    ### Options args:
    "in" where n is a number to select another current channel, ex. "i2"
    "pn" where n is a number to select another potentiostat group, ex. "P2"
    "area" - to normalize to area
    
    ### Options keywords:
    legend = "name"
    """


    def __init__(self,*args, **kwargs):
        #EC_Setup.__init__(self,*args, **kwargs)
        Voltammetry.__init__(self, *args, **kwargs)
        # self.E=[]
        self.i_p=[]
        self.i_n=[]
 
        if not args:
            return
        else:
            #print(kwargs)
            self.conv(EC_Data(args[0]), *args, **kwargs)

    #########################################  
    
    def __repr__(self):
        """Get the name of the data file.
        """
        return f"CV_Data('{self.setup_data.fileName}')"
    
       
    def __add__(self, other: CV_Data):
        """_summary_

        Args:
            other (CV_Data): CV_Data to be added 

        Returns:
            CV_Data: returns a copy of the inital dataset. 
        """
        new_cv = self.copy() # copy.deepcopy(self)
        new_cv.add(other)
        return new_cv   
    
    def __sub__(self, other: float) -> CV_Data:
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            CV_Data: a copy of the original data
        """
        new_cv = self.copy() # copy.deepcopy(self)
        new_cv.sub(other)
        return new_cv
    
    def __mul__(self, other: float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            CV_Data: a copy of the original data
        """
        new_cv = self.copy() #copy.deepcopy(self)
        new_cv.mul(other)
        return new_cv
    #############################################################################
    def __truediv__(self, other: float):
        """ 

        Args:
            other (float): factor to div. the data.

        Returns:
            CV_Data: a copy of the original data
        """
        new_cv = self.copy() # copy.deepcopy(self)
        new_cv.div(other)
        return new_cv
    #############################################################################   
    #####################################################################################################
    def add(self, other: CV_Data):
        """_summary_

        Args:
            other (CV_Data): Add something to the current of the CV_Data.

        Raises:
            ValueError: _description_
            TypeError: _description_
        """
        if isinstance(other, CV_Data):
            self.i_p = self.i_p + other.i_p
            self.i_n = self.i_n + other.i_n
        elif isinstance(other, LSV_Data):
            self.i_p = self.i_p + other.i
            self.i_n = self.i_n + other.i
        elif isinstance(other, QV):
            self.i_p = self.i_p + other.value
            self.i_n = self.i_n + other.value
        elif isinstance(other, str):
            self.i_p = self.i_p + float(other)
            self.i_n = self.i_n + float(other)
        elif isinstance(other, list):
            if len(other) == 2:
                self.i_p = self.i_p + float(other[0])
                self.i_n = self.i_n + float(other[1])
            else:
                raise ValueError("List must have length 2")
        elif isinstance(other, float) or isinstance(other, int):
            self.i_p = self.i_p + other
            self.i_n = self.i_n + other
        else:
            raise TypeError("Unsupported type for subtraction")
        

    #####################################################################################################   
    
    
    def sub(self, other: CV_Data) -> None:
        if isinstance(other, CV_Data):
            self.i_p = self.i_p - other.i_p
            self.i_n = self.i_n - other.i_n
        elif isinstance(other, LSV_Data):
            self.i_p = self.i_p - other.i
            self.i_n = self.i_n - other.i
        elif isinstance(other, QV):
            self.i_p = self.i_p - other.value
            self.i_n = self.i_n - other.value
        elif isinstance(other, str):
            self.i_p = self.i_p - float(other)
            self.i_n = self.i_n - float(other)
        elif isinstance(other, list):
            if len(other) == 2:
                self.i_p = self.i_p - float(other[0])
                self.i_n = self.i_n - float(other[1])
            else:
                raise ValueError("List must have length 2")
        elif isinstance(other, float) or isinstance(other, int):
            print("AAA",other)
            self.i_p = self.i_p - other
            self.i_n = self.i_n - other
        else:
            raise TypeError("Unsupported type for subtraction")
        
    #############################################################################
    
    def mul(self, mul_factor:float):
        """divide the current by a factor.
        Args:
            div_factor (float): div the current dataset with the factor.
        """
    
        self.i_p = self.i_p * float(mul_factor)
        self.i_n = self.i_n * float(mul_factor)
    
    def div(self, div_factor:float):
        """divide the current by a factor.
        Args:
            div_factor (float): div the current dataset with the factor.
        """
        self.i_p = self.i_p / float(div_factor)
        self.i_n = self.i_n / float(div_factor)
     
    #############################################################################
    
    def set_i_at_E_to_zero(self, E:float, *args, **kwargs):
        """Set the current at a specific voltage to zero and adjust the rest of the current.

        Args:
            E (float): potential where to set the current to zero.
        """
        new_data = copy.deepcopy(self)
        new_data.set_active_RE(args)
        current = new_data.get_i_at_E(E,*args,**kwargs)
        self.sub(current)
    
     
    def smooth(self, smooth_width:int):
        try:
            self.i_p = self._smooth(self.i_p,smooth_width)
            self.i_n = self._smooth(self.i_n,smooth_width)      
        finally:
            return


    ######################################################################################################
    def conv(self, ec_data: EC_Data, *args, ** kwargs):
        """Converts EC_Data to a CV

        Args:
            ec_data (EC_Data): the data that should be converted.
        """
        #print("Convert:",kwargs)
        
        #ch_E ="E"
        #for a in args:
        #    if a == "IR":
        #        ch_E = "E-IR"
        options = {
            'x_smooth' : 0,
            'y_smooth' : 0,
            'IRCORR': None,
            'E' : "E",
            'i' : 'i'
        }
        options.update(kwargs)
        sel_channels = EC_Channels(*args,**kwargs)
        ir_comp =False
        r_comp=None
        vertex =[]
        try:
            data_E,q,u,dt_x = ec_data.get_channel(sel_channels.Voltage)
            data_i,q,u,dt_y = ec_data.get_channel(sel_channels.Current)
        except NameError as e:
            print(e)
            raise NameError(e)
            return
        
        try:
            comp = options.get("IRCORR",None)
            if comp is not None:
                
                ir_comp, data_IR = get_IR(ec_data,sel_channels,comp)
                vertex = find_vertex(data_E)
                r_comp = data_IR/data_i
                if ir_comp:
                    data_E = data_E - data_IR
                
        except NameError as e:
            print(e)
            raise NameError(e)
            return

        
        self.setup_data = copy.deepcopy(ec_data.setup_data)
        self.convert(ec_data.Time,data_E,data_i,vertex = vertex, **kwargs)
        self.IR_COMPENSATED = ir_comp
        self.R_COMP = r_comp
        E_title = "E"
        #if ir_comp: ###NOT NEEDED
        #    E_title ="E-iR"
        self.setup_data.select_MWE_CH(sel_channels.MWE_CH)   
        
        try:
            self.IR_COMPENSATED = ir_comp
            E_title = "E"
            #if ir_comp: ###NOT NEEDED
            #    E_title ="E-iR"
            if 'Ref.Electrode' in self.setup:
                self.E_label = f"{E_title} vs " + self.RE
                #print("aaaaa")
            else:
                self.E_label =f"{E_title}"
            if self.is_MWE:
                self.setup_data.select_MWE_CH(sel_channels.MWE_CH)
            

        except ValueError as e:
            if(self.is_MWE):
                print(e)
                print("select a current channel, such as i_0")
            else:
                print("no_data")
        
        #self.setup = data.setup
        #self.set_area(data._area, data._area_unit)
        #self.set_rotation(data.rotation, data.rotation_unit)
        #self.name = data.name
        return

    #####################################################################################################    
    def convert(self, time, Potential_V, Current_A, **kwargs):
        """Converts data to CV data

        Args:
            time (_type_): time
            E (_type_): potential
            i (_type_): current
            direction(str): direction
        """
        x= Potential_V
        y= Current_A

        #vertex =kwargs.get("vertex",None)
        #if vertex is None:
        #    vertex = find_vertex(x)
        #print("Convert", len(E))
        #print("SETP",self.setup)
        #Start_Delay, = extract_value_unit(self.setup_data._setup['Start_Delay'])
        #print("Start", self.setup['Start'])
        #print("V1", self.setup['V1'])
        V0, V0_str = extract_value_unit(self.setup['Start'])
        #print("V1", self.setup['V1'])
        V1, V1_str = extract_value_unit(self.setup['V1'])
        #print("V2", self.setup['V2'])
        V2, V2_str = extract_value_unit(self.setup['V2'])
        # print("CV", V0,V1,V2)
        options = plot_options(**kwargs)
        #print("CONVERTING",len(time), len(E), len(i))
        #try:
        #    y_smooth = int(options['y_smooth'])
        #    if(y_smooth > 0):
        #        y = savgol_filter(y, y_smooth, 1)
        #finally:
        #    pass
        positive_start = False
        if V0 == V1:
            positive_start = (V1 < V2)
        else:
            positive_start = V0 < V1
        #print("startDIR:", positive_start)

        y = options.smooth_y(y)

        self.xmin = x.min()
        self.xmax = x.max()

        #x_start = np.mean(x[0:3])
        #index_min = np.argmin(x)
        #index_max = np.argmax(x)

        #array of dx

        x_div = np.gradient(savgol_filter(x, 10, 1))
        #dt:
        t_div = (time.max() - time.min()) / (time.size - 1)
        zero_crossings = np.where(np.diff(np.signbit(x_div)))[0]
        #print("ZERO:",zero_crossings)
        self.rate_V_s = np.mean(np.abs(x_div)) / t_div
        #print(f"Rate: {self.rate_V_s}")
        #up_start =0
        #up_end = 0
        ## Number of vertext
        Two_vertex = len(zero_crossings)>1
        #print("MIN",x[zero_crossings[0]], np.min(x[0:zero_crossings[1]]))
        #print("argMIN",zero_crossings[0], np.argmin(x[0:zero_crossings[1]]))
        if not Two_vertex:  #if the CV consists of 2 LSV, there is only one zero crossing.
            zero_crossings = np.append(zero_crossings,len(x))
      
        if positive_start:
            zero_crossings[0] = np.argmax(x[0:zero_crossings[1]])
        else:
            zero_crossings[0] = np.argmin(x[0:zero_crossings[1]])
      
        self.E = self.make_E_axis()
        zero_crossings = np.append(zero_crossings, x.size)
        #print("ZERO:",len(zero_crossings),zero_crossings, "2x vertex", Two_vertex)

        if positive_start:
            x_u = x[0:zero_crossings[0]]
            y_u = y[0:zero_crossings[0]]
            x_n = np.flipud(x[zero_crossings[0]:zero_crossings[1]])
            y_n = np.flipud(y[zero_crossings[0]:zero_crossings[1]])
            if Two_vertex:
                x_u2 = x[zero_crossings[1]:zero_crossings[2]]
                y_u2 = y[zero_crossings[1]:zero_crossings[2]] 
                # print(zero_crossings)
                mask = x_u2<x_u.min()
                
                x_u2=np.array(x_u2[mask])
                if len(y_u2)>=len(mask):
                    y_u2=np.array(y_u2[mask])
                        
        else:
            #print("neg first sweep")
            x_n = np.flipud(x[0:zero_crossings[0]])
            y_n = np.flipud(y[0:zero_crossings[0]])
            x_u = x[zero_crossings[0]-1:zero_crossings[1]]
            y_u = y[zero_crossings[0]-1:zero_crossings[1]]
            if Two_vertex:
                x_n2 = np.flipud(x[zero_crossings[1]:zero_crossings[2]])
                y_n2 = np.flipud(y[zero_crossings[1]:zero_crossings[2]])
                mask = x_n2>x_n.max()
                x_n2=np.array(x_n2[mask])
                y_n2=np.array(y_n2[mask])

        #y_pos=np.interp(x_sweep, x_u, y_u)
        #y_neg=np.interp(x_sweep, x_n, y_n)
        y_pos=   self.interpolate(x_u, y_u)
        y_pos =  self.clean_up_edges(y_pos,0)
        
        if Two_vertex and positive_start:
            y_pos2 = self.interpolate(x_u2, y_u2)
            y_pos2 =  self.clean_up_edges(y_pos2,0)
            y_pos = y_pos + y_pos2
       
        y_neg=self.interpolate(x_n, y_n)
        y_neg = self.clean_up_edges(y_neg,0)

        if Two_vertex and not positive_start:
          #  print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
          #  print("x_n2",len(x_n2))
          #  print("y_n2",len(y_n2))
            y_neg2 = self.interpolate(x_n2, y_n2)
            y_neg2 = self.clean_up_edges(y_neg2,0)
            y_neg=y_neg+y_neg2
            #print("YNEG",y_neg[0])
            
        #print("YPOS",y_pos)        
        #print("YNEG",y_neg.size)
        #"""
        if positive_start or (not positive_start and Two_vertex):
            indexes = y_pos.nonzero()[0]
            if len(indexes)>0:
                max_arg= indexes.max()
                y_neg[max_arg]=y_pos[max_arg]    
                
        if not positive_start or (positive_start and Two_vertex):
            #c = a.nonzero()[0]
            mask =y_neg.nonzero()[0]
            min_arg= mask.min()
            #np.flatnonzero(y_neg).min()
            #print("BBB", min_arg,y_neg[min_arg],y_neg[min_arg+1],y_pos.nonzero()[0].min())
            y_pos[min_arg]=y_neg[min_arg]
        #"""    
        self.i_p = self.clean_up_edges(y_pos)
        self.i_n = self.clean_up_edges(y_neg)
        
   ######################################################################################### 
    def norm(self, norm_to:str|tuple):
        """Normalise the current to certain factors. 

        Args:
            norm_to (str | tuple): _description_
        """
        r = Voltammetry.norm(self, norm_to,[self.i_p,self.i_n ] )
        #n = Voltammetry.norm(self, norm_to,self.i_n )
        if r is not None:
            v= r[0]
            self.i_p = v[0]
            self.i_n = v[1]
            
        return 
    ###############################
    ###under deve
    def set_active_RE(self,shift_to:str|tuple = None):
        # end_norm_factor = None
        # print("argeLIST", type(norm_to))
        
        a = Voltammetry.set_active_RE(self,shift_to, [self.i_p, self.i_n])
        if a is not None:
            a,b = a
            self.i_p = b[0]
            self.i_n = b[1]
            # print("pot_shift",a, "REEE",self.E_label)
        return 
    
    ############################################################################        
    def plot(self,*args,**kwargs):
        '''
        plots y_channel vs x_channel.\n
        to add to a existing plot, add the argument: \n
        "plot=subplot"\n
        "x_smooth= number" - smoothing of the x-axis. \n
        "y_smooth= number" - smoothing of the y-axis. \n
        
        
        Returns:
            line, ax: description
        '''
        if should_plot_be_made(*args,**kwargs):
            dir = Voltammetry()._direction(*args,**kwargs)
            if dir == POS or dir == NEG or dir == AVG or dir == DIF:
                lsv = self.get_sweep(dir)
                return lsv.plot(*args,**kwargs)
            
            data = copy.deepcopy(self)
            options = plot_options(**kwargs)
            options.options["dir"]=dir
            #print("AAAAAAAAAAAAAAAAAAAAAAA")
            #print(options.get_y_smooth())
            # print(options.get_legend(),self.legend(**kwargs))
            #print(options.get_title())
            if self.is_MWE:
                options.set_title(f"{self.setup_data.name}#{self.setup_data._MWE_CH}")
            else:
                options.set_title(self.setup_data.name)
                
            options.name = data.setup_data.name
            options.legend = data.legend(*args, **kwargs)
            # print("AAAA",data.legend(*args, **kwargs))
            
            data.norm(args)
            # print(args)
            data.set_active_RE(args)
            options.x_data = data.E
            if(options.get_dir() == POS.casefold()):  
                options.y_data = data.i_p
            
            elif(options.get_dir() == NEG.casefold()):  
                options.y_data = data.i_n
                
            else:
                options.x_data=np.concatenate((data.E, data.E), axis=None)
                options.y_data=np.concatenate((data.i_p, data.i_n), axis=None)  
            
            # options.set_x_txt("E vs "+ data.setup_data.getACTIVE_RE(), data.E_unit)
            options.set_x_txt(data.E_label, data.E_unit)
            options.set_y_txt(data.i_label, data.i_unit) 
            
           
            return options.exe()
        else:
            return None,None
    
    ####################################################################################################
    """def get_index_of_E(self, E:float):
        index = 0
        for x in self.E:
            if x > E:
                break
            else:
                index = index + 1
        return index
    """
    ########################################################################################################
    def get_i_at_E(self, E:float, direction:str = "all",*args, **kwargs):
        """Get the current at a specific voltage.

        Args:
            E (float): potential where to get the current. 
            dir (str): direction, "pos,neg or all"
        Returns:
            Quantity_Value_Unit: current of selected sweep
            or 
            List[Quantity_Value_Unit,Quantity_Value_Unit] of positive and negative sweep. 
        """
        #if args is not None:
        list_args=[arg for arg in args]
        list_args.insert(0,direction)
        loc_args=tuple(list_args)
        
        dir = self._direction(*loc_args,**kwargs)
       
        update_label = kwargs.get("update_label",True)
        print(dir)
        if dir == "" or dir == "all".casefold():
            lsv_pos = self.get_sweep(POS,update_label)
            lsv_neg = self.get_sweep(NEG,update_label)
            return [lsv_pos.get_i_at_E(E,*args,**kwargs) , lsv_neg.get_i_at_E(E,*args,**kwargs)]
        else:
            lsv = self.get_sweep(dir)
            return lsv.get_i_at_E(E,*args,**kwargs)
 
    
    ###########################################################################################

    def get_E_at_i(self, i:float,tolerance:float=0,  dir:str = "all", *args, **kwargs):
        """Get the voltage at a specific current..

        Args:
            i (float): the current. 
            dir (str): direction, "pos,neg or all"
            
            "tolerance": value
            
        Returns:
            float: Voltage at a specific current.
        """
        options = {"plot": None
                   }
        options.update(kwargs)
                       
        if dir.casefold() == POS.casefold():
            
            return self._get_E_at_i(self.i_p, i, **kwargs)
        elif dir.casefold() == NEG.casefold():
            
            return self._get_E_at_i(self.i_n, i, **kwargs)
        else:
            
            return [self._get_E_at_i(self.i_p, i, **kwargs) , self._get_E_at_i(self.i_n, i, **kwargs)]
    
    ###########################################################################################

    def get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of maximum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
            _type_: _description_
        """
        dir = self._direction(*args, **kwargs)
        
        if dir == "" or dir == "ALL".casefold():
            lsv_p = self.get_sweep(POS)
            lsv_n = self.get_sweep(NEG)
            return lsv_p.get_E_of_max_i(E1,E2),lsv_n.get_E_of_max_i(E1,E2)
        else:
            lsv = self.get_sweep(dir)
            return lsv.get_E_of_max_i(E1,E2)
        
    def get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of maximum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
            _type_: _description_
        """
        dir = self._direction(*args, **kwargs)
        
        if dir == "" or dir == "ALL".casefold():
            lsv_p = self.get_sweep(POS)
            lsv_n = self.get_sweep(NEG)
            return lsv_p.get_E_of_min_i(E1,E2),lsv_n.get_E_of_min_i(E1,E2)
        else:
            lsv = self.get_sweep(dir)
            return lsv.get_E_of_min_i(E1,E2)           


    def get_sweep(self,sweep:str, update_label = True):
        """Creates a single voltammogram from a CV.

        Args:
            sweep (str): the direction,use POS,NEG,AVG or DIF"

        Returns:
            LSV_Data: The sweep as LSV_data
        """
        lsv = LSV_Data()
        # lsv.setup_data =  copy.deepcopy(self.setup_data)
        lsv.copy_from(self)
        
        if str(sweep).casefold() == POS.casefold():
            lsv.i = copy.deepcopy(self.i_p)
            lsv.i_label = self.i_label+"$_{+}$"
            lsv.dir = POS
        elif str(sweep).casefold() == NEG.casefold():
            lsv.i = copy.deepcopy(self.i_n)
            lsv.i_label = self.i_label+"$_{-}$"
            lsv.dir = NEG
        elif str(sweep).casefold() == AVG.casefold():
            lsv.i = copy.deepcopy((self.i_n+self.i_p)/2)
            lsv.i_label = "( " + self.i_label+"$_{+} $+ " + self.i_label+"$_{-}$)/2"
            lsv.dir = AVG
        elif str(sweep).casefold() == DIF.casefold():
            lsv.i = (self.i_p-self.i_n)
            lsv.i_label = "( " + self.i_label+"$_{+}$ - " + self.i_label+"$_{-}$ )"
            lsv.dir = DIF
        else:
            print("use pos,neg,avg or dif")
        if not update_label:
            lsv.i_label =self.i_label
        return lsv
        
        

    ###########################################################################################

    def integrate(self, start_E:float, end_E:float, *args, **kwargs):
        """Integrate Current between the voltage limit using cumulative_simpson

        Args:
            start_E (float): potential where to get the current.
            end_E(float) 
            optional args:
                "all", "pos", "neg" - for the direction
                "line": to make a line between i(end_E) and i(start_E), and the integrate between the i(E) and the line.
                "offset_at_emax": Subtracting the value i(E_min) from the i(E) and then integrate.
                "offset_at_emin": Subtracting the value i(E_max) from the i(E) and then integrate.
        Returns:
            [float]: charge
        """
        dir = "all"
        show_plot = True
        for arg in args:
            if "show_plot".casefold() == str(arg).casefold():
                show_plot = True
            if "no_plot".casefold() == str(arg).casefold():
                show_plot = False
            
            if POS.casefold() == str(arg).casefold():
                kwargs["dir"] =POS
            if NEG.casefold() == str(arg).casefold():
                kwargs["dir"] =NEG
                           
        data = copy.deepcopy(self)
  
        
        if kwargs.get("plot",None) is None:
            #line, ax = options.exe()
            
            line, ax = data.plot(*args, **kwargs)
            kwargs["plot"]=ax
            
        data.norm(args)
        data.set_active_RE(args)
        dir = kwargs.get("dir", "all")
        if dir != NEG:   
            Q_p, d_p  =  data._integrate(  start_E, end_E, data.i_p, *args, **kwargs)
        if dir != POS:
            Q_n, d_n  =  data._integrate(  start_E, end_E, data.i_n, *args, **kwargs)

        
        #Q_unit =self.i_unit.replace("A","C")
        #yn= np.concatenate(i_p,i_n,axis=0)      
        
        if dir == POS:
            return Q_p#[Q_p[end]-Q_p[0],Q_unit] 
        elif dir == NEG:
            return  Q_n #[Q_n[end]-Q_n[0],Q_unit]
        else:
            return [Q_p, Q_n] #[Q_p[end]-Q_p[0] ,Q_unit, Q_n[end]-Q_n[0],Q_unit]
        
        
   ##################################################################################################################
    def Tafel(self, lims=[-1,1], E_for_idl:float=None , *args, **kwargs):
        """_summary_

        Args:
            lims (list):  The range where the tafel slope should be calculated 
            E_for_idl (float,optional.): potential that used to determin the diffusion limited current. This is optional.
            
        """
        
        data_plot,analyse_plot,fig = create_Tafel_data_analysis_plot("CV", **kwargs)   
        Tafel_kwargs = kwargs.copy()
        Tafel_kwargs[DATA_PLOT]=data_plot
        Tafel_kwargs[ANALYSE_PLOT]=analyse_plot
        dir = self._direction(*args,**kwargs)

        # rot=[]
        # y = []
        # E = []
        #Epot=-0.5
        # y_axis_title =""
        
        Tafel_pos = None
        Tafel_neg = None
        
        if(dir ==""):
            lsv_pos =self.get_sweep(POS,False)
            Tafel_pos = lsv_pos.Tafel(lims,E_for_idl,*args, **Tafel_kwargs)
            lsv_neg =self.get_sweep(NEG,False)
            Tafel_neg = lsv_neg.Tafel(lims,E_for_idl,*args, **Tafel_kwargs)
        elif(dir == POS):
            lsv_pos =self.get_sweep(POS,True)
            Tafel_pos = lsv_pos.Tafel(lims,E_for_idl,*args, **Tafel_kwargs)
        elif(dir == NEG):
            lsv_neg =self.get_sweep(NEG,True)
            Tafel_neg = lsv_neg.Tafel(lims,E_for_idl,*args, **Tafel_kwargs)
        
     
        saveFig(fig,**kwargs)

        return Tafel_pos, Tafel_neg
    
