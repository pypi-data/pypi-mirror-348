"""
Created 7/5/23
File is a copy of xes_individual in the GA folder, but with some modifications to make it work with xes analysis file:
-Evan Restuccia (evan@restuccias.com)
"""
from tkinter import N

from matplotlib.bezier import get_parallels
from xes_neo.gui.xes_fit import peak,background

class Individual():
    """
    The Individual holds all peaks and backgrounds in the self.peakArr and self.bkgnArr
    (SVSC/peak shirley backgrounds are stored in each peak class)
    The arrays are populated individually and then used to manage and compile all factors external to each
    component of the fit.
    Generally, an individual is a fit in its entirety.

    get_params() will get all fit parameters
    mutate_() will mutate the entire fit
    """
    def __init__(self,backgrounds,peaks,scale_var,pars_range=''):
        """
        backgrounds (array) Array where each element is the name of the background type desired
        peaks (array) array where each element is the name of the desired peakType
        pars_range (dict) each key is the name of a parameter with a tuple that contains the range the parameter is allowed to explore

        """
        self.scale_var = scale_var
        self.SVSC_toggle = False
        self.pars_range = pars_range

        #both peaks and backgrounds are arrays of strings which represent the type of the background of the peak/bkgn
        self.nPeaks = len(peaks)
        self.nBackgrounds = len(backgrounds)
        self.peakArr = [None]* self.nPeaks
        self.bkgnArr = [None] * self.nBackgrounds

        """
        the Photon Energy needs to be personalized
        we take the range, which right now is something like (0,.2), i.e. the allowed variance in PE
        Then we add our photon energy to it to move the range to the right spot

        In the gui folder, we skip this try block, because we plan on custom setting these values later, and use a dummy paramRange of ''
        """
        if 'SVSC_shirley' in backgrounds:
            self.SVSC_toggle = True
            self.bkgnArr = [None] * (self.nBackgrounds-1)
        else:
            self.SVSC_toggle = False

        #print(self.peakArr)
        
        
        #I dont think we need this:
        if pars_range != '':
            pars_range['Photon Energy'][0],pars_range['Photon Energy'][1] = PE1,PE2
            pars_range['spinOrbitSplitting'][0],pars_range['spinOrbitSplitting'][1] = SOS1,SOS2
            pars_range['Gaussian'][0],pars_range['Gaussian'][1] = S1,S2
            pars_range['Lorentzian'][0],pars_range['Lorentzian'][1] = G1,G2
            pars_range['Amplitude'][0],pars_range['Amplitude'][1] = A1,A2
            pars_range['Lorentzian Coster-Kronig'][0],pars_range['Lorentzian Coster-Kronig'][1] = CK1,CK2
            

        
    

        for i in range(self.nPeaks):
            #self.peakArr[i] = peak(pars_range,peaks[i])
          
            self.peakArr[i] = peak(pars_range,peaks[i])

            if self.SVSC_toggle:
                self.peakArr[i].SVSC_toggle(True)
        '''
        j=0
        for i,bkgn in enumerate(backgrounds):
            #print(bkgn)
            if bkgn.lower() == 'svsc_shirley':
                #print("Pass")
                j+=1
                pass
            else:
                self.bkgnArr[i-j] = background(pars_range,bkgn, peaks[i])
        '''
        #each index in the peaks/background array is the name of the peak/background type to be used
        k=0
        n=0
        

        for i in range(self.nBackgrounds):
            if backgrounds[i] == 'SVSC_shirley':
                self.nBackgrounds -=1
                pass
            elif backgrounds[i] == 'Shirley-Sherwood':

                self.bkgnArr[k] = background(pars_range,backgrounds[i], peaks[n]) #Creating a unique shirley background for each peak...I think

                k +=1
                n +=1

            else:

                #n = 0 #Doesn't matter which peak we are looking at --> Only matters in Shirley case
                self.bkgnArr[k] = background(pars_range,backgrounds[i], peaks[n])

                k+=1




    def add_peak(self,peakType):
        self.peakArr.append(peak(self.pars_range,peakType))
       
           
    def add_bkgn(self,bkgnType):
        self.bkgnArr.append(background(self.pars_range,bkgnType))


    #adds all backgrounds and peaks as one y value array
    def getFit(self,x,y, peakType, backgrounds):
        
        yFit = [0]*len(x)

        for i in range(self.nPeaks):
           
            if(peakType == "Doniach-Sunjic"):
                asymD = self.peakArr[i].asymmetryDoniach
            else:
                asymD = 0
            PE = self.peakArr[i].photonEnergy
            width = self.peakArr[i].lorentz
            sigma = self.peakArr[i].gaussian
            A = self.peakArr[i].amp
            asym = self.peakArr[i].asymmetry
            singlet = self.peakArr[i].is_singlet
            coster_kronig = self.peakArr[i].is_coster_kronig #I do not know why but this is not taking in the correct bool statement for Coster-Kronig, only takes in init value in xes_fit gui
          
            if coster_kronig == True:
                width_CK = self.peakArr[i].lorentz_CK
            else:
                width_CK = self.peakArr[i].lorentz
            branch = self.peakArr[i].branching_ratio
            split = self.peakArr[i].spinOrbitSplit

            #asymD = self.peakArr[i].asymmetryDoniach
            if self.SVSC_toggle:
                peak_y,svsc_y = self.peakArr[i].getY(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)
                yFit += peak_y
                yFit += svsc_y
            else:
                yFit += self.peakArr[i].getY(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)

        n = 0
        for i in range(self.nBackgrounds):

           
            if(peakType == "Doniach-Sunjic"):
                asymD = self.peakArr[i].asymmetryDoniach
            else:
                asymD = 0
            PE = self.peakArr[n].photonEnergy
            width = self.peakArr[n].lorentz
            sigma = self.peakArr[n].gaussian
            A = self.peakArr[n].amp
            asym = self.peakArr[n].asymmetry
            singlet = self.peakArr[n].is_singlet
            coster_kronig = self.peakArr[n].is_coster_kronig
            if coster_kronig == True:
                width_CK = self.peakArr[n].lorentz_CK
            else:
                width_CK = self.peakArr[n].lorentz
            branch = self.peakArr[n].branching_ratio
            split = self.peakArr[n].spinOrbitSplit
           
            
            yFit += self.bkgnArr[i].getY(x,y, PE , width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split, self.scale_var) #ISSUE COMES FROM HERE --> NOT SEEING THE self.photonEnergy or self.lorentz VALUES

            if backgrounds[i] == 'Shirley-Sherwood':
                n += 1

        return yFit

    def getFWHM(self,x, peakType):
        FWHM = [0]*self.nPeaks
        for i in range(self.nPeaks):
            if(peakType == "Doniach-Sunjic"):
                asymD = self.peakArr[i].asymmetryDoniach
            else:
                asymD = 0
            PE = self.peakArr[i].photonEnergy
            width = self.peakArr[i].lorentz
            sigma = self.peakArr[i].gaussian
            A = self.peakArr[i].amp
            asym = self.peakArr[i].asymmetry
            singlet = self.peakArr[i].is_singlet
            coster_kronig = self.peakArr[i].is_coster_kronig
            if coster_kronig == True:
                width_CK = self.peakArr[i].lorentz_CK
            else:
                width_CK = self.peakArr[i].lorentz
            branch = self.peakArr[i].branching_ratio
            split = self.peakArr[i].spinOrbitSplit
            FWHM[i] = self.peakArr[i].getFWHM(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)

        return FWHM





    def getFitWithComponents(self,x,y, peakType, backgrounds):
        """
        gets fit and also returns all the components that make up the fit
        """
        yFit = [0]*len(x)
        #print(self.peakArr)
        bkgn_components_arr = []
        peak_components_arr = []
        for i in range(self.nPeaks):
            PE = self.peakArr[i].photonEnergy
            width = self.peakArr[i].lorentz
            sigma = self.peakArr[i].gaussian
            A = self.peakArr[i].amp
            asym = self.peakArr[i].asymmetry
            singlet = self.peakArr[i].is_singlet
            coster_kronig = self.peakArr[i].is_coster_kronig
            if coster_kronig == True:
                width_CK = self.peakArr[i].lorentz_CK
            else:
                width_CK = self.peakArr[i].lorentz
            branch = self.peakArr[i].branching_ratio
            split = self.peakArr[i].spinOrbitSplit

            if(peakType == "Doniach-Sunjic"):
                asymD = self.peakArr[i].asymmetryDoniach
            else:
                asymD = 0

            if self.SVSC_toggle:
                peakComp,svsc =  self.peakArr[i].getY(x)
                yFit += peakComp
                yFit += svsc
                bkgn_components_arr.append(svsc)
                peak_components_arr.append(peakComp)

            else:

                peakComp =  self.peakArr[i].getY(x, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split)
                yFit += peakComp

                peak_components_arr.append(peakComp)

        n = 0
        total_bkgn = [0]*len(x)
        total_bkgn = [0]*len(x)
        for i in range(self.nBackgrounds):


            if(peakType == "Doniach-Sunjic"):
                asymD = self.peakArr[i].asymmetryDoniach
            else:
                asymD = 0
            PE = self.peakArr[n].photonEnergy
            width = self.peakArr[n].lorentz
            sigma = self.peakArr[n].gaussian
            A = self.peakArr[n].amp
            asym = self.peakArr[n].asymmetry
            singlet = self.peakArr[n].is_singlet
            coster_kronig = self.peakArr[n].is_coster_kronig
            if coster_kronig == True:
                width_CK = self.peakArr[n].lorentz_CK
            else:
                width_CK = self.peakArr[n].lorentz
            branch = self.peakArr[n].branching_ratio
            split = self.peakArr[n].spinOrbitSplit
            bkgnComp = self.bkgnArr[i].getY(x,y, PE, width, sigma, A, asym, asymD, singlet, coster_kronig, width_CK, branch, split,self.scale_var)

            yFit += bkgnComp
            bkgn_components_arr.append(bkgnComp)
            if backgrounds[i] == 'Shirley-Sherwood':
                n += 1

        #print("BACKGROUND SUM =", net_background)
                n += 1

        #print("BACKGROUND SUM =", net_background)
        #inefficient but only needs to work a few times so it should be fine
        for i in range(len(peak_components_arr)):
            for l in range(len(bkgn_components_arr)):
                for k in range(len(x)):
                    peak_components_arr[i][k] += bkgn_components_arr[l][k]


        for i in range(len(bkgn_components_arr)):
            for j in range(len(y)):
                total_bkgn[j] += bkgn_components_arr[i][j]
        net_bkgn_left = []
        net_bkgn_right = []
        for i in range(30):
            net_bkgn_left.append(total_bkgn[i] - y[i])

        for i in range(len(y)-1, len(y)-30, -1):
            net_bkgn_right.append(total_bkgn[i] - y[i])
        #Create some kind of check to see if this value is negative or if its positive value is above %*average_left_&_right of y
        #print("NET BACKGROUND DIFFERENCE LEFT", sum(net_bkgn_left)/len(net_bkgn_left))
        #print("NET BACKGROUND DIFFERENCE RIGHT", sum(net_bkgn_right)/len(net_bkgn_right))





        for i in range(len(bkgn_components_arr)):
            for j in range(len(y)):
                total_bkgn[j] += bkgn_components_arr[i][j]
        net_bkgn_left = []
        net_bkgn_right = []
        for i in range(30):
            net_bkgn_left.append(total_bkgn[i] - y[i])

        for i in range(len(y)-1, len(y)-30, -1):
            net_bkgn_right.append(total_bkgn[i] - y[i])
        #Create some kind of check to see if this value is negative or if its positive value is above %*average_left_&_right of y
        #print("NET BACKGROUND DIFFERENCE LEFT", sum(net_bkgn_left)/len(net_bkgn_left))
        #print("NET BACKGROUND DIFFERENCE RIGHT", sum(net_bkgn_right)/len(net_bkgn_right))



        return yFit,peak_components_arr,bkgn_components_arr

    def get(self):
        """
        Get the whole set
        """
        
        return (self.peakArr + self.bkgnArr)

    def get_params(self,is_coster_kronig):
        params = []
       
        
        for i in range(len(self.peakArr)):
            params.append(self.peakArr[i].get(is_coster_kronig[i]))
        
        #print(self.bkgnArr[1].get(), "HELLO")
        #print(self.bkgnArr[1].get(), "HELLO")
        for i in range(len(self.bkgnArr)):
            params.append(self.bkgnArr[i].get())
        return params

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


    def verbose(self):
        """
        Print out the Populations
        """
        for i in range(self.npaths):
            self.Population[i].verbose()

    ''' Could be useful later I just dont want to write it
    def set_peak(self,i,A,h_f,m):
        self.Population[i].set(A,h_f,m)
    '''
