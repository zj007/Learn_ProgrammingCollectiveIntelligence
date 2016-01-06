#encoding:utf8

import sqlite3
import sys
from cibiao import ignore_words

class searcher(object):
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
    
    def get_wordlocation(self, word):
        wordrow = self._con.execute(
                'select rowid from wordlist where word="%s"' % word
            ).fetchone()
        if wordrow != None:
            wordid = wordrow[0]
        else:
            return [], None
        cur = self._con.execute(
                'select urlid, wordid, location from wordlocation where wordid=%d' % wordid
                )
        if cur != None:
             l = [row for row in cur]
             l.sort(key = lambda x : x[2])
             l.sort(key = lambda x : x[0])
             #print 'w_L : %s' % l
             return l, wordid
        return [], wordid

    def get_url_name(self, id):
        return self._con.execute(
                'select url from urllist where rowid=%d' % id
                ).fetchone()[0]

    def get_match_urls(self, q):
        words = [w for w in q.split(' ') if w and w not in ignore_words]
        url_set = [None for i in xrange(len(words))]
        wordids = []
        ori_rows = []
        for i, word in enumerate(words):
            word_location, wordid = self.get_wordlocation(word)
            ori_rows.extend(word_location)
            url_set[i] = {e[0] for e in word_location}
            wordids.append(wordid)
        result_url = url_set[0]
        for i in xrange(1, len(words)):
            result_url &= url_set[i]
        rows = []
        for e in ori_rows:
            if e[0] in result_url:
                rows.append(e)
        return rows, wordids
    
    def get_scored_list(self, rows, wordids):
        total_scores = {row[0]:0 for row in rows}
        
        weights = [
            (0.4, self.frequency_score(rows, wordids)),  
            (0.6, self.location_score(rows, wordids)),  
        ]
        
        for (weight, scores) in weights:
            for url in total_scores:
                total_scores[url] += weight * scores[url]
        
        return total_scores
    
    def query(self, q):
        rows, wordids = self.get_match_urls(q)
        #print rows
        scores = self.get_scored_list(rows, wordids)
        url_list = [(score, url) for url, score in scores.items()]
        url_list.sort(key = lambda x : x[0], reverse = True)
        for score, url in url_list[:10]:
            print '%f\t%s' % (score, self.get_url_name(url))

    def normalizescores(self, scores, big_is_better = True):
        min_value = 0.00001
        if not big_is_better:
            min_score = min(scores.values())
            return {url:float(min_score) / max(min_value, score) for url, score in scores.items()}
        else:
            max_score = max(scores.values())
            if max_score <= 0:
                max_score = min_value
            return {url:float(score) / max_score for url, score in scores.items()}
    
    #rank
    def frequency_score(self, rows, wordids):
        counts = {row[0] : 0 for row in rows}
        for row in rows:
            counts[row[0]] += 1
        return self.normalizescores(counts)
        #return counts

    def location_score(self, rows, wordids):
        min_location = {row[0] : 10000000 for row in rows}
        word_map = {wordid:[] for wordid in wordids}
        for row in rows:
            word_map[row[1]].append(row)
        for url in min_location:
            location = 0
            for wordid in wordids:
                for row in word_map[wordid]:
                    if row[0] == url:
                        location += row[2]
                        break
            min_location[url] = location
        #print min_location
        return self.normalizescores(min_location, False)

    def distance_score(self, rows, wordids):
        if len(wordids) <= 1:
            return {row[0] : 1.0 for row in rows}
        pass

if __name__ == '__main__':
    s = searcher('searchindex.db')
    s.query(sys.argv[1])
