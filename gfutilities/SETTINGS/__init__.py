"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
__all__ = ['settings']


# These are settings that are reported by the device when queried.
_REPORTED_SETTINGS = {
####### AIR ASSIST #######
    "AAdc": 204,
    "AAfc": 536870912,
    "AAid": 204,  # (int) Air Assist PWM Duty Cycle 0-1023 (Possibly Warm Up Phase)
    "AAil": 1000,
    "AAin": 0,
    "AAix": 0,
    "AAli": 1000,
    "AArd": 0,    # (int) Air Assist PWM Duty Cycle 0-1023 (Likely Run Phase)
    "AArl": 1000,
    "AArn": 0,
    "AArx": 0,
    "AAsd": 0,
    "AAsl": 1000,
    "AAsn": 0,
    "AAsx": 0,
    "AAtv": 3457,
    "AAwd": 0,    # (int) Air Assist PWM Duty Cycle 0-1023 (Possibly Cool Down Phase))
    "AAwl": 1000,
    "AAwn": 0,
    "AAwx": 0,
####### ???????? #######
    "AScm": 0,
    "AShw": "00000000000000000000000000000000000000000000",
####### BOARD ACCEL #######
    "BAai": 0,
    "BAar": 0,
    "BAdb": 5,
    "BAdl": 5,
    "BAfa": 0,
    "BAfo": 0,
    "BAil": 0,
    "BAli": 0,
    "BApc": 500,
    "BApi": 500,
    "BApr": 200,
    "BArl": 0,
    "BAsi": 2,
    "BAsr": 2,
    "BAxi": 0,
    "BAxr": 0,
    "BAyi": 0,
    "BAyr": 0,
    "BAzi": 0,
    "BAzr": 0,
####### BEAM DETECT #######
    "BDet": 96,    # e t
    "BDie": 0,
    "BDlk": 1966,  # lambda k
    "BDlt": 6553,  # lambda t
    "BDpe": 0,
    "BDtr": 32,    # theta r
    "BDtt": 40,    # theta t
####### ???????? #######
    "BLev": 0,
    "BLva": 0,
    "BLvb": 0,
    "BLvc": 0,
####### BOARD TEMP #######
    "BTcx": 2147483647,
    "BTfc": 0,
    "BTfo": 0,
    "BTin": -2147483648,
    "BTix": 2147483647,
    "BTli": 1000,  # (int) Board Temp - Logging interval
    "BTpd": 5000,  # (int) Board Temp - Period
    "BTrn": -2147483648,
    "BTrx": 2147483647,
    "BTvl": 2752,
    "BTwn": -2147483648,
    "BTwx": 2147483647,
    "BTxb": 0,
####### ???????? #######
    "CAid": 0,
    "CAwb": 0,
####### ???????? #######
    "CCbp": 0,
    "CCbt": 0,
    "CCfl": 0,
    "CCml": 0,
    "CCpb": 200000,
    "CCro": 5000,
    "CCst": 2,
    "CCup": 0,
    "CCxp": 0,
    "CCyp": 0,
    "CCzp": 0,
####### ???????? #######
    "CDcb": 0,
    "CDcc": 1,
    "CDsb": 0,
    "CDtb": 0,
####### ???????? #######
    "CFdn": 0,
    "CFdt": 0,
    "CFdx": 0,
    "CFen": 0,
    "CFer": 0,
    "CFex": 0,
    "CFhp": 0,
    "CFhs": 0,
    "CFhw": 0,
    "CFhx": 0,
    "CFki": 0,
    "CFkp": 0,
    "CFli": 0,
    "CFpd": 0,
    "CFpp": 0,
    "CFps": 1,
    "CFrh": 0,
    "CFsp": 0,
####### ???????? #######
    "CMdt": 18364,
    "CMet": 18134,
    "CMin": 4008,
    "CMix": 50010,
    "CMli": 100,
    "CMpd": 1000,
    "CMrn": 1017,
    "CMrx": 31040,
    "CMts": 0,
    "CMup": 100,
    "CMut": 18134,
    "CMwn": 1017,
    "CMwx": 31040,
####### ???????? #######
    "CTin": 391,
    "CTix": 935,
    "CTrn": 591,
    "CTrx": 971,
    "CTwn": 591,
    "CTwx": 971,
####### EXHAUST FAN #######
    "EFdc": 0,
    "EFfc": 536870912,
    "EFid": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Possibly Warm Up Phase))
    "EFil": 1000,
    "EFin": 0,
    "EFix": 0,
    "EFli": 1000,
    "EFrd": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Likely Run Phase))
    "EFrl": 1000,
    "EFrn": 0,
    "EFrx": 0,
    "EFsd": 0,
    "EFsl": 1000,
    "EFsn": 0,
    "EFsx": 0,
    "EFtv": 0,
    "EFwd": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Possibly Cool down Phase))
    "EFwl": 1000,
    "EFwn": 0,
    "EFwx": 0,
