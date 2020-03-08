import json
import requests


class Client_Public():
    """
    """
    @classmethod
    def mock_request(cls, url, body):
        """
            模拟请求.
        """
        headers = {
            'content-type': "application/json"
            # 'content-type': 'charset=utf8',
            # 'content-type': 'charset=gb2312'
        }

        bodyJsonStr = json.dumps(body)
        print(bodyJsonStr)

        # 发起请求.
        response = requests.post(
            url, data=json.dumps(body), headers=headers
        )

        # 打印应答结果.
        print(
            response.content.decode("unicode_escape")
            # response.content
        )


