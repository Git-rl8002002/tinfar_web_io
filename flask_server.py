#!/usr/bin/python3
# -*- coding: UTF-8 -*-

#Author   : JasonHung
#Date     : 20221102
#Update   : 20230509
#Function : web io cloud platform

from argparse import Namespace
from dataclasses import dataclass
from email import charset
from hashlib import md5
import hashlib , time , logging , random
from tabnanny import check
from flask import Flask,render_template,request,session,url_for,redirect,escape,abort,jsonify
from flask_socketio import SocketIO , emit 
from control.web_cloud_dao import web_cloud_dao 

db = web_cloud_dao()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret' 
socketio = SocketIO(app , async_mode='threading' , transports=['websocket'])  

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

##############
# variables
##############
ver     = web_cloud_dao.param['ver']
title   = web_cloud_dao.param['title']
content = web_cloud_dao.param['content']


##########
# /test
##########
@app.route("/test")
def test():
    try:
        return render_template('test.html')
    except Exception as e:
        logging.info("<< Error >> test : " + str(e))
    finally:
        pass

###############################
# /submit_check_account_user
###############################
@app.route("/submit_check_account_user" , methods=['POST','GET'])
def submit_check_account_user():
    if 'user' in session:
        # operation record title
        operation_record_title = '權限管理 - 送出檢查帳號'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                a_user = request.form['a_user']
                
                res = db.submit_check_account(a_user)

                a_list = db.account_list()
                a_record = db.account_usage_record(user)
                
                return render_template('ajax/load_check_account_user.html' , user=user , lv=lv , title=title , a_list=a_list , res=res , a_record=a_record)
                
        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#############################
# /submit_del_account_form
#############################
@app.route("/submit_del_account_form" , methods=['POST','GET'])
def submit_del_account_form():
    if 'user' in session:
        # operation record title
        operation_record_title = '權限管理 - 送出刪除帳號'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                a_user = request.form['a_user']
                a_pwd = request.form['a_pwd']
                a_lv = request.form['a_lv']
                a_status = request.form['a_status']
                
                res = db.submit_del_account(a_user,a_pwd,a_lv,a_status)

                a_list = db.account_list()
                a_record = db.account_usage_record(user)
                
                if res == 'ok':
                    return render_template('ajax/load_account_list.html' , user=user , lv=lv , title=title , a_list=a_list , a_record=a_record)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###############################
# /submit_alter_account_form
###############################
@app.route("/submit_alter_account_form" , methods=['POST','GET'])
def submit_alter_account_form():
    if 'user' in session:
        # operation record title
        operation_record_title = '權限管理 - 送出修改帳號'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                a_user = request.form['a_user']
                a_pwd = request.form['a_pwd']
                a_lv = request.form['a_lv']
                a_status = request.form['a_status']
                
                res = db.submit_alter_account(a_user,a_pwd,a_lv,a_status)

                a_list = db.account_list()
                a_record = db.account_usage_record(user)
                
                if res == 'ok':
                    return render_template('ajax/load_account_list.html' , user=user , lv=lv , title=title , a_list=a_list , a_record=a_record)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

#############################
# /submit_add_account_form
#############################
@app.route("/submit_add_account_form" , methods=['POST','GET'])
def submit_add_account_form():
    if 'user' in session:
        # operation record title
        operation_record_title = '權限管理 - 送出新增帳號'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                a_user = request.form['a_user']
                a_pwd = request.form['a_pwd']
                a_lv = request.form['a_lv']
                
                res = db.submit_add_account(a_user,a_pwd,a_lv)

                a_list = db.account_list()
                a_record = db.account_usage_record(user)
                
                if res == 'ok':
                    return render_template('ajax/load_account_list.html' , user=user , lv=lv , title=title , a_list=a_list , a_record=a_record)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################
# /load_alter_account_form
###########################
@app.route("/load_alter_account_form" , methods=['POST','GET'])
def load_alter_account_form():
    if 'user' in session:
        # operation record title
        operation_record_title = '權限管理 - 修改帳號表格'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            if request.method == 'POST':

                a_user = request.form['a_user']
                res = db.load_alter_account(a_user)

                a_list = db.account_list()
                a_record = db.account_usage_record(a_user)
            
                return render_template('ajax/load_alter_account_form.html' , user=user , lv=lv , title=title , a_list=a_list , res=res , a_record=a_record)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

