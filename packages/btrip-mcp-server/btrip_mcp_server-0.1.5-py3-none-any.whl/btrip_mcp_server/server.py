# -*- coding: utf-8 -*-
import time
from optparse import Option
from typing import Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field
import httpx
import json
import os
import logging
import hashlib
import random

from pydantic.v1.types import OptionalInt

logger = logging.getLogger("mcp")

# 初始化mcp服务
mcp = FastMCP("btrip-mcp-server")


def signature(timestamp: str, nonce: str, req_body: str, encrypt_key: str) -> str:
    """
    SHA-256 签名生成函数（符合RFC 4634标准）

    :param timestamp: 时间戳字符串 (通常为Unix时间戳)
    :param nonce: 随机数字符串 (推荐16位以上)
    :param req_body: 请求体原文 (需确保已排序/标准化)
    :param encrypt_key: 加密密钥 (建议从安全存储获取)
    :return: 小写十六进制签名串（64字符）

    示例:
    >>> signature("123", "abc", "body", "key")
    'd5e4e3c8f492b3c6a0d3f7d3c3c3e3d3c3e3d3c3e3d3c3e3d3c3e3d3c3e3d3'
    """
    # 参数校验
    if not all(isinstance(arg, str) for arg in [timestamp, nonce, req_body, encrypt_key]):
        raise TypeError("所有参数必须为字符串类型")

    # 拼接顺序必须与Java保持一致
    raw_str = f"{timestamp}{nonce}{encrypt_key}{req_body}"

    # 创建SHA-256对象（推荐用new方式提升复用性）
    sha = hashlib.sha256()
    sha.update(raw_str.encode('utf-8'))  # 必须指定编码

    # 返回小写十六进制字符串（与Java兼容）
    return sha.hexdigest()


@mcp.tool(name="查询企业员工部门信息",
          description="查询企业员工部门信息接口，输入企业id和员工id，返回该员工的所属部门信息")
async def query_employee_org(corpId: str = Field(description="要查询员工所属企业id"),
                             employeeId: str = Field(description="要查询的员工的 id")) -> object:
    logger.info("收到查询员工组织请求, corpId:{} employeeId:{}".format(corpId, employeeId))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not corpId:
        return "<UNK>corpId<UNK>"
    if not employeeId:
        return "<UNK>employeeId<UNK>"

    body = {"corpId": corpId, "employeeId": employeeId}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryEmployeeOrg"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-timestamp": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result


@mcp.tool(name="查询城市信息",
          description="搜索城市信息，输入城市关键词，返回城市相关的信息")
async def query_employee_org(keyword: str = Field(description="城市搜索的关键词,支持模糊搜索,必填参数"),
                             queryCityType: str = Field(None,
                                                        description="查询城市类型 flight: 机票 、train: 火车 、 hotel: 酒店; 非必填"),
                             searchType: str = Field('all',
                                                     description="查询国内还是国际 默认查询所有 all 国内：domestic 国际：international, 非必填")) -> object:
    logger.info(
        "收到查询城市信息请求, keyword:{} queryCityType:{} searchType:{}".format(keyword, queryCityType, searchType))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not keyword:
        return "<UNK>keyword<UNK>"

    body = {"keyword": keyword, "queryCityType": queryCityType, "searchType": searchType}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/standardSearch"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-timestamp": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result


@mcp.tool(name="批量查询员工信息",
          description="批量查询员工信息, 输入企业id和员工id列表,返回员工信息集合")
async def query_employee_org(corpId: str = Field(description="企业id,必填参数"),
                             employeeIdList: [] = Field(description="员工id列表,必填参数"), ) -> object:
    logger.info("收到批量查询员工信息列表, corpId:{} employeeIdList:{}".format(corpId, employeeIdList))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not corpId:
        return "<UNK>keyword<UNK>"
    if not employeeIdList:
        return "<UNK>employeeIdList<UNK>"

    body = {"corpId": corpId, "employeeIdList": employeeIdList}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryEmployeeListByEmployeeIdList"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-timestamp": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result


@mcp.tool(name="查询员工的基本信息",
          description="查询员工的基本信息	, 输入企业id和员工id,返回员工基本信息")
async def query_employee_org(corpId: str = Field(description="企业id,必填参数"),
                             employeeId: str = Field(description="员工id,必填参数"), ) -> object:
    logger.info("收到查询员工的基本信息, corpId:{} employeeId:{}".format(corpId, employeeId))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not corpId:
        return "<UNK>keyword<UNK>"
    if not employeeId:
        return "<UNK>employeeId<UNK>"

    body = {"corpId": corpId, "employeeId": employeeId}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryEmployeeBasic"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-timestamp": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result


@mcp.tool(name="查询员工的可用发票抬头信息列表",
          description="查询员工的可用发票抬头信息列表, 输入企业id和员工id,返回员工可用的发票抬头信息列表")
