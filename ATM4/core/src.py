import hashlib
import json
import random
from lib import commom
from lib.commom import get_logger
from conf import settings


def login():
    print('\n欢迎进入登录页面！\n')
    username = input('请输入用户名：').strip()
    code = ''.join((random.sample([str(i) for i in range(2, 10)], 2) + random.sample(
        [chr(i) for i in range(97, 123) if i != 108], 3)))
    usercode = input('请输入验证码\t{}\t:'.format(code)).strip()
    if usercode != code:
        print('验证码输入有误，请重新登录！')
        return
    count = 3
    while count > 0:
        if commom.checkname(username):
            password = input('请输入密码：').strip()
            str1 = str((lambda x: len(x))(username)) + '不信你能破解！'
            ret = hashlib.md5(str1.encode('utf-8'))
            ret.update(password.encode('utf-8'))
            password = ret.hexdigest()
            if commom.checkpwd(username, password):
                print('登录成功！')
                commom.loginin(username)
                settings.name = username
                return
            else:
                print('密码错误，请重新输入，您还有%s机会！' % (count - 1))
        else:
            print('不存在该用户，请重新输入！')
            break
        count -= 1


def register():
    print('\n欢迎进入注册页面！\n')
    register_dict = {}
    status = 1
    username = input('请您输入用户名（由字母数字组成）：').strip()
    code = ''.join((random.sample([str(i) for i in range(2, 10)], 2) + random.sample(
        [chr(i) for i in range(97, 123) if i != 108], 3)))
    usercode = input('请输入验证码\t{}\t:'.format(code)).strip()
    if usercode != code:
        print('验证码输入有误，请重新注册！')
        return
    if username.isalnum():
        if commom.checkname(username):
            print('用户名已存在，请重新注册！')
        else:
            register_dict['username'] = username
            password = input('请输入密码（不超过14个字符）：').strip()
            if 0 < len(password) < 15:
                str1 = str((lambda x: len(x))(username)) + '不信你能破解！'
                ret = hashlib.md5(str1.encode('utf-8'))
                ret.update(password.encode('utf-8'))
                password = ret.hexdigest()
                register_dict['password'] = password
                register_dict['money'] = 0
                date1 = input('请输入办卡年份（例如：2019）：').strip()
                date2 = input('请输入办卡月份（例如：01）：').strip()
                date3 = input('请输入办卡日（例如：01）：').strip()
                if date1.isdigit and date2.isdigit and date3.isdigit() and len(date1) == 4 and 0 < len(
                        date2) < 3 and 0 < len(date3) < 3:
                    if not commom.check_date(date1, date2, date3):
                        print('输入的时间超过了现实时间,请重新注册！')
                        return
                    if commom.check_date(date1, date2, date3) == ValueError:
                        print('日期格式不正确,请重新注册！')
                        return
                    register_dict['date'] = '{}-{}-{}'.format(date1, date2, date3)
                    register_dict['status'] = status
                    print('注册成功！')
                    get_logger('register').info('{}注册成功'.format(username))
                    with open(settings.db_path + username + '_paidgoods.json', encoding='utf-8', mode='w') as f3:
                        f3.write(json.dumps({}) + '\n')
                    with open(settings.db_path + username + '_unpaidgoods.json', encoding='utf-8', mode='w') as f4:
                        f4.write(json.dumps({}) + '\n')
                    with open(settings.db_path + username + '.json', encoding='utf-8', mode='w') as f1:
                        json.dump(register_dict, f1, ensure_ascii=False)
                    commom.billflow_tofile(0, '注册+', name=username)
                    settings.name = username
                    settings.flag = True
                    settings.flag1 = False
                    return
                else:
                    print('日期格式不正确，请重新注册！')
            else:
                print('密码过长，请重新注册！')

    else:
        print('用户名格式不正确，请重新注册！')


@commom.login_auth
def check():
    f1 = open(settings.db_path + settings.name + '.json', encoding='utf-8')
    check_dict = json.load(f1)
    print('您的余额为%s元。' % check_dict['money'])
    f1.close()
    return check_dict['money']


@commom.login_auth
def deposit():
    print('\n欢迎进入存钱页面！\n')
    money = input('请输入您要充值的金额：').strip()
    if money.isdigit():
        money = int(money)
        f1 = open(settings.db_path + settings.name + '.json', encoding='utf-8')
        deposit_dict = json.load(f1)
        deposit_dict['money'] += money
        f1.close()
        f2 = open(settings.db_path + settings.name + '.json', encoding='utf-8', mode='w')
        json.dump(deposit_dict, f2, ensure_ascii=False)
        f2.close()
        print('充值成功！目前您的余额为%s元。' % deposit_dict['money'])
        get_logger('deposit').info('{}充值{}元,余额{}元'.format(settings.name, money, deposit_dict['money']))
        commom.billflow_tofile(money, '存钱 +', name=settings.name)
        return
    else:
        print('请输入数字！')


