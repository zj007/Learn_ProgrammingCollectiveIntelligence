#encoding:utf8

import urllib2
import BeautifulSoup as soup
from urlparse import urljoin
import sqlite3
import re

class crawler:
    
    ignore_words = ('the', 'of', 'to', 'and', 'a',
                    'an', 'is', 'in', 'it', 'he',
                    'she', 'then', 'else', 'if',
                    'while', 'when', 'hi', 'hello'
                    )
    
    def __init__(self, db_name):
        """初始化crawler，传入数据库名称"""
        self._con = sqlite3.connect(db_name)
    
    def __del__(self):
        self._con.close()
        
    def db_commit(self):
        self._con.commit()
    
    def get_con(self):
        return self._con
       
    def get_entry_id(self, table, field, value, create_new = True):
        """获取条目的id，如果条目不存在，就将条目加入到数据库中"""
        cur = self._con.execute(
            'select rowid from %s where %s = "%s"' % (table, field, value)
        )
        res = cur.fetchone()
        if res == None:
            cur = self._con.execute(
                "insert into %s (%s) values ('%s')" % (table, field, value)
            )
            return cur.lastrowid
        else:
            return res[0]
        
    def add_to_index(self, url, soup):
        """为每个网页建立索引"""
        if self.isindexed(url):
            print 'url:%s already indexed'
            return
        
        print 'Indexing %s' % url
        
        text = self.get_text_only(soup)
        words = self.separatewords(text)
        
        urlid = self.get_entry_id('urllist', 'url', url)
        
        for i in xrange(len(words)):
            word = words[i]
            if word in self.ignore_words:
                continue
            wordid = self.get_entry_id('wordlist', 'word', word)
            self._con.execute('insert into wordlocation(urlid, wordid, location) \
                values (%d, %d, %d)' % (urlid, wordid, i))
    
    def get_text_only(self, soup):
        """从html中提出文本"""
        v = soup.string
        if v == None:
            c = soup.contents
            result_text = ''
            for t in c:
                sub_text = self.get_text_only(t)
                result_text += sub_text + '\n'
            return result_text
        return v.strip()
        
    def separatewords(self, text):
        """分词"""
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']
        
    def isindexed(self, url):
        u = self._con.execute(
            "select rowid from urllist where url='%s'" % url
        ).fetchone()
        if u != None:
            v = self._con.execute(
                'select * from wordlocation where urlid=%d' % u[0]
            ).fetchone()
            if v != None:
                return True
        return False
    
    def add_linkref(self, url_from, utl_to, link_text):
        pass
    
    def crawl(self, pages, allowed_domain ,depth = 2):
        """从一小组的网页开始广度优先搜索，直到某一给定的深度，
        期间为网页建立索引
        """
        for i in xrange(depth):
            new_pages = set()
            for page in pages:
                page_allowed = True
                if allowed_domain:
                    page_allowed = False
                    for domain in allowed_domain:
                        if page.startswith(domain):
                            page_allowed = True
                if not page_allowed:
                    continue
                try:
                    c = urllib2.urlopen(page)
                except:
                    print 'Could not open %s'%page
                    continue
                s = soup.BeautifulSoup(c.read())
                self.add_to_index(page, s)
        
                links = s('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        href = link['href']
                        if 'http' == href[:4]:
                            url = href
                        else:
                            url = urljoin(page, href)
                        url = url.split('#')[0]
                        if '\'' in url or '"' in url:
                            continue
                        if not self.isindexed(url):
                            new_pages.add(url)
                        link_text = self.get_text_only(link)
                        self.add_linkref(page, url, link_text)
                self.db_commit()
            pages = new_pages
        
    def create_index_tables(self):
        """创建数据库表"""
        self._con.execute('create table urllist(url)')
        self._con.execute('create table wordlist(word)')
        self._con.execute('create table wordlocation(urlid, wordid, location)')
        self._con.execute('create table link(fromid integer, toid integer)')
        self._con.execute('create table linkwords(wordid, linkid)')
        self._con.execute('create index wordidx on wordlist(word)')
        self._con.execute('create index urlidx on urllist(url)')
        self._con.execute('create index wordurlidx on wordlocation(wordid)')
        self._con.execute('create index urltoidx on link(toid)')
        self._con.execute('create index urlfromidx on link(fromid)')
        self.db_commit()
    
if __name__ == '__main__':
    pages = ['https://en.wikipedia.org/wiki/Python']
    allowed_domain = ['https://en.wikipedia.org']
    my_crawler = crawler('searchindex.db')
    my_crawler.create_index_tables()
    my_crawler.crawl(pages, allowed_domain)
