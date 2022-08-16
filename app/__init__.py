from flask import Flask, render_template, request
from flask_cors import CORS
import pymysql
import json
# ======================================================================
# 以下為投資組合
import pandas as pd
from pandas_datareader import data
import requests
import csv
import time as ti
from datetime import datetime
import datetime  as dt
# ======================================================================
# 以下為選股
import bs4
from bs4 import BeautifulSoup
# ======================================================================
# 熱度圖
import numpy as np
import finlab
from finlab import data as data1
import plotly.express as px
import plotly
import plotly.graph_objects as go
# ======================================================================


# 上櫃清單&辨識函式(輸出為: 編號+.tw或.two)
uplist = ['1240', '1258', '1259', '1264', '1268', '1336', '1565', '1569', '1570', '1580', '1584', '1586', '1591', '1593', '1595', '1599', '1742', '1777', '1781', '1784', '1785', '1788', '1796', '1799', '1813', '1815', '2035', '2061', '2063', '2064', '2065', '2066', '2067', '2070', '2221', '2230', '2235', '2596', '2640', '2641', '2643', '2718', '2719', '2724', '2726', '2729', '2732', '2734', '2736', '2740', '2743', '2745', '2752', '2754', '2755', '2756', '2916', '2924', '2926', '2937', '2947', '3064', '3066', '3067', '3071', '3073', '3078', '3081', '3083', '3085', '3086', '3088', '3089', '3093', '3095', '3105', '3114', '3115', '3118', '3122', '3128', '3131', '3141', '3147', '3152', '3162', '3163', '3169', '3171', '3176', '3178', '3188', '3191', '3202', '3205', '3206', '3207', '3211', '3213', '3217', '3218', '3219', '3221', '3224', '3226', '3227', '3228', '3230', '3232', '3234', '3236', '3252', '3259', '3260', '3264', '3265', '3268', '3272', '3276', '3284', '3285', '3287', '3288', '3289', '3290', '3293', '3294', '3297', '3303', '3306', '3310', '3313', '3317', '3322', '3323', '3324', '3325', '3332', '3339', '3349', '3354', '3357', '3360', '3362', '3363', '3372', '3373', '3374', '3379', '3388', '3390', '3402', '3426', '3434', '3438', '3441', '3444', '3455', '3465', '3466', '3479', '3483', '3484', '3489', '3490', '3491', '3492', '3498', '3499', '3508', '3511', '3512', '3516', '3520', '3521', '3522', '3523', '3526', '3527', '3529', '3531', '3537', '3540', '3541', '3546', '3548', '3551', '3552', '3555', '3556', '3558', '3564', '3567', '3570', '3577', '3580', '3581', '3587', '3594', '3597', '3609', '3611', '3615', '3623', '3624', '3625', '3628', '3629', '3630', '3631', '3632', '3642', '3646', '3652', '3663', '3664', '3666', '3672', '3675', '3680', '3684', '3685', '3687', '3689', '3691', '3693', '3707', '3709', '3710', '3713', '4102', '4105', '4107', '4109', '4111', '4113', '4114', '4116', '4120', '4121', '4123', '4126', '4127', '4128', '4129', '4130', '4131', '4138', '4139', '4147', '4153', '4154', '4157', '4160', '4161', '4162', '4163', '4167', '4168', '4171', '4173', '4174', '4175', '4183', '4188', '4192', '4198', '4205', '4207', '4303', '4304', '4305', '4401', '4402', '4406', '4413', '4416', '4417', '4419', '4420', '4430', '4432', '4433', '4502', '4503', '4506', '4510', '4513', '4523', '4527', '4528', '4529', '4530', '4533', '4534', '4535', '4538', '4541', '4542', '4543', '4549', '4550', '4554', '4556', '4558', '4561', '4563', '4568', '4577', '4580', '4609', '4702', '4706', '4707', '4711', '4712', '4714', '4716', '4721', '4726', '4728', '4729', '4735', '4736', '4741', '4743', '4744', '4745', '4747', '4754', '4760', '4767', '4768', '4804', '4806', '4903', '4905', '4907', '4908', '4909', '4911', '4923', '4924', '4931', '4933', '4939', '4944', '4945', '4946', '4950', '4953', '4966', '4971', '4972', '4973', '4974', '4979', '4987', '4991', '4995', '5009', '5011', '5013', '5014', '5015', '5016', '5201', '5202', '5205', '5206', '5209', '5210', '5211', '5212', '5213', '5220', '5223', '5227', '5228', '5230', '5236', '5245', '5251', '5263', '5272', '5274', '5276', '5278', '5281', '5287', '5289', '5291', '5299', '5301', '5302', '5309', '5310', '5312', '5314', '5315', '5321', '5324', '5328', '5340', '5344', '5345', '5347', '5348', '5351', '5353', '5355', '5356', '5364', '5371', '5381', '5383', '5386', '5392', '5398', '5403', '5410', '5425', '5426', '5432', '5438', '5439', '5443', '5450', '5452', '5455', '5457', '5460', '5464', '5465', '5468', '5474', '5475', '5478', '5481', '5483', '5487', '5488', '5489', '5490', '5493', '5498', '5508', '5511', '5512', '5514', '5516', '5520', '5523', '5529', '5530', '5536', '5543', '5601', '5603', '5604', '5609', '5701', '5703', '5704', '5820', '5864', '5878', '5902', '5903', '5904', '5905', '6015', '6016', '6020', '6021', '6023', '6026', '6101', '6103', '6104', '6111', '6113', '6114', '6118', '6121', '6122', '6123', '6124', '6125', '6126', '6127', '6129', '6130', '6134', '6138', '6140', '6143', '6144', '6146', '6147', '6148', '6150', '6151', '6154', '6156', '6158', '6160', '6161', '6163', '6167', '6169', '6170', '6171', '6173', '6174', '6175', '6179', '6180', '6182', '6185', '6186', '6187', '6188', '6190', '6194', '6195', '6198', '6199', '6203', '6204', '6207', '6208', '6210', '6212', '6217', '6218', '6219', '6220', '6221', '6222', '6223', '6227', '6228', '6229', '6231', '6233', '6234', '6236', '6237', '6240', '6241', '6242', '6244', '6245', '6246', '6247', '6248', '6259', '6261', '6263', '6264', '6265', '6266', '6270', '6274', '6275', '6276', '6279', '6284', '6287', '6290', '6291', '6292', '6294', '6404', '6411', '6417', '6418', '6419', '6425', '6432', '6435', '6441', '6446', '6457', '6461', '6462', '6465', '6469', '6470', '6472', '6482', '6485', '6486', '6488', '6492', '6494', '6496', '6499', '6506', '6508', '6509', '6510', '6512', '6514', '6516', '6523', '6527', '6530', '6532', '6535', '6538', '6542', '6546', '6547', '6548', '6556', '6560', '6561', '6568', '6569', '6570', '6574', '6576', '6577', '6578', '6588', '6589', '6590', '6593', '6594', '6596', '6603', '6609', '6612', '6613', '6615', '6616', '6624', '6629', '6640', '6642', '6643', '6649', '6651', '6654', '6661', '6662', '6664', '6667', '6679', '6680', '6683', '6684', '6690', '6693', '6697', '6703', '6712', '6716', '6721', '6727', '6728', '6732', '6733', '6735', '6741', '6747', '6751', '6752', '6761', '6762', '6763', '6767', '6788', '6803', '6804', '6823', '6829', '7402', '7556', '8024', '8027', '8032', '8034', '8038', '8040', '8042', '8043', '8044', '8047', '8048', '8049', '8050', '8054', '8059', '8064', '8066', '8067', '8068', '8069', '8071', '8074', '8076', '8077', '8080', '8083', '8084', '8085', '8086', '8087', '8088', '8089', '8091', '8092', '8093', '8096', '8097', '8099', '8107', '8109', '8111', '8121', '8147', '8155', '8171', '8176', '8182', '8183', '8234', '8240', '8255', '8277', '8279', '8284', '8289', '8291', '8299', '8342', '8349', '8354', '8358', '8383', '8390', '8401', '8403', '8409', '8410', '8415', '8416', '8418', '8420', '8421', '8423', '8424', '8426', '8431', '8432', '8433', '8435', '8436', '8437', '8440', '8444', '8446', '8450', '8455', '8472', '8476', '8477', '8489', '8905', '8906', '8908', '8916', '8917', '8921', '8923', '8924', '8927', '8928', '8929', '8930', '8931', '8932', '8933', '8935', '8936', '8937', '8938', '8941', '8942', '9949', '9950', '9951', '9960', '9962']
uplist = set(uplist)
def upname(data):
    if str(data) in uplist:
        data = data+'.two'
        print(data)
    else:
        data = data+'.tw'
    return data


