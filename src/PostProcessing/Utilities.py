from et_xmlfile.tests.common_imports import _str

class PostProcessingUtilities(object):

    fieldNamesList = ['p','p_rgh','U','rho','alpha',
                      'rhoPhi', 'phi', 'T', 'T.vapor', 
                      'T.water', 'T.air', 'alphaSum_',
                      'alphaSum',
                      'alphas', 'alphat', 'dgdt.vapor',
                      'dgdt.water', 'dgdt.air',
                      'alpha.water', 'alpha.vapor',
                      'alpha.air', 'k', 'omega','epsilon',
                      'nut', 'yPlus']
    
    fieldDimesionsDict = {'p': 'Pa', 'p_rgh': 'Pa', 'U': 'm/s',
                          'rho': 'kg/m^3', 'T': 'K', 'alpha': '-'}

    def __init__(self, 
                 params, 
                 **kwargs):
        ''' This class provides utilies for the 
        post processing apps in OpenFOAM cases'''
    
    @staticmethod
    def getFieldNameFromString(_string):       
        name = []
        for fieldName in PostProcessingUtilities.fieldNamesList:
            if fieldName in _string:
                name.append(fieldName)
#             elif fieldName == _string:
#                name.append(fieldName)
        if len(name) is 0:
            return 'Could not find a valid field name in the given String'
        
        # The field 'p' results in an ambigious search pattern. Removing
        # The 'p' field when appropiate below:
        if 'p' in name and len(name) > 1:
            for i in name:
                if i != 'p':
                    name = [i]
        # When plotting vector data, the magnitude of the vector is plotted
        if 'U' in name and len(name) == 1:
            name=["mag_U"]

        return name[0]
    
    @staticmethod
    def getDimensionOfField(_field):
        name = {}
        for key, value in PostProcessingUtilities.fieldDimesionsDict.items():
            if key in _field:
                name[key] = value
        if len(name) is 0:
            return 'Could not find a valid field name in the given String'
        
        if len(name.keys()) > 1:
            for key, value in name.items():
                if key != 'p':
                    return value
        else:
            for value in name.values():
                return value
