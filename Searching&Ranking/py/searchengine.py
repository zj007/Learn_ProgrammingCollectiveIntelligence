#encoding:utf8

import urllib2
import BeautifulSoup as soup
from urlparse import urljoin

class crawler:
    
    ignore_words = ('the', 'of', 'to', 'and', 'a',
                    'an', 'is', 'in', 'it', 'he',
                    'she', 'then', 'else', 'if',
                    'while', 'when', 'hi', 'hello'
                    )
    
    def __init__(self, db_name):
        """初始化crawler，传入数据库名称"""
        pass
    
    def __del__(self):
        pass
        
    def db_commit(self):
        pass
       
    def get_entry_id(self, table, field, value, create_new = True):
        """获取条目的id，如果条目不存在，就将条目加入到数据库中"""
        return None
        
    def add_to_index(self, url, soup):
        """为每个网页建立索引"""
        print 'Indexing %s' % url
    
    def get_text_only(self, soup):
        """从html中提出文本"""
        return None
        
    def separatewords(self, text):
        """分词"""
        return None
        
    def isindexed(self, url):
        return False
    
    def add_linkref(self, url_from, utl_to, link_text):
        pass
    
    def crawl(self, pages, depth = 2):
        """从一小组的网页开始广度优先搜索，直到某一给定的深度，
        期间为网页建立索引
        """
        for i in xrange(depth):
            new_pages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print 'Could not open %s'%page
                    continue
                s = soup.BeautifulSoup(c.read())
                self.add_to_index(page, soup)
        
                links = s('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        href = link['href']
                        if 'http' == href[:4]:
                            url = href
                        else:
                            url = urljoin(page, href)
                        url = url.split('#')[0]
                        if not self.isindexed(url):
                            new_pages.add(url)
                        link_text = self.get_text_only(link)
                        self.add_linkref(page, url, link_text)
                self.db_commit()
            pages = new_pages
        
    def create_index_tables(self):
        """创建数据库表"""
        pass
    
    
