# XES_Neo
#### Versions: 0.0.16
#### Last update: April, 10, 2025 #Constant updates
#### LANL O#: O4887

This program utilizes a genetic algorithm in fitting of XES data

## Pre-requisites
Usage of this software is highly recommend to use `anaconda` or `pip` package managers.

  - Python: => 3.9
  - Numpy: => 1.20
  - Scipy: => 1.6
  - Matplotlib: > 3.0
  - Numba: => 0.60

It is highly recommend to create a new environment in `anaconda` to prevent packages conflicts.

        conda create --name xes_neo python>=3.8
        conda activate xes_neo


## Installations
To install XES_Neo, simply clone the repo:

        git clone https://github.com/lanl/XES_Neo_Public.git 
        cd xes
        pip install .


## Usage
To run a sample test, make sure the environment is set correctly, and select a input file:

        xes_neo -i test/test.ini

## Update
XES Neo is under active development, to update the code after pulling from the repository:

        git pull
        pip install .
## GUI

We also have provided a GUI for use in additions to our program, with additional helper script to facilitate post-analysis. To use the GUI:

        cd gui
        python xes_neo_gui.py

The GUI allows for custom parameters for different indentator during the post-analysis process.

## Potential Errors
If you get an error message involving psutl, make sure you are in the right conda environment and install psutil

        conda activate xps_neo
        conda install psutl

## Citation:

TBA

## License:

This program is Open-Source under the BSD-3 License.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

	Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

	Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

	Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
