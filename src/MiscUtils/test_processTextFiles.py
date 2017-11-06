#!/usr/bin/env python


import os
import processTextFiles


class test_processTextFiles:

    cwd = None
    oldCwd = None


    def __init__(self, cwd):
        #setting current working directory
        if os.path.exists(cwd):
            self.oldCwd = cwd
            self.cwd = os.path.abspath(cwd)
            os.chdir(self.cwd)
            #print('oldCwd = ' + self.oldCwd)
            #print('cwd    = ' + self.cwd)
    
    
    def testProcessTestFiles(self):
        #os.walk() : iterates through all the folders of root and lists for each folder the subfolders and files.
        procTFile = processTextFiles.processTextFiles()
        
        
        for root, subFolders, files in os.walk(self.cwd):
            for aFile in files:
                #print('root = ' + root)
                #print('fileName = ' + file)
                absFilePath = os.path.join(root,aFile)
                #print('absFilePath = ' + absFilePath)
                
                #Testing
                procTFile.storeFilePath(absFilePath)
                
        #Testing 
        procTFile.buildFileWithFolderNameDict()
        procTFile.sortFolderNameFilesDict()
                
           
           
           
if __name__ == '__main__':
    cwd = '/home/timo/OpenFOAM/timo-4.0/developer/solver_validation_templates/6interphaseChangeFoam/orig_standard_pitzDaily_minus10meterpersecond/postProcessing/singleGraph'
    test = test_processTextFiles(cwd)
    test.testProcessTestFiles()
