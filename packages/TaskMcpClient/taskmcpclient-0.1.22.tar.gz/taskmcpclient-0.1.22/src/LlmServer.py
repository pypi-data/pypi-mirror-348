# -*- coding: utf-8 -*-
"""
 __createTime__ = 20250427-105337
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
封装MCP场景下的LLM服务
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from weberFuncs import PrintTimeMsg, PrettyPrintStr
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
# from markitdown import MarkItDown
import xmltodict


class LlmServer:
    def __init__(self, sWorkDir='', sEnvFN='.env'):
        # PrintTimeMsg('LlmServer.__init__')
        sFullEnvFN = sEnvFN
        if sWorkDir:
            sFullEnvFN = os.path.join(sWorkDir, sEnvFN)
            # PrintTimeMsg(f'LlmServer.sFullEnvFN={sFullEnvFN}=')
            # self._check_init_env_file(sFullEnvFN)
        bLoad = load_dotenv(dotenv_path=sFullEnvFN, verbose=True)  # load environment variables from .env
        PrintTimeMsg(f"LlmServer.load_dotenv({sFullEnvFN})={bLoad}")
        sOpenAiUrl = os.getenv("OPENAI_BASE_URL")
        sOpenAiKey = os.getenv("OPENAI_API_KEY")
        self.sOpenAiModel = os.getenv("OPENAI_MODEL")
        PrintTimeMsg(f'LlmServer.sOpenAiUrl={sOpenAiUrl}, sOpenAiModel={self.sOpenAiModel}')
        self.openai = OpenAI(api_key=sOpenAiKey, base_url=sOpenAiUrl)  # 兼容 OpenAI 客户端
        # self.markitdown = MarkItDown()  # 转为Markdown格式

    # def _check_init_env_file(self, sEnvFN):
    #     # 创建 .env 并写入初始值
    #     if not os.path.exists(sEnvFN):
    #         lsEnvKey = [
    #             'OPENAI_BASE_URL',
    #             'OPENAI_API_KEY',
    #             'OPENAI_MODEL',
    #         ]
    #         with open(sEnvFN, 'w', encoding='utf-8') as f:
    #             for sK in lsEnvKey:
    #                 f.write(f'{sK}=\n')

    async def get_llm_response(self, lsMsg: list, lsTools: list):
        # 向 LLM 发起query请求
        response = self.openai.chat.completions.create(
            model=self.sOpenAiModel,
            # max_tokens=1000,
            messages=lsMsg,
            tools=lsTools,
        )
        PrintTimeMsg(f'get_llm_response().response={response}')
        return response

    # async def parse_tool_call_result(self, oResult):
    #     # 解析 tool_call 返回结果
    #     # PrintTimeMsg(f"_callbackTool.oResult={PrettyPrintStr(oResult)}=")
    #     PrintTimeMsg(f"_callbackTool.oResult.isError={oResult.isError}=")
    #     if oResult.isError:
    #         PrintTimeMsg(f"_callbackTool.oResult.content={oResult.content}=")
    #     else:
    #         PrintTimeMsg(f"_callbackTool.len(oResult.content)={len(oResult.content)}=")
    #         for oContent in oResult.content:
    #             # PrintTimeMsg(f"_callbackTool.oContent={PrettyPrintStr(oContent)}=")
    #             try:
    #                 sXmlStr = '<root>%s</root>' % oContent.text
    #                 dictRoot = xmltodict.parse(sXmlStr, encoding='utf-8')
    #                 dictData = dictRoot.get('root', {})
    #                 lsT = []
    #                 for k,v in dictData.items():
    #                     lsT.append(f'  - {k}={v}')
    #                 sMdText = '\n'.join(lsT)
    #                 # sTitle = dictData.get('title', '')
    #                 # sLink =  dictData.get('link', '')
    #                 # sAuthor =  dictData.get('author', '')
    #                 # sMdText = f"""[{sTitle}]({sLink}) By: {sAuthor}"""
    #                 #
    #                 # PrintTimeMsg(f"_callbackTool.sMdText={sMdText}=")
    #             except Exception as e:
    #                 PrintTimeMsg(f"_callbackTool.e={repr(e)}=")
    #                 sMdText = oContent.text

    async def _exec_llm_query_response(self, callbackTool, lsMsg, lsTools, lsFinalTextOut):
        # 执行一次LLM请求响应
        response = await self.get_llm_response(lsMsg, lsTools)  # 处理消息
        for choice in response.choices:
            message = choice.message
            if not message.tool_calls:  # 如果不调用工具，则添加到 lsFinalTextOut 中
                lsFinalTextOut.append(message.content)
            else:  # 如果是工具调用，则获取工具名称和输入
                tool_name = message.tool_calls[0].function.name
                try:
                    tool_args = json.loads(message.tool_calls[0].function.arguments)
                except Exception as e:
                    PrintTimeMsg(f"process_query.json_argv.e={repr(e)}=")
                    tool_args = {}
                PrintTimeMsg(f'process_query.tool_name={tool_name},tool_args={tool_args}=')
                try:
                    oResult = await callbackTool(tool_name, tool_args)
                    # await self.parse_tool_call_result(oResult)
                    PrintTimeMsg(f"_callbackTool.oResult.isError={oResult.isError}=")
                    if oResult.isError:
                        PrintTimeMsg(f"_callbackTool.oResult.content={oResult.content}=")
                        continue

                    PrintTimeMsg(f"_callbackTool.len(oResult.content)={len(oResult.content)}=")
                    iContentCnt = 0
                    for oContent in oResult.content:
                        # PrintTimeMsg(f"_callbackTool.oContent={PrettyPrintStr(oContent)}=")
                        try:
                            sXmlStr = '<root>%s</root>' % oContent.text
                            dictRoot = xmltodict.parse(sXmlStr, encoding='utf-8')
                            dictData = dictRoot.get('root', {})
                            iContentCnt += 1
                            lsT = []
                            lsT.append('')  # 多一条换行
                            lsT.append(f'- 第{iContentCnt}条内容')
                            for k,v in dictData.items():
                                lsT.append(f'  - {k}={v}')
                            sMdText = '\n'.join(lsT)
                            # sTitle = dictData.get('title', '')
                            # sLink =  dictData.get('link', '')
                            # sAuthor =  dictData.get('author', '')
                            # sMdText = f"""[{sTitle}]({sLink}) By: {sAuthor}"""
                            # PrintTimeMsg(f"_callbackTool.sMdText={sMdText}=")
                        except Exception as e:
                            PrintTimeMsg(f"_exec_llm_query_response.parse.e={repr(e)}=")
                            sMdText = oContent.text
                        lsFinalTextOut.append(sMdText)
                except Exception as e:
                    PrintTimeMsg(f"_exec_llm_query_response.e={repr(e)}=")
                    return

                # 继续与工具结果进行对话
                if message.content and hasattr(message.content, 'text'):
                    lsMsg.append({
                      "role": "assistant",
                      "content": message.content
                    })
                # 将工具调用结果添加到消息
                lsMsg.append({
                    "role": "user",
                    "content": str(oResult.content)
                })
                # 获取下一个LLM响应，递归调用
                await self._exec_llm_query_response(callbackTool, lsMsg, lsTools, lsFinalTextOut)

    async def process_query(self, sQuery: str, lsTools: list, callbackTool) -> str:
        # 使用 OpenAI 和可用工具处理查询
        # callbackTool: Callable[[str, list], str]
        # WeiYF 严格声明函数原型，会增加python代码的复杂性，在应用开发中不提倡

        # 创建消息列表
        lsMsg = [{"role": "user", "content": sQuery}]
        lsFinalTextOut = []
        await self._exec_llm_query_response(callbackTool, lsMsg, lsTools, lsFinalTextOut)
        return '\n'.join(lsFinalTextOut)

    async def process_query_bak(self, sQuery: str, lsTools: list, callbackTool) -> str:
        # 使用 OpenAI 和可用工具处理查询
        # callbackTool: Callable[[str, list], str]
        # WeiYF 严格声明函数原型，会增加python代码的复杂性，在应用开发中不提倡

        # 创建消息列表
        lsMsg = [{"role": "user", "content": sQuery}]

        # available_tools = await self.get_tools()  # 列出可用工具
        response = await self.get_llm_response(lsMsg, lsTools)  # 处理消息

        # tool_results = []
        ls_final_text = []  # 返回结果文本
        for choice in response.choices:
            message = choice.message
            if not message.tool_calls:  # 如果不调用工具，则添加到 ls_final_text 中
                ls_final_text.append(message.content)
            else:  # 如果是工具调用，则获取工具名称和输入
                # 解包tool_calls
                tool_name = message.tool_calls[0].function.name
                try:
                    tool_args = json.loads(message.tool_calls[0].function.arguments)
                except Exception as e:
                    PrintTimeMsg(f"process_query.json_argv.e={repr(e)}=")
                    tool_args = {}
                # PrintTimeMsg(f"准备调用工具:【{tool_name}】参数:【{json.dumps(tool_args, ensure_ascii=False, indent=2)}】")
                PrintTimeMsg(f'process_query.tool_name={tool_name},tool_args={tool_args}=')
                # 执行工具调用，获取结果
                oResult = await callbackTool(tool_name, tool_args)
                # # tool_results.append({"call": tool_name, "result": result})
                # # final_text.append(f"[调用工具:【{tool_name}】参数:【{tool_args}】, 返回【{result}】]")
                # # PrintTimeMsg(f'process_query().result={result}')
                # sResultMd = self.markitdown.convert(str(result))
                # # PrintTimeMsg(f'process_query().sResultMd={sResultMd}')
                # final_text.append(f"调用工具:【{tool_name}】参数:【{tool_args}】, 返回【{sResultMd}】]")
                await self.parse_tool_call_result(oResult)

                # 继续与工具结果进行对话
                if message.content and hasattr(message.content, 'text'):
                    lsMsg.append({
                      "role": "assistant",
                      "content": message.content
                    })
                # 将工具调用结果添加到消息
                lsMsg.append({
                    "role": "user",
                    "content": str(oResult.content)
                })
                # 获取下一个LLM响应
                response = self.get_llm_response(lsMsg, lsTools)
                # 将结果添加到 final_text
                ls_final_text.append(response.choices[0].message.content)
        # PrintTimeMsg(f'process_query().tool_results={tool_results}')
        # return "\\n".join(final_text)
        return "\n".join(ls_final_text)


def mainLlmServer():
    import asyncio
    o = LlmServer()
    # lsMessages = [{
    #     'role': 'user',
    #     'content': '天为什么蓝色的？'
    # }]
    # o.get_llm_response(lsMessages, [])

    def callbackTool(sName, lsArgs):
        PrintTimeMsg(f"callbackTool(sName={sName}, lsArgs={lsArgs})")
        return f"callbackTool(sName={sName}, lsArgs={lsArgs})"

    asyncio.run(o.process_query('天为什么蓝色的？', [], callbackTool))


if __name__ == '__main__':
    mainLlmServer()