@commom.login_auth
def money_change(para, para1, para2):
    f1 = open(settings.db_path + para + '.json', encoding='utf-8')
    f1_dict = json.load(f1)
    f1.close()
    if para2 == 'add':
        f1_dict['money'] += para1
    elif para2 == 'reduce':
        f1_dict['money'] -= para1
    f2 = open(settings.db_path + para + '.json', encoding='utf-8', mode='w')
    json.dump(f1_dict, f2, ensure_ascii=False)
    f2.close()


@commom.login_auth
def transfer():
    print('\n欢迎进入转账页面！\n')
    username = input('请您输入对方的账户名：').strip()
    if commom.checkname(username):
        money = input('请输入您要转账的金额：').strip()
        f1 = open(settings.db_path + settings.name + '.json', encoding='utf-8')
        f1_dict = json.load(f1)
        money1 = f1_dict['money']
        f1.close()
        if money.isdigit():
            money = int(money)
            if money1 >= money:
                money_change(settings.name, money, 'reduce')
                commom.billflow_tofile(money, '给%s转账-' % username, name=settings.name)
                money_change(username, money, 'add')
                commom.billflow_tofile(money, '%s给您转账+' % settings.name, name=username)
                get_logger('transfer').info('{}给{}转账{}元'.format(settings.name, username, money))  # 记录该文件的运行状态
                print('转账完成！')
            else:
                print('您的余额不足，转账失败！')
                return
        else:
            print('请输入数字！')
            return
    else:
        print('账户名不存在！')
        return


@commom.login_auth
def billflow():
    print('\n欢迎进入流水查询界面！\n')
    with open(settings.db_path + settings.name + '_billflow.json', encoding='utf-8') as f1:
        for line in f1:
            dic1 = json.loads(line)
            print('时间：{}\t{}{}元，余额{}元'.format(dic1['time'], dic1['ways'], dic1['money'], dic1['balance']))
    return


@commom.login_auth
def shopping():
    print('\n欢迎进入购物界面！\n')
    goods = []
    shopping_car = {}

    def print_shoppingcar():
        nonlocal shopping_car
        print('\n序号  商品名称  价格    数量')
        shopping_car = {i1: shopping_car[i1] for i1 in sorted(shopping_car)}
        for count, value in shopping_car.items():
            print(' {}      {}     {}       {}'.format(count + 1, value['name'], value['price'], value['mount']))

    with open(settings.product_path, encoding='utf-8') as f1:
        title_list = f1.readline().strip().split()
        for line in f1:
            dic = dict()
            line_list = line.strip().split()
            for i in range(len(title_list)):
                dic[title_list[i]] = line_list[i]
            goods.append(dic)
    for serial_number, goods_dict in enumerate(goods, start=1):
        print('{}\t{}\t{}'.format(serial_number, goods_dict['name'], goods_dict['price']))
    print('{}\t{}\n{}\t{}'.format('n/N', '结算', 'q/Q', '退出'))
    flag2 = True
    while flag2:
        choice = input('\n请输入商品序号，n/N结算，q/Q退出').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice in range(1, len(goods) + 1):
                if (choice - 1) not in shopping_car:
                    shopping_car[choice - 1] = {'name': goods[choice - 1]['name'], 'price': goods[choice - 1]['price'],
                                                'mount': 1}
                else:
                    shopping_car[choice - 1]['mount'] += 1
                print('您选择了以下商品:商品名称:{} \t 价格:{}, \t 数量：1,并成功添加到购物车！'.format(goods[choice - 1]['name'],
                                                                             goods[choice - 1]['price']))
            else:
                print('该商品不存在，请重新选择：')
        elif choice.upper() == 'N':
            while 1:
                print('\n您购物车里的商品如下：')
                print_shoppingcar()
                total_price = 0
                for dict1 in shopping_car.values():
                    total_price += int(dict1['price']) * dict1['mount']
                print('以上商品总价为：%s元' % total_price)
                money = check()
                if money >= total_price:
                    money -= total_price
                    print('\n您此次成功购买了如下商品：')
                    print_shoppingcar()
                    print('\n您此次一共消费了%s元。' % total_price)
                    print('\n您账户目前的余额是%d,欢迎下次光临！' % money)
                    get_logger('shopping').info(
                        '{}购买商品，消费{}元, 余额{}元'.format(settings.name, total_price, money))
                    money_change(settings.name, total_price, 'reduce')
                    commom.billflow_tofile(total_price, '购买商品-', name=settings.name)
                    with open(settings.db_path + settings.name + '_paidgoods.json', encoding='utf-8', mode='a') as f1:
                        f1.write(json.dumps(shopping_car) + '\n')
                    flag2 = False
                    break
                else:
                    choice1 = input('\n余额不足!还差%s元,存钱输入r/R,删除商品输入序号，退出购买输入q/Q：' % (total_price - money))
                    if choice1.isdigit():
                        choice1 = int(choice1)
                        if (choice1 - 1) in shopping_car:
                            shopping_car[choice1 - 1]['mount'] -= 1
                            if not shopping_car[choice1 - 1]['mount']:
                                del shopping_car[choice1 - 1]
                            print('删除成功！')
                        else:
                            print('没有该商品，请重新选择！')
                    elif choice1.upper() == 'R':
                        deposit()
                    elif choice1.upper() == 'Q':
                        print('您有以下商品未购买:')
                        print_shoppingcar()
                        print('您的未购买商品已被保存！')
                        with open(settings.db_path + settings.name + '_unpaidgoods.json', encoding='utf-8',
                                  mode='a') as f1:
                            f1.write(json.dumps(shopping_car) + '\n')
                        flag2 = False
                        break
                    else:
                        print('请输入数字！')
        elif choice.upper() == 'Q':
            print('您有以下商品未购买:')
            print_shoppingcar()
            print('您的未购买商品已被保存！')
            with open(settings.db_path + settings.name + '_unpaidgoods.json', encoding='utf-8', mode='a') as f1:
                f1.write(json.dumps(shopping_car) + '\n')
            break
        else:
            print('请您输入序号！')


