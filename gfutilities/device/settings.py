"""
(C) Copyright 2020
Scott Wiederhold, s.e.wiederhold@gmail.com
https://community.openglow.org

SPDX-License-Identifier:    MIT
"""
import time
import logging
from queue import Queue
from ..configuration import get_cfg, set_cfg
from ..service.websocket import send_wss_event

_SETTINGS = {
    # Settings that are communicated between the service and the device.
    # Mostly just sent to the service from the machine, and it seems to make little difference.
    # Default values are included for those that are not otherwise set (see further down).
    # Throwing garbage values doesn't seem to hurt.  Not sure what the point of this exercise is...
    #
    # "ITEM": (<data type>, <report>, <min value>, <max value>, <default value>)
    "AAdc": (int, True, 0, 1023, 204),  # AirAssist
    "AAfc": (int, True, None, None, 536870912),  # AirAssist
    "AAid": (int, True, 0, 1023, 204),  # AirAssist
    "AAil": (int, True, None, None, 1000),  # AirAssist
    "AAin": (int, True, None, None, 0),  # AirAssist
    "AAix": (int, True, None, None, 0),  # AirAssist
    "AAli": (int, True, None, None, 1000),  # AirAssist
    "AArd": (int, True, None, None, 0),  # AirAssist
    "AArl": (int, True, None, None, 1000),  # AirAssist
    "AArn": (int, True, None, None, 0),  # AirAssist
    "AArx": (int, True, None, None, 0),  # AirAssist
    "AAsd": (int, True, None, None, 0),  # AirAssist
    "AAsl": (int, True, None, None, 1000),  # AirAssist
    "AAsn": (int, True, None, None, 0),  # AirAssist
    "AAsx": (int, True, None, None, 0),  # AirAssist
    "AAtv": (int, True, None, None, 3457),  # AirAssist
    "AAwd": (int, True, None, None, 0),  # AirAssist
    "AAwl": (int, True, None, None, 1000),  # AirAssist
    "AAwn": (int, True, None, None, 0),  # AirAssist
    "AAwx": (int, True, None, None, 0),  # AirAssist
    "AScm": (int, True, None, None, 0),  #
    "AShw": (str, True, None, None, "00000000000000000000000000000000000000000000000000000000000"),  #
    "BAai": (int, True, None, None, 0),  # Board Accel
    "BAar": (int, True, None, None, 0),  # Board Accel
    "BAdb": (int, True, None, None, 5),  # Board Accel
    "BAdl": (int, True, None, None, 5),  # Board Accel
    "BAfa": (int, True, None, None, 0),  # Board Accel
    "BAfo": (int, True, None, None, 0),  # Board Accel
    "BAil": (int, True, None, None, 0),  # Board Accel
    "BAli": (int, True, None, None, 0),  # Board Accel
    "BApc": (int, True, None, None, 500),  # Board Accel
    "BApi": (int, True, None, None, 500),  # Board Accel
    "BApr": (int, True, None, None, 200),  # Board Accel
    "BArl": (int, True, None, None, 0),  # Board Accel
    "BAsi": (int, True, None, None, 2),  # Board Accel
    "BAsr": (int, True, None, None, 2),  # Board Accel
    "BAxi": (int, True, None, None, 0),  # Board Accel
    "BAxr": (int, True, None, None, 0),  # Board Accel
    "BAyi": (int, True, None, None, 0),  # Board Accel
    "BAyr": (int, True, None, None, 0),  # Board Accel
    "BAzi": (int, True, None, None, 0),  # Board Accel
    "BAzr": (int, True, None, None, 0),  # Board Accel
    "BDet": (int, True, None, None, 96),  # e t Beam Detect
    "BDie": (int, True, None, None, 0),  # Beam Detect
    "BDlk": (int, True, None, None, 1966),  # Beam Detect: lambda k
    "BDlt": (int, True, None, None, 6553),  # Beam Detect: lambda t
    "BDpe": (int, True, None, None, 0),  # Beam Detect
    "BDtr": (int, True, None, None, 32),  # Beam Detect: theta r
    "BDtt": (int, True, None, None, 40),  # Beam Detect: theta t
    "BLev": (int, True, None, None, 0),  #
    "BLva": (int, True, None, None, 0),  #
    "BLvb": (int, True, None, None, 0),  #
    "BLvc": (int, True, None, None, 0),  #
    "BTcx": (int, True, None, None, 2147483647),  # Board Temp
    "BTfc": (int, True, None, None, 0),  # Board Temp
    "BTfo": (int, True, None, None, 0),  # Board Temp
    "BTin": (int, True, None, None, -2147483648),  # Board Temp
    "BTix": (int, True, None, None, 2147483647),  # Board Temp
    "BTli": (int, True, None, None, 1000),  # Board Temp
    "BTpd": (int, True, None, None, 2500),  # Board Temp
    "BTrn": (int, True, None, None, -2147483648),  # Board Temp
    "BTrx": (int, True, None, None, 2147483647),  # Board Temp
    "BTvl": (int, True, None, None, 752),  # Board Temp
    "BTwn": (int, True, None, None, -2147483648),  # Board Temp
    "BTwx": (int, True, None, None, 2147483647),  # Board Temp
    "BTxb": (int, True, None, None, 0),  # Board Temp
    "CAid": (int, True, None, None, 0),  #
    "CAwb": (int, True, None, None, 0),  #
    "CCbp": (int, True, None, None, 0),  #
    "CCbt": (int, True, None, None, 0),  #
    "CCfl": (int, True, None, None, 0),  #
    "CCml": (int, True, None, None, 0),  #
    "CCpb": (int, True, None, None, 200000),  #
    "CCro": (int, True, None, None, 5000),  #
    "CCst": (int, True, None, None, 2),  #
    "CCup": (int, True, None, None, 0),  #
    "CCxp": (int, True, None, None, 0),  #
    "CCyp": (int, True, None, None, 0),  #
    "CCzp": (int, True, None, None, 0),  #
    "CDcb": (int, True, None, None, 0),  #
    "CDcc": (int, True, None, None, 1),  #
    "CDsb": (int, True, None, None, 0),  #
    "CDtb": (int, True, None, None, 0),  #
    "CFdn": (int, True, None, None, 0),  #
    "CFdt": (int, True, None, None, 0),  #
    "CFdx": (int, True, None, None, 0),  #
    "CFen": (int, True, None, None, 0),  #
    "CFer": (int, True, None, None, 0),  #
    "CFex": (int, True, None, None, 0),  #
    "CFhp": (int, True, None, None, 0),  #
    "CFhs": (int, True, None, None, 0),  #
    "CFhw": (int, True, None, None, 0),  #
    "CFhx": (int, True, None, None, 0),  #
    "CFki": (int, True, None, None, 0),  #
    "CFkp": (int, True, None, None, 0),  #
    "CFli": (int, True, None, None, 0),  #
    "CFpd": (int, True, None, None, 0),  #
    "CFpp": (int, True, None, None, 0),  #
    "CFps": (int, True, None, None, 1),  #
    "CFrh": (int, True, None, None, 0),  #
    "CFsp": (int, True, None, None, 0),  #
    "CMdt": (int, True, None, None, 18364),  #
    "CMet": (int, True, None, None, 18134),  #
    "CMin": (int, True, None, None, 4008),  #
    "CMix": (int, True, None, None, 50010),  #
    "CMli": (int, True, None, None, 100),  #
    "CMpd": (int, True, None, None, 1000),  #
    "CMrn": (int, True, None, None, 1017),  #
    "CMrx": (int, True, None, None, 31040),  #
    "CMts": (int, True, None, None, 0),  #
    "CMup": (int, True, None, None, 100),  #
    "CMut": (int, True, None, None, 18134),  #
    "CMwn": (int, True, None, None, 1017),  #
    "CMwx": (int, True, None, None, 31040),  #
    "CTin": (int, True, None, None, 391),  #
    "CTix": (int, True, None, None, 935),  #
    "CTrn": (int, True, None, None, 591),  #
    "CTrx": (int, True, None, None, 971),  #
    "CTwn": (int, True, None, None, 591),  #
    "CTwx": (int, True, None, None, 971),  #
    "EFdc": (int, True, None, None, 0),  # Exhaust Fan
    "EFfc": (int, True, None, None, 536870912),  # Exhaust Fan
    "EFid": (int, True, 0, 65535, 0),  # Exhaust Fan
    "EFil": (int, True, None, None, 1000),  # Exhaust Fan
    "EFin": (int, True, None, None, 0),  # Exhaust Fan
    "EFix": (int, True, None, None, 0),  # Exhaust Fan
    "EFli": (int, True, None, None, 1000),  # Exhaust Fan
    "EFrd": (int, True, 0, 65535, 0),  # Exhaust Fan
    "EFrl": (int, True, None, None, 1000),  # Exhaust Fan
    "EFrn": (int, True, None, None, 0),  # Exhaust Fan
    "EFrx": (int, True, None, None, 0),  # Exhaust Fan
    "EFsd": (int, True, None, None, 0),  # Exhaust Fan
    "EFsl": (int, True, None, None, 1000),  # Exhaust Fan
    "EFsn": (int, True, None, None, 0),  # Exhaust Fan
    "EFsx": (int, True, None, None, 0),  # Exhaust Fan
    "EFtv": (int, True, None, None, 0),  # Exhaust Fan
    "EFwd": (int, True, None, None, 0),  # Exhaust Fan
    "EFwl": (int, True, None, None, 1000),  # Exhaust Fan
    "EFwn": (int, True, None, None, 0),  # Exhaust Fan
    "EFwx": (int, True, None, None, 0),  # Exhaust Fan
    "FAdc": (int, True, None, None, 0),  #
    "FAfc": (int, True, None, None, 0),  #
    "FAid": (int, True, None, None, 0),  #
    "FAil": (int, True, None, None, 0),  #
    "FAin": (int, True, None, None, 0),  #
    "FAix": (int, True, None, None, 0),  #
    "FAli": (int, True, None, None, 0),  #
    "FArd": (int, True, None, None, 0),  #
    "FArl": (int, True, None, None, 0),  #
    "FArn": (int, True, None, None, 0),  #
    "FArx": (int, True, None, None, 0),  #
    "FAtv": (int, True, None, None, 0),  #
    "FAwd": (int, True, None, None, 0),  #
    "FAwl": (int, True, None, None, 0),  #
    "FAwn": (int, True, None, None, 0),  #
    "FAwx": (int, True, None, None, 0),  #
    "FEdc": (int, True, None, None, 0),  #
    "FEfc": (int, True, None, None, 0),  #
    "FEid": (int, True, None, None, 0),  #
    "FEil": (int, True, None, None, 0),  #
    "FEin": (int, True, None, None, 0),  #
    "FEix": (int, True, None, None, 0),  #
    "FEli": (int, True, None, None, 0),  #
    "FErd": (int, True, None, None, 0),  #
    "FErl": (int, True, None, None, 0),  #
    "FErn": (int, True, None, None, 0),  #
    "FErx": (int, True, None, None, 0),  #
    "FEta": (int, True, None, None, 0),  #
    "FEtb": (int, True, None, None, 0),  #
    "FEtc": (int, True, None, None, 0),  #
    "FEtd": (int, True, None, None, 0),  #
    "FEwd": (int, True, None, None, 0),  #
    "FEwl": (int, True, None, None, 0),  #
    "FEwn": (int, True, None, None, 0),  #
    "FEwx": (int, True, None, None, 0),  #
    "FIdc": (int, True, None, None, 0),  #
    "FIfc": (int, True, None, None, 0),  #
    "FIid": (int, True, None, None, 0),  #
    "FIil": (int, True, None, None, 0),  #
    "FIin": (int, True, None, None, 0),  #
    "FIix": (int, True, None, None, 0),  #
    "FIli": (int, True, None, None, 0),  #
    "FIrd": (int, True, None, None, 0),  #
    "FIrl": (int, True, None, None, 0),  #
    "FIrn": (int, True, None, None, 0),  #
    "FIrx": (int, True, None, None, 0),  #
    "FIta": (int, True, None, None, 0),  #
    "FItb": (int, True, None, None, 0),  #
    "FItc": (int, True, None, None, 0),  #
    "FItd": (int, True, None, None, 0),  #
    "FIwd": (int, True, None, None, 0),  #
    "FIwl": (int, True, None, None, 0),  #
    "FIwn": (int, True, None, None, 0),  #
    "FIwx": (int, True, None, None, 0),  #
    "FSli": (int, True, None, None, 0),  #
    "FSls": (int, True, None, None, 0),  #
    "FSmd": (int, True, None, None, 0),  #
    "FSms": (int, True, None, None, 0),  #
    "FSpv": (int, True, None, None, 0),  #
    "FStv": (int, True, None, None, 0),  #
    "FTcx": (int, True, None, None, 2147483647),  #
    "FTin": (int, True, None, None, -2147483648),  #
    "FTix": (int, True, None, None, 2147483647),  #
    "FTli": (int, True, None, None, 0),  #
    "FTpd": (int, True, None, None, 2500),  #
    "FTrn": (int, True, None, None, -2147483648),  #
    "FTrx": (int, True, None, None, 2147483647),  #
    "FTvl": (int, True, None, None, 0),  #
    "FTwn": (int, True, None, None, -2147483648),  #
    "FTwx": (int, True, None, None, 2147483647),  #
    "FTxb": (int, True, None, None, 0),  #
    "FVer": (int, True, None, None, 0),  #
    "HAai": (int, True, None, None, 0),  # Head Accel
    "HAdr": (int, True, None, None, 5),  # Head Accel
    "HAdb": (int, True, None, None, 5),  # Head Accel
    "HAdl": (int, True, None, None, 5),  # Head Accel
    "HAfa": (int, True, None, None, 0),  # Head Accel
    "HAfo": (int, True, None, None, 0),  # Head Accel
    "HAil": (int, True, None, None, 0),  # Head Accel
    "HAli": (int, True, None, None, 0),  # Head Accel
    "HApc": (int, True, None, None, 500),  # Head Accel
    "HApi": (int, True, None, None, 500),  # Head Accel
    "HApr": (int, True, None, None, 200),  # Head Accel
    "HArl": (int, True, None, None, 0),  # Head Accel
    "HAsi": (int, True, None, None, 2),  # Head Accel
    "HAsr": (int, True, None, None, 2),  # Head Accel
    "HAxi": (int, True, None, None, 0),  # Head Accel
    "HAxr": (int, True, None, None, 0),  # Head Accel
    "HAyi": (int, True, None, None, 0),  # Head Accel
    "HAyr": (int, True, None, None, 0),  # Head Accel
    "HAzi": (int, True, None, None, 0),  # Head Accel
    "HAzr": (int, True, None, None, 0),  # Head Accel
    "HCae": (int, True, None, None, 0),  # Head Cam: Auto Exposure
    "HCag": (int, True, None, None, 0),  # Head Cam: Auto Gain
    "HCaw": (int, True, None, None, 2),  # Head Cam: AWB
    "HCbb": (int, True, None, None, 1400),  # Head Cam: Blue Balance
    "HCex": (int, True, None, None, 3000),  # Head Cam: Exposure
    "HCga": (int, True, None, None, 30),  # Head Cam: Gain
    "HChf": (int, True, 0, 1, 1),  # Head Cam: Horizontal Flip
    "HCil": (int, False, None, None, None),  # Head Cam Illumination
    "HCrb": (int, True, None, None, 1100),  # Head Cam: Red Balance
    "HCvf": (int, True, 0, 1, 0),  # Head Cam: Vertical Flip
    "HEfv": (int, True, None, None, None),  # Head: Firmware Version Head
    "HEhl": (int, True, None, None, 0),  # Head
    "HEid": (int, True, None, None, 1100),  # Head
    "HEsn": (int, True, None, None, None),  # Serial Number Head
    "HEua": (int, True, None, None, 841174597),  # Head
    "HEub": (int, True, None, None, 5472275),  # Head
    "HEuc": (int, True, None, None, 19),  # Head
    "HEul": (int, True, None, None, 0),  # Head
    "HEwl": (int, True, None, None, 0),  # Head
    "HIix": (int, True, None, None, 1023),  #
    "HIpd": (int, True, None, None, 100),  #
    "HIrx": (int, True, None, None, 1023),  #
    "HTcx": (int, True, None, None, 2147483647),  # Head Temp
    "HTfc": (int, True, None, None, 0),  # Head Temp
    "HTfo": (int, True, None, None, 0),  # Head Temp
    "HTin": (int, True, None, None, -2147483648),  # Head Temp
    "HTix": (int, True, None, None, 2147483647),  # Head Temp
    "HTli": (int, True, None, None, 1000),  # Head Temp
    "HTpd": (int, True, None, None, 2500),  # Head Temp
    "HTrn": (int, True, None, None, -2147483648),  # Head Temp
    "HTrx": (int, True, None, None, 2147483647),  # Head Temp
    "HTvl": (int, True, None, None, 768),  # Head Temp
    "HTwn": (int, True, None, None, -2147483648),  # Head Temp
    "HTwx": (int, True, None, None, 2147483647),  # Head Temp
    "HTxb": (int, True, None, None, 0),  # Head Temp
    "HVcr": (int, True, None, None, 0),  #
    "HVli": (int, True, None, None, 0),  #
    "HVvo": (int, True, None, None, 0),  #
    "IAid": (int, True, None, None, 0),  #
    "IFdc": (int, True, None, None, 0),  # Intake Fan
    "IFdm": (int, True, None, None, 0),  # Intake Fan
    "IFfc": (int, True, None, None, 536870912),  # Intake Fan
    "IFid": (int, True, 0, 65535, 0),  # Intake Fan: Idle PWM
    "IFil": (int, True, None, None, 1000),  # Intake Fan
    "IFin": (int, True, None, None, 0),  # Intake Fan
    "IFix": (int, True, None, None, 0),  # Intake Fan
    "IFli": (int, True, None, None, 1000),  # Intake Fan
    "IFrd": (int, True, 0, 65535, 0),  # Intake Fan: Run PWM
    "IFrl": (int, True, None, None, 1000),  # Intake Fan
    "IFrn": (int, True, None, None, 0),  # Intake Fan
    "IFrx": (int, True, None, None, 0),  # Intake Fan
    "IFsd": (int, True, None, None, 0),  # Intake Fan
    "IFsl": (int, True, None, None, 1000),  # Intake Fan
    "IFsn": (int, True, None, None, 0),  # Intake Fan
    "IFsx": (int, True, None, None, 0),  # Intake Fan
    "IFta": (int, True, None, None, 40882666),  # Intake Fan
    "IFtb": (int, True, None, None, 40424667),  # Intake Fan
    "IFwd": (int, True, 0, 65535, 0),  # Intake Fan
    "IFwl": (int, True, None, None, 1000),  # Intake Fan
    "IFwn": (int, True, None, None, 0),  # Intake Fan
    "IFwx": (int, True, None, None, 0),  # Intake Fan
    "IMct": (int, True, None, None, 3500),  #
    "IMfs": (int, True, None, None, 2),  #
    "IMjq": (int, True, None, None, 40),  #
    "IMmd": (int, True, None, None, 509649408),  #
    "IRli": (int, True, None, None, 0),  #
    "IRva": (int, True, None, None, 32),  #
    "IRvb": (int, True, None, None, 32),  #
    "IRvc": (int, True, None, None, 35),  #
    "IRvd": (int, True, None, None, 36),  #
    "ITcx": (int, True, None, None, 2147483647),  # Interconnect Temp
    "ITfc": (int, True, None, None, 0),  # Interconnect Temp
    "ITfo": (int, True, None, None, 0),  # Interconnect Temp
    "ITin": (int, True, None, None, -2147483648),  # Interconnect Temp
    "ITix": (int, True, None, None, 2147483647),  # Interconnect Temp
    "ITli": (int, True, None, None, 1000),  # Interconnect Temp
    "ITpd": (int, True, None, None, 5000),  # Interconnect Temp
    "ITrn": (int, True, None, None, -2147483648),  # Interconnect Temp
    "ITrx": (int, True, None, None, 2147483647),  # Interconnect Temp
    "ITvl": (int, True, None, None, 7904),  # Interconnect Temp
    "ITwn": (int, True, None, None, -2147483648),  # Interconnect Temp
    "ITwx": (int, True, None, None, 2147483647),  # Interconnect Temp
    "ITxb": (int, True, None, None, 0),  # Interconnect Temp
    "LAai": (int, True, None, None, 0),  # Lid Accel
    "LAar": (int, True, None, None, 0),  # Lid Accel
    "LAdb": (int, True, None, None, 5),  # Lid Accel
    "LAdl": (int, True, None, None, 5),  # Lid Accel
    "LAfa": (int, True, None, None, 0),  # Lid Accel
    "LAfo": (int, True, None, None, 0),  # Lid Accel
    "LAil": (int, True, None, None, 0),  # Lid Accel
    "LAli": (int, True, None, None, 0),  # Lid Accel
    "LApc": (int, True, None, None, 500),  # Lid Accel
    "LApi": (int, True, None, None, 500),  # Lid Accel
    "LApr": (int, True, None, None, 200),  # Lid Accel
    "LArl": (int, True, None, None, 0),  # Lid Accel
    "LAsi": (int, True, None, None, 2),  # Lid Accel
    "LAsr": (int, True, None, None, 2),  # Lid Accel
    "LAxi": (int, True, None, None, 0),  # Lid Accel
    "LAxr": (int, True, None, None, 0),  # Lid Accel
    "LAyi": (int, True, None, None, 0),  # Lid Accel
    "LAyr": (int, True, None, None, 0),  # Lid Accel
    "LAzi": (int, True, None, None, 0),  # Lid Accel
    "LAzr": (int, True, None, None, 0),  # Lid Accel
    "LCae": (int, True, None, None, 0),  # Lid Cam: Auto Exposure
    "LCag": (int, True, None, None, 0),  # Lid Cam: Auto Gain
    "LCaw": (int, True, None, None, 2),  # Lid Cam: AWB
    "LCbb": (int, True, None, None, 1400),  # Lid Cam: Blue Balance
    "LCex": (int, True, None, None, 3000),  # Lid Cam: Exposure
    "LCfl": (int, True, None, None, 0),  # Lid Cam: Flash On
    "LCfm": (int, True, None, None, 2),  # Lid Cam: Flash Mode
    "LCga": (int, True, None, None, 30),  # Lid Cam: Gain
    "LChf": (int, True, 0, 1, 1),  # Lid Cam: Horizontal Flip
    "LCrb": (int, True, None, None, 1100),  # Lid Cam: Red Balance
    "LCvf": (int, True, 0, 1, 0),  # Lid Cam: Vertical Flip
    "LLev": (int, True, None, None, 0),  # Lid LED
    "LLsp": (int, True, None, None, 28),  # Speed Lid LED
    "LLvl": (int, True, None, None, 101),  # Brightness Lid LED
    "LTcx": (int, True, None, None, 2147483647),  # Lid Temp
    "LTfc": (int, True, None, None, 0),  # Lid Temp
    "LTfo": (int, True, None, None, 0),  # Lid Temp
    "LTin": (int, True, None, None, -2147483648),  # Lid Temp
    "LTix": (int, True, None, None, 2147483647),  # Lid Temp
    "LTli": (int, True, None, None, 1000),  # Lid Temp
    "LTpd": (int, True, None, None, 5000),  # Lid Temp
    "LTrn": (int, True, None, None, -2147483648),  # Lid Temp
    "LTrx": (int, True, None, None, 2147483647),  # Lid Temp
    "LTvl": (int, True, None, None, 0),  # Lid Temp
    "LTwn": (int, True, None, None, -2147483648),  # Lid Temp
    "LTwx": (int, True, None, None, 2147483647),  # Lid Temp
    "LTxb": (int, True, None, None, 0),  # Lid Temp
    "MCbc": (int, True, None, None, 1),  # BaseMachine Control: Boot attempts
    "MCbf": (int, True, None, None, 1),  # BaseMachine Control: Boot Flags
    "MCbr": (int, True, None, None, 320),  # BaseMachine Control: Manufacturing Info
    "MCbu": (int, True, None, None, 20576),  # BaseMachine Control: Boot Fuses
    "MCcl": (int, True, None, None, 1000),  # BaseMachine Control
    "MCcn": (int, True, None, None, 0),  # BaseMachine Control
    "MCcp": (int, True, None, None, 2500),  # BaseMachine Control
    "MCct": (int, True, None, None, 49156),  # BaseMachine Control
    "MCcx": (int, True, None, None, 65000),  # BaseMachine Control
    "MCdb": (int, True, None, None, 0),  # BaseMachine Control
    "MCds": (int, True, None, None, 0),  # BaseMachine Control
    "MCdt": (int, True, None, None, None),  # BaseMachine Control: BaseMachine Time
    "MCdv": (str, True, None, None, None),  # BaseMachine Control: Software Version
    "MCip": (str, True, None, None, None),  # BaseMachine Control: IP Address
    "MCla": (float, True, None, None, 0.13574219),  # BaseMachine Control
    "MClb": (float, True, None, None, 0.032226562),  # BaseMachine Control
    "MClc": (float, True, None, None, 0.010742188),  # BaseMachine Control
    "MCld": (int, True, None, None, 0),  # BaseMachine Control
    "MCma": (int, True, None, None, 0),  # BaseMachine Control
    "MCmi": (int, True, None, None, 0),  # BaseMachine Control
    "MCov": (str, True, None, None, None),  # BaseMachine Control: Firmware Version
    "MCpt": (int, True, None, None, 4),  # BaseMachine Control
    "MCrc": (int, True, None, None, 2),  # BaseMachine Control
    "MCsn": (int, True, None, None, None),  # BaseMachine Control: Serial Number
    "MCsv": (str, True, None, None, "2.3.0"),  # BaseMachine Control
    "MCsw": (int, True, None, None, 27),  # BaseMachine Control
    "MCtc": (int, True, None, None, 0),  # BaseMachine Control
    "MCut": (float, True, None, None, 0.26666668),  # BaseMachine Control
    "NIcc": (int, True, None, None, 1),  # Network Interface
    "NIcf": (int, True, None, None, 0),  # Network Interface
    "NIdc": (int, True, None, None, 0),  # Network Interface
    "NIdf": (int, True, None, None, 0),  # Network Interface
    "NIft": (int, True, None, None, 0),  # Network Interface
    "NIim": (int, True, None, None, 1500),  # MTU Network Interface
    "NIma": (str, True, None, None, "de:ad:be:ef:00:00"),  # MAC Network Interface
    "NIrb": (float, True, None, None, 0.017756462),  # Network Interface
    "NIrd": (int, True, None, None, 0),  # Network Interface
    "NIre": (int, True, None, None, 0),  # Network Interface
    "NIro": (int, True, None, None, 0),  # Network Interface
    "NIrp": (int, True, None, None, 50),  # Network Interface
    "NIrr": (float, True, None, None, 19.5),  # Network Interface
    "NIsa": (int, True, None, None, -57),  # Network Interface
    "NIss": (int, True, None, None, -42),  # Network Interface
    "NItb": (float, True, None, None, 0.0094909668),  # Network Interface
    "NItd": (int, True, None, None, 0),  # Network Interface
    "NIte": (int, True, None, None, 0),  # Network Interface
    "NItp": (int, True, None, None, 60),  # Network Interface
    "NItr": (float, True, None, None, 72.199997),  # Network Interface
    "NIts": (int, True, None, None, 0),  # Network Interface
    "NIuc": (int, True, None, None, 0),  # Network Interface
    "NIuf": (int, True, None, None, 0),  # Network Interface
    "NRab": (int, True, None, None, 131072),  #
    "NRac": (int, True, None, None, 7),  #
    "NRae": (int, True, None, None, 2),  #
    "NRaf": (int, True, None, None, 1000),  #
    "NRaj": (int, True, None, None, 1000),  #
    "NRib": (int, True, None, None, 131072),  #
    "NRic": (int, True, None, None, 3),  #
    "NRie": (int, True, None, None, 2),  #
    "NRif": (int, True, None, None, 1000),  #
    "NRij": (int, True, None, None, 500),  #
    "NRpb": (int, True, None, None, 131072),  #
    "NRpc": (int, True, None, None, 3),  #
    "NRpe": (int, True, None, None, 2),  #
    "NRpf": (int, True, None, None, 1000),  #
    "NRpj": (int, True, None, None, 500),  #
    "NRwb": (int, True, None, None, 131072),  #
    "NRwc": (int, True, None, None, 120),  #
    "NRwe": (int, True, None, None, 2),  #
    "NRwf": (int, True, None, None, 500),  #
    "NRwj": (int, True, None, None, 250),  #
    "PAcc": (int, True, None, None, 853),  # Purge Air
    "PAcm": (int, True, None, None, 0),  # Purge Air
    "PAli": (int, True, None, None, 1000),  # Purge Air
    "PAon": (int, True, None, None, 1),  # On Purge Air
    "PAos": (int, True, None, None, 0),  # Purge Air
    "PApd": (int, True, None, None, 1000),  # Purge Air
    "PCid": (int, True, None, None, 19795),  # ID PIC
    "PRcp": (float, True, None, None, 2.875),  #
    "PRfc": (int, True, None, None, 0),  #
    "PRlc": (int, True, None, None, 0),  #
    "PRls": (int, True, None, None, 0),  #
    "PRnt": (int, True, None, None, 12),  #
    "PRrs": (int, True, None, None, 11206656),  #
    "PRsc": (int, True, None, None, 1),  #
    "PRvs": (int, True, None, None, 141811712),  #
    "PTli": (int, True, None, None, 1000),  # Power Temp
    "PTmn": (int, True, None, None, 0),  # Power Temp
    "PTmx": (int, True, None, None, 4294967295),  # Power Temp
    "PTpd": (int, True, None, None, 5000),  # Power Temp
    "PTvl": (int, True, None, None, 628),  # Power Temp
    "RAid": (int, True, None, None, 0),  #
    "SAid": (int, True, None, None, 0),  # Request ID the settings report is responding to
    "SLto": (int, True, None, None, 300000),  #
    "TCon": (int, True, None, None, 0),  #
    "TCth": (int, True, None, None, 2147483647),  #
    "TCtt": (int, True, None, None, 0),  #
    "UAid": (int, True, None, None, 0),  #
    "ULst": (int, True, None, None, 0),  #
    "WPon": (int, True, 0, 1, 1),  # On Water Pump
    "WSst": (int, True, None, None, 0),  #
    "WTaf": (int, True, None, None, 3221225472),  # Water Temp
    "WTbf": (int, True, None, None, 3221225472),  # Water Temp
    "WTua": (int, True, None, None, 755),  # Water Temp
    "WTub": (int, True, None, None, 754),  # Water Temp
    "WTva": (int, True, None, None, 754),  # Water Temp
    "WTvb": (int, True, None, None, 751),  # Water Temp
    "XScc": (int, True, None, None, 33),  # Current X Step
    "XSdm": (int, True, None, None, 1),  # Decay Mode X Step
    "XShc": (int, True, None, None, 33),  # Current X Step
    "XSmm": (int, True, None, None, 1),  # Microstepping Mode X Step
    "XSrc": (int, True, None, None, 0),  # Current X Step
    "YScc": (int, True, None, None, 5),  # Current Y Step
    "YSdm": (int, True, None, None, 1),  # Decay Mode Y Step
    "YShc": (int, True, None, None, 5),  # Current Y Step
    "YSmm": (int, True, None, None, 1),  # Microstepping Mode Y Step
    "YSrc": (int, True, None, None, 0),  # Current Y Step
    "ZHin": (int, True, None, None, 180),  # Homing Step Interval (ms) Z Step
    "ZScc": (int, True, None, None, 1),  # Current Z Step
    "ZSen": (int, True, 0, 1, 0),  # Enable Z Step
    "ZShc": (int, True, None, None, 1),  # Current Z Step
    "ZSmd": (int, True, None, None, 1),  # Microstepping Mode Z Step
    "ZSrc": (int, True, None, None, 0),  # Current Z Step
}