####### ???????? #######
    "FAdc": 0,
    "FAfc": 0,
    "FAid": 0,
    "FAil": 0,
    "FAin": 0,
    "FAix": 0,
    "FAli": 0,
    "FArd": 0,
    "FArl": 0,
    "FArn": 0,
    "FArx": 0,
    "FAtv": 0,
    "FAwd": 0,
    "FAwl": 0,
    "FAwn": 0,
    "FAwx": 0,
####### FILTER EXHAUST #######
    "FEdc": 0,
    "FEfc": 0,
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
    "FIfc": 0,
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
    "FSli": 0,
    "FSls": 0,
    "FSmd": 0,
    "FSms": 0,
    "FSpv": 0,
    "FStv": 0,
####### ???????? #######
    "FTcx": 2147483647,
    "FTin": -2147483648,
    "FTix": 2147483647,
    "FTli": 0,
    "FTpd": 2500,
    "FTrn": -2147483648,
    "FTrx": 2147483647,
    "FTvl": 0,
    "FTwn": -2147483648,
    "FTwx": 2147483647,
    "FTxb": 0,
####### ???????? #######
    "FVer": 0,
####### HEAD ACCEL #######
    "HAai": 0,
    "HAdr": 5,     # (int) Head Accel Duration
    "HAdb": 5,
    "HAdl": 5,
    "HAfa": 0,
    "HAfo": 0,
    "HAil": 0,
    "HAli": 0,
    "HApc": 500,
    "HApi": 500,
    "HApr": 200,
    "HArl": 0,
    "HAsi": 2,
    "HAsr": 2,
    "HAxi": 0,
    "HAxr": 0,
    "HAyi": 0,
    "HAyr": 0,
    "HAzi": 0,
    "HAzr": 0,
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
####### ???????? #######
    "HIix": 1023,
    "HIpd": 100,
    "HIrx": 1023,
####### HEAD TEMP #######
    "HTcx": 2147483647,
    "HTfc": 0,
    "HTfo": 0,
    "HTin": -2147483648,
    "HTix": 2147483647,
    "HTli": 1000,        # (int) Board Temp - Logging interval (ms)
    "HTpd": 2500,        # (int) Head Temp - Period (ms)
    "HTrn": -2147483648,
    "HTrx": 2147483647,
    "HTvl": 768,
    "HTwn": -2147483648,
    "HTwx": 2147483647,
    "HTxb": 0,
####### ???????? #######
    "HVcr": 0,
    "HVli": 0,
    "HVvo": 0,
####### ???????? #######
    "IAid": 0,
####### INTAKE FAN #######
    "IFdc": 0,
    "IFdm": 0,
    "IFfc": 536870912,
    "IFid": 0,    # (int) Intake Fan PWM Duty Cycle 0-65535 (Possibly Warm Up Phase))
    "IFil": 1000,
    "IFin": 0,
    "IFix": 0,
    "IFli": 1000,
    "IFrd": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Likely Run Phase))
    "IFrl": 1000,
    "IFrn": 0,
    "IFrx": 0,
    "IFsd": 0,
    "IFsl": 1000,
    "IFsn": 0,
    "IFsx": 0,
    "IFta": 40882666,
    "IFtb": 40424667,
    "IFwd": 0,    # (int) Exhaust Fan PWM Duty Cycle 0-65535 (Possibly Cool down Phase))
    "IFwl": 1000,
    "IFwn": 0,
    "IFwx": 0,
####### ???????? #######
    "IMct": 3500,
    "IMfs": 2,
    "IMjq": 40,
    "IMmd": 509649408,
####### ???????? #######
    "IRli": 0,
    "IRva": 32,
    "IRvb": 32,
    "IRvc": 35,
    "IRvd": 36,
####### INTERCONNECT TEMP #######
    "ITcx": 2147483647,
    "ITfc": 0,
    "ITfo": 0,
    "ITin": -2147483648,
    "ITix": 2147483647,
    "ITli": 1000,        # (int) Interconnect Temp - Logging interval (ms)
    "ITpd": 5000,        # (int) Interconnect Temp - Logging interval (ms)
    "ITrn": -2147483648,
    "ITrx": 2147483647,
    "ITvl": 7904,
    "ITwn": -2147483648,
    "ITwx": 2147483647,
    "ITxb": 0,
####### LID ACCEL #######
    "LAai": 0,
    "LAar": 0,
    "LAdb": 5,
    "LAdl": 5,
    "LAfa": 0,
    "LAfo": 0,
    "LAil": 0,
    "LAli": 0,
    "LApc": 500,
    "LApi": 500,
    "LApr": 200,
    "LArl": 0,
    "LAsi": 2,
    "LAsr": 2,
    "LAxi": 0,
    "LAxr": 0,
    "LAyi": 0,
    "LAyr": 0,
    "LAzi": 0,
    "LAzr": 0,
