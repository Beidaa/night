import random
from time import localtime
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os
 

res = get('http://myip.ipip.net', timeout=5).text
print(res)
def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)
 
 
def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token
 
 
def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    key="21da10412b9240dba830a492de395b2b"
    # 获取地区的location--id
    location_id = "101230207"
    weather_url = "https://devapi.qweather.com/v7/weather/3d?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # daily.sunset 日落时间
    sunset2 = response["daily"][2]["sunset"]
    print (sunset2)
    # daily.tempMax 预报当天最高温度
    tempMax2=response["daily"][2]["tempMax"]
#    daily.tempMin  预报当天最低温度
    tempMin2=response["daily"][2]["tempMin"]
#daily.textDay 预报白天天气状况文字描述
    textDay2=response["daily"][2]["textDay"]
#daily.windScaleDay 预报白天风力等级
    windScaleDay2=response["daily"][2]["windScaleDay"]
    #daily.uvIndex 紫外线强度指数
    uvIndex2=response["daily"][2]["uvIndex"]

    #tomorrow
    sunset1 = response["daily"][1]["sunset"]
    print (sunset1)
    # daily.tempMax 预报当天最高温度
    tempMax1=response["daily"][1]["tempMax"]
#    daily.tempMin  预报当天最低温度
    tempMin1=response["daily"][1]["tempMin"]
#daily.textDay 预报白天天气状况文字描述
    textDay1=response["daily"][1]["textDay"]
#daily.windScaleDay 预报白天风力等级
    windScaleDay1=response["daily"][1]["windScaleDay"]
    #daily.uvIndex 紫外线强度指数
    uvIndex1=response["daily"][1]["uvIndex"]


    return sunset2,tempMax2,tempMin2,textDay2,windScaleDay2,uvIndex2,sunset1,tempMax1,tempMin1,textDay1,windScaleDay1,uvIndex1

 
 
def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 获取农历生日的今年对应的月和日
        try:
            birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        except TypeError:
            print("请检查生日的日子是否在今年存在")
            os.system("pause")
            sys.exit(1)
        birthday_month = birthday.month
        birthday_day = birthday.day
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
 
    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day
 
 
# def get_ciba():
#     url = "http://open.iciba.com/dsapi/"
#     headers = {
#         'Content-Type': 'application/json',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
#     }
#     r = get(url, headers=headers)
#     note_en = r.json()["content"]
#     note_ch = r.json()["note"]
#     return note_ch, note_en
def get_ciba():
    url = "http://api.tianapi.com/saylove/index?key=4bd63a1e9f1b96e518d2a9857359a3f1"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en1 = r.json()["newslist"]
    note_en2=note_en1[0]
    note_en=note_en2["content"]
    
    # note_ch = r.json()["note"]
    return  note_en
 
 
