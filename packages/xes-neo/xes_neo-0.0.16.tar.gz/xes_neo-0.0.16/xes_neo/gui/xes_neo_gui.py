"""
Authors     Alana Humiston, Megan Burrill, Miu lun lau
Email       athompson9@hawk.iit.edu, mburrill@hawk.iit.edu, andylau@u.boisestate.edu
Version     0.0.16
Date        4, 18, 2025
"""

"""
TODO
- analysis [Done]
- improve graphing
- preprocessing?
- connect calibration to nano-indent
"""
#Testing to see if I can push with other computer
from tkinter import *
from threading import Thread
from tkinter import ttk, Tk, N, W, E, S, StringVar, IntVar, DoubleVar, BooleanVar, Checkbutton, NORMAL, DISABLED, \
    scrolledtext, filedialog, messagebox, LabelFrame, Toplevel, END, TOP
from tkinter.font import Font
from tokenize import Double

# import matplotlib
import matplotlib
from matplotlib.hatch import HorizontalHatch
import numpy as np
import configparser


matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
# from threading import *
# import os
import os, subprocess, asyncio
import signal
import pathlib
import multiprocessing as mp
# custom Libraries
from xes_neo.gui.xes_plot import Data_plot, Analysis_plot
#import preprocess_data
import xes_neo.gui.xes_data as data
import xes_neo.gui.xes_analysis2
from xes_neo.periodic_table import ElementData
#from uncertainties import ufloat