app = Flask(__name__)
# CORS(app) # 處理跨域同源政策問題
# 首頁
@app.route('/EZ-GU',methods=['GET'])
def index():
    active = 'active'
    tiele = 'EZ-GU'
    name_ha = '2330.tw'
    return render_template('index.html', active01 = active, tiele = tiele, name_ha = name_ha)


# about
@app.route('/',methods=['GET'])
def about():
    tiele = 'BDSE25-4'
    return render_template('about.html', tiele = tiele)


# /選股
@app.route('/widget',methods=['GET','POST'])
def widget():
    active = 'active'
    tiele = '選股推薦'
    
    def plot_tw_stock_treemap(start=None, end=None, area_ind='market_value', item='return_ratio', clip=None):
  
        # 讀取存取json檔
        
        with open("./app/static/hotmap_json",'r', encoding="utf-8") as f:
            type_json =json.load(f)
            df =pd.json_normalize(type_json)

            if df is None:
                return None
            df['custom_item_label'] = round(df[item], 2).astype(str)

            if area_ind not in ["market_value", "turnover", "turnover_ratio"]:
                return None

            if item in ['return_ratio']:
                color_continuous_midpoint = 0
            else:
                color_continuous_midpoint = np.average(df[item], weights=df[area_ind])
            
            
            fig = px.treemap(df,
                            path=['country', 'market', 'category', 'stock_id_name'],

                            values=area_ind, # 占比大小由市值決定
                            color=item,  #  顏色由漲跌幅決定     

                            #  熱度圖區塊顏色設定color_continuous_scal(也可用官方搭配好顏色)
                            color_continuous_scale='armyrose',
                            # color_continuous_scale=[[0, '#ffd700'], [0.5,'white' ], [1.0, '#ff6100']],
                            
                            color_continuous_midpoint=color_continuous_midpoint,
                            custom_data=['custom_item_label', 'close', 'turnover'],
                            # width=1200,height=900
                            )

            
         
            fig.update_traces(textposition='middle center',
                            textfont_size=24,
                            
                            # 鼠標滑過顯示訊息
                            hovertemplate ="收盤價: $ %{customdata[1]:.2f}<br>漲跌幅: %{color:.2f}%"
                            )
        # 熱度圖背景色、字形顏色設定
            fig.update_layout(
                  paper_bgcolor= '#191C24',title_font_color='white',font_color='white',autosize=True
                  )
        return fig                
            
    graphJSON = json.dumps(plot_tw_stock_treemap(), cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('widget.html', active02 = active, tiele = tiele, graphJSON=graphJSON)

# /投資組合
@app.route('/form',methods=['GET','POST'])
def form():
    active = 'active'
    tiele = '投資組合評估'
    return render_template('form.html', active03 = active, tiele = tiele)

# /table
@app.route('/table',methods=['GET'])
def table():
    return render_template('table.html')

# /chart
@app.route('/chart',methods=['GET'])
def chart():
    return render_template('chart.html')

# /SP_01/to_name
@app.route('/SP_01/<name>',methods=['GET','POST'])
def to_name_01(name):
    name_org = upname(name)
    tiele = upname(name) + ' 券商買賣排行'
    return render_template('ByS_Ranking.html',name = name_org ,tiele = tiele)

# /SP_02/to_name
@app.route('/SP_02/<name>',methods=['GET','POST'])
def to_name_02(name):
    name_org = upname(name)
    tiele = upname(name) + ' 融資融券資訊'
    return render_template('Margin_Trading_and_Short_Selling.html',name = name_org ,tiele = tiele)

# /SP_03/to_name
@app.route('/SP_03/<name>',methods=['GET','POST'])
def to_name_03(name):
    name_org = upname(name)
    tiele = upname(name) + ' EPS'
    return render_template('EPS.html',name = name_org ,tiele = tiele)



# /404
@app.errorhandler(404)
def page_not_found(e):
    tiele = '404'
    return render_template('parts/404.html' ,tiele = tiele), 404

# ===================================================(以下為路由)


# /K_line路由 接收前端的ajax請求
@app.route('/K_line',methods=['GET','POST'])

def my_echart():
    # 接收前端的傳值
    q = request.values.get('q')
    url_name = request.form.get('name')

    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        q = upname(q)
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info where Symbol="' +q+ '" AND Date BETWEEN "2022-04-29" AND "2022-07-13"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()
        

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)
            

            cur.close()
    # 用在選推薦分頁
    elif url_name :
        url_name = upname(url_name)
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info where Symbol="'+url_name+'"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()
        

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)
            

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-01-05" AND "2022-07-13"' 
        cur.execute(sql)
        u = cur.fetchall()
        # print(u)

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)
            

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /MACD路由 接收前端的ajax請求
@app.route('/MACD',methods=['GET','POST'])

