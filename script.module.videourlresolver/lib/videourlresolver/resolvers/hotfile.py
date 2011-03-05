
import hashlib, urllib, urllib2, filehostmodule, os

class HotFileModule(filehostmodule.FileHostModule):
	
	def __init__(self):
		self.username=""
		self.password=""
	
	def __hotfileapicall(self, action, user, pas, params):
				md5mod=hashlib.md5()
				md5mod.update(pas)
				pwmd5 = md5mod.hexdigest()
				url = 'http://api.hotfile.com/'
				data = {'action': action, 'username': user, 'passwordmd5': pwmd5}
				for par in params:
					data[par] = params[par]
				data = urllib.urlencode(data)
				req = urllib2.Request(url + "?" + data)
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
				response = urllib2.urlopen(req)
				return response.read()
	
	def __getHFLink(self, user, pas, url):
		return self.__hotfileapicall("getdirectdownloadlink", user, pas, {"link":url})
		
	def __getHFLinks(self, user, pas, urls):
		return self.__hotfileapicall("getdirectdownloadlinks", user, pas, {"links":",".join(urls)})

	def __checkHFLinks(self, user, pas, urls):
		resp=self.__hotfileapicall("checklinks", user, pas, {"fields":"status","links":",".join(urls)})
		resparray=resp.split()
		retlinks=[]
		for i in range(0,len(urls)-1):
			if resparray[i][0]=="1":
				retlinks.append(urls[i])
		return retlinks

	def getIconFileHost(self):
		return os.path.join(__file__, "resolver_icons", "hotfile.png")
	
	def getRegularExpression(self):
		return r"http://(www.)?hotfile\.com/dl/\d+/[0-9a-zA-Z]+/"
	
	def filterOnlineURLs(self, urls):
		validurls = self.filterValidURLs(urls)
		return self.__checkHFLinks(self.username,self.password,validurls)

	def isLoginValid(self, username, password):
		return not self.__hotfileapicall("getuserinfo",username,password,[])==".invalid username or password"

	def isLoginForStreaming(self, username, password):
		return self.__hotfileapicall("getuserinfo",username,password,[]).find("is_premium=1")>-1
	
	def login(self, username, password):
		self.username=username
		self.password=password
		return self.isLoginValid(username, password)

	def isLoggedIn(self):
		return self.isLoginValid(self.username, self.password)
	
	def logout(self):
		self.username=""
		self.password=""
		return True

	def resolveURLs(self, urls):
		res=self.__getHFLinks(self.username,self.password,urls)
		ret=[]
		resa=res.split("\n")
		for line in resa:
			try:
				cols=line.split("|")
				if cols[0]!="":
					if cols[1][0:4]=="http":
						ret.append(cols[1])
			except:
				pass
		return ret

	def getFileName(self, url):
		res=self.__getHFLinks(self.username,self.password,[url])
		cols=res.replace("\n","").split("|")
		try:
			if cols[0]!="":
				if cols[1][0:4]=="http":
					return cols[0]
		except:
			pass
		return None