class App():
    """
    Start of the application
    """

    def __init__(self):
        self.__version__ = 0.1
        self.root = Tk(className='XES Neo GUI')
        self.root.wm_title("XES GUI (Beta)")
        self.root.geometry("1100x750") #Changed size from 975x650 to 1100x750
        self.mainframe = ttk.Notebook(self.root, padding='5')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S), columnspan=5)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(True, True)
        self.padx = 5
        self.pady = 3

        # Specify standard font
        self.entryFont = Font(family='TkTextFont', size=10) #Changed from 11
        self.labelFont = Font(family='TkMenuFont', size=10) # Changed from 11
        s = ttk.Style()
        # s.configure('my.TButton', font=labelFont)

        # Set multiprocessing run type
        mp.set_start_method('spawn')

        # initialize variables
        self.initialize_var()
        self.initialize_tabs()
        self.build_tabs()

    def initialize_var(self):
        """
        Initalize all possible variables in the GUI
        """
        # Inputs (column 0)
        # Averaging Section of Input Tab:
        self.all_files_display = StringVar(self.root, 'Please choose file/s')  #Files that you want to average
        self.all_files = np.array([])
        self.averaged_file = StringVar(self.root, 'Please choose file/s') #File to save the averaged data to
        self.num_files = DoubleVar(self.root, 0) #Number of files to be averaged after selection
        self.num_points = DoubleVar(self.root, 0) #Number of points in each data file
        self.xPoints_for_data_plot = np.array([])
        self.yPoints_for_data_plot = np.array([])
        self.xPoints_avg = np.array([]) #Averaged x points for plotting
        self.yPoints_avg = np.array([]) #Averaged y points for plotting
        self.plot_data = np.array([],[])

        # There is a string var to give the prompt on selection, then a path saved to allow easier and safer manipulation
        self.csv_file = StringVar(self.root, "Please choose a data file")
        self.csv_generate_from = pathlib.Path()
        self.file_name = "Data file"
        self.csv_folder = StringVar(self.root, "Please choose a folder containing data files")
        self.csv_folder_path = pathlib.Path()
        self.output_folder = StringVar(self.root, 'Please choose a folder to save outputs')
        self.output_folder_path = pathlib.Path()
        self.output_file = pathlib.Path()
        #File reading options
        self.skipLn = StringVar(self.root,"0")
        self.scale_var = BooleanVar(self.root,"False")

        #Adding in fit file selection to input variables used in previous fitting process
        self.fit_file = StringVar(self.root, "Load in fit file information")
        self.fit_generate_from = pathlib.Path()
        self.fit_file_name = "Data file"
        self.fit_file_selected = False
        #self.fit_peak_number = 1

        self.poly1_value = ''
        self.poly2_value = ''
        self.poly3_value = ''
        self.toug2_value = ''
        self.toug3_value = ''
        self.linear_value = ''
        self.exp_value = ''
        self.shirley_value = ''


        # Waiting to create path variable for calibration because I think it will be deleted
        #self.csv_calibration_file = StringVar(self.root, "Please choose a calibration file") #--------------Will need to comment out-----------
        self.yes_folder = IntVar()
        self.multi_known = BooleanVar(value =False)
        self.multi_known = False  # This will change to true when the user has already said if they do/do not want to generate/run multiple files in the folder so generate ini does nto keep asking
        self.filelist = []
        self.command_list = mp.Queue()
        self.proc_list = []
        self.pid_list = []
        # Preprocessing
        self.preprocess_file = pathlib.Path()
        self.stop_not_pressed = True

        # Variables for the dropdown menu
        self.file_menu = ttk.Combobox()
        self.data_obj = 0



        # Populations (column 2)
        self.population = IntVar(self.root, 2000)
        self.num_gen = IntVar(self.root, 10)
        self.best_sample = IntVar(self.root, 20)
        self.lucky_few = IntVar(self.root, 10)

        # Mutations (column 3)
        self.chance_of_mutation = IntVar(self.root, 20)
        self.original_chance_of_mutation = IntVar(self.root, 20) #I dont think this is being used anywhere
        self.mutated_options = IntVar(self.root, 0)

        # Fitting parameters(column 4)

        #New XES parameters
        #how to make unique for each peak?
        self.number_of_peaks = DoubleVar(self.root, 1)
        self.element_select = []
        self.photoLine_select = []
        self.transitionLine_select = []
        self.PE_guesses = []
        self.sigma_guesses = []
        self.gamma_guesses = []
        self.amp_guesses = []
        self.so_split = []


        self.PE_up_lim = []
        self.PE_low_lim = []
        self.PE_limit = []
        self.PE_corr = []
        self.PE_corr_mult = []

        self.sigma_up_lim = []
        self.sigma_low_lim = []
        self.sigma_limit = []
        self.sigma_corr = []
        self.sigma_corr_mult = []

        self.gamma_up_lim = []
        self.gamma_low_lim = []
        self.gamma_limit = []
        self.gamma_corr = []
        self.gamma_corr_mult = []

        self.amp_up_lim = []
        self.amp_low_lim = []
        self.amp_limit = []
        self.amp_corr = []
        self.amp_corr_mult = []

       


        for i in range(10):
            self.sigma_guesses.append(DoubleVar(self.root, 1.0))
            self.gamma_guesses.append(DoubleVar(self.root, 1.0))
            self.amp_guesses.append(DoubleVar(self.root, 500))
            self.PE_guesses.append(DoubleVar(self.root, 284.50))
            self.so_split.append(DoubleVar(self.root, 0.00))
            
            self.PE_up_lim.append(DoubleVar(self.root, 0.25))
            self.PE_low_lim.append(DoubleVar(self.root, -0.25))
            self.sigma_up_lim.append(DoubleVar(self.root, 0.25))
            self.sigma_low_lim.append(DoubleVar(self.root, -0.25))
            self.gamma_up_lim.append(DoubleVar(self.root, 0.25))
            self.gamma_low_lim.append(DoubleVar(self.root, -0.25))
            self.amp_up_lim.append(DoubleVar(self.root, 100))
            self.amp_low_lim.append(DoubleVar(self.root, -100))
           

        self.peaks = []
        self.path_branching = []
        self.peak_singlet = []
        self.peak_coster_kronig = []
        self.data_KE = False
        self.data_XES = True
        self.data_peak_add = BooleanVar(self.root, False)
        for i in range(10):
            self.peaks.append(StringVar(self.root, "Select a peak type"))
            self.element_select.append(StringVar(self.root, " "))
            self.photoLine_select.append(StringVar(self.root, " "))
            self.transitionLine_select.append(StringVar(self.root, " "))
            self.path_branching.append(DoubleVar(self.root, 0.5))
            self.peak_singlet.append(BooleanVar(self.root, True))
            self.peak_coster_kronig.append(BooleanVar(self.root, False))
            


            self.PE_limit.append(BooleanVar(self.root, False))
            self.PE_corr.append(StringVar(self.root, "Peak #"))
            self.PE_corr_mult.append(DoubleVar(self.root, 1.0))

            self.sigma_limit.append(BooleanVar(self.root, False))
            self.sigma_corr.append(StringVar(self.root, "Peak #"))
            self.sigma_corr_mult.append(DoubleVar(self.root, 1.0))

            self.gamma_limit.append(BooleanVar(self.root, False))
            self.gamma_corr.append(StringVar(self.root, "Peak #"))
            self.gamma_corr_mult.append(DoubleVar(self.root, 1.0))

            self.amp_limit.append(BooleanVar(self.root, False))
            self.amp_corr.append(StringVar(self.root, "Peak #"))
            self.amp_corr_mult.append(DoubleVar(self.root, 1.0))


            #self.data_KE.append(BooleanVar(self.root, False))
        self.background_types = []
        #self.path_bkgn = StringVar(self.root, "Select a background type") #Dont think we need anymore because we want to use an array now
        #self.path_branching = StringVar(self.root, "Select branching ratio")

        self.spinOrbitSplit_min, self.spinOrbitSplit_max, self.spinOrbitSplit_delta = -0.2, 0.2, 0.01
        self.gamma_CK_min, self.gamma_CK_max, self.gamma_CK_delta = -0.13, 0.43, 0.01 #allow coster-kronig to be much wider
        self.PE_min,self.PE_max,self.PE_delta = -0.5,0.5,.01
        #self.sigma_min,self.sigma_max,self.sigma_delta = 0,2,.001
        #self.fwhm_min,self.fwhm_max,self.fwhm_delta = 0,0.5,.001
        #self.amp_min,self.amp_max,self.amp_delta = 0,5000, 0.05 #Was 0-5000: arbitrary. Max set in xes.py

        #GOING TO GET RID OF THESE PARAMETERS: INSTEAD HAVE THE PARAMETER RANGES TAB
        
        #Changed sigma, gamma, and amp to pe user inputs. The ranges are now selected the same way as PE --> This is done in the individual tab
        self.sigma_min,self.sigma_max,self.sigma_delta = -0.13,0.13,.01 #changed from +/- 0.13
        self.fwhm_min,self.fwhm_max,self.fwhm_delta = -0.13,0.13,.01
        self.amp_min,self.amp_max,self.amp_delta = -500,500, 0.5
        self.asymmetry_min,self.asymmetry_max,self.asymmetry_delta = 1.0,5.0, 0.01 #NEED TO ADD IN LIMIT BUTTON
        self.asymmetryDoniach_min,self.asymmetryDoniach_max,self.asymmetryDoniach_delta = 0, 1, 0.01 #Doniach Sunjic asymmetry
        self.C_min, self.C_max, self.C_delta = 1, 1000, 1 #For Tougaard 3 Parameter. May need to change range to be bigger
        self.D_min, self.D_max, self.D_delta = 1, 20000, 1 #For Tougaard 3 Parameter. May need to change range to be bigger. Some D as big as 13300...User input?
        self.background_min,self.background_max,self.background_delta = 0,5000,0.05 #Max set in xes.py
        #self.background_shir_min,self.background_shir_max,self.background_shir_delta = 0,5000,0.05 #Max set in xes.py
        self.slope_min,self.slope_max,self.slope_delta = 0,5, 0.0001 #Max AND Min set in xes.py
        self.slope_min,self.slope_max,self.slope_delta = 0,5, 0.0001 #Max AND Min set in xes.py
        self.exp_amp_min, self.exp_amp_max, self.exp_amp_delta = 0.01, 9.99, 0.01 #New parameters for exponential background
        self.exp_decay_min, self.exp_decay_max, self.exp_decay_delta = 0, 1, 0.01
       #need to make background a checkButton not a picker
       #need to make a checkButton for Doublet vs. Singlet --> diable so_split and path_branching

        # Graph (column 5)
        self.print_graph = BooleanVar(self.root, False)
        self.num_output_paths = BooleanVar(self.root, True)
        self.steady_state_exit = BooleanVar(self.root, True)

        # Output tab (column 6)
        self.print_graph = BooleanVar(self.root, False)
        self.num_output_paths = BooleanVar(self.root, True)
        self.steady_state_exit = BooleanVar(self.root, True)
        self.n_ini = IntVar(self.root, 100)
        self.pop_min = IntVar(self.root, 100)
        self.pop_max = IntVar(self.root, 5001)
        self.gen_min = IntVar(self.root, 20)
        self.gen_max = IntVar(self.root, 501)
        self.mut_min = IntVar(self.root, 20)
        self.mut_max = IntVar(self.root, 51)
        self.run_folder = BooleanVar(self.root, False)
        self.pertub_check = IntVar(self.root, 0)
        self.checkbutton_whole_folder = ttk.Checkbutton()

        self.analysis_dir = StringVar(self.root, "Please choose a data file")
        # Analysis (column 7)
        # I don't know what goes here so leave blank instead

    def initialize_tabs(self):
        """
        Initialize tabs for the main frame
        """
        s = ttk.Style()
        s.configure('TNotebook.Tab', font=('TkHeadingFont', '11'))
        height = 1
        # Creating tabs
        self.input_tab = ttk.Frame(self.mainframe, height=height)
        self.population_tab = ttk.Frame(self.mainframe, height=height)
        #self.calibration_tab = ttk.Frame(self.mainframe, height=height)
        self.mutation_tab = ttk.Frame(self.mainframe, height=height)
        self.periodicTable_tab = ttk.Frame(self.mainframe, height=height) #New tab. Going to replace Fitting Parameters tab in the future
        self.fitting_param_tab = ttk.Frame(self.mainframe, height=height)
        self.param_range_tab = ttk.Frame(self.mainframe, height=height)
        self.graph_tab = ttk.Frame(self.mainframe, height=height)
        self.output_tab = ttk.Frame(self.mainframe, height=height)
        self.analysis_tab = ttk.Frame(self.mainframe, height=height)

        # Adding tabs
        self.mainframe.add(self.input_tab, text="Inputs")
        self.mainframe.add(self.population_tab, text='Populations')
        self.mainframe.add(self.mutation_tab, text="Mutations")
        self.mainframe.add(self.periodicTable_tab, text="Element Selection") 
        self.mainframe.add(self.fitting_param_tab, text="Fitting Parameters")
        self.mainframe.add(self.param_range_tab, text= "Parameter Ranges")
        self.mainframe.add(self.graph_tab, text="Plots")
        self.mainframe.add(self.output_tab, text="Output")
        self.mainframe.add(self.analysis_tab, text="Analysis")

    def build_tabs(self):
        """
        Build tabs. Will call function for each tab
        """
        self.build_global()
        self.build_inputs_tab()
        self.build_population_tab()
        self.build_mutations_tab()
        self.build_periodicTable_tab() 
        self.build_fitting_param_tab()
        self.build_param_range_tab()
        self.build_plot_tab()
        self.build_output_tab()
        self.build_analysis_tab()

        self.mainframe.grid_rowconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_rowconfigure(2, weight=1)
        self.mainframe.grid_columnconfigure(3, weight=1)
        self.mainframe.grid_columnconfigure(4, weight=1)

    def description_tabs(self, arr, tabs, sticky=(W, E), row=None, column=None, return_description=False):
        # Rows = index of rows
        # Loops through array of descriptors to be added to the tabs
        description_list = []
        if row is not None:
            assert len(row) == len(arr)
        for i, inputs in enumerate(arr):
            entry = ttk.Label(tabs, text=inputs, font=self.labelFont)
            if row is not None:
                k = row[i]
            else:
                k = i
            entry.grid_configure(column=column, row=k, sticky=sticky, padx=self.padx, pady=self.pady)
            description_list.append(entry)
        if description_list:
            return description_list
        

    def description_tabs_column(self, arr, tabs, sticky=(W, E), row=None, column=None, return_description=False):
        # Rows = index of rows
        # Loops through array of descriptors to be added to the tabs
        description_list = []
        if column is not None:
            assert len(column) == len(arr)
        for i, inputs in enumerate(arr):
            entry = ttk.Label(tabs, text=inputs, font=self.labelFont)
            if column is not None:
                k = column[i]
            else:
                k = i
            entry.grid_configure(column=k, row=row, sticky=sticky, padx=self.padx, pady=self.pady)
            description_list.append(entry)
        if description_list:
            return description_list


    # When the user selects a particular file from the input directory in the dropdown menu it will be assigned to the
    # csv generate from variable so that it is used for running
    def file_selected(self, event):
        self.csv_generate_from = pathlib.Path(self.csv_folder_path.joinpath(self.file_menu.get()))
        # print("file selected: ", self.csv_generate_from)

    # Writes the ini file to filename using the user inputs or defaults if nothing is changed
    def write_ini(self, filename):
        # First select data range
        # preprocess_data.read_files(self.csv_generate_from, limits=(self.percent_min.get(), self.percent_max.get()))
        # self.preprocess_file = pathlib.Path.cwd().joinpath('example.txt')

        # print("write ini csv path generate from", str(self.csv_generate_from))
        inputs = ("[Inputs]\ndata_file = {data}\noutput_file = {out} \nskipln = {skipLn}"
                  "".format(
            data=str(self.csv_generate_from),
            out=str(self.output_file),
            skipLn = str(self.skipLn.get()),
        
            #calibration=str(self.csv_calibration_file.get()),#deleted: calibration=str(self.csv_calibration_file.get())
            #dat_cutoff=", ".join(str(i) for i in [self.percent_min.get(), self.percent_max.get()])
        ))
        populations = ("\n\n[Populations]\npopulation = {pop}\nnum_gen = {numgen}\nbest_sample = {best} "
                       "\nlucky_few = {luck}".format(pop=str(self.population.get()),
                                                     numgen=str(self.num_gen.get()),
                                                     best=str(self.best_sample.get()),
                                                     luck=str(self.lucky_few.get())))
        # Sends range for power law equation as [min, max]

        elements = []
        photoelectronLines = []
        transitionLines = []
        guesses = []
        PE_guess_min = []
        PE_guess_max = []
        PE_guess_delta = []
        PE_guesses_range = []
        sigma_guesses = []
        gamma_guesses = []
        amp_guesses = []
        amp_guess_min = []
        amp_guess_max = []
        amp_guess_delta = []
        amp_guesses_range = []
        so_guesses = []
        inputPeaks = []
        inputBranching = []
        inputSinglet = []
        inputCK = []
        #inputKE = []
        sigma_guess_delta = []
        gamma_guess_delta = []

        PE_up_lim = []
        PE_low_lim = []
        PE_limit = []
        PE_corr = []
        PE_corr_mult = []

        sigma_up_lim = []
        sigma_low_lim = []
        sigma_limit = []
        sigma_corr = []
        sigma_corr_mult = []

        gamma_up_lim = []
        gamma_low_lim = []
        gamma_limit = []
        gamma_corr = []
        gamma_corr_mult = []

        amp_up_lim = []
        amp_low_lim = []
        amp_limit = []
        amp_corr = []
        amp_corr_mult = []

       
        #Default values if none are selected in periodic table tab (These have no meaning right now)
        
        global element
        global photoelectronLine
        global transitionLine
        try:
            element
        except NameError:
            print("Element Not Selected")
            element =[]
            for i in range(int(self.number_of_peaks.get())):
                element.append('N/s')
        
        try:
            photoelectronLine
        except NameError:
            print("Absorption Edge Not Selected")
            photoelectronLine = []
            for i in range(int(self.number_of_peaks.get())):
                photoelectronLine.append('N/s')

        try:
            transitionLine
        except NameError:
            #print("Absorption Edge Not Selected. Defaulting to K edge")
            transitionLine = []
            for i in range(int(self.number_of_peaks.get())):
                transitionLine.append('N/s')
        
       
     
        for i in range(int(self.number_of_peaks.get())):

            elements.append(element[i])
            photoelectronLines.append(photoelectronLine[i])
            transitionLines.append(transitionLine[i])
            guesses.append(self.PE_guesses[i].get())
            PE_min = -0.5 #Initially set ranges to +/- 0.5 eV from input value --> This is changed in xes.py
            PE_max = 0.5
            PE_guess_min.append(PE_min)
            PE_guess_max.append(PE_max)
            PE_guess_delta.append(0.01)
            PE_guesses_range.append([PE_min, PE_max, 0.01])
            sigma_guesses.append(self.sigma_guesses[i].get())
            gamma_guesses.append(self.gamma_guesses[i].get())
            amp_guesses.append(self.amp_guesses[i].get())
            amp_min = float(self.amp_guesses[i].get())*-0.10 #AMP range set to +/-10% of input value --> This is larger if baseline is large
            amp_max = float(self.amp_guesses[i].get())*0.10
            amp_guess_min.append(amp_min)
            amp_guess_max.append(amp_max)
            amp_guess_delta.append(0.5)
            amp_guesses_range.append([amp_min, amp_max, 0.5])
            so_guesses.append(self.so_split[i].get())
            inputPeaks.append(self.peaks[i].get())
            inputBranching.append(self.path_branching[i].get())
            inputSinglet.append(self.peak_singlet[i].get())
            inputCK.append(self.peak_coster_kronig[i].get())
            sigma_guess_delta.append(0.001)
            gamma_guess_delta.append(0.001)
          
            PE_up_lim.append(self.PE_up_lim[i].get())
            PE_low_lim.append(self.PE_low_lim[i].get())
            PE_limit.append(self.PE_limit[i].get())
            PE_corr.append(self.PE_corr[i].get())
            PE_corr_mult.append(self.PE_corr_mult[i].get())

            sigma_up_lim.append(self.sigma_up_lim[i].get())
            sigma_low_lim.append(self.sigma_low_lim[i].get())
            sigma_limit.append(self.sigma_limit[i].get())
            sigma_corr.append(self.sigma_corr[i].get())
            sigma_corr_mult.append(self.sigma_corr_mult[i].get())

            gamma_up_lim.append(self.gamma_up_lim[i].get())
            gamma_low_lim.append(self.gamma_low_lim[i].get())
            gamma_limit.append(self.gamma_limit[i].get())
            gamma_corr.append(self.gamma_corr[i].get())
            gamma_corr_mult.append(self.gamma_corr_mult[i].get())

            amp_up_lim.append(self.amp_up_lim[i].get())
            amp_low_lim.append(self.amp_low_lim[i].get())
            amp_limit.append(self.amp_limit[i].get())
            amp_corr.append(self.amp_corr[i].get())
            amp_corr_mult.append(self.amp_corr_mult[i].get())

    
        peak_add_remove = self.data_peak_add
       
           #inputKE.append(self.data_KE[i].get())
        #print("PE UP", PE_up_lim, "PE LOW", PE_low_lim, "PE LIMIT", PE_limit, "PE CORR", PE_corr, )
        #print(amp_guesses_range)



        #\nspinOrbitSplit_range = {spinOrbitSplit_range}
        paths = ("\n\n[Paths]\nnPeaks={nPeaks} \nbackground_type = {bkgn_type} \npeak_type = {peak_type} \nbranching_ratio = {branching_ratio} \ngamma_CK_range = {gamma_CK_range} \ngamma_CK_guess = {gamma_CK_guess} \nPE_range_min = {PE_range_min} \nPE_range_max = {PE_range_max} \nPE_range_delta = {PE_range_delta} \nPE = {PE} \nPE_limited = {PE_limited} \nPE_correlated = {PE_correlated} \nPE_correlated_mult = {PE_correlated_mult} \nis_singlet = {is_singlet} \nis_coster_kronig = {is_coster_kronig} \nelement_select = {element_select} \nphotoLine_select = {photoLine_select} \ntransitionLine_select = {transitionLine_select} \nspinOrbitSplit_range = {spinOrbitSplit_range} \nspinOrbitSplit = {spinOrbitSplit} \nsigma_range_min = "
                 "{sigma_range_min} \nsigma_range_max = {sigma_range_max} \nsigma_range_delta = {sigma_range_delta} \nsigma_guess = {sigma_guess} \nsigma_limited = {sigma_limited} \nsigma_correlated = {sigma_correlated} \nsigma_correlated_mult = {sigma_correlated_mult} \ngamma_range_min = {gamma_range_min} \ngamma_range_max = {gamma_range_max} \ngamma_range_delta = {gamma_range_delta} \ngamma_guess = {gamma_guess} \ngamma_limited = {gamma_limited} \ngamma_correlated = {gamma_correlated} \ngamma_correlated_mult = {gamma_correlated_mult} \nasymmetry_range = {asymmetry_range} \nasymmetryDoniach_range = {asymmetryDoniach_range} \namp_range_min = {amp_range_min} \namp_range_max = {amp_range_max} \namp_range_delta = {amp_range_delta} \namp_guess = {amp_guess} \namp_limited = {amp_limited} \namp_correlated = {amp_correlated} \namp_correlated_mult = {amp_correlated_mult} \nk_range = {k_range} \nbackground_range = {background_range} \nCTou3_range = {CTou3_range} \nDTou3_range = {DTou3_range} \nslope_range = {slope_range} \nexp_amp_range = {exp_amp_range} \nexp_decay_range = {exp_decay_range} \nscale_bool = {scale_bool} \npeak_adding = {peak_adding}"
                 .format(nPeaks=int(self.number_of_peaks.get()),
                         bkgn_type = ",".join(str(i) for i in self.background_types), #Do we need to get this?
                         #bkgn_type = str(self.path_bkgn.get()),
                         peak_type = ",".join(str(i) for i in inputPeaks),
                         branching_ratio = ", ".join(str(i) for i in inputBranching),
                         gamma_CK_range = ", ".join(str(i) for i in [self.gamma_CK_min, self.gamma_CK_max, self.gamma_CK_delta]),
                         gamma_CK_guess = ", ".join(str(i) for i in gamma_guesses), #Making it the same initial inputs as the regular gamma values
                         #PE_range=", ".join(str(i) for i in [self.PE_min, self.PE_max, self.PE_delta]),
                         PE_range_min =",".join(str(i) for i in PE_low_lim),
                         PE_range_max =",".join(str(i) for i in PE_up_lim), #EDIT SIGMA AND GAMMA TO BE LIKE AMP AND PE IN MIN/MAX RANGE
                         PE_range_delta =",".join(str(i) for i in PE_guess_delta),
                         PE = ", ".join(str(i) for i in guesses),
                         PE_limited = ", ".join(str(i) for i in PE_limit),
                         PE_correlated = ", ".join(str(i) for i in PE_corr),
                         PE_correlated_mult = ", ".join(str(i) for i in PE_corr_mult),
                         is_singlet = ", ".join(str(i) for i in inputSinglet),
                         is_coster_kronig = ", ".join(str(i) for i in inputCK),
                         #is_KE = ", ".join(str(i) for i in inputKE),
                         element_select  = ", ".join(str(i) for i in elements),
                         photoLine_select = ", ".join(str(i) for i in photoelectronLines),
                         transitionLine_select = ", ".join(str(i) for i in transitionLines),
                         spinOrbitSplit_range=", ".join(str(i) for i in [self.spinOrbitSplit_min, self.spinOrbitSplit_max, self.spinOrbitSplit_delta]),
                         spinOrbitSplit = ", ".join(str(i) for i in so_guesses), #Currently the spin-orbit splitting value is being taken as a constant from the user --> Will have to update to be a part of the GA taking info on each element
                         
                         sigma_range_min =",".join(str(i) for i in sigma_low_lim),
                         sigma_range_max =",".join(str(i) for i in sigma_up_lim),
                         sigma_range_delta =",".join(str(i) for i in sigma_guess_delta),

                         #sigma_range=", ".join(str(i) for i in [self.sigma_min, self.sigma_max, self.sigma_delta]),
                         sigma_guess = ", ".join(str(i) for i in sigma_guesses),
                         sigma_limited = ", ".join(str(i) for i in sigma_limit),
                         sigma_correlated = ", ".join(str(i) for i in sigma_corr),
                         sigma_correlated_mult = ", ".join(str(i) for i in sigma_corr_mult),
                         #fwhm_range=", ".join(str(i) for i in [self.fwhm_min, self.fwhm_max, self.fwhm_delta]),

                         gamma_range_min =",".join(str(i) for i in gamma_low_lim),
                         gamma_range_max =",".join(str(i) for i in gamma_up_lim),
                         gamma_range_delta =",".join(str(i) for i in gamma_guess_delta),
                         

                         gamma_guess = ", ".join(str(i) for i in gamma_guesses),
                         gamma_limited = ", ".join(str(i) for i in gamma_limit),
                         gamma_correlated = ", ".join(str(i) for i in gamma_corr),
                         gamma_correlated_mult = ", ".join(str(i) for i in gamma_corr_mult),

                         amp_range_min =",".join(str(i) for i in amp_low_lim),
                         amp_range_max =",".join(str(i) for i in amp_up_lim),
                         amp_range_delta =",".join(str(i) for i in amp_guess_delta),
                         #amp_range =",".join(str(i) for i in [self.amp_min,self.amp_max,self.amp_delta]),
                         amp_guess = ", ".join(str(i) for i in amp_guesses),
                         amp_limited = ", ".join(str(i) for i in amp_limit),
                         amp_correlated = ", ".join(str(i) for i in amp_corr),
                         amp_correlated_mult = ", ".join(str(i) for i in amp_corr_mult),

                         asymmetry_range=",".join(str(i) for i in [self.asymmetry_min, self.asymmetry_max, self.asymmetry_delta]),
                         asymmetryDoniach_range=",".join(str(i) for i in [self.asymmetryDoniach_min,self.asymmetryDoniach_max,self.asymmetryDoniach_delta]),
                         k_range = ", ".join(str(i) for i in [0,0.06,0.001]), 
                         background_range = ", ".join(str(i) for i in [self.background_min, self.background_max, self.background_delta]),
                         #background_shir_range = ", ".join(str(i) for i in [self.background_shir_min, self.background_shir_max, self.background_shir_delta]),
                         CTou3_range=", ".join(str(i) for i in [self.C_min, self.C_max, self.C_delta]),
                         DTou3_range=", ".join(str(i) for i in [self.D_min, self.D_max, self.D_delta]),
                         slope_range = ", ".join(str(i) for i in [self.slope_min, self.slope_max, self.slope_delta]),
                         exp_amp_range = ", ".join(str(i) for i in [self.exp_amp_min, self.exp_amp_max, self.exp_amp_delta]),
                         exp_decay_range = ", ".join(str(i) for i in [self.exp_decay_min, self.exp_decay_max, self.exp_decay_delta]),
                         #per_range=", ".join(str(i) for i in [self.percent_min.get(), self.percent_max.get()]),
                         #nu=self.nu.get()
                         scale_bool = self.scale_var,
                         peak_adding = peak_add_remove
                         ))

        mutations = ("\n\n[Mutations]\nchance_of_mutation = {chance} \noriginal_chance_of_mutation = {original} "
                     "\nmutated_options = {opt}"
                     .format(chance=str(self.chance_of_mutation.get()),
                             original=str(self.original_chance_of_mutation.get()),
                             opt=str(self.mutated_options.get())))
        outputs = ("\n\n[Outputs]\nprint_graph = {graph} \nnum_output_paths = {num} "
                   .format(graph=False, num=False))
        # I have more variables but do not see them in the nano-indent ini and am going to leave for now and see
        # I think I have now deleted the extra variables other than the calibration file
        print(str(inputs))
        with open(filename, 'w') as writer:
            writer.write(str(inputs))
            writer.write(str(populations))
            writer.write(str(mutations))
            writer.write(str(paths))
            writer.write(str(outputs))
        return filename

    def loop_gen_ini_same_params(self):
        """
        Will loop through every file in the selected directory and run it with the same parameters
        """
        # file_list = [file.absolute() for file in self.output_folder_path.glob('**/*.ini') if file.is_file()]
        file_list = [filename for filename in self.csv_folder_path.glob('**/*txt') if filename.is_file()]
        # file_list = [filename for filename in self.csv_folder_path.iterdir() if filename.is_file()]
        # stem = self.output_folder_path.stem
        # print(file_list)
        for each in file_list:
            # Change the output file name to match the file name
            name_out = each.stem + '_out.txt'
            # parent = self.output_folder_path.parent
            # print("Output name ", name_out)
            output_path = self.output_folder_path.joinpath(name_out)
            # sets equal so that the name in ini file matches
            self.output_file = output_path
            # Write an ini for for it
            self.csv_generate_from = each
            name = str(each.stem) + '.ini'
            # print("ini name: ", name)
            file_each_path = self.output_folder_path.joinpath(name)
            file_each_path.touch()
            # print('file path: ', str(file_each_path))
            self.write_ini(file_each_path)
        self.multi_known = False

    def generate_directory_popup(self):
        # Popup to ask if the user wants to run all files or just the selected file
        self.multi_known = True
        directory_popup = Toplevel(self.root)
        msg = "Do you want to generate ini files for all files in this directory with the same parameters or just the selected file?"
        entry = ttk.Label(directory_popup, text=msg)
        entry.grid(column=0, row=0, columnspan=2, padx=5, pady=3)
        B1 = ttk.Button(directory_popup, text="All files",
                        command=lambda: [directory_popup.destroy(), self.loop_gen_ini_same_params(),
                                         change_multi_known()])
        B2 = ttk.Button(directory_popup, text="Just this one",
                        command=lambda: [directory_popup.destroy(), self.generate_ini(), change_multi_known()])
        B1.grid(column=0, row=1, padx=5, pady=3, sticky=E)
        B2.grid(column=1, row=1, padx=5, pady=3, sticky=W)
        directory_popup.grid_columnconfigure((0, 1), weight=1)
        directory_popup.grid_rowconfigure((0, 1), weight=1)
        directory_popup.protocol('WM_DELETE_WINDOW', directory_popup.destroy)
        directory_popup.attributes('-topmost', 'true')

        def change_multi_known():
            self.multi_known = False

    def generate_ini(self):
        if self.yes_folder.get() == 1 and self.multi_known is False:  # A folder is selected
            # pop up and ask if generate ini for all files, call appropriate loops
            self.generate_directory_popup()
        else:
            def unique_path():
                counter = 0
                while True:
                    num_name = str(name) + "_" + str(counter) + '.ini'
                    out_name = self.csv_generate_from.stem + "_" + str(counter) + '_out.txt'
                    self.output_file = self.output_folder_path.joinpath(out_name)
                    path = self.output_folder_path.joinpath(num_name)
                    if not path.exists():
                        return path
                    counter += 1

            name = self.csv_generate_from.stem
            file_path = unique_path()
            file_path.touch()
            self.write_ini(file_path)
            return file_path
            # os.chdir(pathlib.Path.cwd().parent)  # change the working directory from gui to nano-indent
            # ini_file = filedialog.asksaveasfilename(initialdir=pathlib.Path.cwd(),
            #                                       title="Choose output ini file",
            #                                      filetypes=[("ini files", "*.ini")])
            # if ini_file is None:
            #   return
            # if isinstance(ini_file, tuple) == False:
            #   if len(ini_file) != 0:
            #      self.write_ini(ini_file)
            #     messagebox.showinfo('', 'Ini file written to {fileloc}'.format(fileloc=ini_file))

            # os.chdir(pathlib.Path.cwd().joinpath('gui'))

    def select_csv_folder(self):
        os.chdir(pathlib.Path.cwd().parent)
        folder_name = pathlib.Path(filedialog.askdirectory(initialdir=pathlib.Path.cwd(), title="Choose a folder"))
        self.csv_folder.set(folder_name)
        self.csv_folder_path = folder_name  # No file has been selected yet - this is the folder
        # This calls a method to create a dropdown menu next to generate ini button of the files in the directory
        self.file_dropdown()
        os.chdir(pathlib.Path.cwd().joinpath('gui'))
        return folder_name

    #def read_input(self, filename):
        # parse with configparser
        # replace the C values in the calibration tab
        #config = configparser.ConfigParser()
        #config.read(filename)
        #self.C0.set(config['Calibrations']['C0'])
        #self.C1.set(config['Calibrations']['C1'])
        #self.C2.set(config['Calibrations']['C2'])
        #self.C3.set(config['Calibrations']['C3'])
        #self.C4.set(config['Calibrations']['C4'])
        #self.C5.set(config['Calibrations']['C5'])
        #self.C6.set(config['Calibrations']['C6'])
        #self.C7.set(config['Calibrations']['C7'])
        #self.C8.set(config['Calibrations']['C8'])
        #self.E_i.set(config['tip_const']['E_i'])
        #self.nu_i.set(config['tip_const']['nu_i'])
        # self.nu.set(config['nu']['nu'])

    #def select_calibration_file(self):
        #os.chdir(pathlib.Path.cwd().parent)  # change the working directory from gui to nano-indent
        #file_name = filedialog.askopenfilename(initialdir=pathlib.Path.cwd(), title="Choose txt/csv", filetypes=(
        #    ("txt files", "*.txt"), ("csv files", "*.csv"), ("all files", "*.*")))
        #self.csv_calibration_file.set(file_name)
        #if file_name:
        #    self.read_input(file_name)
        #os.chdir(pathlib.Path.cwd().joinpath('gui'))
       # return file_name

    def select_output_folder(self):
        """
        Select output folder
        """
        os.chdir(pathlib.Path.cwd().parent)  # change the working directory from gui to nano-indent
        folder_name = pathlib.Path(filedialog.askdirectory(initialdir=pathlib.Path.cwd(), title="Choose a folder"))
        self.output_folder.set(folder_name)
        print("select output folder, folder.get ", self.output_folder.get())
        self.output_folder_path = pathlib.Path(folder_name)
        self.output_file = self.output_folder_path.joinpath('out.txt')
        os.chdir(pathlib.Path.cwd().joinpath('gui'))
        return folder_name

    def loop_direc_same_params(self):
        """
        Will loop through every file in the selected directory and run it with the same parameters
        """
        # file_list = [file.absolute() for file in self.output_folder_path.glob('**/*.ini') if file.is_file()]
        file_list = [filename for filename in self.csv_folder_path.glob('**/*txt') if filename.is_file()]
        # file_list = [filename for filename in self.csv_folder_path.iterdir() if filename.is_file()]
        # stem = self.output_folder_path.stem
        # print(file_list)
        for each in file_list:
            # Change the output file name to match the file name
            name_out = each.stem + '_out.txt'
            # parent = self.output_folder_path.parent
            # print("Output name ", name_out)
            # Create output file
            output_path = self.output_folder_path.joinpath(name_out)
            output_path.touch()
            self.output_file = output_path

            # Write an ini for for it
            self.csv_generate_from = each
            name = str(each.stem) + '.ini'
            print("ini name: ", name)
            file_each_path = self.output_folder_path.joinpath(name)
            file_each_path.touch()
            self.write_ini(file_each_path)
            self.command_list.put(str(file_each_path))
            print("Finished adding to command_list")
            # Run the ini using the run_multi_function
            # self.run_multi_ini()
            # Use labda in button press - next go to run_multi_ini so we can stop

    def loop_direc_diff_params(self):
        # At current this just rins the single file selected
        # Would be cool but a lot of work to make it loop through files and accept new inputs
        # file_list = [filename for filename in self.folder_path.iterdir() if filename.is_file()]
        if not pathlib.Path(self.csv_folder_path.joinpath(self.file_menu.get())).is_file():
            print("No file selected from dropdown menu")
        else:
            name = self.generate_ini()
            self.stop_term()
            command = 'xes_neo -i ' + f'"{name.absolute().as_posix()}"' #Changing to xes_neo
            self.proc = subprocess.Popen("exec " + command, shell=True)

    def directory_popup(self):
        # Popup to ask if the user wants to run all files or just the selected file
        self.multi_known = True
        directory_popup = Toplevel(self.root)
        msg = "Do you want to run all files in this directory with the same parameters or just the selected file?"
        entry = ttk.Label(directory_popup, text=msg)
        entry.grid(column=0, row=0, columnspan=2, padx=5, pady=3)
        B1 = ttk.Button(directory_popup, text="All files",
                        command=lambda: [directory_popup.destroy(), self.loop_direc_same_params(),
                                         self.run_multi_ini()])
        B2 = ttk.Button(directory_popup, text="Just this one",
                        command=lambda: [directory_popup.destroy(), self.loop_direc_diff_params()])
        B1.grid(column=0, row=1, padx=5, pady=3, sticky=E)
        B2.grid(column=1, row=1, padx=5, pady=3, sticky=W)
        directory_popup.grid_columnconfigure((0, 1), weight=1)
        directory_popup.grid_rowconfigure((0, 1), weight=1)
        directory_popup.protocol('WM_DELETE_WINDOW', directory_popup.destroy)
        directory_popup.attributes('-topmost', 'true')

    def run_term(self):
        """
        Runs two separate methods
        if yes folder = 1 means that there is a folder selected
            leads to a popup that allows the user to run all the files with the same parameters
        else a single file is selected and run
        """
        if self.yes_folder.get() == 1:  # A folder is selected
            # pop up and ask if run all files, call appropriate loops
            self.directory_popup()
        else:
            name = self.generate_ini()
            self.stop_term()
            command = 'python ../xes.py -i ' + f'"{name.absolute().as_posix()}"' #changing nano_indent.py to xes.py
            print(command)
            self.proc = subprocess.Popen(''.join(command), shell=True)
            self.proc_list.append(self.proc)

    def build_global(self):
        '''
        Create global tab -  generate ini, run, about, dropdown
        '''

        def about_citation():
            popup = Toplevel()
            popup.wm_title("About: Ver: " + str(self.__version__))
            msg = 'Citation:' \
                  '\nTitle' \
                  '\n Authors' \
                  '\n[Submission], Year'
            cite = ttk.Label(popup, text='Citation:', font='TkTextFont')
            cite.grid(column=0, row=0, sticky=W, padx=self.padx, pady=self.pady)
            citation = scrolledtext.ScrolledText(popup, font="TkTextFont")
            citation.grid(column=0, row=1, padx=self.padx, pady=self.pady)
            with open('media/Citation') as f:
                citation.insert(END, f.read())

            License_Label = ttk.Label(popup, text='License:', font='TkTextFont')
            License_Label.grid(column=0, row=2, sticky=W, padx=self.padx, pady=self.pady)
            license = scrolledtext.ScrolledText(popup)
            license.grid(column=0, row=3, sticky=N + S + W + E, padx=self.padx, pady=self.pady)
            with open('../LICENSE') as f:
                license.insert(END, f.read())
            B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
            B1.grid(column=0, row=4, padx=self.padx, pady=self.pady)

            popup.grid_columnconfigure((1, 3), weight=1)
            popup.grid_rowconfigure((1, 3), weight=1)
            popup.protocol('WM_DELETE_WINDOW', popup.destroy)

        # Column 2 is the dropdown list, is created later as it will only appear if needed
        self.generate_button = ttk.Button(self.root, text="Generate Input", command=self.generate_ini)
        self.generate_button.grid(column=3, row=2, sticky=E, padx=self.padx, pady=self.pady)

        self.run_button = ttk.Button(self.root, text='Run', command=self.run_term)
        self.run_button.grid(column=4, row=2, columnspan=1, sticky=E, padx=self.padx, pady=self.pady)
        self.stop_button = ttk.Button(self.root, text='Stop',
                                      command=lambda: [self.stop_term(), self.run_multi_ini()])

        self.stop_button.grid(column=1, row=2, columnspan=1, sticky=W, padx=self.padx, pady=self.pady)

        self.about_button = ttk.Button(self.root, text='About', command=about_citation)
        self.about_button.grid(column=0, row=2, columnspan=1, sticky=W, padx=self.padx, pady=self.pady)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(3, weight=1)

        self.root.grid_rowconfigure(0, weight=1)

        # Create a empty frame
        self.label_frame = LabelFrame(self.root, text="Terminal", padx=5, pady=5)
        self.label_frame.grid(column=0, row=1, columnspan=5, padx=self.padx, pady=self.pady, sticky=E + W + N + S)

        # Create the textbox
        self.label_frame.rowconfigure(0, weight=1)
        self.label_frame.columnconfigure(0, weight=1)
        self.txtbox = scrolledtext.ScrolledText(self.label_frame, width=40, height=5) #Changed height from 10 -Alaina 02/14/2024
        self.txtbox.grid(row=0, column=0, sticky=E + W + N + S)

    def file_dropdown(self):
        p = self.csv_folder_path
        self.filelist = [filename.name for filename in p.glob('**/*txt') if filename.is_file()]
        self.file_menu['values'] = self.filelist
        self.file_menu['state'] = 'readonly'
        # sets the width of the combobox to be the length of the first file in the directory, not perfect but best dynamic solution I could think of
        self.file_menu['width'] = len(self.filelist[0])
        self.file_menu.bind("<<ComboboxSelected>>", self.file_selected)

    def build_inputs_tab(self):
        # Add the tab names
        arr_input = ["Input file", "Input Folder", "Output folder","Lines to skip", "Average Files: ", "Files to Average", "Averaged File", "Load in fit File"]
        self.description_tabs(arr_input, self.input_tab, row=[3, 4, 5, 6, 8, 9, 10, 13]) #deleted 'calibration file' from row 6

        self.input_tab.grid_columnconfigure(1, weight=1)



        def create_data_obj(x,y,z):
            #separate create func so that it can be called whenever skipLn is updated
            try:
                self.data_obj = data.xes_data(pathlib.Path(self.file_name),int(self.skipLn.get()))
                print("File read successfully")
            except:
                print("Error reading file, try inputting skipped lines")

        def select_folder():
            if self.yes_folder.get() == 1:  # When multiple input is checked
                csv_file_button.config(state=DISABLED)
                csv_folder_button.config(state=NORMAL)
                self.csv_folder.set("Please select a folder")
                self.csv_file.set("Folder is selected")
                if self.pertub_check.get() == 1:  # They are also running multiple instances of each file
                    self.checkbutton_whole_folder.config(state='normal')
                # self.file_dropdown()
                # Because no folder is selected yet this errors when put here
            elif self.yes_folder.get() == 0:  # Not Checked
                csv_file_button.config(state=NORMAL)
                csv_folder_button.config(state=DISABLED)
                self.csv_folder.set("File is selected")
                self.csv_file.set("Please select a file")
                if self.pertub_check.get() == 1:  # They are running multiple instances and previously may have selected a folder - disable folder button
                    self.checkbutton_whole_folder.config(state='disabled')
                    self.run_folder.set(
                        False)  # If they previously selected an entire folder need to now only run through the single file

        # functions for input data file
        def select_csv_file():
            os.chdir(pathlib.Path.cwd().parent)  # change the working directory from gui to nano-indent
            file_name = filedialog.askopenfilename(initialdir=pathlib.Path.cwd(), title="Choose txt/csv",
                                                   filetypes=(("txt files", "*.txt"), ("csv files", "*.csv"),
                                                              ("all files", "*.*")))
            if not file_name:
                self.csv_file.set('Please select a file')
            else:
                self.csv_folder.set("File is selected")
                self.csv_file.set(pathlib.Path(file_name))
                self.csv_generate_from = pathlib.Path(file_name)
                self.file_name = file_name
                # create the data objectives

                create_data_obj('','','')

            # disable the dropdown file menu (if user had folder and changed their mind)
            if self.yes_folder.get() == 0:
                self.file_menu.configure(state="disabled")
                self.csv_folder.set("File selected")
            os.chdir(pathlib.Path.cwd().joinpath('gui'))

        def select_csv_folder():
            os.chdir(pathlib.Path.cwd().parent)
            initial_dir = pathlib.Path.cwd()
            folder_name = filedialog.askdirectory(initialdir=pathlib.Path.cwd(), title="Choose a folder")

            if not folder_name:  # They did not select a folder
                self.csv_folder.set("Please choose a folder")
            else:
                folder_path = pathlib.Path(folder_name)
                self.csv_file.set("Folder is selected")
                self.csv_folder.set(folder_path)
                self.csv_folder_path = folder_path  # No file has been selected yet - this is the folder
                # This calls a method to create a dropdown menu next to generate ini button of the files in the directory
                self.file_dropdown()
            os.chdir(pathlib.Path.cwd().joinpath('gui'))

        def get_fit_params():
            #Getting all the values from configuration settings file and updating them in the GUI for running a new fit using the same parameters
           
            self.fit_file_selected = True

            


            #fit_file_path = os.path.join(os.getcwd(),args.params)
            config = configparser.ConfigParser()
            print("Reading in fitting parameters from Configuration Setttings file")
            print("Fit file name: ", config.read(self.fit_file.get()))
            
            
            #Reading all the paramters and storing them as StringVar, DoubleVar, etc.
            self.population =   config.get('Populations', 'population')
            self.population = StringVar(self.root, self.population)
            self.num_gen =   config.get('Populations', 'num_gen')
            self.num_gen = StringVar(self.root, self.num_gen)
            self.best_sample =   config.get('Populations', 'best_sample')
            self.best_sample = StringVar(self.root, self.best_sample)
            self.lucky_few =   config.get('Populations', 'lucky_few')
            self.lucky_few = StringVar(self.root, self.lucky_few)
            
            self.chance_of_mutation = config.get('Mutations', 'chance_of_mutation')
            self.chance_of_mutation = StringVar(self.root, self.chance_of_mutation)
            self.original_chance_of_mutation = config.get('Mutations', 'original_chance_of_mutation')
            self.original_chance_of_mutation = StringVar(self.root, self.original_chance_of_mutation)
            self.mutated_options = config.get('Mutations', 'mutated_options')
            self.mutated_options = StringVar(self.root, self.mutated_options)
            
            self.number_of_peaks = config.get('Paths', 'nPeaks')
            self.number_of_peaks = IntVar(self.root,self.number_of_peaks)
            self.background_types = config.get('Paths', 'background_type').split(',')
            peakTypes = config.get('Paths', 'peak_type').split(',')
            branching_ratio = (config.get('Paths', 'branching_ratio')).split(', ')
            PE_range_min = (config.get('Paths', 'PE_range_min')).split(',')
            PE_range_max = (config.get('Paths', 'PE_range_max')).split(',')
            PE_limited = (config.get('Paths', 'PE_limited')).split(', ')
            PE_correlated = (config.get('Paths', 'PE_correlated')).split(', ')
            PE_correlated_mult = (config.get('Paths', 'PE_correlated_mult')).split(', ') 
            energy = (config.get('Paths', 'PE')).split(', ')
            is_singlet = (config.get('Paths', 'is_singlet')).split(', ')
            is_coster_kronig = (config.get('Paths', 'is_coster_kronig')).split(', ')
            spinOrbitSplit = (config.get('Paths', 'spinOrbitSplit')).split(', ')

            sigma_range_min = (config.get('Paths', 'sigma_range_min')).split(',')
            sigma_range_max = (config.get('Paths', 'sigma_range_max')).split(',')
            sigma_limited = (config.get('Paths', 'sigma_limited')).split(', ')
            sigma_correlated = (config.get('Paths', 'sigma_correlated')).split(', ')
            sigma_correlated_mult = (config.get('Paths', 'sigma_correlated_mult')).split(', ') 
            sigma_guess = (config.get('Paths', 'sigma_guess')).split(', ')

            gamma_range_min = (config.get('Paths', 'gamma_range_min')).split(',')
            gamma_range_max = (config.get('Paths', 'gamma_range_max')).split(',')
            gamma_limited = (config.get('Paths', 'gamma_limited')).split(', ')
            gamma_correlated = (config.get('Paths', 'gamma_correlated')).split(', ')
            gamma_correlated_mult = (config.get('Paths', 'gamma_correlated_mult')).split(', ') 
            gamma_guess = (config.get('Paths', 'gamma_guess')).split(', ')

            amp_range_min = (config.get('Paths', 'amp_range_min')).split(',')
            amp_range_max = (config.get('Paths', 'amp_range_max')).split(',')
            amp_limited = (config.get('Paths', 'amp_limited')).split(', ')
            amp_correlated = (config.get('Paths', 'amp_correlated')).split(', ')
            amp_correlated_mult = (config.get('Paths', 'amp_correlated_mult')).split(', ') 
            amp_guess = (config.get('Paths', 'amp_guess')).split(', ')
            
            #Updating background checkboxes in Fitting Parameters tab
            for i in self.background_types:
                if i == "Shirley-Sherwood":
                    self.shirley_value = IntVar(value=1)
                if i == "Linear":
                    self.linear_value = IntVar(value=1)
                if i == "Exponential":
                    self.exp_value = IntVar(value=1)
                if i == "2-Param Tougaard":
                    self.toug2_value = IntVar(value=1)
                if i == "3-Param Tougaard":
                    self.toug3_value = IntVar(value=1)
                if i == "Polynomial 1":
                    self.poly1_value = IntVar(value=1)
                if i == "Polynomial 2":
                    self.poly2_value = IntVar(value=1)
                if i == "Polynomial 3":
                    self.poly3_value = IntVar(value=1)
                  
               
            #Converting values into the correct list format for calling in the GA
            for i in range(int(self.number_of_peaks.get())):
                

                self.peaks[i] = StringVar(self.root,peakTypes[i])
                self.path_branching[i] = DoubleVar(self.root, branching_ratio[i])
                self.PE_low_lim[i] = DoubleVar(self.root, PE_range_min[i])
                self.PE_up_lim[i] = DoubleVar(self.root, PE_range_max[i])
                self.PE_limit[i] = BooleanVar(self.root, PE_limited[i])
                self.PE_corr[i] = StringVar(self.root, PE_correlated[i])
                self.PE_corr_mult[i] = DoubleVar(self.root, PE_correlated_mult[i])
                self.PE_guesses[i] = DoubleVar(self.root, energy[i])
                self.peak_singlet[i] = BooleanVar(self.root, is_singlet[i])
                self.peak_coster_kronig[i] = BooleanVar(self.root, is_coster_kronig[i])
                self.so_split[i] = DoubleVar(self.root, spinOrbitSplit[i])

                self.sigma_low_lim[i] = DoubleVar(self.root, sigma_range_min[i])
                self.sigma_up_lim[i] = DoubleVar(self.root, sigma_range_max[i])
                self.sigma_limit[i] = BooleanVar(self.root, sigma_limited[i])
                self.sigma_corr[i] = StringVar(self.root, sigma_correlated[i])
                self.sigma_corr_mult[i] = DoubleVar(self.root, sigma_correlated_mult[i])
                self.sigma_guesses[i] = DoubleVar(self.root, sigma_guess[i])

                self.gamma_low_lim[i] = DoubleVar(self.root, gamma_range_min[i])
                self.gamma_up_lim[i] = DoubleVar(self.root, gamma_range_max[i])
                self.gamma_limit[i] = BooleanVar(self.root, gamma_limited[i])
                self.gamma_corr[i] = StringVar(self.root, gamma_correlated[i])
                self.gamma_corr_mult[i] = DoubleVar(self.root, gamma_correlated_mult[i])
                self.gamma_guesses[i] = DoubleVar(self.root, gamma_guess[i])

                self.amp_low_lim[i] = DoubleVar(self.root, amp_range_min[i])
                self.amp_up_lim[i] = DoubleVar(self.root, amp_range_max[i])
                self.amp_limit[i] = BooleanVar(self.root, amp_limited[i])
                self.amp_corr[i] = StringVar(self.root, amp_correlated[i])
                self.amp_corr_mult[i] = DoubleVar(self.root, amp_correlated_mult[i])
                self.amp_guesses[i] = DoubleVar(self.root, amp_guess[i])

            #Need to recall these tabs so that the new values are updated in the GUI
            self.build_population_tab()
            self.build_mutations_tab()
            self.build_fitting_param_tab()
            self.build_param_range_tab()
                
            
           
            


        def select_fit_file():
            
            fit_file_name = filedialog.askopenfilename(initialdir=pathlib.Path.cwd(), title="Choose ini",
                                                   filetypes=(("ini files", "*.ini"),
                                                              ("all files", "*.*")))
            
            if not fit_file_name:
                self.fit_file.set('Please select a file')
            else:
                self.fit_file.set(pathlib.Path(fit_file_name))
                self.fit_generate_from = pathlib.Path(fit_file_name)
                self.fit_file_name = fit_file_name
                get_fit_params() #WHere we get all the values after inmporting the configuration settings file
            
            




        multiple_input_button = ttk.Checkbutton(self.input_tab,
                                                variable=self.yes_folder,
                                                command=select_folder,
                                                offvalue=0, onvalue=1)
        multiple_input_button.grid(column=0, row=2, sticky=E)

        def select_files_to_average():
            os.chdir("..") #change the working directory from gui to XES

            all_files = filedialog.askopenfilenames(initialdir = os.getcwd(), title = "Choose txt/csv", filetypes = (("txt files", "*.txt"),("csv files","*.csv"),("all files","*.*")))

            if not all_files:
                self.all_files.set('Please choose files to average')
                #os.chdir("gui")
            else:
                self.all_files_display.set(all_files)
                self.all_files = all_files
                #os.chdir("gui")
                #print(self.all_files)
            os.chdir(pathlib.Path.cwd().joinpath('gui'))

        def select_file_to_save_averaged_data():
            os.chdir("..")
            averaged_file = filedialog.asksaveasfilename(initialdir = os.getcwd(), title = "Choose txt/csv", filetypes = (("txt files", "*.txt"),("csv files","*.csv"),("all files","*.*")))

            if not averaged_file:
                self.averaged_file.set('Please choose a file to save averaged data')
                # os.chdir("gui")
            else:
                self.averaged_file.set(averaged_file)
                # os.chdir("gui")
            os.chdir(pathlib.Path.cwd().joinpath('gui'))

        def average_selected_data():
            #Finds lines to skip at top of data that are comments
            #lines_to_skip = 2

            # with open(self.all_files[0]) as file:
            #     str=file.readline()
            #     while(not str.__contains__('***')):
            #         lines_to_skip += 1
            #         str=file.readline()
            lines_to_skip = int(self.skipLn.get()) #Should we make a seperate variable for averaging files skip

            self.num_files = len(self.all_files)
            try:
                print("File read successfully")
                self.num_points = len(np.loadtxt(self.all_files[0], skiprows=lines_to_skip, usecols=(0,))) #Error here if skiplines is not correct
                self.xPoints_for_data_plot = np.loadtxt(self.all_files[0], skiprows=lines_to_skip, usecols=(0,))
                self.yPoints_for_data_plot = np.loadtxt(self.all_files[0], skiprows=lines_to_skip, usecols=(8,))

                for i in range(self.num_files):
                    if i > 0:
                        self.xPoints_for_data_plot += np.array(np.loadtxt(self.all_files[i], skiprows=lines_to_skip, usecols=(0,)))
                        self.yPoints_for_data_plot += np.array(np.loadtxt(self.all_files[i], skiprows=lines_to_skip, usecols=(8,)))

                self.xPoints_avg = np.array(self.xPoints_for_data_plot/self.num_files)
                self.yPoints_avg = np.array(self.yPoints_for_data_plot/self.num_files)

                self.plot_data = np.column_stack((self.xPoints_avg,self.yPoints_avg))
                np.savetxt(self.averaged_file.get(), self.plot_data)
                print("Average file outputted")
            except:
                print("Error reading file, try inputting skipped lines")
                
        

        # Entries:
        # Add the tab entry boxes for inputs
        csv_file_entry = ttk.Entry(self.input_tab, textvariable=self.csv_file, font=self.entryFont)
        csv_file_entry.grid(column=1, row=3, sticky=(W, E))
        csv_folder_entry = ttk.Entry(self.input_tab, textvariable=self.csv_folder, font=self.entryFont)
        csv_folder_entry.grid(column=1, row=4, sticky=(W, E))

        # Add the tab entry boxes for outputs
        output_folder_entry = ttk.Entry(self.input_tab, textvariable=self.output_folder, font=self.entryFont)
        output_folder_entry.grid(column=1, row=5, sticky=(W, E))

        # Add the tab entry boxes for averaging
        entry_files_to_average = ttk.Combobox(self.input_tab, textvariable=self.all_files_display, font=self.entryFont)
        entry_files_to_average.grid(column=1, row=9, sticky=(W,E),padx=self.padx,pady=self.pady)

        entry_averaged_file = ttk.Entry(self.input_tab, textvariable=self.averaged_file, font=self.entryFont)
        entry_averaged_file.grid(column=1, row=10, sticky=(W,E),padx=self.padx,pady=self.pady)

        # Buttons:
        # Adding button to chose file or folder input
        checkbutton_label = ttk.Label(self.input_tab, text="Check to select a folder of input files",
                                      font=self.labelFont)
        checkbutton_label.grid(column=1, row=2, sticky=W)
        
        #Do all XES data come in low to high photon energy?
        '''
        self.KE_check = 2
        def KE_selected():
            global KE_check
            if (self.KE_check % 2) == 0:
                print("Reading data in kinetic energy")
                self.data_KE = True
                
                self.KE_check = 1
            else:
                print("Reading data in binding energy")
                self.data_KE = False

                self.KE_check = 2

        self.checkbutton_KE = ttk.Checkbutton(self.input_tab, text="KE",onvalue= True,offvalue=False, command=KE_selected)
        #self.checkbutton_doublets[i] = ttk.Checkbutton(self.fitting_param_tab, text="Doublet", command=doublet_selected)
        self.checkbutton_KE.grid(column=0, row=2, sticky=W)
        self.checkbutton_KE.state(['!alternate'])
        '''


       
        '''
        self.XES_check = 2
        def XES_selected():
            global XES_check
            if (self.XES_check % 2) == 0:
                print("Reading data in photon energy")
                self.data_XES = True
        
                self.XES_check = 1
            else:
                print("Reading data in binding energy")
                self.data_XES = False

                self.XES_check = 2

        self.checkbutton_XES = ttk.Checkbutton(self.input_tab, text="XES", onvalue= 0,offvalue=1, command=XES_selected) #Dont need a variable --> Will cause buttons to get mixed up for on/off
        #self.checkbutton_doublets[i] = ttk.Checkbutton(self.fitting_param_tab, text="Doublet", command=doublet_selected)
        self.checkbutton_XES.grid(column=0, row=12, sticky=W)
        self.checkbutton_XES.state(['!alternate'])
        '''
        
        self.peak_add_check = 2
        def peak_add_selected():
            global peak_add_check
            if (self.peak_add_check % 2) == 0:
                print("Allowing algorithm to add/remove peaks")
                self.data_peak_add = True
        
                self.peak_add_check = 1
            else:
                print("Not allowing algorithm to add/remove peaks")
                self.data_peak_add = False

                self.peak_add_check = 2
      
        self.checkbutton_peak_add = ttk.Checkbutton(self.input_tab, text="Allow peak addition/removal", command=peak_add_selected)
        #self.checkbutton_doublets[i] = ttk.Checkbutton(self.fitting_param_tab, text="Doublet", command=doublet_selected)
        self.checkbutton_peak_add.grid(column=1, row=12, sticky=W)
        self.checkbutton_peak_add.state(['!alternate'])


        # Adding buttons to select each different file/folder
        csv_file_button = ttk.Button(self.input_tab, text="Select File", command=select_csv_file,
                                     style='my.TButton')
        csv_file_button.grid(column=2, row=3, sticky=W)
        # Link this to a variable so when folder is selected file dropdown appears
        csv_folder_button = ttk.Button(self.input_tab, text="Select Folder", command=select_csv_folder,
                                       style='my.TButton')
        csv_folder_button.grid(column=2, row=4, sticky=W)
        csv_folder_button.config(state=DISABLED)  # Unless the multiple file button is checked this will be disabled
        output_folder_button = ttk.Button(self.input_tab, text="Select Folder", command=self.select_output_folder,
                                          style='my.TButton')
        output_folder_button.grid(column=2, row=5, sticky=W)

        # Lines to Skip Entry
        skipLn_entry = ttk.Entry(self.input_tab,textvariable=self.skipLn,font = self.entryFont,width=5)
        skipLn_entry.grid(column=1,row=6,sticky=W)
        self.skipLn.trace_add("write",create_data_obj)

        #Loading in fit file button
        fit_file_button = ttk.Button(self.input_tab, text="Select File", command=select_fit_file,
                                     style='my.TButton')
        fit_file_button.grid(column=2, row=13, sticky=W)

        #Scale Data Button
        self.scale_check = 1
        self.scale = False
        def scale_raw():
           
            if (self.scale_check % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                
                self.scale = False
                self.scale_var = False
                self.scale_check = 1
            else: #state of button is on
                self.scale = True
                self.scale_check = 2
                self.scale_var = True

            print(self.scale)


        self.checkbutton_scale = ttk.Checkbutton(self.input_tab, text="Scale Data", command=scale_raw)
        self.checkbutton_scale.grid(column=2, row=6, sticky=W)
        self.checkbutton_scale.state(['!alternate'])

        #Loading in fit file:
        fit_file_entry = ttk.Entry(self.input_tab, textvariable=self.fit_file, font=self.entryFont)
        fit_file_entry.grid(column=1, row=13, sticky=(W, E))




        # Line between Inputs and Averaging
        separator = ttk.Separator(self.input_tab, orient='horizontal')
        separator.grid(column=0, row=7, columnspan=4, sticky=W + E, padx=self.padx,pady=self.pady)

        # Adding buttons for averaging section
        button_choose_files = ttk.Button(self.input_tab, text="Select Files",command=select_files_to_average, style='my.TButton')
        button_choose_files.grid(column=2, row=9, sticky=W,padx=self.padx,pady=self.pady)

        button_output_file = ttk.Button(self.input_tab,text="Select File",command=select_file_to_save_averaged_data, style='my.TButton')
        button_output_file.grid(column=2, row=10, sticky=W,padx=self.padx,pady=self.pady)

        button_average_data = ttk.Button(self.input_tab,text="Average",command=average_selected_data, style='my.TButton')
        button_average_data.grid(column=0, row=11, sticky=W,padx=self.padx,pady=self.pady)

        #self.file_menu.grid(column=2, row=2, sticky=(W, E))

        #self.file_menu.grid(column=2, row=3, sticky=(W, E))


    def build_population_tab(self):
        """
        Build population tab
        """
        arr_pop = ["Population", "Number of generations", "Best individuals (%)", "Lucky survivor (%)"]
        self.description_tabs(arr_pop, self.population_tab, row=[2, 3, 4, 5])
        population_entry = ttk.Entry(self.population_tab, width=7, textvariable=self.population, font=self.entryFont)
        population_entry.grid(column=2, row=2, sticky=W)
        num_gen_entry = ttk.Entry(self.population_tab, width=7, textvariable=self.num_gen, font=self.entryFont)
        num_gen_entry.grid(column=2, row=3, sticky=W)
        best_sample_entry = ttk.Entry(self.population_tab, width=7, textvariable=self.best_sample, font=self.entryFont)
        best_sample_entry.grid(column=2, row=4, sticky=W)
        lucky_few_entry = ttk.Entry(self.population_tab, width=7, textvariable=self.lucky_few, font=self.entryFont)
        lucky_few_entry.grid(column=2, row=5, sticky=W)

    def build_mutations_tab(self):
        arr_mutations = ["Mutation chance (%)", "Original chance of mutation (%)",
                         "Mutation options"]
        self.description_tabs(arr_mutations, self.mutation_tab, row=[2, 3, 4])
        mut_list = list(range(101))
        chance_of_mutation_entry = ttk.Combobox(self.mutation_tab, width=7, textvariable=self.chance_of_mutation,
                                                values=mut_list,
                                                state="readonly")
        chance_of_mutation_entry.grid(column=4, row=2, sticky=W)
        original_chance_of_mutation_entry = ttk.Combobox(self.mutation_tab, width=7,
                                                         textvariable=self.original_chance_of_mutation,
                                                         values=mut_list, state="readonly")
        original_chance_of_mutation_entry.grid(column=4, row=3, sticky=W)
        mutated_options_drop_list = ttk.Combobox(self.mutation_tab, width=2, textvariable=self.mutated_options,
                                                 values=[0, 1, 2, 3],
                                                 state="readonly")
        mutated_options_drop_list.grid(column=4, row=4, sticky=W)


    def build_periodicTable_tab(self):
        
        temp_root = self.root
        PE_guesses = self.PE_guesses
        gamma_guesses = self.gamma_guesses
        gamma_low_lim = self.gamma_low_lim
        gamma_up_lim = self.gamma_up_lim
        #Dont know if we need these
        #sos_guesses = self.sos_guesses
        #br_guesses = self.br_guesses
        singlet = self.peak_singlet
        peakType = self.peaks
        is_coster_kronig = self.peak_coster_kronig
        num_peaks = self.number_of_peaks
        outer_self = self

        self.photoelectronLineArr = []
        self.elementArr = []
        self.transitionLineArr = []
        self.count_table = 0
        for i in range(10):
            self.photoelectronLineArr.append(" ")
            self.elementArr.append(" ")
            self.transitionLineArr.append(" ")




        #Code taken from https://codereview.stackexchange.com/questions/272438/python-tkinter-periodic-table-of-chemical-elements and adapted to fit XES data -- Alaina Humiston
        #Periodic Table of information. When the element is clicked it prompts the user to select the spectral line of interest
        #Used to help narrow down the fitting ranges of parameters in XES data

        symbols = ['H','He','Li','Be','B','C','N','O','F','Ne',
           'Na','Mg','Al','Si','P','S','Cl','Ar','K', 'Ca',
           'Sc', 'Ti', 'V','Cr', 'Mn', 'Fe', 'Co', 'Ni',
           'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
           'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru',
           'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te',
           'I', 'Xe','Cs', 'Ba','La', 'Ce', 'Pr', 'Nd', 'Pm',
           'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm',
           'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir',
           'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
           'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am',
           'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr',
           'Rf', 'Db', 'Sg', 'Bh','Hs', 'Mt', 'Ds', 'Rg', 'Cn',
           'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        keywords =['name','index','element catagory','group','period','block',
                'atomic mass','state of matter','density','electronegativity']

        values = [['Hydrogen',1,'Reactive Nonmetal',1,1,'s',1.01,'gas',0.08,2.2],#H
                 ['Helium',2,'Noble Gas',18,1,'s',4.00,'gas',0.18,'n.A'],#He
                ['Lithium',3,'Alkali Metal',1,2,'s',6.94,'solid',0.53,0.98],#Li
                ['Beryllium',4,'Alkaline Earth Metal',2,2,'s',9.01,'solid',1.84,1.57],#Be
                ['Boron',5,'Metalloid',13,2,'p',10.81,'solid',2.46,2.04],#B
                ['Carbon',6,'Reactive Nonmetal',14,2,'p',12.01,'solid',2.26,2.55],#C
                ['Nitrogen',7,'Reactive Nonmetal',15,2,'p',14.00,'gas',1.17,3.04],#N
                ['Oxygen',8,'Reactive Nonmetal',16,2,'p',15.99,'gas',1.43,3.44],#O
                ['Fluorine',9,'Reactive Nonmetal',17,2,'p',18.99,'gas',1.70,3.98],#F
                ['Neon',10,'Noble Gas',18,2,'p',20.17,'gas',0.90,'n.A'],#Ne

                ['Sodium',11,'Alkali Metal',1,3,'s',22.99,'solid',0.97,0.93],#Na
                ['Magnesium',12,'Alkaline Earth Metal',2,3,'s',24.31,'solid',1.74,1.31],#Mg
                ['Aluminium',13,'Post-transition Metal',13,3,'p',26.98,'solid',2.69,1.61],#Al
                ['Silicon',14,'Metalloid',14,3,'p',28.08,'solid',2.34,1.90],#Si
                ['Phosphorus',15,'Reactive Nonmetal',15,3,'p',30.97,'solid',2.4,2.19],#P
                ['Sulfur',16,'Reactive Nonmetal',16,3,'p',32.06,'solid',2.07,2.58],#S
                ['Chlorine',17,'Reactive Nonmetal',17,3,'p',35.45,'gas',3.22,3.16],#Cl
                ['Argon',18,'Noble Gas',18,3,'p',39.95,'gas',1.78,'n.A'],#Ar
                ['Potassium',19,'Alkali Metal',1,4,'s',39.09,'solid',0.86,0.82],#K
                ['Calicium',20,'Alkaline Earth Metal',2,4,'s',40.08,'solid',1.55,1.00],#Ca

                ['Scandium',21,'Transition Metal',3,4,'d',44.96,'solid',2.99,1.36],#Sc
                ['Titanium',22,'Transition Metal',4,4,'d',47.87,'solid',4.5,1.54],#Ti
                ['Vanadium',23,'Transition Metal',5,4,'d',50.94,'solid',6.11,1.63],#V
                ['Chromium',24,'Transition Metal',6,4,'d',51.99,'solid',7.14,1.66],#Cr
                ['Manganese',25,'Transition Metal',7,4,'d',54.94,'solid',7.43,1.55],#Mn
                ['Iron',26,'Transition Metal',8,4,'d',55.85,'solid',7.87,1.83],#Fe
                ['Cobalt',27,'Transition Metal',9,4,'d',58.93,'solid',8.90,1.88],#Co
                ['Nickel',28,'Transition Metal',10,4,'d',58.69,'solid',8.90,1.91],#Ni

                ['Copper',29,'Transition Metal',11,4,'d',63.54,'solid',8.92,1.90],#Cu
                ['Zinc',30,'Transition Metal',12,4,'d',65.38,'solid',7.14,1.65],#Zn
                ['Gallium',31,'Post-transition Metal',13,4,'p',69.72,'solid',5.90,1.81],#Ga
                ['Germanium',32,'Metalloid',14,4,'p',72.63,'solid',5.32,2.01],#Ge
                ['Arsenic',33,'Metalloid',15,4,'p',74.92,'solid',5.73,2.18],#As
                ['Selenium',34,'Metalloid',16,4,'p',78.97,'solid',4.82,2.55],#Se
                ['Bromine',35,'Reactive Nonmetal',17,4,'p',79.90,'fluid',3.12,2.96],#Br
                ['Krypton',36,'Noble Gas',18,4,'p',83.80,'gas',3.75,3.00],#Kr

                ['Rubidium',37,'Alkali Metal',1,5,'s',85.47,'solid',1.53,0.82],#Rb
                ['Strontium',38,'Alkaline Earth Metal',2,5,'s',87.62,'solid',2.63,0.95],#Sr
                ['Yttrium',39,'Transition Metal',3,5,'d',88.91,'solid',4.47,1.22],#Y
                ['Zirconium',40,'Transition Metal',4,5,'d',91.22,'solid',6.50,1.33],#Zr
                ['Niobium',41,'Transition Metal',5,5,'d',92.90,'solid',8.57,1.6],#Nb
                ['Molybdenum',42,'Transition Metal',6,5,'d',95.95,'solid',10.28,2.16],#Mo
                ['Technetium',43,'Transition Metal',7,5,'d',98.90,'solid',11.5,1.9],#Tc
                ['Ruthenium',44,'Transition Metal',8,5,'d',101.07,'solid',12.37,2.2],#Ru

                ['Rhodium',45,'Transition Metal',9,5,'d',102.90,'solid',12.38,2.28],#Rh
                ['Palladium',46,'Transition Metal',10,5,'d',106.42,'solid',11.99,2.20],#Pd
                ['Silver',47,'Transition Metal',11,5,'d',107.87,'solid',10.49,1.93],#Ag
                ['Cadmium',48,'Transition Metal',12,5,'d',112.41,'solid',8.65,1.69],#Cd
                ['Indium',49,'Post-transition Metal',13,5,'p',114.82,'solid',7.31,1.78],#In
                ['Tin',50,'Post-transition Metal',14,5,'p',118.71,'solid',5.77,1.96],#Sn
                ['Antimony',51,'Metalloid',15,5,'p',121.76,'solid',6.70,2.05],#Sb
                ['Tellurium',52,'Metalloid',16,5,'p',127.60,'solid',6.24,2.10],#Te

                ['Iodine',53,'Reactive Nonmetal',17,5,'p',126.90,'solid',4.94,2.66],#I
                ['Xenon',54,'Noble Gas',18,5,'p',131.29,'gas',5.90,2.6],#Xe
                ['Caesium',55,'Alkali Metal',1,6,'s',132.91,'solid',1.90,0.79],#Cs
                ['Barium',56,'Alkaline Earth Metal',2,6,'s',137.33,'solid',3.62,0.89],#Ba
                ['Lanthanum',57,'Transition Metal',3,6,'d',138.90,'solid',6.17,1.1],#La
                ['Cerium',58,'Lanthanide','La',6,'f',140.12,'solid',6.77,1.12],#Ce
                ['Praseodymium',59,'Lanthanide','La',6,'f',140.91,'solid',6.48,1.13],#Pr
                ['Neodymium',60,'Lanthanide','La',6,'f',144.24,'solid',7.00,1.14],#Nd
                ['Promethium',61,'Lanthanide','La',6,'f',146.91,'solid',7.2,'n.A.'],#Pm

                ['Samarium',62,'Lanthanide','La',6,'f',150.36,'solid',7.54,1.17],#Sm
                ['Europium',63,'Lanthanide','La',6,'f',151.96,'solid',5.25,'n.A'],#Eu
                ['Gadolinium',64,'Lanthanide','La',6,'f',157.25,'solid',7.89,1.20],#Gd
                ['Terbium',65,'Lanthanide','La',6,'f',158.93,'solid',8.25,'n.A'],#Tb
                ['Dysprosium',66,'Lanthanide','La',6,'f',162.50,'solid',8.56,1.22],#Dy
                ['Holmium',67,'Lanthanide','La',6,'f',164.93,'solid',8.78,1.23],#Ho
                ['Erbium',68,'Lanthanide','La',6,'f',167.26,'solid',9.05,1.24],#Er
                ['Thulium',69,'Lanthanide','La',6,'f',168.93,'solid',9.32,1.25],#Tm

                ['Ytterbium',70,'Lanthanide','La',6,'f',173.05,'solid',6.97,'n.A'],#Yb
                ['Lutetium',71,'Lanthanide','La',6,'f',174.97,'solid',9.84,1.27],#Lu
                ['Hafnium',72,'Transition Metal',4,6,'d',178.49,'solid',13.28,1.3],#Hf
                ['Tantalum',73,'Transition Metal',5,6,'d',180.95,'solid',16.65,1.5],#Ta
                ['Tungsten',74,'Transition Metal',6,6,'d',183.84,'solid',19.25,2.36],#W
                ['Rhenium',75,'Transition Metal',7,6,'d',186.21,'solid',21.00,1.9],#Re
                ['Osmium',76,'Transition Metal',8,6,'d',190.23,'solid',22.59,2.2],#Os
                ['Irdium',77,'Transition Metal',9,6,'d',192.22,'solid',22.56,2.2],#Ir

                ['Platinum',78,'Transition Metal',10,6,'d',195.08,'solid',21.45,2.2],#Pt
                ['Gold',79,'Transition Metal',11,6,'d',196.97,'solid',19.32,2.54],#Au
                ['Mercury',80,'Transition Metal',12,6,'d',200.59,'fluid',13.55,2.00],#Hg
                ['Thallium',81,'Post-transition Metal',13,6,'p',204.38,'solid',11.85,1.62],#Tl
                ['Lead',82,'Post-transition Metal',14,6,'p',207.20,'solid',11.34,2.33],#Pb
                ['Bismuth',83,'Post-transition Metal',15,6,'p',208.98,'solid',9.78,2.02],#Bi
                ['Polonium',84,'Post-transition Metal',16,6,'p',209.98,'solid',9.20,2.0],#Po
                ['Astatine',85,'Post-transition Metal',17,6,'p',209.99,'solid','n.A',2.2],#At
                ['Radon',86,'Noble Gas',18,6,'p',222.00,'gas',9.73,'n.A'],#Rn

                ['Francium',87,'Alkali Metal',1,7,'s',223.02,'solid','n.A',0.7],#Fr
                ['Radium',88,'Alkaline Earth Metal',2,7,'s',226.03,'solid',5.5,0.9],#Ra
                ['Actinium',89,'Actinide',3,7,'d',227.03,'solid',10.07,1.1],#Ac
                ['Thorium',90,'Actinide','Ac',7,'f',232.04,'solid',11.72,1.3],#Th
                ['Protactinium',91,'Actinide','Ac',7,'f',231.04,'solid',15.37,1.5],#Pa
                ['Uranium',92,'Actinide','Ac',7,'f',238.03,'solid',19.16,1.38],#U
                ['Neptunium',93,'Actinide','Ac',7,'f',237.05,'solid',20.45,1.36],#Np
                ['Plutonium',94,'Actinide','Ac',7,'f',244.06,'solid',19.82,1.28],#Pu
                ['Americium',95,'Actinide','Ac',7,'f',243.06,'solid',13.67,1.3],#Am

                ['Curium',96,'Actinide','Ac',7,'f',247.07,'solid',13.51,1.3],#Cm
                ['Berkelium',97,'Actinide','Ac',7,'f',247,'solid',14.78,1.3],#Bk
                ['Californium',98,'Actinide','Ac',7,'f',251,'solid',15.1,1.3],#Cf
                ['Einsteinium',99,'Actinide','Ac',7,'f',252,'solid',8.84,'n.A'],#Es
                ['Fermium',100,'Actinide','Ac',7,'f',257.10,'solid','n.A','n.A'],#Fm
                ['Medelevium',101,'Actinide','Ac',7,'f',258,'solid','n.A','n.A'],#Md
                ['Nobelium',102,'Actinide','Ac',7,'f',259,'solid','n.A.','n.A'],#No
                ['Lawrencium',103,'Actinide','Ac',7,'f',266,'solid','n.A','n.A'],#Lr

                ['Rutherfordium',104,'Transition Metal',4,7,'d',261.11,'solid',17.00,'n.A'],#Rf
                ['Dubnium',105,'Transition Metal',5,7,'d',262.11,'n.A','n.A','n.A'],#Db
                ['Seaborgium',106,'Transition Metal',6,7,'d',263.12,'n.A','n.A','n.A'],#Sg
                ['Bohrium',107,'Transition Metal',7,7,'d',262.12,'n.A','n.A','n.A'],#Bh
                ['Hassium',108,'Transition Metal',8,7,'d',265,'n.A','n.A','n.A'],#Hs
                ['Meitnerium',109,'Unknown',9,7,'d',268,'n.A','n.A','n.A'],#Mt
                ['Darmstadtium',110,'Unknown',10,7,'d',281,'n.A','n.A','n.A'],#Ds
                ['Roentgenium',111,'Unknown',11,7,'d',280,'n.A','n.A','n.A'],#Rg
                ['Copernicium',112,'Unknown',12,7,'d',277,'n.A','n.A','n.A'],#Cn

                ['Nihonium',113,'Unknown',13,7,'p',287,'n.A','n.A','n.A'],#Nh
                ['Flerovium',114,'Unknown',14,7,'p',289,'n.A','n.A','n.A'],#Fl
                ['Moscovium',115,'Unknown',15,7,'p',288,'n.A','n.A','n.A'],#Mc
                ['Livermorium',116,'Unknown',16,7,'p',293,'n.A','n.A','n.A'],#Lv
                ['Tennessine',117,'Unknown',17,7,'p',292,'n.A','n.A','n.A'],#Ts
                ['Oganesson',118,'Unknown',18,7,'p',294,'solid',6.6,'n.A']#Og
                ]

        category_colors = {'Alkali Metal' : '#ffabb5',
                            'Alkaline Earth Metal':'#d5b5e6',
                            'Transition Metal':'#91ccff',
                            'Post-transition Metal':'#b6f58c',
                            'Metalloid':'#acc79b',
                            'Reactive Nonmetal':'#f2f18d',
                            'Noble Gas':'#ffc191',
                            'Unknown':'#c8cfca',
                            'Lanthanide':'#a7f3fa',
                            'Actinide':'#a7fade'}
        self.la_offset = -8
        self.ac_offset = -8

        def make_periodicTable(self,symbol,**kwargs):
            

            outer_self = self
            self.kwargs = kwargs
            self.command= kwargs.pop('command', lambda:print('No command'))
            self.WIDTH,self.HEIGHT,self.BD = 50,50,2
            self.CMP = self.BD*1
            bg = category_colors.get(kwargs.get('element catagory'))

            style = ttk.Style()


            style.configure('table.TFrame', background = bg, foreground = 'black')
            style.configure('table.TLabel', background = bg, foreground = 'black')


            table = ttk.Frame(self.periodicTable_tab, relief = 'raised', style ='table.TFrame' )
            table.configure(width=self.WIDTH,height=self.HEIGHT)
            table.grid_propagate(0)

            self.idx = ttk.Label(table,text=kwargs.get('index'),font=('Arial', 4),style ='table.TLabel') #issue with bg
            #self.u = tk.Label(self,text=kwargs.get('atomic mass'),bg=bg)

            self.name = ttk.Label(table,text=kwargs.get('name'),font=('Arial', 4),style ='table.TLabel')
            symb = ttk.Label(table,text=symbol,font=('bold', 12),style ='table.TLabel')

            

            #self.e = tk.Label(self,text=kwargs.get('electronegativity'),bg=bg)
            #self.d = tk.Label(self,text=kwargs.get('density'),bg=bg)

            table.grid_columnconfigure(1, weight=2)
            table.grid_rowconfigure(1, weight=2)

            self.idx.grid(row=0,column=0,sticky='w')


            mid_x = self.WIDTH/2-self.name.winfo_reqwidth()/2
            mid_y = self.HEIGHT/2-self.name.winfo_reqheight()/2
            offset= 16
            self.name.place(in_=table,x=mid_x-self.CMP,y=mid_y-self.CMP+offset)

            mid_x = self.WIDTH/2-symb.winfo_reqwidth()/2
            mid_y = self.HEIGHT/2-symb.winfo_reqheight()/2
            symb.place(in_=table,x=mid_x-self.CMP,y=mid_y-self.CMP-offset/2)


            r,c = kwargs.pop('period'),kwargs.pop('group')
            self.offset = 2
            offset = 12
            if c in ('La','Ac'):

                if c == 'La':
                    c =self.la_offset+offset

                    self.la_offset +=1
                    r += self.offset


                if c == 'Ac':
                    c =self.ac_offset+offset
                    self.ac_offset +=1
                    r += offset

            table.grid(row=r,column=c,sticky='nswe')


            def in_active(self):
                #if str(event.type) == 'Enter': self.flag = True
                #if str(event.type) == 'Leave':
                self.flag = False;table.configure(relief='raised')


            def indicate(self): #Want to add in GUI to pop up for spectral line selection

                table.configure(relief='sunken')


            def update_element_selection_values(self):
                #Get values from periodic_table file and update the values in the GUI based on element selection and photoelectron line
                #Updates include: BE value, lorentzian width and width range, if the data should be fit as a doublet and if so the spin-orbit splitting and branching ratio. 
                #If the element selected is a transition metal, peak type defaults to Double Lorentzian, else Voigt selected. Other elements that should use Double Lorentzian?
                #Still under development: Which elements/photoelectron lines should have coster-kronig effects and Tougaard background selection along with other backgrounds

                outer_self.count_table += 1
                global element
                global photoelectronLine
                global transitionLine

                #Turning these into arrays for each element 
                element = outer_self.elementArr #self.element_select
                photoelectronLine = outer_self.photoelectronLineArr #self.photoLine_select
                transitionLine = outer_self.transitionLineArr #self.transitionLine_select
                
                self.periodicTable = ElementData(element,photoelectronLine, transitionLine)
                PE_lit, is_singlet, so_split, Br, PE_alt, alt_width, width_range, width, rec_width, default, peakTypes, ck = self.periodicTable.getParams(element,photoelectronLine, transitionLine)

                PE_PT = [0.0]* 10
                width_PT = [0.0]* 10
                width_min = [0.0]* 10
                width_max = [0.0]* 10

              
                for i in range(10):
                
                    if int(round(PE_alt[i])) == 0: 
                        PE_PT[i] = PE_lit[i]
                    else:
                        PE_PT[i] = PE_alt[i]

                    #Default to alt_width, then rec_width, then width
                    if alt_width[i] == 0:
                        width_PT[i] = rec_width[i]
                        if rec_width[i] == 0:
                            width_PT[i] = width[i]
                    else:
                        width_PT[i] = alt_width[i]

                    width_min[i] = -width_range[i]
                    width_max[i] = width_range[i]


                #branching_ratio_PT = Br
                #is_singlet_PT = singlet
                #spinOrbitSplit_PT = so_split
     
                '''
                
                #PE_temp = []
                gamma_temp = []
                gamma_up_temp = []
                gamma_low_temp = []
                br_temp = []
                sos_temp = []
                singlet_temp = []
                peakTypes_temp = []
                ck_temp = []

                gamma_guess = width_PT
                gamma_low = width_min
                gamma_up = width_max
                branching_ratio = Br
                spinOrbitSplit = so_split
                singlet_bool = is_singlet
                peakTypes_val = peakTypes
                ck_val = ck

                outer_self.background_types = [] #Think it is appending one too many baselines when element is selected. Redefine here to empty list 
                
                
                for i in range(10):
                    PE_temp.append(PE_PT)
                    gamma_temp.append(gamma_guess)
                    gamma_up_temp.append(gamma_up)
                    gamma_low_temp.append(gamma_low)
                    br_temp.append(branching_ratio)
                    sos_temp.append(spinOrbitSplit)
                    singlet_temp.append(singlet_bool)
                    peakTypes_temp.append(peakTypes_val)
                    ck_temp.append(ck_val)
                '''
                outer_self.background_types = [] #Think it is appending one too many baselines when element is selected. Redefine here to empty list 
           
                for i in range(10):
                    PE_guesses[i] = DoubleVar(temp_root, PE_PT[i]) 
                    gamma_guesses[i] = DoubleVar(temp_root, width_PT[i]) 
                    gamma_up_lim[i] = DoubleVar(temp_root, width_max[i])
                    gamma_low_lim[i] = DoubleVar(temp_root, width_min[i])
                    #br_guesses[i] = DoubleVar(temp_root, br_temp[i])
                    #sos_guesses[i] = DoubleVar(temp_root, sos_temp[i])
                    singlet[i] = BooleanVar(temp_root, is_singlet[i])
                    peakType[i] = StringVar(temp_root, peakTypes[i])
                    is_coster_kronig[i] = BooleanVar(temp_root, ck[i]) 
         
             
                outer_self.build_fitting_param_tab()
                outer_self.build_param_range_tab()




            def transitionSelect(self,element,absEdge):
                top=self.top=Toplevel(table)
                #absEdge = symb.cget("text")
                selectLine = ttk.Label(top, text='Select Transition:', font='TkTextFont').pack(side='top',  padx=10,  pady=10)
                if self.element == "H" or self.element == "He" or self.element == "Li" or self.element == "Be" or self.element == "B":
                    self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                elif self.element == "C" or self.element == "N" or self.element == "O" or self.element == "F":
                    self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                    self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                    self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                elif self.element == "Ne":
                    self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                    self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                    self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                    self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                elif self.element == "Na" or self.element == "Mg":
                    if absEdge == "K":
                        self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                        self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                        self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                        self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L1":
                        self.L1L2 = Button(top,text='L1L2',command=lambda *args: spectraSelect(self,absEdge,'L1L2')).pack(side='left',  padx=10,  pady=10)
                        self.L1L3 = Button(top,text='L1L3',command=lambda *args: spectraSelect(self,absEdge,'L1L3')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L2":
                        self.L2M1 = Button(top,text='L2M1',command=lambda *args: spectraSelect(self,absEdge,'L2M1')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L3":
                        self.L3M1 = Button(top,text='L3M1',command=lambda *args: spectraSelect(self,absEdge,'L3M1')).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Al" or self.element == "Si" or self.element == "P" or self.element == "S" or self.element == "Cl" or self.element == "Ar":
                    if absEdge == "K":
                        self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                        self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                        self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                        self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                        self.KM2 = Button(top,text='KM2',command=lambda *args: spectraSelect(self,absEdge,'KM2')).pack(side='left',  padx=10,  pady=10)
                        self.KM3 = Button(top,text='KM3',command=lambda *args: spectraSelect(self,absEdge,'KM3')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L1":
                        if self.element == "Al":
                            self.L1L2 = Button(top,text='L1L2',command=lambda *args: spectraSelect(self,absEdge,'L1L2')).pack(side='left',  padx=10,  pady=10)
                            self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                            self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                            self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "P" or self.element == "S" or self.element == "Cl":
                            self.L1L2 = Button(top,text='L1L2',command=lambda *args: spectraSelect(self,absEdge,'L1L2')).pack(side='left',  padx=10,  pady=10)
                            self.L1L3 = Button(top,text='L1L3',command=lambda *args: spectraSelect(self,absEdge,'L1L3')).pack(side='left',  padx=10,  pady=10)
                            self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                            self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                            self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Si" or self.element == "Ar":
                            self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                            self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                            self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L2":
                        self.L2M1 = Button(top,text='L2M1',command=lambda *args: spectraSelect(self,absEdge,'L2M1')).pack(side='left',  padx=10,  pady=10)
                        self.L2M2 = Button(top,text='L2M2',command=lambda *args: spectraSelect(self,absEdge,'L2M2')).pack(side='left',  padx=10,  pady=10)
                        self.L2M3 = Button(top,text='L2M3',command=lambda *args: spectraSelect(self,absEdge,'L2M3')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L3":
                        self.L3M1 = Button(top,text='L3M1',command=lambda *args: spectraSelect(self,absEdge,'L3M1')).pack(side='left',  padx=10,  pady=10)
                        self.L3M2 = Button(top,text='L3M2',command=lambda *args: spectraSelect(self,absEdge,'L3M2')).pack(side='left',  padx=10,  pady=10)
                        self.L3M3 = Button(top,text='L3M3',command=lambda *args: spectraSelect(self,absEdge,'L3M3')).pack(side='left',  padx=10,  pady=10)

                elif self.element == "K" or self.element == "Ca" or self.element == "V" or self.element == "Cr" or self.element == "Mn" or self.element == "Fe" or self.element == "Co" or self.element == "Ni" or self.element == "Cu" or self.element == "Zn":
                    if absEdge == "K":
                        if self.element == "K" or self.element == "Ca" or self.element == "V":
                            self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                            self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                            self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                            self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                            self.KM2 = Button(top,text='KM2',command=lambda *args: spectraSelect(self,absEdge,'KM2')).pack(side='left',  padx=10,  pady=10)
                            self.KM3 = Button(top,text='KM3',command=lambda *args: spectraSelect(self,absEdge,'KM3')).pack(side='left',  padx=10,  pady=10)
                            self.KM4 = Button(top,text='KM4',command=lambda *args: spectraSelect(self,absEdge,'KM4')).pack(side='left',  padx=10,  pady=10)
                            self.KN1 = Button(top,text='KN1',command=lambda *args: spectraSelect(self,absEdge,'KN1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Cr" or self.element == "Mn" or self.element == "Fe" or self.element == "Co" or self.element == "Ni" or self.element == "Cu":
                            self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                            self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                            self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                            self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                            self.KM2 = Button(top,text='KM2',command=lambda *args: spectraSelect(self,absEdge,'KM2')).pack(side='left',  padx=10,  pady=10)
                            self.KM3 = Button(top,text='KM3',command=lambda *args: spectraSelect(self,absEdge,'KM3')).pack(side='left',  padx=10,  pady=10)
                            self.KM4 = Button(top,text='KM4',command=lambda *args: spectraSelect(self,absEdge,'KM4')).pack(side='left',  padx=10,  pady=10)
                            self.KM5 = Button(top,text='KM5',command=lambda *args: spectraSelect(self,absEdge,'KM5')).pack(side='left',  padx=10,  pady=10)
                            self.KN1 = Button(top,text='KN1',command=lambda *args: spectraSelect(self,absEdge,'KN1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Zn":
                            self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                            self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                            self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                            self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                            self.KM2 = Button(top,text='KM2',command=lambda *args: spectraSelect(self,absEdge,'KM2')).pack(side='left',  padx=10,  pady=10)
                            self.KM3 = Button(top,text='KM3',command=lambda *args: spectraSelect(self,absEdge,'KM3')).pack(side='left',  padx=10,  pady=10)
                            self.KM4 = Button(top,text='KM4',command=lambda *args: spectraSelect(self,absEdge,'KM4')).pack(side='left',  padx=10,  pady=10)
                            self.KM5 = Button(top,text='KM5',command=lambda *args: spectraSelect(self,absEdge,'KM5')).pack(side='left',  padx=10,  pady=10)
                            self.KN1 = Button(top,text='KN1',command=lambda *args: spectraSelect(self,absEdge,'KN1')).pack(side='left',  padx=10,  pady=10)
                            self.KN2 = Button(top,text='KN2',command=lambda *args: spectraSelect(self,absEdge,'KN2')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L1":
                        if self.element == "K" or self.element == "Ca":
                            self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                            self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                            self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N1 = Button(top,text='L1N1',command=lambda *args: spectraSelect(self,absEdge,'L1N1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "V" or self.element == "Cr":
                            self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                            self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                            self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                            self.L1M4 = Button(top,text='L1M4',command=lambda *args: spectraSelect(self,absEdge,'L1M4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N1 = Button(top,text='L1N1',command=lambda *args: spectraSelect(self,absEdge,'L1N1')).pack(side='left',  padx=10,  pady=10)
                        else:
                            self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                            self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                            self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                            self.L1M4 = Button(top,text='L1M4',command=lambda *args: spectraSelect(self,absEdge,'L1M4')).pack(side='left',  padx=10,  pady=10)
                            self.L1M5 = Button(top,text='L1M5',command=lambda *args: spectraSelect(self,absEdge,'L1M5')).pack(side='left',  padx=10,  pady=10)
                            self.L1N1 = Button(top,text='L1N1',command=lambda *args: spectraSelect(self,absEdge,'L1N1')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L2":
                        if self.element == "K" or self.element == "Ca":
                            self.L2M1 = Button(top,text='L2M1',command=lambda *args: spectraSelect(self,absEdge,'L2M1')).pack(side='left',  padx=10,  pady=10)
                            self.L2M2 = Button(top,text='L2M2',command=lambda *args: spectraSelect(self,absEdge,'L2M2')).pack(side='left',  padx=10,  pady=10)
                            self.L2M3 = Button(top,text='L2M3',command=lambda *args: spectraSelect(self,absEdge,'L2M3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N1 = Button(top,text='L2N1',command=lambda *args: spectraSelect(self,absEdge,'L2N1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "V" or self.element == "Cr":
                            self.L2M1 = Button(top,text='L2M1',command=lambda *args: spectraSelect(self,absEdge,'L2M1')).pack(side='left',  padx=10,  pady=10)
                            self.L2M2 = Button(top,text='L2M2',command=lambda *args: spectraSelect(self,absEdge,'L2M2')).pack(side='left',  padx=10,  pady=10)
                            self.L2M3 = Button(top,text='L2M3',command=lambda *args: spectraSelect(self,absEdge,'L2M3')).pack(side='left',  padx=10,  pady=10)
                            self.L2M4 = Button(top,text='L2M4',command=lambda *args: spectraSelect(self,absEdge,'L2M4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N1 = Button(top,text='L2N1',command=lambda *args: spectraSelect(self,absEdge,'L2N1')).pack(side='left',  padx=10,  pady=10)
                        else:
                            self.L2M1 = Button(top,text='L2M1',command=lambda *args: spectraSelect(self,absEdge,'L2M1')).pack(side='left',  padx=10,  pady=10)
                            self.L2M2 = Button(top,text='L2M2',command=lambda *args: spectraSelect(self,absEdge,'L2M2')).pack(side='left',  padx=10,  pady=10)
                            self.L2M3 = Button(top,text='L2M3',command=lambda *args: spectraSelect(self,absEdge,'L2M3')).pack(side='left',  padx=10,  pady=10)
                            self.L2M4 = Button(top,text='L2M4',command=lambda *args: spectraSelect(self,absEdge,'L2M4')).pack(side='left',  padx=10,  pady=10)
                            self.L2M5 = Button(top,text='L2M5',command=lambda *args: spectraSelect(self,absEdge,'L2M5')).pack(side='left',  padx=10,  pady=10)
                            self.L2N1 = Button(top,text='L2N1',command=lambda *args: spectraSelect(self,absEdge,'L2N1')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L3":
                        if self.element == "K" or self.element == "Ca":
                            self.L3M1 = Button(top,text='L3M1',command=lambda *args: spectraSelect(self,absEdge,'L3M1')).pack(side='left',  padx=10,  pady=10)
                            self.L3M2 = Button(top,text='L3M2',command=lambda *args: spectraSelect(self,absEdge,'L3M2')).pack(side='left',  padx=10,  pady=10)
                            self.L3M3 = Button(top,text='L3M3',command=lambda *args: spectraSelect(self,absEdge,'L3M3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N1 = Button(top,text='L3N1',command=lambda *args: spectraSelect(self,absEdge,'L3N1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "V" or self.element == "Cr":
                            self.L3M1 = Button(top,text='L3M1',command=lambda *args: spectraSelect(self,absEdge,'L3M1')).pack(side='left',  padx=10,  pady=10)
                            self.L3M2 = Button(top,text='L3M2',command=lambda *args: spectraSelect(self,absEdge,'L3M2')).pack(side='left',  padx=10,  pady=10)
                            self.L3M3 = Button(top,text='L3M3',command=lambda *args: spectraSelect(self,absEdge,'L3M3')).pack(side='left',  padx=10,  pady=10)
                            self.L3M4 = Button(top,text='L3M4',command=lambda *args: spectraSelect(self,absEdge,'L3M4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N1 = Button(top,text='L3N1',command=lambda *args: spectraSelect(self,absEdge,'L3N1')).pack(side='left',  padx=10,  pady=10)
                        else:
                            self.L3M1 = Button(top,text='L3M1',command=lambda *args: spectraSelect(self,absEdge,'L3M1')).pack(side='left',  padx=10,  pady=10)
                            self.L3M2 = Button(top,text='L3M2',command=lambda *args: spectraSelect(self,absEdge,'L3M2')).pack(side='left',  padx=10,  pady=10)
                            self.L3M3 = Button(top,text='L3M3',command=lambda *args: spectraSelect(self,absEdge,'L3M3')).pack(side='left',  padx=10,  pady=10)
                            self.L3M4 = Button(top,text='L3M4',command=lambda *args: spectraSelect(self,absEdge,'L3M4')).pack(side='left',  padx=10,  pady=10)
                            self.L3M5 = Button(top,text='L3M5',command=lambda *args: spectraSelect(self,absEdge,'L3M5')).pack(side='left',  padx=10,  pady=10)
                            self.L3N1 = Button(top,text='L3N1',command=lambda *args: spectraSelect(self,absEdge,'L3N1')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "M2":
                        if self.element == "K" or self.element == "Ca":
                            self.M2N1 = Button(top,text='M2N1',command=lambda *args: spectraSelect(self,absEdge,'M2N1')).pack(side='left',  padx=10,  pady=10)
                        else:
                            self.M2M4 = Button(top,text='M2M4',command=lambda *args: spectraSelect(self,absEdge,'M2M4')).pack(side='left',  padx=10,  pady=10)
                
                elif self.element == "Sc" or self.element == "Ti":
                    if absEdge == "K":
                        self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                        self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                        self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                        self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                        self.KM2 = Button(top,text='KM2',command=lambda *args: spectraSelect(self,absEdge,'KM2')).pack(side='left',  padx=10,  pady=10)
                        self.KM3 = Button(top,text='KM3',command=lambda *args: spectraSelect(self,absEdge,'KM3')).pack(side='left',  padx=10,  pady=10)
                        self.KM4 = Button(top,text='KM4',command=lambda *args: spectraSelect(self,absEdge,'KM4')).pack(side='left',  padx=10,  pady=10)
                        self.KN1 = Button(top,text='KN1',command=lambda *args: spectraSelect(self,absEdge,'KN1')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L1":
                        self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                        self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                        self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                        self.L1M4 = Button(top,text='L1M4',command=lambda *args: spectraSelect(self,absEdge,'L1M4')).pack(side='left',  padx=10,  pady=10)
                        self.L1N1 = Button(top,text='L1N1',command=lambda *args: spectraSelect(self,absEdge,'L1N1')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L2":
                        self.L2M1 = Button(top,text='L2M1',command=lambda *args: spectraSelect(self,absEdge,'L2M1')).pack(side='left',  padx=10,  pady=10)
                        self.L2M2 = Button(top,text='L2M2',command=lambda *args: spectraSelect(self,absEdge,'L2M2')).pack(side='left',  padx=10,  pady=10)
                        self.L2M3 = Button(top,text='L2M3',command=lambda *args: spectraSelect(self,absEdge,'L2M3')).pack(side='left',  padx=10,  pady=10)
                        self.L2M4 = Button(top,text='L2M4',command=lambda *args: spectraSelect(self,absEdge,'L2M4')).pack(side='left',  padx=10,  pady=10)
                        self.L2N1 = Button(top,text='L2N1',command=lambda *args: spectraSelect(self,absEdge,'L2N1')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L3":
                        self.L3M1 = Button(top,text='L3M1',command=lambda *args: spectraSelect(self,absEdge,'L3M1')).pack(side='left',  padx=10,  pady=10)
                        self.L3M2 = Button(top,text='L3M2',command=lambda *args: spectraSelect(self,absEdge,'L3M2')).pack(side='left',  padx=10,  pady=10)
                        self.L3M3 = Button(top,text='L3M3',command=lambda *args: spectraSelect(self,absEdge,'L3M3')).pack(side='left',  padx=10,  pady=10)
                        self.L3M4 = Button(top,text='L3M4',command=lambda *args: spectraSelect(self,absEdge,'L3M4')).pack(side='left',  padx=10,  pady=10)
                        self.L3N1 = Button(top,text='L3N1',command=lambda *args: spectraSelect(self,absEdge,'L3N1')).pack(side='left',  padx=10,  pady=10)
                        

                elif self.element == "Ga" or self.element == "Ge" or self.element == "As" or self.element == "Se" or self.element == "Br" or self.element == "Kr" or self.element == "Rb" or self.element == "Sr" or self.element == "Y" or self.element == "Zr" or self.element == "Nb" or self.element == "Mo" or self.element == "Tc" or self.element == "Ru" or self.element == "Rh" or self.element == "Pd" or self.element == "Ag" or self.element == "Cd" or self.element == "In" or self.element == "Sn" or self.element == "Sb" or self.element == "Te" or self.element == "I" or self.element == "Xe" or self.element == "Cs" or self.element == "Ba" or self.element == "La" or self.element == "Ce" or self.element == "Pr" or self.element == "Nd" or self.element == "Pm" or self.element == "Sm" or self.element == "Eu" or self.element == "Gd" or self.element == "Tb" or self.element == "Dy" or self.element == "Ho" or self.element == "Er" or self.element == "Tm" or self.element == "Yb" or self.element == "Lu" or self.element == "Hf" or self.element == "Ta" or self.element == "W" or self.element == "Re" or self.element == "Os" or self.element == "Ir" or self.element == "Pt" or self.element == "Au" or self.element == "Hg" or self.element == "Tl" or self.element == "Pb" or self.element == "Bi" or self.element == "Po" or self.element == "At" or self.element == "Rn" or self.element == "Fr" or self.element == "Ra" or self.element == "Ac" or self.element == "Th" or self.element == "Pa" or self.element == "U" or self.element == "Np" or self.element == "Pu" or self.element  == "Am" or self.element == "Cm":
                    if absEdge == "K":
                        self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                        self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                        self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                        self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                        self.KM2 = Button(top,text='KM2',command=lambda *args: spectraSelect(self,absEdge,'KM2')).pack(side='left',  padx=10,  pady=10)
                        self.KM3 = Button(top,text='KM3',command=lambda *args: spectraSelect(self,absEdge,'KM3')).pack(side='left',  padx=10,  pady=10)
                        self.KM4 = Button(top,text='KM4',command=lambda *args: spectraSelect(self,absEdge,'KM4')).pack(side='left',  padx=10,  pady=10)
                        self.KM5 = Button(top,text='KM5',command=lambda *args: spectraSelect(self,absEdge,'KM5')).pack(side='left',  padx=10,  pady=10)
                        self.KN1 = Button(top,text='KN1',command=lambda *args: spectraSelect(self,absEdge,'KN1')).pack(side='left',  padx=10,  pady=10)
                        self.KN2 = Button(top,text='KN2',command=lambda *args: spectraSelect(self,absEdge,'KN2')).pack(side='left',  padx=10,  pady=10)
                        self.KN3 = Button(top,text='KN3',command=lambda *args: spectraSelect(self,absEdge,'KN3')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Kr":
                            self.KN4 = Button(top,text='KN4',command=lambda *args: spectraSelect(self,absEdge,'KN4')).pack(side='left',  padx=10,  pady=10)
                            self.KO2 = Button(top,text='KO2',command=lambda *args: spectraSelect(self,absEdge,'KO2')).pack(side='left',  padx=10,  pady=10)
                            self.KP2 = Button(top,text='KP2',command=lambda *args: spectraSelect(self,absEdge,'KP2')).pack(side='left',  padx=10,  pady=10)
                            self.KQ2 = Button(top,text='KQ2',command=lambda *args: spectraSelect(self,absEdge,'KQ2')).pack(side='left',  padx=10,  pady=10)
                            self.KR2 = Button(top,text='KR2',command=lambda *args: spectraSelect(self,absEdge,'KR2')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Rb" or self.element == "Sr":
                            self.KN4 = Button(top,text='KN4',command=lambda *args: spectraSelect(self,absEdge,'KN4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Y" or self.element == "Zr" or self.element == "Nb" or self.element == "Mo" or self.element == "Tc" or self.element == "Ru" or self.element == "Rh" or self.element == "Pd" or self.element == "Ag" or self.element == "Cd" or self.element == "Xe" or self.element == "Cs" or self.element == "Pr" or self.element == "Pm" or self.element == "Po" or self.element == "Rn" or self.element == "Fr" or self.element == "Ra" or self.element == "Ac" or self.element == "Pa" or self.element == "Np" or self.element == "Pu" or self.element  == "Am" or self.element == "Cm":
                            self.KN4 = Button(top,text='KN4',command=lambda *args: spectraSelect(self,absEdge,'KN4')).pack(side='left',  padx=10,  pady=10)
                            self.KN5 = Button(top,text='KN5',command=lambda *args: spectraSelect(self,absEdge,'KN5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "In" or self.element == "Sn" or self.element == "Sb" or self.element == "Te" or self.element == "I" or self.element == "Nd":
                            self.KN4 = Button(top,text='KN4',command=lambda *args: spectraSelect(self,absEdge,'KN4')).pack(side='left',  padx=10,  pady=10)
                            self.KN5 = Button(top,text='KN5',command=lambda *args: spectraSelect(self,absEdge,'KN5')).pack(side='left',  padx=10,  pady=10)
                            self.KO2 = Button(top,text='KO2',command=lambda *args: spectraSelect(self,absEdge,'KO2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ba" or self.element == "La" or self.element == "Ce" or self.element == "Sm" or self.element == "Eu" or self.element == "Gd" or self.element == "Tb" or self.element == "Dy" or self.element == "Ho" or self.element == "Er" or self.element == "Tm" or self.element == "Yb" or self.element == "Lu" or self.element == "Hf" or self.element == "Ta" or self.element == "W" or self.element == "Re" or self.element == "Os" or self.element == "Ir" or self.element == "Pt" or self.element == "Au" or self.element == "Hg" or self.element == "Tl" or self.element == "Pb" or self.element == "Bi" or self.element == "At" or self.element == "Th" or self.element == "U":
                            self.KN4 = Button(top,text='KN4',command=lambda *args: spectraSelect(self,absEdge,'KN4')).pack(side='left',  padx=10,  pady=10)
                            self.KN5 = Button(top,text='KN5',command=lambda *args: spectraSelect(self,absEdge,'KN5')).pack(side='left',  padx=10,  pady=10)
                            self.KO2 = Button(top,text='KO2',command=lambda *args: spectraSelect(self,absEdge,'KO2')).pack(side='left',  padx=10,  pady=10)
                            self.KO3 = Button(top,text='KO3',command=lambda *args: spectraSelect(self,absEdge,'KO3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pb" or self.element == "At" or self.element == "Th" or self.element == "U":
                                self.KP2 = Button(top,text='KP2',command=lambda *args: spectraSelect(self,absEdge,'KP2')).pack(side='left',  padx=10,  pady=10)
                                self.KP3 = Button(top,text='KP3',command=lambda *args: spectraSelect(self,absEdge,'KP3')).pack(side='left',  padx=10,  pady=10)

                    elif absEdge == "L1":
                        self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                        self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                        self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                        self.L1M4 = Button(top,text='L1M4',command=lambda *args: spectraSelect(self,absEdge,'L1M4')).pack(side='left',  padx=10,  pady=10)
                        self.L1M5 = Button(top,text='L1M5',command=lambda *args: spectraSelect(self,absEdge,'L1M5')).pack(side='left',  padx=10,  pady=10)
                        self.L1N1 = Button(top,text='L1N1',command=lambda *args: spectraSelect(self,absEdge,'L1N1')).pack(side='left',  padx=10,  pady=10)
                        self.L1N2 = Button(top,text='L1N2',command=lambda *args: spectraSelect(self,absEdge,'L1N2')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "As" or self.element == "Se" or self.element == "Br" or self.element == "Kr" or self.element == "Rb" or self.element == "Sr":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Y" or self.element == "Zr" or self.element == "Nb":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Mo" or self.element == "Tc" or self.element == "Ru" or self.element == "Rh" or self.element == "Pd" or self.element == "Ag" or self.element == "Cd":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "In" or self.element == "Sn" or self.element == "Sb" or self.element == "Te" or self.element == "I":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                            self.L1O2 = Button(top,text='L1O2',command=lambda *args: spectraSelect(self,absEdge,'L1O2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Cs" or self.element == "Ba":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                            self.L1O2 = Button(top,text='L1O2',command=lambda *args: spectraSelect(self,absEdge,'L1O2')).pack(side='left',  padx=10,  pady=10)
                            self.L1O3 = Button(top,text='L1O3',command=lambda *args: spectraSelect(self,absEdge,'L1O3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Po" or self.element == "At" or self.element == "Rn" or self.element == "Fr" or self.element == "Ac" or self.element  == "Am":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                            self.L1N6 = Button(top,text='L1N6',command=lambda *args: spectraSelect(self,absEdge,'L1N6')).pack(side='left',  padx=10,  pady=10)
                            self.L1N7 = Button(top,text='L1N7',command=lambda *args: spectraSelect(self,absEdge,'L1N7')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Am":
                                self.L1O4 = Button(top,text='L1O4',command=lambda *args: spectraSelect(self,absEdge,'L1O4')).pack(side='left',  padx=10,  pady=10)
                                self.L1O5 = Button(top,text='L1O5',command=lambda *args: spectraSelect(self,absEdge,'L1O5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Nd" or self.element == "Pm":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                            self.L1N6 = Button(top,text='L1N6',command=lambda *args: spectraSelect(self,absEdge,'L1N6')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pm":
                                return
                            self.L1O1 = Button(top,text='L1O1',command=lambda *args: spectraSelect(self,absEdge,'L1O1')).pack(side='left',  padx=10,  pady=10)
                            self.L1O2 = Button(top,text='L1O2',command=lambda *args: spectraSelect(self,absEdge,'L1O2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "La" or self.element == "Ce" or self.element == "Pr" or self.element == "Sm" or self.element == "Eu" or self.element == "Gd" or self.element == "Tb" or self.element == "Dy" or self.element == "Pa" or self.element == "Pu" or self.element == "Cm":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                            self.L1N6 = Button(top,text='L1N6',command=lambda *args: spectraSelect(self,absEdge,'L1N6')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Eu" or self.element == "Gd" or self.element == "Tb" or self.element == "Dy" or self.element == "Pa" or self.element == "Pu" or self.element == "Cm":
                                self.L1N7 = Button(top,text='L1N7',command=lambda *args: spectraSelect(self,absEdge,'L1N7')).pack(side='left',  padx=10,  pady=10)
                            self.L1O2 = Button(top,text='L1O2',command=lambda *args: spectraSelect(self,absEdge,'L1O2')).pack(side='left',  padx=10,  pady=10)
                            self.L1O3 = Button(top,text='L1O3',command=lambda *args: spectraSelect(self,absEdge,'L1O3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Gd" or self.element == "Tb":
                                self.L1O4 = Button(top,text='L1O4',command=lambda *args: spectraSelect(self,absEdge,'L1O4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ho" or self.element == "Er" or self.element == "Tm" or self.element == "Yb" or self.element == "Lu" or self.element == "Hf" or self.element == "Ta" or self.element == "W" or self.element == "Re" or self.element == "Os" or self.element == "Ir" or self.element == "Pt" or self.element == "Au" or self.element == "Hg" or self.element == "Tl" or self.element == "Pb":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                            self.L1N6 = Button(top,text='L1N6',command=lambda *args: spectraSelect(self,absEdge,'L1N6')).pack(side='left',  padx=10,  pady=10)
                            self.L1N7 = Button(top,text='L1N7',command=lambda *args: spectraSelect(self,absEdge,'L1N7')).pack(side='left',  padx=10,  pady=10)
                            self.L1O1 = Button(top,text='L1O1',command=lambda *args: spectraSelect(self,absEdge,'L1O1')).pack(side='left',  padx=10,  pady=10)
                            self.L1O2 = Button(top,text='L1O2',command=lambda *args: spectraSelect(self,absEdge,'L1O2')).pack(side='left',  padx=10,  pady=10)
                            self.L1O3 = Button(top,text='L1O3',command=lambda *args: spectraSelect(self,absEdge,'L1O3')).pack(side='left',  padx=10,  pady=10)
                            self.L1O4 = Button(top,text='L1O4',command=lambda *args: spectraSelect(self,absEdge,'L1O4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Hf" or self.element == "Ta" or self.element == "W" or self.element == "Re" or self.element == "Os" or self.element == "Ir" or self.element == "Pt" or self.element == "Au" or self.element == "Hg" or self.element == "Tl" or self.element == "Pb":
                                self.L1O5 = Button(top,text='L1O5',command=lambda *args: spectraSelect(self,absEdge,'L1O5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Bi" or self.element == "Ra" or self.element == "Th" or self.element == "U" or self.element == "Np":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                            self.L1N6 = Button(top,text='L1N6',command=lambda *args: spectraSelect(self,absEdge,'L1N6')).pack(side='left',  padx=10,  pady=10)
                            self.L1N7 = Button(top,text='L1N7',command=lambda *args: spectraSelect(self,absEdge,'L1N7')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Th":
                                self.L1O1 = Button(top,text='L1O1',command=lambda *args: spectraSelect(self,absEdge,'L1O1')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Ra" or self.element == "Th" or self.element == "U" or self.element == "Np":
                                self.L1O2 = Button(top,text='L1O2',command=lambda *args: spectraSelect(self,absEdge,'L1O2')).pack(side='left',  padx=10,  pady=10)
                                self.L1O3 = Button(top,text='L1O3',command=lambda *args: spectraSelect(self,absEdge,'L1O3')).pack(side='left',  padx=10,  pady=10)
                                self.L1O4 = Button(top,text='L1O4',command=lambda *args: spectraSelect(self,absEdge,'L1O4')).pack(side='left',  padx=10,  pady=10)
                                self.L1O5 = Button(top,text='L1O5',command=lambda *args: spectraSelect(self,absEdge,'L1O5')).pack(side='left',  padx=10,  pady=10)
                                self.L1P2 = Button(top,text='L1P2',command=lambda *args: spectraSelect(self,absEdge,'L1P2')).pack(side='left',  padx=10,  pady=10)
                                self.L1P3 = Button(top,text='L1P3',command=lambda *args: spectraSelect(self,absEdge,'L1P3')).pack(side='left',  padx=10,  pady=10)
                                return
                            self.L1O1 = Button(top,text='L1O1',command=lambda *args: spectraSelect(self,absEdge,'L1O1')).pack(side='left',  padx=10,  pady=10)
                            self.L1O2 = Button(top,text='L1O2',command=lambda *args: spectraSelect(self,absEdge,'L1O2')).pack(side='left',  padx=10,  pady=10)
                            self.L1O3 = Button(top,text='L1O3',command=lambda *args: spectraSelect(self,absEdge,'L1O3')).pack(side='left',  padx=10,  pady=10)
                            self.L1O4 = Button(top,text='L1O4',command=lambda *args: spectraSelect(self,absEdge,'L1O4')).pack(side='left',  padx=10,  pady=10)
                            self.L1O5 = Button(top,text='L1O5',command=lambda *args: spectraSelect(self,absEdge,'L1O5')).pack(side='left',  padx=10,  pady=10)
                            self.L1P1 = Button(top,text='L1P1',command=lambda *args: spectraSelect(self,absEdge,'L1P1')).pack(side='left',  padx=10,  pady=10)
                            self.L1P2 = Button(top,text='L1P2',command=lambda *args: spectraSelect(self,absEdge,'L1P2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Xe":
                            self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                            self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                            self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                            self.L1P2 = Button(top,text='L1P2',command=lambda *args: spectraSelect(self,absEdge,'L1P2')).pack(side='left',  padx=10,  pady=10)
                            self.L1Q2 = Button(top,text='L1Q2',command=lambda *args: spectraSelect(self,absEdge,'L1Q2')).pack(side='left',  padx=10,  pady=10)
                            self.L1R2 = Button(top,text='L1R2',command=lambda *args: spectraSelect(self,absEdge,'L1R2')).pack(side='left',  padx=10,  pady=10)
                            self.L1S2 = Button(top,text='L1S2',command=lambda *args: spectraSelect(self,absEdge,'L1S2')).pack(side='left',  padx=10,  pady=10)

                    elif absEdge == "L2":
                        self.L2M1 = Button(top,text='L2M1',command=lambda *args: spectraSelect(self,absEdge,'L2M1')).pack(side='left',  padx=10,  pady=10)
                        self.L2M2 = Button(top,text='L2M2',command=lambda *args: spectraSelect(self,absEdge,'L2M2')).pack(side='left',  padx=10,  pady=10)
                        self.L2M3 = Button(top,text='L2M3',command=lambda *args: spectraSelect(self,absEdge,'L2M3')).pack(side='left',  padx=10,  pady=10)
                        self.L2M4 = Button(top,text='L2M4',command=lambda *args: spectraSelect(self,absEdge,'L2M4')).pack(side='left',  padx=10,  pady=10)
                        self.L2M5 = Button(top,text='L2M5',command=lambda *args: spectraSelect(self,absEdge,'L2M5')).pack(side='left',  padx=10,  pady=10)
                        self.L2N1 = Button(top,text='L2N1',command=lambda *args: spectraSelect(self,absEdge,'L2N1')).pack(side='left',  padx=10,  pady=10)
                        self.L2N2 = Button(top,text='L2N2',command=lambda *args: spectraSelect(self,absEdge,'L2N2')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "As" or self.element == "Se" or self.element == "Br" or self.element == "Kr" or self.element == "Rb" or self.element == "Sr":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Y" or self.element == "Zr" or self.element == "Nb":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Mo" or self.element == "Tc" or self.element == "Ru" or self.element == "Rh" or self.element == "Pd" or self.element == "Ag" or self.element == "Cd" or self.element == "In" or self.element == "Sn" or self.element == "Sb" or self.element == "Te" or self.element == "I" or self.element == "Cs":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ba":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                            self.L2O1 = Button(top,text='L2O1',command=lambda *args: spectraSelect(self,absEdge,'L2O1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "La" or self.element == "Pm":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                            self.L2N6 = Button(top,text='L2N6',command=lambda *args: spectraSelect(self,absEdge,'L2N6')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pm":
                                return
                            self.L2O2 = Button(top,text='L2O2',command=lambda *args: spectraSelect(self,absEdge,'L2O2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ce":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                            self.L2N6 = Button(top,text='L2N6',command=lambda *args: spectraSelect(self,absEdge,'L2N6')).pack(side='left',  padx=10,  pady=10)
                            self.L2O1 = Button(top,text='L2O1',command=lambda *args: spectraSelect(self,absEdge,'L2O1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Pr" or self.element == "Eu" or self.element == "Gd" or self.element == "Tb" or self.element == "Dy" or self.element == "Ho" or self.element == "Tm" or self.element == "Re" or self.element == "Os" or self.element == "Bi" or self.element == "At" or self.element == "Rn" or self.element == "Fr" or self.element == "Ac" or self.element == "Pa" or self.element == "U" or self.element == "Am" or self.element == "Cm":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                            self.L2N6 = Button(top,text='L2N6',command=lambda *args: spectraSelect(self,absEdge,'L2N6')).pack(side='left',  padx=10,  pady=10)
                            self.L2N7 = Button(top,text='L2N7',command=lambda *args: spectraSelect(self,absEdge,'L2N7')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pa" or self.element == "Am" or self.element == "Cm":
                                self.L2O4 = Button(top,text='L2O4',command=lambda *args: spectraSelect(self,absEdge,'L2O4')).pack(side='left',  padx=10,  pady=10)
                                return
                            if self.element == "At" or self.element == "Rn" or self.element == "Fr" or self.element == "Ac":
                                return
                            self.L2O1 = Button(top,text='L2O1',command=lambda *args: spectraSelect(self,absEdge,'L2O1')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Eu":
                                self.L2O2 = Button(top,text='L2O2',command=lambda *args: spectraSelect(self,absEdge,'L2O2')).pack(side='left',  padx=10,  pady=10)
                                self.L2O4 = Button(top,text='L2O4',command=lambda *args: spectraSelect(self,absEdge,'L2O4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Re" or self.element == "Os" or self.element == "Bi" or self.element == "U":
                                self.L2O3 = Button(top,text='L2O3',command=lambda *args: spectraSelect(self,absEdge,'L2O3')).pack(side='left',  padx=10,  pady=10)
                                self.L2O4 = Button(top,text='L2O4',command=lambda *args: spectraSelect(self,absEdge,'L2O4')).pack(side='left',  padx=10,  pady=10)
                                if self.element == "U":
                                    self.L2P2 = Button(top,text='L2P2',command=lambda *args: spectraSelect(self,absEdge,'L2P2')).pack(side='left',  padx=10,  pady=10)
                                    self.L2P3 = Button(top,text='L2P3',command=lambda *args: spectraSelect(self,absEdge,'L2P3')).pack(side='left',  padx=10,  pady=10)
                                    self.L2P4 = Button(top,text='L2P4',command=lambda *args: spectraSelect(self,absEdge,'L2P4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Gd" or self.element == "Tb" or self.element == "Dy" or self.element == "Ho" or self.element == "Tm":
                                self.L2O4 = Button(top,text='L2O4',command=lambda *args: spectraSelect(self,absEdge,'L2O4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Nd" or self.element == "Sm" or self.element == "W" or self.element == "Pt" or self.element == "Tl" or self.element == "Po":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                            self.L2N6 = Button(top,text='L2N6',command=lambda *args: spectraSelect(self,absEdge,'L2N6')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "W" or self.element == "Pt" or self.element == "Tl" or self.element == "Po":
                                self.L2N7 = Button(top,text='L2N7',command=lambda *args: spectraSelect(self,absEdge,'L2N7')).pack(side='left',  padx=10,  pady=10)
                            self.L2O1 = Button(top,text='L2O1',command=lambda *args: spectraSelect(self,absEdge,'L2O1')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pt" or self.element == "Po":
                                self.L2O4 = Button(top,text='L2O4',command=lambda *args: spectraSelect(self,absEdge,'L2O4')).pack(side='left',  padx=10,  pady=10)
                                return
                            self.L2O2 = Button(top,text='L2O2',command=lambda *args: spectraSelect(self,absEdge,'L2O2')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Sm" or self.element == "W" or self.element == "Tl":
                                self.L2O4 = Button(top,text='L2O4',command=lambda *args: spectraSelect(self,absEdge,'L2O4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Er" or self.element == "Yb" or self.element == "Lu" or self.element == "Hf" or self.element == "Ta" or self.element == "Ir" or self.element == "Au" or self.element == "Hg" or self.element == "Ra" or self.element == "Th" or self.element == "Np" or self.element == "Pu":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                            self.L2N6 = Button(top,text='L2N6',command=lambda *args: spectraSelect(self,absEdge,'L2N6')).pack(side='left',  padx=10,  pady=10)
                            self.L2N7 = Button(top,text='L2N7',command=lambda *args: spectraSelect(self,absEdge,'L2N7')).pack(side='left',  padx=10,  pady=10)
                            self.L2O1 = Button(top,text='L2O1',command=lambda *args: spectraSelect(self,absEdge,'L2O1')).pack(side='left',  padx=10,  pady=10)
                            self.L2O2 = Button(top,text='L2O2',command=lambda *args: spectraSelect(self,absEdge,'L2O2')).pack(side='left',  padx=10,  pady=10)
                            self.L2O3 = Button(top,text='L2O3',command=lambda *args: spectraSelect(self,absEdge,'L2O3')).pack(side='left',  padx=10,  pady=10)
                            self.L2O4 = Button(top,text='L2O4',command=lambda *args: spectraSelect(self,absEdge,'L2O4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Ra" or self.element == "Th":
                                self.L2P1 = Button(top,text='L2P1',command=lambda *args: spectraSelect(self,absEdge,'L2P1')).pack(side='left',  padx=10,  pady=10)
                                self.L2P2 = Button(top,text='L2P2',command=lambda *args: spectraSelect(self,absEdge,'L2P2')).pack(side='left',  padx=10,  pady=10)
                                self.L2P3 = Button(top,text='L2P3',command=lambda *args: spectraSelect(self,absEdge,'L2P3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Th":
                                self.L2P4 = Button(top,text='L2P4',command=lambda *args: spectraSelect(self,absEdge,'L2P4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Hg" or self.element == "Np":
                                self.L2P1 = Button(top,text='L2P1',command=lambda *args: spectraSelect(self,absEdge,'L2P1')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Np":
                                self.L2P4 = Button(top,text='L2P4',command=lambda *args: spectraSelect(self,absEdge,'L2P4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Pb":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                            self.L2N6 = Button(top,text='L2N6',command=lambda *args: spectraSelect(self,absEdge,'L2N6')).pack(side='left',  padx=10,  pady=10)
                            self.L2N7 = Button(top,text='L2N7',command=lambda *args: spectraSelect(self,absEdge,'L2N7')).pack(side='left',  padx=10,  pady=10)
                            self.L2O1 = Button(top,text='L2O1',command=lambda *args: spectraSelect(self,absEdge,'L2O1')).pack(side='left',  padx=10,  pady=10)
                            self.L2O3 = Button(top,text='L2O3',command=lambda *args: spectraSelect(self,absEdge,'L2O3')).pack(side='left',  padx=10,  pady=10)
                            self.L2O4 = Button(top,text='L2O4',command=lambda *args: spectraSelect(self,absEdge,'L2O4')).pack(side='left',  padx=10,  pady=10)
                            self.L2P1 = Button(top,text='L2P1',command=lambda *args: spectraSelect(self,absEdge,'L2P1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Xe":
                            self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                            self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                            self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                            self.L2P1 = Button(top,text='L2P1',command=lambda *args: spectraSelect(self,absEdge,'L2P1')).pack(side='left',  padx=10,  pady=10)
                            self.L2P4 = Button(top,text='L2P4',command=lambda *args: spectraSelect(self,absEdge,'L2P4')).pack(side='left',  padx=10,  pady=10)
                            self.L2Q4 = Button(top,text='L2Q4',command=lambda *args: spectraSelect(self,absEdge,'L2Q4')).pack(side='left',  padx=10,  pady=10)


                    elif absEdge == "L3":
                        self.L3M1 = Button(top,text='L3M1',command=lambda *args: spectraSelect(self,absEdge,'L3M1')).pack(side='left',  padx=10,  pady=10)
                        self.L3M2 = Button(top,text='L3M2',command=lambda *args: spectraSelect(self,absEdge,'L3M2')).pack(side='left',  padx=10,  pady=10)
                        self.L3M3 = Button(top,text='L3M3',command=lambda *args: spectraSelect(self,absEdge,'L3M3')).pack(side='left',  padx=10,  pady=10)
                        self.L3M4 = Button(top,text='L3M4',command=lambda *args: spectraSelect(self,absEdge,'L3M4')).pack(side='left',  padx=10,  pady=10)
                        self.L3M5 = Button(top,text='L3M5',command=lambda *args: spectraSelect(self,absEdge,'L3M5')).pack(side='left',  padx=10,  pady=10)
                        self.L3N1 = Button(top,text='L3N1',command=lambda *args: spectraSelect(self,absEdge,'L3N1')).pack(side='left',  padx=10,  pady=10)
                        self.L3N2 = Button(top,text='L3N2',command=lambda *args: spectraSelect(self,absEdge,'L3N2')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "As" or self.element == "Se" or self.element == "Br" or self.element == "Kr" or self.element == "Rb" or self.element == "Sr":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Y" or self.element == "Zr":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Nb" or self.element == "Mo" or self.element == "Tc" or self.element == "Ru" or self.element == "Rh" or self.element == "Pd" or self.element == "Ag" or self.element == "Cd":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "In" or self.element == "Sn" or self.element == "Sb" or self.element == "Te" or self.element == "I" or self.element == "Cs" or self.element == "Ba":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3O1 = Button(top,text='L3O1',command=lambda *args: spectraSelect(self,absEdge,'L3O1')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "La" or self.element == "Pm":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3N6 = Button(top,text='L3N6',command=lambda *args: spectraSelect(self,absEdge,'L3N6')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pm":
                                return
                            self.L3N7 = Button(top,text='L3N7',command=lambda *args: spectraSelect(self,absEdge,'L3N7')).pack(side='left',  padx=10,  pady=10)
                            self.L3O2 = Button(top,text='L3O2',command=lambda *args: spectraSelect(self,absEdge,'L3O2')).pack(side='left',  padx=10,  pady=10)
                            self.L3O3 = Button(top,text='L3O3',command=lambda *args: spectraSelect(self,absEdge,'L3O3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "La" or self.element == "Pr" or self.element == "Nd" or self.element == "Eu" or self.element == "Dy" or self.element == "Ho" or self.element == "W" or self.element == "Po" or self.element == "At" or self.element == "Rn" or self.element == "Fr" or self.element == "Ac" or self.element == "Am" or self.element == "Cm":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3N6 = Button(top,text='L3N6',command=lambda *args: spectraSelect(self,absEdge,'L3N6')).pack(side='left',  padx=10,  pady=10)
                            self.L3N7 = Button(top,text='L3N7',command=lambda *args: spectraSelect(self,absEdge,'L3N7')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "At" or self.element == "Rn" or self.element == "Fr" or self.element == "Ac" or self.element == "Cm":
                                return
                            if self.element == "Ho" or self.element == "Po" or self.element == "Am":
                                self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                                if self.element == "Po" or self.element == "Am":
                                    self.L3O5 = Button(top,text='L3O5',command=lambda *args: spectraSelect(self,absEdge,'L3O5')).pack(side='left',  padx=10,  pady=10)
                                return
                            self.L3O1 = Button(top,text='L3O1',command=lambda *args: spectraSelect(self,absEdge,'L3O1')).pack(side='left',  padx=10,  pady=10)
                            self.L3O2 = Button(top,text='L3O2',command=lambda *args: spectraSelect(self,absEdge,'L3O2')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Eu":
                                self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                                return
                            if self.element == "Nd":
                                return
                            self.L3O3 = Button(top,text='L3O3',command=lambda *args: spectraSelect(self,absEdge,'L3O3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Dy" or self.element == "W":
                                self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Cs:":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3O1 = Button(top,text='L3O1',command=lambda *args: spectraSelect(self,absEdge,'L3O1')).pack(side='left',  padx=10,  pady=10)
                            self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Sm":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3N6 = Button(top,text='L3N6',command=lambda *args: spectraSelect(self,absEdge,'L3N6')).pack(side='left',  padx=10,  pady=10)
                            self.L3O1 = Button(top,text='L3O1',command=lambda *args: spectraSelect(self,absEdge,'L3O1')).pack(side='left',  padx=10,  pady=10)
                            self.L3O2 = Button(top,text='L3O2',command=lambda *args: spectraSelect(self,absEdge,'L3O2')).pack(side='left',  padx=10,  pady=10)
                            self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Gd" or self.element == "Tb" or self.element == "Er" or self.element == "Tm" or self.element == "Yb" or self.element == "Lu" or self.element == "Hf" or self.element == "Ta" or self.element == "Re" or self.element == "Os" or self.element == "Ra" or self.element == "Pa" or self.element == "Np" or self.element == "Pu":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3N6 = Button(top,text='L3N6',command=lambda *args: spectraSelect(self,absEdge,'L3N6')).pack(side='left',  padx=10,  pady=10)
                            self.L3N7 = Button(top,text='L3N7',command=lambda *args: spectraSelect(self,absEdge,'L3N7')).pack(side='left',  padx=10,  pady=10)
                            self.L3O1 = Button(top,text='L3O1',command=lambda *args: spectraSelect(self,absEdge,'L3O1')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Yb" or self.element == "Lu" or self.element == "Hf" or self.element == "Ta" or self.element == "Np":
                                self.L3O2 = Button(top,text='L3O2',command=lambda *args: spectraSelect(self,absEdge,'L3O2')).pack(side='left',  padx=10,  pady=10)
                                self.L3O3 = Button(top,text='L3O3',command=lambda *args: spectraSelect(self,absEdge,'L3O3')).pack(side='left',  padx=10,  pady=10)
                            self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pa" or self.element == "Np" or self.element == "Pu":
                                self.L3O5 = Button(top,text='L3O5',command=lambda *args: spectraSelect(self,absEdge,'L3O5')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Ra":
                                self.L3O5 = Button(top,text='L3O5',command=lambda *args: spectraSelect(self,absEdge,'L3O5')).pack(side='left',  padx=10,  pady=10)
                                self.L3P2 = Button(top,text='L3P2',command=lambda *args: spectraSelect(self,absEdge,'L3P2')).pack(side='left',  padx=10,  pady=10)
                                self.L3P3 = Button(top,text='L3P3',command=lambda *args: spectraSelect(self,absEdge,'L3P3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ir" or self.element == "Pt" or self.element == "Hg" or self.element == "U":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3N6 = Button(top,text='L3N6',command=lambda *args: spectraSelect(self,absEdge,'L3N6')).pack(side='left',  padx=10,  pady=10)
                            self.L3N7 = Button(top,text='L3N7',command=lambda *args: spectraSelect(self,absEdge,'L3N7')).pack(side='left',  padx=10,  pady=10)
                            self.L3O1 = Button(top,text='L3O1',command=lambda *args: spectraSelect(self,absEdge,'L3O1')).pack(side='left',  padx=10,  pady=10)
                            self.L3O2 = Button(top,text='L3O2',command=lambda *args: spectraSelect(self,absEdge,'L3O2')).pack(side='left',  padx=10,  pady=10)
                            self.L3O3 = Button(top,text='L3O3',command=lambda *args: spectraSelect(self,absEdge,'L3O3')).pack(side='left',  padx=10,  pady=10)
                            self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "U":
                                self.L3P2 = Button(top,text='L3P2',command=lambda *args: spectraSelect(self,absEdge,'L3P2')).pack(side='left',  padx=10,  pady=10)
                                self.L3P3 = Button(top,text='L3P3',command=lambda *args: spectraSelect(self,absEdge,'L3P3')).pack(side='left',  padx=10,  pady=10)
                                self.L3P4 = Button(top,text='L3P4',command=lambda *args: spectraSelect(self,absEdge,'L3P4')).pack(side='left',  padx=10,  pady=10)
                            self.L3O5 = Button(top,text='L3O5',command=lambda *args: spectraSelect(self,absEdge,'L3O5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Au" or self.element == "Tl" or self.element == "Pb" or self.element == "Bi" or self.element == "Th":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3N6 = Button(top,text='L3N6',command=lambda *args: spectraSelect(self,absEdge,'L3N6')).pack(side='left',  padx=10,  pady=10)
                            self.L3N7 = Button(top,text='L3N7',command=lambda *args: spectraSelect(self,absEdge,'L3N7')).pack(side='left',  padx=10,  pady=10)
                            self.L3O1 = Button(top,text='L3O1',command=lambda *args: spectraSelect(self,absEdge,'L3O1')).pack(side='left',  padx=10,  pady=10)
                            self.L3O2 = Button(top,text='L3O2',command=lambda *args: spectraSelect(self,absEdge,'L3O2')).pack(side='left',  padx=10,  pady=10)
                            self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                            self.L3O5 = Button(top,text='L3O5',command=lambda *args: spectraSelect(self,absEdge,'L3O5')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Bi":
                                self.L3P2 = Button(top,text='L3P2',command=lambda *args: spectraSelect(self,absEdge,'L3P2')).pack(side='left',  padx=10,  pady=10)
                                self.L3P3 = Button(top,text='L3P3',command=lambda *args: spectraSelect(self,absEdge,'L3P3')).pack(side='left',  padx=10,  pady=10)
                            self.L3P1 = Button(top,text='L3P1',command=lambda *args: spectraSelect(self,absEdge,'L3P1')).pack(side='left',  padx=10,  pady=10)
                            self.L3P2 = Button(top,text='L3P2',command=lambda *args: spectraSelect(self,absEdge,'L3P2')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pb" or self.element == "Th":
                                self.L3P3 = Button(top,text='L3P3',command=lambda *args: spectraSelect(self,absEdge,'L3P3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Th":
                                self.L3P4 = Button(top,text='L3P4',command=lambda *args: spectraSelect(self,absEdge,'L3P4')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Xe":
                            self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                            self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                            self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                            self.L3O4 = Button(top,text='L3O4',command=lambda *args: spectraSelect(self,absEdge,'L3O4')).pack(side='left',  padx=10,  pady=10)
                            self.L3P1 = Button(top,text='L3P1',command=lambda *args: spectraSelect(self,absEdge,'L3P1')).pack(side='left',  padx=10,  pady=10)
                            self.L3P4 = Button(top,text='L3P4',command=lambda *args: spectraSelect(self,absEdge,'L3P4')).pack(side='left',  padx=10,  pady=10)
                            self.L3Q4 = Button(top,text='L3Q4',command=lambda *args: spectraSelect(self,absEdge,'L3Q4')).pack(side='left',  padx=10,  pady=10)
                    
                    elif absEdge == "M1":
                        if self.element == "Br":
                            self.M1M2 = Button(top,text='M1M2',command=lambda *args: spectraSelect(self,absEdge,'M1M2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Nb" or self.element == "Mo" or self.element == "Pd" or self.element == "Ag" or self.element == "Bi" or self.element == "Th" or self.element == "U":
                            self.M1N2 = Button(top,text='M1N2',command=lambda *args: spectraSelect(self,absEdge,'M1N2')).pack(side='left',  padx=10,  pady=10)
                            self.M1N3 = Button(top,text='M1N3',command=lambda *args: spectraSelect(self,absEdge,'M1N3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Th" or self.element == "U":
                                self.M1O3 = Button(top,text='M1O3',command=lambda *args: spectraSelect(self,absEdge,'M1O3')).pack(side='left',  padx=10,  pady=10)
                                if self.element == "U":
                                    self.M1P3 = Button(top,text='M1P3',command=lambda *args: spectraSelect(self,absEdge,'M1P3')).pack(side='left',  padx=10,  pady=10)
                            return
                        elif self.element == "Ta" or self.element == "W" or self.element == "Os" or self.element == "Ir" or self.element == "Pt" or self.element == "Au" or self.element == "Tl" or self.element == "Pb":
                            self.M1N3 = Button(top,text='M1N3',command=lambda *args: spectraSelect(self,absEdge,'M1N3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "W":
                                self.M1O2 = Button(top,text='M1O2',command=lambda *args: spectraSelect(self,absEdge,'M1O2')).pack(side='left',  padx=10,  pady=10)
                                self.M1O3 = Button(top,text='M1O3',command=lambda *args: spectraSelect(self,absEdge,'M1O3')).pack(side='left',  padx=10,  pady=10)
                            return
                        elif self.element == "Sn" or self.element == "Sb" or self.element == "Te":
                            self.M1P3 = Button(top,text='M1P3',command=lambda *args: spectraSelect(self,absEdge,'M1P3')).pack(side='left',  padx=10,  pady=10)
                            return
                        self.M1M3 = Button(top,text='M1M3',command=lambda *args: spectraSelect(self,absEdge,'M1M3')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Np":
                            self.M1N2 = Button(top,text='M1N2',command=lambda *args: spectraSelect(self,absEdge,'M1N2')).pack(side='left',  padx=10,  pady=10)
                            self.M1N3 = Button(top,text='M1N3',command=lambda *args: spectraSelect(self,absEdge,'M1N3')).pack(side='left',  padx=10,  pady=10)
                            self.M1O2 = Button(top,text='M1O2',command=lambda *args: spectraSelect(self,absEdge,'M1O2')).pack(side='left',  padx=10,  pady=10)
                            self.M1O3 = Button(top,text='M1O3',command=lambda *args: spectraSelect(self,absEdge,'M1O3')).pack(side='left',  padx=10,  pady=10)
                            self.M1P2 = Button(top,text='M1P2',command=lambda *args: spectraSelect(self,absEdge,'M1P2')).pack(side='left',  padx=10,  pady=10)
                            self.M1P3 = Button(top,text='M1P3',command=lambda *args: spectraSelect(self,absEdge,'M1P3')).pack(side='left',  padx=10,  pady=10)
                    
                    elif absEdge == "M2":
                        if self.element == "Br" or self.element == "Rb" or self.element == "Sr" or self.element == "Y" or self.element == "Nb" or self.element == "Mo" or self.element == "Ru" or self.element == "Rh" or self.element == "Pd":
                            self.M2M4 = Button(top,text='M2M4',command=lambda *args: spectraSelect(self,absEdge,'M2M4')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Zr":
                            self.M2M4 = Button(top,text='M2M4',command=lambda *args: spectraSelect(self,absEdge,'M2M4')).pack(side='left',  padx=10,  pady=10)
                            return
                        if self.element == "Er" or self.element == "Ta" or self.element == "Ir" or self.element == "Pt" or self.element == "Au" or self.element == "Tl" or self.element == "Bi":
                            self.M2N4 = Button(top,text='M2N4',command=lambda *args: spectraSelect(self,absEdge,'M2N4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Tl":
                                self.M2O4 = Button(top,text='M2O4',command=lambda *args: spectraSelect(self,absEdge,'M2O4')).pack(side='left',  padx=10,  pady=10)
                            return
                        self.M2N1 = Button(top,text='M2N1',command=lambda *args: spectraSelect(self,absEdge,'M2N1')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Nb" or self.element == "Ru" or self.element == "Pd" or self.element == "Ag" or self.element == "Sn" or self.element == "Sb" or self.element == "Cs" or self.element == "Ba" or self.element == "La" or self.element == "Ce" or self.element == "Os":
                            if self.element == "Ag":
                                self.M2M4 = Button(top,text='M2M4',command=lambda *args: spectraSelect(self,absEdge,'M2M4')).pack(side='left',  padx=10,  pady=10)
                            self.M2N4 = Button(top,text='M2N4',command=lambda *args: spectraSelect(self,absEdge,'M2N4')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Cd":
                            self.M2N4 = Button(top,text='M2N4',command=lambda *args: spectraSelect(self,absEdge,'M2N4')).pack(side='left',  padx=10,  pady=10)
                            self.M2N5 = Button(top,text='M2N5',command=lambda *args: spectraSelect(self,absEdge,'M2N5')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "W" or self.element == "Pb" or self.element == "Th" or self.element == "Pa" or self.element == "Am":
                            self.M2N4 = Button(top,text='M2N4',command=lambda *args: spectraSelect(self,absEdge,'M2N4')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pb" or self.element == "Th" or self.element == "Pa":
                                self.M2O4 = Button(top,text='M2O4',command=lambda *args: spectraSelect(self,absEdge,'M2O4')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "U" or self.element == "Np":
                            self.M2N4 = Button(top,text='M2N4',command=lambda *args: spectraSelect(self,absEdge,'M2N4')).pack(side='left',  padx=10,  pady=10)
                            self.M2O1 = Button(top,text='M2O1',command=lambda *args: spectraSelect(self,absEdge,'M2O1')).pack(side='left',  padx=10,  pady=10)
                            self.M2O4 = Button(top,text='M2O4',command=lambda *args: spectraSelect(self,absEdge,'M2O4')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Np":
                            self.M2P1 = Button(top,text='M2P1',command=lambda *args: spectraSelect(self,absEdge,'M2P1')).pack(side='left',  padx=10,  pady=10)
                            self.M2Q1 = Button(top,text='M2Q1',command=lambda *args: spectraSelect(self,absEdge,'M2Q1')).pack(side='left',  padx=10,  pady=10)

                    elif absEdge == "M3":
                        if self.element == "Br" or self.element == "Rb" or self.element == "Sr" or self.element == "Y" or self.element == "Tc" or self.element == "Np":
                            self.M3M4 = Button(top,text='M3M4',command=lambda *args: spectraSelect(self,absEdge,'M3M4')).pack(side='left',  padx=10,  pady=10)
                            self.M3M5 = Button(top,text='M3M5',command=lambda *args: spectraSelect(self,absEdge,'M3M5')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Tc":
                                return
                        if self.element == "Zr" or self.element == "Ru":
                            self.M3M5 = Button(top,text='M3M5',command=lambda *args: spectraSelect(self,absEdge,'M3M5')).pack(side='left',  padx=10,  pady=10)
                            self.M3N4 = Button(top,text='M3N4',command=lambda *args: spectraSelect(self,absEdge,'M3N4')).pack(side='left',  padx=10,  pady=10)
                            self.M3N5 = Button(top,text='M3N5',command=lambda *args: spectraSelect(self,absEdge,'M3N5')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Ru":
                                return
                        if self.element == "Nb" or self.element == "Mo" or self.element == "Pd" or self.element == "Ag" or self.element == "Cd" or self.element == "Sb" or self.element == "Te":
                            self.M3M5 = Button(top,text='M3M5',command=lambda *args: spectraSelect(self,absEdge,'M3M5')).pack(side='left',  padx=10,  pady=10)
                            self.M3N1 = Button(top,text='M3N1',command=lambda *args: spectraSelect(self,absEdge,'M3N1')).pack(side='left',  padx=10,  pady=10)
                            self.M3N4 = Button(top,text='M3N4',command=lambda *args: spectraSelect(self,absEdge,'M3N4')).pack(side='left',  padx=10,  pady=10)
                            self.M3N5 = Button(top,text='M3N5',command=lambda *args: spectraSelect(self,absEdge,'M3N5')).pack(side='left',  padx=10,  pady=10)
                            return
                        if self.element == "Rh":
                            self.M3M4 = Button(top,text='M3M5',command=lambda *args: spectraSelect(self,absEdge,'M3M5')).pack(side='left',  padx=10,  pady=10)
                            self.M3N1 = Button(top,text='M3N1',command=lambda *args: spectraSelect(self,absEdge,'M3N1')).pack(side='left',  padx=10,  pady=10)
                            self.M3N4 = Button(top,text='M3N4',command=lambda *args: spectraSelect(self,absEdge,'M3N4')).pack(side='left',  padx=10,  pady=10)
                            self.M3N5 = Button(top,text='M3N5',command=lambda *args: spectraSelect(self,absEdge,'M3N5')).pack(side='left',  padx=10,  pady=10)
                            return
                        if self.element == "In" or self.element == "I" or self.element == "Xe" or self.element == "La" or self.element == "Pr" or self.element == "Nd" or self.element == "Pm" or self.element == "Sm" or self.element == "Eu" or self.element == "Gd" or self.element == "Tb" or self.element == "Dy" or self.element == "Ho" or self.element == "Er" or self.element == "Tm" or self.element == "Lu" or self.element == "Re" or self.element == "Po" or self.element == "At" or self.element == "Rn" or self.element == "Fr" or self.element == "Ra" or self.element == "Ac" or self.element == "Pu" or self.element == "Am":
                            self.M3N4 = Button(top,text='M3N4',command=lambda *args: spectraSelect(self,absEdge,'M3N4')).pack(side='left',  padx=10,  pady=10)
                            self.M3N5 = Button(top,text='M3N5',command=lambda *args: spectraSelect(self,absEdge,'M3N5')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pu" or self.element == "Am":
                                self.M3O1 = Button(top,text='M3O1',command=lambda *args: spectraSelect(self,absEdge,'M3O1')).pack(side='left',  padx=10,  pady=10)
                                self.M3O5 = Button(top,text='M3O5',command=lambda *args: spectraSelect(self,absEdge,'M3O5')).pack(side='left',  padx=10,  pady=10)
                            return
                        self.M3N1 = Button(top,text='M3N1',command=lambda *args: spectraSelect(self,absEdge,'M3N1')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Sn" or self.element == "Cs" or self.element == "Ba" or self.element == "Ce" or self.element == "Yb" or self.element == "Hf" or self.element == "Os" or self.element == "Ir" or self.element == "Hg" or self.element == "Tl" or self.element == "Pb" or self.element == "Bi" or self.element == "Th" or self.element == "Pa" or self.element == "Np":
                            self.M3N4 = Button(top,text='M3N4',command=lambda *args: spectraSelect(self,absEdge,'M3N4')).pack(side='left',  padx=10,  pady=10)
                            self.M3N5 = Button(top,text='M3N5',command=lambda *args: spectraSelect(self,absEdge,'M3N5')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pb" or self.element == "Bi" or self.element == "Th" or self.element == "Pa" or self.element == "Np":
                                self.M3O1 = Button(top,text='M3O1',command=lambda *args: spectraSelect(self,absEdge,'M3O1')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Ir" or self.element == "Tl" or self.element == "Pb" or self.element == "Bi" or self.element == "Th" or self.element == "Pa" or self.element == "Np":
                                self.M3O4 = Button(top,text='M3O4',command=lambda *args: spectraSelect(self,absEdge,'M3O4')).pack(side='left',  padx=10,  pady=10)
                                self.M3O5 = Button(top,text='M3O5',command=lambda *args: spectraSelect(self,absEdge,'M3O5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ta":
                            self.M3N3 = Button(top,text='M3N3',command=lambda *args: spectraSelect(self,absEdge,'M3N3')).pack(side='left',  padx=10,  pady=10)
                            self.M3N4 = Button(top,text='M3N4',command=lambda *args: spectraSelect(self,absEdge,'M3N4')).pack(side='left',  padx=10,  pady=10)
                            self.M3N5 = Button(top,text='M3N5',command=lambda *args: spectraSelect(self,absEdge,'M3N5')).pack(side='left',  padx=10,  pady=10)
                            self.M3O1 = Button(top,text='M3O1',command=lambda *args: spectraSelect(self,absEdge,'M3O1')).pack(side='left',  padx=10,  pady=10)
                            self.M3O4 = Button(top,text='M3O4',command=lambda *args: spectraSelect(self,absEdge,'M3O4')).pack(side='left',  padx=10,  pady=10)
                            self.M3O5 = Button(top,text='M3O5',command=lambda *args: spectraSelect(self,absEdge,'M3O5')).pack(side='left',  padx=10,  pady=10)
                            return
                        elif self.element == "W" or self.element == "Pt" or self.element == "Au":
                            self.M3N4 = Button(top,text='M3N4',command=lambda *args: spectraSelect(self,absEdge,'M3N4')).pack(side='left',  padx=10,  pady=10)
                            self.M3N5 = Button(top,text='M3N5',command=lambda *args: spectraSelect(self,absEdge,'M3N5')).pack(side='left',  padx=10,  pady=10)
                            self.M3O1 = Button(top,text='M3O1',command=lambda *args: spectraSelect(self,absEdge,'M3O1')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Pt" or self.element == "Au":
                                self.M3O4 = Button(top,text='M3O4',command=lambda *args: spectraSelect(self,absEdge,'M3O4')).pack(side='left',  padx=10,  pady=10)
                            self.M3O5 = Button(top,text='M3O5',command=lambda *args: spectraSelect(self,absEdge,'M3O5')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "U":
                            self.M3N4 = Button(top,text='M3N4',command=lambda *args: spectraSelect(self,absEdge,'M3N4')).pack(side='left',  padx=10,  pady=10)
                            self.M3N5 = Button(top,text='M3N5',command=lambda *args: spectraSelect(self,absEdge,'M3N5')).pack(side='left',  padx=10,  pady=10)
                            self.M3N7 = Button(top,text='M3N7',command=lambda *args: spectraSelect(self,absEdge,'M3N7')).pack(side='left',  padx=10,  pady=10)
                            self.M3O1 = Button(top,text='M3O1',command=lambda *args: spectraSelect(self,absEdge,'M3O1')).pack(side='left',  padx=10,  pady=10)
                            self.M3O4 = Button(top,text='M3O4',command=lambda *args: spectraSelect(self,absEdge,'M3O4')).pack(side='left',  padx=10,  pady=10)
                            return
                        elif self.element == "Np":
                            self.M3P1 = Button(top,text='M3P1',command=lambda *args: spectraSelect(self,absEdge,'M3P1')).pack(side='left',  padx=10,  pady=10)
                            self.M3Q1 = Button(top,text='M3Q1',command=lambda *args: spectraSelect(self,absEdge,'M3Q1')).pack(side='left',  padx=10,  pady=10)
                            
                    
                    elif absEdge == "M4":
                        if self.element == "Zr":
                            self.M4N2 = Button(top,text='M4N2',command=lambda *args: spectraSelect(self,absEdge,'M4N2')).pack(side='left',  padx=10,  pady=10)
                            self.M4O2 = Button(top,text='M4O2',command=lambda *args: spectraSelect(self,absEdge,'M4O2')).pack(side='left',  padx=10,  pady=10)
                            return
                        if self.element == "Ir":
                            self.M4N3 = Button(top,text='M4N3',command=lambda *args: spectraSelect(self,absEdge,'M4N3')).pack(side='left',  padx=10,  pady=10)
                            self.M4N6 = Button(top,text='M4N6',command=lambda *args: spectraSelect(self,absEdge,'M4N6')).pack(side='left',  padx=10,  pady=10)
                            self.M4O2 = Button(top,text='M4O2',command=lambda *args: spectraSelect(self,absEdge,'M4O2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Np":
                            self.M4N1 = Button(top,text='M4N1',command=lambda *args: spectraSelect(self,absEdge,'M4N1')).pack(side='left',  padx=10,  pady=10)
                        self.M4N2 = Button(top,text='M4N2',command=lambda *args: spectraSelect(self,absEdge,'M4N2')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "At":
                            self.M4N6 = Button(top,text='M4N6',command=lambda *args: spectraSelect(self,absEdge,'M4N6')).pack(side='left',  padx=10,  pady=10)
                        self.M4N3 = Button(top,text='M4N3',command=lambda *args: spectraSelect(self,absEdge,'M4N3')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Nb" or self.element == "Mo" or self.element == "Ru" or self.element == "Rh" or self.element == "Pd" or self.element == "Ag" or self.element == "Cd" or self.element == "In" or self.element == "Sn" or self.element == "Sb" or self.element == "I" or self.element == "Xe" or self.element == "Cs":
                            self.M4O2 = Button(top,text='M4O2',command=lambda *args: spectraSelect(self,absEdge,'M4O2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Te:":
                            self.M4O1 = Button(top,text='M4O1',command=lambda *args: spectraSelect(self,absEdge,'M4O1')).pack(side='left',  padx=10,  pady=10)
                            self.M4O2 = Button(top,text='M4O2',command=lambda *args: spectraSelect(self,absEdge,'M4O2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ba" or self.element == "Ta" or self.element == "W" or self.element == "Np":
                            self.M4N6 = Button(top,text='M4N6',command=lambda *args: spectraSelect(self,absEdge,'M4N6')).pack(side='left',  padx=10,  pady=10)
                            self.M4O2 = Button(top,text='M4O2',command=lambda *args: spectraSelect(self,absEdge,'M4O2')).pack(side='left',  padx=10,  pady=10)
                            self.M4O3 = Button(top,text='M4O3',command=lambda *args: spectraSelect(self,absEdge,'M4O3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "La" or self.element == "Ce" or self.element == "Pr" or self.element == "Nd" or self.element == "Pm" or self.element == "Sm" or self.element == "Eu" or self.element == "Gd" or self.element == "Tb" or self.element == "Dy" or self.element == "Ho" or self.element == "Er" or self.element == "Tm" or self.element == "Yb" or self.element == "Lu" or self.element == "Hf" or self.element == "Re" or self.element == "Os" or self.element == "Pt" or self.element == "Au" or self.element == "Hg" or self.element == "Tl" or self.element == "Pb" or self.element == "Bi" or self.element == "Po" or self.element == "Rn" or self.element == "Fr" or self.element == "Ra" or self.element == "Ac" or self.element == "Th" or self.element == "Pa" or self.element == "U" or self.element == "Pu" or self.element == "Am":
                            if self.element == "Os":
                                self.M4N4 = Button(top,text='M4N4',command=lambda *args: spectraSelect(self,absEdge,'M4N4')).pack(side='left',  padx=10,  pady=10)
                            self.M4N6 = Button(top,text='M4N6',command=lambda *args: spectraSelect(self,absEdge,'M4N6')).pack(side='left',  padx=10,  pady=10)
                            self.M4O2 = Button(top,text='M4O2',command=lambda *args: spectraSelect(self,absEdge,'M4O2')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Hg" or self.element == "U":
                                self.M4O3 = Button(top,text='M4O3',command=lambda *args: spectraSelect(self,absEdge,'M4O3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Bi" or self.element == "U":
                                self.M4P2 = Button(top,text='M4P2',command=lambda *args: spectraSelect(self,absEdge,'M4P2')).pack(side='left',  padx=10,  pady=10)
                                self.M4P3 = Button(top,text='M4P3',command=lambda *args: spectraSelect(self,absEdge,'M4P3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Np":
                            self.M4O6 = Button(top,text='M4O6',command=lambda *args: spectraSelect(self,absEdge,'M4O6')).pack(side='left',  padx=10,  pady=10)
                            self.M4P2 = Button(top,text='M4P2',command=lambda *args: spectraSelect(self,absEdge,'M4P2')).pack(side='left',  padx=10,  pady=10)
                            self.M4P3 = Button(top,text='M4P3',command=lambda *args: spectraSelect(self,absEdge,'M4P3')).pack(side='left',  padx=10,  pady=10)
                    
                    elif absEdge == "M5":
                        if self.element == "Ag":
                            self.M5N1 = Button(top,text='M5N1',command=lambda *args: spectraSelect(self,absEdge,'M5N1')).pack(side='left',  padx=10,  pady=10)
                            self.M5N2 = Button(top,text='M5N2',command=lambda *args: spectraSelect(self,absEdge,'M5N2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Rh" or self.element == "Pd" or self.element == "Ir" or self.element == "Th" or self.element == "Np":
                            self.M5N2 = Button(top,text='M5N2',command=lambda *args: spectraSelect(self,absEdge,'M5N2')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Dy":
                            self.M5N6 = Button(top,text='M5N6',command=lambda *args: spectraSelect(self,absEdge,'M5N6')).pack(side='left',  padx=10,  pady=10)
                            self.M5N7 = Button(top,text='M5N7',command=lambda *args: spectraSelect(self,absEdge,'M5N7')).pack(side='left',  padx=10,  pady=10)
                            self.M5O3 = Button(top,text='M5O3',command=lambda *args: spectraSelect(self,absEdge,'M5O3')).pack(side='left',  padx=10,  pady=10)
                            return
                        self.M5N3 = Button(top,text='M5N3',command=lambda *args: spectraSelect(self,absEdge,'M5N3')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Cd" or self.element == "Sn" or self.element == "Te:" or self.element == "Cs":
                            self.M5O3 = Button(top,text='M5O3',command=lambda *args: spectraSelect(self,absEdge,'M5O3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Pr" or self.element == "Nd" or self.element == "Pm" or self.element == "Sm" or self.element == "Tb" or self.element == "Tm" or self.element == "Yb" or self.element == "Lu" or self.element == "Hf" or self.element == "Os" or self.element == "Ir" or self.element == "Tl" or self.element == "Bi" or self.element == "Po" or self.element == "At" or self.element == "Rn" or self.element == "Fr" or self.element == "Ra" or self.element == "Ac" or self.element == "Th" or self.element == "Pa" or self.element == "U" or self.element == "Pu" or self.element == "Am":
                            self.M5N6 = Button(top,text='M5N6',command=lambda *args: spectraSelect(self,absEdge,'M5N6')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Th":
                                self.M5P3 = Button(top,text='M5P3',command=lambda *args: spectraSelect(self,absEdge,'M5P3')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Sm":
                                return
                            self.M5N7 = Button(top,text='M5N7',command=lambda *args: spectraSelect(self,absEdge,'M5N7')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ta":
                            self.M5N4 = Button(top,text='M5N4',command=lambda *args: spectraSelect(self,absEdge,'M5N4')).pack(side='left',  padx=10,  pady=10)
                            self.M5N5 = Button(top,text='M5N5',command=lambda *args: spectraSelect(self,absEdge,'M5N5')).pack(side='left',  padx=10,  pady=10)
                            self.M5N6 = Button(top,text='M5N6',command=lambda *args: spectraSelect(self,absEdge,'M5N6')).pack(side='left',  padx=10,  pady=10)
                            self.M5N7 = Button(top,text='M5N7',command=lambda *args: spectraSelect(self,absEdge,'M5N7')).pack(side='left',  padx=10,  pady=10)
                            self.M5O3 = Button(top,text='M5O3',command=lambda *args: spectraSelect(self,absEdge,'M5O3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ce":
                            self.M5N6 = Button(top,text='M5N6',command=lambda *args: spectraSelect(self,absEdge,'M5N6')).pack(side='left',  padx=10,  pady=10)
                            self.M5N7 = Button(top,text='M5N7',command=lambda *args: spectraSelect(self,absEdge,'M5N7')).pack(side='left',  padx=10,  pady=10)
                            self.M5O2 = Button(top,text='M5O2',command=lambda *args: spectraSelect(self,absEdge,'M5O2')).pack(side='left',  padx=10,  pady=10)
                            self.M5O3 = Button(top,text='M5O3',command=lambda *args: spectraSelect(self,absEdge,'M5O3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Eu" or self.element == "Gd" or self.element == "Ho" or self.element == "Er" or self.element == "W" or self.element == "Re" or self.element == "Pt" or self.element == "Au" or self.element == "Hg" or self.element == "Pb" or self.element == "Np": 
                            self.M5N6 = Button(top,text='M5N6',command=lambda *args: spectraSelect(self,absEdge,'M5N6')).pack(side='left',  padx=10,  pady=10)
                            self.M5N7 = Button(top,text='M5N7',command=lambda *args: spectraSelect(self,absEdge,'M5N7')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Ho":
                                return
                            self.M5O3 = Button(top,text='M5O3',command=lambda *args: spectraSelect(self,absEdge,'M5O3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Ba" or self.element == "La":
                            self.M5N7 = Button(top,text='M5N7',command=lambda *args: spectraSelect(self,absEdge,'M5N7')).pack(side='left',  padx=10,  pady=10)
                            self.M5O3 = Button(top,text='M5O3',command=lambda *args: spectraSelect(self,absEdge,'M5O3')).pack(side='left',  padx=10,  pady=10)
                        elif self.element == "Np":
                            self.M5O6 = Button(top,text='M5O6',command=lambda *args: spectraSelect(self,absEdge,'M5O6')).pack(side='left',  padx=10,  pady=10)
                            self.M5P3 = Button(top,text='M5P3',command=lambda *args: spectraSelect(self,absEdge,'M5P3')).pack(side='left',  padx=10,  pady=10)
                            self.M5Q7 = Button(top,text='M5Q7',command=lambda *args: spectraSelect(self,absEdge,'M5Q7')).pack(side='left',  padx=10,  pady=10)

                    elif absEdge == "N1":
                        if self.element == "U":
                            self.N1O3 = Button(top,text='N1O3',command=lambda *args: spectraSelect(self,absEdge,'N1O3')).pack(side='left',  padx=10,  pady=10)
                        self.N1P2 = Button(top,text='N1P2',command=lambda *args: spectraSelect(self,absEdge,'N1P2')).pack(side='left',  padx=10,  pady=10)
                        self.N1P3 = Button(top,text='N1P3',command=lambda *args: spectraSelect(self,absEdge,'N1P3')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "U":
                            self.N1P4 = Button(top,text='N1P4',command=lambda *args: spectraSelect(self,absEdge,'N1P4')).pack(side='left',  padx=10,  pady=10)


                    elif absEdge == "N2":
                        if self.element == "U":
                            self.N2P1 = Button(top,text='N2P1',command=lambda *args: spectraSelect(self,absEdge,'N2P1')).pack(side='left',  padx=10,  pady=10)
                        self.N2O4 = Button(top,text='N2O4',command=lambda *args: spectraSelect(self,absEdge,'N2O4')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Th":
                            self.N2P1 = Button(top,text='N2P1',command=lambda *args: spectraSelect(self,absEdge,'N2P1')).pack(side='left',  padx=10,  pady=10)
                    

                    elif absEdge == "N3":
                        self.N3O5 = Button(top,text='N3O5',command=lambda *args: spectraSelect(self,absEdge,'N3O5')).pack(side='left',  padx=10,  pady=10)


                    elif absEdge == "N4":
                        if self.element == "Pr" or self.element == "Nd" or self.element == "Sm" or self.element == "Tb" or self.element == "Dy" or self.element == "Er" or self.element == "Yb" or self.element == "Ta" or self.element == "W" or self.element == "Os" or self.element == "Ir" or self.element == "Pt" or self.element == "Au" or self.element == "Hg" or self.element == "Pb" or self.element == "Th":
                            self.N4N6 = Button(top,text='N4N6',command=lambda *args: spectraSelect(self,absEdge,'N4N6')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Er" or self.element == "Yb" or self.element == "W" or self.element == "Os" or self.element == "Ir" or self.element == "Pt" or self.element == "Au" or self.element == "Hg" or self.element == "Pb" or self.element == "Th":
                                return
                            self.N4O2 = Button(top,text='N4O2',command=lambda *args: spectraSelect(self,absEdge,'N4O2')).pack(side='left',  padx=10,  pady=10)
                            return
                        elif self.element == "U":
                            self.N4N6 = Button(top,text='N4N6',command=lambda *args: spectraSelect(self,absEdge,'N4N6')).pack(side='left',  padx=10,  pady=10)
                            self.N4O4 = Button(top,text='N4O4',command=lambda *args: spectraSelect(self,absEdge,'N4O4')).pack(side='left',  padx=10,  pady=10)
                            return
                        elif self.element == "La" or self.element == "Ce" or self.element == "Eu":
                            self.N4O2 = Button(top,text='N4O2',command=lambda *args: spectraSelect(self,absEdge,'N4O2')).pack(side='left',  padx=10,  pady=10)
                            return
                        self.N4O2 = Button(top,text='N4O2',command=lambda *args: spectraSelect(self,absEdge,'N4O2')).pack(side='left',  padx=10,  pady=10)
                        self.N4O3 = Button(top,text='N4O3',command=lambda *args: spectraSelect(self,absEdge,'N4O3')).pack(side='left',  padx=10,  pady=10)

                    elif absEdge == "N5":
                        if self.element == "Er" or self.element == "Yb" or self.element == "Ta" or self.element == "Ir" or self.element == "Au":
                            self.N5N6 = Button(top,text='N5N6',command=lambda *args: spectraSelect(self,absEdge,'N5N6')).pack(side='left',  padx=10,  pady=10)
                            if self.element == "Yb" or self.element == "Ta" or self.element == "Ir" or self.element == "Au":
                                return
                        if self.element == "W" or self.element == "Os" or self.element == "Pt" or self.element == "Hg" or self.element == "Tl" or self.element == "Pb" or self.element == "Th" or self.element == "U":
                            self.N5N6 = Button(top,text='N5N6',command=lambda *args: spectraSelect(self,absEdge,'N5N6')).pack(side='left',  padx=10,  pady=10)
                            self.N5N7 = Button(top,text='N5N7',command=lambda *args: spectraSelect(self,absEdge,'N5N7')).pack(side='left',  padx=10,  pady=10)
                            return
                        self.N5O3 = Button(top,text='N5O3',command=lambda *args: spectraSelect(self,absEdge,'N5O3')).pack(side='left',  padx=10,  pady=10)

                    elif absEdge == "N6":
                        if self.element == "U":
                            self.N6O5 = Button(top,text='N6O5',command=lambda *args: spectraSelect(self,absEdge,'N6O5')).pack(side='left',  padx=10,  pady=10)
                        self.N6O4 = Button(top,text='N6O4',command=lambda *args: spectraSelect(self,absEdge,'N6O4')).pack(side='left',  padx=10,  pady=10)
                        if self.element == "Bi":
                            return
                        self.N6O5 = Button(top,text='N6O5',command=lambda *args: spectraSelect(self,absEdge,'N6O5')).pack(side='left',  padx=10,  pady=10)

                    #Are there any N7 edges???
                    elif absEdge == "N7":
                        self.N7O5 = Button(top,text='N7O5',command=lambda *args: spectraSelect(self,absEdge,'N7O5')).pack(side='left',  padx=10,  pady=10)

                    elif absEdge == "O3":
                        self.O3P4 = Button(top,text='O3P4',command=lambda *args: spectraSelect(self,absEdge,'O3P4')).pack(side='left',  padx=10,  pady=10)

                    elif absEdge == "O4":
                        self.O4Q2 = Button(top,text='O4Q2',command=lambda *args: spectraSelect(self,absEdge,'O4Q2')).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Bk" or self.element == "Cf" or self.element == "Es" or self.element == "Fm":
                    if absEdge == "K":
                        self.KL1 = Button(top,text='KL1',command=lambda *args: spectraSelect(self,absEdge,'KL1')).pack(side='left',  padx=10,  pady=10)
                        self.KL2 = Button(top,text='KL2',command=lambda *args: spectraSelect(self,absEdge,'KL2')).pack(side='left',  padx=10,  pady=10)
                        self.KL3 = Button(top,text='KL3',command=lambda *args: spectraSelect(self,absEdge,'KL3')).pack(side='left',  padx=10,  pady=10)
                        self.KM1 = Button(top,text='KM1',command=lambda *args: spectraSelect(self,absEdge,'KM1')).pack(side='left',  padx=10,  pady=10)
                        self.KM2 = Button(top,text='KM2',command=lambda *args: spectraSelect(self,absEdge,'KM2')).pack(side='left',  padx=10,  pady=10)
                        self.KM3 = Button(top,text='KM3',command=lambda *args: spectraSelect(self,absEdge,'KM3')).pack(side='left',  padx=10,  pady=10)
                        self.KM4 = Button(top,text='KM4',command=lambda *args: spectraSelect(self,absEdge,'KM4')).pack(side='left',  padx=10,  pady=10)
                        self.KM5 = Button(top,text='KM5',command=lambda *args: spectraSelect(self,absEdge,'KM5')).pack(side='left',  padx=10,  pady=10)
                        self.KN1 = Button(top,text='KN1',command=lambda *args: spectraSelect(self,absEdge,'KN1')).pack(side='left',  padx=10,  pady=10)
                        self.KN2 = Button(top,text='KN2',command=lambda *args: spectraSelect(self,absEdge,'KN2')).pack(side='left',  padx=10,  pady=10)
                        self.KN3 = Button(top,text='KN3',command=lambda *args: spectraSelect(self,absEdge,'KN3')).pack(side='left',  padx=10,  pady=10)
                        self.KN4 = Button(top,text='KN4',command=lambda *args: spectraSelect(self,absEdge,'KN4')).pack(side='left',  padx=10,  pady=10)
                        self.KN5 = Button(top,text='KN5',command=lambda *args: spectraSelect(self,absEdge,'KN5')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L1":
                        self.L1M1 = Button(top,text='L1M1',command=lambda *args: spectraSelect(self,absEdge,'L1M1')).pack(side='left',  padx=10,  pady=10)
                        self.L1M2 = Button(top,text='L1M2',command=lambda *args: spectraSelect(self,absEdge,'L1M2')).pack(side='left',  padx=10,  pady=10)
                        self.L1M3 = Button(top,text='L1M3',command=lambda *args: spectraSelect(self,absEdge,'L1M3')).pack(side='left',  padx=10,  pady=10)
                        self.L1M4 = Button(top,text='L1M4',command=lambda *args: spectraSelect(self,absEdge,'L1M4')).pack(side='left',  padx=10,  pady=10)
                        self.L1M5 = Button(top,text='L1M5',command=lambda *args: spectraSelect(self,absEdge,'L1M5')).pack(side='left',  padx=10,  pady=10)
                        self.L1N1 = Button(top,text='L1N1',command=lambda *args: spectraSelect(self,absEdge,'L1N1')).pack(side='left',  padx=10,  pady=10)
                        self.L1N2 = Button(top,text='L1N2',command=lambda *args: spectraSelect(self,absEdge,'L1N2')).pack(side='left',  padx=10,  pady=10)
                        self.L1N3 = Button(top,text='L1N3',command=lambda *args: spectraSelect(self,absEdge,'L1N3')).pack(side='left',  padx=10,  pady=10)
                        self.L1N4 = Button(top,text='L1N4',command=lambda *args: spectraSelect(self,absEdge,'L1N4')).pack(side='left',  padx=10,  pady=10)
                        self.L1N5 = Button(top,text='L1N5',command=lambda *args: spectraSelect(self,absEdge,'L1N5')).pack(side='left',  padx=10,  pady=10)
                        self.L1N6 = Button(top,text='L1N6',command=lambda *args: spectraSelect(self,absEdge,'L1N6')).pack(side='left',  padx=10,  pady=10)
                        self.L1N7 = Button(top,text='L1N7',command=lambda *args: spectraSelect(self,absEdge,'L1N7')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L2":
                        self.L2M1 = Button(top,text='L2M1',command=lambda *args: spectraSelect(self,absEdge,'L2M1')).pack(side='left',  padx=10,  pady=10)
                        self.L2M2 = Button(top,text='L2M2',command=lambda *args: spectraSelect(self,absEdge,'L2M2')).pack(side='left',  padx=10,  pady=10)
                        self.L2M3 = Button(top,text='L2M3',command=lambda *args: spectraSelect(self,absEdge,'L2M3')).pack(side='left',  padx=10,  pady=10)
                        self.L2M4 = Button(top,text='L2M4',command=lambda *args: spectraSelect(self,absEdge,'L2M4')).pack(side='left',  padx=10,  pady=10)
                        self.L2M5 = Button(top,text='L2M5',command=lambda *args: spectraSelect(self,absEdge,'L2M5')).pack(side='left',  padx=10,  pady=10)
                        self.L2N1 = Button(top,text='L2N1',command=lambda *args: spectraSelect(self,absEdge,'L2N1')).pack(side='left',  padx=10,  pady=10)
                        self.L2N2 = Button(top,text='L2N2',command=lambda *args: spectraSelect(self,absEdge,'L2N2')).pack(side='left',  padx=10,  pady=10)
                        self.L2N3 = Button(top,text='L2N3',command=lambda *args: spectraSelect(self,absEdge,'L2N3')).pack(side='left',  padx=10,  pady=10)
                        self.L2N4 = Button(top,text='L2N4',command=lambda *args: spectraSelect(self,absEdge,'L2N4')).pack(side='left',  padx=10,  pady=10)
                        self.L2N5 = Button(top,text='L2N5',command=lambda *args: spectraSelect(self,absEdge,'L2N5')).pack(side='left',  padx=10,  pady=10)
                        self.L2N6 = Button(top,text='L2N6',command=lambda *args: spectraSelect(self,absEdge,'L2N6')).pack(side='left',  padx=10,  pady=10)
                        self.L2N7 = Button(top,text='L2N7',command=lambda *args: spectraSelect(self,absEdge,'L2N7')).pack(side='left',  padx=10,  pady=10)
                    elif absEdge == "L3":
                        self.L3M1 = Button(top,text='L3M1',command=lambda *args: spectraSelect(self,absEdge,'L3M1')).pack(side='left',  padx=10,  pady=10)
                        self.L3M2 = Button(top,text='L3M2',command=lambda *args: spectraSelect(self,absEdge,'L3M2')).pack(side='left',  padx=10,  pady=10)
                        self.L3M3 = Button(top,text='L3M3',command=lambda *args: spectraSelect(self,absEdge,'L3M3')).pack(side='left',  padx=10,  pady=10)
                        self.L3M4 = Button(top,text='L3M4',command=lambda *args: spectraSelect(self,absEdge,'L3M4')).pack(side='left',  padx=10,  pady=10)
                        self.L3M5 = Button(top,text='L3M5',command=lambda *args: spectraSelect(self,absEdge,'L3M5')).pack(side='left',  padx=10,  pady=10)
                        self.L3N1 = Button(top,text='L3N1',command=lambda *args: spectraSelect(self,absEdge,'L3N1')).pack(side='left',  padx=10,  pady=10)
                        self.L3N2 = Button(top,text='L3N2',command=lambda *args: spectraSelect(self,absEdge,'L3N2')).pack(side='left',  padx=10,  pady=10)
                        self.L3N3 = Button(top,text='L3N3',command=lambda *args: spectraSelect(self,absEdge,'L3N3')).pack(side='left',  padx=10,  pady=10)
                        self.L3N4 = Button(top,text='L3N4',command=lambda *args: spectraSelect(self,absEdge,'L3N4')).pack(side='left',  padx=10,  pady=10)
                        self.L3N5 = Button(top,text='L3N5',command=lambda *args: spectraSelect(self,absEdge,'L3N5')).pack(side='left',  padx=10,  pady=10)
                        self.L3N6 = Button(top,text='L3N6',command=lambda *args: spectraSelect(self,absEdge,'L3N6')).pack(side='left',  padx=10,  pady=10)
                        self.L3N7 = Button(top,text='L3N7',command=lambda *args: spectraSelect(self,absEdge,'L3N7')).pack(side='left',  padx=10,  pady=10)
                   



            def spectraSelect(self,selection,transition):
                global photoelectronLine
                global element
                global transitionLine
                element = self.element
                n_elements = int(num_peaks.get())

                try:
                    outer_self.elementArr[outer_self.count_table] = element
                    outer_self.photoelectronLineArr[outer_self.count_table] = selection
                    outer_self.transitionLineArr[outer_self.count_table] = transition 
                    print("Peak", outer_self.count_table+1, "assigned:", outer_self.elementArr[outer_self.count_table], outer_self.transitionLineArr[outer_self.count_table])
                except:
                    print("Peak maximum reached. Use CLEAR button to reset peak assignment")
                    return
                
                photoelectronLine = selection
                transitionLine = transition

                self.element_select = self.element
                self.photoLine_select = selection
                self.transitionLine_select = transition

                update_element_selection_values(self)

                
                '''
                print("Element:", self.element[outer_self.count_table], " Edge:", photoelectronLine[outer_self.count_table], " Line:", transitionLine[outer_self.count_table], "selected")
                if self.element == "H":
                    print("Hydrogen is not detectable using XES please select a new element")
                if self.element == "He":
                    print("Helium is not detectable in most XES systems. Make sure you have made the correct selection.")
                '''
                update_peaks_table(0)

                


            def elementSpectra(self,table):
                #Elemental X-ray Lines taken from X-Ray Data Booklet. Center for X-Ray Optics and Advanced Light Source. Oct. 2009. url: https://xdb.lbl.gov
                top=self.top=Toplevel(table)
                self.element = symb.cget("text")

                #Want to switch this over to be peak dependent. Need to turn element, transitionLine, and photoelectronLine into arrays
                #transitionLine = 'N/A'
                #photoelectronLine = '1s'
                


                selectLine = ttk.Label(top, text='Select Absorption Edge:', font='TkTextFont').pack(side='top',  padx=10,  pady=10)

                if self.element == "H" or self.element == "He" or self.element == "Li" or self.element == "Be" or self.element == "B":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "C" or self.element == "N" or self.element == "O" or self.element == "F":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: spectraSelect(self,'L1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                elif self.element == "Ne":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: spectraSelect(self,'L1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: spectraSelect(self,'L2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: spectraSelect(self,'L3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                elif self.element == "Na" or self.element == "Mg":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Al" or self.element == "Si":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "P" or self.element == "S" or self.element == "Cl" or self.element == "Ar":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: spectraSelect(self,'M3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                
                elif self.element == "K" or self.element == "Ca" or self.element == "V" or self.element == "Cr" or self.element == "Mn" or self.element == "Fe" or self.element == "Co" or self.element == "Ni" or self.element == "Cu":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: spectraSelect(self,'M3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Sc" or self.element == "Ti":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: spectraSelect(self,'M3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Zn":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: spectraSelect(self,'M3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: spectraSelect(self,'M4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: spectraSelect(self,'M5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Ga" or self.element == "Ge" or self.element == "As":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: spectraSelect(self,'M3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: spectraSelect(self,'M4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: spectraSelect(self,'M5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                
                elif self.element == "Se":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: spectraSelect(self,'M3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: spectraSelect(self,'M4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                
                elif self.element == "Br":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                
                elif self.element == "Kr":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: spectraSelect(self,'M4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: spectraSelect(self,'M5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                
                elif self.element == "Rb" or self.element == "Nb" or self.element == "Mo" or self.element == "Pd" or self.element == "Ag":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                
                elif self.element == "Sr" or self.element == "Y" or self.element == "Zr" or self.element == "Ru" or self.element == "Rh":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Tc":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Cd":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "In" or self.element == "I":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Sn" or self.element == "Sb" or self.element == "Te":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)


                elif self.element == "Xe":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Cs" or self.element == "Ba":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "La" or self.element == "Ce":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
               
                elif self.element == "Pr" or self.element == "Nd" or self.element == "Sm" or self.element == "Eu" or self.element == "Tb" or self.element == "Dy":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Pm":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    #self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    #self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Gd":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    #self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Ho" or self.element == "Lu" or self.element == "Hf":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Er":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    #self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Tm":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    #self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Yb":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Ta" or self.element == "Os" or self.element == "Ir" or self.element == "Pt" or self.element == "Au":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    
                elif self.element == "W":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: transitionSelect(self,self.element,'N2')).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Re":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                
                elif self.element == "Hg":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                   
                elif self.element == "Tl" or self.element == "Pb":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: transitionSelect(self,self.element,'N6')).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Bi":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: transitionSelect(self,self.element,'N1')).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: transitionSelect(self,self.element,'N6')).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Po" or self.element == "At" or self.element == "Ac":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Pa":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Rn":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixS = Button(top,text='P1',command=lambda *args: spectraSelect(self,'P1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Fr" or self.element == "Ra":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixS = Button(top,text='P1',command=lambda *args: spectraSelect(self,'P1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP1_2 = Button(top,text='P2',command=lambda *args: spectraSelect(self,'P2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP3_2 = Button(top,text='P3',command=lambda *args: spectraSelect(self,'P3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Th":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: transitionSelect(self,self.element,'N1')).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: transitionSelect(self,self.element,'N2')).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: transitionSelect(self,self.element,'N3')).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: transitionSelect(self,self.element,'N6')).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: transitionSelect(self,self.element,'O3')).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: transitionSelect(self,self.element,'O4')).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixS = Button(top,text='P1',command=lambda *args: spectraSelect(self,'P1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP1_2 = Button(top,text='P2',command=lambda *args: spectraSelect(self,'P2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP3_2 = Button(top,text='P3',command=lambda *args: spectraSelect(self,'P3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "U":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: transitionSelect(self,self.element,'N1')).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: transitionSelect(self,self.element,'N2')).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: transitionSelect(self,self.element,'N3')).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: transitionSelect(self,self.element,'N4')).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: transitionSelect(self,self.element,'N5')).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: transitionSelect(self,self.element,'N6')).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixS = Button(top,text='P1',command=lambda *args: spectraSelect(self,'P1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP1_2 = Button(top,text='P2',command=lambda *args: spectraSelect(self,'P2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP3_2 = Button(top,text='P3',command=lambda *args: spectraSelect(self,'P3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Np":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: transitionSelect(self,self.element,'M1')).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixS = Button(top,text='P1',command=lambda *args: spectraSelect(self,'P1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP1_2 = Button(top,text='P2',command=lambda *args: spectraSelect(self,'P2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP3_2 = Button(top,text='P3',command=lambda *args: spectraSelect(self,'P3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)

                elif self.element == "Pu" or self.element  == "Am":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: transitionSelect(self,self.element,'M2')).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: transitionSelect(self,self.element,'M3')).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: transitionSelect(self,self.element,'M4')).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: transitionSelect(self,self.element,'M5')).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixS = Button(top,text='P1',command=lambda *args: spectraSelect(self,'P1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP1_2 = Button(top,text='P2',command=lambda *args: spectraSelect(self,'P2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP3_2 = Button(top,text='P3',command=lambda *args: spectraSelect(self,'P3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                   

                elif self.element == "Cm" or self.element == "Bk" or self.element == "Cf" or self.element == "Es" or self.element == "Fm":
                    self.oneS = Button(top,text='K',command=lambda *args: transitionSelect(self,self.element,'K')).pack(side='left',  padx=10,  pady=10)
                    self.twoS = Button(top,text='L1',command=lambda *args: transitionSelect(self,self.element,'L1')).pack(side='left',  padx=10,  pady=10)
                    self.twoP1_2 = Button(top,text='L2',command=lambda *args: transitionSelect(self,self.element,'L2')).pack(side='left',  padx=10,  pady=10)
                    self.twoP3_2 = Button(top,text='L3',command=lambda *args: transitionSelect(self,self.element,'L3')).pack(side='left',  padx=10,  pady=10)
                    self.threeS = Button(top,text='M1',command=lambda *args: spectraSelect(self,'M1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP1_2 = Button(top,text='M2',command=lambda *args: spectraSelect(self,'M2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeP3_2 = Button(top,text='M3',command=lambda *args: spectraSelect(self,'M3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD3_2 = Button(top,text='M4',command=lambda *args: spectraSelect(self,'M4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.threeD5_2 = Button(top,text='M5',command=lambda *args: spectraSelect(self,'M5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourS = Button(top,text='N1',command=lambda *args: spectraSelect(self,'N1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP1_2 = Button(top,text='N2',command=lambda *args: spectraSelect(self,'N2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourP3_2 = Button(top,text='N3',command=lambda *args: spectraSelect(self,'N3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD3_2 = Button(top,text='N4',command=lambda *args: spectraSelect(self,'N4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourD5_2 = Button(top,text='N5',command=lambda *args: spectraSelect(self,'N5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fourF5_2 = Button(top,text='N6',command=lambda *args: spectraSelect(self,'N6',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveS = Button(top,text='O1',command=lambda *args: spectraSelect(self,'O1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP1_2 = Button(top,text='O2',command=lambda *args: spectraSelect(self,'O2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveP3_2 = Button(top,text='O3',command=lambda *args: spectraSelect(self,'O3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD3_2 = Button(top,text='O4',command=lambda *args: spectraSelect(self,'O4',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.fiveD5_2 = Button(top,text='O5',command=lambda *args: spectraSelect(self,'O5',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixS = Button(top,text='P1',command=lambda *args: spectraSelect(self,'P1',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP1_2 = Button(top,text='P2',command=lambda *args: spectraSelect(self,'P2',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.sixP3_2 = Button(top,text='P3',command=lambda *args: spectraSelect(self,'P3',transitionLine)).pack(side='left',  padx=10,  pady=10)
                    self.no_edge = Button(top,text='N/A',command=lambda *args: spectraSelect(self,'N/A',transitionLine)).pack(side='left',  padx=10,  pady=10)
                else: #elements Z > 100
                    selectNA = ttk.Label(top, text='No information currently exists in our database for this element:', font='TkTextFont').pack(side='top',  padx=10,  pady=10)

                
                #self.button=Button(top,text='Ok',command=self.cleanup)
                #self.button.pack()

            def execute(self):

                #print(symb.cget("text")) #This is the variable we want to pull --> Now we want each each with their respective spectral lines

                elementSpectra(self,table)
                #self.b["state"] = "disabled"
                #self.master.wait_window(self.w.top)
                #self.b["state"] = "normal"


                table.configure(relief='raised')


            table.bind('<Enter>', in_active)
            table.bind('<Leave>', in_active)
            table.bind('<ButtonPress-1>', indicate) #Pressing button

            table.bind('<ButtonRelease-1>', execute) #Releasing button
            #print("HELLO")
            [child.bind('<ButtonPress-1>', indicate) for child in table.winfo_children()]
            [child.bind('<ButtonRelease-1>', execute) for child in table.winfo_children()]




        def test():
            print('testing..')


        top_text = ttk.Label(self.periodicTable_tab, text="Click on table to assign to peaks:", font=self.labelFont)
        top_text.grid_configure(column=0, row=0, columnspan=6, sticky=W, padx=self.padx, pady=self.pady)

        for idx,symbol in enumerate(symbols):
            kwargs = {}
            for k,v in zip(keywords,values[idx]):
                kwargs.update({k:v})

            make_periodicTable(self,symbol,command=test,**kwargs)
       
        
        arr_xes_peaks = ["Peak #"]
       
        self.num = int(self.number_of_peaks.get())
        new_num = DoubleVar(self.root, 1)
        element_sel = str(self.element_select[self.num-1].get())

      
        self.description_tabs(arr_xes_peaks, self.periodicTable_tab, row=[30])
        num_peaks_selected = [1,2,3,4,5,6,7,8,9,10]
        arr_xes_table = ["Element", "Assign."]
        self.description_tabs_column(arr_xes_table, self.periodicTable_tab, column=[0, 1], row=31)
     
        def clear_array():
                #Resetting all selections
                global element
                global photoelectronLine
                global transitionLine
                print("Data Cleared")
                outer_self.photoelectronLineArr = [' ']* 10
                outer_self.elementArr = [' ']* 10
                outer_self.transitionLineArr = [' ']* 10
                element = outer_self.elementArr 
                photoelectronLine = outer_self.photoelectronLineArr 
                transitionLine = outer_self.transitionLineArr 
                
                update_peaks_table(0)

                self.periodicTable = ElementData(element,photoelectronLine, transitionLine)
                PE_lit, is_singlet, so_split, Br, PE_alt, alt_width, width_range, width, rec_width, default, peakTypes, ck = self.periodicTable.getParams(element,photoelectronLine, transitionLine)

                PE_PT = [0.0]* 10
                width_PT = [0.0]* 10
                width_min = [0.0]* 10
                width_max = [0.0]* 10
                for i in range(10):
                
                    if int(round(PE_alt[i])) == 0: 
                        PE_PT[i] = PE_lit[i]
                    else:
                        PE_PT[i] = PE_alt[i]

                    #Default to alt_width, then rec_width, then width
                    if alt_width[i] == 0:
                        width_PT[i] = rec_width[i]
                        if rec_width[i] == 0:
                            width_PT[i] = width[i]
                    else:
                        width_PT[i] = alt_width[i]

                    width_min[i] = -width_range[i]
                    width_max[i] = width_range[i]
                
                outer_self.background_types = [] #Think it is appending one too many baselines when element is selected. Redefine here to empty list 
                
                for i in range(10):
                    PE_guesses[i] = DoubleVar(temp_root, PE_PT[i]) 
                    gamma_guesses[i] = DoubleVar(temp_root, width_PT[i]) 
                    gamma_up_lim[i] = DoubleVar(temp_root, width_max[i])
                    gamma_low_lim[i] = DoubleVar(temp_root, width_min[i])
                    #br_guesses[i] = DoubleVar(temp_root, br_temp[i])
                    #sos_guesses[i] = DoubleVar(temp_root, sos_temp[i])
                    singlet[i] = BooleanVar(temp_root, is_singlet[i])
                    peakType[i] = StringVar(temp_root, peakTypes[i])
                    is_coster_kronig[i] = BooleanVar(temp_root, ck[i]) 
         
             
                outer_self.build_fitting_param_tab()
                outer_self.build_param_range_tab()
               

                outer_self.count_table = 0
               
        def update_peaks_table(args):
            
           
            global element
            global photoelectronLine
            global transitionLine
            

            self.num = int(new_num.get())
            
            element_sel = str(self.element_select[self.num-1].get())
           

            self.element_entry = ttk.Label(self.periodicTable_tab, text=element[self.num-1], font=self.entryFont)
            self.element_entry.grid(column=0, row=32, sticky=(W, E))
    
            self.trans_entry = ttk.Label(self.periodicTable_tab, text=transitionLine[self.num-1], font=self.entryFont)
            self.trans_entry.grid(column=1, row=32, sticky=(W, E))

        clear_button = ttk.Button(self.periodicTable_tab, text="CLEAR", command=clear_array,style='my.TButton')
        clear_button.grid(column=2, row=30, sticky=W)
        number_of_peaks_entry_table = ttk.Combobox(self.periodicTable_tab, textvariable=new_num, font=self.entryFont,values= num_peaks_selected, width = 1)
        number_of_peaks_entry_table.grid(column=1, row=30, sticky=(W, E)) #on same row as background checkbox
        number_of_peaks_entry_table.bind('<<ComboboxSelected>>', update_peaks_table)
        
        






    def build_fitting_param_tab(self):
        """
        Build fitting parameters tab
        """
       
        arr_xes_peaks = ["No. of Peaks"]
        self.description_tabs(arr_xes_peaks, self.fitting_param_tab, row=[2]) #tabs start at row=1. Row=2 is for background and number_of_peaks


        #Row 3 is for the singlet/doublet checkbuttons

        #Doublet Selected: #Should make this peak dependent in the future

        self.peak_state = 'normal' #initial state for so_split and path_branching



        '''
        checkbutton_doublet = ttk.Checkbutton(self.fitting_param_tab, text="Doublet", command=doublet_selected)
        checkbutton_doublet.grid(column=0, row=3, sticky=W)
        checkbutton_doublet.state(['!alternate']) #initial state of checkbutton is alternate --> need to set it to off otherwise checkbutton is filled with black square
        '''

        #Peak type picker:
        self.peak_types = ['Voigt', 'Gaussian', 'Lorentzian','Double Lorentzian', 'Doniach-Sunjic'] #leave it like this so it can be accessed elsewhere -evan
        path_peakType = ttk.Label(self.fitting_param_tab, text="Fit Type", font=self.labelFont)
        path_peakType.grid_configure(column=2, row=5, sticky=W, padx=self.padx, pady=self.pady)

        PE = ttk.Label(self.fitting_param_tab,text = "Energy",font = self.labelFont)
        PE.grid(column = 3,row = 5,sticky = W, padx= self.padx,pady= self.pady)

        sig = ttk.Label(self.fitting_param_tab,text = "Sigma",font = self.labelFont)
        sig.grid(column = 4,row = 5,sticky = W, padx= self.padx,pady= self.pady)

        gam = ttk.Label(self.fitting_param_tab,text = "Gamma",font = self.labelFont)
        gam.grid(column = 5,row = 5,sticky = W, padx= self.padx,pady= self.pady)

        A = ttk.Label(self.fitting_param_tab,text = "Amplitude",font = self.labelFont)
        A.grid(column = 6,row = 5,sticky = W, padx= self.padx,pady= self.pady)


        branching_ratio_button = ttk.Label(self.fitting_param_tab,text = "Branching Ratio",font = self.labelFont)
        branching_ratio_button.grid(column = 8,row = 5,sticky = W, padx= self.padx,pady= self.pady)

        so_split_button = ttk.Label(self.fitting_param_tab,text = "Spin-Orbit Splitting",font = self.labelFont)
        so_split_button.grid(column = 9,row = 5,sticky = W, padx= self.padx,pady= self.pady)

        self.PE_entries = [0] *10
        self.sigma_range_entries = [0] *10
        self.gamma_range_entries = [0] *10
        self.amp_range_entries = [0] *10
        self.checkbutton_doublets = [0] *10
        self.checkbutton_coster_kronig = [0] *10
        self.peakTypes_entries = [0] *10
        self.branching_entries = [0] *10
        self.so_split_entries = [0] *10 #changed
        self.separators = [0]*10
        self.peak_labels = []
        self.oldNum = 1
        
        #Creates a row for each peak
      
        def updatePeakSelectionRows(args):
            
            self.num = int(self.number_of_peaks.get())
            peak_labels = []
            rows = []
            i=0

            for row in range(6,6+(2*self.num),2):


                peak_labels.append("Peak " + str(i+1))

                rows.append(row)
                self.val = 1


                self.peakTypes_entries[i] = ttk.Combobox(self.fitting_param_tab, textvariable=self.peaks[i], font=self.entryFont,
                                            values= self.peak_types, width=17)
                self.peakTypes_entries[i].grid(column=2, row=row, sticky=W)

                #Photon Energy:
                self.PE_entries[i] = ttk.Entry(self.fitting_param_tab, textvariable=self.PE_guesses[i], font=self.entryFont, width=12)
                self.PE_entries[i].grid(column=3, row=row, sticky=(W, E))

                self.sigma_range_entries[i] = ttk.Entry(self.fitting_param_tab, textvariable=self.sigma_guesses[i], font=self.entryFont, width=8)
                self.sigma_range_entries[i].grid(column=4, row=row, sticky=(W, E))

                self.gamma_range_entries[i] = ttk.Entry(self.fitting_param_tab, textvariable=self.gamma_guesses[i], font=self.entryFont, width=8)
                self.gamma_range_entries[i].grid(column=5, row=row, sticky=(W, E))

                self.amp_range_entries[i] = ttk.Entry(self.fitting_param_tab, textvariable=self.amp_guesses[i], font=self.entryFont, width=8)
                self.amp_range_entries[i].grid(column=6, row=row, sticky=(W, E))



                self.checkbutton_doublets[i] = ttk.Checkbutton(self.fitting_param_tab, text="Doublet", variable = self.peak_singlet[i],onvalue= False,offvalue=True)
                #self.checkbutton_doublets[i] = ttk.Checkbutton(self.fitting_param_tab, text="Doublet", command=doublet_selected)
                self.checkbutton_doublets[i].grid(column=7, row=row, sticky=W)
                self.checkbutton_doublets[i].state(['!alternate']) #initial state of checkbutton is alternate --> need to set it to off otherwise checkbutton is filled with black square

                #self.checkbutton_coster_kronig[i] = ttk.Checkbutton(self.fitting_param_tab, text="Coster-Kronig", variable = self.peak_coster_kronig[i],onvalue= True,offvalue=False)
                #self.checkbutton_coster_kronig[i].grid(column=11, row=row, sticky=W)
                #self.checkbutton_coster_kronig[i].state(['!alternate'])

                self.branching_entries[i] = ttk.Combobox(self.fitting_param_tab, textvariable=self.path_branching[i], font=self.entryFont,
                            values=['0.5', '0.666', '0.75'], width=12, state=self.peak_state)
                self.so_split_entries[i] = ttk.Entry(self.fitting_param_tab, textvariable=self.so_split[i], font=self.entryFont, width=8) #added so_split stuff
                self.so_split_entries[i].config(state=self.peak_state)

                #path_branching.config(state='disabled')
                self.branching_entries[i].grid(column=8, row=row, sticky=W)
                self.so_split_entries[i].grid(column=9, row=row, sticky=(W, E))
                self.separators[i] = ttk.Separator(self.fitting_param_tab,orient = 'horizontal')
                self.separators[i].grid(column= 0,row = row+1,columnspan=10,sticky=W+E,padx=self.padx)





               
                i+=1
            #destroy any that were leftover

            for k in np.arange(self.num,self.oldNum):

                #Still having some issues with entry box destruction --> May have something to do with var type of self.num or k range
                # AttributeError: 'int' object has no attribute 'destroy'
                self.peakTypes_entries[k].destroy()
                self.PE_entries[k].destroy()
                self.sigma_range_entries[k].destroy()
                self.gamma_range_entries[k].destroy()
                self.amp_range_entries[k].destroy()
                self.checkbutton_doublets[k].destroy()
                self.so_split_entries[k].destroy()
                self.branching_entries[k].destroy()
                self.separators[k].destroy()
                num_diff = self.oldNum - self.num

            self.oldNum = self.num

            for label in self.peak_labels:

                label.destroy()
            #print(peak_labels)

            self.peak_labels = self.description_tabs(peak_labels,self.fitting_param_tab,row = rows)

        #Nunber of Peaks:
        number_of_peaks_options = [1,2,3,4,5,6,7,8,9,10]
        number_of_peaks_entry = ttk.Combobox(self.fitting_param_tab, textvariable=self.number_of_peaks, font=self.entryFont,values= number_of_peaks_options, width = 5)
        number_of_peaks_entry.grid(column=2, row=2, sticky=(W, E)) #on same row as background checkbox
        number_of_peaks_entry.bind('<<ComboboxSelected>>', updatePeakSelectionRows)


        #-------------------------------------Backgrounds-----------------------------------------------------

        #Backgrounds Checkboxes:
        path_bkgn = ttk.Label(self.fitting_param_tab, text="Background Type:", font=self.labelFont)
        path_bkgn.grid_configure(column=3, row=2, sticky=W, padx=self.padx, pady=self.pady)

        global background_types
        #self.background_types = [] #make an array of the background types selected

        #-----Baseline Background------

        self.baseline_selected = 1
        def baseline_bkgn():
            global background_types
            global baseline_selected
            if (self.baseline_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('Baseline')
                self.baseline_selected = 1
            else: #state of button is on
                self.background_types.append('Baseline')
                self.baseline_selected = 2


        defaultOn = IntVar(value=1)
        checkbutton_baseline = ttk.Checkbutton(self.fitting_param_tab,variable = defaultOn, text="Baseline", command=baseline_bkgn)
        checkbutton_baseline.grid(column=4, row=2, sticky=W)
        checkbutton_baseline.state(['!alternate']) #Default is that baseline is always selected

        if self.fit_file_selected == False:  
            baseline_bkgn() #Automatically selecting baseline 
        else:
            for i in self.background_types:
                if i == 'Baseline':
                    self.baseline_selected = 2




    

     #-----1st Order Polynomial Background------
        '''

        self.polynomial1_selected = 1
        def polynomial1_bkgn():
            global background_types
            global polynomial1_selected
            if (self.polynomial1_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('Polynomial 1')
                self.polynomial1_selected = 1
            else: #state of button is on
                self.background_types.append('Polynomial 1')
                self.polynomial1_selected = 2
            
        if self.fit_file_selected == True:  
            for i in self.background_types:
                if i == 'Polynomial 1':
                    self.polynomial1_selected = 2



        checkbutton_poly1 = ttk.Checkbutton(self.fitting_param_tab,variable = self.poly1_value, text="Polynomial 1", command=polynomial1_bkgn)
        checkbutton_poly1.grid(column=4, row=4, sticky=W)
        checkbutton_poly1.state(['!alternate']) #Default is that baseline is always selected



         #-----2nd Order Polynomial Background------

        self.polynomial2_selected = 1
        def polynomial2_bkgn():
            global background_types
            global polynomial2_selected
            if (self.polynomial2_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('Polynomial 2')
                self.polynomial2_selected = 1
            else: #state of button is on
                self.background_types.append('Polynomial 2')
                self.polynomial2_selected = 2

        if self.fit_file_selected == True:  
            for i in self.background_types:
                if i == 'Polynomial 2':
                    self.polynomial2_selected = 2



        checkbutton_poly2 = ttk.Checkbutton(self.fitting_param_tab,variable = self.poly2_value, text="Polynomial 2", command=polynomial2_bkgn)
        checkbutton_poly2.grid(column=5, row=4, sticky=W)
        checkbutton_poly2.state(['!alternate']) #Default is that baseline is always selected




         #-----3nd Order Polynomial Background------

        self.polynomial3_selected = 1
        def polynomial3_bkgn():
            global background_types
            global polynomial3_selected
            if (self.polynomial3_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('Polynomial 3')
                self.polynomial3_selected = 1
            else: #state of button is on
                self.background_types.append('Polynomial 3')
                self.polynomial3_selected = 2

        if self.fit_file_selected == True:  
            for i in self.background_types:
                if i == 'Polynomial 3':
                    self.polynomial3_selected = 2



        checkbutton_poly3 = ttk.Checkbutton(self.fitting_param_tab,variable = self.poly3_value, text="Polynomial 3", command=polynomial3_bkgn)
        checkbutton_poly3.grid(column=6, row=4, sticky=W)
        checkbutton_poly3.state(['!alternate']) #Default is that baseline is always selected

        '''


        #-----Peak Shirley/SVSC Background------
        '''
        self.SVSC_selected = 1
        def SVSC_bkgn():
            global background_types
            global baseline_selected
            if (self.SVSC_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('SVSC_shirley')
                self.SVSC_selected = 1
            else: #state of button is on
                self.background_types.append('SVSC_shirley')
                self.SVSC_selected = 2

        checkbutton_doublet = ttk.Checkbutton(self.fitting_param_tab,text = "Peak-Shirley", command = SVSC_bkgn )
        checkbutton_doublet.grid(column=6,row =2,sticky = W)
        checkbutton_doublet.state(['!alternate'])
        '''
        '''
        #-----3 Parameter Tougaard-----

        self.tougaard3_selected = 1
        def tougaard3_bkgn():
            global background_types
            global baseline_selected
            if (self.tougaard3_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('3-Param Tougaard')
                self.tougaard3_selected = 1
            else: #state of button is on
                self.background_types.append('3-Param Tougaard')
                self.tougaard3_selected = 2

        if self.fit_file_selected == True:  
            for i in self.background_types:
                if i == '3-Param Tougaard':
                    self.tougaard3_selected = 2

        checkbutton_tougaard3 = ttk.Checkbutton(self.fitting_param_tab,variable = self.toug3_value,text = "3-Param Tougaard", command = tougaard3_bkgn )
        checkbutton_tougaard3.grid(column=6,row =2,sticky = W)
        checkbutton_tougaard3.state(['!alternate'])





        #-----2 Parameter Tougaard-----

        self.tougaard2_selected = 1
        def tougaard2_bkgn():
            global background_types
            global baseline_selected
            if (self.tougaard2_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('2-Param Tougaard')
                self.tougaard2_selected = 1
            else: #state of button is on
                self.background_types.append('2-Param Tougaard')
                self.tougaard2_selected = 2

        if self.fit_file_selected == True:  
            for i in self.background_types:
                if i == '2-Param Tougaard':
                    self.tougaard2_selected = 2

        checkbutton_tougaard2 = ttk.Checkbutton(self.fitting_param_tab,variable = self.toug2_value,text = "2-Param Tougaard", command = tougaard2_bkgn )
        checkbutton_tougaard2.grid(column=6,row =3,sticky = W)
        checkbutton_tougaard2.state(['!alternate'])
        




        #-----Shirley-Sherwood Background------

        self.shirley_selected = 1
        def shirley_bkgn():
            global background_types
            global shirley_selected
            if (self.shirley_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('Shirley-Sherwood')
                self.shirley_selected = 1
            else: #state of button is on
                self.background_types.append('Shirley-Sherwood')
                self.shirley_selected = 2
            return self.shirley_selected
        
        if self.fit_file_selected == True:  
            for i in self.background_types:
                if i == 'Shirley-Sherwood':
                    self.shirley_selected = 2
        
        checkbutton_shirley = ttk.Checkbutton(self.fitting_param_tab,variable = self.shirley_value, text="Shirley-Sherwood", command=shirley_bkgn)
        checkbutton_shirley.grid(column=4, row=2, sticky=W)
        checkbutton_shirley.state(['!alternate'])
        '''

        '''
         #-----SVSC Background------

        self.SVSC_selected = 1
        def SVSC_bkgn():
            global background_types
            global SVSC_selected
            if (self.SVSC_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('SVSC')
                self.SVSC_selected = 1
            else: #state of button is on
                self.background_types.append('SVSC')
                self.SVSC_selected = 2
            return self.SVSC_selected
        '''
        '''
        checkbutton_doublet = ttk.Checkbutton(self.fitting_param_tab, text="SVSC", command=SVSC_bkgn)
        checkbutton_doublet.grid(column=6, row=2, sticky=W)
        checkbutton_doublet.state(['!alternate'])
        '''

        #-----Integral Slope-----

        self.slope_selected = 1
        def integral_slope_bkgn():
            global background_types
            global slope_selected
            if (self.slope_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('Linear')
                self.slope_selected = 1
            else: #state of button is on
                self.background_types.append('Linear')
                self.slope_selected = 2
            return self.slope_selected
        
        if self.fit_file_selected == True:  
            for i in self.background_types:
                if i == 'Linear':
                    self.slope_selected = 2

        checkbutton_slope = ttk.Checkbutton(self.fitting_param_tab,variable = self.linear_value, text="Linear", command=integral_slope_bkgn)
        checkbutton_slope.grid(column=5, row=2, sticky=W)
        checkbutton_slope.state(['!alternate'])

        '''
        #-----Exponential-----
        self.exponential_selected = 1
        def exponential():
            global background_types
            global exponential_selected
            if (self.exponential_selected % 2) == 0: #state of button is off. Used when button is clicked on then off again.
                self.background_types.remove('Exponential')
                self.exponential_selected = 1
            else: #state of button is on
                self.background_types.append('Exponential')
                self.exponential_selected = 2
            return self.exponential_selected
        
        if self.fit_file_selected == True:  
            for i in self.background_types:
                if i == 'Exponential':
                    self.exponential_selected = 2

        checkbutton_exponential = ttk.Checkbutton(self.fitting_param_tab,variable = self.exp_value, text="Exponential", command=exponential)
        checkbutton_exponential.grid(column=4, row=3, sticky=W)
        checkbutton_exponential.state(['!alternate'])
        '''




        #Picker for background. No longer using --> changed to checkbuttons to allow for multiple
        #path_bkgns_entry = ttk.Combobox(self.fitting_param_tab, textvariable=self.path_bkgn, font=self.entryFont,
        #                               values=['Shirley-Sherwood', 'Linear']) #need to change to checkButton
        #path_bkgns_entry.grid(column=4, row=2, sticky=W)
        '''
        path_peakType = ttk.Label(self.fitting_param_tab, text="Fit Type", font=self.labelFont)
        path_peakType.grid_configure(column=2, row=5, sticky=W, padx=self.padx, pady=self.pady)
        path_peakTypes_entry = ttk.Combobox(self.fitting_param_tab, textvariable=self.path_peakType, font=self.entryFont,
                                       values= self.peak_types)
        path_peakTypes_entry.grid(column=2, row=5, sticky=W)
        '''



        updatePeakSelectionRows(0)














   
    def build_param_range_tab(self):
       
        """
        Build parameter ranges tab
        """
        arr_xes_peaks = ["Peak #"]
       
        self.num = int(self.number_of_peaks.get())
        #self.num = int(self.number_of_peaks.get())
        new_num = DoubleVar(self.root, 1)
        self.description_tabs(arr_xes_peaks, self.param_range_tab, row=[2])
        num_peaks_selected = [1,2,3,4,5,6,7,8,9,10]
        upper_limit_label = ttk.Label(self.param_range_tab,text = "Upper Limit",font = self.labelFont)
        upper_limit_label.grid(column = 3,row = 3,sticky = W, padx= self.padx,pady= self.pady)
        lower_limit_label = ttk.Label(self.param_range_tab,text = "Lower Limit",font = self.labelFont)
        lower_limit_label.grid(column = 2,row = 3,sticky = W, padx= self.padx,pady= self.pady)
        fixed_label = ttk.Label(self.param_range_tab,text = "Fixed",font = self.labelFont)
        fixed_label.grid(column = 4,row = 3,sticky = W, padx= self.padx,pady= self.pady)
        correlated_label = ttk.Label(self.param_range_tab,text = "Correlated Peak #",font = self.labelFont)
        correlated_label.grid(column = 5,row = 3,sticky = W, padx= self.padx,pady= self.pady)
        correlated_mult_label = ttk.Label(self.param_range_tab,text = "Correlated Multiplier",font = self.labelFont)
        correlated_mult_label.grid(column = 6,row = 3,sticky = W, padx= self.padx,pady= self.pady)
        #Maybe change "Correlated" to "Correlated Peak #" and add in "Correlation Multiplier"?

       
        def update_peaks(args):
            #self.num = int(self.number_of_peaks.get()) #This is effecting all the peaks --> Good for assigning correct vars but bad because final value it is left on is considered the number of peaks :(
            self.num = int(new_num.get())
            range_peak = ["Peak " + str(self.num), "Energy", "Sigma", "Gamma", "Amplitude"]
            
            self.range_peak_labels = self.description_tabs(range_peak,self.param_range_tab,row = [3, 4, 5, 6, 7])

            self.PE_up_lim_entry = ttk.Entry(self.param_range_tab, textvariable=self.PE_up_lim[self.num-1], font=self.entryFont, width=12)
            self.PE_up_lim_entry.grid(column=3, row=4, sticky=(W, E))
            self.PE_low_lim_entry = ttk.Entry(self.param_range_tab, textvariable=self.PE_low_lim[self.num-1], font=self.entryFont, width=12)
            self.PE_low_lim_entry.grid(column=2, row=4, sticky=(W, E))
            self.checkbutton_PE_lim = ttk.Checkbutton(self.param_range_tab, variable = self.PE_limit[self.num-1],onvalue= True,offvalue=False)
            self.checkbutton_PE_lim.grid(column=4, row=4, sticky=(W, E))
            self.checkbutton_PE_lim.state(['!alternate'])
            self.PE_corr_entry = ttk.Combobox(self.param_range_tab, textvariable=self.PE_corr[self.num-1], font=self.entryFont,values= num_peaks_selected, width = 5)
            self.PE_corr_entry.grid(column=5, row=4, sticky=(W, E))
            self.PE_corr_mult_entry = ttk.Entry(self.param_range_tab, textvariable=self.PE_corr_mult[self.num-1], font=self.entryFont, width=12)
            self.PE_corr_mult_entry.grid(column=6, row=4, sticky=(W, E))

            self.sigma_up_lim_entry = ttk.Entry(self.param_range_tab, textvariable=self.sigma_up_lim[self.num-1], font=self.entryFont, width=12)
            self.sigma_up_lim_entry.grid(column=3, row=5, sticky=(W, E))
            self.sigma_low_lim_entry = ttk.Entry(self.param_range_tab, textvariable=self.sigma_low_lim[self.num-1], font=self.entryFont, width=12)
            self.sigma_low_lim_entry.grid(column=2, row=5, sticky=(W, E))
            self.checkbutton_sigma_lim = ttk.Checkbutton(self.param_range_tab, variable = self.sigma_limit[self.num-1],onvalue= True,offvalue=False)
            self.checkbutton_sigma_lim.grid(column=4, row=5, sticky=(W, E))
            self.checkbutton_sigma_lim.state(['!alternate'])
            self.sigma_corr_entry = ttk.Combobox(self.param_range_tab, textvariable=self.sigma_corr[self.num-1], font=self.entryFont,values= num_peaks_selected, width = 5)
            self.sigma_corr_entry.grid(column=5, row=5, sticky=(W, E))
            self.sigma_corr_mult_entry = ttk.Entry(self.param_range_tab, textvariable=self.sigma_corr_mult[self.num-1], font=self.entryFont, width=12)
            self.sigma_corr_mult_entry.grid(column=6, row=5, sticky=(W, E))

            self.gamma_up_lim_entry = ttk.Entry(self.param_range_tab, textvariable=self.gamma_up_lim[self.num-1], font=self.entryFont, width=12)
            self.gamma_up_lim_entry.grid(column=3, row=6, sticky=(W, E))
            self.gamma_low_lim_entry = ttk.Entry(self.param_range_tab, textvariable=self.gamma_low_lim[self.num-1], font=self.entryFont, width=12)
            self.gamma_low_lim_entry.grid(column=2, row=6, sticky=(W, E))
            self.checkbutton_gamma_lim = ttk.Checkbutton(self.param_range_tab, variable = self.gamma_limit[self.num-1],onvalue= True,offvalue=False)
            self.checkbutton_gamma_lim.grid(column=4, row=6, sticky=(W, E))
            self.checkbutton_gamma_lim.state(['!alternate'])
            self.gamma_corr_entry = ttk.Combobox(self.param_range_tab, textvariable=self.gamma_corr[self.num-1], font=self.entryFont,values= num_peaks_selected, width = 5)
            self.gamma_corr_entry.grid(column=5, row=6, sticky=(W, E))
            self.gamma_corr_mult_entry = ttk.Entry(self.param_range_tab, textvariable=self.gamma_corr_mult[self.num-1], font=self.entryFont, width=12)
            self.gamma_corr_mult_entry.grid(column=6, row=6, sticky=(W, E))

            self.amp_up_lim_entry = ttk.Entry(self.param_range_tab, textvariable=self.amp_up_lim[self.num-1], font=self.entryFont, width=12)
            self.amp_up_lim_entry.grid(column=3, row=7, sticky=(W, E))
            self.amp_low_lim_entry = ttk.Entry(self.param_range_tab, textvariable=self.amp_low_lim[self.num-1], font=self.entryFont, width=12)
            self.amp_low_lim_entry.grid(column=2, row=7, sticky=(W, E))
            self.checkbutton_amp_lim = ttk.Checkbutton(self.param_range_tab, variable = self.amp_limit[self.num-1],onvalue= True,offvalue=False)
            self.checkbutton_amp_lim.grid(column=4, row=7, sticky=(W, E))
            self.checkbutton_amp_lim.state(['!alternate'])
            self.amp_corr_entry = ttk.Combobox(self.param_range_tab, textvariable=self.amp_corr[self.num-1], font=self.entryFont,values= num_peaks_selected, width = 5)
            self.amp_corr_entry.grid(column=5, row=7, sticky=(W, E))
            self.amp_corr_mult_entry = ttk.Entry(self.param_range_tab, textvariable=self.amp_corr_mult[self.num-1], font=self.entryFont, width=12)
            self.amp_corr_mult_entry.grid(column=6, row=7, sticky=(W, E))

          
        #WHY DOES THIS EFFECT THE ARRAY SIZE OF ALL ENTRIES????
        number_of_peaks_entry = ttk.Combobox(self.param_range_tab, textvariable=new_num, font=self.entryFont,values= num_peaks_selected, width = 5)
        number_of_peaks_entry.grid(column=2, row=2, sticky=(W, E)) #on same row as background checkbox
        number_of_peaks_entry.bind('<<ComboboxSelected>>', update_peaks)
        update_peaks(0)

        #self.range_peak_labels = self.description_tabs(num_peaks_selected,self.param_range_tab,row = [3])
        
        #ADD IN CORRELATED/LIMITED/FIXED RANGES FOR ENERGY, SIGMA, GAMMA, AMPLITUDE

















    def build_plot_tab(self):
        """
        Build plot tab
        """
        self.graph_tab.columnconfigure(0, weight=1)
        self.graph_tab.rowconfigure(1, weight=1)

        def plot_selection():
            #self.data_obj.pre_processing((self.percent_min.get(), self.percent_max.get()))
            data_plot.initial_parameters(self.data_obj, self.data_KE, self.data_XES)
            data_plot.plot_selected()

        def plot_raw():
            global data_KE
            global data_XES
            #self.data_obj.pre_processing((self.percent_min.get(), self.percent_max.get()))
            data_plot.initial_parameters(self.data_obj, self.data_KE, self.data_XES)
            x = []
            y = []
            x.append(self.data_obj.get_x(self.data_KE, self.data_XES))
            y.append(self.data_obj.get_y(self.scale_var))
           

            data_plot.plot(x,y,'Raw Data', 'Raw Data', self.scale_var,self.data_KE, self.data_XES)
            
        def get_scale():
            return self.scale_var 
           

        def plot_both():
            global data_KE
            global data_XES
            self.data_obj.pre_processing((self.percent_min.get(), self.percent_max.get()))
            data_plot.initial_parameters(self.data_obj, self.data_KE, self.data_XES, title=self.csv_generate_from.stem)
            data_plot.plot_raw_and_selected()

        data_plot = Data_plot(self.graph_tab)
        self.plot_button = ttk.Button(self.graph_tab, text='Plot Data', command=plot_raw)
        self.plot_button.grid(column=0, row=0, columnspan=1, sticky=W, padx=self.padx, pady=self.pady)
        self.plot_selected_button = ttk.Button(self.graph_tab, text='Plot Selected Range', command=plot_selection)
        self.plot_selected_button.grid(column=1, row=0, columnspan=1, sticky=W, padx=self.padx, pady=self.pady)

        self.plot_both_button = ttk.Button(self.graph_tab, text='Plot Raw and Selected', command=plot_both)
        self.plot_both_button.grid(column=2, row=0, columnspan=1, sticky=W, padx=self.padx, pady=self.pady)

        
     
    def generate_randomized_ini(self, multifolder, i):
        pop_range = np.arange(self.pop_min.get(), self.pop_max.get(), 100)
        gen_range = np.arange(self.gen_min.get(), self.gen_max.get(), 5)
        mut_range = np.arange(self.mut_min.get(), self.mut_max.get(), 10)

        self.population.set(np.random.choice(pop_range))
        self.num_gen.set(np.random.choice(gen_range))
        self.chance_of_mutation.set(np.random.choice(mut_range))
        name = self.csv_generate_from.stem

        def unique_path():
            counter = i
            while True:
                num_name = str(name) + "_" + str(counter) + '.ini'
                path = self.output_folder_path.joinpath(num_name)
                if not path.exists():
                    return path
                counter += 1

        file_path = unique_path()
        file_path.touch()
        self.write_ini(file_path)

    def generate_multi_ini(self):
        if self.run_folder.get():  # They want to generate ini for every file in directory
            # generates list of files within the folder
            file_list = [filename for filename in self.csv_folder_path.glob('**/*txt') if filename.is_file()]
            # Loop through each file and generate proper number of ini files
            # stem = self.output_folder_path.stem
            # parent = self.output_folder_path.parent
            for i in range(len(file_list)):
                # set the generate_from file to the current file
                self.csv_generate_from = file_list[i]
                fname = file_list[i].stem
                # create specified number of iterations for this file
                for j in range(self.n_ini.get()):
                    # Gives the output path a unique file name
                    name = fname + '_' + str(j) + '_out' + '.txt'
                    output_path = self.output_folder_path.joinpath(name)
                    # output_path.touch()
                    self.output_file = output_path
                    # print("generate_multi output name: ", self.output_folder_path)
                    self.generate_randomized_ini(self.output_folder_path, j)
        else:
            # stem = self.output_folder_path.stem
            for i in range(self.n_ini.get()):
                # Gives the output path a unique file name
                name = self.csv_generate_from.stem + '_' + str(i) + '_out' + '.txt'
                # parent = self.output_folder_path.parent
                output_path = self.output_folder_path.joinpath(name)
                # output_path.touch()
                self.output_file = output_path
                # print("generate_multi output name: ", self.output_folder_path)
                self.generate_randomized_ini(self.output_folder_path, i)
        return self.output_folder_path

    def stop_all(self):
        self.stop_not_pressed = False
        for i in self.proc_list:
            i.kill()
            i.wait()
        while not self.command_list.empty():
            self.command_list.get()
        print("Stopped xes_neo")

    def run_ini_in_command_list(self, flag):
        global loop
        if self.stop_not_pressed and not self.command_list.empty():
            each = self.command_list.get()
            command = "exec xes_neo -i " + each #changed to xes_neo
            self.proc = subprocess.Popen(command, shell=True)
            self.proc.wait()
            self.proc_list.append(self.proc)
            loop = self.root.after(self.run_ini_in_command_list(True))
        else:
            try:
                self.root.after_cancel(loop)
            except:
                pass

        # while self.stop_not_pressed and len(self.command_list) > 0:

    def set_command_list(self):
        self.output_folder_path = self.generate_multi_ini()
        print("in run multi. flag value", self.stop_not_pressed)
        file_list = [f'"{_file.absolute().as_posix()}"' for _file in self.output_folder_path.glob('**/*.ini') if
                     _file.is_file()]
        print("File list in run multi ", file_list)
        for i in range(len(file_list)):
            print("in for ", i)
            self.command_list.put(file_list[i])

    def run_multi_ini(self):
        # Runs all instances of a single file

        print("before loop")
        global loop
        if self.stop_not_pressed and self.command_list:
            print("Stop not pressed and files exist")
            # print("\n\n\n\n\n")
            each = self.command_list.get()
            command = "exec xes_neo -i " + each #changed from nano_neo to xes_neo
            self.proc = subprocess.Popen(command, shell=True)
            self.proc_list.append(self.proc)
            self.pid_list.append(self.proc.pid)
            # print("Current process ID: ", self.proc.pid)
            loop = self.root.after(0, self.run_multi_ini)
            self.proc.wait()
        else:
            # print("in else")
            try:
                # print("trying to cancel")
                self.root.after_cancel(loop)
                # Empty any unrun commands so they do not run on next iteration
                while self.command_list:
                    self.command_list.get()
            except:
                print("In pass")
                pass
            self.stop_not_pressed = True

        # if self.stop_not_pressed:
        #   print("if self.stop_not_pressed is yes")
        #  self.output_folder_path = self.generate_multi_ini()
        # if self.output_folder.get() =='Please choose a folder to save outputs' or not self.output_folder_path:
        #    print("skipped to not running pls work")
        #   return
        # else:
        #   print("in else of run multi")
        # file_list = [str(filename) for filename in self.output_folder_path.glob('**/*.ini') if filename.is_file()]
        # file_list = [f'"{_file.absolute().as_posix()}"' for _file in self.output_folder_path.glob('**/*.ini') if
        #            _file.is_file()]
        #  print("File list in run multi ", file_list)
        # for i in range(len(file_list)):
        #    print("in for ", i)
        #   self.command_list.append(file_list[i])
        # pls_run(self.stop_not_pressed)
        # else:
        #   print("else of run_multi should cause stop")
        #  pls_run(self.stop_not_pressed) # looks the same but it will send in false (hopefully) & cause after_cancel

        # self.run_ini_in_command_list(True)

    def runningThread(self):
        t1 = Thread(target=self.runningmulti)
        print("In runningThread")
        t1.start()

    def runningmulti(self):
        self.set_command_list()
        self.run_multi_ini()

    def build_output_tab(self):
        """
        Will allow for multiple iterations over the same data to be performed
        Each time create & save ini, run, save outputs
        """

        # pertub_check = IntVar(self.output_tab, 0)

        def checkbox_multi():
            widget_lists = [
                entry_n_ini,
                entry_pertub_pop_min,
                entry_pertub_pop_max,
                entry_pertub_gen_min,
                entry_pertub_gen_max,
                entry_pertub_mut_min,
                entry_pertub_mut_max,
                button_gen_nini,
                button_run_nini]
            if self.pertub_check.get() == 0:
                for i in widget_lists:
                    i.config(state='disabled')
                    self.checkbutton_whole_folder.config(state='disabled')
            elif self.pertub_check.get() == 1:
                for i in widget_lists:
                    i.config(state='normal')
                    if self.yes_folder.get() == 1:  # Check to see if folder is selected
                        self.checkbutton_whole_folder.config(state='normal')

        arr_out = ["Print graph", "Steady state exit"]
        self.description_tabs(arr_out, self.output_tab)

        checkbutton_print_graph = ttk.Checkbutton(self.output_tab, var=self.print_graph)
        checkbutton_print_graph.grid(column=1, row=0, sticky=W + E, padx=self.padx)

        checkbutton_steady_state = ttk.Checkbutton(self.output_tab, var=self.steady_state_exit)
        checkbutton_steady_state.grid(column=1, row=1, sticky=W + E, padx=self.padx)

        # Create separators
        separator = ttk.Separator(self.output_tab, orient='horizontal')
        separator.grid(column=0, row=2, columnspan=4, sticky=W + E, padx=self.padx)
        self.output_tab.columnconfigure(3, weight=1)

        arr_out = ["Create Multiple Input Files", "Number of Ini Files", "Pertubutions-Population(min,max)",
                   "Pertubutions-Generation(min,max)", "Pertubutions-Mutation(min,max)"]
        self.description_tabs(arr_out, self.output_tab, row=[3, 5, 6, 7, 8])
        # Create New pertubutuions

        checkbutton_pertub = ttk.Checkbutton(self.output_tab, var=self.pertub_check, command=checkbox_multi)
        checkbutton_pertub.grid(column=1, row=3, sticky=W + E, padx=self.padx)

        pertub_list = list(range(1, 101))

        text = 'Each entry allows user to control perturbation percentage of the desire variables.'
        entry = ttk.Label(self.output_tab, text=text, font=self.labelFont)
        entry.grid_configure(column=0, row=4, columnspan=3, sticky=W + E, padx=self.padx, pady=self.pady)

        entry_n_ini = ttk.Entry(self.output_tab, textvariable=self.n_ini, font=self.entryFont)
        entry_n_ini.grid(column=1, row=5, columnspan=2, sticky=(W, E), padx=self.padx)
        entry_n_ini.config(state='disabled')

        width = 5
        # --------------
        entry_pertub_pop_min = ttk.Entry(self.output_tab, width=width, textvariable=self.pop_min, font=self.entryFont)
        entry_pertub_pop_min.grid(column=1, row=6, sticky=(W, E), padx=self.padx)

        entry_pertub_pop_max = ttk.Entry(self.output_tab, width=width, textvariable=self.pop_max, font=self.entryFont)
        entry_pertub_pop_max.grid(column=2, row=6, sticky=(W, E), padx=self.padx)

        entry_pertub_pop_min.config(state='disabled')
        entry_pertub_pop_max.config(state='disabled')

        # --------------
        entry_pertub_gen_min = ttk.Entry(self.output_tab, width=width, textvariable=self.gen_min, font=self.entryFont)
        entry_pertub_gen_min.grid(column=1, row=7, sticky=(W, E), padx=self.padx)

        entry_pertub_gen_max = ttk.Entry(self.output_tab, width=width, textvariable=self.gen_max, font=self.entryFont)
        entry_pertub_gen_max.grid(column=2, row=7, sticky=(W, E), padx=self.padx)

        entry_pertub_gen_min.config(state='disabled')
        entry_pertub_gen_max.config(state='disabled')

        # --------------
        entry_pertub_mut_min = ttk.Entry(self.output_tab, width=width, textvariable=self.mut_min, font=self.entryFont)
        entry_pertub_mut_min.grid(column=1, row=8, sticky=(W, E), padx=self.padx)

        entry_pertub_mut_max = ttk.Entry(self.output_tab, width=width, textvariable=self.mut_max, font=self.entryFont)
        entry_pertub_mut_max.grid(column=2, row=8, sticky=(W, E), padx=self.padx)

        entry_pertub_mut_min.config(state='disabled')
        entry_pertub_mut_max.config(state='disabled')

        # --------------

        button_gen_nini = ttk.Button(self.output_tab, text="Generate Input Files", command=self.generate_multi_ini)
        button_gen_nini.grid(column=0, row=9, columnspan=3, sticky=W + E, padx=self.padx, pady=self.pady)
        button_gen_nini.config(state='disabled')

        button_run_nini = ttk.Button(self.output_tab, text="Run All Instances",
                                     command=lambda: [self.set_command_list(), self.run_multi_ini()])
        button_run_nini.grid(column=0, row=10, columnspan=3, sticky=W + E, padx=self.padx, pady=self.pady)
        button_run_nini.config(state='disabled')

        # Adding button to chose if run all files in the folder
        self.checkbutton_whole_folder = ttk.Checkbutton(self.output_tab, var=self.run_folder)
        self.checkbutton_whole_folder.grid(column=1, row=11, sticky=W + E, padx=self.padx)
        self.checkbutton_whole_folder.config(state='disabled')

        checkbutton_label = ttk.Label(self.output_tab,
                                      text="Check to generate/run iterations for each file in the directory",
                                      font=self.labelFont)
        checkbutton_label.grid(column=0, row=11, sticky=W)
#___Analysis Tab____________________________________________________________________________________________
    def build_analysis_tab(self):
    
        def select_analysis_folder():
            os.chdir(pathlib.Path.cwd().parent)  # change the working directory from gui to nano-indent

            self.folder_name = filedialog.askdirectory(initialdir=pathlib.Path.cwd(), title="Choose a folder")
            if not self.folder_name:
                self.analysis_dir.set('Please choose a directory')
            else:
                # folder_name = os.path.join(folder_name,'feff')
                self.analysis_dir.set(self.folder_name)

            os.chdir(pathlib.Path.cwd().joinpath('gui'))

        def calculate_and_plot():
            #self.background_types = ['Shirley-Sherwood', 'Slope', 'Exponential', 'Baseline', 'Polynomial 1', 'Polynomial 2', 'Polynomial 3', '3-Param Tougaard', '2-Param Tougaard']

            params = {
                'base': pathlib.Path.cwd().parent,
                'file': self.csv_generate_from,
                'fileName' : self.csv_file.get(),
                'peaks' : self.peak_types,
                'bkgns' : self.background_types,
                'data obj' : self.data_obj


            }

            self.params,self.errors, self.errors_bkgns, self.peak_areas, self.FWHM_values, self.peak_y_vals, self.totalFit, self.background_fit, self.residual_fit, self.y_raw, self.upper_error_area, self.lower_error_area = self.analysis_obj.initial_parameters(self.analysis_dir,params,self.scale_var,self.data_KE, self.data_XES, peakType='Voigt',title='Fit')

            #get_params_for_export()
            self.numPeaks = int(self.number_of_peaks.get()) #This only works if you select number of peaks in fitting paramters tab,not if you just want to look at previous fit

            i=int(self.peak_number.get()-1)
            peakType = self.params[i][-1] #Last element in array is the curve fit type

            if i > self.numPeaks:
                print("Number of peaks limit reached")
                pass
           
            if(peakType.lower() == "lorentzian"):
                PE_text = str(round(self.params[i][0],2)) + "  " + "+/-" + "  " + str(self.errors[i][0])
                self.PE_text = StringVar(value=PE_text)

                lorentzian_text = str(round(self.params[i][1],3)) + "  " + "+/-" + "  " + str(self.errors[i][1])
                self.lorentzian_text = StringVar(value=lorentzian_text)

                amp_text = str(round(self.params[i][2],2)) + "  " + "+/-" + "  " + str(self.errors[i][2])
                self.amp_text = StringVar(value=amp_text)

                area_text = str(round(self.peak_areas[i],2)) + "  " + "+/-" + "  " + str(round(self.upper_error_area[i],3))
                self.area_text = StringVar(value=area_text)

                FWHM_text = str(round(self.FWHM_values[i],2))
                self.FWHM_text = StringVar(value=FWHM_text)

                self.peak_energy_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.PE_text, font=self.entryFont)
                self.peak_energy_entries[i].grid(column=1, row=2, sticky=(W, E))

                self.sigma_entries[i] = ttk.Label(self.analysis_tab, textvariable="0", font=self.entryFont)
                self.sigma_entries[i].grid(column=1, row=3, sticky=(W, E))

                self.lorentzian_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.lorentzian_text, font=self.entryFont)
                self.lorentzian_entries[i].grid(column=1, row=4, sticky=(W, E))

                self.amp_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.amp_text, font=self.entryFont)
                self.amp_entries[i].grid(column=1, row=5, sticky=(W, E))

                self.area_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.area_text, font=self.entryFont)
                self.area_entries[i].grid(column=1, row=6, sticky=(W, E))

                self.FWHM_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.FWHM_text, font=self.entryFont)
                self.FWHM_entries[i].grid(column=1, row=7, sticky=(W, E))


            elif(peakType.lower() == "gaussian"):
               
                PE_text = str(round(self.params[i][0],2)) + "  " + "+/-" + "  " + str(self.errors[i][0])
                self.PE_text = StringVar(value=PE_text)

                sigma_text = str(round(self.params[i][1],3)) + "  " + "+/-" + "  " + str(self.errors[i][1])
                self.sigma_text = StringVar(value=sigma_text)

                amp_text = str(round(self.params[i][2],2)) + "  " + "+/-" + "  " + str(self.errors[i][2])
                self.amp_text = StringVar(value=amp_text)

                area_text = str(round(self.peak_areas[i],2)) + "  " + "+/-" + "  " + str(round(self.upper_error_area[i],3))
                self.area_text = StringVar(value=area_text)

                FWHM_text = str(round(self.FWHM_values[i],2))
                self.FWHM_text = StringVar(value=FWHM_text)

                self.peak_energy_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.PE_text, font=self.entryFont)
                self.peak_energy_entries[i].grid(column=1, row=2, sticky=(W, E))

                self.sigma_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.sigma_text, font=self.entryFont)
                self.sigma_entries[i].grid(column=1, row=3, sticky=(W, E))

                self.lorentzian_entries[i] = ttk.Label(self.analysis_tab, textvariable="0", font=self.entryFont)
                self.lorentzian_entries[i].grid(column=1, row=4, sticky=(W, E))

                self.amp_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.amp_text, font=self.entryFont)
                self.amp_entries[i].grid(column=1, row=5, sticky=(W, E))

                self.area_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.area_text, font=self.entryFont)
                self.area_entries[i].grid(column=1, row=6, sticky=(W, E))

                self.FWHM_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.FWHM_text, font=self.entryFont)
                self.FWHM_entries[i].grid(column=1, row=7, sticky=(W, E))

            else: #Voigt, Double-Lorentzian, Doniach-Sunjic --> Asymmetry values not being shown right now


                PE_text = str(round(self.params[i][0],2)) + "  " + "+/-" + "  " + str(self.errors[i][0])
                self.PE_text = StringVar(value=PE_text)

                sigma_text = str(round(self.params[i][1],3)) + "  " + "+/-" + "  " + str(self.errors[i][1])
                self.sigma_text = StringVar(value=sigma_text)

                lorentzian_text = str(round(self.params[i][2],3)) + "  " + "+/-" + "  " + str(self.errors[i][2])
                self.lorentzian_text = StringVar(value=lorentzian_text)

                amp_text = str(round(self.params[i][3],2)) + "  " + "+/-" + "  " + str(self.errors[i][3])
                self.amp_text = StringVar(value=amp_text)

                area_text = str(round(self.peak_areas[i],2)) + "  " + "+/-" + "  " + str(round(self.upper_error_area[i],3))
                self.area_text = StringVar(value=area_text)

                FWHM_text = str(round(self.FWHM_values[i],2))
                self.FWHM_text = StringVar(value=FWHM_text)

                self.peak_energy_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.PE_text, font=self.entryFont)
                self.peak_energy_entries[i].grid(column=1, row=2, sticky=(W, E))

                self.sigma_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.sigma_text, font=self.entryFont)
                self.sigma_entries[i].grid(column=1, row=3, sticky=(W, E))

                self.lorentzian_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.lorentzian_text, font=self.entryFont)
                self.lorentzian_entries[i].grid(column=1, row=4, sticky=(W, E))

                self.amp_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.amp_text, font=self.entryFont)
                self.amp_entries[i].grid(column=1, row=5, sticky=(W, E))

                self.area_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.area_text, font=self.entryFont)
                self.area_entries[i].grid(column=1, row=6, sticky=(W, E))

                self.FWHM_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.FWHM_text, font=self.entryFont)
                self.FWHM_entries[i].grid(column=1, row=7, sticky=(W, E))

            #updateExportDataRows(self)

        # def get_params_for_export():
        #     self.analysis_export = self.analysis_obj.get_params(self)
        #     return self.analysis_export

        # Labels
        self.num_peak_labels =[0]*10
        self.sigma_labels = [0]*10
        self.lorentzian_labels = [0]*10
        self.amp_labels = [0]*10
        self.area_labels = [0]*10
        self.FWHM_labels = [0]*10
        # Entries
        self.peak_energy_entries = [0]*10
        self.sigma_entries = [0]*10
        self.lorentzian_entries = [0]*10
        self.amp_entries = [0]*10
        self.area_entries = [0]*10
        self.FWHM_entries = [0]*10
        # Export Data Values
        self.peak_energy_export = [0]*10
        self.sigma_export = [0]*10
        self.lorentzian_export = [0]*10
        self.amp_export = [0]*10
        self.area_export = [0]*10
        self.FWHM_export = [0]*10



        def export_indi_peak_fit():
            x = []
            y = []
            total_fit = []

            x.append(self.data_obj.get_x(self.data_KE, self.data_XES))
            y.append(self.data_obj.get_y(self.scale_var))

            XES_Oasis_out_name = self.csv_generate_from.stem + "_fit_Aanalyzer" + '.fil'
            os.chdir(pathlib.Path.cwd().parent)
            XES_Oasis_Fit_folder_path = pathlib.Path(self.folder_name)
            XES_Oasis_Fit_file = XES_Oasis_Fit_folder_path.joinpath(XES_Oasis_out_name)
            os.chdir(pathlib.Path.cwd().joinpath('gui'))
            XES_Oasis_Fit_file = open(XES_Oasis_Fit_file, "w")

            XES_Oasis_Fit_file.write(str("spectraIsIncludedInFil"))
            XES_Oasis_Fit_file.write(str(" \n"))
            #PE condition:
            #XES_Oasis_Fit_file.write(str("drawBindingEnergy"))
            #XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("nextData 0"))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("fileName"))
            XES_Oasis_Fit_file.write(str(" "))
            XES_Oasis_Fit_file.write(str(self.csv_generate_from.stem))
            XES_Oasis_Fit_file.write(str(".txt"))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("spectrumStarts"))
            XES_Oasis_Fit_file.write(str(" \n"))


            #Changed output format to be similiar to Aanalyzer. Only have to output one file to enter into Igor pro to make graphs.
            peak_num = len(self.peak_y_vals)
            out_name = self.csv_generate_from.stem + "_Fit_Arrays" + '.txt'
            os.chdir(pathlib.Path.cwd().parent)
            peakFit_folder_path = pathlib.Path(self.folder_name)
            peakFit_file = peakFit_folder_path.joinpath(out_name)
            os.chdir(pathlib.Path.cwd().joinpath('gui'))
            peakFit_file = open(peakFit_file, "w")
            peakFit_file.write(str("x"))
            peakFit_file.write(str("  "))
            peakFit_file.write(str("yExp"))
            peakFit_file.write(str("  "))
            peakFit_file.write(str("yCal"))
            peakFit_file.write(str("  "))
            peakFit_file.write(str("Bkgn"))
            for i in range(peak_num):
                peakFit_file.write(str("  "))
                peakFit_file.write(str("peak")+str(i+1))
            peakFit_file.write(str(" \n"))
            for j in range(len(x[0])):
                peakFit_file.write(str(x[0][j]))
                peakFit_file.write(str("  "))
                peakFit_file.write(str(self.y_raw[j]))
                peakFit_file.write(str("  "))
                peakFit_file.write(str(self.totalFit[j]))
                peakFit_file.write(str("  "))
                peakFit_file.write(str(self.background_fit[j]))
                peakFit_file.write(str("  "))
                for i in range(peak_num):
                    peakFit_file.write(str(self.peak_y_vals[i][j]))
                    peakFit_file.write(str("  "))
                peakFit_file.write(str(" \n"))
      
            
            peakFit_file.close()



            '''
            for i in range(len(self.peak_y_vals)):

                out_name = self.csv_generate_from.stem + "_" + "Peak" + "_" + str(i+1) + "_" + "fit" + '.txt'
                total_out_name = self.csv_generate_from.stem + "_" + "Total" + "_" + "fit" + '.txt'
                background_out_name = self.csv_generate_from.stem + "_" + "Background" + "_" + "fit" + '.txt'
                residual_out_name = self.csv_generate_from.stem + "_" + "Residual" + "_" + "fit" + '.txt'
                os.chdir(pathlib.Path.cwd().parent)
                #Add in output for raw data with updated scale to zero --> Or do we add back in the scale to all the other arrays???

                peakFit_folder_path = pathlib.Path(self.folder_name)
                peakFit_file = peakFit_folder_path.joinpath(out_name)
                totalPeakFit_folder_path = pathlib.Path(self.folder_name)
                totalPeakFit_file = totalPeakFit_folder_path.joinpath(total_out_name)
                backgroundFit_folder_path = pathlib.Path(self.folder_name)
                backgroundFit_file = backgroundFit_folder_path.joinpath(background_out_name)
                residualFit_folder_path = pathlib.Path(self.folder_name)
                residualFit_file = residualFit_folder_path.joinpath(residual_out_name)

                os.chdir(pathlib.Path.cwd().joinpath('gui'))



                peakFit_file = open(peakFit_file, "w")
                totalPeakFit_file = open(totalPeakFit_file, "w")
                backgroundFit_file = open(backgroundFit_file, "w")
                residualFit_file = open(residualFit_file, "w")


                #Need to reverse x for saving
                for j in range(len(x[0])):

                    peakFit_file.write(str(x[0][j]))
                    peakFit_file.write(str("  "))
                    peakFit_file.write(str(self.peak_y_vals[i][j])) #Individual peak fit components
                    peakFit_file.write(str(" \n"))
                    totalPeakFit_file.write(str(x[0][j]))
                    totalPeakFit_file.write(str("  "))
                    totalPeakFit_file.write(str(self.totalFit[j]))
                    totalPeakFit_file.write(str(" \n"))
                    backgroundFit_file.write(str(x[0][j]))
                    backgroundFit_file.write(str("  "))
                    backgroundFit_file.write(str(self.background_fit[j]))
                    backgroundFit_file.write(str(" \n"))
                    residualFit_file.write(str(x[0][j]))
                    residualFit_file.write(str("  "))
                    residualFit_file.write(str(self.residual_fit[j]))
                    residualFit_file.write(str(" \n"))


                peakFit_file.close()
                totalPeakFit_file.close()
                backgroundFit_file.close()

                print("Peak ", i+1, " information saved to output file location")
            '''

            photonEnergy = 1486.6


            for j in range(len(x[0])):
                if x[0][0] < x[0][-1]: #KE condition
                    x_value = x[0][j]
                else:
                    x_value = photonEnergy - x[0][j]
                XES_Oasis_Fit_file.write(str(x_value))
                XES_Oasis_Fit_file.write(str("  "))
                XES_Oasis_Fit_file.write(str(y[0][j]))
                XES_Oasis_Fit_file.write(str(" \n"))

            XES_Oasis_Fit_file.write(str("spectrumEnds"))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("comment")) #Allow for users to input comments?
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("skipLines"))
            XES_Oasis_Fit_file.write(str(" "))
            XES_Oasis_Fit_file.write(str(self.skipLn.get()))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("xChannel 0 yChannel 1"))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str(" shift         0  offset         0  gain         1  externalX         0"))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("Parameters"))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("recoverParameters"))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("leftLimit"))
            XES_Oasis_Fit_file.write(str("    "))
            XES_Oasis_Fit_file.write(str(x[0][0]))
            XES_Oasis_Fit_file.write(str("   "))
            XES_Oasis_Fit_file.write(str("rightLimit"))
            XES_Oasis_Fit_file.write(str("    "))
            XES_Oasis_Fit_file.write(str(x[0][-1]))
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("tolerance       0.01")) #Idk if we need this parameter in XES Neo
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("maxNumIterations  4")) # Set to default Aanalyzer value
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("iterationsIntegralBkgn  6")) # Set to default Aanalyzer value
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("photonEnergy     1486.6")) #Allow for this to change based on user photonEnergy input
            XES_Oasis_Fit_file.write(str(" \n"))
            XES_Oasis_Fit_file.write(str("backgroundTypeNew"))
            XES_Oasis_Fit_file.write(str(" \n"))
            #Finding and writing out all the background parameters to fit file
            for i in range(len(self.params)):
                for j in range(len(self.params[i])):
                    if self.params[i][j] == 'Baseline':
                        XES_Oasis_Fit_file.write(str(" Poly0 poly0Bkgn   "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j-1]))
                        XES_Oasis_Fit_file.write(str("  free"))
                        XES_Oasis_Fit_file.write(str(" \n"))


                    elif self.params[i][j] == 'Polynomial 1':
                        XES_Oasis_Fit_file.write(str(" Poly1 poly1Bkgn   "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j-1]))
                        XES_Oasis_Fit_file.write(str("  free"))
                        XES_Oasis_Fit_file.write(str(" \n"))

                    elif self.params[i][j] == 'Polynomial 2':
                        XES_Oasis_Fit_file.write(str(" Poly2 poly2Bkgn   "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j-1]))
                        XES_Oasis_Fit_file.write(str("  free"))
                        XES_Oasis_Fit_file.write(str(" \n"))

                    elif self.params[i][j] == 'Polynomial 3':
                        XES_Oasis_Fit_file.write(str(" Poly3 poly3Bkgn   "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j-1]))
                        XES_Oasis_Fit_file.write(str("  free"))
                        XES_Oasis_Fit_file.write(str(" \n"))

                    elif self.params[i][j] == 'Exponential': #Exponential is done in combo with tougaard CTou2PActive/CTou3PActive line IDK if it will work if not written like that
                        XES_Oasis_Fit_file.write(str(" Exp exponent   "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j-1]))
                        XES_Oasis_Fit_file.write(str("  free"))
                        XES_Oasis_Fit_file.write(str(" \n"))

                    elif self.params[i][j] == 'Shirley-Sherwood':
                        XES_Oasis_Fit_file.write(str(" Int integralBkgn ")) #IDK why but Aanalyzer has it that this is called something else when Slope AND Shirley are selected
                        XES_Oasis_Fit_file.write(str(self.params[i][j-1])) #IntSlope integralSlopeBkgn
                        XES_Oasis_Fit_file.write(str("  free"))
                        XES_Oasis_Fit_file.write(str(" \n"))

                    elif self.params[i][j] == 'Linear':
                        XES_Oasis_Fit_file.write(str(" Int integralBkgn "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j-1]))
                        XES_Oasis_Fit_file.write(str("  free"))
                        XES_Oasis_Fit_file.write(str(" \n"))


                    elif self.params[i][j] == '2-Param Tougaard':
                        XES_Oasis_Fit_file.write(str(" useTou2PActive BTou2PActive      "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j+1])) #We need to have this parameter printed out #B2
                        XES_Oasis_Fit_file.write(str("  fix")) #This is currently the only parameter being held fixed
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str(" CTou2PActive      "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j+1]))

                    elif self.params[i][j] == '3-Param Tougaard':
                        XES_Oasis_Fit_file.write(str(" useTou3PActive BTou3PActive      "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j+1])) #We need to have this parameter printed out #B3
                        XES_Oasis_Fit_file.write(str("  free"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str(" CTou3PActive      "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j+1]))
                        XES_Oasis_Fit_file.write(str("    "))
                        XES_Oasis_Fit_file.write(str(" DTou3PActive      "))
                        XES_Oasis_Fit_file.write(str(self.params[i][j+2]))

            #Getting fit components of each peak
            for k in range(len(self.peak_y_vals)):
                XES_Oasis_Fit_file.write(str("nextPeak "))
                XES_Oasis_Fit_file.write(str(k))
                XES_Oasis_Fit_file.write(str(" \n"))



                peakType = self.params[k][-1]

                photonEnergy = 1486.6 #Want as user input later
                if x[0][0] < x[0][-1]: #KE condition
                    KE = self.params[k][0]
                else:
                    KE = photonEnergy - self.params[k][0] #Values are read in BE in Aanalyzer



                if(peakType.lower() == "lorentzian"):
                    if len(self.params[k]) >= 5:
                        XES_Oasis_Fit_file.write(str("doublet"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str(self.params[k][3])) #This needs to be negative in Aanalyzer
                        XES_Oasis_Fit_file.write(str(" free"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str("branchingRatio      "))
                        XES_Oasis_Fit_file.write(str("0.75")) #WE DO NOT HAVE A WAY OF OUTPUTTING THIS RIGHT NOW --> FIX THIS
                        XES_Oasis_Fit_file.write(str(" fix"))
                        XES_Oasis_Fit_file.write(str(" \n"))

                    else:
                        XES_Oasis_Fit_file.write(str("singlet"))
                        XES_Oasis_Fit_file.write(str(" \n"))

                    XES_Oasis_Fit_file.write(str("gauss   1 limited"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("lorentzian      "))
                    XES_Oasis_Fit_file.write(str(self.params[k][1]))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("energy   "))
                    XES_Oasis_Fit_file.write(str(KE))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("asymmetry         1  limitUp    10 limitDown     1"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("asymmetryDoniach       0.1  limitUp     1 limitDown     0"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("area   "))
                    XES_Oasis_Fit_file.write(str(self.peak_areas[k]))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("peakType "))
                    XES_Oasis_Fit_file.write(str(peakType))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("peakColor clOlive")) #Change this based on k
                    XES_Oasis_Fit_file.write(str(" \n"))

                elif(peakType.lower() == "gaussian"):
                    if len(self.params[k]) >= 5:
                        XES_Oasis_Fit_file.write(str("doublet"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str("soSplitting  "))
                        XES_Oasis_Fit_file.write(str(self.params[k][3]))
                        XES_Oasis_Fit_file.write(str(" free"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str("branchingRatio      "))
                        XES_Oasis_Fit_file.write(str("0.75")) #WE DO NOT HAVE A WAY OF OUTPUTTING THIS RIGHT NOW --> FIX THIS
                        XES_Oasis_Fit_file.write(str(" fix"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                    else:
                        XES_Oasis_Fit_file.write(str("singlet"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("gauss   "))
                    gauss = self.params[k][1] * 2 * np.sqrt(2*np.log(2.0))
                    XES_Oasis_Fit_file.write(str(gauss))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("lorentzian      0.27 limited"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("energy   "))
                    XES_Oasis_Fit_file.write(str(KE))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("asymmetry         1  limitUp    10 limitDown     1"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("asymmetryDoniach       0.1  limitUp     1 limitDown     0"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("area   "))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("peakType "))
                    XES_Oasis_Fit_file.write(str(peakType))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("peakColor clOlive")) #Change this based on k
                    XES_Oasis_Fit_file.write(str(" \n"))

                elif(peakType.lower() == "voigt"):
                    if len(self.params[k]) >= 6:
                        XES_Oasis_Fit_file.write(str("doublet"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str("soSplitting  "))
                        XES_Oasis_Fit_file.write(str(self.params[k][4]))
                        XES_Oasis_Fit_file.write(str(" free"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str("branchingRatio      "))
                        XES_Oasis_Fit_file.write(str("0.75")) #WE DO NOT HAVE A WAY OF OUTPUTTING THIS RIGHT NOW --> FIX THIS
                        XES_Oasis_Fit_file.write(str(" fix"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                    else:
                        XES_Oasis_Fit_file.write(str("singlet"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("gauss   "))
                    gauss = self.params[k][1] * 2 * np.sqrt(2*np.log(2.0))
                    XES_Oasis_Fit_file.write(str(gauss))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("lorentzian      "))
                    XES_Oasis_Fit_file.write(str(self.params[k][2]))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("energy   "))
                    XES_Oasis_Fit_file.write(str(KE))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("asymmetry         1  limitUp    10 limitDown     1"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("asymmetryDoniach       0.1  limitUp     1 limitDown     0"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("area   "))
                    XES_Oasis_Fit_file.write(str(self.peak_areas[k]))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("peakType "))
                    XES_Oasis_Fit_file.write(str(peakType))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("peakColor clOlive")) #Change this based on k
                    XES_Oasis_Fit_file.write(str(" \n"))

                elif(peakType.lower() == "double lorentzian"):
                    if len(self.params[k]) >= 6:
                        XES_Oasis_Fit_file.write(str("doublet"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str("soSplitting  "))
                        XES_Oasis_Fit_file.write(str(self.params[k][5]))
                        XES_Oasis_Fit_file.write(str(" free"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                        XES_Oasis_Fit_file.write(str("branchingRatio      "))
                        XES_Oasis_Fit_file.write(str("0.75")) #WE DO NOT HAVE A WAY OF OUTPUTTING THIS RIGHT NOW --> FIX THIS
                        XES_Oasis_Fit_file.write(str(" fix"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                    else:
                        XES_Oasis_Fit_file.write(str("singlet"))
                        XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("gauss   "))
                    gauss = self.params[k][1] * 2 * np.sqrt(2*np.log(2.0))
                    XES_Oasis_Fit_file.write(str(gauss))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("lorentzian      "))
                    XES_Oasis_Fit_file.write(str(self.params[k][2]))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("energy   "))
                    XES_Oasis_Fit_file.write(str(KE))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("asymmetry         "))
                    XES_Oasis_Fit_file.write(str(self.params[k][4]))
                    XES_Oasis_Fit_file.write(str("  limitUp    10 limitDown     1"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("asymmetryDoniach       0.1  limitUp     1 limitDown     0"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("area   "))
                    XES_Oasis_Fit_file.write(str(self.peak_areas[k]))
                    XES_Oasis_Fit_file.write(str(" free"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("peakType "))
                    XES_Oasis_Fit_file.write(str("DoubleLorentzian"))
                    XES_Oasis_Fit_file.write(str(" \n"))
                    XES_Oasis_Fit_file.write(str("peakColor clOlive")) #Change this based on k
                    XES_Oasis_Fit_file.write(str(" \n"))


            XES_Oasis_Fit_file.write(str("  endOfParameters"))
            XES_Oasis_Fit_file.write(str(" \n"))






            XES_Oasis_Fit_file.close()
            print("Fit saved to output file location")





        #Function for exporting peak parameters as LaTeX table:
        def export_peak_parameters():




            out_name = self.csv_generate_from.stem + "_" + "LaTeX_Table" + '.txt'

            os.chdir(pathlib.Path.cwd().parent)  # change the working directory from gui to nano-indent


            table_folder_path = pathlib.Path(self.folder_name)
            table_file = table_folder_path.joinpath(out_name)
            os.chdir(pathlib.Path.cwd().joinpath('gui'))

            #name_of_file = str("Output_table")

            #completeName = os.path.abspath(name_of_file+".txt")

            table_file = open(table_file, "w")

            #Header and peak rows
            headers = []
            PE_vals = []
            sigma_vals = []
            gamma_vals = []
            amp_vals = []
            area_vals = []
            fwhm_vals = []

            data = dict()
            headers.append("Peak \\#") #Error here for some reason. "invalid escape error"
            peak_range = len(self.params) - len(self.errors_bkgns) #To save first press "Plot Best Fit"
            for i in range(0, peak_range): #appending the values of each peak to each specified row in the table

                headers.append(str(i+1))
                peakType = self.params[i][-1] #Last element in array is the curve fit type

                if(peakType.lower() == "lorentzian"):
                    PE_vals.append(str(round(self.params[i][0],2)) + " \\textpm " +  str(self.errors[i][0]))
                    sigma_vals.append(" ")
                    gamma_vals.append(str(round(self.params[i][1],3)) + " \\textpm " +  str(self.errors[i][1]))
                    amp_vals.append(str(round(self.params[i][2],2)) + " \\textpm " +  str(self.errors[i][2]))
                    area_vals.append(str(round(self.peak_areas[i],2)) + " \\textpm " +  str(round(self.upper_error_area[i],3)))
                    fwhm_vals.append(str(round(self.FWHM_values[i],2)))
                elif(peakType.lower() == "gaussian"):
                    PE_vals.append(str(round(self.params[i][0],2)) + " \\textpm " +  str(self.errors[i][0]))
                    sigma_vals.append(str(round(self.params[i][1],3)) + " \\textpm " +  str(self.errors[i][1]))
                    gamma_vals.append(" ")
                    amp_vals.append(str(round(self.params[i][2],2)) + " \\textpm " +  str(self.errors[i][2]))
                    area_vals.append(str(round(self.peak_areas[i],2)) + " \\textpm " +  str(round(self.upper_error_area[i],3)))
                    fwhm_vals.append(str(round(self.FWHM_values[i],2)))
                else:
                    PE_vals.append(str(round(self.params[i][0],2)) + " \\textpm " +  str(self.errors[i][0]))
                    sigma_vals.append(str(round(self.params[i][1],3)) + " \\textpm " +  str(self.errors[i][1]))
                    gamma_vals.append(str(round(self.params[i][2],3)) + " \\textpm " +  str(self.errors[i][2]))
                    amp_vals.append(str(round(self.params[i][3],2)) + " \\textpm " +  str(self.errors[i][3]))
                    area_vals.append(str(round(self.peak_areas[i],2)) + " \\textpm " +  str(round(self.upper_error_area[i],3)))
                    fwhm_vals.append(str(round(self.FWHM_values[i],2)))




            data["PE"] = PE_vals
            data["Sigma"] = sigma_vals
            data["Gamma"] = gamma_vals
            data["Amp"] = amp_vals
            data["Area"] = area_vals
            data["FWHM"] = fwhm_vals


            textabular = f"{'c'*len(headers)}"
            texheader = " & ".join(headers) + "\\\\"
            texdata = "\\hline\n"
            for label in data:
                texdata += f"{label} & {' & '.join(map(str,data[label]))} \\\\\n"



            table_begin = str("\\begin{tabular}{"+textabular+"}")
            table_header = str(texheader)
            hline = str("\\hline\n")
            table_data = str(texdata)
            table_end = str("\\end{tabular}")
            table_file.write(table_begin)
            table_file.write(hline)
            table_file.write(hline)
            table_file.write(table_header)
            table_file.write(table_data)
            table_file.write(hline)
            table_file.write(hline)
            table_file.write(table_end)
            table_file.close()
            print("Fitting Parameters Saved as LaTeX Table")

        def updateExportDataRows(args):
            #self.num = int(self.number_of_peaks.get())
            self.num = 1
            #self.Peak_number = abs(self.peak_number)

            i=int(self.peak_number.get()-1)
            #voigt_for_peak_type = 'Voigt'
            #values = self.peak_types in self.peakTypes_entries[i] if you want multiple background types


            #for row in range(1,((4*int(self.peak_number.get()))+1),4): #4 because 4 paramters. add changes here to output more values



            peakType = self.params[i][-1] #Last element in array is the curve fit type
            

            if(peakType.lower() == "lorentzian"):
                PE_text = str(round(self.params[i][0],2)) + "  " + "+/-" + "  " + str(self.errors[i][0])
                self.PE_text = StringVar(value=PE_text)

                lorentzian_text = str(round(self.params[i][1],3)) + "  " + "+/-" + "  " + str(self.errors[i][1])
                self.lorentzian_text = StringVar(value=lorentzian_text)

                amp_text = str(round(self.params[i][2],2)) + "  " + "+/-" + "  " + str(self.errors[i][2])
                self.amp_text = StringVar(value=amp_text)

                area_text = str(round(self.peak_areas[i],2)) + "  " + "+/-" + "  " + str(round(self.upper_error_area[i],3))
                self.area_text = StringVar(value=area_text)

                FWHM_text = str(round(self.FWHM_values[i],2))
                self.FWHM_text = StringVar(value=FWHM_text)

                self.peak_energy_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.PE_text, font=self.entryFont)
                self.peak_energy_entries[i].grid(column=1, row=2, sticky=(W, E))

                self.sigma_entries[i] = ttk.Label(self.analysis_tab, textvariable="0", font=self.entryFont)
                self.sigma_entries[i].grid(column=1, row=3, sticky=(W, E))

                self.lorentzian_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.lorentzian_text, font=self.entryFont)
                self.lorentzian_entries[i].grid(column=1, row=4, sticky=(W, E))

                self.amp_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.amp_text, font=self.entryFont)
                self.amp_entries[i].grid(column=1, row=5, sticky=(W, E))

                self.area_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.area_text, font=self.entryFont)
                self.area_entries[i].grid(column=1, row=6, sticky=(W, E))

                self.FWHM_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.FWHM_text, font=self.entryFont)
                self.FWHM_entries[i].grid(column=1, row=7, sticky=(W, E))

            elif(peakType.lower() == "gaussian"):
                PE_text = str(round(self.params[i][0],2)) + "  " + "+/-" + "  " + str(self.errors[i][0])
                self.PE_text = StringVar(value=PE_text)

                sigma_text = str(round(self.params[i][1],3)) + "  " + "+/-" + "  " + str(self.errors[i][1])
                self.sigma_text = StringVar(value=sigma_text)

                amp_text = str(round(self.params[i][2],2)) + "  " + "+/-" + "  " + str(self.errors[i][2])
                self.amp_text = StringVar(value=amp_text)

                area_text = str(round(self.peak_areas[i],2)) + "  " + "+/-" + "  " + str(round(self.upper_error_area[i],3))
                self.area_text = StringVar(value=area_text)

                FWHM_text = str(round(self.FWHM_values[i],2))
                self.FWHM_text = StringVar(value=FWHM_text)

                self.peak_energy_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.PE_text, font=self.entryFont)
                self.peak_energy_entries[i].grid(column=1, row=2, sticky=(W, E))

                self.sigma_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.sigma_text, font=self.entryFont)
                self.sigma_entries[i].grid(column=1, row=3, sticky=(W, E))

                self.lorentzian_entries[i] = ttk.Label(self.analysis_tab, textvariable="0", font=self.entryFont)
                self.lorentzian_entries[i].grid(column=1, row=4, sticky=(W, E))

                self.amp_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.amp_text, font=self.entryFont)
                self.amp_entries[i].grid(column=1, row=5, sticky=(W, E))

                self.area_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.area_text, font=self.entryFont)
                self.area_entries[i].grid(column=1, row=6, sticky=(W, E))

                self.FWHM_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.FWHM_text, font=self.entryFont)
                self.FWHM_entries[i].grid(column=1, row=7, sticky=(W, E))
            else: #Voigt, Double-Lorentzian, Doniach-Sunjic --> Asymmetry values not being shown right now


                PE_text = str(round(self.params[i][0],2)) + "  " + "+/-" + "  " + str(self.errors[i][0])
                self.PE_text = StringVar(value=PE_text)

                sigma_text = str(round(self.params[i][1],3)) + "  " + "+/-" + "  " + str(self.errors[i][1])
                self.sigma_text = StringVar(value=sigma_text)

                lorentzian_text = str(round(self.params[i][2],3)) + "  " + "+/-" + "  " + str(self.errors[i][2])
                self.lorentzian_text = StringVar(value=lorentzian_text)

                amp_text = str(round(self.params[i][3],2)) + "  " + "+/-" + "  " + str(self.errors[i][3])
                self.amp_text = StringVar(value=amp_text)

                area_text = str(round(self.peak_areas[i],2)) + "  " + "+/-" + "  " + str(round(self.upper_error_area[i],3))
                self.area_text = StringVar(value=area_text)

                FWHM_text = str(round(self.FWHM_values[i],2))
                self.FWHM_text = StringVar(value=FWHM_text)

                self.peak_energy_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.PE_text, font=self.entryFont)
                self.peak_energy_entries[i].grid(column=1, row=2, sticky=(W, E))

                self.sigma_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.sigma_text, font=self.entryFont)
                self.sigma_entries[i].grid(column=1, row=3, sticky=(W, E))

                self.lorentzian_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.lorentzian_text, font=self.entryFont)
                self.lorentzian_entries[i].grid(column=1, row=4, sticky=(W, E))

                self.amp_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.amp_text, font=self.entryFont)
                self.amp_entries[i].grid(column=1, row=5, sticky=(W, E))

                self.area_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.area_text, font=self.entryFont)
                self.area_entries[i].grid(column=1, row=6, sticky=(W, E))

                self.FWHM_entries[i] = ttk.Label(self.analysis_tab, textvariable=self.FWHM_text, font=self.entryFont)
                self.FWHM_entries[i].grid(column=1, row=7, sticky=(W, E))


            #i += 1

            #print(peak_labels)
        '''
        def get_areas(self,dir,params):
            #dir = str(dir.get())
            self.xes_analysis = xes_analysis2.xes_analysis(dir,params)
            self.xes_analysis.extract_data(plot_err=False)
            totalArea, peakAreas = self.xes_analysis.analyze()
            print(totalArea)
        '''
        """
        TODO:
        read in output file and get the relevant values to put in the boxes
        """
        self.analysis_obj = Analysis_plot(self.analysis_tab)

        # analysis_chisqr = StringVar(self.analysis_tab, 0.0)
        # analysis_background = StringVar(self.analysis_tab, 0.0)

        # For now put in placeholders
        # Select Folder Button
        analysis_button = ttk.Button(self.analysis_tab, text="Select Folder",command=select_analysis_folder)  # Add command to export data
        analysis_button.grid(column=0, row=0, sticky=(W, E), padx=self.padx, pady=self.pady, columnspan=2)

        self.peak_number = DoubleVar(self.root, 1) #Changed from 0 to 1 --> works for 1 peak not multiple. Combobox goes away. I think this is being used after folder is selected instead of waiting for user selection
        peak_number_options = [1,2,3,4,5,6,7,8,9,10]
        peak_number_entry = ttk.Combobox(self.analysis_tab, textvariable=self.peak_number, font=self.entryFont,values= peak_number_options)
        peak_number_entry.grid(column=1, row=1, sticky=(W, E)) #on same row as background checkbox
        peak_number_entry.bind('<<ComboboxSelected>>', updateExportDataRows)



        peak_labels = "Peak"
        PE_labels = "Energy"
        sigma_labels = "Sigma"
        lorentzian_labels = "Gamma"
        amp_labels = "Amp"
        area_labels = "Area"
        FWHM_labels = "FWHM"
        self.num_peak_labels = ttk.Label(self.analysis_tab, text=peak_labels, font=self.labelFont)
        self.num_peak_labels.grid_configure(column=0, row=1, sticky=W, padx=self.padx, pady=self.pady)
        self.PE_labels = ttk.Label(self.analysis_tab, text=PE_labels, font=self.labelFont)
        self.PE_labels.grid_configure(column=0, row=2, sticky=W, padx=self.padx, pady=self.pady)
        self.sigma_labels = ttk.Label(self.analysis_tab, text=sigma_labels, font=self.labelFont)
        self.sigma_labels.grid_configure(column=0, row=3, sticky=W, padx=self.padx, pady=self.pady)
        self.lorentzian_labels = ttk.Label(self.analysis_tab, text=lorentzian_labels, font=self.labelFont)
        self.lorentzian_labels.grid_configure(column=0, row=4, sticky=W, padx=self.padx, pady=self.pady)
        self.amp_labels = ttk.Label(self.analysis_tab, text=amp_labels, font=self.labelFont)
        self.amp_labels.grid_configure(column=0, row=5, sticky=W, padx=self.padx, pady=self.pady)
        self.area_labels = ttk.Label(self.analysis_tab, text=area_labels, font=self.labelFont)
        self.area_labels.grid_configure(column=0, row=6, sticky=W, padx=self.padx, pady=self.pady)
        self.FWHM_labels = ttk.Label(self.analysis_tab, text=FWHM_labels, font=self.labelFont)
        self.FWHM_labels.grid_configure(column=0, row=7, sticky=W, padx=self.padx, pady=self.pady)




        # Entries___________________________________________________________________________________________
        # entry_chisqr_best = ttk.Label(self.analysis_tab, textvariable=analysis_chisqr, font=self.entryFont, borderwidth=2,
        #                           relief="groove", background='#a9a9a9')
        # entry_chisqr_best.grid(column=1, row=4, sticky=(W, E), padx=self.padx)

        # entry_background = ttk.Label(self.analysis_tab, textvariable=analysis_background, font=self.entryFont,borderwidth=2,
        #                               relief="groove", background='#a9a9a9')
        # entry_background.grid(column=1, row=5, sticky=(W, E), padx=self.padx)

        # Number of Peak to Find Row
        self.numPeaks = int(self.number_of_peaks.get())

        # Chisqr Entry
        # entry_chisqr_best = ttk.Label(self.analysis_tab, textvariable=analysis_chisqr, font=self.entryFont, borderwidth=2,
        #                           relief="groove", background='#a9a9a9')
        # entry_chisqr_best.grid(column=1, row=4, sticky=(W, E), padx=self.padx)

        # Plot Best Fit Button
        button_plot = ttk.Button(self.analysis_tab,text="Plot Best Fit",command=calculate_and_plot)  # Add command to plot data using postprocessing
        button_plot.grid(column=0, row=((4*self.numPeaks)+5), sticky=(W, E), padx=self.padx, pady=self.pady, columnspan=2)



        # Export Values Button

        button_export = ttk.Button(self.analysis_tab, text="Export Values to LaTeX Table", command = export_peak_parameters)  # Add command to export data
        button_export.grid(column=0, row=((4*self.numPeaks)+6), sticky=(W, E), padx=self.padx, pady=self.pady, columnspan=2)

        button_export_fit = ttk.Button(self.analysis_tab, text="Export Peak Fit", command = export_indi_peak_fit)  # Add command to export data
        button_export_fit.grid(column=0, row=((4*self.numPeaks)+7), sticky=(W, E), padx=self.padx, pady=self.pady, columnspan=2)

        self.analysis_tab.columnconfigure(3, weight=1)
        self.analysis_tab.rowconfigure(0, weight=1)
        self.analysis_tab.rowconfigure(1, weight=1)
        self.analysis_tab.rowconfigure(2, weight=1)
        self.analysis_tab.rowconfigure(3, weight=1)
        self.analysis_tab.rowconfigure(4, weight=1)
        self.analysis_tab.rowconfigure(5, weight=1)
        self.analysis_tab.rowconfigure(6, weight=1)
        self.analysis_tab.rowconfigure(7, weight=1)
        self.analysis_tab.rowconfigure(8, weight=1)
        self.analysis_tab.rowconfigure(9, weight=1)

    def stop_term(self):
        #print("In stop term")
        #print("PID TO KILL ", self.pid_list[len(self.pid_list)-1])
        #command = 'kill -9 ', self.pid_list[len(self.pid_list)-1]
        #os.killpg(self.pid_list[len(self.pid_list)-1], signal.SIGTERM)
        #subprocess.Popen(command)
        # print("/n/n/n/n/n/n/n/n/n/n"
        #       "**************"
        #       "*******************"
        #       "(++++&****************************"
        #       ""
        #       "/n/n/n/n/n/n")

        self.stop_not_pressed = False
        if not self.command_list.empty():
            self.stop_all()
        elif hasattr(self, 'proc'):
            self.proc.kill()
            self.proc.terminate()
            print("Stopped xes_neo")
            self.proc.kill()

    def on_closing(self):
        """
        on closing function
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_term()
            if hasattr(self, 'terminal'):
                self.root.quit()
                self.terminal.destroy()
            else:
                self.root.quit()

    def Run(self):
        """
        Run the code
        """
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.root.mainloop()


root = App()
root.Run()
