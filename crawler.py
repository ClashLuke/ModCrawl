import threading
import requests
import random
import shutil
import time
import sys
import re

#-=-=-=-=-=-=-=-=-=-#
# GLOBAL DEFINITION #
#-=-=-=-=-=-=-=-=-=-#

tab = ' '*8
splitters = [' ', '"', '\'', '#', ':', ';', '<', '>', '{', '}', '[', ']', '(', ')']
dotWords = [
		"\\ \\[dot\\]\\ ", "\\ DOT\\ ", "\\ Точка\\ ", "\\(\\.\\)", "\\(bod\\)",
		"\\(dot\\)", "\\(piste\\)", "\\(pont\\)", "\\(ponto\\)", "\\(punct\\)",
		"\\(punkt\\)", "\\(punkts\\)", "\\(punktur\\)", "\\(punt\\)", "\\(punto\\)",
		"\\(taškas\\)", "\\(tocka\\)", "\\-\\.\\-", "\\.\\</span\\>",
		"\\.\\<span\\ class\\=b0\\>", "\\.\\<span\\ class\\=b1\\>",
		"\\.\\<span\\ class\\=b2\\>", "\\.\\<span\\ class\\=b3\\>",
		"\\.\\<span\\ class\\=b4\\>", "\\.\\<span\\ class\\=b5\\>",
		"\\.\\<span\\ class\\=b6\\>", "\\[\\.\\]", "\\[bod\\]", "\\[DOT\\]", "\\[piste\\]",
		"\\[pont\\]", "\\[ponto\\]", "\\[punct\\]", "\\[punkt\\]", "\\[punkts\\]",
		"\\[punktur\\]", "\\[punt\\]", "\\[punto\\]", "\\[taškas\\]", "\\[tocka\\]",
		"\\_\\.\\_", "\\_bod\\_", "\\_DOT\\_", "\\_piste\\_", "\\_pont\\_",
		"\\_ponto\\_", "\\_punct\\_", "\\_punkt\\_", "\\_punkts\\_", "\\_punktur\\_",
		"\\_punt\\_", "\\_punto\\_", "\\_taškas\\_", "\\_tocka\\_", "\\{\\.\\}",
		"\\{bod\\}", "\\{dot\\}", "\\{piste\\}", "\\{pont\\}", "\\{ponto\\}",
		"\\{punct\\}", "\\{punkt\\}", "\\{punkts\\}", "\\{punktur\\}", "\\{punt\\}",
		"\\{punto\\}", "\\{taškas\\}", "\\{tocka\\}", "\\<\\.\\>", "\\</em\\>\\.",
		"\\<bod\\>", "\\<dot\\>", "\\<piste\\>", "\\<pont\\>", "\\<ponto\\>",
		"\\<punct\\>", "\\<punkt\\>", "\\<punkts\\>", "\\<punktur\\>", "\\<punt\\>",
		"\\<punto\\>", "\\<taškas\\>", "\\<tocka\\>", "bod", "\\-bod\\-", "dot",
		"dot\\-", "piste", "\\-piste\\-", "pont", "\\-pont\\-", "ponto",
		"\\-ponto\\-", "punct", "\\-punct\\-", "punkt", "\\-punkt\\-",
		"punkts", "\\-punkts\\-", "punktur", "\\-punktur\\-", "punt", "punt\\-", "punto",
		"\\-punto\\-", "taškas", "\\-taškas\\-", "tocka", "\\-tocka\\-", "\\."
		]

