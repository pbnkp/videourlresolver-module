'''
The API that users use to control videourlresolver.
Handles all other resolvers,
as long as they conform to specification (see readme)

You do not even need to edit this file to add your resolver.
'''


import os
import sys


#check if running in XBMC
try:     import xbmc
except:  __xbmc__ = False
else:    __xbmc__ = True

__modulename__ = 'videourlresolver'
__xbmcmodulename__ = 'script.module.' + __modulename__
__datadirname__ = __modulename__ + '_files' # only used when not running in xbmc
__wkdir__ = os.getcwd()
__parentdir__ = ( os.path.dirname(__wkdir__) )
__resolvers__ = os.path.join(__wkdir__,'resolvers')
__icons__ = os.path.join(__resolvers__,'resolver_icons')

#append resolver lib path to library.
sys.path.append( os.path.join(__resolvers__,'lib') )

# get path to where we store the files eg. cookies
if __xbmc__ == True: __filespath__ = xbmc.translatePath('special://profile/addon_data/'+__xbmcmodulename__)
elif __xbmc__ == False: __filespath__ = os.path.join(__parentdir__,__datadirname__)
            
#to avoid any errors, create the directory, as xbmc doesn't always do this.           
try:
    if not os.path.exists(__filespath__): os.makedirs(__filespath__)
except:
        #need to put our own proper error here, not use a print
        print "could not create data directory!"        



# scan resolvers directory, and import all resolvers.


def resolve(url, hoster = False):
    ''' ressolve urls of any host, pass me either a list, a string or some html page source'''
    pass


def login(username, password, hoster):
    '''Login to sites that support logins'''
    pass
