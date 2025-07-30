

from ec4py.analysis.analysis_ran_sev import ran_sev
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import numpy as np

import unittest   # The test framework


rot =np.array([300,400,500])

def  rn(value):
    return round(value*1000000)/1000000

class Test_Analysis_RanSevich(unittest.TestCase):
    
    def test_linear_slope(self):
        
        y_data = 1*np.sqrt(rot)
        unit = "AAA"
        result = ran_sev(rot, y_data, unit, "", "bo")
        self.assertEqual(rn(result.value), 1.0)
        y_data = 2*y_data
        result = ran_sev(rot, y_data, unit, "", "bo")
        self.assertEqual(rn(result.value), 2.0)
        # self.assertEqual(result.unit, "m")

        
    def test_units_slope(self):
        
        y_data = 1*rot
        unit = "AAA"
        result = ran_sev(rot, y_data, "", "", "bo")
        self.assertEqual(result.unit, "V^-0.5 s^0.5")
        result = ran_sev(rot, y_data, unit, "", "bo")
        self.assertEqual(result.unit, unit+" V^-0.5 s^0.5")
        # self.assertEqual(result.unit, "m")
    
    def test_quantity_slope(self):
       
        y_data = 1*rot
        result = ran_sev(rot, y_data, "", "", "bo")
        self.assertEqual(result.quantity, "v^-0.5")
        q = "AAA"
        result = ran_sev(rot, y_data, "", q, "bo")
        self.assertEqual(result.quantity, q+" v^-0.5")
        
    def real_data(self):
        pass
        
    
  

if __name__ == '__main__':
    unittest.main()