atWords = [
		'\\ \\[at\\]\\ ', '\\ \\[dog\\]\\ ', '\\ aet\\ ', '\\ apenstaartje\\ ',
		'\\ apestaartje\\ ', '\\ arroba\\ ', '\\ AT\\ ', '\\ ät\\ ', '\\ ätt\\ ',
		'\\ eta\\ ', '\\ hja\\ ', '\\ hjá\\ ', '\\ krøllalfa\\ ', '\\ kukac\\ ', '\\ la\\ ',
		'\\ malpa', '\\ malpka\\ ', '\\ na\\ ', '\\ nospam', '\\ nospam\\ \\@', '\\ pri\\ ',
		'\\ snabel\\ ', '\\ snabel\\-a\\ ', '\\ taškas\\ ', '\\ zav\\ ', '\\ zavinac\\ ',
		'\\ znak\\ ', '\\ Собачка\\ ', '\\(\\)', '\\(\\@\\)', '\\(a\\)', '\\(à\\)',
		'\\(aet\\)', '\\(apenstaartje\\)', '\\(apestaartje\\)', '\\(arroba\\)', '\\(at\\)',
		'\\(ät\\)', '\\(ätt\\)', '\\(eta\\)', '\\(hja\\)', '\\(hjá\\)', '\\(krøllalfa\\)',
		'\\(kukac\\)', '\\(malpa\\)', '\\(malpka\\)', '\\(nospam\\)\\@', '\\(pri\\)',
		'\\(Shift\\+2\\)', '\\(snabel\\)', '\\(snabel\\-a\\)', '\\(taškas\\)',
		'\\(wpisz\\ znak\\ \\@\\)', '\\(zav\\)', '\\(zavinac\\)', '\\(znak\\ \\@\\)',
		'\\(znak\\)', '\\(собака\\)', '\\)nospam', '\\.\\@\\.', '\\.a\\.', '\\.à\\.',
		'\\.aet\\.', '\\.apenstaartje\\.', '\\.apestaartje\\.', '\\.arroba\\.', '\\.at\\.',
		'\\.ät\\.', '\\.ätt\\.', '\\.eta\\.', '\\.hja\\.', '\\.hjá\\.', '\\.krøllalfa\\.',
		'\\.kukac\\.', '\\.malpa\\.', '\\.malpka\\.', '\\.nospam\\.', '\\.pri\\.',
		'\\.snabel\\.', '\\.snabel\\-a\\.', '\\.taškas\\.', '\\.zav\\.', '\\.zavinac\\.'
		'\\.znak\\.', '\\-\\@\\-', '\\@\\ nospam', '\\@\\(nospam\\)', '\\@\\[nospam\\]',
		'\\@\\<em\\>', '\\@\\<span\\ class\\=b0\\>', '\\@\\<span\\ class\\=b1\\>',
		'\\@\\<span\\ class\\=b2\\>', '\\@\\<span\\ class\\=b3\\>',
		'\\@\\<span\\ class\\=b4\\>', '\\@\\<span\\ class\\=b5\\>',
		'\\@\\<span\\ class\\=b6\\>', '\\@nospam', '\\@\\-nospam\\-', '\\@nospam\\.',
		'\\[\\@\\]', '\\[\\]', '\\[a\\]', '\\[à\\]', '\\[aet\\]', '\\[apenstaartje\\]',
		'\\[apestaartje\\]', '\\[arroba\\]', '\\[AT\\]', '\\[ät\\]', '\\[ätt\\]',
		'\\[dog\\]', '\\[eta\\]', '\\[hja\\]', '\\[hjá\\]', '\\[krøllalfa\\]',
		'\\[kukac\\]', '\\[malpa\\]', '\\[malpka\\]', '\\[nospam\\]\\@', '\\[pri\\]',
		'\\[snabel\\]', '\\[snabel\\-a\\]', '\\[sobaka\\]', '\\[taškas\\]', '\\[zav\\]',
		'\\[zavinac\\]', '\\[znak\\]', '\\]nospam', '\\_\\@\\_', '\\_a\\_', '\\_à\\_',
		'\\_aet\\_', '\\_apenstaartje\\_', '\\_apestaartje\\_', '\\_arroba\\_', '\\_AT\\_',
		'\\_ät\\_', '\\_ätt\\_', '\\_eta\\_', '\\_hja\\_', '\\_hjá\\_', '\\_krøllalfa\\_',
		'\\_kukac\\_', '\\_malpa\\_', '\\_malpka\\_', '\\_pri\\_', '\\_snabel\\_',
		'\\_snabel\\-a\\_', '\\_taškas\\_', '\\_zav\\_', '\\_zavinac\\_', '\\_znak\\_',
		'\\{\\@\\}', '\\{a\\}', '\\{à\\}', '\\{aet\\}', '\\{apenstaartje\\}',
		'\\{apestaartje\\}', '\\{arroba\\}', '\\{at\\}', '\\{ät\\}', '\\{ätt\\}',
		'\\{eta\\}', '\\{hja\\}', '\\{hjá\\}', '\\{krøllalfa\\}', '\\{kukac\\}',
		'\\{malpa\\}', '\\{malpka\\}', '\\{pri\\}', '\\{snabel\\}', '\\{snabel\\-a\\}',
		'\\{taškas\\}', '\\{zav\\}', '\\{zavinac\\}', '\\{znak\\}', '~\\@~', '~a~', '~à~',
		'~aet~', '~apenstaartje~', '~apestaartje~', '~arroba~', '~at~', '~ät~', '~ätt~',
		'~eta~', '~hja~', '~hjá~', '~krøllalfa~', '~kukac~', '~malpa~', '~malpka~', '~pri~',
		'~snabel~', '~snabel\\-a~', '~taškas~', '~zav~', '~zavinac~', '~znak~', '\\<\\@\\>',
		'\\<\\-\\@\\-\\>', '\\<a\\>', '\\<\\-a\\-\\>', '\\<à\\>', '\\<à\\-\\>', '\\<aet\\>',
		'\\<\\-aet\\-\\>', '\\<apenstaartje\\>', '\\<\\-apenstaartje\\>',
		'\\<apestaartje\\>', '\\<\\-apestaartje\\-\\>', '\\<arroba\\>', '\\<\\-arroba\\-\\>',
		'\\<at\\>', '\\<\\-at\\-\\>', '\\<ät\\>', '\\<\\-ät\\-\\>', '\\<ätt\\>',
		'\\<\\-ätt\\-\\>', '\\<eta\\>', '\\<\\-eta\\-\\>', '\\<hja\\>', '\\<\\-hja\\-\\>',
		'\\<hjá\\>', '\\<\\-hjá\\-\\>', '\\<krøllalfa\\>', '\\<\\-krøllalfa\\-\\>',
		'\\<kukac\\>', '\\<\\-kukac\\-\\>', '\\<malpa\\>', '\\<malpa\\-\\>', '\\<malpka\\>',
		'\\<\\-malpka\\-\\>', '\\<pri\\>', '\\<\\-pri\\-\\>', '\\<snabel\\>',
		'\\<\\-snabel\\-\\>', '\\<snabel\\-a\\>', '\\<\\-snabel\\-a\\-\\>', '\\<taškas\\>',
		'\\<\\-taškas\\-\\>', '\\<zav\\>', '\\<\\-zav\\-\\>', '\\<zavinac\\>',
		'\\<\\-zavinac\\-\\>', '\\<znak\\>', '\\<\\-znak\\-\\>', '\\-a\\-', '\\-à\\-',
		'\\-aet\\-', '\\-apenstaartje\\-', '\\-apestaartje\\-', '\\-arroba\\-', '\\-at\\-',
		'\\-ät\\-', '\\-ätt\\-', '\\-eta\\-', '\\-hja\\-', '\\-hjá\\-', '\\-krøllalfa\\-',
		'\\-kukac\\-', '\\-malpa\\-', '\\-malpka\\-', 'nospam\\@', '\\-nospam\\-\\@',
		'\\-pri\\-', '\\-snabel\\-', '\\-snabel\\-a\\-', '\\-taškas\\-', '\\-zav\\-',
		'\\-zavinac\\-', '\\-znak\\-', 'Собачка', '\\@'
		]

