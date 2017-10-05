import os
from os import path
from PyFoam.Applications.PyFoamApplication import PyFoamApplication
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.ThirdParty.tqdm import tqdm

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import shutil
from pathlib import Path
import numpy as np

from PostProcessing.Utilities import PostProcessingUtilities as postUtils


class PlotLine(PyFoamApplication):
 
    def __init__(self, 
                 args=None, 
                 **kwargs):

            description="""
            Some description needed
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
            
            
    @staticmethod
    def getXYValues(_npArray):
        if len(_npArray[1,:]) == 2:
            x = _npArray[:,0]
            y = _npArray[:,1]
            return x,y
        elif len(_npArray[1,:]) == 4:
            i = 1
            y = np.array(_npArray[:,0])*0
            while i < 4:
                y += _npArray[:,i]**2
                y = np.sqrt(y)
                i += 1
            x = _npArray[:,0]
            return x,y
        else:
            x,y = None,None
            return x,y
        
        
    
        
    def run(self):
        _dirs=self.parser.getArgs()
        
        if len(_dirs)==0:
            _dirs=[path.curdir]
            
        absDirs = []
        for _dir in _dirs:
            absDirs.append(path.abspath(_dir))
        
        #Iterate through all folder given as an argument
        for _dir in absDirs:
            print("\n\nWorking on Case: \n {} \n".format(_dir))
            # Checks wheter the given path is a valid Foam case
            if path.isdir(path.abspath(_dir)) is True:
                sol=SolutionDirectory(_dir)
                if sol.isValid():
                    self.sol = sol
                    os.chdir(os.path.abspath(_dir))
        
            self.postProcessingDir = path.join(self.sol.name, "postProcessing")
            fieldDirs = os.listdir(self.postProcessingDir)
            
            if path.exists(path.join(self.postProcessingDir, "plots")) is False:
                os.mkdir(path.join(self.postProcessingDir, "plots"))
            else:
                print("Folder with plots already exists. Remove the folder before executing.")
                exit()
           
            self.plotDir = path.join(self.postProcessingDir, "plots")
    
    
            # Iterate the folders for the fields in postProcessing
            #dirIter = tqdm(fieldDirs, unit='Dirs', desc='Dirs')
            for fieldDir in fieldDirs:
                
                fieldDirPath = path.join(self.postProcessingDir, fieldDir)
                if path.isdir(fieldDirPath) is False:
                    continue
    
                _fieldName = Path(fieldDir).name
                _fieldName= postUtils.getFieldNameFromString(_fieldName)
                _fieldDim = postUtils.getDimensionOfField(_fieldName)
                print("\n Reading field: {}".format(_fieldName))
    
                os.chdir(self.plotDir)
                os.mkdir(fieldDir)
                os.chdir(fieldDir)
                
                _dict = {}
                for root, subFolders, files in os.walk(fieldDirPath):
                    for aFile in files:
                        absFilePath = os.path.join(root,aFile)
                        _dict[root]=absFilePath
                
                    
                #Finding the maximum and minium values of the field for all time steps
                plotFieldsIter = tqdm(_dict.items(),unit=" Files")   
                ymaxList = []
                yminList = []
                for key, value in plotFieldsIter:
                    try:
                        pd1 = pd.read_csv(value, delimiter=' ', header=None)
                        myArray = np.array(pd1)
                        x,y = self.getXYValues(myArray)
                        ymaxList.append(np.max(y))
                        yminList.append(np.min(y))
                    except:
                        pass            
                try:
                    ymax = np.max(ymaxList)*1.1
                    ymin = np.min(yminList)*0.9
                    if ymax == ymin:
                        ymax += 1
                        ymin -= 1
                    plotFieldsIter.close()
                except:
                    print("Caught exception, ymax is: {}".format(ymax))
                    print("Caught exception, ymin is: {}".format(ymin))
                    ymax = 0
                    ymin = 0
                
                print("\n Plotting field: {}".format(_fieldName))
                # Iterate through the files of one field
                plotFieldsIter = tqdm(_dict.items(),unit=" Files")   
                for key, value in plotFieldsIter:
                    _root = key
                    _absFilePath = value
                     
                    _timestep = Path(key).name
                    
     
                    _fileName = "{}_{}".format(_timestep,_fieldName)
                    _filePath = path.join(self.plotDir, Path(key).parent.name)
                    _figurePath = path.join(_filePath, _fileName)
                     
                    
                    try:
                        pd1 = pd.read_csv(value, delimiter=' ', header=None)
                        my_data = pd1
                        myArray = np.array(my_data)
                        x,y = self.getXYValues(myArray)    
                                                
                        #Plotting commands
                        theLabel = '{} [{}]'.format(_fieldName,_fieldDim)
                        simName = path.basename(sol.name)
                        theTitle = "{} - Field {} of Sim: {}".format(_timestep, _fieldName, simName)
                        plt.plot(x,y, color='black', linestyle='solid', label=theLabel)
                        plt.title(theTitle)
                        axes = plt.gca()
                        axes.set_ylim([ymin,ymax])
                        plt.legend()
                        plt.savefig("{}.png".format(_figurePath))
                        plt.close()
                        pd1 = _filePath
                    except:
                        print("\n Couldnt read the csv file for field {} \n".format(_fieldName))
                plotFieldsIter.close()
            
            
        
        
        
        
           

            
        
        
        

if __name__ == '__main__':
    #NoTwo(['Thats an arg right here'])
    try:
        shutil.rmtree("/media/timo/linuxSimData/compMultiphaseCavitation_validation/standardSolverCoarseTests_template/step_coarse_kunz/postProcessing/plots")
    except:
        pass
    # Debuging
    PlotLine(["/media/timo/linuxSimData/compMultiphaseCavitation_validation/standardSolverCoarseTests_template/step_coarse_kunz"])

    # IRL Testing
    try:
        shutil.rmtree("/media/timo/linuxSimData/compMultiphaseCavitation_validation/Branches/master/kunz_ParameterStudy/kunz_CcCv_130.0/plots")
    except:
        pass
    #PlotLine(["/media/timo/linuxSimData/compMultiphaseCavitation_validation/Branches/master/kunz_ParameterStudy/kunz_CcCv_130.0/"])

    
    