def my_MACD():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        q = upname(q)
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, MACD, MACDsignal, MACDhist FROM stock_info where Symbol="'+q+'" AND Date BETWEEN "2022-03-01" AND "2022-07-12"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, MACD, MACDsignal, MACDhist FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()
        # print(u)

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /Change_MK(漲跌幅)路由 接收前端的ajax請求
@app.route('/Change_MK',methods=['GET','POST'])

def my_Change_MK():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        q = upname(q)
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, Change_MK FROM stock_info where Symbol="'+q+'" AND Date BETWEEN "2020-05-13" AND "2022-07-12"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, Change_MK FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2020-05-13" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]), 2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /BBAND(布林通道)路由 接收前端的ajax請求
@app.route('/BBAND',methods=['GET','POST'])

def my_BBAND():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        q = upname(q)
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume, upper, middle, lower FROM stock_info where Symbol="'+q+'" AND Date BETWEEN "2022-01-05" AND "2022-07-13"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[7]),2))
            result.append(round((data[8]),2))
            result.append(round((data[9]),2))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume, upper, middle, lower FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-01-05" AND "2022-07-13"' 
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[7]),2))
            result.append(round((data[8]),2))
            result.append(round((data[9]),2))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[3]),2))
            result.append(round((data[2]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /KDJ路由 接收前端的ajax請求
@app.route('/KDJ',methods=['GET','POST'])

def my_KDJ():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        q = upname(q)
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, SLOWK, SLOWD, SLOWJ FROM stock_info where Symbol="'+q+'" AND Date BETWEEN "2022-03-01" AND "2022-07-12"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, SLOWK, SLOWD, SLOWJ FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()
        # print(u)

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /OBV路由 接收前端的ajax請求
@app.route('/OBV',methods=['GET','POST'])

def my_OBV():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        q = upname(q)
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, OBV FROM stock_info where Symbol="'+q+'" AND Date BETWEEN "2020-05-13" AND "2022-07-12"'
        print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, OBV FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2020-05-13" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /RSI路由 
@app.route('/RSI',methods=['GET','POST'])

def my_RSI():
    # 接收前端的傳值
    q = request.values.get('q')


    # 當有取得前端輸入值q時，用輸入值做搜尋
    if q :
        q = upname(q)
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, RSI9, RSI14, RSI25 FROM stock_info where Symbol="'+q+'" AND Date BETWEEN "2022-03-01" AND "2022-07-12"'
        # print(sql)
        cur.execute(sql)
        u = cur.fetchall()

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
            # print(jsonData)
            j = json.dumps(jsonData)

            cur.close()
            # conn.close()

    # 若沒有則帶入預設
    else:
        conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
        cur = conn.cursor()
        sql = 'SELECT Symbol, Date, RSI9, RSI14, RSI25 FROM stock_info where Symbol="2330.tw" AND Date BETWEEN "2022-03-01" AND "2022-07-12"' 
        cur.execute(sql)
        u = cur.fetchall()
        # print(u)

        # 轉換成JSON數據格式
        jsonData = []

        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)

            cur.close()
            # conn.close()
    # print(j)
    return(j) 

# /from_in路由
# /投資組合(.two修改未完成)
@app.route('/form_in',methods=['GET','POST'])
def form_in():
    start_yt = '2002/01/01'
    end_yt = '2021/12/31'

    #接收輸入值
    name_st = request.values.get('name_st')
    input_Date = request.values.get('input_Date')
    input_Cost = request.values.get('input_Cost')
    input_Share = request.values.get('input_Share')
    SL_buy = []
    SD_buy = []
    SC_buy = []
    SS_buy = []
    standard_deviation_list = []
    IRR_list = []
    sharpe_list = []
    Beta_list = []

    if name_st:
        #2021年美國聯邦銀行利率
        url = "https://api.finmindtrade.com/api/v4/data"
        parameter = {
        "dataset": "InterestRate",
        "data_id": "FED",
        "start_date": "2021-03-17",
        }
        Interest_rate_data = requests.get(url, params=parameter)
        Interest_rate_data = Interest_rate_data.json()
        Interest_rate_data = pd.DataFrame(Interest_rate_data['data'])

        # 新增空DataFrame
        stock_NB_buy = pd.DataFrame()
        stock_YAHOO_ORDER_buy = pd.DataFrame()
        stock_ALL_INFO_buy = pd.DataFrame()
        IP_buy = pd.DataFrame()

        # 18-21年台灣加權指數平均報酬率
        name_mk = '^twii'
        df_mk = data.DataReader(name_mk,'yahoo', start_yt, end_yt)
        df_mk['Change%MK'] = (df_mk['Close']/df_mk['Close'].shift(1)-1)*100
        change_mk_avg = df_mk['Change%MK'].mean() * 100

        # 18-21年美國10年國債平均利率
        name_usyt = '^TNX'
        df_us10yt = data.DataReader(name_usyt,'yahoo', start_yt, end_yt)
        df_us10yt['Change%USYT'] = (df_us10yt['Close'] / df_us10yt['Close'].shift(1)-1)*100
        us10yt_avg = df_us10yt['Change%USYT'].mean() * 100

        print('18-21年美國10年國債平均利率=',us10yt_avg)
        print('18-21年{}平均報酬率='.format(name_mk),change_mk_avg)

        if name_st:
            SL_buy.append(name_st)

        if input_Date:
            SD_buy.append(input_Date)

        if input_Cost:
            SC_buy.append(input_Cost)

        if input_Share:
            SS_buy.append(input_Share)

            
        # 確認當前日期是否為週末
        # 確認當前時間是否早於09:30(若早於上午0930，則自動抓取前一天之資訊) 
        # today = dt.date.today()
        # yahoo_limit_time = dt.time(9, 30)
        # localtime = dt.datetime.now().time()
        # def check_weekend(today):
        #     if today.weekday() == 5:
        #         return str(today + dt.timedelta(days=-1))
        #     if today.weekday() == 6:
        #         return str(today + dt.timedelta(days=-2))
        #     if localtime < yahoo_limit_time:
        #         return str(today + dt.timedelta(days=-1))
        #     if localtime > yahoo_limit_time:
        #         return datetime.strftime(today, "%Y-%m-%d")
        #     else:
        #         return datetime.strftime(today, "%Y-%m-%d")
        
        day_y = dt.datetime.today()
        yahoo_limit_time = dt.time(9, 30)
        localtime = dt.datetime.now().time()
        def check_weekend(day_y):
            if day_y == day_y:
                if day_y.weekday() == 0:
                    if localtime < yahoo_limit_time:
                        return str(day_y + dt.timedelta(days=-3))
                    if localtime > yahoo_limit_time:
                        return datetime.strftime(day_y, "%Y-%m-%d")
            if today.weekday() == 5:
                return str(day_y + dt.timedelta(days=-1))
            if today.weekday() == 6:
                return str(day_y + dt.timedelta(days=-2))
            if day_y == day_y:
                if localtime < yahoo_limit_time:
                    return str(day_y + dt.timedelta(days=-1))
                if localtime > yahoo_limit_time:
                    return datetime.strftime(day_y, "%Y/%m/%d")
            else:
                return datetime.strftime(day_y, "%Y/%m/%d")
        # 調整輸入日期，輸入予證交所爬取資料
        # 市場未結束時(09:00 - 13:30)，證交所資料尚未統整，故抓取前一天資料
        input_Date = datetime.strptime(input_Date, "%Y-%m-%d").date()
        today = dt.date.today()
        time = dt.time(14, 40) # 設定1430等待證交所完整資料上傳
        localtime = dt.datetime.now().time()
        def check_datetime(input_Date):
            if input_Date == today:
                if input_Date.weekday() == 0:
                    if localtime < time:
                        return str(input_Date + dt.timedelta(days=-3))
                    if localtime > time:
                        return datetime.strftime(input_Date, "%Y-%m-%d")
            if input_Date.weekday() == 5:
                return str(input_Date + dt.timedelta(days=-1))
            if input_Date.weekday() == 6:
                return str(input_Date + dt.timedelta(days=-2))
            if input_Date == today:
                if localtime < time:
                    return str(input_Date + dt.timedelta(days=-1))
                if localtime > time:
                    return datetime.strftime(input_Date, "%Y-%m-%d")
            else:
                return datetime.strftime(input_Date, "%Y-%m-%d")
        
        date_range = [i.strftime("%Y%m%d") for i in pd.date_range(
            check_datetime(input_Date),
            check_datetime(input_Date)
        )]

        for d in date_range:
            url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX'
            # url_up = 'https://www.twse.com.tw/exchangeReport/MI_INDEX'
            formdata = {
                'response': 'csv',
                'date': d, 
                'type': 'ALLBUT0999',
            }
            # 取得資料並且解析(判斷是上櫃還是上市)
            # if str(name_st) in uplist:
            #     r = requests.get(url_up, params=formdata)
            # else:

            r = requests.get(url, params=formdata)
            r.text.encode('utf8')
            cr = csv.reader(r.text.splitlines(), delimiter=',')
            my_list = list(cr)
            # print(my_list)

            # 資料整理
            if len(my_list) > 0:
                for i in range(len(my_list)):
                    if len(my_list[i]) > 0:
                        if my_list[i][0] == '證券代號':
                            new_list = my_list[i:]
                            break
                # print(new_list)
                for j in range(len(new_list)):
                    if j != 0:
                        try:
                            new_list[j][0] = new_list[j][0].split('"')[1]
                        except:
                            break
                # print(new_list)
                df = pd.DataFrame(new_list[1:], columns=new_list[0])

                print('已篩選出 {} 全上市股票行情資料'.format(date_range))
                ti.sleep(1)
            else:
                print('No Data')
                No_Data = pd.DataFrame({
                'Date' : SD_buy[0]+" 當日無開盤",
                'id' : SL_buy
                },index = range(len(SL_buy)))
                data_in = No_Data.to_json(orient = 'records',force_ascii=False)
                
                return(data_in)
            

        # 18-21年指定個股平均報酬率
        name_rr = str('{}.tw'.format(name_st))
        df_rr = data.DataReader(name_rr, 'yahoo', start_yt, end_yt)
        df_rr['Change%RR'] = (df_rr['Close'] / df_rr['Close'].shift(1)-1)*100
        change_rr_avg = df_rr['Change%RR'].mean() * 100

        # 篩選資料並加入新DataFrame
        # print(df['證券代號'])
        stock_NB_buy = pd.concat([stock_NB_buy, df.loc[df['證券代號'] == name_st]], axis = 0)
        # print(stock_NB_buy)

        # 篩出指定欄位
        stock_LS_buy = stock_NB_buy[['證券代號','證券名稱','開盤價','最高價','最低價','收盤價','漲跌(+/-)','漲跌價差','本益比']]
        # 增加欄位至指定位置
        stock_LS_buy.insert(0,'交易日期',SD_buy)
        stock_LS_buy = stock_LS_buy.reset_index()

        # yahoo DataReader:當下股票資訊
        start = check_weekend(today)
        end = check_weekend(today)
        # start = "2022-07-24"
        # end = "2022-07-24"
        name = str('{}.tw'.format(name_st))
        df_st_buy = data.DataReader(name, 'yahoo', start, end)
        # print(df_st_buy)
        
        # 將證交所、Yahoo Finance資料合併
        stock_YAHOO_ORDER_buy = pd.concat([stock_YAHOO_ORDER_buy, df_st_buy],axis = 0,ignore_index = True)
        
        # 彙整所有DataFrame
        stock_ALL_INFO_buy = pd.concat([stock_LS_buy, stock_YAHOO_ORDER_buy], axis = 1)
        stock_ALL_INFO_buy['收盤價'] = stock_ALL_INFO_buy['收盤價'].astype(float, errors = 'raise')
        # print(stock_ALL_INFO_buy)

        # 18-21年個股曝險程度及報酬率
        name = str('{}.tw'.format(name_st))
        df_days_st = data.DataReader(name, 'yahoo', start_yt, end_yt)

        # 個股標準差(standard_deviation)
        standard_deviation = df_days_st['Close'].std()
        if standard_deviation != 0:
            standard_deviation_list.append(standard_deviation)

        # 年化報酬率(IRR)
        TR = df_days_st['Close'].iloc[-1] / df_days_st['Close'].iloc[0] - 1
        days = len(df_days_st)
        IRR = ((1+TR)**(270/days)-1)*100
        if IRR != 0:
            IRR_list.append(IRR)

        # 個股夏普值
        sharpe = (IRR - us10yt_avg) / standard_deviation
        if sharpe != 0:
            sharpe_list.append(sharpe)
            
        # 貝他值 Beta
        # 股票收益率 減去 無風險利率
        SV = change_rr_avg - us10yt_avg
        # 加權指數收益率 減去 無風險利率
        MV = change_mk_avg - us10yt_avg
        # 貝他值 = (股票收益率 減去 無風險利率之差) / (加權指數收益率 減去 無風險利率之差)
        beta = SV / MV
        if beta != 0:
            Beta_list.append(beta)
        
        risk = pd.DataFrame({
            'ID' : SL_buy,
            'SD' : standard_deviation_list,
            'IRR' : IRR_list,
            'Sharpe' : sharpe_list,
            'Beta' : Beta_list
        },index = SL_buy)
        risk.insert(5, 'RR', 0)
        risk.insert(6, 'MR', 0)
        risk.insert(7, 'Rate', 0)
        
        # 蒐集input元素並製成DataFrame
        all_INPUT_buy = pd.DataFrame({
            'Number' : SL_buy,
            'Date' : SD_buy,
            'Cost' : SC_buy,
            'Share' : SS_buy
        },index = range(len(SL_buy)))
        all_INPUT_buy['Number'] = all_INPUT_buy['Number'].astype(float, errors = 'raise')
        all_INPUT_buy['Cost'] = all_INPUT_buy['Cost'].astype(float, errors = 'raise')
        all_INPUT_buy['Share'] = all_INPUT_buy['Share'].astype(float, errors = 'raise')

        print(stock_ALL_INFO_buy)
        print("=======================================")
        print(risk)
        print("=======================================")
        if stock_ALL_INFO_buy.isnull().values.any():
            stock_ALL_INFO_buy = stock_ALL_INFO_buy.drop(stock_ALL_INFO_buy.index[[1]])
            stock_YAHOO_ORDER_buy = stock_YAHOO_ORDER_buy.drop(stock_YAHOO_ORDER_buy.index[[1]])

        print(stock_YAHOO_ORDER_buy)
        print("=======================================")
        print(all_INPUT_buy)
        # 建立投資組合表格
        IP_buy = pd.DataFrame(columns=['id','id_name','YEAR','SP','BT','現價','成本基準','買入股數','買進手續費','買價','現值','持股漲跌幅'],index = SD_buy)
        if len(stock_ALL_INFO_buy) > 0:
            # print(stock_ALL_INFO_buy)
            for NM in range(len(stock_ALL_INFO_buy)):
                IP_buy.at[IP_buy.index[NM], 'id'] = stock_ALL_INFO_buy.at[stock_ALL_INFO_buy.index[NM], '證券代號']
                IP_buy.at[IP_buy.index[NM], 'id_name'] = stock_ALL_INFO_buy.at[stock_ALL_INFO_buy.index[NM], '證券名稱']
        if len(risk) > 0:
            for NR in range(len(risk)):
                IP_buy.at[IP_buy.index[NR], 'YEAR'] = risk.at[risk.index[NR], 'IRR']
                IP_buy.at[IP_buy.index[NR], 'SP'] = risk.at[risk.index[NR], 'Sharpe']
                IP_buy.at[IP_buy.index[NR], 'BT'] = risk.at[risk.index[NR], 'Beta']
        if len(stock_YAHOO_ORDER_buy) > 0:
            for NY in range(len(stock_YAHOO_ORDER_buy)):
                IP_buy.at[IP_buy.index[NY], '現價'] = stock_YAHOO_ORDER_buy.at[stock_YAHOO_ORDER_buy.index[NY], 'Close']
        if len(all_INPUT_buy) > 0:
            for NB in range(len(all_INPUT_buy)):
                IP_buy.at[IP_buy.index[NB], '成本基準'] = all_INPUT_buy.at[all_INPUT_buy.index[NB], 'Cost']
                IP_buy.at[IP_buy.index[NB], '買入股數'] = all_INPUT_buy.at[all_INPUT_buy.index[NB], 'Share']
                IP_buy.at[IP_buy.index[NB], '買進手續費'] = float(IP_buy.at[IP_buy.index[NB], '成本基準']) * float(IP_buy.at[IP_buy.index[NB], '買入股數']) * 0.001425
                IP_buy.at[IP_buy.index[NB], '買價'] = float(IP_buy.at[IP_buy.index[NB], '成本基準']) * float(IP_buy.at[IP_buy.index[NB], '買入股數']) + float(IP_buy.at[IP_buy.index[NB], '買進手續費'])
                IP_buy.at[IP_buy.index[NB], '現值'] = float(stock_ALL_INFO_buy.at[stock_ALL_INFO_buy.index[NB], '收盤價']) * float(IP_buy.at[IP_buy.index[NB], '買入股數'])
                IP_buy.at[IP_buy.index[NB], '持股漲跌幅'] = (IP_buy.at[IP_buy.index[NB], '現值']-IP_buy.at[IP_buy.index[NB], '買價'])/IP_buy.at[IP_buy.index[NB], '買價'] * 100
                
                # 將指定欄位整行轉型
                IP_buy['買價'] = IP_buy['買價'].astype(float, errors = 'raise')

        
    # IP_buy.insert(12, 'MV', change_mk_avg-us10yt_avg)
    IP_buy.insert(12, 'change_mk_avg', change_mk_avg)
    IP_buy.insert(13, 'us10yt_avg', us10yt_avg)
    IP_buy.insert(0,'Date',SD_buy)
    # MV加權指數收益率 減去 無風險利率
    IP_buy['MV'] = IP_buy['change_mk_avg'] - IP_buy['us10yt_avg']
    # IP_buy = stock_LS_buy.reset_index()
    # IP_buy = IP_buy.reset_index(inplace=True)

    data_in = IP_buy.to_json(orient = 'records',force_ascii=False)
    # print(data_in)

    return(data_in)

# /SPK_1路由
# /選股-投信
@app.route('/SPK_1',methods=['GET','POST'])
def SPK_1():

    #使用requests
    url = "https://goodinfo.tw/tw/StockList.asp?RPT_TIME=&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E6%8A%95%E4%BF%A1%E7%B4%AF%E8%A8%88%E8%B2%B7%E8%B6%85%E5%BC%B5%E6%95%B8+%E2%80%93+%E7%95%B6%E6%97%A5%40%40%E6%8A%95%E4%BF%A1%E7%B4%AF%E8%A8%88%E8%B2%B7%E8%B6%85%40%40%E6%8A%95%E4%BF%A1%E8%B2%B7%E8%B6%85%E5%BC%B5%E6%95%B8+%E2%80%93+%E7%95%B6%E6%97%A5"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    res = requests.get(url,headers=headers)
    res.encoding = "utf-8"
    ti.sleep(2)

    #使用bs4的BeautifulSoup
    soup = bs4.BeautifulSoup(res.text,"lxml")
    data = soup.select_one("#txtStockListData")

    #使用pandas
    df = pd.read_html(data.prettify())
    dfs = df[1]
    dfs.drop(['外資  買進  張數','外資  賣出  張數','外資  買賣超  張數','自營  買進  張數','自營  賣出  張數','自營  買賣超  張數','合計  買進  張數','合計  賣出  張數','合計  買賣超  張數'], axis=1 ,inplace = True)
    dfs.drop([18],axis=0,inplace=True)

    stock20 = dfs.head(20)

    # ascii：預設值True，如果資料中含有非ASCII的字元，則會類似\uXXXX的顯示資料，設定成False後，就能正常顯示
    # records為切割DataFrame資料方法之一(allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.)。
    stock20_in = stock20.to_json(orient = 'records',force_ascii=False)
    # print(stock20_in)

    return(stock20_in)

# /選股-投信-券商買賣排行
@app.route('/ByS_Ranking',methods=['GET','POST'])
def ByS_Ranking():

    url_name = request.form.get('name')
    print(url_name)

    lst = {url_name}
    url_test = 'https://histock.tw/stock/branch.aspx?no=%s'
    for i in lst:
        url = url_test %i
            
    tables = pd.read_html(url)

    df1 = tables[0]
    # df1.rename(columns ={'券商名稱.1': '券商名稱', '買張.1': '買張', '賣張.1': '賣張', '均價.1': '均價'},inplace = True)
    df1.fillna({'買張':0,'買張.1':0,'賣張':0,'賣張.1':0}, inplace=True )
    df1 = df1.astype({"買張":"int","賣張":"int",'買張.1':"int","賣張.1":"int"})
    blankIndex=[''] * len(df1)
    df1.index=blankIndex

    # stock20 = dfs.head(20)

    # ascii：預設值True，如果資料中含有非ASCII的字元，則會類似\uXXXX的顯示資料，設定成False後，就能正常顯示
    # records為切割DataFrame資料方法之一(allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.)。
    ByS_Ranking = df1.to_json(orient = 'records',force_ascii=False)
    # print(ByS_Ranking)

    return(ByS_Ranking)

# /SPK_2路由
# /選股-週轉率Turnover
@app.route('/SPK_2',methods=['GET','POST'])
def SPK_2():

    #使用requests
    url = 'https://goodinfo.tw/tw/StockList.asp?RPT_TIME=&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E7%B4%AF%E8%A8%88%E6%88%90%E4%BA%A4%E9%87%8F%E9%80%B1%E8%BD%89%E7%8E%87%28%E7%95%B6%E6%97%A5%29%40%40%E7%B4%AF%E8%A8%88%E6%88%90%E4%BA%A4%E9%87%8F%E9%80%B1%E8%BD%89%E7%8E%87%40%40%E7%95%B6%E6%97%A5'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
    res = requests.get(url,headers=headers)
    res.encoding = "utf-8"

    #使用bs4的BeautifulSoup
    soup = bs4.BeautifulSoup(res.text,"lxml")
    data = soup.select_one("#txtStockListData")

    #使用pandas
    df = pd.read_html(data.prettify())
    dfs = df[1]
    dfs.drop(['10日  累計  成交量  週轉率','一個月  累計  成交量  週轉率','三個月  累計  成交量  週轉率','半年  累計  成交量  週轉率','今年  累計  成交量  週轉率','一年  累計  成交量  週轉率', '二年  累計  成交量  週轉率', '三年  累計  成交量  週轉率'],axis=1,inplace=True)
    dfs.drop([18],axis=0,inplace=True)

    Turnover20 = dfs.head(20)

    # ascii：預設值True，如果資料中含有非ASCII的字元，則會類似\uXXXX的顯示資料，設定成False後，就能正常顯示
    # records為切割DataFrame資料方法之一(allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.)。
    Turnover20_in = Turnover20.to_json(orient = 'records',force_ascii=False)
    # print(Turnover20_in)

    return(Turnover20_in)

# /選股-投信-融資融券Margin_Trading_and_Short_Selling
@app.route('/MTaSS',methods=['GET','POST'])
def MTaSS():

    url_name = request.form.get('name')
    # print(url_name)

    lst = {url_name}
    url_test = 'https://histock.tw/stock/chips.aspx?no=%s&m=mg'
    for i in lst:
        url = url_test %i
    tables = pd.read_html(url)    

    df1 = tables[0]
    df1.columns = df1.columns.to_flat_index()
    df1 = df1.rename(columns={(     '日期',     '日期'):     '日期',('資券互抵(張)','資券互抵(張)'):'資券互抵(張)',('資券當沖(%)','資券當沖(%)'):'資券當沖(%)',('券資比(%)','券資比(%)'):'券資比(%)'\
                            ,(     '價格',     '價格'):     '價格',(     '比例',     '比例'):     '比例',(    '成交量',    '成交量'):    '成交量'},errors='raise')
    df1.rename(columns ={   ('融資', '增加'): '融資增加',   ('融資', '餘額'):'融資餘額', ('融資', '使用率％'):'融資使用率%',('融券', '增加'):'融券增加',   ('融券', '餘額'): '融券餘額',(     '融券',    '使用率％'): '融券使用率%'},inplace = True)
    blankIndex=[''] * len(df1)
    df1.index=blankIndex

    # ascii：預設值True，如果資料中含有非ASCII的字元，則會類似\uXXXX的顯示資料，設定成False後，就能正常顯示
    # records為切割DataFrame資料方法之一(allowed values are: {‘split’, ‘records’, ‘index’, ‘columns’, ‘values’, ‘table’}.)。
    MTaSS = df1.to_json(orient = 'records',force_ascii=False)
    # print(MTaSS)
    return(MTaSS)



# /SPK_3路由
# /選股-波動收縮規律close > upper(強力買入)
@app.route('/SPK_3',methods=['GET','POST'])
def SPK_3():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Date = (SELECT MAX(Date) FROM stock_info) AND Volume BETWEEN 50000 AND 5000000 AND Volume10 BETWEEN 50000 AND 5000000 AND Volume30 BETWEEN 50000 AND 5000000 AND Volume60 BETWEEN 50000 AND 5000000 AND Volume90 BETWEEN 50000 AND 5000000 AND SAM50 > SAM100 AND SAM100 > SAM200 AND Close > upper'
    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    # 轉換成JSON數據格式
    jsonData = []

    for data in u:
        result = []
        result.append(str(data[0]))
        result.append(str(data[1]))
        result.append(round((data[2]),2))
        result.append(round((data[3]),2))
        result.append(round((data[4]),2))
        result.append(round((data[5]),2))
        result.append(round((data[6]),2))

        jsonData.append(result)

        # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
        # print(jsonData)
        j = json.dumps(jsonData)
        print(j)

    return(j)

# /SPK_4路由
# /選股-波動收縮規律close > upper(買入)
@app.route('/SPK_4',methods=['GET','POST'])
def SPK_4():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Date = (SELECT MAX(Date) FROM stock_info) AND Volume BETWEEN 50000 AND 5000000 AND Volume10 BETWEEN 50000 AND 5000000 AND Volume30 BETWEEN 50000 AND 5000000 AND Volume60 BETWEEN 50000 AND 5000000 AND Volume90 BETWEEN 50000 AND 5000000 AND SAM50 > SAM100 AND SAM100 > SAM200 AND Close > middle AND Close < upper'
    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    # 轉換成JSON數據格式
    jsonData = []

    for data in u:
        result = []
        result.append(str(data[0]))
        result.append(str(data[1]))
        result.append(round((data[2]),2))
        result.append(round((data[3]),2))
        result.append(round((data[4]),2))
        result.append(round((data[5]),2))
        result.append(round((data[6]),2))

        jsonData.append(result)

        # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
        # print(jsonData)
        j = json.dumps(jsonData)
        print(j)

    return(j)

# /SPK_5路由
# /選股-波動收縮規律close > upper(中立&賣出)
@app.route('/SPK_5',methods=['GET','POST'])
def SPK_5():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Date = (SELECT MAX(Date) FROM stock_info) AND Volume BETWEEN 50000 AND 5000000 AND Volume10 BETWEEN 50000 AND 5000000 AND Volume30 BETWEEN 50000 AND 5000000 AND Volume60 BETWEEN 50000 AND 5000000 AND Volume90 BETWEEN 50000 AND 5000000 AND SAM50 > SAM100 AND SAM100 > SAM200 AND Close >= lower AND Close < middle'
    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    # 轉換成JSON數據格式
    jsonData = []

    for data in u:
        result = []
        result.append(str(data[0]))
        result.append(str(data[1]))
        result.append(round((data[2]),2))
        result.append(round((data[3]),2))
        result.append(round((data[4]),2))
        result.append(round((data[5]),2))
        result.append(round((data[6]),2))

        jsonData.append(result)

        # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
        # print(jsonData)
        j = json.dumps(jsonData)
        print(j)

    return(j)

# /SPK_6路由
# /選股-波動收縮規律close > upper(強力賣出)
@app.route('/SPK_6',methods=['GET','POST'])
def SPK_6():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Date = (SELECT MAX(Date) FROM stock_info) AND Volume BETWEEN 50000 AND 5000000 AND Volume10 BETWEEN 50000 AND 5000000 AND Volume30 BETWEEN 50000 AND 5000000 AND Volume60 BETWEEN 50000 AND 5000000 AND Volume90 BETWEEN 50000 AND 5000000 AND SAM50 > SAM100 AND SAM100 > SAM200 AND Close <= lower'
    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    # 轉換成JSON數據格式
    jsonData = []

    for data in u:
        result = []
        result.append(str(data[0]))
        result.append(str(data[1]))
        result.append(round((data[2]),2))
        result.append(round((data[3]),2))
        result.append(round((data[4]),2))
        result.append(round((data[5]),2))
        result.append(round((data[6]),2))

        jsonData.append(result)

        # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
        # print(jsonData)
        j = json.dumps(jsonData)
        print(j)

    return(j)

# /RSI_1路由
# /選股-技術指標RSI條件(超買)
@app.route('/RSI_1',methods=['GET','POST'])
def RSI_1():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Date = (SELECT MAX(Date) FROM stock_info) AND RSI9>80'
    print(sql)
    cur.execute(sql)
    u = cur.fetchall()
    print(u)

    jsonData = []

    if u == ():
        u = ((("無符合條件股票","請改用其他條件")))
        for data in u:
            result = []
            result.append(data)


            jsonData.append(result)

            j = json.dumps(jsonData, ensure_ascii=False)
    else:
        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)
    
    print(j)
    return(j)

# /RSI_1路由
# /選股-技術指標RSI條件(超賣)
@app.route('/RSI_1_2',methods=['GET','POST'])
def RSI_1_2():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Date = (SELECT MAX(Date) FROM stock_info) AND RSI9<20'
    print(sql)
    cur.execute(sql)
    u = cur.fetchall()
    print(u)

    jsonData = []

    if u == ():
        u = ((("無符合條件股票","請改用其他條件")))
        for data in u:
            result = []
            result.append(data)


            jsonData.append(result)

            j = json.dumps(jsonData, ensure_ascii=False)
    else:
        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)
    
    print(j)
    return(j)


