# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250509-100600
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
计算某个定时控制匹配的时间
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from weberFuncs import PrintTimeMsg, GetCurrentTime


def str_to_int_default(sVal, iDefault=0):
    # 将字符串转为整数，提供缺省值以避免异常
    try:
        iResult = int(sVal)
    except ValueError:
        iResult = iDefault
    return iResult


def calc_match_time(sAtEvery, iMinMinute=5):
    # 依据定时控制计算当前匹配的时间
    # sAtEvery定时控制，取值：
    #    every 1h 每小时
    #    at 09:45 定时
    #    once 仅一次
    # iMinMinute 最小粒度，默认5分钟，可大不可小，必须是5/10/15/20/30/60
    # 20250509-091857  every 1h  ->  20250509-090000
    # 20250509-093857  every 0.5h  ->  20250509-093000
    # 20250509-091857  every 2h  ->  20250509-080000
    # 20250509-091857  at 09:45   ->  20250509-094500
    # 20250509-091857  once ->  YYYYMMDD-hhnnss
    # 返回匹配时间串，以及下次检查间隔分钟数
    if iMinMinute not in [5, 10, 15, 20, 30, 60]:
        if iMinMinute < 5:
            iMinMinute = 5
        elif iMinMinute > 60:
            iMinMinute = 60
        else:
            iMinMinute = iMinMinute // 5 * 5

    sResult = 'YYYYMMDD-hhnnss'
    iNextMinute = iMinMinute
    sYmdHns = GetCurrentTime()
    sHHNN = ''
    if sAtEvery.startswith('at '):
        sHN = sAtEvery[3:]
        sH, cSep, sN = sHN.partition(':')
        iH = str_to_int_default(sH)
        iN = str_to_int_default(sN) // iMinMinute * iMinMinute
        sHHNN = '%.2d%.2d' % (iH, iN)
        iNextMinute = 60
    elif sAtEvery.startswith('every '):
        sEveryParam = sAtEvery[6:]
        if not sEveryParam:
            sEveryParam = '1h'
        elif sEveryParam == '0.5h':
            sEveryParam = '30m'  # 转为整数
        sUnit = sEveryParam[-1:]
        if sUnit == 'h':  # 按小时处理
            iHour = str_to_int_default(sEveryParam[:-1])
            lsHourV = [1, 2, 3, 4, 6, 8, 12]
            if iHour not in lsHourV:
                for i in range(len(lsHourV)):
                    if lsHourV[i] <= iHour < lsHourV[i + 1]:
                        iHour = lsHourV[i]
                        break
                else:
                    if iHour > 12:
                        iHour = 12
                    else:
                        iHour = 1
            iH = str_to_int_default(sYmdHns[9:11])
            iH = iH // iHour * iHour
            sHHNN = '%.2d00' % iH
            iNextMinute = 60 * iHour
        else:  # 按分钟处理
            iN = str_to_int_default(sEveryParam[:-1])
            iN = iN // iMinMinute * iMinMinute
            iHN = str_to_int_default(sYmdHns[9:11]) * 60 + str_to_int_default(sYmdHns[11:13])
            iHN = iHN // iN * iN
            sHHNN = '%.2d%.2d' % (iHN // 60, iHN % 60)
            iNextMinute = iMinMinute
    if sHHNN:
        sResult = '%s-%s00' % (sYmdHns[:8], sHHNN)
    PrintTimeMsg(f'calc_match_time({sAtEvery},{iMinMinute}).sResult={sResult}={iNextMinute}')
    return sResult, iNextMinute


def mainClassOne():
    calc_match_time('every 1h')
    calc_match_time('every 20m')
    calc_match_time('every 120m')
    calc_match_time('every 5h')
    calc_match_time('once')
    calc_match_time('at 10:18')
    calc_match_time('at 3:8')
    calc_match_time('at 23:58')
    calc_match_time('at 0:59')
    calc_match_time('at 9:')
    calc_match_time('at :9')
    calc_match_time('at 9.')


if __name__ == '__main__':
    mainClassOne()

