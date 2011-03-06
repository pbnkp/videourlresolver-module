'''
Countdown XBMC 0.2
Copyleft Anarchintosh

Set a countdown dialog for XBMC.
Necessary for some filehosters eg. megaupload
'''
if __xbmc__ == False:
    import time
    
def countdown(time_to_wait,title='',text=''):
    if __xbmc__ == True:
        do_xbmc_wait(time_to_wait,title,text)
    else:
        time.sleep(time_to_wait)

def do_xbmc_wait(time_to_wait,title,text):

    print 'waiting '+str(time_to_wait)+' secs'

    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create(title)

    secs=0
    percent=0
    increment = 100 / time_to_wait

    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = increment*secs
        secs_left = str((time_to_wait - secs))
        remaining_display = ' Wait '+secs_left+' seconds for the video stream to activate...'
        pDialog.update(percent,' '+text,remaining_display)
        xbmc.sleep(1000)
        if (pDialog.iscanceled()):
             cancelled = True
             break

    if cancelled == True:     
         print 'wait cancelled'
         return False
    else:
         print 'done waiting'
         return True

    print 'done waiting'
    return 'done'
