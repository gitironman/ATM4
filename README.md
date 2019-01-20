ATM V4.0.0
===========================

1，软件定位，软件的基本功能
模拟一个取款机，这个取款机不仅可以存钱，转账，等还可以跳转到购物页面，进行购物。

2，简要的使用说明
程序启动，页面显示下面内容供用户选择：
1，登录（可支持多个账户（非同时）登录）。
2，注册。
3，查看余额。
4，存钱。
5，转账。
6，查看最近流水。(涉及到钱的操作记录)
7，购物。
8，查看已购买商品。
9，查看心仪商品（添加到购物车未付款的商品）。
10，退出。
用户输入序号选择对应的功能；
与用户交互过程中，程序会显示提示，用户根据提示即可正常使用。

3，常见问题说明
（1）注册时，办卡时间需要用户输入，程序没有判断是否在现在的时间之前。（待添加）
（2）可以自己给自己转账
（3）用户没有使用购物功能的情况下，选择8或9只会显示一个商品标题，没有商品信息或提示。

###########环境依赖
python3.6.7（作者版本） 
或 python3以上版本

常用IDE运行starts.py即可
或用python解释器运行(作者用pycharm3.1 IDE运行starts.py启动程序)

###########部署步骤
无

###########目录结构描述                  
├── bin                         
│   └── starts.py              // 启动文件
├── conf                       
│   └──settings.py             // 配置文件
├── core                       
│   └── src.py                 // 主功能文件
├── db                        
│   └── product_info           // 购物车商品信息文件
│   └── username.json          // 以账户名命名的文件，存储用户账户信息。
│   └── username_*.json        // 分别为用户的流水、已购商品和心怡商品记录文件。
├── lib                        
│   └── commom.py              // 登录验证等公共组件
├── log                                       
│   └── boss.log               // 老板日志
│   └── staff.log              // 员工日志
└── Readme.md                   // 本帮助文件


###########V1.0.0 版本内容更新
1. 新功能     完成10个主要功能的函数，能正常使用
###########V2.0.0 版本内容更新
1. 新功能     软件开发规范化（分模块）
###########V3.0.0 版本内容更新
1. 新功能     嵌入log模块,重排购物车序号
###########V4.0.0 版本内容更新
1. 新功能     用json进行文件的读取和写入，取代eval
              hashlib.md5加密用户账户的密码
              登录、注册增加验证码功能
              判断办卡时间是否大于现实时间
