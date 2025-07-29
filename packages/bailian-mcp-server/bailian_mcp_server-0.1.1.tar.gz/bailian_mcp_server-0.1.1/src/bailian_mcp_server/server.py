# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP
from pydantic import Field
import httpx
import json
import os
import logging
import dashscope
from http import HTTPStatus
from dashscope import VideoSynthesis
logger = logging.getLogger('mcp')

settings = {
    'log_level': 'DEBUG'
}
# 初始化mcp服务
mcp = FastMCP('bailian-mcp-server', log_level='ERROR', settings=settings)
# 定义工具
@mcp.tool(name='通义万相-文生视频', description='通义万相-文生视频，输入提示词生成视频，例如：一只小猫在月光下奔跑')
async def query_logistics(
        prompt: str = Field(description='文生视频提示词')
) -> str:
    """通义万相-文生视频
    Args:
        prompt: 文生视频提示词
    Returns:
        视频地址
    """
    logger.info('收到文生视频请求，提示词：{}'.format(prompt))
    api_key = os.getenv("API_KEY", "")
    if not api_key:
        return '请先设置API_KEY环境变量'
    # call sync api, will return the result
    print('please wait...')
    dashscope.api_key = api_key
    rsp = VideoSynthesis.call(model='wanx2.1-t2v-turbo',
                                  prompt=prompt,
                                  size='624*624')
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        return rsp.output.video_url
    else:
        return ('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

def run():
    mcp.run(transport='stdio')
if __name__ == '__main__':
   run()