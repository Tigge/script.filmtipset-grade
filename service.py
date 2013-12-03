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

import xbmc
import xbmcaddon
import xbmcgui
import filmtipset

FILMTIPSET_ACCESS_KEY = "7ndg3Q3qwW8dPzbJMrB5Rw"

class XBMCPlayer(xbmc.Player):

    def __init__(self, *args):
        self.imdb = None
        self.time = None
        self.time_total = None
        
    def onPlayBackStarted(self):
        self.update()

    def onPlayBackEnded(self):
        self.onDone()

    def onPlayBackStopped(self):
        self.onDone()

    def update(self):
        info = self.getVideoInfoTag()
        self.imdb = info.getIMDBNumber()
        self.time = self.getTime()
        self.time_total = self.getTotalTime()

    def onDone(self):
        print "getTime", self.time
        print "getTotalTime", self.time_total
        print "imdb", self.imdb
        
        addon = xbmcaddon.Addon(id='script.filmtipset-grade')
        
        key = addon.getSetting("key")
        user = addon.getSetting("user")
        
        grader = filmtipset.Filmtipset(FILMTIPSET_ACCESS_KEY, key, user)
        movie = grader.get_movie_imdb(self.imdb)
        print movie
        if movie["grade"]["type"] != "seen":
            
            dialog = xbmcgui.Dialog()
            grade = dialog.select("Grade " + movie["orgname"] + " on filmtipset:",
                ["Skip", "1", "2", "3", "4", "5"])
            
            if grade != 0:
                print dialog, grade
                print grader.grade(movie["id"], grade)

player = XBMCPlayer()

while(not xbmc.abortRequested):
    if player.isPlayingVideo():
        player.update()
    xbmc.sleep(1000)