###########################
# /load_add_account_form
###########################
@app.route("/load_add_account_form" , methods=['POST','GET'])
def load_add_account_form():
    if 'user' in session:
        # operation record title
        operation_record_title = '權限管理 - 新增帳號表格'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            
            return render_template('ajax/load_add_account_form.html' , user=user , lv=lv , title=title)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 


#######################
# /load_account_list
#######################
@app.route("/load_account_list" , methods=['POST','GET'])
def load_account_list():
    if 'user' in session:
        # operation record title
        operation_record_title = '權限管理 - 載入帳號清單'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            a_list = db.account_list()
            a_record = db.account_usage_record(user)
            
            return render_template('ajax/load_account_list.html' , user=user , lv=lv , title=title , a_list=a_list , a_record=a_record)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

################
# /db_account
################
@app.route("/db_account")
def db_account():
    if 'user' in session:
        # operation record title
        operation_record_title = '權限管理 - 帳號管理'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            a_list = db.account_list()
            a_record = db.account_usage_record(user)
            
            return render_template('account_manager.html' , user=user , lv=lv , title=title , content=content , a_list=a_list , a_record=a_record)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

######
# /
######
@app.route("/")
def index():
    if 'user' in session:
        # operation record title
        operation_record_title = '載入 index 主頁'    
        # session 
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            res_scraping_news = db.scraping_news()
            res_scraping_film = db.scraping_film()
            res_web_colud = db.web_cloud()
            
            res_ck101_news = db.scraping_news_ck101_news()
            res_etnews = db.scraping_news_etnews()
            res_udn = db.scraping_news_udn()
            res_tech = db.scraping_news_tech()
            res_pcdiy = db.scraping_news_pcdiy()

            return render_template('index.html' , async_mode=socketio.async_mode , msg2=user , msg3=res_scraping_news , msg4=res_scraping_film , msg5=res_web_colud  , user=user , lv=lv , title=title , content=content , res_etnews=res_etnews , res_udn=res_udn , res_tech=res_tech , res_pcdiy=res_pcdiy , res_ck101_news=res_ck101_news)

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login'))

##########
# /login
##########
@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        check_account = db.login(request.form['user'] , request.form['pwd'])

        if type(check_account) == tuple:
            
            # r_time
            r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            # operation record title
            operation_record_title = '登入成功，載入 index 主頁'    
            # session  
            session['user'] = request.form['user']
            # for python3 md5 use method
            m = hashlib.md5()
            m.update(r_time.encode('utf-8'))
            h = m.hexdigest()
            session['login_code'] = h
            session['ip'] = request.remote_addr
            session['lv'] = check_account[0]
            
            # login record
            db.login_record(session['user'],session['login_code'],r_time,session['ip'])

            # operation record
            db.operation_record(r_time , session['user'] , session['login_code'] , operation_record_title)    

            #################
            # main content
            #################
            res_scraping_news  = db.scraping_news()
            res_scraping_film  = db.scraping_film()
            res_web_colud      = db.web_cloud()
            
            res_ck101_news = db.scraping_news_ck101_news()
            res_etnews = db.scraping_news_etnews()
            res_udn = db.scraping_news_udn()
            res_tech = db.scraping_news_tech()
            res_pcdiy = db.scraping_news_pcdiy()

            return render_template('index.html' , msg3=res_scraping_news , msg4=res_scraping_film , msg5=res_web_colud , user=session['user'] , lv=session['lv'] , title=title , content=content , res_etnews=res_etnews , res_udn=res_udn , res_tech=res_tech , res_pcdiy=res_pcdiy , res_ck101_news=res_ck101_news)

        else:
            res_data = "登入失敗，帳密錯誤，重新輸入 !!!"
            return render_template('login.html' , ver=ver , login_msg=res_data , title=title)
    else:
        return render_template('login.html' , ver=ver ,  title=title)

###########
# /logout 
###########
@app.route("/logout")
def logout():
    if 'user' in session:
        # operation record title
        operation_record_title = '登出成功'    
        # session 
        user = session['user']
        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
    
        # logout record
        try:
            db.logout_record(session['user'] , session['login_code'] , r_time)
        except Exception as e:
            logging.info("<< Error >> logout record : " + str(e))
        
        # operation record
        db.operation_record(r_time , user , session['login_code'] , operation_record_title)    

        # clean up session param
        session.pop('user',None)
        session.pop('login_code',None)
        session.pop('ip',None)
        session.pop('lv',None)

    return redirect(url_for('index'))

