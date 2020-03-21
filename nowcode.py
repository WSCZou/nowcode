import requests
from lxml import etree
from pyquery import PyQuery as pq
import pymysql
import time
import re
import json


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://www.nowcoder.com/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'www.nowcoder.com'
        }
        self.login_url = 'https://www.nowcoder.com/login'
        self.post_url = 'https://www.nowcoder.com/login/do?token='
        self.session = requests.Session()
        self.home_url='https://www.nowcoder.com/makePaper?source=3&tagIds=571&difficulty=3&questionCount=5'

    def myreplace(a):
        b = a.replace('[', '')
        c = b.replace(',', '')
        d = c.replace('\'', '')
        e = d.replace(']', '')
        f = e.replace(' ', '')
        return f

    def login(self, email, pwd):
        post_data = {
            'email': email,
            'pwd': pwd,
        }
        def parse_url(data={}):
            item = data.items()
            urls = "?"
            for i in item:
                (key, value) = i
                temp_str = key + "=" + value
                urls = urls + temp_str + "&"
            urls = urls[:len(urls) - 1]
            return urls
        def parse_answerurl(data={}):
            item = data.items()
            answerurl = "?"
            for i in item:
                (key, value) = i
                temp_str = key + "=" + value
                answerurl = answerurl + temp_str + "&"
            answerurl = answerurl[:len(answerurl) - 1]
            return answerurl

        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
                response2= self.session.post(self.home_url)
                #print(response2.text)
                selector=etree.HTML(response2.text)
                opid=selector.xpath('//*[@id="jsQuestionInfo"]/@data-pid')
                otid=selector.xpath('//*[@id="jsQuestionInfo"]/@data-tid')
                oqid=selector.xpath('/ html / body / div[1] / div[2] / div[1] / div / div[4] / ul/ li/ a/@data-qid')
        URL = "https://www.nowcoder.com/question/next"
        count=321
        for i in oqid:
            dicts = {'pid': opid[0], 'qid': i, 'tid': otid[0]}
            newurl=URL + parse_url(dicts)
            newcreat=str(newurl)
            response3= self.session.post(url=newcreat)
            #print(response3.text)
            #selector1 = etree.HTML(response3.text)
            doc=pq(response3.text)
            #question=selector1.xpath('/html/body/div[1]/div[2]/div[1]/div/div[3]/div[1]/div/text()')

            question=doc('.subject-question')
            question2=question.text()
            question3 = json.dumps(question2,ensure_ascii=False)


            #question3=question2.replace('\n','\\n')
            #question4=question3.replace('"',"\"")
            #question2=question1.decode('utf-8')
            time1 = time.strftime("%Y-%m-%d")
            count = count + 1
            db = pymysql.connect("118.89.36.125", "root", "1126", "ExamSystem", charset="utf8")
            #db = pymysql.connect("localhost", "root", "123456", "spiders",charset="utf8")
            question4 = db.escape_string(question3)
            cursor = db.cursor()
            #cursor.execute("set names gb2312")
            sql1 = "INSERT INTO Question(date,description,lang,type) VALUES ('%s','%s','%s','%s');"%(time1,question4,'Javascript','radio')
            cursor.execute(sql1)
            db.commit()

            choice=doc('.subject-options')

            s = []
            for li in choice.items():
                content = li.text()
                s.append('\"'+content+'\"')

            str1 = ",".join(s)
            s2='['
            s3=']'
            str2=s2+str1+s3
            str3=json.dumps(str2,ensure_ascii=False)
            str4=db.escape_string(str3)
            sql3 = "update Question set content='" + str4 + "' where id='%d'" % count
            cursor.execute(sql3)
            db.commit()

        answerurl="https://www.nowcoder.com/question/next"
        dicts2 = {'pid': opid[0], 'qid': oqid[0],'tid':otid[0]}
        answernewurl = answerurl + parse_answerurl(dicts2)
        answerurlcreat=str(answernewurl)
        response_answer = self.session.post(url=answerurlcreat)
        response_answer
        count = count-4
        m=1
        for i in oqid:
            if m == 1:
                m=m+1
                continue
            jiexiurl="https://www.nowcoder.com/test/question/done"
            dicts2 = {'tid': otid[0], 'qid': i }
            jiexinewnewurl = jiexiurl + parse_answerurl(dicts2)
            jixiurlcreat=str(jiexinewnewurl)
            response_jiexi=self.session.get(url=jixiurlcreat)
            anser=pq(response_jiexi.text)
            answer2=anser('.result-subject-answer h1')
            answer3 = answer2.text()
            answer4=re.findall('[A-Z]{1,4}',answer3)
            answer5=str(answer4)
            answer5=Login.myreplace(answer5)
            answer6=json.dumps(answer5, ensure_ascii=False)
            answer7 = db.escape_string(answer6)

            sql4 = "update Question set answer='" + answer7 + "' where id='%d'" % count
            count=count+1
            cursor.execute(sql4)
            db.commit()
            print(answer7)
        db.close()



if __name__ == "__main__":
    login = Login()
    login.login(email='1214311807@qq.com', pwd='zjl2111999314')