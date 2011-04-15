import re,sys,urllib


def _functionId(obj, nFramesUp):
	""" Create a string naming the function n frames up on the stack. """
	fr = sys._getframe(nFramesUp+1)
	co = fr.f_code
	return "%s.%s" % (obj.__class__, co.co_name)

def notImplemented(obj=None):
	""" Use this instead of 'pass' for the body of abstract methods. """
	raise Exception("Unimplemented abstract method: %s" % _functionId(obj, 1))


#class that is inherited by all resolvers.		
class FileHostModule:
	"""
	Generic FileHostModule for resolving and checking links for file hosts within XBMC addons
	"""

##########Methods that need to be implemented by each plugin#####

	def getIconFileHost(self):
		"""
		Returns a URL with an icon for the filehost.
		"""
		notImplemented(self)
	
	def getIconURL(self, url):
		"""
		Returns a URL with an icon for the specified URL
		"""
		return self.getIconFileHost()
	
	def getRegularExpression(self):
		"""
		Returns a regular expression that finds links of this file host within HTML source.
		"""
		notImplemented(self)
		
	def filterOnlineURLs(self,urls):
		"""
		Filters a list of URLs for the ones that are accessible with this module
		"""
		notImplemented(self)
		
	def isLoginValid(self,username,password):
		"""
		Checks if the specified login credentials are valid
		"""
		notImplemented(self)

	def isLoginForStreaming(self,username,password):
		"""
		Checks if the supplied link is valid for streaming files within XBMC (think about free or expired accounts)
		"""
		notImplemented(self)
		
	def login(self,username,password):
		"""
		Logs into a file host service and stores cookie information for later use
		""" 
		notImplemented(self)

	def isLoggedIn(self):
		"""
		Checks if the user is still logged in
		"""
		notImplemented(self)
	
	def logout(self):
		"""
		Logs out the currently logged in user.
		This deletes the login cookies.
		"""
		notImplemented(self)
		
	def getPlaylistItems(self,urls):
		"""
		returns playlist items (resolved) for the specified urls. Adds all available meta info to it (icon, filename, etc.)
		"""
		notImplemented(self)

########## Helper/convenience functions that might work for all plugins #####

	def
	(self, url):
		"""
		Checks if the supplied link is valid for this file host
		"""
		try:
			return (len(self.filterValidURLs([url]))>0)
		except:
			return False
	
	def filterValidURLs(self,urls):
		"""
		Checks if the supplied links are valid for this file host
		"""
		res=[]
		for url in urls:
			if re.findall(self.getRegularExpression(),url)!=None:
				res.append(url)
		return res



	def isURLOnline(self,url):
		"""
		Checks if a URL of this file host is online
		"""
		try:
			return (len(self.filterOnlineURLs([url]))>0)
		except:
			return False


	def resolveURLs(self,urls):
		"""
		Resolves a url for this module's host
		"""
		return self.filterOnlineURLs(urls)

	def resolveURL(self,url):
		"""
		Checks if the supplied link is valid for this file host
		"""
		try:
			return self.filterOnlineURLs([url])[0]
		except:
			return None
	
	def findURLs(self,pagesource):
		"""
		Finds URLs of this host within HTML page source
		"""
		res=[]
		reres=re.findall(self.getRegularExpression(),pagesource)
		for oneurl in reres:
			try:
				res.append(oneurl[0])
			except:
				pass
		return res

	def findAndResolveURLs(self, pagesource):
		"""
		Resolves all links found in the supplied HTML source to streamable URLs
		"""
		r=self.findURLs(pagesource)
		return self.resolveURLs(r)

	def getFileName(self,url):
		"""
		Returns the filename of a URL for this host (some do not store this in the URL)
		"""
		try:
			return re.findall(r"/([\w_.-]*?(?=\?)|[\w_.-]*$/)",url)[0]
		except:
			return ""
		
	
	def getPlaylistItem(self,url):
		"""
		returns a playlist item (resolved) for the specified url. Adds all available meta info to it (icon, filename, etc.)
		"""
		return self.getPlaylistItems([url])