####### LID CAMERA #######
    "LCae": 0,     # (int) Lid Cam - Auto Exposure
    "LCag": 0,     # (int) Lid Cam - Auto Gain
    "LCaw": 2,     # (int) Lid Cam - Auto White Balance
    "LCbb": 1400,  # (int) Lid Cam - Blue Balance
    "LCex": 3000,  # (int) Lid Cam - Exposure
    "LCfl": 0,     # (int) Lid Cam - Flash On
    "LCfm": 2,     # (int) Lic Cam - Flash Mode
    "LCga": 30,    # (int) Lid Cam - Gain
    "LChf": 1,     # (int) Lid Cam - Horizontal Flip
    "LCrb": 1100,  # (int) Lid Cam - Red Balance
    "LCvf": 0,     # (int) Lid Cam - Vertical Flip
####### LID LED #######
    "LLev": 0,
    "LLsp": 28,    # (int) Lid LED Speed
    "LLvl": 101,   # (int) Lid LED Brightness
####### LID TEMP #######
    "LTcx": 2147483647,
    "LTfc": 0,
    "LTfo": 0,
    "LTin": -2147483648,
    "LTix": 2147483647,
    "LTli": 1000,        # (int) Lid Temp - Logging interval
    "LTpd": 5000,        # (int) Lid Temp - Period
    "LTrn": -2147483648,
    "LTrx": 2147483647,
    "LTvl": 0,
    "LTwn": -2147483648,
    "LTwx": 2147483647,
    "LTxb": 0,
####### MACHINE CONTROL #######
    "MCbc": 1,      # (int) Boot attempts
    "MCbf": 1,      # (int) Boot Flags (1 - power-on, 2 - software reset, )
    "MCbr": 320,    # (int) Manufacturing Info ??
    "MCbu": 20576,  # (int) Boot Fuses 0x00005060
    "MCcl": 1000,   # (int) CPU Temp - Logging Interval
    "MCcn": 0,
    "MCcp": 2500,   # (int) CPU Temp - Period
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
    "MCsv": "2.3.0",
    "MCsw": 27,
    "MCtc": 0,
    "MCut": 0.26666668,
####### NETWORK INTERFACE #######
    "NIcc": 1,
    "NIcf": 0,
    "NIdc": 0,
    "NIdf": 0,
    "NIft": 0,
    "NIim": 1500,  # MTU
    "NIma": "de:ad:be:ef:00:00", # MAC ADDRESS
    "NIrb": 0.017756462,
    "NIrd": 0,
    "NIre": 0,
    "NIro": 0,
    "NIrp": 50,
    "NIrr": 19.5,
    "NIsa": -57,
    "NIss": -42,
    "NItb": 0.0094909668,
    "NItd": 0,
    "NIte": 0,
    "NItp": 60,
    "NItr": 72.199997,
    "NIts": 0,
    "NIuc": 0,
    "NIuf": 0,
####### ???????? #######
    "NRab": 131072,
    "NRac": 7,
    "NRae": 2,
    "NRaf": 1000,
    "NRaj": 1000,
    "NRib": 131072,
    "NRic": 3,
    "NRie": 2,
    "NRif": 1000,
    "NRij": 500,
    "NRpb": 131072,
    "NRpc": 3,
    "NRpe": 2,
    "NRpf": 1000,
    "NRpj": 500,
    "NRwb": 131072,
    "NRwc": 120,
    "NRwe": 2,
    "NRwf": 500,
    "NRwj": 250,
####### PURGE AIR #######
    "PAcc": 853,
    "PAcm": 0,
    "PAli": 1000,  # (int) Purge Air - Logging Interval
    "PAon": 1,     # (int) Purge Air - On
    "PAos": 0,
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
    "SLto": 300000,
####### ???????? #######
    "TCon": 0,
    "TCth": 2147483647,
    "TCtt": 0,
####### ???????? #######
    "UAid": 0,
####### ???????? #######
    "ULst": 0,
####### WATER PUMP #######
    "WPon": 1,  # (int) Water Pump - On
####### ???????? #######
    "WSst": 0,
####### WATER TEMPERATURE #######
    "WTaf":3221225472,
    "WTbf":3221225472,
    "WTua": 755,
    "WTub": 754,
    "WTva": 754,
    "WTvb": 751,
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
    "ZSmd": 1,   # (int) Z Stepper Microstepping Mode
    "ZSrc": 0    # (int) Z Stepper Run Current
}


"""
These are settings that have been observed in actions, but not in MOTION or device reports:

HCil: Head Cam Illumination  - This setting is set to 1072693248 (3FF00000) to turn on the laser.

"""