# /RSI_2路由
# /選股-技術指標RSI條件( (-2) RSI(9)<RSI(14) (-1)天 RSI(9)>RSI(14))
@app.route('/RSI_2',methods=['GET','POST'])
def RSI_2():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Symbol = any(SELECT Symbol FROM stock_info WHERE Date = (SELECT date_sub(max(Date),interval 1 DAY) FROM stock_info) AND RSI9 < RSI14) AND Date = (SELECT MAX(Date) FROM stock_info) AND RSI9 > RSI14'

    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    # 轉換成JSON數據格式
    jsonData = []

    for data in u:
        result = []
        result.append(str(data[0]))
        result.append(str(data[1]))
        result.append(round((data[2]),2))
        result.append(round((data[3]),2))
        result.append(round((data[4]),2))
        result.append(round((data[5]),2))
        result.append(round((data[6]),2))

        jsonData.append(result)

        # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
        # print(jsonData)
        j = json.dumps(jsonData)
        print(j)

    return(j)


# /JDK_1路由
# /選股-技術指標JDK條件(超買)
@app.route('/JDK_1',methods=['GET','POST'])
def JDK_1():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Date = (SELECT MAX(Date) FROM stock_info) AND SLOWK > 80 '

    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    jsonData = []

    if u == ():
        u = ((("無符合條件股票","請改用其他條件")))
        for data in u:
            result = []
            result.append(data)


            jsonData.append(result)

            j = json.dumps(jsonData, ensure_ascii=False)
    else:
        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)
   
    return(j)