#########################
# /del_menu_car_record
#########################
@app.route("/del_menu_car_record",methods=['POST','GET'])
def del_menu_car_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click del menu car record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                del_no = request.form['del_no']
                res = db.del_menu_car_record(user , del_no)
                
                if res == 'ok':
                    data = db.menu_car_record(user)
                    return render_template('menu_car_record.html' , msg=data , user=user , lv=lv , title=title)    
                    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

###########################
# /del_menu_money_record
###########################
@app.route("/del_menu_money_record",methods=['POST','GET'])
def del_menu_money_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click del menu money record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                del_no = request.form['del_no']
                res = db.del_menu_money_record(user , del_no)
                
                if res == 'ok':
                    data = db.menu_money_record(user)
                    return render_template('ajax/reload_menu_money_record.html' , msg=data , user=user , lv=lv , title=title)    
                    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

#######################
# /menu_car_record
#######################
@app.route("/menu_car_record")
def menu_car_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click menu car record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            data = db.menu_car_record(user)

            data2 = db.menu_car_record_by_day(user)
            data3 = db.menu_car_record_by_year(user)
            data4 = db.menu_car_record_by_month(user)

            return render_template('menu_car_record.html' , msg=data , msg2=data2 , msg3=data3 , msg4=data4 , user=user , lv=lv , title=title , content=content)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

#######################
# /menu_website_record
#######################
@app.route("/menu_website_record")
def menu_website_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click menu website record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            data = db.menu_website_record(user)
            data2 = db.menu_money_record_by_day(user)
            data3 = db.menu_money_record_by_year(user)
            data4 = db.menu_money_record_by_month(user)

            return render_template('menu_website_record.html' , msg=data , msg2=data2 , msg3=data3 , msg4=data4 , user=user , lv=lv , title=title , content=content)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

#######################
# /menu_money_record
#######################
@app.route("/menu_money_record")
def menu_money_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click menu money record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            data = db.menu_money_record(user)
            data2 = db.menu_money_record_by_day(user)
            data3 = db.menu_money_record_by_year(user)
            data4 = db.menu_money_record_by_month(user)
            data5 = db.menu_money_record_by_kind(user)

            return render_template('menu_money_record.html' , msg=data , msg2=data2 , msg3=data3 , msg4=data4 , msg5=data5 , user=user , lv=lv , title=title , content=content)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

##########################
# /money_record_by_year
##########################
@app.route("/money_record_by_year")
def menu_money_by_year():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click menu money record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            year = db.money_record_by_year(user)
            for by_year in year:
                month = db.money_record_by_month(user,by_year[0])
            
            for by_month in month:
                day = db.money_record_by_day(user,by_year[0],by_month[0])

            for by_day in day:
                total_money = db.money_record_total_money(user,by_year[0],by_month[0],by_day[0])
                content = db.money_record_content(user,by_year[0],by_month[0],by_day[0])

            return render_template('money_record_by_year.html' , year=year , month=month ,  day=day , user=user , lv=lv , title=title)    
            

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))    

####################################
# /select_car_record_by_go_out_km
####################################
@app.route("/select_car_record_by_go_out_km",methods=['POST','GET'])
def select_car_record_by_go_out_km():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click select car record by go out km'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                kind = request.form['kind']
                
                # r_time2
                r_time2 = time.strftime("%Y-%m-%d" , time.localtime())
    
                # select car kind
                data = db.select_car_record_by_kind(kind)

                return render_template("ajax/select_car_record_by_kind.html" , msg=data)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login')) 

##########################
# /add_car_record_form
#########################
@app.route("/add_car_record_form")
def add_car_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click add car record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            # r_time2
            r_time2 = time.strftime("%Y-%m-%d" , time.localtime())
    
            # cars kind
            kind = db.add_car_record_kind(user)

            return render_template("ajax/add_car_record_form.html" , user=user , r_time=r_time2 , kind=kind)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login')) 


###########################
# /add_website_record_form
###########################
@app.route("/add_website_record_form")
def add_website_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click add website record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            # r_time2
            r_time2 = time.strftime("%Y-%m-%d" , time.localtime())
    
            # money kind
            kind = db.add_money_record_kind(user)

            return render_template("ajax/add_money_record_form.html" , user=user , r_time=r_time2 , kind=kind)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login')) 