urlBlacklist = [
		".3g2", ".3gp", ".3gp2", ".3gpp", ".3gpp2", ".7z", ".ace", ".ai", ".aif", ".ani",
		".apk", ".arc", ".arj", ".asf", ".asx", ".avi", ".bak", ".bat", ".bh", ".bin",
		".bing.", ".bmp", ".bz", ".cab", ".cda", ".cer", ".cfg", ".cgi", ".cla", ".class",
		".com", ".cpl", ".cpp", ".cs", ".css", ".csv", ".cur", ".dat", ".db", ".deb", ".dll",
		".dmg", ".dmp", ".doc", ".drv", ".exe", ".f4v", ".flac", ".flv", ".fnt", ".fon",
		".gadget", ".gif", ".google.", ".gtp", ".gz", ".h", ".h264", ".icns", ".ico", ".ini",
		".iso", ".jar", ".java", ".jpeg", ".jpg", ".js", ".jsp", ".key", ".lha", ".log",
		".m4v", ".mdb", ".mid", ".midi", ".mkv", ".mod", ".moov", ".mov", ".mp3", ".mp4",
		".mpa", ".mpeg", ".mpg", ".msi", ".mts", ".odp", ".ods", ".ogg", ".otf", ".part",
		".pdf", ".pkg", ".pl", ".png", ".pps", ".ppt", ".ps", ".psd", ".py", ".rar", ".riff",
		".rm", ".rmi", ".rpm", ".rss", ".sav", ".sh", ".spl", ".sql", ".srt", ".stl", ".svg",
		".swf", ".swift", ".sys", ".tar", ".tff", ".tif", ".tiff", ".tmp", ".toast", ".vb",
		".vcd", ".vdi", ".vid", ".vob", ".wav", ".wim", ".wm", ".wma", ".wmv", ".wpl",
		".wsf", ".xbm", ".xlr", ".xls", ".xml", ".xss", ".yahoo.", ".yuv", ".z", ".zip",
		"addreply.php", "altavista.com", "answers.com", "ask.com", "baidu.com",
		"dictionary.reference.com", "doubleclick", "editpost.php", "formmail.php", "fraud",
		"go.mail.ru", "googleadservices.com", "javascript", "msn.com", "nova.rambler.ru",
		"pms.php", "print.php", "profil.php", "report.php", "scam", "spam", "usercp.php",
		"www.w3.org", "yandex."
		]