# /JDK_1_2路由
# /選股-技術指標JDK條件(超賣)
@app.route('/JDK_1_2',methods=['GET','POST'])
def JDK_1_2():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Date = (SELECT MAX(Date) FROM stock_info) AND SLOWK < 20'

    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    jsonData = []

    if u == ():
        u = ((("無符合條件股票","請改用其他條件")))
        for data in u:
            result = []
            result.append(data)


            jsonData.append(result)

            j = json.dumps(jsonData, ensure_ascii=False)
    else:
        for data in u:
            result = []
            result.append(str(data[0]))
            result.append(str(data[1]))
            result.append(round((data[2]),2))
            result.append(round((data[3]),2))
            result.append(round((data[4]),2))
            result.append(round((data[5]),2))
            result.append(round((data[6]),2))

            jsonData.append(result)

            j = json.dumps(jsonData)
   
    return(j)


# /JDK_2路由
# /選股-技術指標JDK條件((-2天) K < D (-1天) K > D)
@app.route('/JDK_2',methods=['GET','POST'])
def JDK_2():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Symbol = any(SELECT Symbol FROM stock_info WHERE Date = (SELECT date_sub(max(Date),interval 1 DAY) FROM stock_info) AND SLOWK < SLOWD) AND Date = (SELECT MAX(Date) FROM stock_info) AND SLOWK > SLOWD'

    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    # 轉換成JSON數據格式
    jsonData = []

    for data in u:
        result = []
        result.append(str(data[0]))
        result.append(str(data[1]))
        result.append(round((data[2]),2))
        result.append(round((data[3]),2))
        result.append(round((data[4]),2))
        result.append(round((data[5]),2))
        result.append(round((data[6]),2))

        jsonData.append(result)

        # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
        # print(jsonData)
        j = json.dumps(jsonData)
        print(j)

    return(j)


