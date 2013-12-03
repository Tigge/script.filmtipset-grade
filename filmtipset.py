# Copyright (c) 2013, Gustav Tiger
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import urllib
import json

class Filmtipset:
    """Class for communicating with the Filmtipset API"""
    
    URL_API = "http://www.filmtipset.se/api/api.cgi"
    
    def __init__(self, access_key, user_key, user):
        self.access_key = access_key
        self.user_key = user_key
        self.user = user

    def _request(self, action, parameters):
        """Filmtipset API request, takes an action (imdb, movie, grade, etc)
           and a map of additional parameters"""
        values = {"accesskey": self.access_key,
                  "userkey": self.user_key,
                  "user": self.user,
                  "returntype": "json",
                  "action": action}
        
        values.update(parameters)
        
        url = Filmtipset.URL_API + "?" + urllib.urlencode(values)
        return json.load(urllib.urlopen(url), "iso-8859-1")

    def get_movie(self, movie):
        """ Get movie information from a filmtipset id"""
        data = self._request("movie", {"id": movie, "nocomments": 1})
        return data[0]["data"][0]["movie"]
        
    def get_movie_imdb(self, imdb):
        """ Get movie information from an iMDB id"""
        if imdb.startswith("tt"):
            imdb = imdb[2:]
        data = self._request("imdb", {"id": imdb, "nocomments": 1})
        return data[0]["data"][0]["movie"]

    def grade(self, movie, grade):
        """ Grade movie specified by a filmtipset id, and a grade [1-5]"""
        response = self._request("grade", {"id": movie, "grade": grade})[0]
        try:
            movie = response["data"][0]["movie"]
            seen  = movie["grade"]["type"] == "seen"
            return seen and int(movie["grade"]["value"]) == int(grade)
        except KeyError:
            return False
