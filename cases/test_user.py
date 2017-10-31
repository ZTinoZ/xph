# encoding:utf-8

import requests, json, nose, sys
sys.path.append('..')
from data.read_cases import *
from configs.common1 import *
from nose.tools import nottest, istest, assert_equal


class TestUser:

    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown_class(self):
        # data = xlrd.open_workbook(r'../data/cases.xls')
        # table = data.sheet_by_name(module_name='user')
        # num = table.cell(1, 7).value
        # del_app_user('')
        pass

    # APP用户注册
    @nottest
    def test_1_app_register(self, module_name='user', phone='15000000000'):

        # 获取验证码
        sign = get_sha1(phone)
        json_param = {"sign": sign, "phone": phone}
        url = 'http://192.168.2.200/sms/register'
        r = requests.post(url=url, json=json_param)
        if r.status_code == 200:
            sms = get_sms(phone)
        elif r.status_code == 400:
            raise '该手机号当天发送短信已超过10条'
        else:
            raise '获取验证码失败'

        x1 = read_xls1(module_name)
        param1 = tuple(x1)
        x2 = read_xls2(param1)
        param2 = tuple(x2)
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户注册':
                json_param = json.JSONDecoder().decode(param2[i][4])
                json_param['verification_code'] = sms
                r = requests.post(url=param2[i][3], json=json_param, headers=base_headers)
                message = param2[i][2].encode('utf-8') + 'Failed!'
                self.assertEqual(param2[i][5], r.status_code, message)
            else:
                break

    # APP用户登录
    def test_2_app_login(self, module_name='user'):
        x1 = read_xls1(module_name)
        param1 = tuple(x1)
        x2 = read_xls2(param1)
        param2 = tuple(x2)
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户登录':
                json_param = json.JSONDecoder().decode(param2[i][4])
                r = requests.post(url=param2[i][3], json=json_param, headers=base_headers)
                c = r.json()
                message = param2[i][2].encode('utf-8') + 'Failed!'
                assert_equal(param2[i][5], r.status_code, message)
            else:
                continue

    # APP用户修改用户信息

    # APP用户修改密码


if __name__ == '__main__':
    nose.main()