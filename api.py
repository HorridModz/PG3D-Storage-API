__author__ = "ChrxnZX | Pulsed#1874 + HorridModz | User123456789#6424"
__version__ = "2.0.0"
ignoreversion = "2.0.0"
updatechecking = True

import os
import sys
import re

_importsuccess = False
# Method 1
try:
    import requests
except ModuleNotFoundError:
    _importsuccess = False
else:
    _importsuccess = True
# Method 2
if not _importsuccess:
    try:
        import pip
        pip.main(["install", "requests"])
        import requests
    except Exception:
        _importsuccess = False
    else:
        _importsuccess = True
# Method 3
if not _importsuccess:
    try:
        import subprocess
        subprocess.call("pip install requests")
        import requests
    except Exception:
        _importsuccess = False
    else:
        _importsuccess = True
# Method 4
if not _importsuccess:
    try:
        import subprocess
        subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    except Exception:
        _importsuccess = False
    else:
        _importsuccess = True
del _importsuccess


def _getrequest(link, errormessage=None):
    if "requests" in globals():
        try:
            response = requests.get(link)
        except requests.exceptions.ConnectionError:
            if errormessage is not None:
                print(f"{errormessage}: No internet connection.")
        except requests.exceptions.HTTPError as err:
            if errormessage is not None:
                print(f"{errormessage}: HTTP error occurred during request to {link}: {str(err)}.")
        except requests.exceptions.Timeout as err:
            if errormessage is not None:
                print(f"{errormessage}: Request to {link} timed Out: {str(err)}.")
        except Exception as err:
            if errormessage is not None:
                print(f"{errormessage}: Request to {link} failed: {str(err)}.")
    else:
        if errormessage is not None:
            print(f"{errormessage}: Failed to import requests module.")
    if "response" in locals() and response.status_code != 200:
        if errormessage is not None:
            print(f"{errormessage}:"
                  f" {link}"
                  " returned http status code"
                  f" {str(response.status_code)}")
    return (response.status_code == 200, response.text) if "response" in locals() else (None, None)


def checkforupdates():
    def _ignoreversion(version):
        with open(__file__, 'w') as f:
            new = re.sub("\nignoreversion = .*\n", f"\nignoreversion = \"{version}\"\n", currentcode)
            f.write(new)

    def _update():
        success, text = _getrequest("https://raw.githubusercontent.com/ChrxnZ/PG3D-Storage-API/main/api.py",
                                    errormessage=None)
        if success:
            with open(__file__, 'w') as f:
                f.write(text)
        else:
            raise requests.exceptions.RequestException(
                "Request to https://raw.githubusercontent.com/ChrxnZ/PG3D-Storage-API/main/api.py failed.")

    # End of _update() function
    success, text = _getrequest("https://raw.githubusercontent.com/ChrxnZ/PG3D-Storage-API/main/Info/currentVer.txt",
                                errormessage=None)
    if success:
        cloudversion = text.strip()
        if not (cloudversion == __version__ or cloudversion == ignoreversion):
            print("PG3D API has an update! https://github.com/ChrxnZ/PG3D-Storage-API/")
            toupdate = input("Would you like to update it? (Y/N):")
            if toupdate.strip().lower() == "y":
                with open(__file__, 'r') as f:
                    currentcode = f.read()
                try:
                    _update()
                except Exception as err:
                    print("Update failed: " + str(err))
                    try:
                        with open(__file__, 'r+') as f:
                            if f.read() != currentcode:
                                print("PG3D API has been corrupted. Attempting to repair...")
                                try:
                                    f.write(currentcode)
                                except Exception:
                                    print("Failed to repair PG3D API.")
                                else:
                                    print("Successfully repaired PG3D API.")
                    except Exception:
                        pass
                else:
                    print("Successfully updated PG3D API! Rerun the api.")
                    sys.exit()
            else:
                toignore = input("Would you like to permanently ignore this version? (Y/N):")
                if toignore.strip().lower() == "y":
                    with open(__file__, 'r') as f:
                        currentcode = f.read()
                    try:
                        _ignoreversion(cloudversion)
                    except Exception as err:
                        print("Failed to permanently ignore this version: " + str(err))
                        try:
                            with open(__file__, 'r+') as f:
                                if f.read() != currentcode:
                                    print("PG3D API has been corrupted. Attempting to repair...")
                                    try:
                                        f.write(currentcode)
                                    except Exception:
                                        print("Failed to repair PG3D API.")
                                    else:
                                        print("Successfully repaired PG3D API.")
                        except Exception:
                            pass
                    else:
                        print("Successfully ignored this version! Rerun PG3D API.")
                        sys.exit()
        else:
            print("No updates found")


_Paths = {
    "PG3DRoot": "/storage/emulated/0/Android/data/com.pixel.gun3d",
    "LBTXS": "/storage/emulated/0/Android/data/com.pixel.gun3d/files/lobby_textures/",
}


def detect_android():
    from os import environ
    return 'ANDROID_BOOTLOGO' in environ


def _getFolderNamesInDIR(Dir):
    return [f for f in os.listdir(Dir) if os.path.isdir(os.path.join(Dir, f))]


def getUsedIdsOnDevice():
    if not os.path.isdir(_Paths["PG3DRoot"]):
        raise FileNotFoundError(f"Could not find {_Paths['PG3DRoot']}. Is Pixel Gun 3D installed?")
    if not os.path.isdir(_Paths["LBTXS"]):
        raise FileNotFoundError(f"Could not find {_Paths['LBTXS']}.")
    try:
        return [file[5:] for file in _getFolderNamesInDIR(_Paths["LBTXS"])]
    except PermissionError:
        raise PermissionError("Could not access {Paths['LBTXS']}. Is your device rooted?")


def _disableupdatechecking():
    with open(__file__, 'w') as f:
        new = currentcode.replace("\nupdatechecking = True\n", "\nupdatechecking = False\n")
        f.write(new)


# if updatechecking:
    # tocheckforupdates = input("Would you like to check for updates? (Y/N):")
    # if tocheckforupdates.strip().lower() == "y":
        # checkforupdates()
    # else:
        # todisable = input("Would you like to permanently disable update checking? (Y/N):")
        # if todisable.strip().lower() == "y":
            # with open(__file__, 'r') as f:
                # currentcode = f.read()
            # try:
                # _disableupdatechecking()
            # except Exception as err:
                # print("Failed to permanently disable update checking: " + str(err))
                # try:
                    # with open(__file__, 'r+') as f:
                        # if f.read() != currentcode:
                            # print("PG3D API has been corrupted. Attempting to repair...")
                            # try:
                                # f.write(currentcode)
                            # except Exception:
                                # print("Failed to repair PG3D API.")
                            # else:
                                # print("Successfully repaired PG3D API.")
                # except Exception:
                    # pass
            # else:
                # print("Successfully disabled update checking! Rerun PG3D API.")
                # sys.exit()
checkforupdates()
if not detect_android():
    raise RuntimeError("PG3D API is only for Android devices!")
if __name__ == "__main__":
    print(getUsedIdsOnDevice())
