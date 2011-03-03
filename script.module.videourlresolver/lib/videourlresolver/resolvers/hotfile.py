'''
Hotfile Premium Resolver

Unbehagan

Not yet tested....
'''

import md5,urllib,urllib2

def hotfileapicall(action, user, pas, params):
			pwmd5= md5.new(pas).hexdigest()
			#print pwmd5
			url = 'http://api.hotfile.com/'
			data={'action': action,'username': user, 'passwordmd5': pwmd5}
			for par in params:
				data[par]=params[par]
			data=urllib.urlencode(data)
			req = urllib2.Request(url+"?"+data)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
			response = urllib2.urlopen(req)
			return response.read()

def getHFLink(user,pas,url):
	return hotfileapicall("getdirectdownloadlink",user,pas,{"link":url})
	
def getHFLinks(user,pas,url):
	return hotfileapicall("getdirectdownloadlink",user,pas,{"link":url})


params=get_params()

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
