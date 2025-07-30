"""
Module for reading binary TDMS files produced by EC4 DAQ\n

ec_data is used to load in the raw files.

"""
from __future__ import annotations
from .ec_data import EC_Data
from .ec_datas import EC_Datas
from .cv_data import CV_Data
from .cv_datas import CV_Datas
#from ec4py.step_data import Step_Data

#from typing import TYPE_CHECKING
#if TYPE_CHECKING:  # Only imports the below statements during type checking

from .step_data import Step_Data
#import ec4py.step_data as step_data
#if TYPE_CHECKING:  # Only imports the below statements during type checking
from .step_datas import Step_Datas
from .eis_data import EIS_Data
from .eis_datas import EIS_Datas
from .util import Quantity_Value_Unit
from .lsv_data import LSV_Data
from .lsv_datas import LSV_Datas
from .ec_setup import RHE,SHE,RATE,SQRT_RATE, AREA,AREA_CM,ROT,SQRT_ROT, MASS, LOADING
from .util_graph import NO_PLOT,LEGEND
from .method_util.util_voltammetry import POS,NEG,AVG,DIF


__all__ = ["EC_Data", "EC_Datas", 
           "CV_Data", "POS", "NEG", "AVG","DIF",
           "CV_Datas", 
           "EIS_Data",
           "EIS_Datas",
           "Step_Data", "Step_Datas", 
           "Quantity_Value_Unit",
           "LSV_Data","LSV_Datas",
           "RHE","SHE",
           "RATE","SQRT_RATE", "AREA","AREA_CM","ROT","SQRT_ROT", "MASS", "LOADING",
           "NO_PLOT","LEGEND"]
