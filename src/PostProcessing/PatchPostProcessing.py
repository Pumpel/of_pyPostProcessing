
from subprocess import check_output
import pickle
from io import StringIO
import pandas as pd


class PatchBase(object):
    
    def __init__(self):
        self.output = None
        self.fileName = None
        self.fieldName = None
        self.patchName = None
        
        
    
    def writeLogFile(self):
        with open('log.{}'.format(self.fileName), 'w') as f:
            f.write(self.output)
            
    """
    This method exctracts the scalar and vector values 
    from a string (utf-8 encoded), given by the output of a
    postProcess utility (foamVersion 4.0)
    """            
    @staticmethod
    def extractFieldValues(inputString=None, 
                           fieldName=None, 
                           patchName=None,
                           valueKeyWord=None):
        s = StringIO(inputString)
        resultsList = list()
        tmpDict = dict()
        time_switch = False
        for line in s:
            line = line.split()
            if len(line) > 2:
                if line[0] == "Time" and line[1] == "=":
                    time_switch = True
                    tmpDict["Field"] = fieldName
                    tmpDict["Patch"] = patchName
                    tmpDict["Time"] = line[2]                           #2 is the position of the time value in string line
                if line[0] == valueKeyWord:                             #get line with calculated values    
                    
                    if len(line) == 7:                                  #check if the line contains a vector
                        tmpDict["ValueType"] = "Vector"
                        x = line[4]                                     #Cleaning the vector values
                        x = x.replace("(", "")
                        y = line[5]
                        z = line[6]
                        z = z.replace(")", "")
                        tmpDict["x"] = x                                #Adding the field values to the dict
                        tmpDict["y"] = y
                        tmpDict["z"] = z
                        time_switch = False                             #All infos for one time step gathered, 
                                                                        #mark the dict as ready for the results list
                                                                        
                    if len(line) == 5:
                        tmpDict["ValueType"] = "Scalar"
                        val = line[4]
                        val = val.replace("(", "")
                        val = val.replace(")", "")
                        tmpDict["Value"] = val                  
                        time_switch = False                                                        
                                                                        
                if time_switch == False:                                #After finding the values for the field, append the dict to 
                                                                        #the final results list
                    if bool(tmpDict):
                        resultsList.append(tmpDict)
                        tmpDict = dict()                                #Instead of setting the dict to None, reassing a new dict. This way
                                                                        #The old dict is now owned by the resultsList and the new dict is empty
        return resultsList
    
    @staticmethod
    def constructDataFrame(resultsList):
        df = pd.DataFrame(resultsList)
        df["Time"] = pd.to_numeric(df["Time"])
        if df.iloc[0]["ValueType"] == "Vector":
            df["x"] = pd.to_numeric(df["x"])
            df["y"] = pd.to_numeric(df["y"])
            df["z"] = pd.to_numeric(df["z"])
        elif df.iloc[0]["ValueType"] == "Scalar":
            df["Value"] = pd.to_numeric(df["Value"])
        return df


class PatchAverage(PatchBase):
    
    operationName = "patchAverage"

    
    def __init__(self,fieldName=None, patchName=None):
        self.fieldName = fieldName
        self.patchName = patchName
        self.fileName  = "{}_{}_{}".format(PatchAverage.operationName, fieldName, patchName)
        # Keyword is used to find the line with the values in the log file
        self.valueKeyWord = "average({})".format(self.patchName)   
        
        self.calcPatchAverage()
        self.writeLogFile()
        self.resultsList        = PatchAverage.extractFieldValues(self.output, self.fieldName, self.patchName, self.valueKeyWord)
        self.resultsDataFrame   = PatchAverage.constructDataFrame(self.resultsList)
        
    
    def calcPatchAverage(self):
        self.output = check_output(["postProcess",  "-func", "patchAverage({},name={})".format(self.fieldName,self.patchName)])
        self.output = self.output.decode("utf-8")            
    
#     def writeLogFile(self):
#         with open('log.patchAverage_{}_{}'.format(self.fieldName, self.patchName), 'w') as f:
#             f.write(self.output)
        
        
    def pickleResultsList(self):
        try:
            pickle.dump(self.resultsList, open(self.fileName, "wb"))
        except:
            print("Could not pickle the resultsList.")
            
            

class PatchFlowRate(PatchBase):
    
    operationName = "patchFlowRate"
    
    def __init__(self, patchName=None):
        self.fieldName = None
        self.patchName = patchName
        self.fileName  = "{}_{}".format(PatchFlowRate.operationName, patchName)
        # Keyword is used to find the line with the values in the log file
        self.valueKeyWord = "sum({})".format(self.patchName)   
        
        self.calcPatchFlowRate()
        self.writeLogFile()
        self.resultsList        = PatchAverage.extractFieldValues(self.output, self.fieldName, self.patchName, self.valueKeyWord)
        self.resultsDataFrame   = PatchAverage.constructDataFrame(self.resultsList)
        

    def calcPatchFlowRate(self):
        self.output = check_output(["postProcess",  "-func", "flowRatePatch(name={})".format(self.patchName)])
        self.output = self.output.decode("utf-8")   



class PatchMagnitude(PatchBase):
    
    operationName = "patchMagnitude"
    
    def __init__(self, fieldName=None, patchName=None):
        self.fieldName = fieldName
        self.patchName = patchName
        self.fileName  = "{}_{}_{}".format(PatchMagnitude.operationName, fieldName, patchName)
        self.calcMagnitude()
        self.writeLogFile()
        
    def calcMagnitude(self):
        self.output = check_output(["postProcess",  "-func", "mag({})".format(self.fieldName)])
        self.output = self.output.decode("utf-8")            
        self.writeLogFile()
            
            
if __name__ == "__main__":
    import os
    os.chdir("/media/timo/linuxSimData/Cavitation/compMultiphaseCavitation_validation/Branches/Features/AcousticCourantNo/RouseMcNown_bluntHead_2D_grid5/parameterStudy_001/bluntHead_2Dgrid4_komega_kunz_myWave_sim003")
    #patchFlowRate = PatchFlowRate("Inlet")
    patchavg = PatchAverage("p", "Inlet")
    