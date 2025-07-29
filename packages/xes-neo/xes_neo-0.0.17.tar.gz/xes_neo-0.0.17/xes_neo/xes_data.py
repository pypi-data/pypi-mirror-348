import numpy as np

class xes_data():
    def __init__(self,fileName,skipLn):
        self.fileName = fileName
        self.skipLn = skipLn #int represnting files to skip
       
        self.read_file_txt()

    #not yet complete i was just throwing down some starter code
    def read_file_txt(self):
        self.x,self.y = np.loadtxt(self.fileName,skiprows=self.skipLn,unpack=True)
        self.numP = len(self.x)
       
        

    def get_x(self):
        return self.x

    def get_y(self, scale_var):
        y_val = []
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
        
        min_y = np.min(self.y)
        
        '''
        for i in range(len(self.y)):
            self.y[i] = self.y[i] - min_y #setting background to zero. Not sure if this is applied everywhere (being seen) right now 
        y_val = self.y
        '''
        
       

        return y_val
    
    #Subtracting off last y value from data (makes the data go to zero to help with baseline range)
    '''
    def get_y(self):
        new_y = [0]*len(self.y)
        for i in range(len(self.y)):
            new_y[i] = self.y[i] - self.y[-1]
        print(new_y)
        #return self.y
        return new_y
    '''

