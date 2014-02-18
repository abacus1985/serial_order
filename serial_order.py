#!/usr/bin/env python

from pytvdbapi import api
db = api.TVDB('6FEF706303C7EBBD')
result = db.search('Dexter', 'it')
len(result)
show = result[0]
print(show.SeriesName)
len(show)  # List the number of seasons of the show, season 0 is the specials season
season = show[1]
len(season)  # List the number of episodes in the season, they start at index 1
print(season.season_number)
episode = season[2]
print(episode.EpisodeNumber)
print(episode.EpisodeName)
