import httpx

from asgiref.sync import sync_to_async
from fastapi import Request
from user_agents import parse
from XdbSearchIP.xdbSearcher import XdbSearcher

from common.dataclasses import IpInfo, UserAgentInfo
from common.logger import logger
from core.config import settings
from core.path_conf import IP2REGION_XDB
from database.db_redis import redis_client


def get_request_ip(request: Request) -> str:
    """Получаем запрошенный ip-адрес"""
    real = request.headers.get("X-Real-IP")
    if real:
        ip = real
    else:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.client.host
    # 忽略 pytest
    if ip == "testclient":
        ip = "127.0.0.1"
    return ip


async def get_location_online(ip: str, user_agent: str) -> dict | None:
    """
    Получение ip-адресов онлайн является территориальным, доступность не может быть гарантирована, а уровень точности высок

    :param ip:
    :param user_agent:
    :return:
    """
    async with httpx.AsyncClient(timeout=3) as client:
        ip_api_url = f"http://ip-api.com/json/{ip}?lang=zh-CN"
        headers = {"User-Agent": user_agent}
        try:
            response = await client.get(ip_api_url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Не удалось получить ip-адрес онлайн, сообщение об ошибке：{e}")
            return None


@sync_to_async
def get_location_offline(ip: str) -> dict | None:
    """
    Получение ip-адреса в автономном режиме является территориальным, точность не может быть гарантирована, и он доступен на 100%
    :param ip:
    :return:
    """
    try:
        cb = XdbSearcher.loadContentFromFile(dbfile=IP2REGION_XDB)
        searcher = XdbSearcher(contentBuff=cb)
        data = searcher.search(ip)
        searcher.close()
        data = data.split("|")
        # logger.error(data)
        if len(data) < 4:
            logger.error(f"Неверный формат данных для IP: {ip}, данные: {data}")
            return None
        return {
            "country": data[0] if data[0] != "0" else None,
            "regionName": data[2] if data[2] != "0" else None,
            "city": data[3] if data[3] != "0" else None,
        }
    except Exception as e:
        logger.error(
            f"Ошибка автономного получения территории ip-адреса, сообщение об ошибке：{e}"
        )
        return None


async def parse_ip_info(request: Request) -> IpInfo:
    country, region, city = None, None, None
    ip = get_request_ip(request)
    location = await redis_client.get(f"{settings.IP_LOCATION_REDIS_PREFIX}:{ip}")
    if location:
        country, region, city = location.split(" ")
        return IpInfo(ip=ip, country=country, region=region, city=city)
    if settings.IP_LOCATION_PARSE == "online":
        location_info = await get_location_online(ip, request.headers.get("User-Agent"))
    elif settings.IP_LOCATION_PARSE == "offline":
        location_info = await get_location_offline(ip)
    else:
        location_info = None
    if location_info:
        country = location_info.get("country")
        region = location_info.get("regionName")
        city = location_info.get("city")
        await redis_client.set(
            f"{settings.IP_LOCATION_REDIS_PREFIX}:{ip}",
            f"{country} {region} {city}",
            ex=settings.IP_LOCATION_EXPIRE_SECONDS,
        )
    return IpInfo(ip=ip, country=country, region=region, city=city)


def parse_user_agent_info(request: Request) -> UserAgentInfo:
    user_agent = request.headers.get("User-Agent")
    _user_agent = parse(user_agent)
    os = _user_agent.get_os()
    browser = _user_agent.get_browser()
    device = _user_agent.get_device()
    return UserAgentInfo(user_agent=user_agent, device=device, os=os, browser=browser)
