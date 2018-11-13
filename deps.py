#from sets import set #uncomment for usage in Python2 [Warning: Py2 uses a slower sets implementation]
import requests, re, os
from sys import platform

anti = [".jpg", ".gif", ".js", ".css", ".xss", ".mp3", ".mp4", ".ogg", ".flac", ".png", ".bmp", ".pdf", ".aif", ".cda", ".mid", ".midi", ".mpa", ".wav", ".wma", ".wpl", ".7z", ".arj", ".deb", ".pkg", ".rar", ".zip", ".z", ".tar", ".gz", ".bz", ".rpm", ".bin", ".dmg", ".iso", ".toast", ".vcd", ".vdi", ".csv", ".dat", ".db", ".log", ".mdb", ".sav", ".sql", ".xml", ".apk", ".bat", ".cgi", ".pl", ".py", ".com", ".exe", ".gadget", ".jar", ".wsf", ".fnt", ".fon", ".otf", ".tff", ".ai", ".ico", ".jpeg", ".ps", ".psd", ".svg", ".tif", ".tiff", ".jsp", ".rss", ".part", ".cer", ".key", ".odp", ".pps", ".ppt", ".class", ".cpp", ".cs", ".h", ".java", ".sh", ".swift", ".vb", ".ods", ".xlr", ".xls",  ".bak", ".cab", ".cfg", ".cpl", ".cur", ".dll", ".dmp", ".drv", ".icns", ".ini", ".msi", ".wim", ".sys", ".tmp", ".3g2", ".3gp", ".avi", ".flv", ".m4v", ".mkv", ".mov", ".mkv", ".mpg", ".mpeg", ".swf", ".doc"]


##====================================##
##  ##============================##  ##
##  ##                            ##  ##
##  ##        DEPENDENCIES        ##  ##
##  ##                            ##  ##
##  ##============================##  ##
##====================================##
       

def merge(source1, source2, result):
	try:
		res = list(set(open(source1, "r").readlines()+open(source1, "r").readlines()))
		open(source1, "w").write("")
		open(source2, "w").write("")
		print_to = open(result, "a")
		for i in res:
			print_to.write(i)
		return True
	except:
		return False


def req(url, prox, out, regex):
	out = open(out, "a")
	try:
		p_dict = {"http":"http://"+prox, "https":"https://"+prox, "ftp":"ftp://"+prox}	
		r = requests.get(url, proxies=p_dict).text
		res = re.findall(regex,r)
		for i in range(len(res)):
			breaking = True
			tmp = str(res[i][0][:-1].encode("utf-8"))
			for a in anti:
				if a in tmp:
					breaking = False
					break
			if breaking:
				out.write(tmp + "\n")
	except:
		pass


def check_duplicates(file_souce, file_source2 = ""):
	try:
		if file_source2 == "":
			f = open(file_source, "r+")
			s = list(set(f.readlines()))
			f.write("")
			f.close()
			f = open(file_source, "a")
			for t in s:
				f.write(t)
			return True
		l1 = open(file_source, "r").readlines()
		l2 = open(file_source2, "r").readlines()
		open(file_source,"w").write("")
		f = open(file_source,"a")
		for l in l1:
			if not(l1 in l2):
				f.write(l)

	except:
		return False

    
def clear():
        if platform == "linux" or platform == "linux2":
            os.system('clear')
        else:
            os.system('cls')



def input_default(text, default, typ = "string"):
    i = input("\033[0m" + text + '\t[' + str(default) + ']\t\033[1;33m')
    print('\033[0m',end='')
    if i == "":
        return default
    else:
        if typ == "string":
            return i

        elif typ == "int":
            try:
                return(int(i))
            except:
                print("Your input is not legit. Make sure you entered a \033[1;33m" + typ + "\033[0m.")
                return(input_default(text, default, typ))
