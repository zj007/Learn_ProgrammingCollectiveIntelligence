#encoding:utf8

import sqlite3
import sys

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
    
    def get_index(self, word):
        wordrow = self._con.execute(
                'select rowid from wordlist where word="%s"' % word
            ).fetchone()
        if wordrow != None:
            wordid = wordrow[0]
        else:
            return []
        cur = self._con.execute(
                'select urlid, wordid, location from wordlocation where wordid=%d' % wordid
                )
        if cur != None:
             l = [row for row in cur]
             l.sort(key = lambda x : x[0])
             return l
        return []

    def get_url_name(self, id):
        return self._con.execute(
                'select url from urllist where rowid=%d' % id
                ).fetchone()[0]

    def get_match_rows_new(self, q):
        words = q.split(' ')
        url_set = [None for i in xrange(len(words))]
        for i, word in enumerate(words):
            url_set[i] = {e[0] for e in self.get_index(word)}
        result = url_set[0]
        for i in xrange(1, len(words)):
            result &= url_set[i]
        return [self.get_url_name(e) for e in result]
    
    def get_scored_list(self, rows, wordids):
        total_scores = {row[0]:0 for row in rows}
        
        weights = [
            
        ]
        
        for (weight, scores) in weights:
            for url in total_scores:
                total_scores[url] += weight * scores[url]
        
        return total_scores
    
    def query(self, q):
        rows, wordids = self.get_match_rows(q)
        scores = self.get_scored_list(rows, wordids)
        url_list = [(score, url) for url, score in scores.items()]
        url_list.sort(key = lambda x : x[0], reverse = True)
        for score, url in url_list[:10]:
            print '%f\t%s' % (score, self.get_url_name(url))

if __name__ == '__main__':
    s = searcher('searchindex.db')
    print s.get_match_rows_new(sys.argv[1])
