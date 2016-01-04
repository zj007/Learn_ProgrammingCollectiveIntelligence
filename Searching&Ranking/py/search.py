#encoding:utf8

import sqlite3

class searcher:
    def __init__(self, db_name):
        self._con = sqlite3.connect(db_name)
        
    def __del__(self):
        self._con.close()
    
    def get_match_rows(self, q):
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []
        
        words = q.split(' ')
        tablenumber = 0
        
        for word in words:
            wordrow = self._con.execute(
                'select rowid from wordlist where word="%s"' % word
            ).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber - 1, tablenumber)
                fieldlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' %tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1
        full_query = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        cur = self._con.execute(full_query)
        rows = [row for row in cur]
        
        return rows, wordids