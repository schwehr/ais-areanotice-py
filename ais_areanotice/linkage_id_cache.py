#!/usr/bin/env python

import os
import pickle
import datetime

class Linkage:
    def __init__(self,cache_file,min_id=0,max_id=1023):
        self.cache_file = cache_file
        self.min_id = min_id
        self.max_id = max_id

        if os.path.isfile(cache_file):
            infile = file(cache_file)
            self.cache = pickle.load(infile)
            expired = []
            now = datetime.datetime.utcnow()
            for k,v in self.cache.iteritems():
                if v['expiration'] < now:
                    expired.append(k)
            for e in expired:
                del(self.cache[e])
        else:
            self.cache = {}

    def getID(self,key,expiration):
        if self.cache.has_key(key):
            return self.cache[key]['id']
        unavailable = []
        for k,v in self.cache.iteritems():
            unavailable.append(v['id'])
        candidate = self.min_id
        while candidate <= self.max_id:
            if not candidate in unavailable:
                self.cache[key] = {'id':candidate,'expiration':expiration}
                self.save()
                return candidate
            candidate += 1
        return None
    

    def save(self):
        outfile = file(self.cache_file,'w')
        pickle.dump(self.cache,outfile)
