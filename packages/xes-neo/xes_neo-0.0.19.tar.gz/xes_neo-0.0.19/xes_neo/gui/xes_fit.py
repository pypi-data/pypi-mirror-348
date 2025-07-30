"""
Author: Evan Restuccia (evan@restuccias.com)
"""

from turtle import back
from matplotlib import get_backend
import numpy as np
#from pyparsing import None_debug_action
import scipy as scipy
from scipy import signal
import random
import decimal
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning #Use this to get rid of numba warnings that are outputted in the terminal during run
import warnings
import numba as nb


warnings.filterwarnings('ignore')
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
#import chart_studio.plotly as py
#import peakutils
#from pybaselines import Baseline, utils #Will have to have people install this in order to make it run
#This is a test
class peak():
    #Probably default these to -1 later as a test condition, but not yet sure
    def __init__(self,paramRange,peakType, is_singlet = True, is_coster_kronig = False): #Coster-Kronig only works rn if this is True, but it will be true for all peaks.
        
        """
        Skips  the try catch block here, because the analysis which requires the fit
        will custom set the peaks later with values read from the GA output

        To add a Peak type:
        Add its peakType option to the picker in the GUI
        Give its parameters ranges and pass them into the write_ini in the gui
        add the range to ini_parser and also the paramrange dict in xes_neo
        add that bkgnType in init here, and assign the function to self.peakFunc
        add the get function for it
        add the set function in the gui xes_fit
        """
        
        #fetch ranges for the values from the dict
        self.SVSC = False
        self.paramRange= paramRange
        self.is_singlet = is_singlet
        self.is_coster_kronig = is_coster_kronig
       
        if paramRange != '':
            self.gaussRange = np.arange(paramRange['Gaussian'][0],paramRange['Gaussian'][1],paramRange['Gaussian'][2])
            self.lorentzRange = np.arange(paramRange['Lorentzian'][0],paramRange['Lorentzian'][1],paramRange['Lorentzian'][2])

            self.lorentzCKRange = np.arange(paramRange['Lorentzian Coster-Kronig'][0],paramRange['Lorentzian Coster-Kronig'][1],paramRange['Lorentzian Coster-Kronig'][2])

            self.photonEnergyRange = np.arange(paramRange['Photon Energy'][0],paramRange['Photon Energy'][1],paramRange['Photon Energy'][2])
            self.ampRange = np.arange(paramRange['Amplitude'][0],paramRange['Amplitude'][1],paramRange['Amplitude'][2])
            self.asymmetryRange = np.arange(paramRange['Asymmetry'][0],paramRange['Asymmetry'][1],paramRange['Asymmetry'][2])
            self.asymmetryDoniachRange = np.arange(paramRange['Asymmetry Doniach-Sunjic'][0],paramRange['Asymmetry Doniach-Sunjic'][1],paramRange['Asymmetry Doniach-Sunjic'][2])
            
            
            
            try:
                self.spinOrbitSplitRange = np.arange(paramRange['spinOrbitSplitting'][0],paramRange['spinOrbitSplitting'][1],paramRange['spinOrbitSplitting'][2])
            except:
                self.spinOrbitSplitRange = [0,0,0]


            #fully free within their range
            self.gaussian = np.random.choice(self.gaussRange)
            self.lorentz = np.random.choice(self.lorentzRange)
            #self.lorentz_CK = np.random.choice(self.lorentzCKRange) #Coster-Kronig
            #self.lorentz_CK = self.lorentz/1
            self.lorentz_CK = np.random.choice(self.lorentzCKRange)
            self.amp = np.random.choice(self.ampRange) #Scaling issues --> figure out what is wrong
            self.asymmetry = np.random.choice(self.asymmetryRange)
            self.asymmetryDoniach = np.random.choice(self.asymmetryDoniachRange)
            


            #the range is a modifier on the input value
            self.photonEnergy= np.random.choice(self.photonEnergyRange) #Not using rn --> changed to set parameter
            #self.s_o_split = np.random.choice(self.s_o_splittingRange) #Not using rn
        else:
            self.gaussian = None
            self.lorentz = None
            self.lorentz_CK = None
            self.photonEnergy = None
            self.amp = None
            self.asymmetry = None
        self.peakType = peakType
        self.peak_y = []

        
        if paramRange != '':
            self.branching_ratio = paramRange['branching_ratio']
            
            self.spinOrbitSplit= np.random.choice(self.spinOrbitSplitRange)
        else:
            self.branching_ratio = 1
            self.spinOrbitSplit = None
        
        
        self.SVSC = False
        self.peakType = peakType
        if(self.peakType.lower() == "voigt"):
            self.func = self.voigtFunc
        elif(self.peakType.lower() == "gaussian"):
            self.func = self.gaussFunc
        elif(self.peakType.lower() == "lorentzian"):
            self.func = self.lorentzFunc
        elif(self.peakType.lower() == "double lorentzian"):
            self.func = self.doubleLorentzFunc
        elif(self.peakType.lower() == "doniach-sunjic"):
            self.func = self.doniachSunjicFunc

        else:
            print("Error assigning peak type")
            print("Peaktype found is: " + str(self.peakType))
            exit()
        


    def peakFunc(self,x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        return self.func(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)

    #----------------------------Getters-------------------------------------------------------

    def get(self,is_coster_kronig,for_output_data_file = False):
        
        """
        Gets params in format [Singlet Params, bool for is_singlet, doublet params, peakType]
        """
        #Add in FWHM values for each curve type --> Voigt has 3, gauss and loretnz only have one
        params = []
        if self.peakType.lower() == 'voigt':
            params = [self.photonEnergy,self.gaussian,self.lorentz,self.amp] #mutate relies on the order here, so to change this you need to change
            #params = [self.photonEnergy,self.gaussian,self.lorentz,self.amp,self.peakType] #mutate relies on the order here, so to change this you need to change mutate
        if self.peakType.lower() == 'gaussian':
            params = [self.photonEnergy,self.gaussian,self.amp]#everything except lorentzian which in this case is the width i believe --> Still want FWHM
            #params = [self.photonEnergy,self.gaussian,self.amp,self.peakType]#everything except lorentzian which in this case is the width i believe --> Still want FWHM
        if self.peakType.lower() == 'lorentzian':
            params = [self.photonEnergy,self.lorentz,self.amp]
            #params = [self.photonEnergy,self.lorentz,self.amp,self.peakType]
        if self.peakType.lower() == 'double lorentzian':
            params = [self.photonEnergy,self.gaussian,self.lorentz,self.amp,self.asymmetry]
            #params = [self.photonEnergy,self.gaussian,self.lorentz,self.amp,self.asymmetry,self.peakType]
        if self.peakType.lower() == 'doniach-sunjic':
            params = [self.photonEnergy,self.gaussian,self.lorentz,self.amp,self.asymmetry] #no gaussian needed
            #params = [self.photonEnergy,self.lorentz,self.amp,self.asymmetry,self.peakType] #no gaussian needed
        
        #grab the bool is_singlet if writing for output
        if(for_output_data_file):
            params.append(self.is_singlet)
        self.is_coster_kronig = is_coster_kronig
      
    

       
        
       
            
            
        #ISSUE: INDIVIDUAL NOT SEEING COSTER KRONIG AS TRUE UNLIKE SINGLET. NOT SURE WHY???


        #grab the doublet params if its a doublet
       
        if not(self.is_singlet):
            if(for_output_data_file):
                params.append(self.branching_ratio)
            params.append(self.spinOrbitSplit)

            if self.is_coster_kronig: #If it is a doublet AND is Coster-Kronig
              
                params.append(self.lorentz_CK) #This is not being seen right now therefore not being outputted in analysis tab. Change if self.is_coster_kronig to if not()? why?
                #params.append(self.is_coster_kronig)
            params.append(self.is_coster_kronig)
            
          


            

        #and always end on the peakType
        params.append(self.peakType)



        #Add this peaks shirley background if using peak shirley
        if self.SVSC:
            SVSC_params = self.SVSC_background.get()
            for param in SVSC_params:
                params.append(param)
            return params
        else:
            if len(params) == 0:
                print("Cant do 'def get' in peaks class in XES_FIT, most likely a new peak was added and needs to be added to the get options")
                exit()
            else:
                return params

    """
    I don't think this set of functions is used ever
    """
    def getGaussian(self):
        return self.gaussian
    def getLorenztian(self):
        return self.lorentz
    def getAmplitude(self):
        return self.amp
    def getPhotonEnergy(self):
        return self.photonEnergy
    def getAsymmetry(self):
        return self.asymmetry
    def getAsymmetryDoniach(self):
        return self.asymmetryDoniach
    def getSpinOrbitSplit(self):
        return self.spinOrbitSplit



    def getFWHM(self,x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split): #Not wure where to call this in order to output the FWHM values for each peak curve type
        self.photonEnergy = PE
        self.lorentz = width
        self.lorentz_CK = width_CK
        self.is_coster_kronig = coster_kronig
        self.gaussian = sigma
        self.amp = A
        self.asymmetry = asym
        self.asymmetryDoniach = asymD
        self.is_singlet = singlet
        self.branching_ratio = branch
        self.spinOrbitSplit = split

        #MAD = np.mean(np.absolute(self.peak_y-np.mean(self.y))) #Mean Absolute Deviaition
        #self.lorentz = gamma = FWHM of a pure Lorentzian lineshape
        if(self.peakType.lower() == "voigt"):

            self.fwhm_g = 2*self.gaussian*np.sqrt(2*np.log(2))
            self.fwhm_l = self.lorentz
            self.fwhm_v = 0.5346*self.fwhm_l + np.sqrt(0.2166*pow(self.fwhm_l,2) + pow(self.fwhm_g, 2))
            #self.fwhm_v = self.fwhm_l/2 + np.sqrt(pow(self.fwhm_l, 2)/4 + pow(self.fwhm_g, 2))

            return self.fwhm_v #, self.fwhm_l, self.fwhm_g
        elif(self.peakType.lower() == "gaussian"):
            self.fwhm_g = 2*self.gaussian*np.sqrt(2*np.log(2))
            #print(self.fwhm_g)
            return self.fwhm_g
        elif(self.peakType.lower() == "lorentzian"):
            self.fwhm_l = self.lorentz
            return self.fwhm_l
        elif(self.peakType.lower() == "double lorentzian"):
            self.fwhm_g = 2*self.gaussian*np.sqrt(2*np.log(2))
            self.fwhm_l = self.lorentz
            self.fwhm_v = 0.5346*self.fwhm_l + np.sqrt(0.2166*pow(self.fwhm_l,2) + pow(self.fwhm_g, 2))
            #self.fhwm_v = self.fwhm_l/2 + np.sqrt(pow(self.fwhm_l, 2)/4 + pow(self.fwhm_g, 2))
            return self.fwhm_v #, self.fwhm_l, self.fwhm_g #Should double lorentzian still provide FWHM_L?
        elif(self.peakType.lower() == "doniach-sunjic"):
            self.fwhm_g = 2*self.gaussian*np.sqrt(2*np.log(2))
            self.fwhm_l = self.lorentz #Should this be two values? One for the asymmetrical side of the peak
            self.fwhm_v = 0.5346*self.fwhm_l + np.sqrt(0.2166*pow(self.fwhm_l,2) + pow(self.fwhm_g, 2))
            #self.fhwm_v = self.fwhm_l/2 + np.sqrt(pow(self.fwhm_l, 2)/4 + pow(self.fwhm_g, 2))
            return self.fwhm_v #, self.fwhm_l, self.fwhm_g #Should double lorentzian still provide FWHM_G?
        else:
            print("Error in FWHM caluclation")
            print("Peaktype found is: " + str(self.peakType))
            pass
    def getY(self,x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        """
        Gets the y values for a peak by running the peakFunc, then, if it has an SVSC background, it will tell its
        SVSC background to run and return both
        """
        #self.FWHM_values = self.getFWHM()
        #print("FWHM: ",self.FWHM_values)
    
        self.peakFunc(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)
        if self.SVSC:
            SVSC_vals = self.SVSC_background.getY(x,self.peak_y)
            return self.peak_y,SVSC_vals
        return self.peak_y

    #------------------------SVSC "On" Switch and SVSC handling----------------------------

    def SVSC_toggle(self,boolVal):
        """
        Turns on the SVSC for a peak if the option is turned on and creates a peak for it
        """
        self.SVSC = boolVal
        self.SVSC_background = background(self.paramRange,'SVSC_shirley')

    def set_svsc_shirley(self,val):
        self.SVSC_background.set_shirley_sherwood(val)

     #------------------------Setters--------------------------------------

    def set(self,params,doublet_params, CK_params, is_singlet=False, is_coster_kronig=True): #Changed is_coster_kronig to True here. WHy is is_singlet set to False here?
        """
        This is the main differentiator between the fit in gui and xesfolders
        The set function takes in a list of params, and should expect them to come in the same order that they were pushed out
        in the get function.

        """
        if(self.peakType.lower() == "voigt"):
            self.set_voigt(params)
        elif(self.peakType.lower() == "gaussian"):
            self.set_gauss(params)
        elif(self.peakType.lower() == "lorentzian"):
            self.set_lorentz(params)
        elif(self.peakType.lower() == "double lorentzian"):
            self.set_doubleLorentz(params)
        elif(self.peakType.lower() == "doniach-sunjic"):
            self.set_doniachSunjic(params)
        else:
            print("Error, cant find type to set, type found was: " + str(self.peakType))
  
        if not is_singlet:
            self.is_singlet = is_singlet
            self.branching_ratio = doublet_params[0]
            self.spinOrbitSplit = doublet_params[1]
          
            if is_coster_kronig == True:

                self.lorentz_CK = CK_params[0]


    #probably can delete these functions
    def setGaussian(self,newVal):
        self.gaussian = newVal
    def setLorentzian(self,newVal):
        self.lorentz = newVal
    def setAmplitude(self,newVal):
        self.amp = newVal
    def setPhotonEnergy(self,newVal):
        self.photonEnergy = newVal
    def setAsymmetry(self,newVal):
        self.asymmetry = newVal
    def setAsymmetryDoniach(self,newVal):
        self.asymmetryDoniach = newVal
    def setSpinOrbitSplit(self,newVal):
        self.spinOrbitSplit = newVal





    def set_voigt(self,paramList):
        self.photonEnergy = paramList[0]
        self.gaussian = paramList[1]
        self.lorentz = paramList[2]
        self.amp = paramList[3]
        #self.FWHM_values = paramList[4]

    def set_gauss(self,paramList):
        self.photonEnergy = paramList[0]
        self.gaussian = paramList[1]
        self.amp = paramList[2]
        #self.FWHM_values = paramList[3]
        #does lorentz effect gauss? --> it is just the width which is not used in the equation at all

    def set_lorentz(self,paramList):
        self.photonEnergy = paramList[0]
        self.lorentz = paramList[1]
        self.amp = paramList[2]
        #self.FWHM_values = paramList[3]

    def set_doubleLorentz(self,paramList):
        self.photonEnergy = paramList[0]
        self.gaussian = paramList[1]
        self.lorentz = paramList[2]
        self.amp = paramList[3]
        self.asymmetry = paramList[4]
        #self.FWHM_values = paramList[5]

    def set_doniachSunjic(self,paramList):
        self.photonEnergy = paramList[0]
        self.gaussian = paramList[1]
        self.lorentz = paramList[2]
        self.amp = paramList[3]
        self.asymmetryDoniach = paramList[4]
        #self.FWHM_values = paramList[5]

    #---------------------------------------Mutation Functions-------------------------------------------------


    def mutate(self,chance):
        self.mutateGauss(chance)
        self.mutateAmplitude(chance)
        self.mutatePE(chance)
        self.mutateLorentz(chance)
        self.mutateAsymmetry(chance)
        self.mutateAsymmetryDoniach(chance)
        '''
        if is_singlet==False:
            self.mutateSpinOrbitSplit
        '''
        if(self.SVSC):
            self.SVSC_background.mutate(chance)

    def mutateGauss(self,chance):
        if random.random()*100 < chance:
            self.gaussian = np.random.choice(self.gaussRange)
    def mutateLorentz(self,chance):
        if random.random()*100 < chance:
            self.lorentz = np.random.choice(self.lorentzRange)
    def mutateAmplitude(self,chance):
        if random.random()*100 < chance:
            self.amp = np.random.choice(self.ampRange)
    def mutatePE(self,chance):
        if random.random()*100 < chance:
            self.photonEnergy = np.random.choice(self.photonEnergyRange)
    def mutateAsymmetry(self,chance):
        if random.random()*100 < chance:
            self.asymmetry = np.random.choice(self.asymmetryRange)
    def mutateAsymmetryDoniach(self,chance):
        if random.random()*100 < chance:
            self.asymmetryDoniach = np.random.choice(self.asymmetryDoniachRange)
    '''
    def mutateSpinOrbitSplit(self,chance):
        if random.random()*100 < chance:
            self.spinOrbitSplit = np.random.choice(self.spinOrbitSplitRange)
    '''

    #Peak curve fit equations start at line 6681 in Aanalyzer PUnit1


    #----------------------Peak Curve Form Definitions------------------------------------------#


    #A bit scrappy at the moment, may need cleaning later
    def voigtFunc(self,x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):


        #Check to see if the data is in KE energy
        self.photonEnergy = PE
        self.lorentz = width
        self.lorentz_CK = width_CK
        self.is_coster_kronig = coster_kronig
        self.gaussian = sigma
        self.amp = A
        self.asymmetry = asym
        self.asymmetryDoniach = asymD
        self.is_singlet = singlet
        self.branching_ratio = branch
        self.spinOrbitSplit = split

        """
        Calculate the Voigt lineshape with variable peak position and intensity using a convolution of a Gaussian and a Lorentzian distribution.

        Parameters:
            x (array-like): The input array of independent variables.
            self.photonEnergy (float): The position of the peak.
            self.gaussian (float): The standard deviation of the Gaussian distribution.
            self.lorentz (float): The full width at half maximum (FWHM) of the Lorentzian distribution.
            intensity (float): The intensity of the peak.

        Returns:
            array-like: The values of the Voigt lineshape at the given x-values.
        """
        if self.gaussian ==0:
            self.gaussian += self.paramRange['Gaussian'][2]


        data_range= max(x) - min(x)
        data_range /= 2
        middle = min(x)+data_range
        offset = self.photonEnergy-middle
        num_points = len(x)
        x_values, dx = np.linspace(-data_range,data_range,num_points,retstep=True)


        gaussian = np.exp(-np.power(x_values, 2) / (2*(np.power(self.gaussian, 2)))) / (self.gaussian * np.sqrt(2 * np.pi))

        if self.is_singlet == True:
            #lorentz
            #                        gamma
            #            ----------------------------
            #                           2    gamma   2
            #            2 Pi ((x - PE ) + ( -----  )  )
            #                                  2
            lorentzian = (self.lorentz / (2*np.pi*(np.power(x_values+offset, 2) + np.power(self.lorentz/2, 2))))

            #gaussian
            #                    2
            #        - (x - PE)
            #        ------------
            #                2
            #         2 sigma
            #    e
            #    -----------------
            #            _____
            #    sigma  |/2 Pi

            
            final_voigt = scipy.signal.convolve(gaussian,lorentzian,'same')

     

        if self.is_singlet == False: #If it is a doublet

            if self.is_coster_kronig == True:

                nu1 = self.lorentz
                de11 = np.power((x_values+offset), 2) + np.power((self.lorentz/2), 2)
                de12 = 2*np.pi*de11
                lorentzian1 = (nu1/de12)/(1-self.branching_ratio)

                nu2 = self.branching_ratio*self.lorentz_CK
                de21 = np.power(x_values+offset+self.spinOrbitSplit,2) + np.power(self.lorentz_CK/2,2)
                de22 = 2*np.pi*de21
                lorentzian2 = (nu2/de22)/(1-self.branching_ratio)
                lorentzian = lorentzian1 + lorentzian2

                
                #Attempted multiiple things but the doublet is still not working.
                final_voigt = scipy.signal.fftconvolve(gaussian,lorentzian,'same')
            else:

                nu1 = self.lorentz
                de11 = np.power((x_values+offset), 2) + np.power((self.lorentz/2), 2)
                de12 = 2*np.pi*de11
                lorentzian1 = (nu1/de12)/(1-self.branching_ratio)

                nu2 = self.branching_ratio*self.lorentz
                de21 = np.power(x_values+offset+self.spinOrbitSplit,2) + np.power(self.lorentz/2,2)
                de22 = 2*np.pi*de21
                lorentzian2 = (nu2/de22)/(1-self.branching_ratio)
                lorentzian = lorentzian1 + lorentzian2


             
                #Attempted multiiple things but the doublet is still not working.
                final_voigt = scipy.signal.fftconvolve(gaussian,lorentzian,'same')



        #normalize the height so that intensity is the height of the max of the peak

        scale = max(final_voigt)
        for i in range(len(final_voigt)):
            final_voigt[i] *= (self.amp/scale)

        #returns, but also updates the yValues of the fit to improve efficiency, we can call that instead of recalculating every time
        if x[0] < x[-1]:
            final_voigt = final_voigt[::-1]
        else:
            pass

        self.peak_y = final_voigt
        #peak.voigt = voigt

        return final_voigt



    def gaussFunc(self,x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        self.photonEnergy = PE
        self.lorentz = width
        self.lorentz_CK = width_CK
        self.is_coster_kronig = coster_kronig
        self.gaussian = sigma
        self.amp = A
        self.asymmetry = asym
        self.asymmetryDoniach = asymD
        self.is_singlet = singlet
        self.branching_ratio = branch
        self.spinOrbitSplit = split

        

        if self.gaussian == 0:
            self.gaussian = .01

        gaussian = np.exp(-np.power(x - self.photonEnergy, 2) / (2 * np.power(self.gaussian, 2))) / (self.gaussian * np.sqrt(2 * np.pi))

        gaussian_max = max(gaussian)
        if(gaussian_max != 0):
            peakAmp = self.amp/max(gaussian)
        else:
            peakAmp = 0
        gauss_curve = gaussian * peakAmp

        #self.peak_y = gauss_curve

        if self.is_singlet == False: #If it is a doublet
            gaussian1 = (np.exp(-np.power(x - self.photonEnergy, 2) / (2 * np.power(self.gaussian, 2))) / (self.gaussian * np.sqrt(2 * np.pi)))/(1-self.branching_ratio)
            gaussian2 = self.branching_ratio * (np.exp(-np.power((x - (self.photonEnergy + self.spinOrbitSplit)), 2) / (2 * np.power(self.gaussian, 2))) / (self.gaussian * np.sqrt(2 * np.pi)))/(1-self.branching_ratio)
            gaussian = gaussian1 + gaussian2

            gaussian_max = max(gaussian)
            if(gaussian_max != 0):
                peakAmp = self.amp/max(gaussian)
            else:
                peakAmp = 0
            gauss_curve = gaussian * peakAmp
        '''
        if x[0] < x[-1]: #KE CONDITION
            gauss_curve = gauss_curve[::-1]
        else:
            pass
        '''
        self.peak_y = gauss_curve
        
        return gauss_curve





    def lorentzFunc(self,x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):

        global photonEnergy
        self.photonEnergy = PE
        self.lorentz = width
        self.lorentz_CK = width_CK
        self.is_coster_kronig = coster_kronig
        self.gaussian = sigma
        self.amp = A
        self.asymmetry = asym
        self.asymmetryDoniach = asymD
        self.is_singlet = singlet
        self.branching_ratio = branch
        self.spinOrbitSplit = split


        data_range= max(x) - min(x)
        data_range /= 2

        middle = min(x)+data_range
        offset = self.photonEnergy-middle
        num_points = len(x)
        x_values, dx = np.linspace(-data_range,data_range,num_points,retstep=True)

      
        #self.peak_y = lorentzian
        if self.is_singlet == True:
            lorentzian = (self.lorentz / (2*np.pi*(np.power(x_values+offset, 2) + np.power(self.lorentz/2, 2))))
            scale = max(lorentzian)
            for i in range(len(lorentzian)):
                lorentzian[i] *= (self.amp/scale)




        elif self.is_singlet == False: #If it is a doublet
            #No clue why but self.lorentz does not need to be made into the HWHM for the doublet. Branching ratio is still off for some reason.
            if self.is_coster_kronig == True:
                nu1 = self.lorentz
                de11 = np.power((x_values+offset), 2) + np.power((self.lorentz/2), 2)
                de12 = 2*np.pi*de11
                lorentzian1 = (nu1/de12)/(1-self.branching_ratio)

                nu2 = self.branching_ratio*self.lorentz_CK
                de21 = np.power(x_values+offset+self.spinOrbitSplit,2) + np.power(self.lorentz_CK/2,2)
                de22 = 2*np.pi*de21
                lorentzian2 = (nu2/de22)/(1-self.branching_ratio)

                lorentzian = (lorentzian1 + lorentzian2)


                scale = max(lorentzian)
                for i in range(len(lorentzian)):
                    lorentzian[i] *= (self.amp/scale)

            else:

                nu1 = self.lorentz
                de11 = np.power((x_values+offset), 2) + np.power((self.lorentz/2), 2)
                de12 = 2*np.pi*de11
                lorentzian1 = (nu1/de12)/(1-self.branching_ratio)

                nu2 = self.branching_ratio*self.lorentz
                de21 = np.power(x_values+offset+self.spinOrbitSplit,2) + np.power(self.lorentz/2,2)
                de22 = 2*np.pi*de21
                lorentzian2 = (nu2/de22)/(1-self.branching_ratio)

                lorentzian = (lorentzian1 + lorentzian2)


                scale = max(lorentzian)
                for i in range(len(lorentzian)):
                    lorentzian[i] *= (self.amp/scale)

        

        if x[0] < x[-1]: #KE CONDITION
            lorentzian = lorentzian[::-1]
        else:
            pass

        self.peak_y = lorentzian


        return lorentzian






    def doubleLorentzFunc(self,x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        #Same as voigt but with an added asymmetry factor to the width (lorentz)in the lorentzian equation
        self.photonEnergy = PE
        self.lorentz = width
        self.lorentz_CK = width_CK
        self.is_coster_kronig = coster_kronig
        self.gaussian = sigma
        self.amp = A
        self.asymmetry = asym
        self.asymmetryDoniach = asymD
        self.is_singlet = singlet
        self.branching_ratio = branch
        self.spinOrbitSplit = split


        #print("LORENTZ CK b4", self.lorentz_CK)
        #self.lorentz_CK = self.lorentz/self.branching_ratio
       
        if self.gaussian == 0:
            self.gaussian = .01

        data_range= max(x) - min(x)
        data_range /= 2

        middle = min(x)+data_range
        #offset = self.photonEnergy-middle
        #sos_offset = offset - self.spinOrbitSplit//2 #offset for spin-orbit splitting
        #sos_offset = -sos_offset
        #print(offset, sos_offset)

        num_points = len(x)
        x_values, dx = np.linspace(-data_range,data_range,num_points,retstep=True)
        dx = round(dx, 5)

        mult = 1
        #common multipliers
        offset_adj = 1
        #common multipliers
        if dx >= 0.1:
            offset_adj = 0.3
        else:
            offset_adj = 0.35
        self.photonEnergy = self.photonEnergy #+ dx*mult
        offset = self.photonEnergy-middle - offset_adj #Data is offset by dx*val for some reason
      
      
        #gaussian = np.exp(-np.power(x - self.photonEnergy, 2) / (2 * np.power(self.gaussian, 2))) / (self.gaussian * np.sqrt(2 * np.pi))
        gaussian = np.exp(-np.power(x_values, 2) / ((np.power(self.gaussian, 2)))) / (self.gaussian * np.sqrt(np.pi)) #Took away 2*np.power(self.gaussian,2) and np.sqrt(2*np.pi)

        # Calculate the Lorentzian component

        #Added +offset to all Lorentzian functions instead of Gauss --> It has to be inside the equation to make the leftside of the peak more lorentzian
        new_x = np.zeros(len(x))
        numP = len(x)
        HWHM = self.lorentz/2
        lorentzLeft = HWHM*self.asymmetry #Width of left side of peak due to asymmetry

        HWHM_CK = self.lorentz_CK/2
        lorentzLeft_CK = HWHM_CK*self.asymmetry
        #print("LORENTZ CK", self.lorentz_CK)
       
        #z = np.arange(-xRange, xRange+stepSize,.05)
        yDoubleL = [0]*numP
        y_left = [0]*numP
        y_right = [0]*numP
        #doubleL_lower = [0]*numP #lower PE doublet peak
        #doubleL_higher = [0]*numP #higher PE doublet peak


        #For some reason the peak location gets offset with difference asymmetry values
        #Dependent on dx value......
        asym_offset = 0
        if self.asymmetry < 1.9:
            asym_offset = 0.4
        elif 1.9 <= self.asymmetry < 2.7:
            asym_offset = 0.8
        elif 2.7 <= self.asymmetry < 3.7:
            asym_offset = 1.2
        elif 3.7 <= self.asymmetry < 4.9:
            asym_offset = 1.6
        elif 4.9 <= self.asymmetry < 6.5:
            asym_offset = 2.0
        elif 6.5 <= self.asymmetry < 8.6:
            asym_offset = 2.4
        elif 8.6 <= self.asymmetry < 11.2:
            asym_offset = 2.8
        elif 11.2 <= self.asymmetry < 14.6:
            asym_offset = 3.2
        elif 14.6 <= self.asymmetry < 19.1:
            asym_offset = 3.6
        elif self.asymmetry >= 19.1:
            asym_offset = 4.0


        





        if self.is_singlet == True:
            for i in range(len(x)):

                #KE Condition
                if x[0] < x[-1]:
                    if round(x_values[i] - offset-asym_offset, 5) <= 0:

                        yDoubleL[i] = 1 / ( 1 + np.power( (x_values[i] - offset-asym_offset)/lorentzLeft, 2 ) ) / np.pi
                    else:

                        yDoubleL[i] = 1 / ( 1 + np.power( (x_values[i] - offset-asym_offset)/HWHM, 2 ) ) / np.pi
                    yDoubleL[i] = yDoubleL[i] / (lorentzLeft/2 + HWHM/2)


                else:
                    if round(x_values[i] + offset, 5) >= 0:

                        yDoubleL[i] = 1 / ( 1 + np.power( (x_values[i] + offset)/lorentzLeft, 2 ) ) / np.pi
                    else:

                        yDoubleL[i] = 1 / ( 1 + np.power( (x_values[i] + offset)/HWHM, 2 ) ) / np.pi

                yDoubleL[i] = yDoubleL[i] / (lorentzLeft/2 + HWHM/2)

            lorentzian = yDoubleL

        elif self.is_singlet == False: #If it is a doublet


                for i in range(len(x)):

        

                        if round(x_values[i] - offset, 5) <= 0:
                            yDoubleL_right = 1 / (1 + np.power( (x_values[i] - offset)/ lorentzLeft, 2)) #/ (1 - self.branching_ratio) / np.pi / lorentzLeft/2

                        else:
                            
                            yDoubleL_right = 1 / (1 + np.power( (x_values[i] - offset)/ HWHM, 2)) #/ (1 - self.branching_ratio) / np.pi / HWHM/2


                        #Higher PE peak
                        if round(x_values[i] - offset - self.spinOrbitSplit, 5) <= 0:
                            yDoubleL_left = self.branching_ratio / (1 + np.power( (x_values[i] - (offset + self.spinOrbitSplit)) / lorentzLeft, 2)) #/ (1 - self.branching_ratio) / np.pi / lorentzLeft/2
                        else:
                            
                            yDoubleL_left = self.branching_ratio / (1 + np.power( (x_values[i] - (offset + self.spinOrbitSplit)) / HWHM, 2)) #/ (1 - self.branching_ratio) / np.pi / HWHM/2

                        yDoubleL[i] = (yDoubleL_right + yDoubleL_left) / (1 - self.branching_ratio) / np.pi



              

                lorentzian = yDoubleL

  
        doubleLorentz = scipy.signal.fftconvolve(gaussian,lorentzian,'same')
        doubleLorentz = doubleLorentz / (HWHM/4 + lorentzLeft/4 + HWHM_CK/4 + lorentzLeft_CK/4)
        scale = max(doubleLorentz)
        for i in range(len(doubleLorentz)):
            doubleLorentz[i] *= (self.amp/scale) #got rid of scale
        '''
        if PE_entry == True:
            x = x[::-1]
        '''
    
       


        self.peak_y = doubleLorentz
        
        return doubleLorentz





    #This is bad. Will fix later -Alaina
    def doniachSunjicFunc(self,x,PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        #Formula for Doniach-Sunjic peak equation:
        #
        #             cos(( pi  *  alpha ) / 2  +  (1 -  alpha ) * arctan((x - center) /  self.lorentz ))
        # Func =   ----------------------------------------------------------------------------
        #                                2          2  (1 - alpha) / 2
        #                  ( (x - center)   +   gamma )
        global photonEnergy
        self.photonEnergy = PE
        self.lorentz = width
        self.lorentz_CK = width_CK
        self.is_coster_kronig = coster_kronig
        self.gaussian = sigma
        self.amp = A
        self.asymmetry = asym
        self.asymmetryDoniach = asymD
        self.is_singlet = singlet
        self.branching_ratio = branch
        self.spinOrbitSplit = split

        data_range= max(x) - min(x)
        data_range /= 2

        middle = min(x)+data_range
        offset = self.photonEnergy-middle
        num_points = len(x)
        x_values, dx = np.linspace(-data_range,data_range,num_points,retstep=True)

        if self.gaussian ==0:
            self.gaussian += self.paramRange['Gaussian'][2]

        gaussian = np.exp(-np.power(x_values, 2) / ((np.power(self.gaussian, 2)))) / (self.gaussian * np.sqrt(np.pi))
        HWHM = self.lorentz/2
        HWHM_CK = self.lorentz/2
        if self.is_singlet == True:
            #self.asymmetryDoniach = -self.asymmetryDoniach #Opposite sign because it is in BE not KE


            #Singlet Doniach-Sunjic Equation:
            cos1 = (np.pi*self.asymmetryDoniach)/2
            cos2 = (1-self.asymmetryDoniach)*np.arctan((x_values+offset)/HWHM)
            numerator = np.cos(cos1 + cos2)
            de1 = pow(x_values+offset, 2) + pow(HWHM, 2)
            powDe = (self.asymmetryDoniach-1)/2
            denominator = pow(de1, powDe)
            lorentzian = numerator*denominator



        #Doesnt give doublet right now. Do not know why --> it follows the same methods as Aanalyzer
        elif self.is_singlet == False: #If it is a doublet

            if self.is_coster_kronig == True:

                cos1 = (np.pi*self.asymmetryDoniach)/2
                cos2 = (1-self.asymmetryDoniach)*np.arctan((x_values+offset)/HWHM)
                cos3 = (1-self.asymmetryDoniach)*np.arctan((x_values+self.spinOrbitSplit + offset)/HWHM_CK) #doublet only for the second part of the equation
                numerator1 = np.cos(cos1 + cos2)
                numerator2 = np.cos(cos1 + cos3)
                de1 = pow(x_values+offset, 2) + pow(HWHM, 2)
                de2 = pow(x_values + offset + self.spinOrbitSplit, 2) + pow(HWHM_CK, 2)
                powDe = (self.asymmetryDoniach-1)/2
                denominator1 = pow(de1, powDe)
                denominator2 = pow(de2, powDe)
                lorentzian = numerator1*denominator1 + self.branching_ratio*(numerator2*denominator2)

            else:

                cos1 = (np.pi*self.asymmetryDoniach)/2
                cos2 = (1-self.asymmetryDoniach)*np.arctan((x_values+offset)/HWHM)
                cos3 = (1-self.asymmetryDoniach)*np.arctan((x_values+self.spinOrbitSplit + offset)/HWHM) #doublet only for the second part of the equation
                numerator1 = np.cos(cos1 + cos2)
                numerator2 = np.cos(cos1 + cos3)
                de1 = pow(x_values+offset, 2) + pow(HWHM, 2)
                de2 = pow(x_values + offset + self.spinOrbitSplit, 2) + pow(HWHM, 2)
                powDe = (self.asymmetryDoniach-1)/2
                denominator1 = pow(de1, powDe)
                denominator2 = pow(de2, powDe)
                lorentzian = numerator1*denominator1 + self.branching_ratio*(numerator2*denominator2)




        doniachSunjic = scipy.signal.fftconvolve(gaussian,lorentzian,'same')

        #normalize the height so that intensity is the height of the max of the peak
        scale = max(doniachSunjic)
        for i in range(len(doniachSunjic)):
            doniachSunjic[i] *= (self.amp/scale)


        if x[0] < x[-1]: #KE CONDITION
            doniachSunjic = doniachSunjic[::-1]
        else:
            pass

        self.peak_y = doniachSunjic

        return doniachSunjic




#---------------------------Backgrounds Class---------------------------------------------------------------



class background(peak):
    """
    Background class is largely the same format as the peaks class,getY, set,get, function largely the same without
    most of the hassle the peaks come with

    One thing of note, most backgrounds are held by the individual, but SVSC backgrounds are held by a peak associated with them,
    and the peak takes on the management of it,but inside the background class it is the same as any other background

    To add a Background type:
    Add its bkgnType to the picker in the GUI
    Give its parameters ranges and pass them into the write_ini in the gui
    add the range to ini_parser and also the paramrange dict in xes_neo
    add that bkgnType in init here, and assign the function to self.bkgn
    add the get function for it
    add the set function in the gui xes_fit
    add the bgknType option to the self.bkgn_types at the top of xes_analysis2

    """
    def __init__(self,paramRange,bkgnType, peakType):
        self.bkgnType = bkgnType
        self.paramRange= paramRange
        self.peakType = peakType



        if self.bkgnType == 'Shirley-Sherwood':
            #self.bkgn = self.shirley_Sherwood



            #New Shirley Background
            self.bkgn = self.shirley_bkgn_again
            try:
                self.lorentzRange = np.arange(paramRange['Lorentzian'][0],paramRange['Lorentzian'][1],paramRange['Lorentzian'][2])
                self.photonEnergy = np.clip(self.photonEnergy,self.paramRange['Photon Energy'][0],self.paramRange['Photon Energy'][1])
                self.lorentz = np.random.choice(self.lorentzRange)
            except:
                self.lorentz = 1.2
                self.photonEnergy = 397.36
                
            
            if paramRange != '':
                self.k_range = np.arange(paramRange['k_range'][0],paramRange['k_range'][1],paramRange['k_range'][2])
                self.k = np.random.choice(self.k_range)
            else:
                self.k = 0
            
                
            '''
            if paramRange != '':
                self.backgroundShirRange = np.arange(paramRange['Shirley Background'][0],paramRange['Shirley Background'][1],paramRange['Shirley Background'][2])

                self.backgroundShirley = np.random.choice(self.backgroundShirRange)

            else:

                self.backgroundShirley = 100
            '''


        elif self.bkgnType.lower()  == 'linear':
            self.bkgn = self.linear_background
            try:
                self.backgroundRange = np.arange(paramRange['Background'][0],paramRange['Background'][1],paramRange['Background'][2])
                self.slopeRange = np.arange(paramRange['Slope'][0],paramRange['Slope'][1],paramRange['Slope'][2])

                #self.background is the b value in y = mx+b
                self.background = np.random.choice(self.backgroundRange)
                self.slope = np.random.choice(self.slopeRange)
                #self.slope = 0
            except:
                self.slope = 0
                self.background = -1
                if paramRange == '':
                    pass
        elif self.bkgnType == 'Exponential':
            self.bkgn = self.new_exponential

            try:
                self.A_range = np.arange(paramRange['Exponential Amplitude'][0],paramRange['Exponential Amplitude'][1],paramRange['Exponential Amplitude'][2])
                self.tau_range = np.arange(paramRange['Decay'][0],paramRange['Decay'][1],paramRange['Decay'][2])

                #self.background is the b value in y = mx+b
                self.A = np.random.choice(self.A_range)
                self.tau = np.random.choice(self.tau_range)
                #self.slope = 0
            except:
                self.A = 0
                self.tau = 0
                if paramRange == '':
                    pass
        elif self.bkgnType == 'Polynomial 1':
            self.bkgn = self.polynomial1
        elif self.bkgnType == 'Polynomial 2':
            self.bkgn = self.polynomial2
        elif self.bkgnType == 'Polynomial 3':
            self.bkgn = self.polynomial3
        elif self.bkgnType == '3-Param Tougaard':
            try:
                self.CTou3Range = np.arange(paramRange['CTou3'][0],paramRange['CTou3'][1],paramRange['CTou3'][2])
                self.DTou3Range = np.arange(paramRange['DTou3'][0],paramRange['DTou3'][1],paramRange['DTou3'][2])
                self.CTou3 = np.random.choice(self.CTou3Range)
                self.DTou3 = np.random.choice(self.DTou3Range)
            except:
                self.CTou3 = 1000 #Initial inputs in Aanalyzer
                self.DTou3 = 13300
            self.bkgn = self.Tougaard3Param
        elif self.bkgnType == '2-Param Tougaard':
            self.bkgn = self.Tougaard2Param
        elif self.bkgnType == 'SVSC_shirley':
            self.bkgn = self.shirley_Sherwood
            #func y vals tells you what to integrate over
            try:
                self.k_range = np.arange(paramRange['k_range'][0],paramRange['k_range'][1],paramRange['k_range'][2])
                self.k = np.random.choice(self.k_range)
            except:
                self.k = -1
                
        elif self.bkgnType == 'Baseline':
            self.bkgn = self.baseline2

            if paramRange != '':
                self.baselineRange = np.arange(paramRange['baseline'][0],paramRange['baseline'][1],paramRange['baseline'][2])
                self.baseline_value = np.random.choice(self.baselineRange)
            else:
                self.baseline_value = None

        else:
            print("Error Choosing Background in init of xes_fit")
            print("Background read as: " + str(self.bkgnType))
            exit()
        self.yBkgn = []

    def getY(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split,scale_var):
        y_val = []
        first = 1

        y_max = y.max()

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
            
            #y_val = y/first #Dividing every element by the first value 
            
            y_val = y*scale_val #Multiply by 1000 to scale it
               
        else:
            y_val = y
        y = y_val
       

        self.get_Background(x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)
        return self.yBkgn



    def get_Background(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        self.bkgn(x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)


    def mutate(self,chance):
        if self.bkgnType == 'Shirley-Sherwood':
            self.mutate_k(chance)
            self.mutate_backgroundShir
        if self.bkgnType == 'Baseline':
            self.mutate_baseline_value(chance)
        if self.bkgnType == 'Linear': #Added this in for new background --> Got rid of old slope
            self.mutate_background(chance)
            self.mutate_slope(chance)
        if self.bkgnType == 'SVSC_shirley':
            self.mutate_k(chance)
        if self.bkgnType == 'Exponential':
            self.mutate_A(chance)
            self.mutate_tau(chance)
        if self.bkgnType == '3-Param Tougaard':
            self.mutate_C(chance)
            self.mutate_D(chance)


    def mutate_k(self,chance):
        if random.random()*100 < chance:
            self.k = np.random.choice(self.k_range)

    #def mutate_backgroundShir(self,chance):
        #if random.random()*100 < chance:
            #self.backgroundShirley = np.random.choice(self.backgroundShirRange)

    def mutate_baseline_value(self,chance):
        if random.random()*100 < chance:
            self.baseline_value = np.random.choice(self.baselineRange)

    def mutate_background(self,chance):
        if random.random()*100 < chance:
            self.background = np.random.choice(self.backgroundRange)
    def mutate_slope(self,chance):
        if random.random()*100 < chance:
            self.slope = np.random.choice(self.slopeRange)

    def mutate_A(self,chance):
        if random.random()*100 < chance:
            self.A = np.random.choice(self.A_range)

    def mutate_tau(self,chance):
        if random.random()*100 < chance:
            self.tau = np.random.choice(self.tau_range)

    def mutate_C(self,chance):
        if random.random()*100 < chance:
            self.CTou3 = np.random.choice(self.CTou3Range)

    def mutate_D(self,chance):
        if random.random()*100 < chance:
            self.DTou3 = np.random.choice(self.DTou3Range)




    #Make sure to add in each background here
    def get(self):
       if self.bkgnType == 'Shirley-Sherwood':
            #return [self.k, self.backgroundShirley, self.bkgnType] #GET RID OF self.backgroundShirley
            return [self.k, self.bkgnType]
       elif self.bkgnType == 'Slope':
            return [self.bkgnType]
       elif self.bkgnType == 'Linear':
            return [self.new_b,self.slope,self.bkgnType]
       elif self.bkgnType == 'Exponential':
            return [self.A, self.tau, self.bkgnType]
       elif self.bkgnType == 'Baseline':
            return [self.baseline_value,self.bkgnType]
       elif self.bkgnType == 'Polynomial 1':
            return [self.bkgnType]
       elif self.bkgnType == 'Polynomial 2':
            return [self.bkgnType]
       elif self.bkgnType == 'Polynomial 3':
            return [self.bkgnType]
       elif self.bkgnType == '3-Param Tougaard':
            return [self.bkgnType, self.CTou3, self.DTou3]
       elif self.bkgnType == '2-Param Tougaard':
            return [self.bkgnType]
       elif self.bkgnType == 'SVSC_shirley':
           return [self.k,self.bkgnType]
    def getType(self):
        return self.bkgnType

    def set_k(self,newVal):
        self.k = newVal

    #def set_backgroundShir(self,newVal):
        #self.backgroundShirley = newVal

    def set_shirley_sherwood(self,params):
        self.k = params[0]
        #self.backgroundShirley = params[1]

    def set_baseline(self,params):
        self.baseline_value = params[0]


    def set_background(self,newVal):
        self.background = newVal

    def set_slope(self,newVal):
        self.slope = newVal

    def set_linear(self,params):
        self.new_b = params[0]
        self.slope = params[1]

    def set_exponential(self,params):
        self.A = params[0]
        self.tau = params[1]

    def set_Tougaard3(self,params):
        self.CTou3 = params[0]
        self.DTou3 = params[1]


    '''
    def baseline(self,x,y, PE, width, sigma, A, asym, asymD, singlet, branch, split):
        self.y = y
        self.x = x
        data_baseline = peakutils.baseline(x)
        funcs= data_baseline
        #bkgn_0 = data_baseline.modpoly(y, poly_order=0)[0]
        #funcs = bkgn_0
        self.yBkgn = funcs
        return self.yBkgn
    '''
    def baseline(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        self.y = y
        self.x = x

        poly_0 = np.polyfit(x, y, deg=0)
        funcs = np.polyval(poly_0, x)
        self.yBkgn = funcs

        return self.yBkgn



    def polynomial1(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split): #Doesnt work right now --> error in analysis x, y shapes (401), (0)
        self.y = y
        self.x = x

        numP = len(x)
        funcs = [0]*numP
        for i in np.arange(0, numP):
            funcs[i] = pow( (x[i]-x[int(np.rint(numP/2))]), 1);
        #poly_2 = np.polyfit(x, y, deg=2)
        #funcs = np.polyval(poly_2, x)
        self.yBkgn = funcs

        return self.yBkgn



    def polynomial2(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split): #Doesnt work right now --> error in analysis x, y shapes (401), (0)
        self.y = y
        self.x = x

        numP = len(x)
        funcs = [0]*numP
        for i in np.arange(0, numP):
            funcs[i] = pow( (x[i]-x[int(np.rint(numP/2))]), 2);
        #poly_2 = np.polyfit(x, y, deg=2)
        #funcs = np.polyval(poly_2, x)
        self.yBkgn = funcs

        return self.yBkgn



    def polynomial3(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        self.y = y
        self.x = x

        numP = len(x)
        funcs = [0]*numP
        for i in np.arange(0, numP):
            funcs[i] = pow( (x[i]-x[int(np.rint(numP/2))]), 3);

        self.yBkgn = funcs

        return self.yBkgn



    def new_exponential(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        numP = len(y)
        funcs =[0]*len(y)
        N = 10
        y_left = y[:N]
        y_0 = sum(y_left)/N #Average y at high PE
        x_0 = x[0]
        exp_0 = np.exp(-self.tau*x_0)
        pow_A = np.log10(exp_0)
        new_A = pow(self.A, pow_A)

        #print(self.A, self.tau)
        for i in np.arange(0, numP):
            #funcs[i] = y_0 -new_A*np.exp(-(x[i]*self.tau))
            #funcs[i] = y_0 -new_A*np.exp(-(x[i]*self.tau))
            #print(x[i], funcs[i])
            funcs[i] = y_0*np.exp(-self.tau*x[i])*np.exp(self.A)
            funcs[i] = y_0*np.exp(-self.tau*x[i])*np.exp(self.A)
        self.yBkgn = funcs

        return self.yBkgn


    def exponential_bkgn(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        self.y = y
        self.x = x

        #need to make these parameters outside background functions


        numP = len(y)
        funcs =[0]*len(y)

        #Taken from Aanalyzer code --> not sure why exponent is initially set to 1 or 0
        exponent = 1
        deltaExponent = max(abs(exponent / 100), 0.001)
        exponent += deltaExponent


        #Not sure if the x data needs to be flipped for PE instead of KE --> The exponential should be on the left side of the peak not the right
        for j in range(1, numP): #Cut off before numP so the end point is off. Need to fix this in order to scale down the righthand side of the background to the data
            gar = -exponent * (x[j] - x[numP // 2])

            if gar > 30:
                gar = 30
            elif gar < -30:
                gar = -30

            funcs[j] = -(np.exp(gar)) #Added negative sign to flip exponential to be in the -xy plane instead of +xy plane

        self.yBkgn = funcs

        return self.yBkgn



    def baseline2(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):

        bkgn_vals = [self.baseline_value]*len(y)
        self.yBkgn = bkgn_vals

        return bkgn_vals





     #Integral slope background works for now but is bad. Left side of data is not scaling properly
    def slope_bkgn(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        energyDelay= 0.5 #This is the initial value used in Aanalyzer --> not sure why??
        self.y = y
        self.x = x

        #need to make these parameters outside background functions
        numPeaksUsed = 1
        maxPeaks = 1
        numberBackgrounds = 1
        ma = maxPeaks + numberBackgrounds
        funcs = [0]*len(y)
        numP = len(y)



        for j in np.arange(numP-2, 0, -1): #error changed numP -1 to numP-2
            funcs[j] = (y[j] - y[numP-1]) * (x[j+1] - x[j]) + funcs[j+1] #changed y[numP] to y[numP -1] because of index error

        for j in range(1, numP):
            jDelay = 0
            x_eDelay = x[j] + energyDelay
            while j + jDelay < len(x) and x_eDelay > x[j + jDelay]:
                jDelay += 1
                if j + jDelay > numP:
                    jDelay -=1
                    break

            if j + jDelay > numP-1: #supposed to be just numP --> error
                funcs[j] = 0
            else:
                funcs[j] = funcs[j + jDelay]

        for j in np.arange(numP-2, 0, -1):#error changed numP -1 to numP-2
            funcs[j] = funcs[j] * (x[j+1] - x[j]) + funcs[j+1]


        self.yBkgn = funcs

        return self.yBkgn

    def new_slope(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):

        self.x = x
        self.y = y

        N = 10
        y_left = self.y[:N]
        y_right = self.y[N:]
        x_left = self.x[:N]
        x_right = self.x[N:]

        y_left_avg = sum(y_left)/N
        x_left_avg = sum(x_left)/N
        y_right_avg = sum(y_right)/N
        x_right_avg = sum(x_right)/N

        y_slope = (y_left_avg - y_right_avg)/(x_left_avg - x_right_avg)
        y_intercept = self.y[0] - y_slope*self.x[0]
        funcs = y_slope*self.x + y_intercept

        self.yBkgn = funcs

        return funcs



    def linear_background(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        self.y = y
        self.x = x
        numP = len(self.x)
        self.yBkgn = [0]*numP

        self.new_b = self.y[10] - self.slope*x[10]

        for i in range(numP):
            
            self.yBkgn[i] = self.linear(self.slope,self.x[i],self.new_b)
        #print(self.yBkgn)
        return self.yBkgn

    def linear(self,slope,x,new_b):
        
        return (slope*x)+new_b





    def better_shirley(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        #Not sure where this code came from. May need to cite it later. It has similar structure to the shirley formula described in Herrera's paper
        self.y = y
        self.x = x

        E = x
        J = y


        def integralOne(E, J, B, E1=0, E2=-1):
            integral = []
            if E2 < 0:
                E2 = len(J) + E2
            integral = sum([J[n] - B[n] for n in range(E,E2)])
            return integral

        def integralTwo(E, I, B, E1=0, E2=-1):
            integral = []
            if E2 < 0:
                E2 = len(I) + E2
            integral = sum([I[n] - B[n] for n in range(E1,E2)])
            return integral

        def getBn(E,I,B,E1=0,E2=-1):
            I2 = I[E2]
            I1 = I[E1]
            value = I2 + (I1 - I2)/(integralTwo(E,I,B,E1,E2))*integralOne(E,I,B,E1,E2)
            return value

        def iterateOnce(I,B,E1=0,E2=-1):
            b = [getBn(E,I,B,E1,E2) for E in range(len(I))]
            return b

        Bn = [0 for i in range(len(J))]
        Bn = iterateOnce(J,Bn)
        for i in range(6): #how many iterations it's doing
            B_temp = Bn
            Bn = iterateOnce(J,Bn)
            B_diff = [Bn[j] - B_temp[j] for j in range(len(Bn))] #Could make a check to see if the iterations are getting better. Usually little difference after 7 iterations

        self.yBkgn = Bn


        return self.yBkgn









    def SVSC_shirley(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):

        self.y = y
        self.x = x

        #Should probably declare these items outside of each background type
        numPeaksUsed = 1
        maxPeaks = 1
        numberBackgrounds = 1
        ma = maxPeaks + numberBackgrounds #will need to change to make it able to use multiple peaks/backgrounds
        numP = len(self.y)
        a =[0]*len(self.x) #dont know if we need a anymore?

        #voigt = peak.voigt
        funcs = y #len = numP -1 #recover initial peak curve --> How to get y points of just one peak??? Use PE range + some delta
        backgroundFromPeakShirleyFix = [0]*(len(self.y)-1) #not sure why its one less than the number of points
        SVSC_bkgn = backgroundFromPeakShirleyFix #easier to write --> original name comes from aanalyzer code

        a_old = 0.3
        a_new = 0.5 #are these initial values too large?
        old_fit = 10000
        best_fit = funcs #setting initial best fit --> just equal to y originally
        SVSC_diff = 1
        while a_new >= 0: #Iterates until a = 0, but keeps track of std of background to voigt fit. Need to find a better way for the GA to optimize a
            i = 1
            for i in range(maxPeaks):#calculates background for each peak then iterates
                #a_ratio is some parameter ratio --> I think it is the ratio of one parameter of different correlated peaks, unsure as to which parameter is being correlated
                a_ratio_b4 = a_old #Right now these are just random --> real code: a[ peakShirleyma[ peakShirelyCorrTo] ] / a[ mama[peakShirelyCorrTo] ]
                a_ratio_after = a_new #defined on line 15233 in PUnit1 --> Values are a[] before and after lfitmod is called
                peakShirleyBackground = 0.8*a_ratio_b4 + 0.2*a_ratio_after #I think this is supposed to be the scattering factor? Now sure how it is optimized
                #Maybe for now we should treat peakShirleyBackground as the scattering factor?

                for j in np.arange(numP -2, 0, -1):
                    SVSC_bkgn[j-1] = self.y[j-1]*-(self.x[j+1]-self.x[j])*peakShirleyBackground + SVSC_bkgn[j] #isnt this just what we already had but now with a wider range?
                    funcs[j] += SVSC_bkgn[j-1]
                #should write array in here to store each peak curves background --> will sum these up later
                i +=1

                iteration_diff = np.subtract(voigt, funcs) #need to change voigt to whatever the curve fit y array is
                new_fit = np.std(iteration_diff)
                new_fit_array = funcs
                if new_fit < old_fit:
                    old_fit = new_fit
                    best_fit = new_fit_array
                a_old = a_new
                a_new -= 0.01 #slow decrease for now --> NEED TO FIND BETTER WAY TO OPTIMIZE a_new
                #lfitmod caluculated here --> Calcualtes parameters between iterations: This is what makes the background active
                #Should we call class Peak here to recalculate the fit with the new background? Active curve fitting

        funcs = best_fit
        #return funcs #Not sure how we are calling this (self.yBKgn?)
        self.yBkgn = funcs

        return self.yBkgn





    def shirley_Sherwood(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        #too lazy to find all the x and ys and get rid of the self
        self.y = y
        self.x = x

        #need to make these parameters outside background functions
        numPeaksUsed = 1
        maxPeaks = 1
        numberBackgrounds = 1
        ma = maxPeaks + numberBackgrounds
        useIntegralBkgn=True
        numP = [0]*len(self.y) #we are using this as an array right now but it should just be the number of data points
        a =[0]*len(self.x)


        def iterations(self,x,y):
            numPeaksUsed = 1
            maxPeaks = 1
            numberBackgrounds = 1
            ma = maxPeaks + numberBackgrounds
            useIntegralBkgn=True
            numP = [0]*len(self.y) #we are using this as an array right now but it should just be the number of data points
            a =[0]*len(self.x)
            #need this to find the correct data points in which the bakcground will be removed
            numPointsAroundBackgroundLimitsLocal = 5
            nRightLocal = numPointsAroundBackgroundLimitsLocal // 2
            nLeftLocal = numPointsAroundBackgroundLimitsLocal // 2

            yRightLocal = 0
            yLeftLocal = 0

            for j in range(-(numPointsAroundBackgroundLimitsLocal // 2), numPointsAroundBackgroundLimitsLocal // 2 + 1):
                #yRightLocal += datos[dataNumber].ModifiedCurve.y[nRightLocal + j]
                #yLeftLocal += datos[dataNumber].ModifiedCurve.y[nLeftLocal + j]
                yRightLocal += self.y[len(self.y) - nRightLocal-1 + j]
                yLeftLocal += self.y[nLeftLocal + j]

            yLeftLocal /= (numPointsAroundBackgroundLimitsLocal // 2) * 2 + 1
            yRightLocal /= (numPointsAroundBackgroundLimitsLocal // 2) * 2 + 1



            nLeft = nLeftLocal
            nRight = len(x)-nRightLocal
            global yRight
            yRight = yRightLocal
            yLeft = yLeftLocal


            iterationsIntegralBkgn = 6
            BkgdCurve = []
            funcs = numP
            #funcs = np.zeros((ma, numP))

            if useIntegralBkgn: #from Aanalyzer code line 14867
                ma += 1 #Need to add in array to store each peak background peak[ma] --> sum in other backgrounds? peak[ma] += funcs...
                #funcs[ma][numP] = 0
                #print("K is " + str(self.k))
                for j in range(nRight-1, -1, -1):
                    #funcs[ma][j] = (self.y[j] - yRight[j]) * (self.x[j+1] - self.x[j]) + funcs[ma][j+1]
                    #print(self.y[j] - yRight)
                    funcs[j] = (self.y[j] - yRight) *self.k* -(self.x[j+1] - self.x[j]) + funcs[j+1] #assumes x is in KE, not sure if that changes anything

                '''
                for j in range(0, nLeft):
                    #funcs[ma][j] = funcs[ma][nLeft]
                    funcs[j] = yLeft-yRight
                '''
                integralma = ma

            '''
            #iterates shirley background
            if useIntegralBkgn: #from Aanalyzer code line 15140
                for l in range(iterationsIntegralBkgn):
                    for j in range(nRight-1, nLeft, -1):
                        #funcs[integralma][j] = (self.y[j] - yRight[j] - a[integralma] * funcs[integralma][j]) * (self.x[j+1] - self.x[j]) + funcs[integralma][j+1]
                        funcs[j] = (self.y[j] - yRight - funcs[j]) * (self.x[j+1] - self.x[j]) + funcs[j+1]
                    for j in range(1, nLeft):
                        #funcs[integralma][j] = funcs[integralma][nLeft]
                        funcs[j] = funcs[nLeft]
                        #calls lfitmod here -->calculates chisq and deletes all parameters

                    l += 1
            '''
            return funcs
        for i in range(1): #How many iterations it is performing
            funcs = iterations(self,x,y)
        self.yBkgn = funcs

        ''' Old built in baseline (bad)
        for i in range(len(self.yBkgn)):
            self.yBkgn[i] += yRight

        return self.yBkgn
        '''
    '''
    Just barely started on peak shirley, commented out so it wont cause a compilation error
    def peak_shirley(self,x,y,peak):
        peak.getY
    '''

    @nb.jit
    def Tougaard3Param(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        funcs = np.zeros(len(y))
        CTou3 = self.CTou3 #1000 #These values come from Aanalyzer --> not sure why these are the initial ones but it allows for the user to change them
        DTou3 = self.DTou3
        numP = len(y) #we are using this as an array right now but it should just be the number of data points

        #need this to find the correct data points in which the bakcground will be removed
        numPointsAroundBackgroundLimitsLocal = 5
        nRightLocal = numPointsAroundBackgroundLimitsLocal // 2
        nLeftLocal = numPointsAroundBackgroundLimitsLocal // 2

        yRightLocal = 0
        yLeftLocal = 0

        for j in range(-(numPointsAroundBackgroundLimitsLocal // 2), numPointsAroundBackgroundLimitsLocal // 2 + 1):
            yRightLocal += y[len(y) - nRightLocal-1 + j]
            yLeftLocal += y[nLeftLocal + j]

        yLeftLocal /= (numPointsAroundBackgroundLimitsLocal // 2) * 2 + 1
        yRightLocal /= (numPointsAroundBackgroundLimitsLocal // 2) * 2 + 1

        nRightLocal = len(x)-nRightLocal


        for i in np.arange(nLeftLocal, nRightLocal):
            integralGar = 0
            for j in np.arange(i, nRightLocal):
                energyDif = -(x[j] - x[i])
                integralGar += (y[j] - yRightLocal)*energyDif/(pow(CTou3-pow(energyDif,2),2) + ((DTou3*pow(energyDif,2))*-(x[j+1]-x[j])))
            funcs[i] = integralGar

        BTou3 = (yLeftLocal - yRightLocal)/funcs[nLeftLocal]
        for i in np.arange(nLeftLocal, nRightLocal):
            funcs[i] *= BTou3
            funcs[i] += yRightLocal

        for i in np.arange(0, nLeftLocal):
            funcs[i] = yLeftLocal

        for i in np.arange(nRightLocal, numP):
            funcs[i] = yRightLocal
            self.yBkgn = funcs

        return self.yBkgn





    @nb.jit
    def Tougaard2Param(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split): #Added in but does not work right now
        funcs = np.zeros(len(y))
        numP = len(y) #we are using this as an array right now but it should just be the number of data points

        #need this to find the correct data points in which the bakcground will be removed
        numPointsAroundBackgroundLimitsLocal = 5
        nRightLocal = numPointsAroundBackgroundLimitsLocal // 2
        nLeftLocal = numPointsAroundBackgroundLimitsLocal // 2

        yRightLocal = 0
        yLeftLocal = 0

        for j in range(-(numPointsAroundBackgroundLimitsLocal // 2), numPointsAroundBackgroundLimitsLocal // 2 + 1):
            yRightLocal += y[len(y) - nRightLocal-1 + j]
            yLeftLocal += y[nLeftLocal + j]

        yLeftLocal /= (numPointsAroundBackgroundLimitsLocal // 2) * 2 + 1
        yRightLocal /= (numPointsAroundBackgroundLimitsLocal // 2) * 2 + 1

        nRightLocal = len(x)-nRightLocal

        CTou2 = 1643 #Taken from Aanalyzer



        for i in np.arange(nLeftLocal, nRightLocal):
            integralGar = 0
            for j in np.arange(i, nRightLocal):
                energyDif = -(x[j] - x[i])
                integralGar += (y[j] - yRightLocal)*energyDif/CTou2-pow(energyDif,2)/CTou2-pow(energyDif,2)*(x[j+1] - x[j])
            funcs[i] = integralGar

        BTou2 = (yLeftLocal - yRightLocal)/funcs[nLeftLocal]
        for i in np.arange(nLeftLocal, nRightLocal):
            funcs[i] *= BTou2
            funcs[i] += yRightLocal

        for i in np.arange(0, nLeftLocal):
            funcs[i] = yLeftLocal

        for i in np.arange(nRightLocal, numP):
            funcs[i] = yRightLocal
            self.yBkgn = funcs

        return self.yBkgn




    def shirley_bkgn_again(self,x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split):
        

        #Dont want to be dependent upon I1 and I2:
        #Change to be more like:
        #
        #
        #S(E) = baseline_shirley + k1*(intensity integral peak 1)*Area peak 1 + k2*(intensity integral peak 2)*Area peak 2 .... for each peak
        #
        #Each peak is given a unique scattering factor valued between 0 and 1
        self.y = y
        self.x = x
        #integral = [0]*len(self.y) #we are using this as an array right now but it should just be the number of data points\
        #integral = [self.backgroundShirley]*len(y)


        peak_class = peak(self.paramRange, self.peakType)
        #baseline_shirley = [y[-1]]*len(y) #First value is just last data point in y array aka the rightside of data
        #self.photonEnergy = peak_class.photonEnergy

        if(self.peakType == "Voigt"):


            self.yValues = peak_class.voigtFunc(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split) #These are not the same as the ones we get from peak.peakFunc --> Object attribute error

        elif(self.peakType == "Gaussian"):
            self.yValues = peak_class.gaussFunc(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)
        elif(self.peakType == "Lorentzian"):
            self.yValues = peak_class.lorentzFunc(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)
        elif(self.peakType == "Double Lorentzian"):
            self.yValues = peak_class.doubleLorentzFunc(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)

        elif(self.peakType == "Doniach-Sunjic"):
            self.yValues = peak_class.doniachSunjicFunc(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)

        else:
            print("Error assigning peak type")
            print("Peaktype found is: " + str(self.peakType))
            exit()

        baseline_shirley = [min(self.yValues)]*len(y) #Using the smallest y value as the basis for the right side of the data
        yValues = self.yValues

        '''
        for i in range(len(x)):
            print(x[i], self.yValues[i])
        '''

        def areaA(baseline_shirley):

            numPointsAroundBackgroundLimitsLocal = 5
            nRightLocal = numPointsAroundBackgroundLimitsLocal // 2


            yRightLocal = 0


            for j in range(-(numPointsAroundBackgroundLimitsLocal // 2), numPointsAroundBackgroundLimitsLocal // 2 + 1):
                yRightLocal += self.y[len(self.y) - nRightLocal-1 + j]
            #Upper bound of integral
            yRightLocal /= (numPointsAroundBackgroundLimitsLocal // 2) * 2 + 1
            nRight = len(x)-nRightLocal
            A_sum = 0
            areaA = np.zeros(len(y))
            area_A = np.zeros(len(y))
            #print(nRight)
            #print(nRight)
            for i in np.arange(nRight-1, -1, -1):
                A_sum = np.sum(areaA)

                #areaA[i] = (((self.yValues[i]-baseline_shirley[i])+(self.yValues[i+1]-baseline_shirley[i+1]))/2)*(x[i+1]-x[i])
                areaA[i] = (((self.yValues[i])+(self.yValues[i+1])/2)*(x[i+1]-x[i]))
                area_A[i] = A_sum
                '''
                if areaA[i +1] > areaA[i]:
                    area_A[i] = A_sum - areaA[i]
                elif areaA[i + 1] == areaA[i]:
                    area_A[i] = area_A[i + 1]
                else:
                    pass
                '''

            return abs(area_A)

        total_area = areaA(baseline_shirley)






        def iterations(self,x,baseline_shirley, k_val, yValues):

            #need this to find the correct data points in which the bakcground will be removed
            baseline_shirley = [min(yValues)]*len(y)
            numPointsAroundBackgroundLimitsLocal = 5
            nRightLocal = numPointsAroundBackgroundLimitsLocal // 2


            yRightLocal = 0


            for j in range(-(numPointsAroundBackgroundLimitsLocal // 2), numPointsAroundBackgroundLimitsLocal // 2 + 1):
                yRightLocal += self.y[len(self.y) - nRightLocal-1 + j]
            #Upper bound of integral
            yRightLocal /= (numPointsAroundBackgroundLimitsLocal // 2) * 2 + 1
            nRight = len(x)-nRightLocal
            yRight = yRightLocal

            

            integral = baseline_shirley

            new_integral = baseline_shirley
            deltaX = abs(x[1] - x[2]) #Data stepsize --> this is assumed that the x data is stepwise and equal throughout the whole data range
            #Integral Calculation

            for j in range(nRight-1, -1, -1): #How to include area into this equation??

                #integral[j] = integral[j + 1] + k_val*(yValues[j] - baseline_shirley[j])*-(self.x[j+1] - self.x[j])#yValues and baseline_shirley should change with each
                #yRight is the avg of the right side of the data around the peal
                #k is the scattering factor valued bewteen 0 and 1
                #yValues - baseline_shirley is the difference from the curve fit to the background with baseline_shirley taking on the previous integral fit values for each iteration
                new_integral[j] = integral[j] + k_val*total_area[j]
                #print(k_val*total_area[j])
                #print(k_val*total_area[j])
            #print(np.array(new_integral).sum(), np.array(integral).sum())
            #return integral
            return new_integral




        self.yBkgn = iterations(self,x, baseline_shirley, self.k, yValues)


        return self.yBkgn