_CONFIG_PROVIDERS = {
    # These configuration item values are pulled from the configuration file.
    "MCdv": "MACHINE.APP_VERSION",
    "MCip": "MACHINE.IP_ADDRESS",
    "MCov": "MACHINE.FIRMWARE",
    "MCsn": "MACHINE.SERIAL",
    "HEfv": "MACHINE.HEAD_FIRMWARE",
    "HEsn": "MACHINE.HEAD_SERIAL",
}

_REGISTERED_PROVIDERS = {
    # These configuration item values are the result of running the specified function
    "MCdt": time.time,
}


def send_report(q: Queue, msg: dict) -> None:
    """
    Send device settings report in the required format.
    :param q: {WSS message queue
    :type q: Queue
    :param msg: WSS Message
    :type msg: dict
    :return:
    """
    settings = ''
    logging.info("START")
    for item, (data_type, include_in_report, min_val, max_val, default_val) in _SETTINGS.items():
        value = str(default_val)
        if include_in_report:
            if item == 'SAid':
                value = msg['id']
            if item in _CONFIG_PROVIDERS:
                config_value = get_cfg(_CONFIG_PROVIDERS.get(item))
                if config_value is not None:
                    value = str(config_value)
            if item in _REGISTERED_PROVIDERS:
                value = str(_REGISTERED_PROVIDERS[item]())
            if data_type is int:
                value = int(float(value))
            elif data_type is str:
                value = '"{}"'.format(value)
            else:
                value = data_type(value)
            settings += '"{}":{},'.format(item, value)

    # The service seems to bypass the homing process if we send it an empty settings value.
    # It is assumed that this prevents the machine from re-homing every time it loses and regains
    # the connection to the Glowforge service.
    if not get_cfg('SETTINGS.SET') and not get_cfg('MACHINE.BYPASS_HOMING'):
        send_wss_event(q, msg, 'settings:completed',
                       data={'key': 'settings', 'value': '{"values":{%s}}' % settings[:-1]})
        set_cfg('SETTINGS.SET', True)
    else:
        send_wss_event(q, msg, 'settings:completed', data={'key': 'settings', 'value': '{}'})
    logging.info("COMPLETE")