###########################
# /add_money_record_form
###########################
@app.route("/add_money_record_form")
def add_money_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click add money record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            # r_time2
            r_time2 = time.strftime("%Y-%m-%d" , time.localtime())
    
            # money kind
            kind = db.add_money_record_kind(user)

            return render_template("ajax/add_money_record_form.html" , user=user , r_time=r_time2 , kind=kind)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login')) 

###########################
# /add_calendar_record_form
###########################
@app.route("/add_calendar_record_form")
def add_calendar_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click add calendar record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            # title
            title = '工作日誌'

            # r_time2
            r_time2 = time.strftime("%Y-%m-%d" , time.localtime())
    
            return render_template("ajax/add_calendar_record_form.html" , user=user , r_time=r_time2 , title=title)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))        

###########################
# /add_work_record_form
###########################
@app.route("/add_work_record_form")
def add_work_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click add work record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            # r_time2
            r_time2 = time.strftime("%Y-%m-%d" , time.localtime())
    
            # money kind
            kind = db.add_work_record_kind(user)

            return render_template("ajax/add_work_record_form.html" , user=user , r_time=r_time2 , kind=kind)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))        

##################################
# /submit_add_calendar_record_form
##################################
@app.route("/submit_add_calendar_record_form",methods=['POST','GET'])
def submit_add_calendar_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click submit add calendar record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                account = request.form['user']
                date    = request.form['date']
                title   = request.form['title']
                content = request.form['content']
                r_year  = request.form['r_year']
                r_month = request.form['r_month']

                res = db.submit_add_calendar_record_form(account,date,title,content,r_year,r_month)

                if res == 'ok':
                    title   = '工作日誌'
                    # session 
                    user = session['user']
                    # r_time
                    r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

                    return render_template("ajax/add_calendar_record_form.html" , user=user , r_time=r_time , title=title)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login')) 

##################################
# /submit_add_work_record_form
##################################
@app.route("/submit_add_work_record_form",methods=['POST','GET'])
def submit_add_work_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click submit add work record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                account = request.form['user']
                date    = request.form['date']
                kind    = request.form['kind']
                title   = request.form['title']
                content = request.form['content']

                res = db.submit_add_work_record_form(account,date,kind,title,content)

                if res == 'ok':
                    # session 
                    user = session['user']
                    # r_time
                    r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
                    # money kind
                    kind = db.add_money_record_kind(user)

                    return render_template("ajax/add_work_record_form.html" , user=user , r_time=r_time , kind=kind)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login')) 

##################################
# /submit_add_car_record_form
##################################
@app.route("/submit_add_car_record_form",methods=['POST','GET'])
def submit_add_car_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click submit add car record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                user = request.form['user']
                date = request.form['date']
                kind = request.form['kind']
                go_out_km = request.form['go_out_km']
                go_home_km = request.form['go_home_km']
                total_used_km = request.form['total_used_km']
                destination = request.form['destination']
                r_year = request.form['r_year']
                r_month = request.form['r_month']
                r_day = request.form['r_day']

                res = db.submit_add_car_record_form(user,date,kind,go_out_km,go_home_km,total_used_km,destination,r_year,r_month,r_day)

                if res == 'ok':
                    # session 
                    user = session['user']
                    # r_time
                    r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
                    # money kind
                    kind = db.add_car_record_kind(user)

                    return render_template("ajax/add_car_record_form.html" , user=user , r_time=r_time , kind=kind)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login')) 

##################################
# /submit_add_money_record_form
##################################
@app.route("/submit_add_money_record_form",methods=['POST','GET'])
def submit_add_money_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click submit add money record form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                account = request.form['user']
                date = request.form['date']
                kind = request.form['kind']
                money = request.form['money']
                content = request.form['content']
                record_year = request.form['record_year']
                record_month = request.form['record_month']
                record_day = request.form['record_day']

                res = db.submit_add_money_record_form(account,date,kind,money,content,record_year,record_month,record_day)

                if res == 'ok':
                    # session 
                    user = session['user']
                    # r_time
                    r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
                    # money kind
                    kind = db.add_money_record_kind(user)

                    return render_template("ajax/add_money_record_form.html" , user=user , r_time=r_time , kind=kind)

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login')) 