def send_message(to_user, access_token, region_name, weather, temp, wind_dir,note_en,note_ch):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "region": {
                "value": region_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "temp": {
                "value": temp,
                "color": get_color()
            },
            "wind_dir": {
                "value": wind_dir,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {
                "value": note_ch,
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value["birthday"], year, today)
        if birth_day == 0:
            birthday_data = "今天{}生日哦，祝{}生日快乐！".format(value["name"], value["name"])
        else:
            birthday_data = "距离{}的生日还有{}天".format(value["name"], birth_day)
        # 将生日数据插入data
        data["data"][key] = {"value": birthday_data, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)
def get_marryme():
    dic=['1.志不求易者成，事不避难者进。','2.所有成绩的取得，无不源于奋勇拼搏；所有创新的突破，无不映照精神力量。','3.在新的伟大征程上奋勇前进，必须保持战略定力；在新的伟大征程上奋勇前进，必须坚定历史自信；在新的伟大征程上奋勇前进，必须鼓足奋斗干劲。',

'4.历史的画卷，在砥砺前行中铺展；时代的华章，在接续奋斗里书写。',

'5.苦，能磨砺人的意志；苦，能升华人的境界；苦，也能锻造人的精神。',

'6.这一则“快递故事”的背后，是无所不在的信息网，是四通八达的交通网，是高效运行的物流网，是智能精准的算力支撑，更是一个物畅其流的中国。',

'7.要保持平稳健康的经济环境、国泰民安的社会环境、风清气正的政治环境。',

'8.为中国人民谋幸福、为中华民族谋复兴，致力于为人类谋进步、为世界谋大同，天下为公，人间正道。',

'9.真理光芒穿越时空，思想旗帜引领前路。',

'10.人世间没有一帆风顺的事业，历史总是在跌宕起伏甚至曲折中前进。',

'11.百年风云激荡走过壮阔征程，百年不懈奋斗铸就世纪伟业，百年上下求索作出伟大贡献。',

'12.走过苦难辉煌的过去，走在日新月异的现在，走向光明宏大的未来。',

'13.文化因创新而辉煌，文明因发展而精彩。',

'14.有多清醒的认识，就会有多坚定的选择；有多崇高的信仰，就会有多勇毅的行动。',

'15.大党之大、大国之大，不在于体量大、块头大、拳头大，而在于胸襟大、格局大、担当大。面向未来，我们将一如既往为世界和平安宁作贡献，一如既往为世界共同发展作贡献，一如既往为世界文明交流互鉴作贡献！',

'16.良渚遗址的考古发现，为中华五千年文明史增添实证依据；二里头遗址的发掘，勾勒出“华夏第一王都”的恢宏气象；三星堆遗址考古又有重要发现，许多珍贵文物“沉睡三千年，一醒惊天下”……',

'17.山高水长，不改的是守护文化根脉的赤子之心；斗转星移，不变的是弘扬民族精神的如磐信念。',

'18.沧桑砥砺正道，历史昭示未来。','1.风好正是扬帆时，不待扬鞭自奋蹄。',

'2.善弈者谋势，善谋者致远。',

'3.茫茫九脉流中国，纵横当有凌云笔。',

'4.却顾所来径，苍苍横翠微。',

'5.青绿山水染黛色，溢彩流光化斑斓。',

'6.烈火炼真金，苦难铸辉煌。',

'7.追风赶月莫停留，平芜尽处是春山。',
'8.天下之势不盛则衰，天下之治不进则退。',

'9.鸟欲高飞先振翅，人求上进先读书。',

'10.善学者尽其理，善行者究其难。','1. 人生的境遇各不相同，奋起的背影何其相似。',

'2. 让人民生活幸福是‘国之大者’。',

'3. 和平犹如空气和阳光，受益而不觉，失之则难存。',

'4. 信仰、信念、信心是最好的防腐剂。',
'5. 理想信念就是共产党人精神上的‘钙’，没有理想信念，理想信念不坚定，精神上就会‘缺钙’，就会得‘软骨病’。',

'6. 就业为民生之本，是经济的“晴雨表”。',

'7. 一个人的成长底色，由所读之书来铺陈。而读书的多寡，也在一定程度上决定了心灵家园的广袤或贫瘠。',

'8. 与贫困作斗争，既是物质的角力，也是精神的对垒。',

'9. 做事靠谱、谋事有基、成事有道。',

'10. 天下事，勇于担当，成事方可冀。勇于担当，还要善于担当。',

'11. 环境好，则人才聚、事业兴。',

'12. 一系列惠企纾困政策落地生效，正为更多中小企业“活血补气”。',

'13. 为“擦亮”蓝天，“保卫”碧水，中国始终是坚定的行动派和实干家。',

'14. 知识就是力量，人才就是未来，创新事业呼唤创新人才。',

'15. 引人就是引“智”，揽才就是汇“贤”。',

'16. 揽才，也应多元。“用一贤人则群贤毕至，见贤思齐就蔚然成风。”',

'17. 阅读是秉心之烛火，去探访古今智者仁人的精神空间。',

'18. 腹有诗书气自华，一个人的气质里藏着读过的书、走过的路。',

'19. 阅读是有情怀的文化体验，是有温度的精神旅行。',

'20. “智者阅读群书，亦阅历人生。”',

'21. 不断增强做中国人的志气、骨气、底气。',

'22. 实现了从“沙进人退”到“绿进沙退”“人沙和谐”的历史性转变。',

'23. 目标决定行动，行动成就未来。',
'24. 巩固供应链、产业链、数据链、人才链，构建开放型世界经济。',


'25. 想群众之所想、急群众之所急、解群众之所困。',

'26. 没有比人更高的山，没有比脚更长的路。',

'27. 实践发展永无止境，解放思想永无止境，改革开放永无止境。',

'28. 深入开展维护“舌尖上”“脚底下”安全。',

'29. 充分发挥领导班子的“火车头”作用和领导干部的“头雁效应”。',

'30. 认清“舍”与“得”的关系，办好“减”与“增”的大事。',

'31. 为梦想而不懈奋斗，谁都了不起。',

'32. 唯有精神上站得住、站得稳，一个民族才能在历史洪流中屹立不倒、挺立潮头。',

'33. 对耕、种、管、收等环节，实行全流程或“菜单式”托管服务。',

'34. 法治社会，有法必依、违法必究，任何人都没有法外特权。',

'35. “大胆试、大胆闯、自主改”，同时必须“可复制、可推广”。',

'36. “照镜子、正衣冠、洗洗澡、治治病”，集中解决“四风”问题。',

'37. “党面临的‘赶考’远未结束。”',

'38. 每逢“节点”就成为作风建设的“考点”。',

'39. 八项规定“一子落”，作风建设“满盘活”。',

'40. “对‘国之大者’要心中有数”；“心怀‘国之大者’，不断提高政治判断力、政治领悟力、政治执行力”。',

'41. 加快推动投资审批权责“一张清单”、审批数据“一体共享”、审批事项“一网通办”。',

'42. 人在事上练，刀在石上磨。',

'43. 根系向下，是为了扎进土壤、吸取营养；干部下沉，是为了和群众交心、帮群众办事。',

'44. 将双脚扎进泥土，青春在磨砺中格外茁壮。',

'45. 年轻干部做到“想干事、能干事、干成事”，就要在不断解决问题、破解难题中，加强思想淬炼、政治历练、实践锻炼、专业训练。',

'46. 越是基层一线和艰苦地区，越能让人经风雨见世面；越是复杂局面和急难险重任务，越能给人以“重担压身”的锻炼。',

'47. 中心组学习具有“风向标”和“排头兵”作用。',

'48. 真正管用而有效的法律，不只写在纸上，更要写在人们心里。',

'49. 法律信仰的形成，离不开法治文化的滋养和熏陶。',
'50. 从最坏处着眼，做最充分的准备，朝好的方向努力，争取最好的结果。',

'51. 下好先手棋，打好主动仗。',

'52. 在扶危济困中尽显“绣花情”，在排忧解难中淬炼“绣花技”，在急难险重中练就“绣花功”。',

'53. 全力缩短“说了”和“做了”、“发文了”和“落实了”、“开会研究了”和“问题解决了”、“任务分解了”和“工作完成了”之间的距离。',

'54. 人无精神则不立，国无精神则不强。革命精神是党和国家的宝贵财富。',

'55. 培养更多高素质技术技能人才、能工巧匠、大国工匠。',

'56. 思想是行动的先导，只有认识到位，行动才会自觉主动。',

'57. “破案攻坚”“打伞破网”“打财断血”，以“问题整改”提质、以“组织建设”强基。',

'58. “阅读存折”助力书香社会建设。',

'59. “奋斗终身”，就是生命不息、奋斗不止。',

'60. 党性是党员干部立身、立业、立言、立德的基石，必须在严格的党内生活锻炼中不断增强。',

'61. 发力“双循环”，迈步“高质量”。',

'62. 用“闯”的精神、“创”的劲头、“干”的作风，蹄疾步稳开新局。',

'63. 只有与历史同步伐、与时代共命运的人，才能赢得光明的未来。',

'64. 激发出来的信念信心和热情激情，转化为攻坚克难、干事创业的强大动力和实际成效。',

'65. 既要出重拳“当下改”，也要建制度“长久立”。',
'66. 纠正重“痕”不重“绩”等问题。',

'67. 好的带头人是发展的“领头雁”，能以上率下，把准方向，阔步前进；是前行的“主心骨”，与群众一起想办法、拿主意，敢啃硬骨头；是乡亲的“贴心人”，能公而忘私，与群众同甘共苦。',
'68. 一个村子建设得好，关键要有一个好党支部。',

'69. 一朵浪花，只有汇入大江大河才不会干涸。',

'70. 一个村庄，只有跟着时代节拍才能不断汇聚发展力量。',

'71. 营商环境是生产力，也是竞争力。',

'72. 保持“大战”状态、“大考”作风，在抓好常态化科学精准防控的同时，正拿出“拼”“抢”“实”的状态，努力把疫情造成的损失补回来、把应有增长追回来。',

'73. 职业教育，既关乎国计，也涉及民生。',

'74. 政策不“急转弯”，引导形成市场合理预期',

'75. 为什么人的问题，是检验一个政党、一个政权性质的试金石。',

'76. 勇于担苦、担难、担重、担险，才能培塑锲而不舍的坚忍力。',

'77. 历史和现实已经证明，无论是枪林弹雨还是风刀霜剑，无论是摸着石头过河还是闯关夺隘，前进道路越是艰辛，越是中流浪急、半山坡陡，中国共产党人迸发出的精神力量就越强大。',

'78. 通过拓宽“乡间路”、疏通“梗阻路”、补齐“断头路”等举措，完善山区道路交通网，打通农村公路微循环，解决山区群众“出行难、运输难”问题，带动山区产业发展和村民稳步增收，助力乡村振兴。',

'79. 历史和实践充分证明，科学把握历史规律，按历史规律办事，我们就能无往而不胜。',

'80. 质量兴农、绿色兴农、品牌强农，强化科技支撑是关键。',

'81. 从“人拉肩扛”到全程机械化，从“靠经验”到“靠数据”，传统农业正朝着智慧农业转变。',



'82. 中国现代化离不开农业现代化，农业现代化关键在科技、在人才。',
'83. 神州大地投资潮涌，重大项目建设正酣。',

'84. “自强不息、止于至善”追求卓越从未停歇。',

'85. 我们要心怀“国之大者”，坚定不移推动创新、协调、绿色、开放、共享发展。',

'86. 没有一个人被放弃，没有一个生命被忽视',

'87. 白衣为甲，逆行出征；临危不惧，舍生忘死。',

'88. 与疫情赛跑，基建速度让世界惊叹；疫后重振，同样跑出了武汉速度。',

'89. 从“不计报酬，无论生死”的请战书，到“哪里需要我们，我们就到哪里去”的宣誓词；从“我是党员，我先上”的豪言壮语，到“是我的病人，我不管谁管”的责任担当，在湖北抗疫战场，任何时候，任何地方，压不垮的是不屈不挠的精神力量，冲得上的是勇于牺牲的平凡英雄。',

'90. 做到既重视“米袋子”“菜篮子”，也重视“钱袋子”。',

'91. 思想就是力量。一个民族要走在时代前列，就一刻不能没有理论思维，一刻不能没有思想指引。',

'92. .崇尚英雄、缅怀先烈，激扬英雄精神、砥砺家国情怀，让理想之光不灭、信念之火不熄。',


'93. “生是为中国，死是为中国，一切听之而已。”',

'94. 英雄壮举，源自坚定如钢铁的信仰，千磨万击还坚劲。',
'95. 英雄壮举，源自为国为民的赤子情怀，虽九死其犹未悔。',

'96. 变换的是大地的色彩，不变的是永恒的初心。',

'97. “得一官不荣，失一官不辱，勿道一官无用，地方全靠一官；穿百姓之衣，吃百姓之饭，莫以百姓可欺，自己也是百姓。”',

'98. 以百姓心为心、坚持当“老百姓的官”，全心全意为人民服务、为老百姓办事。',

'99. 党的干部须臾不能忘自己是“人民公仆”，须臾不能忘公仆只能姓“公”、不能姓“私”。',

'100. 心无百姓莫为官。']
    b=len(dic)
    print(b)

    a=random.randint(0,127)
    return  dic[a]
 
if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)
 
    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入地区获取天气信息
    region = config["region"]
    sunset2,tempMax2,tempMin2,textDay2,windScaleDay2,uvIndex2,sunset1,tempMax1,tempMin1,textDay1,windScaleDay1,uvIndex1 = get_weather(region)

        # 获取词霸每日金句
    note_en = get_ciba()
    note_ch =get_marryme()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, region, sunset2,tempMax2,tempMin2,textDay2,windScaleDay2,uvIndex2,sunset1,tempMax1,tempMin1,textDay1,windScaleDay1,uvIndex1, note_ch)
    os.system("pause")
