__author__ = "ChrxnZX | Pulsed#1874"
__version__ = "1.0.0"

initialSetupIndex = 0

import os
try:
	import requests
	#from requests import NewConnectionError
except ModuleNotFoundError:
	initialSetupIndex += 1
	os.system("pip install requests")
	print("Initial Setup Index No. " + str(initialSetupIndex))
	import requests

try:
	import warnings
except ModuleNotFoundError:
	os.system("pip install warnings")
	print("Initial Setup Index No. " + str(initialSetupIndex))
	import warnings

try:
    if not(requests.get("https://raw.githubusercontent.com/ChrxnZ/PG3D-Storage-API/main/Info/currentVer.txt").text.rstrip("\n") == vars()["__version__"]):
    	warnings.warn("This API has an Update! https://github.com/ChrxnZ/PG3D-Storage-API/")
except requests.exceptions.ConnectionError:
    print("Unable To Check For Updates: No Internet Connection. Ignoring..")
except requests.exceptions.HTTPError as err:
    print("Unable To Check For Updates: HTTP Error Occured:" + str(err) + ". Ignoring..") 
except requests.exceptions.Timeout as err:
    print("Unable To Check For Updates: Request Timed Out:" + str(err) + ". Ignoring..")
except requests.exceptions.RequestException as err:
    print("Unable To Check For Updates: Request Failed:" + str(err) + ". Ignoring..")



Paths = {
	"LBTXS" : "/storage/emulated/0/Android/data/com.pixel.gun3d/files/lobby_textures/"
}

def getFolderNamesInDIR(Dir):
    return [f for f in os.listdir(Dir) if os.path.isdir(os.path.join(Dir, f))]


def getUsedIdsOnDevice():
	Raw = getFolderNamesInDIR(Paths["LBTXS"])
	Refined = []
	for File in Raw:
		Refine = File[5:]
		Refined.append(Refine)
	return Refined
	
