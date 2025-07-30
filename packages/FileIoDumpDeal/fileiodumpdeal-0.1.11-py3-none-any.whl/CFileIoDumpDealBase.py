# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250507-092607
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
Program description
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from weberFuncs import PrintTimeMsg, PrintAndSleep
from weberFuncs import TryForceMakeDir
import os


class CFileIoDumpDealBase(object):
    # 通过文件输入输出，对接 TaskMcpClient 等应用
    def __init__(self, sMcpTaskDir):
        # sMcpTaskDir 是对应 TaskMcpClient 的Task工作目录，带尾部task
        self.sMcpTaskDir = sMcpTaskDir  # os.path.join(self.sWorkDir, 'task')
        PrintTimeMsg(f'CFileIoDumpDealBase.sMcpTaskDir={self.sMcpTaskDir}=')
        self.sWasteDir = os.path.join(self.sMcpTaskDir, 'waste')
        TryForceMakeDir(self.sWasteDir)

    def DumpFile4Query(self, sQueryDir):
        # 导出到文件到 sQueryDir 目录，作为 TaskMcpClient 的Query输入
        # 返回导出文件数目
        PrintTimeMsg(f'CFileIoDumpDealBase.DumpFile4Query.sQueryDir={sQueryDir}=')
        iDumpCnt = 0
        iMinNextMinute = 60
        return iDumpCnt, iMinNextMinute

    def DealFileResult(self, sNoExtFN, sResultDir):
        # 将sResultDir目录下的回复文件，提交到其它系统，并移动到备份目录
        # sNoExtFN 不带扩展名及_R/_Q的文件名
        # 返回处理成功与否
        PrintTimeMsg(f'CFileIoDumpDealBase.DumpFile4Query.sNoExtFN={sNoExtFN}={sResultDir}=')
        bDealOk = True
        return bDealOk

    def _ProcessTaskResult(self):
        # 将任务结果文件移到waste目录
        iProcessCnt = 0
        # lsNoExtFN = self._ListTaskResultFile()
        lsNoExtFN = []
        sResultDir = os.path.join(self.sMcpTaskDir, 'result')
        for sFN in os.listdir(sResultDir):
            sNoExtFN, sExt = os.path.splitext(sFN)
            if sExt.lower() != '.md':
                continue
            if sNoExtFN.endswith('_R'):  # 仅关注 _R ，传入不带 _R/_Q 后缀
                lsNoExtFN.append(sNoExtFN[:-2])
        # PrintTimeMsg(f'_ProcessTaskResult({sResultDir}).len(lsNoExtFN)={len(lsNoExtFN)}=')

        for sNoExtFN in lsNoExtFN:
            bDealOk = self.DealFileResult(sNoExtFN, sResultDir)
            sDealOk = 'ok' if bDealOk else 'err'
            for sTail in ['_R', '_Q']:
                sFullResultFN = os.path.join(sResultDir, f'{sNoExtFN}{sTail}.md')
                sFullWasteFN = os.path.join(self.sWasteDir, f'{sDealOk}_{sNoExtFN}{sTail}.md')
                os.rename(sFullResultFN, sFullWasteFN)
                iProcessCnt += 1
            PrintAndSleep(45, f'_ProcessTaskResult.sNoExtFN={sNoExtFN}=Wait45s')
        # PrintTimeMsg(f'_ProcessTaskResult.iProcessCnt={iProcessCnt}=')
        return iProcessCnt

    def LoopFileIoDumpDeal(self, iSleepSeconds):
        """MCP循环监听处理文件请求"""
        PrintTimeMsg("LoopFileIoDumpDeal.Started!")

        sQueryDir = os.path.join(self.sMcpTaskDir, 'query')

        iLoopCnt = 0
        while True:
            try:
                iProcessCnt = self._ProcessTaskResult()
                iDumpCnt, iMinNextMinute = self.DumpFile4Query(sQueryDir)
                iSleepSecs = iMinNextMinute * 60
                if iSleepSecs < iSleepSeconds:
                    iSleepSecs = iSleepSeconds
                # 由于 DealFileResult 和 DumpFile4Query 共用一个循环框架，
                # 休息时间固定是60秒为好
            except Exception as e:
                PrintTimeMsg(f"LoopFileIoDumpDeal.e={repr(e)}=WARNING!")
            PrintAndSleep(iSleepSeconds, f'LoopFileIoDumpDeal.iLoopCnt={iLoopCnt}=iProcessCnt={iProcessCnt},iDumpCnt={iDumpCnt}=')
            iLoopCnt += 1


def mainFileIoDumpDealBase():
    sMcpTaskDir = r'E:\WeberSrcRoot\Rocky9GogsRoot\RobotAgentMCP\TaskMcpClient\task'
    o = CFileIoDumpDealBase(sMcpTaskDir)
    o.LoopFileIoDumpDeal(60)


if __name__ == '__main__':
    mainFileIoDumpDealBase()
