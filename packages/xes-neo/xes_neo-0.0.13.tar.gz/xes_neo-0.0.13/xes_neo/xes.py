import enum
from xes_neo.helper import *
from xes_neo.import_lib import *
from xes_neo.ini_parser import *
#from pathObj import OliverPharr
#from .individual import Individual
#from pathrange import Pathrange_limits  #may be deletable/ built for XAFS
#from xes_neo_data import XES_Data #Do we need this still?

import numpy as np
from xes_neo.xes_individual import Individual
from xes_neo.xes_fit import peak,background
from xes_neo.xes_data import xes_data

from xes_neo.periodic_table import ElementData

from copy import deepcopy #fixes bug at line 70ish with deepcopy
"""
Author: Alana Humiston, Miu Lun Lau
"""


class XES_GA:

    def initialize_params(self,verbose = False):
        """
        Initialize Parameters
        """
        # print("Initialize Parameters")
        print("Initializing Params")
        self.intervalK = 0.05
        self.numGenSinceImproved = 0
        self.tol = np.finfo(np.float64).resolution
        

    def initialize_variable(self):
        """
        Initalize variables
        """
        print("Initializing Variables")
        self.genNum = 0
        self.nChild = 4
        self.globBestFit = [0,0]
        self.currBestFit = [0,0]
        self.bestDiff = 9999e11
        self.bestBest = 999999999e11
        self.diffCounter = 0
        self.element = element
        self.photoelectronLine = photoelectronLine
        self.transitionLine = transitionLine
        self.pathDictionary = {}
        self.data_file = data_file
        #self.data_cutoff = data_cutoff
        # Paths
        self.npaths = npaths
        #self.fits = fits

        # Populations
        self.npops = size_population
        self.ngen = number_of_generation
        self.steady_state = steady_state

        # Mutation Parameters
        self.mut_opt = mutated_options
        self.mut_chance = chance_of_mutation
        # self.mut_chance_e0 = chance_of_mutation_e0

        # Crosover Parameters
        self.n_bestsam = int(best_sample*self.npops*(0.01))
        self.n_lucksam = int(lucky_few*self.npops*(0.01))

        # Time related
        self.time = False
        self.tt = 0

    def initialize_file_path(self,i=0):
        """
        Initalize file paths for each of the file first
        """
        print("initializing file paths")
        self.base = os.getcwd()
        self.output_path = os.path.join(self.base,output_file)
        self.check_output_file(self.output_path)
        self.log_path = os.path.splitext(copy.deepcopy(self.output_path))[0] + ".log"
        self.check_if_exists(self.log_path)

        # Initialize logger
        self.logger = logging.getLogger('')
        # Delete handler
        self.logger.handlers=[]
        file_handler = logging.FileHandler(self.log_path,mode='a+',encoding='utf-8')
        stdout_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stdout_handler)

        self.logger.setLevel(logging.INFO)
        self.logger.info(banner())

    def check_if_exists(self,path_file):
        """
        Check if the directory exists
        """
        if os.path.exists(path_file):
            os.remove(path_file)
        # Make Directory when its missing
        path = pathlib.Path(path_file)
        path.parent.mkdir(parents=True, exist_ok=True)

    def check_output_file(self,file):
        """
        check if the output file for each of the file
        """
        file_base= os.path.splitext(file)[0]
        self.check_if_exists(file)
        self.file = file

        self.file_initial = open(self.output_path,"a+")
        self.file_initial.write("Gen,TPS,FITTNESS,CURRFIT,CURRIND,BESTFIT,BESTIND\n")  # writing header
        self.file_initial.close()

        file_data = os.path.splitext(file)[0] + '_data.csv'
        self.check_if_exists(file_data)
        self.file_data = file_data


    def initialize_range(self,scale_var,data_KE, data_XES,i=0,BestIndi=None):
        
        print("initializing ranges")
        """
        Initalize range

        To Do list:
            Initalize range will be difference for each paths depend if the run are
            in series, therefore the ranges will self-adjust
        """

        #self.periodicTable = ElementData(self.element,self.photoelectronLine, self.transitionLine)
        #PE_lit, singlet, so_split, Br = self.periodicTable.getParams(self.element,self.photoelectronLine) #Calls user selected element and gives elemental information
        #Current issue is that these values are given in variable form but the ones we currently call are all appended to an array.
        #This assumes that when you select something such as Zr3d that you are automatically making all other inputted peaks doublets.
        #This would need to change if you also have satellites/plasmons etc.
        #Next step is figuring out how to use this information in the algorithm.
        #We want to get rid of old user input for PE and instead go with the element
        #Need to also figure out how the user can provide elemental composition?
        #Maybe we call this in intparser instead?


        # data = np.genfromtxt(self.data_file,delimiter=',',skip_header=1)
  
        photoline_select = self.photoelectronLine
        transitionLine_select = self.transitionLine
        scale_var = scale_data
        self.data_obj = xes_data(self.data_file,skipLn = skipLn)
        #HOW TO CALL SCALE_VAR AND GET CORRECT VALUE IN THIS FUNCTION OR INIT?
        self.x_slice = self.data_obj.get_x()
       
        self.y_slice = self.data_obj.get_y(scale_var)
        self.x_array = self.x_slice
        self.y_array = self.y_slice
       

        yAvg = 0
        yTot = 0
        j=0
        for i,yVal in enumerate(self.data_obj.get_y(scale_var)[-10:]): #[-10:] gets last 10 items in array.
            yTot += yVal
            j=i
        yAvg = yTot/(j+1)

        #baseline_range[1] = yAvg
        #[0] = min range, [1] = max range, [2] = delta range
        #baseline_range = [0,yAvg,1]
        #amp_range[1] = max(self.data_obj.get_y()) #From data tesing it seems that having this in actually helps a lot with finding parameters
        
        N = 10
       
        y_left = self.y_array[:N]
        y_right = self.y_array[-N:]
        x_left = self.x_array[:N]
        x_right = self.x_array[-N:]
        self.y_left_avg = sum(y_left)/N
        x_left_avg = sum(x_left)/N
        self.y_right_avg = sum(y_right)/N
        x_right_avg = sum(x_right)/N
        
       
        #Different background ranges depending on if background is linear or not. If not it has a more limited range (closer to 0)
        
        if "Linear" in background_type:
                
          
            if self.y_left_avg > self.y_right_avg:
                if self.y_left_avg or self.y_right_avg < 0:
                   
                    baseline_range = [self.y_right_avg+np.round(self.y_right_avg*0.5, 2),self.y_left_avg-np.round(self.y_left_avg*0.25, 2),1]
                else:
                   
                    baseline_range = [self.y_right_avg-np.round(self.y_right_avg*0.5, 2),self.y_left_avg+np.round(self.y_left_avg*0.25, 2),1]
            else:
                if self.y_left_avg or self.y_right_avg < 0:
                    
                    baseline_range = [self.y_left_avg+np.round(self.y_left_avg*0.5, 2),self.y_right_avg-np.round(self.y_right_avg*0.25, 2),1]
                else:
                   
                    baseline_range = [self.y_left_avg-np.round(self.y_left_avg*0.5, 2),self.y_right_avg+np.round(self.y_right_avg*0.25, 2),1]
            if scale_var == True:
               
                baseline_range = [-0.1,0.1,0.1]
                
        else:
           
            if self.y_left_avg > self.y_right_avg:
                if self.y_right_avg < 0:
                  
                    baseline_range = [self.y_right_avg+np.round(self.y_right_avg*0.05, 2),self.y_left_avg-np.round(self.y_left_avg*0.05, 2),1]
                else:
                   
                    baseline_range = [self.y_right_avg-np.round(self.y_right_avg*0.05, 2),self.y_left_avg+np.round(self.y_left_avg*0.05, 2),1]
            else:
                if self.y_left_avg < 0:
                   
                    baseline_range = [self.y_left_avg+np.round(self.y_left_avg*0.05, 2),self.y_right_avg-np.round(self.y_right_avg*0.05, 2),1]
                else:
                  
                    baseline_range = [self.y_left_avg-np.round(self.y_left_avg*0.05, 2),self.y_right_avg+np.round(self.y_right_avg*0.05, 2),1]
            
            if scale_var == True:
             
                baseline_range = [-0.1,0.1,0.1]
   
                
        #print("BASELINE", baseline_range)
        #print("LEFT", self.y_left_avg, "RIGHT", self.y_right_avg)
        if x_right_avg > x_left_avg: #KE condition 
            y_slope = (self.y_right_avg - self.y_left_avg)/abs(x_right_avg - x_left_avg)
        else:
            y_slope = (self.y_left_avg - self.y_right_avg)/abs(x_left_avg - x_right_avg)
       
        if y_slope < 0:
           
            slope_range[0] = y_slope*1.1
            slope_range[1] = y_slope*0.9
            background_range[0] = -x_left_avg
            background_range[1] = -x_right_avg
           

        else:
            slope_range[0] = y_slope*0.9
            slope_range[1] = y_slope*1.1 #Set to the slope of the average of both sides of the data plus a little more for wiggle room
            if x_left_avg > x_right_avg:
                background_range[1] = x_left_avg
                background_range[0] = x_right_avg
            else:
                background_range[0] = x_left_avg
                background_range[1] = x_right_avg
      
       
        diff = self.y_left_avg - self.y_right_avg
        #background_shir_range[1] = self.y_right_avg + (self.y_right_avg/100)*25


        #Can change ranges to be within a certain percent range of what the user inputs. Right now it is set at 35% but can increase if needed

        '''
        percent_guess = 35/100

        sigma_range[0] =  -sigma_guess[0]*percent_guess
        sigma_range[1] =  sigma_guess[0]*percent_guess

        fwhm_range[0] = -gamma_guess[0]*percent_guess
        fwhm_range[1] =  gamma_guess[0]*percent_guess

        amp_range[0] =  -self.y_right_avg - amp_guess[0]*percent_guess #subtracts self.y_right_avg because amp guess excludes background (assuming user wont do that correctly)
        amp_range[1] =  -self.y_right_avg + amp_guess[0]*percent_guess
        '''

        #print(amp_guess[0])

        for n in range(len(amp_guess)):
            if amp_guess[n] < 0.5*round(self.y_right_avg,2):
                pass
            else:
                amp_guess[n] = amp_guess[n] -round(self.y_right_avg,2) #It is assumed that the user is inputting the amp + baseline so the average of the right data is subtratced to account for this
            
            if amp_guess[n] < 0: #No negative peaks
                amp_guess[n] = 0


        decay_rate = self.y_array[:1]*0.367879441

        for i in np.arange(0, len(self.y_array)): #Finding x value at the decay_rate intensity
            if self.y_array[i] >= decay_rate:
                decay_rate_x = self.x_array[i]
                pass
            else:
                decay_rate_x = self.x_array[i]
        amp_range = []
        PE_range = []
        sigma_range = []
        gamma_range = []

        max_peak = amp_guess[0] #Finding the peak with the largest amplitude and giving it a larger PE range
        #In the future we will need to have the algorithm check the elemental peak assingment here and give it a range based on a database of collected peak information
        peak_location = 0
        for i in amp_guess:
            if i >= max_peak:
                max_peak_location = peak_location
            peak_location += 1
        #PE_range_min[max_peak_location] = -0.5
        #PE_range_max[max_peak_location] = +0.5

        for i in range(len(PE_guess)): #Creating 2D arrays of range values for each peaks PE and amplitude

            if amp_limited[i] == True:
                amp_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                amp_range.append([amp_range_min[i], amp_range_max[i], amp_range_delta[i]])



            if PE_limited[i] == True:
                PE_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                PE_range.append([PE_range_min[i], PE_range_max[i], PE_range_delta[i]])



            if sigma_limited[i] == True:
                sigma_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                sigma_range.append([sigma_range_min[i], sigma_range_max[i], sigma_range_delta[i]])



            if gamma_limited[i] == True:
                gamma_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                gamma_range.append([gamma_range_min[i], gamma_range_max[i], gamma_range_delta[i]])


    
       
        #For data that comes in KE the spinOrbitSplitting needs to be negative
        
        for i in range(len(is_singlet)):
            if self.x_array[0] < self.x_array[-1]:
                if spinOrbitSplit_guess[i] > 0:
                    spinOrbitSplit_guess[i] = -spinOrbitSplit_guess[i]



      

        #exp_decay_range[0] = decay_rate_x - decay_rate_x*0.1
        #exp_decay_range[1] = decay_rate_x + decay_rate_x*0.1
        #background_shir_range[0] = y_right_avg - (y_right_avg/100)*25 #I think with the use of multiple peaks this should be allowed to be zero
        #k_range[1] = self.y_left_avg - y_right_avg + 200
       
        self.pars_range = {
            'Photon Energy': PE_range,
            'PE':PE_guess,
            'PE_limited' :PE_limited,
            'PE_correlated' :PE_correlated,
            'PE_correlated_mult' :PE_correlated_mult,
            'Gaussian': sigma_range,
            'Sigma': sigma_guess,
            'sigma_limited' :sigma_limited,
            'sigma_correlated' :sigma_correlated,
            'sigma_correlated_mult' :sigma_correlated_mult,
            'Lorentzian': gamma_range,
            'Gamma': gamma_guess,
            'gamma_limited' :gamma_limited,
            'gamma_correlated' :gamma_correlated,
            'gamma_correlated_mult' :gamma_correlated_mult,
            'Amplitude' : amp_range,
            'Amp': amp_guess,
            'amp_limited' :amp_limited,
            'amp_correlated' :amp_correlated,
            'amp_correlated_mult' :amp_correlated_mult,
            'Asymmetry' : asymmetry_range,
            'Asymmetry Doniach-Sunjic' : asymmetryDoniach_range,
            'k_range' : k_range,
            'Background' : background_range,
            #'Shirley Background' : background_shir_range,
            'CTou3' : CTou3_range,
            'DTou3' : DTou3_range,
            'Slope' : slope_range,
            'Exponential Amplitude' : exp_amp_range,
            'Decay' : exp_decay_range,
            'npeaks' : npaths,
            'baseline' : baseline_range,
            'branching_ratios' : branching_ratio,
            'is_singlet' : is_singlet,
            'is_coster_kronig' : is_coster_kronig,
            'Lorentzian Coster-Kronig' : gamma_CK_range,
            'Gamma Coster-Kronig' : gamma_CK_guess,
            'spinOrbitSplitting' : spinOrbitSplit_range,
            'spinOrbitSplit' : spinOrbitSplit_guess,
            'photoline' : photoline_select,
            'transitionline' :transitionLine_select
        }
        self.peak_type = peak_type
        self.backgrounds = background_type
       


    ''' Dont' think it's neccesary, we'll see
    def create_range(self,value,percentage,dt,prec): #-------Where is this called?--------
        """
        Create delta to calculate the ranges
        """
        minus = round(value - percentage*value,prec)
        plus = round(value + percentage*value,prec)
        range = np.arange(minus,plus+dt,dt)
        return range
    '''
   

    def scanResidual(self): #Need to expand function to see if overfitting the data --> Reomve that peak
        #Function to analyze the residual to determine if we need to add/subtract a peak
        
        
        
      
        

        yTotal = np.zeros(len(self.x_array)) 
        self.residual = np.zeros(len(self.x_array))
        residual_noiseless = np.zeros(len(self.x_array))

        yTotal = self.currBestY #Using the best fit Y values of the data 
       
        

        for j in range(len(self.x_array)):
            self.residual[j] = ((self.y_array[j] -yTotal[j])) #Positive means under fitting here and negative means overfitting
       

        #Want to subtract off the avg of the residual from both ends of the data to account for noise in data 
        N = 10
        res_left = self.residual[:N]
        res_right = self.residual[-N:]
       

        res_left_avg = sum(res_left)/N
       
        res_right_avg = sum(res_right)/N

        residual_average = (res_left_avg + res_right_avg)/2
       

        for j in range(2, len(self.x_array-2)):
            residual_noiseless[j] = self.residual[j] - residual_average

        max_res_location = 0
        #Finding location of top/bottom 6 maximum/minimum residual (where we want to add/remove a new peak)
        sorting_res = np.argsort(residual_noiseless)
        sorted_res = residual_noiseless[sorting_res]
       
        top_6_rev = sorted_res[-6 : ] 
        bottom_6 = sorted_res[ : 6] 
        top_6_PE = []
        bottom_6_PE = []

        top_6 = top_6_rev[::-1]
        for i in range(len(self.x_array)):
            if residual_noiseless[i] == top_6[0]:
                max_PE_1st_res = self.x_array[i]
            elif residual_noiseless[i] == top_6[1]:
                max_PE_2nd_res = self.x_array[i]
            elif residual_noiseless[i] == top_6[2]:
                max_PE_3rd_res = self.x_array[i]
            elif residual_noiseless[i] == top_6[3]:
                max_PE_4th_res = self.x_array[i]
            elif residual_noiseless[i] == top_6[4]:
                max_PE_5th_res = self.x_array[i]
            elif residual_noiseless[i] == top_6[5]:
                max_PE_6th_res = self.x_array[i]
            elif residual_noiseless[i] == bottom_6[0]:
                min_PE_1st_res = self.x_array[i]
            elif residual_noiseless[i] == bottom_6[1]:
                min_PE_2nd_res = self.x_array[i]
            elif residual_noiseless[i] == bottom_6[2]:
                min_PE_3rd_res = self.x_array[i]
            elif residual_noiseless[i] == bottom_6[3]:
                min_PE_4th_res = self.x_array[i]
            elif residual_noiseless[i] == bottom_6[4]:
                min_PE_5th_res = self.x_array[i]
            elif residual_noiseless[i] == bottom_6[5]:
                min_PE_6th_res = self.x_array[i]
        top_6_PE.append(max_PE_1st_res)
        top_6_PE.append(max_PE_2nd_res)
        top_6_PE.append(max_PE_3rd_res)
        top_6_PE.append(max_PE_4th_res)
        top_6_PE.append(max_PE_5th_res)
        top_6_PE.append(max_PE_6th_res)
        bottom_6_PE.append(min_PE_1st_res)
        bottom_6_PE.append(min_PE_2nd_res)
        bottom_6_PE.append(min_PE_3rd_res)
        bottom_6_PE.append(min_PE_4th_res)
        bottom_6_PE.append(min_PE_5th_res)
        bottom_6_PE.append(min_PE_6th_res)

        pass_cond_max = 0
        pass_cond_min = 0
        new_max_PE = 0
        new_min_PE = 0
        new_max_res = 0
        new_min_res = 0
        upper = PE_guess[0] + 2
        lower = PE_guess[0] - 2
       
        for i in range(len(top_6_PE)):
            
            if top_6_PE[i] > upper or top_6_PE[i] < lower:
                if pass_cond_max > 0:
                    pass
                else:
                    new_max_PE = top_6_PE[i]
                    new_max_res = top_6[i]
                    pass_cond_max +=1
            if bottom_6_PE[i] > upper or bottom_6_PE[i] < lower:
                if pass_cond_min > 0:
                    pass
                else:
                    new_min_PE = bottom_6_PE[i]
                    new_min_res = bottom_6[i]
                    pass_cond_min += 1


        
        

        max_peak = amp_guess[0]
        
        peak_location = 0
        for i in amp_guess: #Finding the location of the maximum amplitude peak
            if i >= max_peak:
                max_peak_location = peak_location
            peak_location += 1
        print("MINIMUM PEAK RESDIUAL", new_min_res, "-30%",-0.3*amp_guess[max_peak_location])
        print("MAXIMUM PEAK RESDIUAL", new_max_res, "15%",0.15*amp_guess[max_peak_location])
        #Check to remove peak. Won't remove if only one peak    
        if len(PE_guess) > 1:    
            if new_min_res < -0.3*amp_guess[max_peak_location] and new_min_res != 0: #NEED TO FIND A BETTER CONDITION FOR ADDING AND REMOVING PEAKS 
                #Do we want to check where the peak is located and make some evaluation from this using new_min_PE?
                print("Data is overfit. Removing peak to try to improve fitting")
                self.removePeak()

        if new_max_res > 0.15*amp_guess[max_peak_location]: #NEED TO FIND A BETTER CONDITION FOR ADDING AND REMOVING PEAKS 

            new_peak_PE = new_max_PE
            new_peak_amp = new_max_res
            print("NEW PEAK PE", new_peak_PE, "NEW PEAK AMPLITUDE", new_peak_amp)
            self.addPeak(new_peak_PE, new_peak_amp)
        else:
            print("NO NEW PEAK ADDED")
            

        
    

    

     

       


    #THIS FUNCTION IS ONLY WORKING FOR VOIGT RIGHT NOW. IMPROPER ADDITION OF THE NEW PARAMETERS WITH OTHER TYPES
    #Where do we call this function? --> Right now it is only functionable in generateFirstGen()
    def addPeak(self, new_PE, new_amp): #New function to be called after so many generations (20?). Used before next generation is created. 
        
        
        PE_guess.append(new_PE) #Want to use reisdual to determine where to add new peak?
        #Condition if the new peak trying to be added is too close to another peak --> Instead adjust amp of that peak
        #How to use reisudal to find these parameters? SOS? Br? etc. --> Take on same values as other peak but give a wider range?
      
        amp_guess.append(new_amp)
        sigma_guess.append(0.5)
        gamma_guess.append(0.25)

        amp_limited.append(False)
        PE_limited.append(False)
        gamma_limited.append(False)
        sigma_limited.append(False)
        amp_min_max = new_amp*0.2
        amp_range_min.append(-amp_min_max)
        amp_range_max.append(amp_min_max)
        amp_range_delta.append(0.05)

        PE_range_min.append(-0.2)
        PE_range_max.append(0.2)
        PE_range_delta.append(0.01)

        #Allowing for larger sigma and gamma range --> Need to figure out how to get a better estimate on these parameters from residual
        sigma_range_min.append(-0.5)
        sigma_range_max.append(0.5)
        sigma_range_delta.append(0.001)
       
        gamma_range_min.append(-0.25)
        gamma_range_max.append(0.25)
        gamma_range_delta.append(0.001)

        
        
        peak_type.append(peak_type[0]) #Appending whatever is the 1st input peak type --> Want to change in the future to have the algorithm decide what is the best peak type
        self.peak_type = peak_type
      

        i = len(PE_guess)

        PE_correlated.append(i)
        amp_correlated.append(i)
        gamma_correlated.append(i)
        sigma_correlated.append(i)

        #How to allow for peak correlation for added peak? Correlate if other peaks have correlation?
        PE_correlated_mult.append(1)
        amp_correlated_mult.append(1)
        sigma_correlated_mult.append(1)
        gamma_correlated_mult.append(1)

       
        #Take on the same values as the first peak? Maximum amp peak?
        branching_ratio.append(branching_ratio[0])
        spinOrbitSplit_guess.append(spinOrbitSplit_guess[0])
        gamma_CK_guess.append(gamma_guess[len(PE_guess)-1]) #taking in same gamma value as the newest gamma added
        is_singlet.append(is_singlet[0])
        is_coster_kronig.append(is_coster_kronig[0])


        npaths = len(PE_guess)
       


        #HAVE TO RECALL ALL THIS SO THAT WE CAN CALL PARS RANGE AGAIN
        photoline_select = self.photoelectronLine
        transitionLine_select = self.transitionLine
        N = 10
        y_left = self.y_array[:N]
        y_right = self.y_array[-N:]
        x_left = self.x_array[:N]
        x_right = self.x_array[-N:]

        self.y_left_avg = sum(y_left)/N
        x_left_avg = sum(x_left)/N
        self.y_right_avg = sum(y_right)/N
        x_right_avg = sum(x_right)/N
        if self.y_left_avg > self.y_right_avg:
            #Should we scale baseline so that the last point (lowest BE/highest KE) is subtratced off the y values (goes to zero) and set highest possible baseline value to the left side of the data?
            baseline_range = [-(self.y_left_avg+np.round(self.y_left_avg*0.2, 2)),self.y_left_avg+np.round(self.y_left_avg*0.05, 2),1] #Changed minimum to allow for background lower. Now allows for 20% below avg. and 5 % above
           
        else:
            baseline_range = [-(self.y_left_avg+np.round(self.y_left_avg*0.2, 2)),self.y_right_avg+np.round(self.y_right_avg*0.05, 2),1]

        amp_range = []
        PE_range = []
        sigma_range = []
        gamma_range = []

        max_peak = amp_range_max[0] #Finding the peak with the largest amplitude and giving it a larger PE range
        #In the future we will need to have the algorithm check the elemental peak assingment here and give it a range based on a database of collected peak information
        '''
        peak_location = 0
        for i in amp_range_max:
            if i >= max_peak:
                max_peak_location = peak_location
            peak_location += 1
        PE_range_min[max_peak_location] = -0.5
        PE_range_max[max_peak_location] = +0.5
        '''

        for i in range(len(PE_guess)): #Creating 2D arrays of range values for each peaks PE and amplitude

            if amp_limited[i] == True:
                amp_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                amp_range.append([amp_range_min[i], amp_range_max[i], amp_range_delta[i]])


            if PE_limited[i] == True:
                
                PE_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                PE_range.append([PE_range_min[i], PE_range_max[i], PE_range_delta[i]])
        


            if sigma_limited[i] == True:
                sigma_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                sigma_range.append([sigma_range_min[i], sigma_range_max[i], sigma_range_delta[i]])



            if gamma_limited[i] == True:
                gamma_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                gamma_range.append([gamma_range_min[i], gamma_range_max[i], gamma_range_delta[i]])


        #REDFINE parse_range after appending everything needed to add a peak

        #Recalling self.pars_range after fitting has already begun seems to restart the guesses for values to the values the algorithm has found and creates new ranges around those values
        self.pars_range = {
            'Photon Energy': PE_range,
            'PE':PE_guess,
            'PE_limited' :PE_limited,
            'PE_correlated' :PE_correlated,
            'PE_correlated_mult' :PE_correlated_mult,
            'Gaussian': sigma_range,
            'Sigma': sigma_guess,
            'sigma_limited' :sigma_limited,
            'sigma_correlated' :sigma_correlated,
            'sigma_correlated_mult' :sigma_correlated_mult,
            'Lorentzian': gamma_range,
            'Gamma': gamma_guess,
            'gamma_limited' :gamma_limited,
            'gamma_correlated' :gamma_correlated,
            'gamma_correlated_mult' :gamma_correlated_mult,
            'Amplitude' : amp_range,
            'Amp': amp_guess,
            'amp_limited' :amp_limited,
            'amp_correlated' :amp_correlated,
            'amp_correlated_mult' :amp_correlated_mult,
            'Asymmetry' : asymmetry_range,
            'Asymmetry Doniach-Sunjic' : asymmetryDoniach_range,
            'k_range' : k_range,
            'Background' : background_range,
            #'Shirley Background' : background_shir_range,
            'CTou3' : CTou3_range,
            'DTou3' : DTou3_range,
            'Slope' : slope_range,
            'Exponential Amplitude' : exp_amp_range,
            'Decay' : exp_decay_range,
            'npeaks' : npaths,
            'baseline' : baseline_range,
            'branching_ratios' : branching_ratio,
            'is_singlet' : is_singlet,
            'is_coster_kronig' : is_coster_kronig,
            'Lorentzian Coster-Kronig' : gamma_CK_range,
            'Gamma Coster-Kronig' : gamma_CK_guess,
            'spinOrbitSplitting' : spinOrbitSplit_range,
            'spinOrbitSplit' : spinOrbitSplit_guess,
            'photoline' : photoline_select,
            'transitionline' :transitionLine_select
        }

    def removePeak(self): #Removing peak from array. Right now it just removes the last input --> Need to change that 
        
        
        PE_guess.pop() 
      
        amp_guess.pop()
        sigma_guess.pop()
        gamma_guess.pop()

        amp_limited.pop()
        PE_limited.pop()
        gamma_limited.pop()
        sigma_limited.pop()
        
        amp_range_min.pop()
        amp_range_max.pop()
        amp_range_delta.pop()

        PE_range_min.pop()
        PE_range_max.pop()
        PE_range_delta.pop()

       
        sigma_range_min.pop()
        sigma_range_max.pop()
        sigma_range_delta.pop()

        gamma_range_min.pop()
        gamma_range_max.pop()
        gamma_range_delta.pop()

        peak_type.pop()
        self.peak_type = peak_type
      

       

        PE_correlated.pop()
        amp_correlated.pop()
        gamma_correlated.pop()
        sigma_correlated.pop()
       
        PE_correlated_mult.pop()
        amp_correlated_mult.pop()
        sigma_correlated_mult.pop()
        gamma_correlated_mult.pop()


        branching_ratio.pop()
        spinOrbitSplit_guess.pop()
        gamma_CK_guess.pop()
        is_singlet.pop()
        is_coster_kronig.pop()
        npaths = len(PE_guess)
       


        #HAVE TO RECALL ALL THIS SO THAT WE CAN CALL PARS RANGE AGAIN
        photoline_select = self.photoelectronLine
        transitionLine_select = self.transitionLine
        N = 10
        y_left = self.y_array[:N]
        y_right = self.y_array[-N:]
        x_left = self.x_array[:N]
        x_right = self.x_array[-N:]

        self.y_left_avg = sum(y_left)/N
        x_left_avg = sum(x_left)/N
        self.y_right_avg = sum(y_right)/N
        x_right_avg = sum(x_right)/N
        if self.y_left_avg > self.y_right_avg:
            #Should we scale baseline so that the last point (lowest BE/highest KE) is subtratced off the y values (goes to zero) and set highest possible baseline value to the left side of the data?
            baseline_range = [-(self.y_left_avg+np.round(self.y_left_avg*0.2, 2)),self.y_left_avg+np.round(self.y_left_avg*0.05, 2),1] #Changed minimum to allow for background lower. Now allows for 20% below avg. and 5 % above
           
        else:
            baseline_range = [-(self.y_left_avg+np.round(self.y_left_avg*0.2, 2)),self.y_right_avg+np.round(self.y_right_avg*0.05, 2),1]

        amp_range = []
        PE_range = []
        sigma_range = []
        gamma_range = []

        max_peak = amp_range_max[0] #Finding the peak with the largest amplitude and giving it a larger PE range
        #In the future we will need to have the algorithm check the elemental peak assingment here and give it a range based on a database of collected peak information
        peak_location = 0
        for i in amp_range_max:
            if i >= max_peak:
                max_peak_location = peak_location
            peak_location += 1
        PE_range_min[max_peak_location] = -0.5
        PE_range_max[max_peak_location] = +0.5

        for i in range(len(PE_guess)): #Creating 2D arrays of range values for each peaks PE and amplitude
         
            if amp_limited[i] == True:
                amp_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                amp_range.append([amp_range_min[i], amp_range_max[i], amp_range_delta[i]])



            if PE_limited[i] == True:
                
                PE_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                PE_range.append([PE_range_min[i], PE_range_max[i], PE_range_delta[i]])
        


            if sigma_limited[i] == True:
                sigma_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                sigma_range.append([sigma_range_min[i], sigma_range_max[i], sigma_range_delta[i]])



            if gamma_limited[i] == True:
                gamma_range.append([-0.00001, 0.00001, 0.00001]) #Making the range basically zero if the parameter is 'fixed'
            else:
                gamma_range.append([gamma_range_min[i], gamma_range_max[i], gamma_range_delta[i]])


        #REDFINE parse_range after appending everything needed to add a peak
        self.pars_range = {
            'Photon Energy': PE_range,
            'PE':PE_guess,
            'PE_limited' :PE_limited,
            'PE_correlated' :PE_correlated,
            'PE_correlated_mult' :PE_correlated_mult,
            'Gaussian': sigma_range,
            'Sigma': sigma_guess,
            'sigma_limited' :sigma_limited,
            'sigma_correlated' :sigma_correlated,
            'sigma_correlated_mult' :sigma_correlated_mult,
            'Lorentzian': gamma_range,
            'Gamma': gamma_guess,
            'gamma_limited' :gamma_limited,
            'gamma_correlated' :gamma_correlated,
            'gamma_correlated_mult' :gamma_correlated_mult,
            'Amplitude' : amp_range,
            'Amp': amp_guess,
            'amp_limited' :amp_limited,
            'amp_correlated' :amp_correlated,
            'amp_correlated_mult' :amp_correlated_mult,
            'Asymmetry' : asymmetry_range,
            'Asymmetry Doniach-Sunjic' : asymmetryDoniach_range,
            'k_range' : k_range,
            'Background' : background_range,
            #'Shirley Background' : background_shir_range,
            'CTou3' : CTou3_range,
            'DTou3' : DTou3_range,
            'Slope' : slope_range,
            'Exponential Amplitude' : exp_amp_range,
            'Decay' : exp_decay_range,
            'npeaks' : npaths,
            'baseline' : baseline_range,
            'branching_ratios' : branching_ratio,
            'is_singlet' : is_singlet,
            'is_coster_kronig' : is_coster_kronig,
            'Lorentzian Coster-Kronig' : gamma_CK_range,
            'Gamma Coster-Kronig' : gamma_CK_guess,
            'spinOrbitSplitting' : spinOrbitSplit_range,
            'spinOrbitSplit' : spinOrbitSplit_guess,
            'photoline' : photoline_select,
            'transitionline' :transitionLine_select
        }
       
        
        




    def generateIndividual(self):
        """
        Generate singular individual
        """
        
        ind = Individual(self.backgrounds,peak_type,self.scale_var,self.pars_range)
        
        return ind

    def generateFirstGen(self):
        print("generating first gen")
        self.Populations=[]

        #ind = Individual(self.backgrounds,peak_type,self.scale_var,self.pars_range)
        #self.addPeak(ind)

        
        for i in range(self.npops):
           
            self.Populations.append(self.generateIndividual())
      
        self.eval_Population()
        self.globBestFit = self.sorted_population[0]

        print("First gen generated")
    # @profile
    def fitness(self,indObj):
        """
        Evaluate fitness of a individual
        """
        loss = 0
        Individual = indObj
        yTotal = np.zeros(len(self.x_slice))
        self.residual = np.zeros(len(self.x_slice))
        
        #HOW TO MAKE SCALE VALUE SEEN HERE?
        yTotal = Individual.getFit(self.x_array,self.y_array, self.backgrounds)
       

        #Segmenting data to see where y falls off 
        
        big_diff = 0

        for i in range(len(self.x_array)-5):
            y_b4 = self.y_array[i]
           
            y_after = self.y_array[i+5]
            
            y_diff = y_b4 - y_after
            if self.x_array[0] < self.x_array[-1]: #KE condition

                if y_diff > 0:
                    new_diff = y_diff
                    if new_diff > big_diff:
                        big_diff = new_diff
                        location = i
            else:

                if y_diff < 0:
                    new_diff = y_diff
                    if new_diff < big_diff:
                        big_diff = new_diff
                        location = i
           

                #print("X B4", self.x[location], "X AFTER", self.x[location+40])
   
        y_low_PE_penalty = 0
        for k in range(location, len(self.x_array)-1):
            if (yTotal[k]- self.y_array[k]) > 0:
                y_low_PE_penalty += (yTotal[k]- self.y_array[k])*5000 #Dont think we need this penalty since we are accomadating for it in the bkgn_penalty

        for j in range(len(self.x_array)):

           # loss = loss + (yTotal[j]*self.x_array[j]**2 - self.y_array[j]* self.x_array[j]**2 )**2
            #loss = loss + (((yTotal[j]- self.y_array[j])**2)*self.y_array[j]
            #loss = loss + (((yTotal[j]- self.y_array[j])**2))*np.sqrt(self.y_array[j])

             #include a penalty for going outside of the spectral envelope
            penalty = 0
            bkgn_penalty = 0
            overfit_penalty = 0
            difference = (yTotal[j] - self.y_array[j])
            if difference > 0:
                overfit_penalty = difference*10000 #Adding penalty for going above the data
            sigma = np.sqrt(abs(self.y_array[j]))
          
            N = 30

            if sum(yTotal[:N])/N > self.y_left_avg: #Penalty for background going above the data on left side of plot
                diff = sum(yTotal[:N])/N - self.y_left_avg
                bkgn_penalty += 300000*sigma*diff

            if sum(yTotal[:N])/N < self.y_left_avg: #Penalty for background going below the data on left side of plot
                diff = abs(sum(yTotal[:N])/N - self.y_left_avg)
                bkgn_penalty += 300000*sigma*diff

            if sum(yTotal[-N:])/N > self.y_right_avg: #Penalty for background going above the data on right side of plot
                diff = sum(yTotal[-N:])/N - self.y_right_avg
                bkgn_penalty += 30000*sigma*diff

            if sum(yTotal[-N:])/N < self.y_right_avg: #Penalty for going below the data on right side of plot
                diff = abs(sum(yTotal[-N:])/N - self.y_right_avg)
                bkgn_penalty += 300000*sigma*diff

            if difference > 0:
                if difference >= 0.5*sigma:
                    penalty = 1000*sigma #Dont know if we need this is we already are taking into account the overfit_penalty
           
            loss = loss + (difference**2)*sigma + penalty*sigma + bkgn_penalty #+ overfit_penalty + y_low_PE_penalty
          
            self.residual[j] = ((yTotal[j]- self.y_array[j])) 
       
      
         # if loss == np.nan:
            # print(individual[0].verbose())
    
        return loss, yTotal
   
    def eval_Population(self):
        """
        Evalulate populations
        """
        
        score = []
        populationPerf = {}
        best_y = []
        temp_temp_score = 10000000000000000000000000
        yPerf = {}
        self.nan_counter = 0
        
        for i,individual in enumerate(self.Populations):
            temp_score, bestY = self.fitness(individual)
            
            #NEW PLAN FOR UPGRADING XES NEO:
            #Take residual from fitness and use it to determine change in range parameters or addition/sutraction of a peak
            #This should come into play only after so many generations without change or with very large residual
            #May need to add in another function that would add/remove a peak --> Get BE from residual idk how to get sigma/gamma/amp?
            #Another function for adjusting parameters --> Algorithm chooses between these two options based on some criteria
            
            #Finding the best y values from the best individual in the fit so far
            if temp_score < temp_temp_score:
                best_y = bestY
                temp_temp_score = temp_score
            # Calculate the score, if encounter nan, discard and generate new individual later
            if np.isnan(temp_score): #Change to be if residual is bad AND numGenSinceImproved > 10% of generation size then .... add/remove peak OR adjust parameters
                self.nan_counter +=1
            else:
                score.append(temp_score)
                populationPerf[individual] = temp_score
                
                
               
        self.sorted_population = sorted(populationPerf.items(), key=operator.itemgetter(1), reverse=False) #Get an error here if y values go below zero for some reason
        
        '''
        for a,b in self.sorted_population:
            print(str(b) + " " + str(a.get_params()))
        '''
        ''' Debugging again
        for i in range(len(self.sorted_population)):
            print(self.sorted_population[i][0].get_peak(0))
        '''
        self.currBestFit = self.sorted_population[0]
        self.currBestY = best_y
      

        return score

    
    def next_generation(self):
        """
        Calculate next generations

        """
        self.st = time.time()
        # ray.init()
        self.logger.info("---------------------------------------------------------")
        self.logger.info(datetime.datetime.fromtimestamp(self.st).strftime('%Y-%m-%d %H:%M:%S'))
        self.logger.info(f"{bcolors.BOLD}Gen: {bcolors.ENDC}{self.genNum+1}")

        self.genNum += 1

        # Evaluate Fittness
        score = self.eval_Population()
        self.bestDiff = abs(self.globBestFit[1]-self.currBestFit[1])
        if self.currBestFit[1] < self.globBestFit[1]:
            self.globBestFit = self.currBestFit
            self.numGenSinceImproved = 0
        else:
            self.numGenSinceImproved += 1

        
        with np.printoptions(precision=5, suppress=True):
            self.logger.info("Different from last best fit: " +str(self.bestDiff))
            self.logger.info("Number of Generations since improved: " + str(self.numGenSinceImproved))
            self.logger.info(bcolors.BOLD + "Best fit: " + bcolors.OKBLUE + str(self.currBestFit[1]) + bcolors.ENDC)
            self.logger.info("Best fit combination:\n" + str((self.sorted_population[0][0].get_params())))
            self.logger.info(bcolors.BOLD + "History Best: " + bcolors.OKBLUE + str(self.globBestFit[1]) +bcolors.ENDC)
            #self.logger.info("NanCounter: " + str(self.nan_counter))
            self.logger.info("History Best Indi:\n" + str((self.globBestFit[0].get_params())))

        nextBreeders = self.selectFromPopulation()
        self.logger.info("Number of Breeders: " + str(len(self.parents)))
        self.logger.info("DiffCounter: " + str(self.diffCounter))
        self.logger.info("Diff %: " + str(self.diffCounter / self.genNum))
        self.logger.info("Mutation Chance: " + str(self.mut_chance))
        self.mutatePopulation()
        self.createChildren()

        
        self.et = timecall()
        self.tdiff = self.et - self.st
        self.tt = self.tt + self.tdiff
        self.logger.info("Time: "+ str(round(self.tdiff,5))+ "s")
       
    def mutatePopulation(self):
        """
        # Mutation operators
        # 0 = original: generated a new versions:
        # 1 = mutated every genes in the total populations
        # 2 = mutated genes inside population based on secondary probability

        # TODO:
            options 2 and 3 needs to reimplmented
        """
        self.nmutate = 0

        if self.mut_opt  == 0:
            # Rechenberg mutation
            if self.genNum > 20:
                if self.bestDiff < 0.1:
                    self.diffCounter += 1
                else:
                    self.diffCounter -= 1
                if (abs(self.diffCounter)/ float(self.genNum)) > 0.2:
                    self.mut_chance += 0.5
                    self.mut_chance = abs(self.mut_chance)
                elif (abs(self.diffCounter) / float(self.genNum)) < 0.2:
                    self.mut_chance -= 0.5
                    self.mut_chance = abs(self.mut_chance)


        for i in range(self.npops):
            if random.random()*100 < self.mut_chance:
                self.nmutate += 1
                self.Populations[i] = self.mutateIndi(i)

        self.logger.info("Mutate Times: " + str(self.nmutate))


    def mutateIndi(self,indi):
        """
        Generate new individual during mutation operator
        """
        if self.mut_opt == 0:
            # Create a new individual with Rechenberg
            newIndi = self.generateIndividual()
        # Random pertubutions
        if self.mut_opt == 1:
            # Random Pertubutions
            self.Populations[indi].mutate_(self.mut_chance)
            newIndi = self.Populations[indi]
            # Mutate every gene in the Individuals

        if self.mut_opt == 2:
            # initalize_variable:
            self.nmutate_success = 0
            og_indi = copy.deepcopy(self.Populations[indi])
            og_score = self.fitness(og_indi)
            mut_indi = copy.deepcopy(self.Populations[indi])
            mut_indi.mutate_(self.mut_chance)
            mut_score = self.fitness(mut_indi)

            with np.errstate(divide='raise', invalid='raise'):
                try:
                    t_bot = (np.log(1-(self.genNum/self.ngen)+self.tol))
                except FloatingPointError:
                    print(self.genNum)
                    print(self.ngen)
                    print(1-(self.genNum/self.ngen))
                    t_bot = (np.log(1-(self.genNum/self.ngen)+self.tol))

            T = - self.bestDiff/t_bot
            if mut_score < og_score:
                self.nmutate_success = self.nmutate_success + 1;
                newIndi = mut_indi
            elif np.exp(-(mut_score-og_score)/(T+self.tol)) > np.random.uniform():

                self.nmutate_success = self.nmutate_success + 1;
                newIndi = mut_indi
            else:
                newIndi = og_indi

        if self.mut_opt == 3: #Not working --> Replace with DE?
            def delta_fun(t,delta_val):
                rnd = np.random.random()
                return delta_val*(1-rnd**(1-(t/self.ngen))**5)

            og_indi = copy.deepcopy(self.Populations[indi])
            og_data = og_indi.get_var() #error --> no value get_var
            for i,path in enumerate(og_data):
                print(i,path)
                arr = np.random.randint(2,size=3)
                for j in range(len(arr)):
                    new_path = []
                    val = path[j]
                    if arr[j] == 0:
                        UP = self.pathrange_Dict[i].get_lim()[j+1][1]
                        del_val = delta_fun(self.genNum,UP-val)
                        val = val + del_val
                    if arr[j] == 1:
                        LB = self.pathrange_Dict[i].get_lim()[j+1][0]
                        del_val = delta_fun(self.genNum,val-LB)
                    new_path.append(val)
                self.Populations[indi].set_path(i,new_path[0],new_path[1],new_path[2])
        if self.mut_opt == 4:
            newIndi = self.generateIndividual(self.bestE0)
        return newIndi

    def selectFromPopulation(self):
        self.parents = []

        select_val = np.minimum(self.n_bestsam,len(self.sorted_population))
        self.n_recover = 0
        if len(self.sorted_population) < self.n_bestsam:
            self.n_recover = self.n_bestsam - len(self.sorted_population)
        for i in range(select_val):
            self.parents.append(self.sorted_population[i][0])

    def crossover(self,individual1, individual2):
        """
        Uniform Cross-Over, 50% percentage chance
        """
     
        child = self.generateIndividual()

        individual1_path = individual1.get_params()
        individual2_path = individual2.get_params()

        #print("Ind 1 : " + str(individual1_path))
        #print("Ind 2 : " + str(individual2_path))
        temp_path = []
        dividers = [] # markers where the strings are in the list of params, this indicates where the array switches to a new peak or background
        #crossover for peak vars
        for j in range(len(individual1_path)):
            if (isinstance(individual1_path[j],str)):
                dividers.append(j)
            if np.random.randint(0,2) == True:
                temp_path.append(individual1_path[j])
            else:
                temp_path.append(individual2_path[j])
            '''
        for j in range(1):
            if np.random.randint(0,2) == True:
                temp_path.append(individual1_path[1][j])
            else:
                temp_path.append(individual2_path[1][j])
        '''
        #print("Temp Path: " + str(temp_path))
        temp_peak = []
        #print(temp_path)
        divider = 0
        peakNum = 0
        bkgnNum = 0
        for k in range(len(dividers)):
            for j in range(divider,dividers[k]+1):
                temp_peak.append(temp_path[j])
            if i < self.npaths:
                
                #print()
                #print("Child pre-write: " + str(child.get_params()))
                #print("temp peak : " + str(temp_peak))
                if child.setPeak(peakNum,temp_peak) == -1:
                    if bkgnNum<len(background_type):
                        #print("Bkgn")
                        child.setBkgn(bkgnNum,temp_peak)
                        bkgnNum += 1
                else:
                    #print("wrote peak")
                    peakNum +=1
                #print("Child after write")
                #print(child.get_params())
                #print()
                temp_peak = []
            divider = j + 1

        #print("Child : " + str(child.get_params()))
        '''
        child.setPeak(i,temp_path[0],temp_path[1],temp_path[2],temp_path[3])
        child.get_background(0).set_k(temp_path[4])
        '''
        '''
        print(temp_path)
        print("Child:")
        print(child.get_params())
        exit()
        '''
        return child

    def createChildren(self):
        """
        Generate Children
        """
        self.nextPopulation = []
        # --- append the breeder ---
        for i in range(len(self.parents)):
            self.nextPopulation.append(self.parents[i])
        # print(len(self.nextPopulation))
        # --- use the breeder to crossover
        # print(abs(self.npops-self.n_bestsam)-self.n_lucksam)

        for i in range(abs(self.npops-self.n_bestsam)-self.n_lucksam):
            par_ind = np.random.choice(len(self.parents),size=2,replace=False)
            child = self.crossover(self.parents[par_ind[0]],self.parents[par_ind[1]])
            self.nextPopulation.append(child)
        # print(len(self.nextPopulation))

        for i in range(self.n_lucksam):
            self.nextPopulation.append(self.generateIndividual())
        # print(len(self.nextPopulation))

        for i in range(self.n_recover):
            self.nextPopulation.append(self.generateIndividual())

        # for i in range(self.nan_counter):
        #     self.nextPopulation.append(self.generateIndividual())

        random.shuffle(self.nextPopulation)
        self.Populations = self.nextPopulation

    def run_verbose_start(self):
        self.logger.info("-----------Inputs File Stats---------------")
        self.logger.info(f"{bcolors.BOLD}File{bcolors.ENDC}: {self.data_file}")
        #self.logger.info(f"{bcolors.BOLD}File Type{bcolors.ENDC}: {self.data_obj._ftype}")
        self.logger.info(f"{bcolors.BOLD}File{bcolors.ENDC}: {self.output_path}")
        self.logger.info(f"{bcolors.BOLD}Population{bcolors.ENDC}: {self.npops}")
        self.logger.info(f"{bcolors.BOLD}Num Gen{bcolors.ENDC}: {self.ngen}")
        self.logger.info(f"{bcolors.BOLD}Mutation Opt{bcolors.ENDC}: {self.mut_opt}")
        self.logger.info("-------------------------------------------")

    def run_verbose_end(self):
        self.logger.info("-----------Output Stats---------------")
        # self.logger.info(f"{bcolors.BOLD}Total)
        self.logger.info(f"{bcolors.BOLD}Total Time(s){bcolors.ENDC}: {round(self.tt,4)}")
        self.logger.info("-------------------------------------------")

    def run(self, data_peak_add):
        self.run_verbose_start()
        self.historic = []
        self.historic.append(self.Populations)
        count = 0
        peak_add = 0
        before_best_fit = 0
        num_peaks = len(PE_guess)
        for i in range(self.ngen):
           
            temp_gen = self.next_generation()
        
       
            #Peak addition/removal determined by user checking selection button in GUI
            
            if peak_add_remove == True:
                
            
                if count == 5*len(PE_guess): #Condition for adding new peak. Does so after so many generations --> Maybe make peak num dependent 10*numPeaks --> Need more time to analyze more peaks
                
                    if peak_add > 0: 
                    
                        if before_best_fit < self.currBestFit[1]: #Check to make sure that the added peak improved the fit
                            #REMOVE PEAK THAT WAS ADDED
                            self.removePeak()
                            print("No improvement from peak addition. Added peak removed")
                    
                
                    self.scanResidual()
                    if len(PE_guess) > num_peaks:
                        num_peaks = len(PE_guess)
                        self.generateFirstGen()
                        if os.path.exists(self.file_data): os.remove(self.file_data)
                    elif len(PE_guess) < num_peaks:
                        num_peaks = len(PE_guess)
                        self.generateFirstGen()
                        if os.path.exists(self.file_data): os.remove(self.file_data) #CAN ADD NEW PEAKS HERE BUT IT WILL NEED TO DESTROY THE OLD OUTPUT FILE AND CREATE A NEW ONE SO THAT THE NUMBER OF COLUMNS ARE ALL THE SAME FOR ANALYSIS
                    before_best_fit = self.currBestFit[1]
                    count = 0
                    peak_add += 1
            
            
            self.output_generations()
            count += 1
           

        #print(self.globBestFit[0].getFit(self.x_array,self.y_array))
        self.run_verbose_end()
        # test_y = self.export_paths(self.globBestFit[0])
        # plt.plot(self.data_obj.get_raw_data()[:,0],self.data_obj.get_raw_data()[:,1],'b-.')
        # plt.plot(self.x_slice,self.y_slice,'o--',label='data')
        # plt.plot(self.x_slice,test_y,'r--',label='model')
        # plt.legend()
        # plt.show()

    def export_paths(self,indObj):
        area_list=[]
        Individual = indObj.get()

        yTotal = np.zeros(len(self.x_slice))
        plt.figure()
        for i,paths in enumerate(Individual):
            y = paths.getY()

            yTotal += y
            # area = np.trapz(y.flatten(),x=self.x_slice.flatten())
            # component = paths.get_func(self.x_slice).reshape(-1,1)

            # area_list.append(area)

        Total_area = np.sum(area_list)
        return yTotal

    def output_generations(self):
        """
        Output generations result into two files
        """
        try:
            f1 = open(self.file,"a")
            f1.write(str(self.genNum) + "," + str(self.tdiff) + "," +
                str(self.currBestFit[1]) + "," + str(self.currBestFit[0].get_params()) +")," +
                str(self.globBestFit[1]) + "," + str(self.globBestFit[0].get_params()) +"\n")
        finally:
            f1.close()
        try:
            f2 = open(self.file_data,"a")
            write = csv.writer(f2)
            bestFit = self.globBestFit[0]
            #write.writerow((bestFit[i][0], bestFit[i][1], bestFit[i][2]))
            str_pars = bestFit.get_params(for_output_file = True)
            write.writerow(str_pars)
            f2.write("#################################\n")
        finally:
            f2.close()

    def __init__(self,scale_var = False,data_KE = False, data_XES = False, data_peak_add = False):
        """
        Steps to Initalize XES
            XES
        """
        
        self.scale_var = scale_var
        # initialize params
        self.initialize_params()
        # variables
        self.initialize_variable()
        # initialze file paths
        self.initialize_file_path()
        # initialize range
        self.initialize_range(scale_var,data_KE, data_XES)
        # Generate first generation
        self.generateFirstGen()
      

        self.run(data_peak_add)

def main():
    XES_GA()

if __name__ == "__main__":
    main()