outBlacklist = urlBlacklist + [
			"bugraq", "daemon", "ezine", "fidonet", "fraud", "-join", "junk",
			"-leave", "listme", "listserv", "mailer-daemon", "majordomo", "noreply",
			"nospam", "notice", "postmaster", "privacy", "remove", "removeme", "ripoff",
			"scam", "spam", "spamcop", "subscribe", "unsubscribe", "username",
			"yourdomain", "yourname", ".php", ".htm"
		]

urlRegex = r"((http:\/\/|https:\/\/)[a-zA-Z0-9]*([\-\.]{1}[a-zA-Z0-9]+)*\.([a-zA-Z]*[0-9]*(\/)?(\.)?(\%)?(\&)?(\\A7)?(\;)?(\:)?(\+)?(\?)?(\=)?)*)"
outRegex = r"(([a-zA-Z0-9_.+-]+("+'|'.join(atWords)+r")[a-zA-Z0-9-]+("+'|'.join(dotWords)+")[a-zA-Z0-9-.]+))"

#-=-=-=-=-=-=-=-=-=-#
# SUPPORT FUNCTIONS #
#-=-=-=-=-=-=-=-=-=-#

def initFiles():
	newUrlsFile = open("newUrls",'w')
	newUrlsFile.write('')
	newUrlsFile.close()
	processedUrlsFile = open("processedUrls",'w')
	processedUrlsFile.write('')
	processedUrlsFile.close()
	processedUrlsFile = open("output.txt",'w')
	processedUrlsFile.write('')
	processedUrlsFile.close()

def printIntended(text, intendation):
	print("        "*intendation,text)

def printBold(text):
	print("\033[1m{}\033[0m".format(text))

