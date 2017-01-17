#key1 = 'AIzaSyD3PdBLQxWMDsaJ1tdHOs02QNBuIEqLSiQ'
#key2 = 'AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY'
#key3 = 'AIzaSyBaaQQyMnT7MUI421WdO67g66igzXL2O4A'
#Flavia2 = 'AIzaSyDbPG5qS-g0pROiPRcOT2G-keWi54ie2-M'
#Andrian = 'AIzaSyCjy-sVWBCyN9FOjBeNg2_OeULs-uXSmMI'
#AleCioc = 'AIzaSyAUrnCmaEs7e7izfCiKYm-k7Ap0EwZzYes'
#Flavia3 = 'AIzaSyCeT4Z_Cfabvpnh2FBbf3TCrhBNtwlfVwU'
#Flavia4 = 'AIzaSyAcPVep5aXJLbuBDV7Qn_JaWSpD4o6s30w'
#Andrian2 = 'AIzaSyBHz8SA5BKIJDOu9mtLJb5JilGvcLnGIiM'
#Flavia5 = 'AIzaSyBqMJcxNQUmciUN8qsI-4JVO9Hh_EJqNfE'
#valeprof = 'AIzaSyB9XupnKFaH-zuVg_lBlz7NO8q6QpWFKZk'
#clara = 'AIzaSyAVpeQaUjVPZznjp1b1sbtUl2iBzHSuGek'
#Michele1 = 'AIzaSyCoFpO5q5MatCal_1lLaxVCr6LcXePo91M'
#Michele2 = 'AIzaSyCGfLn4VqFrbV1PFc6duXi7ojPktJb-ta4'
#Michele3 = 'AIzaSyA6zgFdORCnKRnpp74Ew925aCwbSmzsM9U'
#daviderip = 'AIzaSyBSjjou5aXnl-9L3SIaJR05Vc3Zb8j0WpY'
#alessiaCol = 'AIzaSyAKaQDrgawidGlRNkjqTIMngFZs7pOV8Zc'
#gianni = 'AIzaSyCnksllWfpV0D3iDBomyKRFUkqEvEoNtKg'
#
#key_list= [key1, key2, key3, Flavia2, Andrian, AleCioc, Flavia3, Flavia4, Andrian2, Flavia5, valeprof, clara]
#
#file = open("chiavi.txt", "r")

import pandas as pd

with open("chiavi.txt") as f: 
    content = pd.Series(f.readlines())
    
    