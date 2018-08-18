"""
(C) Copyright 2018
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
__all__ = ['settings']


# These are settings that are reported by the device when queried.
_REPORTED_SETTINGS = {
####### AIR ASSIST #######
    "AAdc": 204,
    "AAid": 204,  # (int) Air Assist PWM Duty Cycle 0-1023 (Possibly Warm Up Phase)
    "AAil": 1000,
    "AAin": 0,
    "AAix": 0,
    "AAli": 1000,
    "AArd": 0,    # (int) Air Assist PWM Duty Cycle 0-1023 (Likely Run Phase)
    "AArl": 1000,
    "AArn": 0,
    "AArx": 0,
    "AAtv": 3457,
    "AAwd": 0,    # (int) Air Assist PWM Duty Cycle 0-1023 (Possibly Cool Down Phase))
    "AAwl": 1000,
    "AAwn": 0,
    "AAwx": 0,
####### ???????? #######
    "AScm": 0,
    "AShw": "00000000000000000000000000000000000000000000",
####### BOARD ACCEL #######
    "BAdr": 5,     # (int) Board Accel Duration
    "BAfa": 0,
    "BAfo": 0,
    "BAil": 0,
    "BAli": 0,
    "BApc": 500,
    "BApi": 500,
    "BApr": 200,
    "BArl": 0,
    "BAxj": 0,
    "BAxs": 0,
    "BAyj": 0,
    "BAys": 0,
    "BAzj": 0,
    "BAzs": 0,
####### BEAM DETECT #######
    "BDet": 96,    # e t
    "BDie": 0,
    "BDlk": 1966,  # lambda k
    "BDlt": 6553,  # lambda t
    "BDpe": 1,
    "BDtr": 32,    # theta r
    "BDtt": 40,    # theta t
####### ???????? #######
    "BLev": 0,
    "BLva": 0,
    "BLvb": 0,
    "BLvc": 0,
####### BOARD TEMP #######
    "BTin": -2147483648,
    "BTix": 2147483647,
    "BTli": 1000,  # (int) Board Temp - Logging interval
    "BTpd": 5000,  # (int) Board Temp - Period
    "BTrn": -2147483648,
    "BTrx": 2147483647,
    "BTvl": 2752,
    "BTwn": -2147483648,
    "BTwx": 2147483647,
####### ???????? #######
    "CAid": 0,
    "CAwb": 0,
####### ???????? #######
    "CCbp": 0,
    "CCbt": 0,
    "CCfl": 0,
    "CCml": 0,
    "CCst": 2,
    "CCxp": 0,
    "CCyp": 0,
    "CCzp": 0,
####### ???????? #######
    "CDcb": 1,
    "CDsd": 300000,
    "CDtb": 23,
####### ???????? #######
    "CFrh": 0,
####### ???????? #######
    "CMdt": 26617,
    "CMen": 1,
    "CMhl": 1000,
    "CMhu": 1000,
    "CMin": 10000,
    "CMix": 30000,
    "CMpf": 0,
    "CMpn": 0,
    "CMrn": 5000,
    "CMrx": 35000,
    "CMsf": 0,
    "CMsm": 1,
    "CMso": 0.0093713738,
    "CMsp": 0,
    "CMto": 0,
    "CMwn": 5000,
    "CMwx": 35000,
####### EXHAUST FAN #######
    "EFdc": 0,
    "EFid": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Possibly Warm Up Phase))
    "EFil": 1000,
    "EFin": 0,
    "EFix": 0,
    "EFli": 1000,
    "EFrd": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Likely Run Phase))
    "EFrl": 1000,
    "EFrn": 0,
    "EFrx": 0,
    "EFtv": 0,
    "EFwd": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Possibly Cool down Phase))
    "EFwl": 1000,
    "EFwn": 0,
    "EFwx": 0,
####### ???????? #######
    "FCsn": 0,
####### FILTER EXHAUST #######
    "FEdc": 0,
    "FEid": 0,
    "FEil": 0,
    "FEin": 0,
    "FEix": 0,
    "FEli": 0,
    "FErd": 0,
    "FErl": 0,
    "FErn": 0,
    "FErx": 0,
    "FEta": 0,
    "FEtb": 0,
    "FEtc": 0,
    "FEtd": 0,
    "FEwd": 0,
    "FEwl": 0,
    "FEwn": 0,
    "FEwx": 0,
####### FILTER INPUT #######
    "FIdc": 0,
    "FIid": 0,
    "FIil": 0,
    "FIin": 0,
    "FIix": 0,
    "FIli": 0,
    "FIrd": 0,
    "FIrl": 0,
    "FIrn": 0,
    "FIrx": 0,
    "FIta": 0,
    "FItb": 0,
    "FItc": 0,
    "FItd": 0,
    "FIwd": 0,
    "FIwl": 0,
    "FIwn": 0,
    "FIwx": 0,
####### ???????? #######
    "FPdc": 0,
    "FPid": 0,
    "FPil": 0,
    "FPin": 0,
    "FPix": 0,
    "FPli": 0,
    "FPrd": 0,
    "FPrl": 0,
    "FPrn": 0,
    "FPrx": 0,
    "FPtv": 0,
    "FPwd": 0,
    "FPwl": 0,
    "FPwn": 0,
    "FPwx": 0,
####### ???????? #######
    "FSli": 0,
    "FSpv": 0,
    "FStv": 0,
####### ???????? #######
    "FUsn": 0,
####### ???????? #######
    "FVer": 0,
####### HEAD ACCEL #######
    "HAdr": 5,     # (int) Head Accel Duration
    "HAfa": 0,
    "HAfo": 0,
    "HAil": 0,
    "HAli": 0,
    "HApc": 500,
    "HApi": 500,
    "HApr": 200,
    "HArl": 100,
    "HAxj": 0,
    "HAxs": 0,
    "HAyj": 0,
    "HAys": 0,
    "HAzj": 0,
    "HAzs": 0,
####### HEAD CAM #######
    "HCae": 0,       # (int) Head Cam - Auto Exposure
    "HCag": 0,       # (int) Head Cam - Auto Gain
    "HCaw": 2,       # (int) Head Cam - Auto White Balance
    "HCbb": 1400,    # (int) Head Cam - Blue Balance
    "HCex": 3000,    # (int) Head Cam - Exposure
    "HCga": 30,      # (int) Head Cam - Gain
    "HChf": 1,       # (int) Head Cam - Horizontal Flip
    "HCrb": 1100,    # (int) Head Cam - Red Balance
    "HCvf": 0,       # (int) Head Cam - Vertical Flip
####### HEAD #######
    "HEfv": {'cfg': 'MACHINE.HEAD_FIRMWARE', 'type': int()},  # (int) Head Firmware Version
    "HEhl": 0,
    "HEid": 1100,
    "HEsn": {'cfg': 'MACHINE.HEAD_SERIAL', 'type': int()},  # (int) Head Serial Number
    "HEua": 841174597,
    "HEub": 5472275,
    "HEuc": 19,
    "HEul": 0,
    "HEwl": 0,
####### HEAD TEMP #######
    "HTin": -2147483648,
    "HTix": 2147483647,
    "HTli": 1000,        # (int) Board Temp - Logging interval (ms)
    "HTpd": 5000,        # (int) Head Temp - Period (ms)
    "HTrn": -2147483648,
    "HTrx": 2147483647,
    "HTvl": 768,
    "HTwn": -2147483648,
    "HTwx": 2147483647,
####### ???????? #######
    "HVcr": 0,
    "HVli": 0,
    "HVvo": 0,
####### ???????? #######
    "IAid": 0,
####### INTAKE FAN #######
    "IFdc": 0,
    "IFid": 0,    # (int) Intake Fan PWM Duty Cycle 0-65535 (Possibly Warm Up Phase))
    "IFil": 1000,
    "IFin": 0,
    "IFix": 0,
    "IFli": 1000,
    "IFrd": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Likely Run Phase))
    "IFrl": 1000,
    "IFrn": 0,
    "IFrx": 0,
    "IFta": 40882666,
    "IFtb": 40424667,
    "IFwd": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Possibly Cool down Phase))
    "IFwl": 1000,
    "IFwn": 0,
    "IFwx": 0,
####### ???????? #######
    "IMjq": 40,
####### ???????? #######
    "IRli": 0,
    "IRva": 32,
    "IRvb": 32,
    "IRvc": 35,
    "IRvd": 36,
####### INTERCONNECT TEMP #######
    "ITin": -2147483648,
    "ITix": 2147483647,
    "ITli": 1000,        # (int) Interconnect Temp - Logging interval (ms)
    "ITpd": 5000,        # (int) Interconnect Temp - Logging interval (ms)
    "ITrn": -2147483648,
    "ITrx": 2147483647,
    "ITvl": 7904,
    "ITwn": -2147483648,
    "ITwx": 2147483647,
####### LID ACCEL #######
    "LAdr": 5,    # (int) Lid Accel Duration
    "LAfa": 0,
    "LAfo": 0,
    "LAil": 0,
    "LAli": 0,
    "LApc": 500,
    "LApi": 500,
    "LApr": 200,
    "LArl": 0,
    "LAxj": 0,
    "LAxs": 0,     # (int) Lid Accel X-Axis
    "LAyj": 0,
    "LAys": 0,     # (int) Lid Accel Y-Axis
    "LAzj": 0,
    "LAzs": 0,     # (int) Lid Accel Z-Axis
####### LID CAMERA #######
    "LCae": 0,     # (int) Lid Cam - Auto Exposure
    "LCag": 0,     # (int) Lid Cam - Auto Gain
    "LCaw": 2,     # (int) Lid Cam - Auto White Balance
    "LCbb": 1400,  # (int) Lid Cam - Blue Balance
    "LCex": 3000,  # (int) Lid Cam - Exposure
    "LCfl": 0,     # (int) Lid Cam - Flash On
    "LCga": 30,    # (int) Lid Cam - Gain
    "LChf": 1,     # (int) Lid Cam - Horizontal Flip
    "LCrb": 1100,  # (int) Lid Cam - Red Balance
    "LCvf": 0,     # (int) Lid Cam - Vertical Flip
####### LID LED #######
    "LLbi": 101,   # (int) Lid LED Brightness - ?
    "LLbo": 45,    # (int) Lid LED Brightness - Open
    "LLbr": 101,   # (int) Lid LED Brightness - ?
    "LLbw": 101,   # (int) Lid LED Brightness - ?
    "LLsp": 28,    # (int) Lid LED Speed
    "LLvl": 101,   # (int) Lid LED Brightness - ?
####### LID TEMP #######
    "LTin": -2147483648,
    "LTix": 2147483647,
    "LTli": 1000,        # (int) Lid Temp - Logging interval
    "LTpd": 5000,        # (int) Lid Temp - Period
    "LTrn": -2147483648,
    "LTrx": 2147483647,
    "LTvl": 0,
    "LTwn": -2147483648,
    "LTwx": 2147483647,
####### MACHINE CONTROL #######
    "MCbc": 1,      # (int) Boot attempts
    "MCbf": 1,      # (int) Boot Flags (1 - power-on, 2 - software reset, )
    "MCbr": 320,    # (int) Manufacturing Info ??
    "MCbu": 20576,  # (int) Boot Fuses 0x00005060
    "MCcl": 1000,   # (int) CPU Temp - Logging Interval
    "MCcn": 0,
    "MCcp": 5000,   # (int) CPU Temp - Period
    "MCct": 49156,
    "MCcx": 65000,
    "MCdb": 0,
    "MCds": 0,
    "MCdt": {'data': 'epoch', 'type': int()},  # (int) Machine Clock time as Linux Epoch
    "MCdv": {'cfg': 'MACHINE.APP_VERSION', 'type': str()},  # (str) Version string from 'glowforge' service.  Search for 'This may indicate a hardware failure.' in executable.  It begins around 10 bytes after.
    "MCip": {'cfg': 'MACHINE.IP_ADDRESS', 'type': str()},  # (str) IP Address
    "MCla": 0.13574219,
    "MClb": 0.032226562,
    "MClc": 0.010742188,
    "MCld": 0,
    "MCma": 0,
    "MCmi": 0,
    "MCov": {'cfg': 'MACHINE.FIRMWARE', 'type': str()},  # (str) Firmware version string.  Typically in <MAJOR>.<MINOR>.<REVISION>-<BUILD> format.
    "MCpt": 4,
    "MCrc": 2,
    "MCsn": {'cfg': 'MACHINE.SERIAL', 'type': int()},  # (int) Serial Number
    "MCsw": 27,
    "MCtc": 0,
    "MCut": 0.26666668,
####### PURGE AIR #######
    "PAcc": 853,
    "PAcm": 0,
    "PAli": 1000,  # (int) Purge Air - Logging Interval
    "PAon": 1,     # (int) Purge Air - On
    "PApd": 1000,  # (int) Purge Air - PWM Period
####### PIC ID #######
    "PCid": 19795,  #SM found in slot 0
####### ???????? #######
    "PRcp": 2.875,
    "PRfc": 0,
    "PRlc": 0,
    "PRls": 0,
    "PRnt": 12,
    "PRrs": 11206656,
    "PRsc": 1,
    "PRvs": 141811712,
####### POWER TEMP #######
    "PTli": 1000,       # (int) Power Temp - Logging Interval
    "PTmn": 0,          # (int) Power Temp - Min
    "PTmx": 4294967295, # (int) Power Temp - Max
    "PTpd": 5000,       # (int) Power Temp - Period
    "PTvl": 628,
####### ???????? #######
    "RAid": 0,
####### ???????? #######
    "SAid": 3116292,
####### ???????? #######
    "TCli": 1000,
    "TCon": 0,
    "TCth": 2147483647,
####### ???????? #######
    "UAid": 0,
####### ???????? #######
    "ULst": 0,
####### WATER PUMP #######
    "WPon": 1,  # (int) Water Pump - On
####### ???????? #######
    "WSst": 0,
####### WATER TEMPERATURE #######
    "WTva": 638,
    "WTvb": 639,
####### X-STEPPER #######
    "XScc": 33,  # (int) X Stepper Current (not sure which)
    "XSdm": 1,   # (int) X Stepper Decay Mode
    "XShc": 33,  # (int) X Stepper Hold Current
    "XSmm": 1,   # (int) X Stepper Microstepping Mode
    "XSrc": 0,   # (int) X Stepper Run Current
####### Y-STEPPER #######
    "YScc": 5,   # (int) Y Stepper Current (not sure which)
    "YSdm": 1,   # (int) Y Stepper Decay Mode
    "YShc": 5,   # (int) Y Stepper Hold Current
    "YSmm": 1,   # (int) Y Stepper Microstepping Mode
    "YSrc": 0,   # (int) Y Stepper Run Current
####### Z-STEPPER #######
    "ZHin": 180, # (int) Z homing step interval (ms)
    "ZScc": 1,   # (int) Z Stepper Current (not sure which)
    "ZSen": 0,   # (int) Z Stepper Enable
    "ZShc": 1,   # (int) Z Stepper Hold Current
    "ZSrc": 0    # (int) Z Stepper Run Current
}


_MOTION_SETTINGS = {

####### AIR-ASSIST #######
    "AAid": 'Warm up Air Assist PWM',
    "AAin": None,
    "AAix": None,
    "AArd": 'Run Air Assist PWM',
    "AArn": None,
    "AArx": None,
    "AAwd": 'Cool down Air Assist PWM',
    "AAwn": None,
    "AAwx": None,
####### BOARD TEMP #######
    "BTrn": None,
    "BTrx": None,
    "BTwn": None,
    "BTwx": None,
####### ?????????? #######
    "CCrp": None,
####### ?????????? #######
    "CFrh": None,
####### ?????????? #######
    "CMin": None,
    "CMix": None,
    "CMrn": None,
    "CMrx": None,
    "CMwn": None,
    "CMwx": None,
####### EXHAUST FAN #######
    "EFid": 'Warm up Exhaust PWM',
    "EFin": None,
    "EFix": None,
    "EFrd": 'Run Exhaust PWM',
    "EFrn": None,
    "EFrx": None,
    "EFwd": 'Cool down Exhaust PWM',
    "EFwn": None,
    "EFwx": None,
####### ??????????? #######
    "FEid": None,
    "FErd": None,
    "FEwd": None,
####### ??????????? #######
    "FPid": None,
    "FPrd": None,
    "FPwd": None,
####### HEAD TEMP #######
    "HTrn": None,
    "HTrx": None,
    "HTwn": None,
    "HTwx": None,
####### INTAKE FAN #######
    "IFid": 'Warm up Intake PWM',
    "IFin": None,
    "IFix": None,
    "IFrd": 'Run Intake PWM',
    "IFrn": None,
    "IFrx": None,
    "IFwd": 'Cool down Intake PWM',
    "IFwn": None,
    "IFwx": None,
####### LID TEMP #######
    "LTrn": None,
    "LTrx": None,
    "LTwn": None,
    "LTwx": None,
####### MACHINE CONTROL #######
    "MCsn": 'Device Serial Number',
####### PIC ID #######
    "PCid": 'PIC Version ID',  # This seems to match the value reported in the settings by the device
####### ???????? #######
    "PDct": None,
    "PDfm": None,
####### POWER TEMP #######
    "PTmn": 'Power Temp Min',
    "PTmx": 'Power Temp Max',
####### STEP File RATE #######
    "STfr": 'Step Frequency',
####### X-STEPPER #######
    "XSdm": 'X Decay Mode',
    "XShc": 'X Hold Current',
    "XSmm": 'X Microstep Mode',
    "XSrc": 'X Run Current',
####### Y-STEPPER #######
    "YSdm": 'Y Decay Mode',
    "YShc": 'Y Hold Current',
    "YSmm": 'Y Microstep Mode',
    "YSrc": 'Y Run Current',

}


"""
These are settings that have been observed in actions, but not in MOTION or device reports:

HCil: Head Cam Illumination  - This setting is set to 1072693248 (3FF00000) to turn on the laser.

"""