def help():
	printBold("NAME") 
	printIntended("ModCrawl - The modular and powerful web crawler\n",1)  
	printBold("SYNOPSIS")
	printIntended("python3 {} [--query] [--engine] [--max] [--help]\n".format(sys.argv[0]),1)
	printBold("OPTIONS")
	printIntended("-h, --help",1)
	printIntended("Prints the help page/manual.\n",2)
	printIntended("-c, --continue",1)
	printIntended("Continue the previous list. Usable when previously started",2)
	printIntended("a crawl operation.\n",2)
	printIntended("-q <arg>, --query <arg>",1)
	printIntended("Use <arg> to create requests at search engines. A",2)
	printIntended("space ' ' character has to be replaced by \"%20\"",2)
	printIntended("sign, all other replacements are handled by the library.\n",2)
	printIntended("-e <arg>, --engine <arg>",1)
	printIntended("Performs search requests at specified search engine(s).",2)
	printIntended("Compatible search engines are ask, bing, duckduckgo,",2)
	printIntended("google, yahoo and webcrawler. They can be used by",2)
	printIntended("building a string out of the first letter of the engine",2)
	printIntended("such as gbwa for ask, bing, google and webcrawler.\n",2)
	printIntended("-m <num>, --max <num>",1)
	printIntended("A parameter to determine the maximum number of URLs which",2)
	printIntended("will be scraped. Set -1 to continue forever\n",2)
	printIntended("-f <num>, --file <num>",1)
	printIntended("Add a keyword file in favor of a querying one keyword.",2)
	printIntended("Allows the usage of multiple keywords, split by newline.\n",2)
	printIntended("-t <num>, --threads <num>",1)
	printIntended("Defines the number of threads to be used when scraping.",2)
	printIntended("threads decrease the time needed to download a website,",2)
	printIntended("since ping times and delays are paralellized.",2)
	sys.exit()

def processArgs():
	query = ""
	fileName = ""
	engine = "g"
	maxUrls = -1
	threadCount = 1
	c = False # Continue?
	for i in range(1,len(sys.argv)):
		if sys.argv[i] == '-q' or sys.argv[i] == '--query':
			try:
				query = sys.argv[i+1]
			except:
				pass
			continue
		if sys.argv[i] == '-f' or sys.argv[i] == '--file':
			try:
				fileName = sys.argv[i+1]
			except:
				pass
			continue
		if sys.argv[i] == '-e' or sys.argv[i] == '--engine':
			try:
				engine = sys.argv[i+1]
			except:
				pass
			continue
		if sys.argv[i] == '-m' or sys.argv[i] == '--max':
			try:
				maxUrls = int(sys.argv[i+1])
			except:
				pass
			continue
		if sys.argv[i] == '-t' or sys.argv[i] == '--threads':
			try:
				threadCount = int(sys.argv[i+1])
			except:
				pass
			continue
		if sys.argv[i] == '-c' or sys.argv[i] == '--continue':
			try:
				c = True
			except:
				pass
			continue
		if sys.argv[i] == '-h' or sys.argv[i] == '--help':
			help()
	if maxUrls == 0 or threadCount == 0 or (query == "" and fileName == ""):
		help()
	return([query, engine, maxUrls, threadCount, fileName, c])

def processQuery(query):
	replacementList = [
				[' ', "%20"], ['!', "%21"], ['#', "%23"],
				['$', "%24"], ["&", "%26"], ["'", "%27"], ['(', "%28"],
				[')', "%29"], ['*', "%2A"], ['+', "%2B"], [',', "%2C"],
				['/', "%2F"], [':', "%3A"], [';', "%3B"], ['=', "%3D"],
				['?', "%3F"], ['@', "%40"], ['[', "%5B"], [']', "%5D"]
			  ]
	for r in replacementList:	
		query = query.replace(r[0],r[1])
	return(query)
	

