
import os
from os import getcwd,chdir,path
import pathlib 
from pathlib import Path

from PyFoam.Applications.PyFoamApplication import PyFoamApplication
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.ThirdParty.tqdm import tqdm

from PostProcessing.PostPUtilities import PostPUtilities as PPUtils

import pandas as pd


class PostPCaseResultsCSV(PyFoamApplication):
    
    def __init__(self, *args, **kwargs):
        
        description="""
        Checks for valid OpenFOAM cases in the given working directory. The result.csv files
        are then concatenated (if present) and saved in the working directory as results_concat.csv
        """
        
        PyFoamApplication.__init__(self,
                                   args=args,
                                   description=description,
                                   usage="%prog [<directories>]",
                                   interspersed=True,
                                   changeVersion=False,
                                   nr=0,
                                   exactNr=False,
                                   **kwargs)
        
    def run(self):
        _argDirs=self.parser.getArgs()
        
        if len(_argDirs)==0:
            _argDirs=[path.curdir]
        
        #Build list with abs paths of all given case dirs
        _absArgDirs = PPUtils.makeAbsPathsInList(_argDirs)
        
        #Change to given working directory
        os.chdir(_absArgDirs[0])
        
        #Directories in the cwd
        _dirList = os.listdir(_absArgDirs[0])
        _dirList = PPUtils.makeAbsPathsInList(_dirList)

        filesDict = dict()
        for root, subFolders, files in os.walk(getcwd()):
            for f in files:
                file = os.path.join(root, f)
                file = Path(file)
                if file.name == "results.csv":
                    filesDict[file.parent.name] = file.absolute()
        
        #Importing the paramters from the csv file
        dataFrame = pd.read_csv('measuredData.csv', header=0)
        dataFrame.drop(0, axis=0, inplace=True)
        dataFrame.drop(list(range(4,25,1)), axis=0, inplace=True)
    
        pdFrames = list()
        for simName, csvFile in filesDict.items():
            #df with avgMagTau values
            frame = pd.read_csv(csvFile)
            #df with simName, so he values can be traced to the respective
            #simlations
            string = simName.split('_')
            f = pd.DataFrame({'SimName' : [simName], 'Measurement' : [int(string[3])]})
            
            #Concat data and simulation identifying simName df
            df = pd.concat([frame, f], axis=1)
            #List of df for all sims
            pdFrames.append(df)
            
    
        resultDFrame = pd.concat(pdFrames)
        resultDFrame.sort_values(by=['Measurement'], ascending=True, inplace=True)
        print()
        print(resultDFrame)
        resultDFrame.to_csv(os.path.join(getcwd(), "resultsFinal.csv"))
        
        
if __name__ == "__main__":
    #NoTwo(['Thats an arg right here'])
    # Debuging
    PostPCaseResultsCSV("/media/timo/linuxSimData/NonNewtonian/cp501/cp501_wedgegrid003_XPP-SE_validationStudy")

    
    