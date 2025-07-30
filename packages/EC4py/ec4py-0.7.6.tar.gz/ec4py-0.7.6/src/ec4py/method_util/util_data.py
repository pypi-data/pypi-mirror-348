import numpy as np
import warnings

from ..ec_util.ec_data_util import EC_Channels
from ..ec_data   import EC_Data

KW_IRCORR = "IRCORR"
ARG_IRCORR_Z = "Z"
ARG_IRCORR_R = "R"
ARG_IRCORR_RMED = "Rmed"
ARG_IRCORR_ZMED = "Zmed"

#IR_comp_Z = "Z"
#IR_comp_R = "R" 
#IR_comp_Rmed = "Rmed"
#IR_comp_Zmed = "Zmed"

#IR_COMP_KWs = {ARG_IRCORR_Z,IR_comp_R,IR_comp_Rmed,IR_comp_Rmed}
ARGS_IRCORR = {ARG_IRCORR_Z,ARG_IRCORR_R,ARG_IRCORR_RMED,ARG_IRCORR_ZMED}




def get_Impedance(ec_data:EC_Data,sel_channels:EC_Channels):
    data_E,q,u,dt_x = ec_data.get_channel(sel_channels.Voltage)
    data_Z,q,u,dt_Z = ec_data.get_channel(sel_channels.Impedance)
    data_phase,q,u,dt_p = ec_data.get_channel(sel_channels.Phase)
    # print("get_Impedance",dt_x,dt_Z,dt_p)
    if(len(data_E)!=len(data_Z)):
        data_t,q,u,dt_t = ec_data.get_channel(sel_channels.Time)
        data_t_z =dt_Z*np.array(range(len(data_Z)))
        data_Z = np.interp(data_t, data_t_z, data_Z)
        data_phase = np.interp(data_t, data_t_z, data_phase)

    return data_Z, data_phase


def calc_ir_manual(ec_data:EC_Data,sel_channels:EC_Channels,comp,**kwargs):
    ir_comp = False
    data_IR = None
    data_i,_,_,_ = ec_data.get_channel(sel_channels.Current)

    try:
        Rsol = float(comp)
        if Rsol > 0:
            ir_comp =True
            r_comp = Rsol
            data_IR = data_i*r_comp
        else:
            raise ValueError("Invalid value for IRCORR. IRCORR must be a positive number.")
    except ValueError as e:
        print(e)
        raise ValueError("Invalid value for IRCORR")
    return ir_comp, data_IR

def calc_ir(ec_data:EC_Data,sel_channels:EC_Channels,s_comp,**kwargs):
    ir_comp = False
    data_IR = None
    data_i,_,_,_ = ec_data.get_channel(sel_channels.Current)
    s_comp=str(s_comp).casefold()
    data_Z,data_phase = get_Impedance(ec_data,sel_channels)
    if  s_comp == ARG_IRCORR_Z.casefold():
        data_IR = data_i*data_Z
        ir_comp =True
        r_comp=[np.min(data_Z),np.max(data_Z)]
    elif  s_comp == ARG_IRCORR_R.casefold():
        R = data_Z*np.cos(data_phase)
        data_IR = data_i*R
        ir_comp =True
        r_comp=[np.min(R),np.max(R)]
        for r in R: 
            if r <0:
                ir_comp = False
                warnings.warn("Negative Resistance Detected. Consider using Z instead of R")
                break
    elif s_comp == ARG_IRCORR_RMED.casefold():
        r_comp = np.median(data_Z*np.cos(data_phase))
        data_IR = data_i*r_comp
        ir_comp =True
    elif s_comp == ARG_IRCORR_ZMED.casefold():
        r_comp = np.median(data_Z)
        data_IR = data_i*r_comp
        ir_comp =True
    return ir_comp, data_IR

def get_IR(ec_data:EC_Data,sel_channels:EC_Channels,comp:float|str, **kwargs):
    data_IR = None
    ir_corr = False
    #comp = kwargs.get("IRCORR",None)
    s_comp=str(comp).casefold()
    for v in ARGS_IRCORR:
        ir_corr = ir_corr or s_comp == v.casefold() 
    if ir_corr:
        ir_corr, data_IR = calc_ir(ec_data,sel_channels,s_comp,**kwargs)
    else:
        ir_corr, data_IR = calc_ir_manual(ec_data,sel_channels,comp)
    return ir_corr, data_IR
        
    """     
        try:
            data_i,_,_,_ = ec_data.get_channel(sel_channels.Current)
            
            if comp is not None:
                s_comp=str(comp).casefold()
                #vertex =find_vertex(data_E)
                data_Z,data_phase = get_Impedance(ec_data,sel_channels)
                if  s_comp == "Z".casefold():
                    data_IR = data_i*data_Z
                    ir_comp =True
                    r_comp=[np.min(data_Z),np.max(data_Z)]
                elif  s_comp == "R".casefold():
                    R = data_Z*np.cos(data_phase)
                    data_IR = data_i*R
                    ir_comp =True
                    r_comp=[np.min(R),np.max(R)]
                elif s_comp == "Rmed".casefold():
                    r_comp = np.median(data_Z*np.cos(data_phase))
                    data_IR = data_i*r_comp
                    ir_comp =True
                elif s_comp == "Zmed".casefold():
                    r_comp = np.median(data_Z)
                    data_IR = data_i*r_comp
                    ir_comp =True
                else:
                    try:
                        Rsol = float(comp)
                        if Rsol > 0:
                            ir_comp =True
                            r_comp = Rsol
                            data_IR = data_i*r_comp
                    except ValueError as e:
                        print(e)
                        raise ValueError("Invalid value for IRCORR")
                        return
                """
   



def get_data_for_convert(ec_data:EC_Data,sel_channels:EC_Channels,*args, **kwargs):
    
    ir_comp = False
    try:
        data_E,q,u,dt_x = ec_data.get_channel(sel_channels.Voltage)
        data_i,q,u,dt_y = ec_data.get_channel(sel_channels.Current)
    except NameError as e:
        print(e)
        raise NameError(e)
        return
    
    try:
        comp = kwargs.get(KW_IRCORR,None)
        if comp is not None:
            ir_comp, IR_data = get_IR(ec_data,sel_channels,comp)    
        
    except NameError as e:
        print(e)
        raise NameError(e)
        return
    
    return data_E,data_i, IR_data, ir_comp 
 
