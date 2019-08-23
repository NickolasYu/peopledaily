# -*- coding:UTF-8 -*-
import re
import urllib
import sys
from bs4 import BeautifulSoup
from datetime import date
from tool_box import tool_box
from DBConnect import MYSQL
from log import log

class spider():
    def __init__(self):
        # setup default encoding
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
        # get configuration information from config.json
        self.tool = tool_box()
        current_path = self.tool.current_path
        config_file = self.tool.get_config()

        # set up the parent url
        self.today = date.today()
        self.urlHead = 'http://paper.people.com.cn/rmrb/html/' 
        self.urlDate = self.today.strftime("%Y-%m/%d") + '/'
        urlTail = 'nbs.D110000renmrb_01.htm'
        self.url = self.urlHead + self.urlDate + urlTail   

        # create news storing main floder
        self.news_path = current_path + config_file['Newspath'].strip()
        self.tool.mkdir(self.news_path)

        # create today's news storing floder
        self.news_path_today = self.news_path + '/' + str(self.today)
        self.tool.mkdir(self.news_path_today)

        # create log floder and new log object
        self.log_path = current_path + config_file['Logpath'].strip()
        self.tool.mkdir(self.log_path)
        self.log = log(self.log_path)

        # connect DB
        try:
            self.db = MYSQL('innovation', config_file)
            self.log.log_event(10, 'DB connected successfully!')
        except:
            self.log.log_event(50, 'DB connection failed!')

    # store all the second urls to list
    def get_all_url(self):
        html = urllib.urlopen(self.url)
        soup = BeautifulSoup(html, 'html.parser')

        all_url = []
        atags = soup.find_all('a', id = 'pageLink')
        for atag in atags:
            href = atag.get('href','')
            if re.search('^n', href):
                link = href
            else:
                link = href[2:len(href)]
            htmltemp = urllib.urlopen(self.urlHead + self.urlDate + link)
            souptemp = BeautifulSoup(htmltemp, 'html.parser')
            tags = souptemp('a')
            for tag in tags:
                link = tag.get('href', '')
                if re.search('^nw', link):
                    if link not in all_url:
                            all_url.append(link)
        return all_url

    def store_news(self):
        self.log.log_event(10, 'Start crawling...')
        for a in self.get_all_url():
            suburl = self.urlHead + self.urlDate + a
            subhtml = urllib.urlopen(suburl)
            subsoup = BeautifulSoup(subhtml, 'html.parser')
            pdate = a[17:25]                              # get publish date
            layout = int(a[28:30])                        # get layout number
            sheet = int(a[26:27])                         # get sheet number
            fsubj = subsoup.find('h1').get_text().strip() # get first subject
            ssubj = subsoup.find('h2').get_text().strip() # get second subject
            news_name = a[0:-4]                           # get news file name
            content = ''                                  # get news content
            contents = subsoup.find_all('div', id = 'articleContent')
            for con in contents:
                content = content + con.get_text()
            content = content.rstrip()

            # save data to db
            values = [pdate, layout, sheet, fsubj, ssubj, news_name]
            self.log.log_event(10, 'News' + news_name + ' is storing...')
            self.db.sql_insert('peopledaily', values)
            self.log.log_event(10, 'News' + news_name + ' is stored into DB')

            # save news to floder
            self.log.log_event(10, 'News' + news_name + ' is loading to ' + self.news_path_today + '/ ...')
            fhand = open(self.news_path_today + '/' + news_name + '.txt', 'w+')
            fhand.writelines(content)
            fhand.close()
            self.log.log_event(10, 'News' + news_name + ' is loaded')

        self.db.close()
        self.log.log_event(10, 'Crawling is completed successfully!')
