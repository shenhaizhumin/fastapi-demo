import requests

'''
curl 'https://dicastal.realibox.com/api/v4/upload_policy/sources?uuid=7e57f7c0-7616-4659-9fc7-f6f8815f4fe4&name=%E8%8C%B6%E5%A3%B6.fbx&scene_uid=5924baa3a64095730589e2d97c63edd63d65885c&uv=0&clear=0&type=0&reduce=100&bake_ao=0' \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://dicastal.realibox.com/xr/editor/5924baa3a64095730589e2d97c63edd63d65885c/?lang=zh' \
  -H 'Cookie: session=54c1825d-bd44-4309-a8b7-5334e7433cbe; Hm_lvt_b808253e6b39183060a095f098973c5f=1594968849,1595215539; Hm_lvt_85fe9162efeefa276d84da75c3bb6c0a=1594970505,1595049205,1595216385; username=6x9xk; Hm_lpvt_85fe9162efeefa276d84da75c3bb6c0a=1595225755; Hm_lpvt_b808253e6b39183060a095f098973c5f=1595227459' \
  --compressed
'''
upload_url = 'http://127.0.0.1:8031/api/v4/upload_policy/project?uuid=d62cf413-4589-45cd-b16c-1af0acb1779c' \
             '&scene_uid=d62cf413-4589-45cd-b16c-1af0acb1779c' \
             '&scene_name=茶壶' \
             '&name=茶壶.fbx' \
             '&path=/项目/zb/1222' \
             '&uv=0' \
             '&clear=0' \
             '&type=0' \
             '&reduce=100' \
             '&bake_ao=0'
# 编辑器上传模型接口
editor_upload_url = 'http://127.0.0.1:8031/api/v4/upload_policy/sources?' \
                    'uuid=7e57f7c0-7616-4659-9fc7-f6f8815f4fe4' \
                    '&name=%E8%8C%B6%E5%A3%B6.fbx' \
                    '&scene_uid=5924baa3a64095730589e2d97c63edd63d65885c' \
                    '&uv=0' \
                    '&clear=0' \
                    '&type=0' \
                    '&reduce=100' \
                    '&bake_ao=0'
scenes_url = 'http://127.0.0.1:8031/api/v4/scenes/{scene_uid}'
# headers = {
#     'Cookie': 'session=54c1825d-bd44-4309-a8b7-5334e7433cbe; '
#               'Hm_lvt_b808253e6b39183060a095f098973c5f=1594968849,1595215539; '
#               'Hm_lvt_85fe9162efeefa276d84da75c3bb6c0a=1594970505,1595049205,1595216385; '
#               'username=6x9xk; '
#               'Hm_lpvt_b808253e6b39183060a095f098973c5f=1595221344; '
#               'Hm_lpvt_85fe9162efeefa276d84da75c3bb6c0a=1595225755'
# }
# ickGxLUy
headers = {
    'Cookie': 'session=67f38624-1d51-4324-9ec5-be3f12ef2d3c; '
              'Hm_lvt_b808253e6b39183060a095f098973c5f=1594968849,1595215539; '
              'Hm_lvt_85fe9162efeefa276d84da75c3bb6c0a=1594970505,1595049205,1595216385; '
              'username=ickGxLUy; '
              'Hm_lpvt_b808253e6b39183060a095f098973c5f=1595221344; '
              'Hm_lpvt_85fe9162efeefa276d84da75c3bb6c0a=1595225755'
}


def test_upload():
    '''
    批量创建项目--上传模型 发签名的接口。
    :return:
    '''
    resp = requests.get(upload_url, headers=headers)
    print(resp.json())


def test_api_v4_scenes_scene_uid(url, scene_uid):
    '''
        获取项目资源的接口
    :param url:
    :param scene_uid:
    :return:
    '''
    resp = requests.get(url.format(scene_uid=scene_uid), headers=headers)
    print(resp.json())


if __name__ == '__main__':
    test_upload()
    # test_api_v4_scenes_scene_uid(scenes_url, 'cf3992d62fa084c8d149ea8779210877ba6c14dc')
    ls = [0,1, 2, 3]
    for i in ls:
        if not i:
            continue
        print(i)