# /MACD_1路由
# /選股-技術指標MACD多方((-2天) MACD<MACD Signal &(-1天) MACD>MACD Signal)
@app.route('/MACD_1',methods=['GET','POST'])
def MACD_1():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Symbol = any(SELECT Symbol FROM stock_info WHERE Date = (SELECT date_sub(max(Date),interval 1 DAY) FROM stock_info) AND MACD < MACDsignal) AND Date = (SELECT MAX(Date) FROM stock_info) AND MACD > MACDsignal;'

    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    # 轉換成JSON數據格式
    jsonData = []

    for data in u:
        result = []
        result.append(str(data[0]))
        result.append(str(data[1]))
        result.append(round((data[2]),2))
        result.append(round((data[3]),2))
        result.append(round((data[4]),2))
        result.append(round((data[5]),2))
        result.append(round((data[6]),2))

        jsonData.append(result)

        # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
        # print(jsonData)
        j = json.dumps(jsonData)
        print(j)

    return(j)

# /MACD_2路由
# /選股-技術指標MACD多方((-2天) MACD<MACD Signal &(-1天) MACD>MACD Signal)
@app.route('/MACD_2',methods=['GET','POST'])
def MACD_2():

    conn = pymysql.connect(host='35.221.190.227',user='root',password='a000000',db='stock_analysis')
    cur = conn.cursor()
    sql = 'SELECT Symbol, Date, High, Low, Open, Close, Volume FROM stock_info WHERE Symbol = any(SELECT Symbol FROM stock_info WHERE Date = (SELECT date_sub(max(Date),interval 1 DAY) FROM stock_info) AND MACD > MACDsignal) AND Date = (SELECT MAX(Date) FROM stock_info) AND MACD < MACDsignal;'

    print(sql)
    cur.execute(sql)
    u = cur.fetchall()

    # 轉換成JSON數據格式
    jsonData = []

    for data in u:
        result = []
        result.append(str(data[0]))
        result.append(str(data[1]))
        result.append(round((data[2]),2))
        result.append(round((data[3]),2))
        result.append(round((data[4]),2))
        result.append(round((data[5]),2))
        result.append(round((data[6]),2))

        jsonData.append(result)

        # json.dumps()用於將dict類型的數據轉成str，因為如果直接將dict類型的數據寫入json會發生報錯，因此將數據寫入時需要用到該函數。
        # print(jsonData)
        j = json.dumps(jsonData)
        print(j)

    return(j)