##########################
# /menu_calendar_record
##########################
@app.route("/menu_calendar_record")
def menu_calendar_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click menu calendar record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            data = db.menu_calendar_record(user)
            by_month = db.menu_calendar_record_by_month(user)
            by_year = db.menu_calendar_record_by_year(user)
            
            return render_template('menu_calendar_record.html' , msg=data , by_month=by_month , by_year=by_year , user=user , lv=lv , title=title , content=content)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

####################################
# /load_menu_money_record_by_kind
####################################
@app.route("/load_menu_money_record_by_kind" , methods=['POST','GET'])
def load_menu_money_record_by_kind():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu money record by kind'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                kind = request.form['kind']
                data = db.load_menu_money_record_by_kind(user , kind)

                return render_template('ajax/load_menu_money_record_by_kind.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

###################################
# /load_menu_money_record_by_day
###################################
@app.route("/load_menu_money_record_by_day" , methods=['POST','GET'])
def load_menu_money_record_by_day():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu money record by day'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                day = request.form['day']
                data = db.load_menu_money_record_by_day(user , day)

                return render_template('ajax/load_menu_money_record_by_day.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

#####################################
# /load_menu_money_record_by_month
#####################################
@app.route("/load_menu_money_record_by_month" , methods=['POST','GET'])
def load_menu_money_record_by_month():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu money record by month'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                month = request.form['month']
                data = db.load_menu_money_record_by_month(user , month)

                return render_template('ajax/load_menu_money_record_by_month.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

#################################
# /load_menu_car_record_by_day
#################################
@app.route("/load_menu_car_record_by_day" , methods=['POST','GET'])
def load_menu_car_record_by_day():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu car record by day'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                day = request.form['day']
                data = db.load_menu_car_record_by_day(user , day)

                return render_template('ajax/load_menu_car_record_by_day.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

###################################
# /load_menu_car_record_by_month
###################################
@app.route("/load_menu_car_record_by_month" , methods=['POST','GET'])
def load_menu_car_record_by_month():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu car record by month'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                month = request.form['month']
                data = db.load_menu_car_record_by_month(user , month)

                return render_template('ajax/load_menu_car_record_by_month.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

##################################
# /load_menu_car_record_by_year
##################################
@app.route("/load_menu_car_record_by_year" , methods=['POST','GET'])
def load_menu_car_record_by_year():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu car record by year'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                year = request.form['year']
                data = db.load_menu_car_record_by_year(user , year)

                return render_template('ajax/load_menu_car_record_by_year.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

####################################
# /load_menu_money_record_by_year
####################################
@app.route("/load_menu_money_record_by_year" , methods=['POST','GET'])
def load_menu_money_record_by_year():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu money record by year'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                year = request.form['year']
                data = db.load_menu_money_record_by_year(user , year)

                return render_template('ajax/load_menu_money_record_by_year.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

###################################
# /load_menu_work_record_by_kind
###################################
@app.route("/load_menu_work_record_by_kind" , methods=['POST','GET'])
def load_menu_work_record_by_kind():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu work record by kind'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                kind = request.form['kind']
                data = db.load_menu_work_record_by_kind(user , kind)

                return render_template('ajax/load_menu_work_record_by_kind.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

########################################
# /load_menu_calendar_record_by_month
########################################
@app.route("/load_menu_calendar_record_by_month" , methods=['POST','GET'])
def load_menu_calendar_record_by_month():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click load menu calendar record by month'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                month = request.form['month']
                data = db.load_menu_calendar_record_by_month(user , month)

                return render_template('ajax/load_menu_calendar_record_by_month.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

######################
# /menu_work_record
######################
@app.route("/menu_work_record")
def menu_work_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click menu work record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            data = db.menu_work_record(user)

            by_kind = db.menu_work_record_by_kind(user)
            by_date = db.menu_work_record_by_date(user)

            return render_template('menu_work_record.html' , msg=data , by_kind=by_kind , by_date=by_date , user=user , lv=lv , title=title , content=content)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

####################################
# reload_menu_money_record_by_day
####################################
@app.route("/reload_menu_money_record_by_day")
def reload_menu_money_record_by_day():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click reload menu money record by day'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            
            data = db.menu_money_record_by_day(user)

            return render_template('ajax/reload_menu_money_record_by_day.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

###########################
# reload_menu_car_record
###########################
@app.route("/reload_menu_car_record")
def reload_menu_car_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click reload menu car record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            
            data = db.menu_car_record(user)

            return render_template('ajax/reload_menu_car_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

#############################
# reload_menu_money_record
#############################
@app.route("/reload_menu_money_record")
def reload_menu_money_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click reload menu money record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            
            data = db.menu_money_record(user)

            return render_template('ajax/reload_menu_money_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

############################
# reload_menu_calendar_record
############################
@app.route("/reload_menu_calendar_record")
def reload_menu_calendar_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click reload menu calendar record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            data = db.menu_calendar_record(user)
            
            return render_template('ajax/reload_menu_calendar_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

############################
# reload_menu_work_record
############################
@app.route("/reload_menu_work_record")
def reload_menu_work_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click reload menu work record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            data = db.menu_work_record(user)

            return render_template('ajax/reload_menu_work_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

############################
# /detail_calendar_record
############################
@app.route("/detail_calendar_record" , methods=['POST','GET'])
def detail_calendar_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click detail calendar record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                no = request.form['no']
                data = db.detail_calendar_record(no)
                
                return render_template('ajax/detail_calendar_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

########################
# /detail_work_record
########################
@app.route("/detail_work_record" , methods=['POST','GET'])
def detail_work_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click detail work record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                no = request.form['no']
                data = db.detail_work_record(no)

                return render_template('ajax/detail_work_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

####################################
# /del_alter_calendar_record_form
####################################
@app.route("/del_alter_calendar_record_form" , methods=['POST','GET'])
def del_alter_calendar_record_form():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click del alter calendar record_form'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                no      = request.form['no']

                res = db.del_alter_calendar_record_form(no)

                if res == 'ok':
                    data = db.detail_calendar_record(no)
                    
                    return render_template('ajax/detail_calendar_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

##################################
# /submit_alter_calendar_record
##################################
@app.route("/submit_alter_calendar_record" , methods=['POST','GET'])
def submit_alter_calendar_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click submit alter work record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                no      = request.form['no']
                r_time  = request.form['r_time']
                title   = request.form['title']
                content = request.form['content']

                res = db.submit_alter_calendar_record(r_time,no,title,content)

                if res == 'ok':
                    data = db.detail_calendar_record(no)
                    
                    return render_template('ajax/detail_calendar_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

##############################
# /submit_alter_work_record
##############################
@app.route("/submit_alter_work_record" , methods=['POST','GET'])
def submit_alter_work_record():
    if 'user' in session:
        # operation record title
        operation_record_title = 'click submit alter work record'    
        # session
        user = session['user']
        lv = session['lv']
        login_code = session['login_code']

        # r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        # check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            # operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == "POST":
                no = request.form['no']
                r_time = request.form['r_time']
                kind = request.form['kind']
                title = request.form['title']
                content = request.form['content']

                res = db.submit_alter_work_record(r_time,no,kind,title,content)

                if res == 'ok':
                    data = db.detail_work_record(no)
                    
                    return render_template('ajax/detail_work_record.html' , msg=data , user=user , lv=lv , title=title)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

############################################################################################################ WebSocket - Flask-SocketIO

#############
# socketIO 
#############

Namespace = '/echo'

@app.route("/echo")
def echo():
    return render_template('echo.html')    

@app.route("/push")
def push_once():
    # r_time
    r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
    event_name = '/echo'
    broadcasted_data = {'data':"test message"}
    socketio.emit(event_name, broadcasted_data , broadcast=False , namespace=Namespace)
    return r_time

@socketio.on('my event' , namespace=Namespace)
def test_message(message):
    emit('my response', {'data': message['data'] , 'count':1})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect' , namespace=Namespace)
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect' , namespace=Namespace)
def test_disconnect():
    logging.info('Client disconnected')

'''
@socketio.on('connect', namespace='/')
def test_connect():
    while True:
        socketio.sleep(5)
        t = random_int_list(1, 100, 10)
        emit('server_response',{'data': t},namespace='/')
 
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list
  
@socketio.on('disconnect', namespace='/')  
def test_disconnect():  
    logging.info('Client disconnected')  
'''

########################################################################################################################################
#
# start
#
########################################################################################################################################
if __name__ == "__main__":
    
    ##########
    # Flask
    ##########
    #app.run(host="0.0.0.0" , port=8080 , debug=True)
    
    ###################
    # Flask-SocketIO
    ###################
    socketio.run(app , host="0.0.0.0" , port=8095 , debug=True)