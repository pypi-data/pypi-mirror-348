import numpy as np

class xes_data():
    def __init__(self,fileName,skipLn, data_KE=False):
        self.fileName = fileName
        self.skipLn = skipLn #int represnting files to skip
        self.read_file_txt(fileName)
        
    #not yet complete i was just throwing down some starter code
    def read_file_txt(self,fileName):
        self.x,self.y = np.loadtxt(self.fileName,skiprows=self.skipLn,unpack=True)
        self.numP = len(self.x)

    
    def get_x(self,data_KE, data_XES):
        if data_KE == True:
            self.x = self.x[::-1]
        else:
            pass

        return self.x

    
    def get_y(self,scale_var):
        
        y_val = []
        #first = self.y[0]
        y_max = 0
        scale_val = 0

       
        first = 1

     
        y_max = self.y.max()
      
        #Scaling is done proportional to the maximum peak height. This also sets background to 0
        if y_max <= 0.001:
            scale_val = first*100000000
        elif y_max <= 0.01:
            scale_val = first*10000000
        elif y_max <= 0.1:
            scale_val = first*1000000
        elif y_max <= 1:
            scale_val = first*100000
        elif y_max <= 10:
            scale_val = first*10000
        elif y_max <= 100:
            scale_val = first*1000
        elif y_max <= 1000:
            scale_val = first*100
        elif y_max <= 10000:
            scale_val = first*10
        else:
            scale_val = first
      

        if scale_var == True:
            #y_val = self.y/first #Dividing every element by the first value 
            
            y_val = self.y*scale_val #Multiply by 1000 to scale it
           
        else:
            y_val = self.y
       
        
        return y_val
        