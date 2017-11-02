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

from PostProcessing.Utilities import PostProcessingUtilities as PPUtils

class PPFile(object):
    
    def __init__(self, _fPath):
        if isinstance(_fPath, Path) is False:
            _path = Path(_fPath)
            
        self.filePath = _path.resolve()
        self.fileName = _path.name


class PPLineFile(PPFile):
    
    def __init__(self, _fPath, _fieldName, _fieldDim, _timeStep, _fieldDirPath):
        PPFile.__init__(self, _fPath)
        self.fieldName = _fieldName
        self.fieldDim = _fieldDim
        self.timeStep = _timeStep
        self.fieldDirPath = _fieldDirPath
            
    
            

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
    
    @staticmethod
    def makeAbsPathsInList(_list):  
        _absDirs = []
        for _dir in _list:
            _absDirs.append(path.abspath(_dir))
        return _absDirs
    
    @staticmethod
    def getValidSolutionDirectory(_caseDir):
        if path.isdir(path.abspath(_caseDir)) is True:
            sol=SolutionDirectory(_caseDir)
            if sol.isValid():
                return sol
            
    def getFieldFiles(self, _fieldDir):
        _fieldDirPath = path.join(self.postProcessingDir, _fieldDir)
        _fieldName = Path(_fieldDir).name
        _fieldName = PPUtils.getFieldNameFromString(_fieldName)
        _fieldDim  = PPUtils.getDimensionOfField(_fieldName)
        
        _list = []
        for root, subFolders, files in os.walk(_fieldDirPath):
            for aFile in files:
                absFilePath = os.path.join(root,aFile)
                _timeStep = Path(root).name
                _list.append(PPLineFile(absFilePath, 
                                        _fieldName,
                                        _fieldDim,
                                        _timeStep, 
                                        _fieldDirPath))
        return _list
        
    def run(self):
        _argDirs=self.parser.getArgs()
        
        if len(_argDirs)==0:
            _argDirs=[path.curdir]
        
        #Build list with abs paths of all given case dirs
        _absArgDirs = PlotLine.makeAbsPathsInList(_argDirs)
        
        #Iterate through all folder given as an argument
        for _dir in _absArgDirs:
            print("\n\nWorking on Case: \n {} \n".format(_dir))
            sol = PlotLine.getValidSolutionDirectory(_dir)
            
            os.chdir(sol.name)
            self.postProcessingDir = path.join(sol.name, "postProcessing")
            self.plotDir = path.join(self.postProcessingDir, "plots")
            #Exit if the folder for plotting exists
            if path.exists(self.plotDir) is False:
                os.mkdir(path.join(self.postProcessingDir, "plots"))
            else:
                print("Folder with plots already exists. Remove the folder before executing.")
                exit()
    
            # Iterate the folders for the fields in postProcessing
            #dirIter = tqdm(fieldDirs, unit='Dirs', desc='Dirs')
            fieldDirs = os.listdir(self.postProcessingDir)
            for fieldDir in fieldDirs:
                #Ignore files found in the /postProcessing directory
                if path.isdir(path.join(self.postProcessingDir, fieldDir)) is False:
                    continue

                print("\n Reading field: {}".format(fieldDir))
                os.chdir(self.plotDir)
                os.mkdir(fieldDir)
                os.chdir(fieldDir)
                
                fieldFiles = self.getFieldFiles(fieldDir)
                #Finding the maximum and minium values of the field for all time steps
                plotFieldFilesIter = tqdm(fieldFiles,unit=" Files")   
                ymaxList = []
                yminList = []
                for _file in plotFieldFilesIter:
                    try:
                        pd1 = pd.read_csv(_file.filePath, delimiter=' ', header=None)
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
                    plotFieldFilesIter.close()
                except:
                    ymax = 0
                    ymin = 0
                    print("Caught exception, ymax is: {}".format(ymax))
                    print("Caught exception, ymin is: {}".format(ymin))

                
                print("\n Plotting field: {}".format(Path(fieldDir).name))
                # Iterate through the files of one field
                plotFieldFilesIter = tqdm(fieldFiles, unit=" Files")   
                for _file in plotFieldFilesIter:
                    _fileName = "{}_{}".format(_file.timeStep,_file.fieldName)
                    _filePath = path.join(self.plotDir, fieldDir)
                    _figurePath = path.join(_filePath, _fileName)
                     
                    
                    try:
                        pd1 = pd.read_csv(_file.filePath, delimiter=' ', header=None)
                        my_data = pd1
                        myArray = np.array(my_data)
                        x,y = self.getXYValues(myArray)    
                                                
                        #Plotting commands
                        theLabel = '{} [{}]'.format(_file.fieldName,_file.fieldDim)
                        simName = path.basename(sol.name)
                        theTitle = "{} - Field: {} of Sim: {}".format(_file.timeStep, _file.fieldName, simName)
                        plt.plot(x,y, color='black', linestyle='solid', label=theLabel)
                        plt.title(theTitle)
                        axes = plt.gca()
                        axes.set_ylim([ymin,ymax])
                        plt.legend()
                        plt.savefig("{}.png".format(_figurePath))
                        plt.close()
                        pd1 = None
                    except:
                        print("\n Couldnt read the csv file for field {} \n".format(_file.fieldName))
                plotFieldFilesIter.close()
            
            
        
        
        
        
           

            
        
        
        

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

    
    