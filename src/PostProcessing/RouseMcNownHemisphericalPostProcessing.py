

import os
from os import getcwd, chdir, mkdir
from pathlib import Path
import subprocess


import numpy as np
import pandas as pd

class Probes(object):
    
    def __init__(self, filePath):
        self.path = Path(filePath)
        
    def getLines(self):
        lines = list()
        with open(self.path, 'r') as f:
            for line in f:
                splitted = line.split(' ')
                lines.append(splitted)
        return lines
    
    def run(self):
        lines = self.getLines()
        print(lines[:])
                
def setUpEnvVariables():
    subprocess.call("cd ${0%/*} || exit 1", shell=True)
    subprocess.call(". $WM_PROJECT_DIR/bin/tools/RunFunctions", shell=True)

def runPostProcessYPlus():
    subprocess.call("postProcess -func 'yPlus'", shell=True)
    
def runPostProcessCoNumber():
    subprocess.call("postProcess -func 'CoNumber'", shell=True)
    
def runPostProcessProbes():
    subprocess.call("postProcess -func 'probes'", shell=True)
    
    




















if __name__ == "__main__":
    
    testCWD = "/media/timo/linuxSimData/Cavitation/compMultiphaseCavitation_validation/templates/hemisphericalHead_templates/WorkingSet/hemisphericalHead_2D_grid8_2_3_corrDCell_totalpmyWave_sim008/"
    chdir(testCWD)
    #setUpEnvVariables()
    #runPostProcessCoNumber()
    #runPostProcessProbes()
    postProcess_p_path = os.path.join(testCWD, "postProcessing/probes/0.000000/p")
    print(postProcess_p_path)
    prob = Probes(postProcess_p_path)
    prob.run()
    
    
    
    
    

