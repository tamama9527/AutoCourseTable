#-*- coding: UTF-8 -*- 
#Author: fb.me/jhang.y.wei
#ez to create useful course timetable
#if have any question or bug,please pm author 
import requests
from BeautifulSoup import BeautifulSoup
import json
import re
import time
account=""
password=""


year=time.localtime().tm_year
str_year=str(year-1911)
month=time.localtime().tm_mon
if month > 7:
    semester = "1"
else:
    semester = "2"

login_url='https://apps.fcu.edu.tw/main/infologin.aspx'
class_url='https://apps.fcu.edu.tw/main/S3202/S3202_timetable_new.aspx/GetCurriculum'
timesetting ={'year': str_year, 'smester': semester}
header_info={
'Accept':'application/json, text/plain, */*',
'Content-Type':'application/json; charset=UTF-8',
}
postdata={}
output={}
c_time={
"1": "08:10~09:00",
"2": "09:10~10:00",
"3": "10:10~11:00",
"4": "11:10~12:00",
"5": "12:10~13:00",
"6": "13:10~14:00",
"7": "14:10~15:00",
"8": "15:10~16:00",
"9": "16:10~17:00",
"10": "17:10~18:00",
"11": "18:10~19:00",
"12": "19:10~20:00",
"13": "20:10~21:00",
"14": "21:10~22:00",
"15": "22:10~23:00"}
#create a new session
s=requests.session()
first=s.get(login_url)
login_page = BeautifulSoup(first.text)
#do get necessary postdata
for element in login_page.findAll('input',{'value': True}):
    postdata[str(element['name'])]=str(element['value'])
del postdata['CancelButton']
postdata['txtUserName']=account
postdata['txtPassword']=password
login_html=s.post(login_url,data=postdata)
login_info = BeautifulSoup(login_html.text)
try:
    #if login fail can print where is wrong
    error=login_info.findAll('span',{'id':'FailureText'})[0]
    error=str(error)[23:len(error)-8]
except:
    #to get course json data
    output['Course']={}
    output['Time']={}
    class_json=s.post(class_url,data=json.dumps(timesetting),headers=header_info)
    class_data=json.loads(class_json.text)
    for i in range(0,15):
        output['Time'][str(i+1)]=c_time[str(i+1)]
    for each_day in class_data['d']['list']:
        print each_day['week']
        for each_class in each_day['courses']:
            #get the course secret key
            secret_key='https://apps.fcu.edu.tw/main/S3202/redirect.aspx?mode=21&code='+str(each_class['course_id'])
            get_secret_date=s.get(secret_key)
            secret_data = BeautifulSoup(get_secret_date.text)

            #use secret key to get more detail like teacher course type
            course_id=str(secret_data.findAll('script',{'type':'text/javascript'})[0]).split('window.sessionStorage.setItem')[1]
            course_id=course_id[15:len(course_id)-5]
            classid={"course_id":""}
            classid['course_id']=course_id

            #course type
            get_class_type=s.post('https://service120-sds.fcu.edu.tw/W3212/action/getdata.aspx/getCourseInfor1',data=json.dumps(classid),headers=header_info)
            type_json_data=str(get_class_type.text.encode('utf-8'))
            class_type = get_class_type.text.split('\"')[18][0:2]
            #teacher name
            get_teacher_name=s.post('https://service120-sds.fcu.edu.tw/W3212/action/getdata.aspx/getCourseInfor2',data=json.dumps(classid),headers=header_info)
            #use 'try catch' to avoid the teacher name is null
            try:
                teacher_name= get_teacher_name.text.split('\"')[6][0:3]
            except:
                print("teacher not found")
                teacher_name="null"
            name=str(each_day['week'])+'-'+str(each_class["period"])
            code='('+each_class['selcode']+')'
            if str(each_class['selcode']) not in output['Course']:
                r=output['Course'][str(each_class['selcode'])]={}
                r['time']={}
            else:
                r=output['Course'][str(each_class['selcode'])]
            r['name']=each_class['title']
            r['teacher']=teacher_name
            r['time'].update({name:each_class["roomname"]})
            print class_type
            if class_type ==u'選修':
                r['status']=0
            else:
                r['status']=1
    #write to a json file for web page
    with open("json/"+str_year+"_"+semester+"_course.json", "w") as outfile:
         json.dump(output, outfile, sort_keys = True, indent = 4)
    print 'success'
else:
    print error
