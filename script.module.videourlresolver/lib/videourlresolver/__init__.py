import os

#check if running in XBMC
try:
    import xbmc
except:
    __xbmc__ = False
else:    
    __xbmc__ = True

#Note: will these values be accessible from other .py files? They need to be.

__xbmcmodulename__ = 'script.module.videoresolver'
__modulename__ = 'videoresolver'
__datadirname__ = 'videoresolver_files' # only used when not running in xbmc
__wkdir__ = os.getcwd()


"""
Get path to where we store the files eg. cookies
When running in XBMC, use addon_data folder.
When not running in XBMC stores files in a dir in the parent directory of videoresolver
 """

if __xbmc__ == False:
    files_path = os.path.join(os.path.dirname(__wkdir__),__datadirname__)
    
    try:
        if not os.path.exists(files_path):
            os.makedirs(files_path)
    except:
        #need to put our own proper error here, not use a print
        print "could not create data directory!"        

    else:
        __filespath__ = files_path
        
if __xbmc__ == True:

    files_path = xbmc.translatePath('special://profile/addon_data/'+__xbmcmodulename__)
            
    #to avoid any errors, create the directory, as xbmc doesn't always do this.           
    try:
        if not os.path.exists(files_path):
            os.makedirs(files_path)
    except:
        #need to put our own proper error here, not use a print
        print "could not create data directory!"        

    else:
        __filespath__ = files_path
