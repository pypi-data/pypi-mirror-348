# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250428-104133
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
启动MCP客户端，连带MCP服务端
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from weberFuncs import PrintTimeMsg, PrettyPrintStr, PrintAndSleep
import os
import asyncio
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

# from FuncForSettings import GetCurrentWorkParam
from LoadMcpServerConfig import LoadMcpServerConfig
from LlmServer import LlmServer
from FileQueryResult import FileQueryResult
from sqids import Sqids


class TaskMcpClient:
    # SEP_CHAR_NAME = '.'  # MCP Server 服务名与函数名的分隔符

    def __init__(self, sEnvFN='.env'):
        self.sWorkDir = os.getcwd()
        PrintTimeMsg(f'TaskMcpClient.sWorkDir={self.sWorkDir}=')
        self.exit_stack = AsyncExitStack()

        oLoadConfig = LoadMcpServerConfig(self.sWorkDir)
        # self.dictCmdPath = GetCurrentWorkParam('dictCmdPath')
        # self.dictMcpServers = GetCurrentWorkParam('dictMcpServers')
        self.dictCmdPath = oLoadConfig.dictCmdPath
        self.dictMcpServers = oLoadConfig.dictMcpServers

        self.dictSessionByName = {}  # 通过 服务名 映射 Sessioon
        self.lsServFuncTools = []  # MCP Server 服务端工具列表
        self.oLlm = LlmServer(self.sWorkDir, sEnvFN)
        self.oFile = FileQueryResult(self.sWorkDir)

        self.sqids = Sqids(
            alphabet='w5U4shrOSJvXbQq9MdtRTcI1oPKjlL8AkYCaVZHNye0G7zu6p3gWBxiEmfD2Fn',
            # alphabet='abcdefghijklmnopqrstuvwxyz',  # 仅小写字母
            min_length=5  # 最少字符数
        )
        self.dictFuncNameByIdx = {}

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

    async def _register_one_mcp_server(self, sModuName, dictMcpServer):
        """注册一个MCP服务"""
        # sModuName 是MCP服务名，模块名
        sType = dictMcpServer.get('type', '')
        if sType not in ['stdio', 'sse']:
            PrintTimeMsg('_register_one_mcp_server({sModuName}).type={sType}=Error,SKIP!')
            return None
        if sType == 'stdio':
            sCmd = dictMcpServer.get('cmd', '')
            if not sCmd:
                sCmd = dictMcpServer.get('command', '')
            server_params = StdioServerParameters(
                command=self.dictCmdPath.get(sCmd, sCmd),
                args=dictMcpServer.get('args', []),
                env=dictMcpServer.get('env', None),
            )
            PrintTimeMsg(f'_register_one_mcp_server({sModuName}).server_params={server_params}=')
            rwContext = await self.exit_stack.enter_async_context(stdio_client(server_params))
            # read_stream, write_stream = rwContext
            # oSession = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
            # await oSession.initialize()
            # PrintTimeMsg(f'_register_one_mcp_server({sModuName}).oSession.initialize!')
            # self.dictSessionByName[sModuName] = oSession
            # async with stdio_client(server_params) as rwContext:
            #     async with ClientSession(*rwContext) as oSession:
            #         await oSession.initialize()
            #         self.dictSessionByName[sModuName] = oSession
        else:
            sUrl = dictMcpServer.get('url', '')
            dictHeader = dictMcpServer.get('headers', {})
            PrintTimeMsg(f'_register_one_mcp_server({sModuName}).sUrl={sUrl},dictHeader={dictHeader}=')
            # 如下写法，oSession 被释放了
            # async with sse_client(sUrl, dictHeader) as rwContext:
            #     async with ClientSession(*rwContext) as oSession:
            #         await oSession.initialize()
            #         self.dictSessionByName[sModuName] = oSession
            rwContext = await self.exit_stack.enter_async_context(sse_client(sUrl, dictHeader))
        read_stream, write_stream = rwContext
        oSession = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        return oSession

    async def connect_mcp_servers(self):
        """连接到多个MCP服务端"""
        for sModuName, dictMcpServer in self.dictMcpServers.items():
            # if sName.startswith('@'):  # 跳过代码示例
            #     continue
            # PrintTimeMsg(f'connect_mcp_servers({sModuName})={PrettyPrintStr(dictMcpServer)}=')
            oSession = await self._register_one_mcp_server(sModuName, dictMcpServer)
            if oSession:
                await oSession.initialize()
                PrintTimeMsg(f'connect_mcp_servers({sModuName}).oSession.initialize!')
                self.dictSessionByName[sModuName] = oSession

        # PrintTimeMsg(f'connect_mcp_servers.dictSessionByName={self.dictSessionByName}=')
        PrintTimeMsg(f"connect_mcp_servers.len(self.dictSessionByName)={len(self.dictSessionByName)}=")
        await self._gather_available_tools()
        # await self._list_prompts()
        # PrintTimeMsg(f'connect_mcp_servers.lsServFuncTools={self.lsServFuncTools}=')
        return

    async def _list_prompts(self):
        # 获取所有 Prompt 模板, WeiYF.测试内容为空
        lsPrompts = []
        for sModuName, oSession in self.dictSessionByName.items():
            response = await oSession.list_prompts()
            PrintTimeMsg(f'_list_prompts({sModuName})={PrettyPrintStr(response)}=')
            lsPrompts.append([prompt.name for prompt in response.prompts])
        PrintTimeMsg(f'_list_prompts()={PrettyPrintStr(lsPrompts)}=')

    async def _gather_available_tools(self):
        """汇总所有MCP服务的工具列表"""
        self.lsServFuncTools = []
        lsFuncDesc = []  # Func简单描述信息列表，用于打印
        iModuleCnt = 0
        for sModuName, oSession in self.dictSessionByName.items():
            response = await oSession.list_tools()
            iModuleCnt += 1
            iFuncCnt = 0
            for tool in response.tools:
                iFuncCnt += 1
                sFullFuncName = 'f%s' % self.sqids.encode([iModuleCnt, iFuncCnt])
                # sModuSeq = f'm%.2d' % iModuleCnt
                # sFuncSeq = 'f%.3d' % iFuncCnt
                # sFullFuncName = f"{sModuSeq}{self.SEP_CHAR_NAME}{sFuncSeq}"
                sIdx = '%s,%s' % (iModuleCnt, iFuncCnt)
                self.dictFuncNameByIdx[sIdx] = {
                    'm': sModuName,
                    'f': tool.name,
                }
                self.lsServFuncTools.append({
                    "type": "function",  # OpenAI兼容写法
                    "function": {
                        "name": sFullFuncName,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                        # 'required': tool.required,  # no required
                    }
                })
                lsFuncDesc.append((sFullFuncName, tool.name, tool.description[:30]))
        # PrintTimeMsg(f"_gather_available_tools.lsServFuncTools={PrettyPrintStr(self.lsServFuncTools)}=")
        iIdx = 0
        for (sFunc, sTool, sDesc) in lsFuncDesc:
            PrintTimeMsg(f"{iIdx}#{sFunc}#{sTool}={sDesc}")
            iIdx += 1

    async def _callbackTool(self, sFullFuncName, lsArgs):
        # 回调执行工具函数
        try:
            # PrintTimeMsg(f"_callbackTool(sName={sFullFuncName}, lsArgs={lsArgs})")
            # sModuSeq, cSep, sFuncSeq = sFullFuncName.partition(self.SEP_CHAR_NAME)  # .
            iModuleCnt, iFuncCnt = self.sqids.decode(sFullFuncName[1:])
            # iModuleCnt = int(sModuSeq[1:])
            # iFuncCnt = int(sFuncSeq[1:])
            sIdx = '%s,%s' % (iModuleCnt, iFuncCnt)
            dictMF = self.dictFuncNameByIdx.get(sIdx, {})
            sModuName = dictMF.get('m', '')
            sFuncName = dictMF.get('f', '')
            PrintTimeMsg(f"_callbackTool({sFullFuncName}={sModuName}.{sFuncName}({lsArgs})...")

            oSession = self.dictSessionByName.get(sModuName, None)
            if oSession:
                oResult = await oSession.call_tool(sFuncName, lsArgs)
                return oResult
        except Exception as e:
            PrintTimeMsg(f"_callbackTool({sFullFuncName}).e={repr(e)}")
        raise Exception(f'_callbackTool.sFullFuncName={sFullFuncName}=NotFound!')

    async def loop_mcp_chat(self):
        """MCP交互聊天循环"""
        PrintTimeMsg("loop_mcp_chat.MCP Client Started!")
        # PrintTimeMsg("Type your queries or 'quit' to exit.")
        while True:
            try:
                query = input("\nQuery: ").strip()
                if not query: continue
                if query.lower() == 'quit':
                    break
                # query = '洛杉矶的天气怎样？'
                # # query = '1234 + 7890 = ?'
                # query = 'xuanyuan的视频里面，网络安全主题相关的播放最高的是哪个?'
                # 调用LLM及工具
                PrintTimeMsg(f"loop_mcp_chat.query={query}=")
                await self.oLlm.process_query(query, self.lsServFuncTools, self._callbackTool)
                final_text = '\n'.join(self.oLlm.lsFinalTextOut)
                PrintTimeMsg(f"loop_mcp_chat.final_text={final_text}=")
                # break
            except Exception as e:
                PrintTimeMsg(f"loop_mcp_chat.e={repr(e)}=")

    async def loop_mcp_file_query(self):
        """MCP循环监听处理文件请求"""
        PrintTimeMsg("loop_mcp_file_query.MCP Client Started!")

        async def callbackQueryResult(sQueryText):
            PrintTimeMsg(f"callbackQueryResult.sQueryText={sQueryText}=")
            await self.oLlm.process_query(sQueryText, self.lsServFuncTools, self._callbackTool)
            return self.oLlm

        iLoopCnt = 0
        while True:
            iSleepSeconds = 60
            try:
                lsNoExtFN = self.oFile.list_file_query_task()
                for sNoExtFN in lsNoExtFN:
                    await self.oFile.deal_file_query_result(sNoExtFN, callbackQueryResult)
            except Exception as e:
                PrintTimeMsg(f"loop_mcp_file_query.e={repr(e)}=")
            PrintAndSleep(iSleepSeconds, f'loop_mcp_file_query.iLoopCnt={iLoopCnt}', iLoopCnt % 10 == 0)
            iLoopCnt += 1


async def mainTaskMcpClient():
    sRunMode = 'chat'  # 默认是聊天模式
    sEnvFN = '.env'  # 环境变量配置文件
    if len(sys.argv) >= 2:
        sRunMode = sys.argv[1]
        if len(sys.argv) >= 3:
            sEnvFN = sys.argv[2]

    client = TaskMcpClient(sEnvFN)
    try:
        await client.connect_mcp_servers()
        # PrintAndSleep(10, 'JustWait')
        if sRunMode == 'task':
            await client.loop_mcp_file_query()
        else:  # chat
            await client.loop_mcp_chat()
    finally:
        await client.cleanup()


def asyncio_loop_run(cbASyncFunc):
    # 循环等待执行异步IO函数
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cbASyncFunc())


def main():
    asyncio_loop_run(mainTaskMcpClient)


if __name__ == '__main__':
    main()
