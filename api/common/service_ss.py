# coding:utf-8
import json
import grequests
from django.conf import settings

'''
content['data'] 的内容：
{
        "key": "55b5d107f0034968ae57edd9d3f16c04",
        "filename": "GsonUtils.java",
        "content_type": "text/x-java-source",
        "size": 728,
        "md5sum": "9e41f72633c06f3900491f62262db9a7",
        "created_at": "2019-01-21T04:55:10.777",
        "app": "medieco",
        "access_count": 1,
        "last_access": "2019-01-21T07:41:01.796",
        "url": "文件 url ，可能含有一个短时间内有效的 token，所以只能在短时间内使用"
}
'''


def get_one_file_info(file_key):
    responses = _file_info([file_key])
    if responses[0] and responses[0].status_code == 200:
        content = json.loads(responses[0].content)
        return content['data']
    else:
        return None


def get_many_files_info(file_keys):
    responses = _file_info(file_keys)
    return [json.loads(res.content)['data'] for res in responses if (res and res.status_code == 200)]


'''
文档：https://github.com/kennethreitz/grequests

grequests 异步请求库
grequests get、post 等是异步方法
grequests map 是同步方法

@:param file_keys array
'''


def _file_info(file_keys):
    url_template = settings.STORAGE_SERVICE_BASE_URL + '/ss/v1/files/{0}'
    rs = (grequests.get(url_template.format(file_key)) for file_key in file_keys)
    # 这里返回一个 response 数组
    responses = grequests.map(rs)
    return responses
