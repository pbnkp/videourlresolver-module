'''
Countdown XBMC 0.1
Copyleft Anarchintosh

Set a countdown dialog for XBMC.
Necessary for some filehosters eg. megaupload
'''

def waiter(seconds):
    if __xbmc__ == True: time.sleep(seconds)
    else: xbmc.sleep((seconds*100))
        
def do_wait(time_to_wait,title):

    print 'waiting '+str(time_to_wait)+' secs'

    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create(title)

    secs=0
    percent=0
    increment = 100 / time_to_wait

    while secs < time_to_wait:
        secs = secs + 1
        percent = increment*secs                   
        display_countdown_info = 'Wait 'str((time_to_wait - secs)+1)+' seconds for the stream to become active.'
        pDialog.update(percent, display_countdown_info)
        waiter(1)

    print 'done waiting'
    return 'done'