def buildSearchLinks(query, engine):
	urls = []
	engines = []
	if "g" in engine:
		urls.append("https://www.google.com/search?q={}".format(query))
		urls.append("https://www.google.com/search?q={}&start=100".format(query))
		urls.append("https://www.google.com/search?q={}&start=200".format(query))
		engines.append("Google")
	if "b" in engine:
		urls.append("https://www.bing.com/search?q={}".format(query))
		urls.append("https://www.bing.com/search?q={}&first=11".format(query))
		urls.append("https://www.bing.com/search?q={}&first=21".format(query))
		urls.append("https://www.bing.com/search?q={}&first=31".format(query))
		urls.append("https://www.bing.com/search?q={}&first=41".format(query))
		urls.append("https://www.bing.com/search?q={}&first=51".format(query))
		urls.append("https://www.bing.com/search?q={}&first=61".format(query))
		urls.append("https://www.bing.com/search?q={}&first=71".format(query))
		urls.append("https://www.bing.com/search?q={}&first=81".format(query))
		urls.append("https://www.bing.com/search?q={}&first=91".format(query))
		engines.append("Bing")
	if "y" in engine:
		urls.append("https://search.yahoo.com/search?p={}".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=11".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=21".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=31".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=41".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=51".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=61".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=71".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=81".format(query))
		urls.append("https://search.yahoo.com/search?p={}&b=91".format(query))
		engines.append("Yahoo")
	if "a" in engine:
		urls.append("https://www.ask.com/web?q={}".format(query))
		urls.append("https://www.ask.com/web?q={}&page=2".format(query))
		urls.append("https://www.ask.com/web?q={}&page=3".format(query))
		urls.append("https://www.ask.com/web?q={}&page=4".format(query))
		urls.append("https://www.ask.com/web?q={}&page=5".format(query))
		urls.append("https://www.ask.com/web?q={}&page=6".format(query))
		urls.append("https://www.ask.com/web?q={}&page=7".format(query))
		urls.append("https://www.ask.com/web?q={}&page=8".format(query))
		urls.append("https://www.ask.com/web?q={}&page=9".format(query))
		engines.append("Ask")
	if "d" in engine:
		urls.append("https://duckduckgo.com/?q={}".format(query))
		engines.append("DuckDuckGo")
	if "w" in engine:
		urls.append("http://www.webcrawler.com/serp?q={}".format(query))
		urls.append("http://www.webcrawler.com/serp?page=2&q={}".format(query))
		urls.append("http://www.webcrawler.com/serp?page=3&q={}".format(query))
		urls.append("http://www.webcrawler.com/serp?page=4&q={}".format(query))
		urls.append("http://www.webcrawler.com/serp?page=5&q={}".format(query))
		urls.append("http://www.webcrawler.com/serp?page=6&q={}".format(query))
		urls.append("http://www.webcrawler.com/serp?page=7&q={}".format(query))
		urls.append("http://www.webcrawler.com/serp?page=8&q={}".format(query))
		urls.append("http://www.webcrawler.com/serp?page=9&q={}".format(query))
		engines.append("Webcrawler")
	return(urls, engines)
		

def init():
	print("Processing arguments",end='\r')
	query, engine, maxUrls, threadCount, fileName, c = processArgs()
	if(not(c)):
		initFiles()
		query = [query]
		if(fileName != ""):
			print("Reading Keywords",end='\r')
			f = open(fileName, 'r')
			r = f.read().split('\n')
			for line in r:
				query.append(line)
		print("Increasing keyword quality",end='\r')
		query = sorted(list(set(query)))
		for i in range(len(query)):
			if query[i] == '':
				del query[i]
			else:
				break
		print("Processing keywords",end='\r')
		searchQuery = [processQuery(q) for q in query]
		query = [q.replace('%20',' ') for q in query]
		print("Building search links",end='\r')
		for q in searchQuery:
			urls, engines = buildSearchLinks(q, engine)
			addNewUrls(urls)
		print("Starting crawler",end='\r')
		print("                          ",end='\r')
		return([maxUrls, engines, query, threadCount])
	return([maxUrls, buildSearchLinks(query, engine)[1], query.replace('%20',' '), threadCount])

