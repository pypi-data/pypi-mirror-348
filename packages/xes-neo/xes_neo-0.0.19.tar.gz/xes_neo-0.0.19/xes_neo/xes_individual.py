"""
Created 7/5/23
Created the file, left out set peak to manually set a peak and its
parameters, it seems non essential for now
-Evan Restuccia (evan@restuccias.com)
"""
from tkinter import N
from matplotlib.bezier import get_parallels
from xes_neo.xes_fit import peak,background
import numpy as np

class Individual():
    def __init__(self,backgrounds,peaks,scale_var,pars_range=''):
        """
        backgrounds (array) Array where each element is the name of the background type desired
        peaks (array) array where each element is the name of the desired peakType
        pars_range (dict) each key is the name of a parameter with a tuple that contains the range the parameter is allowed to explore
        """
       
        self.scale_var = scale_var
        self.pars_range = pars_range
        #both peaks and backgrounds are arrays of strings which represent the type of the background of the peak/bkgn
        self.nPeaks = len(peaks)

        self.nBackgrounds = len(backgrounds)
        #self.peakArr = [None]* self.nPeaks
        self.bkgnArr = [None] * self.nBackgrounds
        self.peakDict = {}
        is_singlet = pars_range['is_singlet']
        is_coster_kronig = pars_range['is_coster_kronig']

        """
        the Photon Energy needs to be personalized
        we take the range, which right now is something like (0,.2), i.e. the allowed variance in PE
        Then we add our photon energy to it to move the range to the right spot
        """
        if 'SVSC_shirley' in backgrounds:
            self.SVSC_toggle = True
            self.bkgnArr = [None] * (self.nBackgrounds-1)
        else:
            self.SVSC_toggle = False
        amp_inputs = pars_range['Amplitude'] #Declaring here so that pars_range['Amplitude'] can become a 1d array in for loop. This method isnt the best but it works
        PE_inputs = pars_range['Photon Energy']
       
        self.peakArr = [None]*len(peaks)
        sigma_inputs = pars_range['Gaussian'] 
        gamma_inputs = pars_range['Lorentzian']


        #Declare these here so that we can change pars_range to be called inside xes_fit for each peak
        full_amp_range = pars_range['Amplitude']
        full_sigma_range = pars_range['Gaussian']
        full_gamma_range = pars_range['Lorentzian']
        full_energy_range = pars_range['Photon Energy']
        
        num_peaks = pars_range['npeaks']
        
       
        for i in range(self.nPeaks): 
        
            '''
            range_key = 'Photon Energy'
            guess_key = 'PE'
            PE_range = pars_range[range_key]
            PE1,PE2 =PE_range[0],PE_range[1]
            photon_energy = pars_range[guess_key][i]
            pars_range[range_key][0],pars_range[range_key][1] = [PE_range[0] + photon_energy, PE_range[1] + photon_energy,]
            '''

            #Want to add in correlation --> make PE_value/sigma_value/gamma_value/amp_value equal to the peak correlated or to multiplication of that value by something?
            #Have range become zero for that value?
            #Not sure how this will work with the random choice value used in xes_fit --> Will the correlation only follow the entry value?

            #Redefine range values to be the correct values and make them 1D to be called in xes_fit.
            self.PE_correlated = int(pars_range['PE_correlated'][i])
           
            self.PE_correlated_mult = pars_range['PE_correlated_mult'][i]
            self.sigma_correlated = int(pars_range['sigma_correlated'][i])
            self.sigma_correlated_mult = pars_range['sigma_correlated_mult'][i]
            self.gamma_correlated = int(pars_range['gamma_correlated'][i])
            self.gamma_correlated_mult = pars_range['gamma_correlated_mult'][i]
            self.amp_correlated = int(pars_range['amp_correlated'][i])
            self.amp_correlated_mult = pars_range['amp_correlated_mult'][i]
            

            if self.PE_correlated > num_peaks:
                print("Energy Peak Correlation out of range in Parameter Ranges tab")
                exit()
            if self.sigma_correlated > num_peaks:
                print("Sigma Peak Correlation out of range in Parameter Ranges tab")
                exit()
            if self.gamma_correlated > num_peaks:
                print("Gamma Peak Correlation out of range in Parameter Ranges tab")
                exit()
            if self.amp_correlated > num_peaks:
                print("Amplitude Peak Correlation out of range in Parameter Ranges tab")
                exit()

            range_key_PE = 'Photon Energy'
            guess_key_PE = 'PE'
            PE_inputs = np.array(PE_inputs)
           
            if PE_inputs.ndim > 1: #If it is a 2D array or not
                PE_range = PE_inputs[self.PE_correlated -1] #2D array  #Takes in same range as correlated peak # -1 because i starts at zero
            else:
                PE_range = PE_inputs #1D array


            PE_value = pars_range[guess_key_PE][self.PE_correlated-1] #Takes in same input value as correlated peak
            PE_value = PE_value*self.PE_correlated_mult
           
            if isinstance(PE_range, float): #Need this here because pars_range gets called later and is a 1D array.
                PE_range = PE_inputs
            #Check to make sure we do not have negative values
            #if PE_range[0] + PE_value < 0: CAN HAVE NEGATIVE PE VALUES!
                #pars_range[range_key_PE] = [0, PE_range[1] +PE_value, PE_range[2]]
            else:
                pars_range[range_key_PE] = [PE_range[0] +PE_value, PE_range[1] +PE_value, PE_range[2]]

            #print("Calculated range is " + str(pars_range[range_key][0]) + " " + str(pars_range[range_key][1]))
            pars_range['branching_ratio'] = pars_range['branching_ratios'][i]
            #pars_range['spinOrbitSplit'] = pars_range['spinOrbitSplit'][i]

            range_key_sos = 'spinOrbitSplitting'
            guess_key_sos = 'spinOrbitSplit'
            spinOrbitSplit_range = pars_range[range_key_sos]
            SOS1,SOS2 =spinOrbitSplit_range[0],spinOrbitSplit_range[1]
            sos = pars_range[guess_key_sos][i]

            pars_range[range_key_sos][0],pars_range[range_key_sos][1] = [spinOrbitSplit_range[0] + sos, spinOrbitSplit_range[1] + sos,]

           

            #New Sigma ranges for each peak
            range_key_sigma = 'Gaussian'
            guess_key_sigma = 'Sigma'

            sigma_inputs = np.array(sigma_inputs)
            if sigma_inputs.ndim > 1:
                sigma_range = sigma_inputs[self.sigma_correlated-1] #2D array
            else:
                sigma_range = sigma_inputs #1D array
           
            S1, S2 = sigma_range[0], sigma_range[1]    
           
            sigma_value = pars_range[guess_key_sigma][self.sigma_correlated-1]
            sigma_value = sigma_value*self.sigma_correlated_mult
           
            if isinstance(sigma_range, float): #Need this here because pars_range gets called later and is a 1D array.
                sigma_range = sigma_inputs

            #Check to make sure we do not have negative values
            if sigma_range[0] + sigma_value < 0:
                pars_range[range_key_sigma] = [0, sigma_range[1] +sigma_value, sigma_range[2]] 
            else:
                pars_range[range_key_sigma] = [sigma_range[0] +sigma_value, sigma_range[1] +sigma_value, sigma_range[2]] 
            
            #New Gamma ranges for each peak
            range_key_gamma = 'Lorentzian'
            guess_key_gamma = 'Gamma'

            gamma_inputs = np.array(gamma_inputs)
            if gamma_inputs.ndim > 1:
                gamma_range = gamma_inputs[self.gamma_correlated-1] #2D array
            else:
                gamma_range = gamma_inputs #1D array

           
            gamma_value = pars_range[guess_key_gamma][self.gamma_correlated-1]
            gamma_value = gamma_value*self.gamma_correlated_mult
            if isinstance(gamma_range, float): #Need this here because pars_range gets called later and is a 1D array.
                gamma_range = gamma_inputs
            #Check to make sure we do not have negative values
            if gamma_range[0] + gamma_value < 0:
                pars_range[range_key_gamma] = [0, gamma_range[1] +gamma_value, gamma_range[2]]
            else:
                pars_range[range_key_gamma] = [gamma_range[0] +gamma_value, gamma_range[1] +gamma_value, gamma_range[2]]

          
           



            '''
            #New user inputs of Sigma, Gamma, and Amplitude
            range_key_sigma = 'Gaussian'
            guess_key_sigma = 'Sigma'
            sigma_range = pars_range[range_key_sigma]
            S1,S2 =sigma_range[0],sigma_range[1]
            sigma_value = pars_range[guess_key_sigma][i]
            pars_range[range_key_sigma][0],pars_range[range_key_sigma][1] = [sigma_range[0] + sigma_value, sigma_range[1] + sigma_value,]

            range_key_gamma = 'Lorentzian'
            guess_key_gamma = 'Gamma'
            fwhm_range = pars_range[range_key_gamma]

            G1,G2 =fwhm_range[0],fwhm_range[1]
            gamma_value = pars_range[guess_key_gamma][i]
            pars_range[range_key_gamma][0],pars_range[range_key_gamma][1] = [fwhm_range[0] + gamma_value, fwhm_range[1] + gamma_value,]
            '''



            #Coster-Kronig Lorentz values:
            range_key_gamma_CK = 'Lorentzian Coster-Kronig'
            guess_key_gamma_CK = 'Gamma Coster-Kronig'
            fwhm_range_CK = pars_range[range_key_gamma_CK]
            
            CK1,CK2 =fwhm_range_CK[0],fwhm_range_CK[1]
            gamma_value_CK = pars_range[guess_key_gamma_CK][i]
            pars_range[range_key_gamma_CK][0],pars_range[range_key_gamma_CK][1] = [fwhm_range_CK[0] + gamma_value_CK, fwhm_range_CK[1] + gamma_value_CK]



            #New Amplitude ranges for each peak
            range_key_amp = 'Amplitude'
            guess_key_amp = 'Amp'

            amp_inputs = np.array(amp_inputs)
            if amp_inputs.ndim > 1:
                amp_range = amp_inputs[self.amp_correlated-1] #2D array
            else:
                amp_range = amp_inputs #1D array

            #A1,A2,A3 =amp_range[0],amp_range[1]
            amp_value = pars_range[guess_key_amp][self.amp_correlated-1]
            amp_value = amp_value*self.amp_correlated_mult
            
            if isinstance(amp_range, float): #Need this here because pars_range gets called later and is a 1D array.
                amp_range = amp_inputs
            #Check to make sure we do not have negative values
            if amp_range[0] + amp_value < 0:
                pars_range[range_key_amp] = [0, amp_range[1] +amp_value, amp_range[2]]
            else:
                pars_range[range_key_amp] = [amp_range[0] +amp_value, amp_range[1] +amp_value, amp_range[2]]
           
            


            self.peakArr[i] = peak(pars_range,peaks[i],is_singlet = is_singlet[i], is_coster_kronig = is_coster_kronig[i], PE_correlated = pars_range['PE_correlated'][i], PE_correlated_mult = pars_range['PE_correlated_mult'][i], sigma_correlated = pars_range['sigma_correlated'][i],sigma_correlated_mult = pars_range['sigma_correlated_mult'][i],gamma_correlated = pars_range['gamma_correlated'][i],gamma_correlated_mult = pars_range['gamma_correlated_mult'][i],amp_correlated = pars_range['amp_correlated'][i],amp_correlated_mult = pars_range['amp_correlated_mult'][i]) #ERROR HERE --> HOW TO MAKE XES_FIT ONLY SEE FIRST ARRAY IN AMPLITUDE???
            pars_range[range_key_sos][0],pars_range[range_key_sos][1] = SOS1,SOS2
        

        '''
        except:
            #Special option if youre creating a custom individual(i.e. for analysis)
            if pars_range =='':
                pass
            else:
                print("Error modding guesses")
                exit()
        '''

        #each index in the peaks/background array is the name of the peak/background type to be used
        k=0
        n=0
        '''
        for i in range(self.nBackgrounds):
            if backgrounds[i] == 'Shirley-Sherwood':
                self.bkgnArr = [None] * (self.nBackgrounds + self.nPeaks)
        '''

        

        for i in range(self.nBackgrounds):
       
            if backgrounds[i] == 'SVSC_shirley':
                self.nBackgrounds -=1
                pass
            elif backgrounds[i] == 'Shirley-Sherwood':

                #while n >= self.nPeaks:
                self.bkgnArr[k] = background(pars_range,backgrounds[i], peaks[n]) #Creating a unique shirley background for each peak...I think

                k +=1
                n +=1

            else:

                #n = 0 #Doesn't matter which peak we are looking at --> Only matters in Shirley case
                self.bkgnArr[k] = background(pars_range,backgrounds[i], peaks[n])
               
                k+=1

        
        #Moved down to account for calling ranges in background()
       
        for i in range(self.nPeaks): 
            
            if self.SVSC_toggle:
                self.peakArr[i].SVSC_toggle(self.SVSC_toggle) #activate peak shirley
          
            #pars_range[range_key][0],pars_range[range_key][1] = PE1,PE2
            for i in range(len(pars_range[range_key_PE])): pars_range[range_key_PE][i] = PE_range[i]
           
            pars_range[range_key_sos][0],pars_range[range_key_sos][1] = SOS1,SOS2

            #Added in sigma, gamma, and amplitude
            for i in range(len(pars_range[range_key_sigma])): pars_range[range_key_sigma][i] = sigma_range[i]
            for i in range(len(pars_range[range_key_gamma])): pars_range[range_key_gamma][i] = gamma_range[i]
            #pars_range[range_key_sigma][0],pars_range[range_key_sigma][1] = S1,S2
            #pars_range[range_key_gamma][0],pars_range[range_key_gamma][1] = G1,G2
            pars_range[range_key_gamma_CK][0],pars_range[range_key_gamma_CK][1] = CK1,CK2
            for i in range(len(pars_range[range_key_amp])): pars_range[range_key_amp][i] = amp_range[i]
            #pars_range[range_key_amp][0],pars_range[range_key_amp][1], pars_range[range_key_amp][2] = A1,A2,A3
           

        #Turn peak ranges back into 2D array to sort through all peaks otherwise it defaults to the last peaks parameter ranges
        pars_range[range_key_sigma] = full_sigma_range
        pars_range[range_key_gamma] = full_gamma_range
        pars_range[range_key_amp] = full_amp_range
        pars_range[range_key_PE] = full_energy_range

        

       

        '''
        for n in range(self.nPeaks):
            for i in range(self.nBackgrounds): #May have to iterate through peaks too if we want background to be peak dependent
                if backgrounds[i] == 'SVSC_shirley':
                    self.nBackgrounds -=1
                    pass
                else:

                    self.bkgnArr[k] = background(pars_range,backgrounds[i], peaks[n])
                    k+=1
        '''
         # Create dictionary of peaks and backgrounds
        for i in range(self.nPeaks):
            self.peakDict[f'peak_{i}'] = self.peakArr[i]
            

        for i in range(self.nBackgrounds):
            self.peakDict[f'bkgn_{i}'] = self.bkgnArr[i]

    def add_peak(self,peakType):
        
        self.peakArr.append(peak(self.pars_range,peakType))
    def add_bkgn(self,bkgnType):
        
        self.bkgnArr.append(background(self.pars_range,bkgnType))
    
    #adds all backgrounds and peaks as one y value array
    def getFit(self,x,y, backgrounds):
        #ISSUE WHEN ONE PEAK IS DL/GAUSS/DS --> MOVES RANGES OVER BY ONE PEAK TILL LAST PEAK WHICH IS CONSTANT. KICKS IN AT START OF SECOND GEN
        yFit = [0]*len(x)
        FWHM = [0]*self.nPeaks
        
       
        for i in range(self.nPeaks):
       
          
            '''
            asymD = self.peakArr[i].asymmetryDoniach
       

            gamma_correlated = int(self.peakArr[i].gamma_correlated)
            gamma_correlated_mult = self.peakArr[i].gamma_correlated_mult
            
            #THIS IS WRONG --> TAKING IN INOUT VALUES NOT THE VALUES FOUND IN XES_FIT
            self.PE_correlated = int(self.pars_range['PE_correlated'][i])
            self.PE_correlated_mult = self.pars_range['PE_correlated_mult'][i]
            self.sigma_correlated = int(self.pars_range['sigma_correlated'][i])
            self.sigma_correlated_mult = self.pars_range['sigma_correlated_mult'][i]
            self.gamma_correlated = int(self.pars_range['gamma_correlated'][i])
            self.gamma_correlated_mult = self.pars_range['gamma_correlated_mult'][i]
            
            self.amp_correlated = int(self.pars_range['amp_correlated'][i])
            self.amp_correlated_mult = self.pars_range['amp_correlated_mult'][i]

            
            PE_value = self.pars_range['PE'][self.PE_correlated-1] 
            PE_value = PE_value*self.PE_correlated_mult
            PE = PE_value

            gamma_value = self.pars_range['Gamma'][self.gamma_correlated-1]
            gamma_value = gamma_value*self.gamma_correlated_mult
            width = gamma_value

            sigma_value = self.pars_range['Sigma'][self.sigma_correlated-1]
            sigma_value = sigma_value*self.sigma_correlated_mult
            sigma = sigma_value
            

            amp_value = self.pars_range['Amp'][self.amp_correlated-1]
            amp_value = amp_value*self.amp_correlated_mult
            A = amp_value

            asym = self.peakArr[i].asymmetry
            singlet = self.peakArr[i].is_singlet
            coster_kronig = self.peakArr[i].is_coster_kronig
            if coster_kronig == True:
                width_CK = self.peakArr[i].lorentz_CK
            else:
                width_CK = self.peakArr[gamma_correlated-1].lorentz
            branch = self.peakArr[i].branching_ratio
            split = self.peakArr[i].spinOrbitSplit
            '''
            
     
            PE_correlated = int(self.peakArr[i].PE_correlated)
           
            PE_correlated_mult = self.peakArr[i].PE_correlated_mult
            sigma_correlated = int(self.peakArr[i].sigma_correlated)
            sigma_correlated_mult = self.peakArr[i].sigma_correlated_mult
            gamma_correlated = int(self.peakArr[i].gamma_correlated)
            gamma_correlated_mult = self.peakArr[i].gamma_correlated_mult
            amp_correlated = int(self.peakArr[i].amp_correlated)
            amp_correlated_mult = self.peakArr[i].amp_correlated_mult
            
            asymD = self.peakArr[i].asymmetryDoniach
            PE = self.peakArr[PE_correlated-1].photonEnergy
            PE = PE*PE_correlated_mult
            width = self.peakArr[gamma_correlated-1].lorentz
            width = width*gamma_correlated_mult
            sigma = self.peakArr[sigma_correlated-1].gaussian
            sigma = sigma*sigma_correlated_mult
            A = self.peakArr[amp_correlated-1].amp
            A = A*amp_correlated_mult
            asym = self.peakArr[i].asymmetry
            singlet = self.peakArr[i].is_singlet
            coster_kronig = self.peakArr[i].is_coster_kronig
            if coster_kronig == True:
                width_CK = self.peakArr[i].lorentz_CK
            else:
                width_CK = self.peakArr[gamma_correlated-1].lorentz
            branch = self.peakArr[i].branching_ratio
            split = self.peakArr[i].spinOrbitSplit

            #print("PEAK #:", i)
            if self.SVSC_toggle:
                peak_y,svsc_y = self.peakArr[i].getY(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)
                yFit += peak_y
                yFit += svsc_y
            else:
                yFit += self.peakArr[i].getY(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)
                FWHM += self.peakArr[i].getFWHM(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)



        n = 0
        for i in range(self.nBackgrounds):
            PE_correlated = int(self.peakArr[n].PE_correlated)
            sigma_correlated = int(self.peakArr[n].sigma_correlated)
            gamma_correlated = int(self.peakArr[n].gamma_correlated)
            amp_correlated = int(self.peakArr[n].amp_correlated)
            


            asymD = self.peakArr[n].asymmetryDoniach
            PE = self.peakArr[PE_correlated-1].photonEnergy
            
            width = self.peakArr[gamma_correlated-1].lorentz
            sigma = self.peakArr[sigma_correlated-1].gaussian
            A = self.peakArr[amp_correlated-1].amp
            asym = self.peakArr[n].asymmetry
            singlet = self.peakArr[n].is_singlet
            coster_kronig = self.peakArr[n].is_coster_kronig
            branch = self.peakArr[n].branching_ratio
            split = self.peakArr[n].spinOrbitSplit
           
            yFit += self.bkgnArr[i].getY(x,y, PE , width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split,self.scale_var) #This is where backgrounds are actually calculated --> Is Shirley taking into account the multiple peaks??

            if backgrounds[i] == 'Shirley-Sherwood':
                n += 1
       
        return yFit
    def get(self):
        """
        Get the whole set
        """
        return (self.peakArr + self.bkgnArr)


    def get_params(self, for_output_file = False):
        params = []
        #fetches all the params as independent lists
       
        for i in range(len(self.peakArr)):
            params.append(self.peakArr[i].get(for_output_file)) #WHAT IS FOR_OUTPUT_FILE???
        for i in range(len(self.bkgnArr)):
            params.append(self.bkgnArr[i].get())

        #puts it in one array
        for i in range(1,len(params)):
            for k in range(len(params[i])):
                params[0].append(params[i][k])

        #print("Params : " + str(params[0]))
        return params[0]

    def get_peak(self,i):
        return self.peakArr[i].get()

    def get_peaks(self):
        return self.peakArr

    def get_background(self,i):
        return self.bkgnArr[i]
    def get_backgrounds(self):
        return self.bkgnArr

    def mutate_(self,chance):
        for peak in self.peakArr:
            peak.mutate(chance)
        for bkgn in self.bkgnArr:
            bkgn.mutate(chance)

    #forces a given peak to have the given values, returns 0 on success, -1 on failure
    def setPeak(self,i,param_arr):

        #param array comes in with its last element indicating its type
        peakType = param_arr[len(param_arr)-1]
        #if param_array is voigt, it comes in form [PE,Gauss,Lorentz,Amplitude,'Voigt']
        if peakType.lower() == 'voigt': #Idk if this is important or now???
            self.peakArr[i].set_voigt(param_arr)
            return 0
        elif peakType.lower() == 'double lorentzian':
            self.peakArr[i].set_doubleLorentz(param_arr)
            return 0
        elif peakType.lower() == 'gaussian':
            self.peakArr[i].set_gauss(param_arr)
            return 0
        elif peakType.lower() == 'lorentzian':
            self.peakArr[i].set_lorentz(param_arr)
            return 0
        elif peakType.lower() == 'doniach-sunjic':
            self.peakArr[i].set_doniachSunjic(param_arr)
            return 0
        else:
            
            return -1

    def setBkgn(self,i,param_arr):
        bkgnType = param_arr[len(param_arr)-1]
        #if param_array is voigt, it comes in form [PE,Gauss,Lorentz,Amplitude,'Voigt']
        if bkgnType.lower() == 'shirley-sherwood':
            self.bkgnArr[i].set_shirley_sherwood(param_arr)

    def verbose(self):
        """
        Print out the Populations
        """
        for i in range(self.npaths):
            self.Population[i].verbose()
