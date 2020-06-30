######################################################################################################
# @file CallBackDemo.py
# @copyright HighFinesse GmbH.
# @author Lovas Szilard <lovas@highfinesse.de>
# @date 2018.09.16
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#
# @brief Python language example for demonstrating usage of wlmData.dll CallBack mechanism.
# Tested with Python 3.7.
# 64-bit Python requires 64-bit wlmData.dll (in System32 folder) and
# 32-bit Python requires 32-bit wlmData.dll (in SysWOW64 folder on Win64 or System32 folder on Win32).
# For more information see the ctypes module documentation:
# https://docs.python.org/3/library/ctypes.html
# and/or WLM manual.pdf
#
# Changelog:
# ----------
# 2018.09.16
# v0.1 - Initial release
#

# wlmData.dll related imports
import wlmData
import wlmConst

# others
import sys
import time

# Set the DLL_PATH variable according to your environment here:
DLL_PATH = "C:\Windows\System32\wlmData.dll"

# Set the Data acquisition time (sec) here:
DATA_ACQUISITION_TIME = 5

# Set the CallBack Thread priority here:
CALLBACK_THREAD_PRIORITY = 2

# Create callback function type using stdcall (WINFUNCTYPE) calling convention.
# The original function signature is void function(long, unsigned long, double)
# For more information see ctypes python library documentation.
CallBackFuncType = wlmData.ctypes.WINFUNCTYPE(None, wlmData.ctypes.c_long, wlmData.ctypes.c_ulong, wlmData.ctypes.c_double)

# Function definition for CallBack function
def MyCallBack(Mode, IntVal, DblVal):
    if Mode == wlmConst.cmiWavelength1:
        print("Ch1 wawelength (vac): %f nm" % DblVal);
    elif Mode == wlmConst.cmiWavelength2:
        print("Ch2 wawelength (vac): %f nm" % DblVal);
    elif Mode == wlmConst.cmiWavelength3:
        print("Ch3 wawelength (vac): %f nm" % DblVal);
    elif Mode == wlmConst.cmiWavelength4:
        print("Ch4 wawelength (vac): %f nm" % DblVal);
    elif Mode == wlmConst.cmiWavelength5:
        print("Ch5 wawelength (vac): %f nm" % DblVal);
    elif Mode == wlmConst.cmiWavelength6:
        print("Ch6 wawelength (vac): %f nm" % DblVal);
    elif Mode == wlmConst.cmiWavelength7:
        print("Ch7 wawelength (vac): %f nm" % DblVal);
    elif Mode == wlmConst.cmiWavelength8:
        print("Ch8 wawelength (vac): %f nm" % DblVal);

# Main program execution starts here
# Load DLL from DLL_PATH
try:
    wlmData.LoadDLL(DLL_PATH)
except:
    sys.exit("Error: Couldn't find DLL on path %s.\nPlease check the DLL_PATH variable!" % DLL_PATH)

# Checks the number of WLM server instance(s)
if wlmData.dll.GetWLMCount(0) == 0:
    print("There is no running wlmServer instance(s).")
else:
    # Creates function pointer to the CallBackFuncType type-casted function
    pCallBackFunction = CallBackFuncType(MyCallBack)

    print("Data acquisition by Callback function for %s seconds." % DATA_ACQUISITION_TIME)

    # Installs CallBack function
    # The tricky part: Casting pCallBackFunction to long pointer (long *)
    wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyInstallCallback, wlmData.ctypes.cast(pCallBackFunction, wlmData.ctypes.POINTER(wlmData.ctypes.c_long)), CALLBACK_THREAD_PRIORITY)

    # Gives a little time for data acquisition
    time.sleep(DATA_ACQUISITION_TIME)

    # Removes CallBack function
    wlmData.dll.Instantiate(wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, None, 0)

    print("CallBack function was removed.")

