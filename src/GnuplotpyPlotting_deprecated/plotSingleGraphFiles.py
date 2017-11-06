#!/usr/bin/env python



import os
from subprocess import Popen, PIPE #for calling gnuplot
from numpy import *
#using the gnuplot package to
#import Gnuplot, Gnuplot.funcutils
import time
import gnuplot_kernel

#import processTextFiles

######
#Assumes to be executed from the postPorcessing directory
######

class plottingWithGnuPlot:
    
    cwd = None
    #Using custom class to store the text files for plotting
    procTFile = None
    

    def __init__(self, cwd):
        print('plottingWithGnuPlot initialized')
        #setting current working directory
        if os.path.exists(cwd):
            self.cwd = os.path.abspath(cwd)
            os.chdir(self.cwd)
            #print('oldCwd = ' + self.oldCwd)
            #print('cwd    = ' + self.cwd)
        #self.procTFile = processTextFiles.processTextFiles()
    
    def demo(self):
        """Demonstrate the Gnuplot package."""
    
        # A straightforward use of gnuplot.  The `debug=1' switch is used
        # in these examples so that the commands that are sent to gnuplot
        # are also output on stderr.
        g = Gnuplot.Gnuplot(debug=1)
        g.title('A simple example') # (optional)
        g('set data style linespoints') # give gnuplot an arbitrary command
        # PostProcessing a list of (x, y) pairs (tuples or a numpy array would
        # also be OK):
        g.plot([[0,1.1], [1,5.8], [2,3.3], [3,4.2]])
        raw_input('Please press return to continue...\n')
    
        g.reset()
        # PostProcessing one dataset from an array and one via a gnuplot function;
        # also demonstrate the use of item-specific options:
        x = arange(10, dtype='float_')
        y1 = x**2
        # Notice how this plotitem is created here but used later?  This
        # is convenient if the same dataset has to be plotted multiple
        # times.  It is also more efficient because the data need only be
        # written to a temporary file once.
        d = Gnuplot.Data(x, y1,
                         title='calculated by python',
                         with_='points 3 3')
        g.title('Data can be computed by python or gnuplot')
        g.xlabel('x')
        g.ylabel('x squared')
        # PostProcessing a function alongside the Data PlotItem defined above:
        g.plot(Gnuplot.Func('x**2', title='calculated by gnuplot'), d)
        raw_input('Please press return to continue...\n')
    
        # Save what we just plotted as a color postscript file.
    
        # With the enhanced postscript option, it is possible to show `x
        # squared' with a superscript (plus much, much more; see `help set
        # term postscript' in the gnuplot docs).  If your gnuplot doesn't
        # support enhanced mode, set `enhanced=0' below.
        g.ylabel('x^2') # take advantage of enhanced postscript mode
        g.hardcopy('gp_test.ps', enhanced=1, color=1)
        print ('\n******** Saved plot to postscript file "gp_test.ps" ********\n')
        raw_input('Please press return to continue...\n')
    
        g.reset()
        # Demonstrate a 3-d plot:
        # set up x and y values at which the function will be tabulated:
        x = arange(35)/2.0
        y = arange(30)/10.0 - 1.5
        # Make a 2-d array containing a function of x and y.  First create
        # xm and ym which contain the x and y values in a matrix form that
        # can be `broadcast' into a matrix of the appropriate shape:
        xm = x[:,newaxis]
        ym = y[newaxis,:]
        m = (sin(xm) + 0.1*xm) - ym**2
        g('set parametric')
        g('set data style lines')
        g('set hidden')
        g('set contour base')
        g.title('An example of a surface plot')
        g.xlabel('x')
        g.ylabel('y')
        # The `binary=1' option would cause communication with gnuplot to
        # be in binary format, which is considerably faster and uses less
        # disk space.  (This only works with the splot command due to
        # limitations of gnuplot.)  `binary=1' is the default, but here we
        # disable binary because older versions of gnuplot don't allow
        # binary data.  Change this to `binary=1' (or omit the binary
        # option) to get the advantage of binary format.
        g.splot(Gnuplot.GridData(m,x,y, binary=0))
        raw_input('Please press return to continue...\n')
    
        # plot another function, but letting GridFunc tabulate its values
        # automatically.  f could also be a lambda or a global function:
        def f(x,y):
            return 1.0 / (1 + 0.01 * x**2 + 0.5 * y**2)
    
        g.splot(Gnuplot.funcutils.compute_GridData(x,y, f, binary=0))
        raw_input('Please press return to continue...\n')
    
        # Explicit delete shouldn't be necessary, but if you are having
        # trouble with temporary files being left behind, try uncommenting
        # the following:
        #del g, d
    
    
    #function that extracts the absolute path of the files from the singleGraph directory and returns them in a list
    def plotSingleGraphFiles(self):
        print('printSingleGraphs called')
        absPath = os.path.abspath('.')
        singleGraphPath = os.path.join(absPath + '/singleGraph')
    
        #make directory for plots
        if os.path.exists(absPath + "/plots_singleGraph") is False:
            os.mkdir( absPath + "/plots_singleGraph", mode=0o755 )
            
        printingPath = absPath + "/plots_singleGraph"
    
        #store old working directory and go to the new for plotting
        oldCWD = os.getcwd()
        print(oldCWD)
        os.chdir(printingPath)
        cwd = os.getcwd()
        print(cwd)
        
        #os.walk() : iterates through all the folders of root and lists for each folder the subfolders and files.
        for root, subFolders, files in os.walk(singleGraphPath):
            for aFile in files:
                #print('root = ' + root)
                #print('fileName = ' + file)
                absFilePath = os.path.join(root,aFile)
                #print('absFilePath = ' + absFilePath)
                #self.plotFile(cwd, absFilePath)
                #head, tail = os.path.split(absFilePath)
                #folderName = os.path.basename(head)
                self.procTFile.storeFilePath(absFilePath)
                
                
        #building a dict with all files and their folders to plot
        self.procTFile.buildFileWithFolderNameDict()
        #print (self.procTFile.folderNameFilesDict)

        #Give sorted dict entries
        for key in sorted(self.procTFile.folderNameFilesDict):
            print("{}: {}").format(key, self.procTFile.folderNameFilesDict[key])
            print("cwd: {}").format(cwd)
            self.plotFile(cwd, self.procTFile.folderNameFilesDict[key])
       
        #
        #Going back to the initial cwd after printing
        os.chdir(oldCWD)
        
                            
    
    #function that will print the files given by the list and store them by name in the specified printPath dir
    def plotFile(self, cwd, absFilePath):
        #print('plotFile called')
        #print printFile
        # A straightforward use of gnuplot.  The `debug=1' switch is used
        # in these examples so that the commands that are sent to gnuplot
        # are also output on stderr.
        g = Gnuplot.Gnuplot(debug=0)    
    
        ##get the folder of the file to use it as prefix.
        ##get the name of the file
        #head = absolute path to folder
        #tail = name of file
        head, tail = os.path.split(absFilePath)
        folderName = os.path.basename(head)
    
        #Setting plotting options
        g('set parametric')
        g('set style data linespoints ')
        g('set hidden')
        g('set contour base')
        plotTitle = 'Vaporfractoin after the edge for time step ' + folderName
        g.title(plotTitle)
        g.xlabel('x in mm')
        g.ylabel('vapor fraction')
        #plotting and writing as svg
        databuff = Gnuplot.File(absFilePath, using='1:2',with_='line', title="alpha.water")
        #g.plot("'" + absFilePath + "'" + " alpah_water ")
        g.plot(databuff)
        g.hardcopy(folderName + "_" + tail + '.svg', terminal='svg', enhanced=1)
        
        
    #function that will print the files given by the list and store them by name in the specified printPath dir
    def plotDictWithFiles(self, cwd, absFilePath):
        #print('plotFile called')
        #print printFile
        # A straightforward use of gnuplot.  The `debug=1' switch is used
        # in these examples so that the commands that are sent to gnuplot
        # are also output on stderr.
        g = Gnuplot.Gnuplot(debug=0)    
    
        ##get the folder of the file to use it as prefix.
        ##get the name of the file
        #head = absolute path to folder
        #tail = name of file
        head, tail = os.path.split(absFilePath)
        folderName = os.path.basename(head)
    
        #Setting plotting options
        g('set parametric')
        g('set style data linespoints ')
        g('set hidden')
        g('set contour base')
        plotTitle = 'Vaporfractoin after the edge for time step ' + folderName
        g.title(plotTitle)
        g.xlabel('x in mm')
        g.ylabel('vapor fraction')
        #plotting and writing as svg
        databuff = Gnuplot.File(absFilePath, using='1:2',with_='line', title="alpha.water")
        #g.plot("'" + absFilePath + "'" + " alpah_water ")
        g.plot(databuff)
        g.hardcopy(folderName + "_" + tail + '.svg', terminal='svg', enhanced=1)       




if __name__ == '__main__':
    cwd = '/media/timo/linuxSimData/compMultiphaseCavitation_validation/standardSolverCoarseTests_template/step_coarse_kunz/postProcessing'
    plotter = plottingWithGnuPlot(cwd)
    plotter.plotSingleGraphFiles()
    #demo()
 
