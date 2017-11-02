'''
Created on Nov 2, 2017

@author: timo
'''
import os
from pathlib import Path
import pandas as pd

if __name__ == '__main__':
    
    os.chdir("/media/timo/linuxSimData/NonNewtonian/cp501/cp501_wedgegrid003_XPP-SE_validationStudy")
    cwd = os.getcwd()
    print("PWD: ")
    print(cwd)
    
    filesDict = dict()
    for root, subFolders, files in os.walk(cwd):
        for f in files:
            file = os.path.join(root, f)
            file = Path(file)
            if file.name == "avgMagTau.csv":
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
    resultDFrame.to_csv(os.path.join(cwd, "simulationResults.csv"))