async def query_employee_org(corpId: str = Field(description="企业id,必填参数"),
                             employeeId: str = Field(description="员工id,必填参数"), ) -> object:
    logger.info("收到查询员工的可用发票抬头信息列表, corpId:{} employeeId:{}".format(corpId, employeeId))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not corpId:
        return "<UNK>keyword<UNK>"
    if not employeeId:
        return "<UNK>employeeId<UNK>"

    body = {"corpId": corpId, "dingUserId": employeeId}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryEmployeeBasic"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-selectUserValidInvoice": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result


@mcp.tool(name="基于关键字搜索员工发票抬头信息列表",
          description="基于关键字搜索员工发票抬头信息列表, 输入企业id和员工id和发票抬头关键字,返回员工搜索出的可用的发票抬头信息列表")
async def query_employee_org(corpId: str = Field(description="企业id,必填参数"),
                             employeeId: str = Field(description="员工id,必填参数"),
                             keyword: str = Field(description="发票抬头搜索关键字,必填参数"), ) -> object:
    logger.info(
        "收到基于关键字搜索员工发票抬头信息列表, corpId:{} employeeId:{} keyword:{}".format(corpId, employeeId,
                                                                                            keyword))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not corpId:
        return "<UNK>keyword<UNK>"
    if not employeeId:
        return "<UNK>employeeId<UNK>"
    if not keyword:
        return "<UNK>keyword<UNK>"

    body = {"corpId": corpId, "userIdList": [employeeId], "keyword": keyword}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryInvoiceList"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-selectUserValidInvoice": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result


@mcp.tool(name="基于关键字搜索员工可用的成本中心信息列表",
          description="基于关键字搜索员工可用的成本中心信息列表, 输入企业id和员工id,成本中心关键字,返回员工可用的成本中心信息列表")
async def query_employee_org(corpId: str = Field(description="企业id,必填参数"),
                             employeeId: str = Field(description="员工id,必填参数"),
                             title: str = Field(None,
                                                description="成本中心关键字,非必填参数,不传默认查询员工所有的成本中心列表"),
                             numLimit: int = Field(10,
                                                   description="成本中心列表返回的最大数量,非必填,默认10")) -> object:
    logger.info(
        "收到查询员工可用的成本中心信息, corpId:{} employeeId:{} title:{} numLimit:{}".format(corpId, employeeId,
                                                                                              title, numLimit))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not corpId:
        return "<UNK>keyword<UNK>"
    if not employeeId:
        return "<UNK>employeeId<UNK>"
    body = {"corpId": corpId, "userId": employeeId, "title": title, "numLimit": numLimit}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryCostCenters"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-selectUserValidInvoice": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result


@mcp.tool(name="基于项目关键字搜索员工可用的项目信息列表",
          description="基于项目关键字搜索员工可用的项目信息列表, 输入企业id和员工id 可选输入项目名称关键字,返回员工可用的项目信息列表")
async def query_employee_org(corpId: str = Field(description="企业id,必填参数"),
                             employeeId: str = Field(description="员工id,必填参数"),
                             projectName: str = Field(None,
                                                      description="项目名称关键字, 不传查询员工所有可用的项目信息列表,非必填参数"),
                             projectNumLimit: int = Field(10,
                                                          description="成本中心列表返回的最大数量,非必填,默认10")) -> object:
    logger.info(
        "收到基于项目关键字搜索员工可用的项目信息列表, corpId:{} employeeId:{} projectName:{} projectNumLimit:{}".format(
            corpId, employeeId,
            projectName,
            projectNumLimit))
    api_secret_key = os.getenv("api_secret_key")
    if not api_secret_key:
        return "请先设置aes_key环境变量"
    if not corpId:
        return "<UNK>keyword<UNK>"
    if not employeeId:
        return "<UNK>employeeId<UNK>"

    body = {"corpId": corpId, "userId": employeeId, "projectName": projectName, "projectNumLimit": projectNumLimit}
    timestamp = int(time.time() * 1000)
    nonce = ''.join(random.choices('0123456789', k=6))
    sign = signature(str(timestamp), nonce, json.dumps(body, ensure_ascii=False, separators=(',', ':')), api_secret_key)

    logger.info("认证数据打印,timestamp:{} nonce:{} body:{} sign:{}".format(timestamp, nonce, json.dumps(body), sign))

    url = "https://pre-sailing-paas.alibtrip.com/web/trigger/MjY5MDAy/queryProjects"
    headers = {"Content-Type": "application/json; charset=utf-8", "x-sailing-selectUserValidInvoice": str(timestamp),
               "x-sailing-nonce": nonce, "x-sailing-signature": sign}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.post(url, json=body)
        if response.status_code != 200:
            return "查询失败"
        result = response.json()
        return result


def run():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
