import requests
import concurrent.futures
import itertools
import sys
import os
import re

def concr(func,data,max_workers=50,thread=None):
	thread = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) if not(thread) else thread
	dat = list(thread.map(func,data))
	if len(dat) and (type(dat[0]) is dict):
		return dat
	else:
		try:
			if len(dat) and dat != None and not(all(map(lambda x: x == None, dat))):
				return list(itertools.chain(*dat))
			else:
				return dat
		except Exception as e:
			print(e)
			print(dat)
module_num = sys.argv[1] if len(sys.argv) > 1 else "2.1"

base_url = "https://tower.la.utexas.edu/reflect?url=http%3A%2F%2Fmedia.laits.utexas.edu%3A8080%2Fvideo_production%2F_hosted%2Fgov_312usfp_sum2015%2Fgov312_topic{}.srt"
base_url_2 = "https://tower.la.utexas.edu/reflect?url=http%3A%2F%2Fmedia.laits.utexas.edu%3A8080%2Fvideo_production%2F_hosted%2Fgov_312usfp_sp2016%2Fgov312_topic{}.srt"
base_url_3 = "https://tower.la.utexas.edu/reflect?url=http%3A%2F%2Fmedia.laits.utexas.edu%3A8080%2Fvideo_production%2F_hosted%2Fgov_312usfp_sum2016%2Fgov312_topic{}.srt"

links = [base_url_3,base_url_2,base_url]



def process_module(module):
	out = ""
	for line in module.split("\n"):
		number = re.match(r"^\d{1,3}\r",line)
		timings = re.match(r"\d\d:\d\d.*,\d.*\r",line)
		if not(number) and not(timings):
			out += " " + line.replace("\r\n"," ").replace("\r"," ").replace("\n"," ").replace("  "," ")
	return out.replace("  "," ").replace("  "," ")


override = {
	"5.4": "https://tower.la.utexas.edu/reflect?url=http%3A%2F%2Fmedia.laits.utexas.edu%3A8080%2Fvideo_services%2F_hosted%2Fgov_312usfp_fa2015%2Fbrennan%2Fgov312_topic5.4.srt"
}

def get_module(number,):
	if number in override:
		return process_module(requests.get(override[number]).text)
	for link in links:
		url = link.format(number)
		req = requests.get(url)
		found = "<title>404 Not Found</title>" not in str(req.content)
		if(found):
			# return re.sub(r'\?(?!")',".\n",re.sub(r'(?:[a-zA-z]{2,})\.(?!")',".\n",process_module(req.text)))
			return process_module(req.text)

def get_or_create(path):
	print("/".join(path.split("/")[:-1]))
	if(not os.path.exists("/".join(path.split("/")[:-1]))):
		os.makedirs("/".join(path.split("/")[:-1]))
	return open(path,"w+")
def load_module(module,submodule):
	# print(module,submodule)
	mod = "{}.{}".format(module,submodule)
	fetch = get_module(mod)
	if(fetch != None):
		handle = get_or_create("./captions/{}/{}-{}.txt".format(str(module).zfill(3),module,submodule))
		handle.write(fetch)
		handle.close()
def load_modules():			
	concr(lambda x: load_module(*x), [(module,submodule) for module in range(1,25) for submodule in range(0,10)],max_workers=25*10/2)

load_modules()

# print(content.replace(""))
# content = re.sub(re.compile(r"(^\d{1,4}\n)|(\d\d\:.*)",re.MULTILINE),"",content).replace("\n"," ")

# content = re.sub(re.compile(r"\\r\\r\d{1,4}",re.MULTILINE),"",content)
# print("\nModule {}".format(module_num))
# print(content)


