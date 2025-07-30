import requests
from typing import List, Optional, Any


def query_schedule(
    tt: str,
    start_timestamp: int = 1746892801000,
    end_timestamp: int = 1747497599000,
    yht_user_ids: List[str] = ["ad87259e-a585-4f68-a08e-a21cc7d8a5b8"],
    team_ids: Optional[List[str]] = None,
) -> Any:
    """
    查询日程接口
    :param start_timestamp: 开始时间戳（毫秒）
    :param end_timestamp: 结束时间戳（毫秒）
    :param yht_user_ids: 用户ID列表
    :param team_ids: 团队ID列表（可选）
    :return: 接口返回的json数据
    """
    url = 'https://c2.yonyoucloud.com/yonbip-ec-schedule/api/v2/magnet/batchTimeRange/schedules'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://c1.yonyoucloud.com',
        'referer': 'https://c1.yonyoucloud.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'yht_access_token': tt
    }
    
    data = {
        'startTimestamp': start_timestamp,
        'endTimestamp': end_timestamp,
        'yhtUserIds': yht_user_ids,
        'teamIds': team_ids or [],
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

