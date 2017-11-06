#!/usr/bin/env python


import os

class processTextFiles:

    absPathsList = []
    folderNameFilesDict = {}
    fodlerNameSameFileNamesDict = {}
    
    def getFolderNameFilesDict(self):
        return self.folderNameFilesDict

    def __init__(self):
        print('processTextFile initialized')

    #store the file in the class intern dict
    def storeFilePath(self, aFilePath):
        print('called storeFilePath')
        absPath = os.path.abspath(aFilePath)
        self.absPathsList.append(absPath)
        #print('Added List entry: ' + self.absPathsList[len(self.absPathsList)-1])
        
    def buildFileWithFolderNameDict(self):
        print('called  buildFileWithFolderNameDict')        
        #Loop through the absPathList
        for i in self.absPathsList:
            head, tail = os.path.split(i)
            folderName = os.path.basename(head)
            self.folderNameFilesDict[folderName]= i 
            #print('folder ' + folderName + ' contains the file: \n' + self.folderNameFilesDict[folderName] + '\n')
    
    def sortFolderNameFilesDict(self):
        for key in sorted(self.folderNameFilesDict):
            print "%s: %s" % (key, self.folderNameFilesDict[key])