def progess(current, maximum):
	currentProgress = int((50*current)//maximum)
	progress100 = int((100*current)//maximum)
	cString = str(current)
	cMax = str(maximum)
	print("Progress: [% 3d"%progress100+'%]'+'#'*currentProgress+' '*(50-currentProgress)+']'+' ({}/{})'.format(' '*(len(cMax)-len(cString))+cString, cMax),end='\r')

def seperator():
	print('\n'+'='*79+'\n')

def applyRegex(string, regex):
	return(re.findall(regex,string))

def searchURL(string):
	return(applyRegex(string, urlRegex))

def searchTarget(string):
	return(applyRegex(string, outRegex))

#-=-=-=-=-=-=-=-=-=-#
# LIBRARY FUNCTIONS #
#-=-=-=-=-=-=-=-=-=-#

def getUrlProxy(url, proxy):
	r = requests.get(url, proxy)
	return(r.text)

def getUrl(url):
	r = requests.get(url)
	return(r.text)

def checkDoublesProcessed(urllist):
	fp = open("processedUrls",'r')
	urlCount = len(urllist)
	for i, line in enumerate(fp):
		for j in range(urlCount):
			try:
				if urllist[j] == line.replace('\n',''):
					del urllist[j]
			except:
				continue
	fp.close()
	return(urllist)
			
def checkDoublesNew(urllist):
	fp = open("newUrls",'r')
	urlCount = len(urllist)
	for i, line in enumerate(fp):
		for j in range(urlCount):
			try:
				if urllist[j] == line.replace('\n',''):
					del urllist[j]
			except:
				continue
	fp.close()
	return(urllist)
			
def checkDoublesOut(outlist):
	fp = open("output.txt",'r')
	urlCount = len(outlist)
	for i, line in enumerate(fp):
		for j in range(len(outlist)):
			try:
				if outlist[j] == line.replace('\n',''):
					del outlist[j]
			except:
				continue
	fp.close()
	return(outlist)

def checkDoublesUrl(urllist):
	urllist = checkDoublesNew(urllist)
	return(checkDoublesProcessed(urllist))

def addNewUrls(urllist):
	urllist = list(set(urllist))
	prevFile = open("processedUrls",'r')
	prevList = prevFile.read().split('\n')
	prevFile.close()
	curFile = open("newUrls",'r')
	prevList = prevList + curFile.read().split('\n')
	curFile.close()
	f = open("newUrls",'a')
	for url in urllist:
		if not(url in prevList) and (len(url.replace(' ','')) != 0):
			f.write(url)
			f.write('\n')
	f.close()

def addNewOut(outlist):
	outlist = list(set(outlist))
	prevFile = open("output.txt",'r')
	prevList = prevFile.read().split('\n')
	prevFile.close()
	f = open("output.txt",'a')
	for out in outlist:
		if not(out in prevList) and (len(out.replace(' ','')) != 0):
			f.write(out)
			f.write('\n')
	f.close()

def removeLastNewUrl():
	curFile = open("newUrls",'r') 
	prevList = curFile.read().split('\n')
	curFile.close()
	newFile = open("newUrls",'w')
	newFile.write('\n'.join(prevList[1:]))
	newFile.close()

def addProcessedUrl(url):
	prevFile = open("processedUrls",'a')
	prevFile.write(url+'\n')
	prevFile.close()

def finishUrlProcessing(url):
	addProcessedUrl(url)
	removeLastNewUrl()

def proxyCheck(proxies, prevTime):
	curTime = int(time.time()//60)
	if(prevTime != curTime):
		proxies = getUrl("https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt").split('\n')
	return([proxies, curTime])

def checkUrlBlacklist(currentUrl):
	for b in urlBlacklist:
		if b in currentUrl:
			return 1
	return 0

def checkOutBlacklist(currentOut):
	for b in outBlacklist:
		if b in currentOut:
			return 1
	return 0

def preProcess(proxies, currentHour):
	curFile = open("newUrls",'r') 
	while True:
		url = curFile.readline().replace('\n','')
		if url != '':
			break
	curFile.close()
	proxies, currentHour = proxyCheck(proxies, currentHour)
	return([url, proxies, currentHour])

def fullProcess(maxUrls, proxies, currentHour):
	try:
		url, proxies, currentHour = preProcess(proxies, currentHour)
	except:
		pass
	removeLastNewUrl()
	try:
		processUrl(url, proxies[maxUrls%len(proxies)])
	except:
		pass
	return([maxUrls, proxies, currentHour])

#-=-=-=-=-=-=-=-#
# API FUNCTIONS #
#-=-=-=-=-=-=-=-#

def processUrl(url, proxy):
	try:
		content = getUrlProxy(url, proxy)
		urls = []
		out = []	
		contentUrl = searchURL(content)
		contentTarget = searchTarget(content)
		for c in contentUrl:
			currentUrl = c[0]
			if(checkUrlBlacklist(currentUrl) == 1):
				continue
			urls.append(currentUrl)
		for c in contentTarget:
			currentOut = c[0]
			if(checkOutBlacklist(currentOut) == 1):
				continue
			for a in atWords:
				currentOut.replace(a.replace('\\',''), '@')
			for d in dotWords:
				currentOut.replace(d.replace('\\',''), '.')
			out.append(currentOut)
		urls = checkDoublesUrl(list(set(urls)))
		out = checkDoublesOut(list(set(out)))
		addNewUrls(urls)
		addNewOut(out)
		finishUrlProcessing(url)
	except KeyboardInterrupt:
		sys.exit(1)
	except:
		return

def scrape(maxUrls, threadCount):
	proxies, currentHour = proxyCheck([], 0)
	current = 0
	increaser = threadCount
	threadCount -= 1
	threads = [None]*threadCount
	if(maxUrls > 0):
		while(current != maxUrls):
			progess(current, maxUrls)
			threads = [threading.Thread(target=fullProcess, args=(maxUrls, proxies, currentHour)) for i in range(threadCount)]
			for t in threads:
				t.start()
				time.sleep(1)
				current += 1
				progess(current, maxUrls)
			current += 1
			progess(current, maxUrls)
	else:
		startTime = int(time.time())
		while(True):
			curDelta = int(time.time()-startTime)
			print("Processed: {}{}Elapsed: {}h {}min {}s".format(current,tab,int((curDelta/60/60)%24),int((curDelta/60)%60),curDelta%60),end='\r')
			maxUrls, proxies, currentHour = fullProcess(maxUrls, proxies, currentHour)
			threads = [threading.Thread(target=fullProcess, args=(maxUrls, proxies, currentHour)) for i in range(threadCount)]
			for t in threads:
				t.start()
				time.sleep(1)
				current += 1
				curDelta = int(time.time()-startTime)
				print("Processed: {}{}Elapsed: {}h {}min {}s".format(current,tab,int((curDelta/60/60)%24),int((curDelta/60)%60),curDelta%60),end='\r')
			maxUrls, proxies, currentHour = fullProcess(maxUrls, proxies, currentHour)
			current += 1
			curDelta = int(time.time()-startTime)
			print("Processed: {}{}Elapsed: {}h {}min {}s".format(current,tab,int((curDelta/60/60)%24),int((curDelta/60)%60),curDelta%60),end='\r')
			maxUrls, proxies, currentHour = fullProcess(maxUrls, proxies, currentHour)
	progess(maxUrls, maxUrls)
	print("\n")

if __name__ == "__main__":
	maxUrls, engines, keyword, threadCount = init()
	print("\n\033[1mModCrawl\033[0m - The modular and powerful web crawler\n")  
	seperator()
	if len(keyword) == 1:
		print("Keyword: {}".format(keyword[0]))
	else:
		print("Keywords: {}".format(", ".join(keyword)))
	print("Search Engines: {}".format(', '.join(engines)))
	print("Maximum URLs to scrape: {}".format(maxUrls))
	print("Threads: {}".format(threadCount))
	seperator()
	scrape(maxUrls, threadCount)
	
