######################################################################################################
# @file DataDemo.py
# @copyright HighFinesse GmbH.
# @author Lovas Szilard <lovas@highfinesse.de>
# @date 2018.09.15
# @version 0.1
#
# Homepage: http://www.highfinesse.com/
#
# @brief Python language example for demonstrating usage of
# wlmData.dll Set/Get function calls.
# Tested with Python 3.7. 64-bit Python requires 64-bit wlmData.dll and
# 32-bit Python requires 32-bit wlmData.dll.
# For more information see ctypes module documentation:
# https://docs.python.org/3/library/ctypes.html
# and/or WLM manual.pdf
#
# Changelog:
# ----------
# 2018.09.15
# v0.1 - Initial release
#

# wlmData.dll related imports
import wlmData
import wlmConst

# others
import sys

#########################################################
# Set the DLL_PATH variable according to your environment
#########################################################
DLL_PATH = "C:\\Windows\System32\wlmData.dll"


# Load DLL from DLL_PATH
try:
    wlmData.LoadDLL(DLL_PATH)
except:
    sys.exit("Error: Couldn't find DLL on path %s. Please check the DLL_PATH variable!" % DLL_PATH)

# Checks the number of WLM server instance(s)
# 此处更改过！！！！
# Read Type, Version, Revision and Build number

Version_type = wlmData.dll.GetWLMVersion(0)
Version_ver = wlmData.dll.GetWLMVersion(1)
Version_rev = wlmData.dll.GetWLMVersion(2)
Version_build = wlmData.dll.GetWLMVersion(3)
print("WLM Version: [%s.%s.%s.%s]" % (Version_type, Version_ver, Version_rev, Version_build))

# Read frequency
Frequency = wlmData.dll.GetFrequency(0.0)
if Frequency == wlmConst.ErrWlmMissing:
    StatusString = "WLM inactive"
elif Frequency == wlmConst.ErrNoSignal:
    StatusString = 'No Signal'
elif Frequency == wlmConst.ErrBadSignal:
   StatusString = 'Bad Signal'
elif Frequency == wlmConst.ErrLowSignal:
    StatusString = 'Low Signal'
elif Frequency == wlmConst.ErrBigSignal:
    StatusString = 'High Signal'
else:
    StatusString = 'WLM is running'

print("Status: %s" % StatusString)

# Read temperaure
Temperature = wlmData.dll.GetTemperature(0.0)
if Temperature <= wlmConst.ErrTemperature:
    print("Temperature: Not available")
else:
    print("Temperature: %.1f °C" % Temperature)

# Read Pressure
Pressure = wlmData.dll.GetPressure(0.0)
if Pressure <= wlmConst.ErrTemperature:
    print("Pressure: Not available")
else:
    print("Pressure: %.1f mbar" % Pressure)

# Read exposure of CCD arrays
Exposure = wlmData.dll.GetExposure(0)
if Exposure == wlmConst.ErrWlmMissing:
    print("Exposure: WLM not active")
elif Exposure == wlmConst.ErrNotAvailable:
    print("Exposure: not available")
else:
    print("Exposure: %d ms" % Exposure)

# Read Ch1 Exposure mode
ExpoMode = wlmData.dll.GetExposureMode(False)
if ExpoMode == 1:
    print("Ch1 Exposure: Auto")

# Read Pulse Mode settings
PulseMode = wlmData.dll.GetPulseMode(0)
if PulseMode == 0:
    PulseModeString = "Continuous Wave (cw) laser"
elif PulseMode == 1:
    PulseModeString = "Standard / Single / internally triggered pulsed"
elif PulseMode == 2:
    PulseModeString = "Double / Externally triggered pulsed"
else:
    PulseModeString = "Other"
print("Pulse mode: %s" %PulseModeString)

# Read Precision (Wide/Fine)
Precision = wlmData.dll.GetWideMode(0)
if Precision == 0:
    PrecisionString = "Fine"
elif Precision == 1:
    PrecisionString = "Wide"
else:
    PrecisionString = "Function not available"
print("Precision: %s" %PrecisionString)

# Print out Frequency
if Frequency == wlmConst.ErrOutOfRange:
    print("Ch1 Error: Out of Range")
elif Frequency <= 0:
    print("Ch1 Error code: %d" % Frequency)
else:
    print("Ch1 Frequency: %f THz" % Frequency)


'''
if wlmData.dll.GetWLMCount(0) != 0:
    print("There is no running wlmServer instance(s).")
else:
    # Read Type, Version, Revision and Build number
    Version_type = wlmData.dll.GetWLMVersion(0)
    Version_ver = wlmData.dll.GetWLMVersion(1)
    Version_rev = wlmData.dll.GetWLMVersion(2)
    Version_build = wlmData.dll.GetWLMVersion(3)
    print("WLM Version: [%s.%s.%s.%s]" % (Version_type, Version_ver, Version_rev, Version_build))

    # Read frequency
    Frequency = wlmData.dll.GetFrequency(0.0)
    if Frequency == wlmConst.ErrWlmMissing:
        StatusString = "WLM inactive"
    elif Frequency == wlmConst.ErrNoSignal:
        StatusString = 'No Signal'
    elif Frequency == wlmConst.ErrBadSignal:
       StatusString = 'Bad Signal'
    elif Frequency == wlmConst.ErrLowSignal:
        StatusString = 'Low Signal'
    elif Frequency == wlmConst.ErrBigSignal:
        StatusString = 'High Signal'
    else:
        StatusString = 'WLM is running'

    print("Status: %s" % StatusString)

    # Read temperaure
    Temperature = wlmData.dll.GetTemperature(0.0)
    if Temperature <= wlmConst.ErrTemperature:
        print("Temperature: Not available")
    else:
        print("Temperature: %.1f °C" % Temperature)

    # Read Pressure
    Pressure = wlmData.dll.GetPressure(0.0)
    if Pressure <= wlmConst.ErrTemperature:
        print("Pressure: Not available")
    else:
        print("Pressure: %.1f mbar" % Pressure)

    # Read exposure of CCD arrays
    Exposure = wlmData.dll.GetExposure(0)
    if Exposure == wlmConst.ErrWlmMissing:
        print("Exposure: WLM not active")
    elif Exposure == wlmConst.ErrNotAvailable:
        print("Exposure: not available")
    else:
        print("Exposure: %d ms" % Exposure)

    # Read Ch1 Exposure mode
    ExpoMode = wlmData.dll.GetExposureMode(False)
    if ExpoMode == 1:
        print("Ch1 Exposure: Auto")

    # Read Pulse Mode settings
    PulseMode = wlmData.dll.GetPulseMode(0)
    if PulseMode == 0:
        PulseModeString = "Continuous Wave (cw) laser"
    elif PulseMode == 1:
        PulseModeString = "Standard / Single / internally triggered pulsed"
    elif PulseMode == 2:
        PulseModeString = "Double / Externally triggered pulsed"
    else:
        PulseModeString = "Other"
    print("Pulse mode: %s" %PulseModeString)

    # Read Precision (Wide/Fine)
    Precision = wlmData.dll.GetWideMode(0)
    if Precision == 0:
        PrecisionString = "Fine"
    elif Precision == 1:
        PrecisionString = "Wide"
    else:
        PrecisionString = "Function not available"
    print("Precision: %s" %PrecisionString)

    # Print out Frequency
    if Frequency == wlmConst.ErrOutOfRange:
        print("Ch1 Error: Out of Range")
    elif Frequency <= 0:
        print("Ch1 Error code: %d" % Frequency)
    else:
        print("Ch1 Frequency: %f THz" % Frequency)



'''