@commom.login_auth
def paidgoods():
    print('\n欢迎进入已购买商品界面！\n')
    dic1 = {}
    with open(settings.db_path + settings.name + '_paidgoods.json', encoding='utf-8') as f1:
        for line in f1:
            dic2 = json.loads(line)
            for k, v in dic2.items():
                k = int(k)
                if k not in dic1:
                    dic1[k] = v
                else:
                    dic1[k]['mount'] += v['mount']
    print('您的已购买商品如下：\n序号  商品名称  价格    数量')
    dic1 = {i: dic1[i] for i in sorted(dic1)}  # 按照购物车字典的键排序
    for count, value in dic1.items():
        print(' {}      {}     {}       {}'.format(count + 1, value['name'], value['price'], value['mount']))
    return


@commom.login_auth
def unpaidgoods():
    print('\n欢迎进入心怡商品界面！\n')
    dic1 = {}
    with open(settings.db_path + settings.name + '_unpaidgoods.json', encoding='utf-8') as f1:
        for line in f1:
            dic2 = json.loads(line)
            for k, v in dic2.items():
                k = int(k)
                if k not in dic1:
                    dic1[k] = v
                else:
                    dic1[k]['mount'] += v['mount']
    print('您的心怡商品如下：\n序号  商品名称  价格    数量')
    dic1 = {i: dic1[i] for i in sorted(dic1)}  # 对购物车字典按照键重新排序
    for count, value in dic1.items():
        print(' {}      {}     {}       {}'.format(count + 1, value['name'], value['price'], value['mount']))
    return


def loginout():
    if settings.flag:
        settings.flag = False
        settings.flag1 = True
        f3 = open(settings.db_path + settings.name + '.json', encoding='utf-8')
        f3_dict = json.load(f3)
        f3_dict['status'] = 0
        f3.close()
        f4 = open(settings.db_path + settings.name + '.json', encoding='utf-8', mode='w')
        json.dump(f3_dict, f4, ensure_ascii=False)
        f4.close()
        print('\n您的账户已退出登录！')
        get_logger('loginout').info('{}退出登录'.format(settings.name))
    else:
        print('\n您没有登录账户，不需要退出登录！')
    return


def run():
    while 1:
        print('''
欢迎进入ATM4.0界面！\n
        1，登录
        2，注册
        3，查看余额
        4，存钱
        5，转账
        6，查看最近流水
        7，购物
        8，查看已购买商品
        9，查看心仪商品
        10，退出登录''')
        choice = input('\n请选择您想要的服务，输入q/Q退出登录同时关闭ATM：').strip()
        if choice.isdigit():
            choice = int(choice)
            if 2 < choice < 11:
                menu[choice]()
            elif (0 < choice < 3) and settings.flag1:
                menu[choice]()
            else:
                if 0 < choice < 3:
                    print('\n您已登录，请您先退出登录！')
                else:
                    print('\n没有您要的服务，请重新选择！')
        else:
            if choice.upper() == 'Q':
                loginout()
                print('\n已关闭ATM！')
                break
            else:
                print('\n请您输入数字！')


menu = {
    1: login,
    2: register,
    3: check,
    4: deposit,
    5: transfer,
    6: billflow,
    7: shopping,
    8: paidgoods,
    9: unpaidgoods,
    10: loginout,
}