# /選股-波動收縮規律&技術指標-子頁EPS
@app.route('/EPS',methods=['GET','POST'])
def EPS():

    url_name = request.form.get('name')

    id =url_name
    url = "https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=" + id +"&amp;YEAR_PERIOD=9999&amp;RPT_CAT=M_YEAR"
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"lxml")
    data = soup.select_one("#txtFinDetailData")
    dfs = pd.read_html(data.prettify())
    df = dfs[0]
    df.columns = df.columns.get_level_values(1)
    df.columns = ["年度","股本(億)","財報評分","收盤價","平均價","漲跌(元)","漲跌(%)","營業收入(億)","營業毛利(億)","營業利益(億)","業外損益(億)",
                "稅後淨利(億)","營業毛利(%)","營業利益(%)","業外損益(%)","稅後淨利(%)","ROE(%)","ROA(%)","稅後EPS","年增(元)",
                "EPS(元)"]
    for i in range(len(df)):
        if df["年度"].iloc[i].isdigit() == False:
            x = dt.datetime.now()
            year = x.year
            df.loc[0,"年度"] = year
    df.index = df["年度"]
    # df = df.drop(["年度"],axis = 1)

    if len(df)>19:
        df = df.drop(["年度"],axis = 0)
        df = df.replace("-","0")
    else:
        df = df.replace("-","0")

    # print(df)
    EPS = df.to_json(orient = 'records',force_ascii=False)
    # print(EPS)
    return(EPS)





