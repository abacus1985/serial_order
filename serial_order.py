#!/usr/bin/env python

import os, shutil
from pytvdbapi import api

db = api.TVDB('6FEF706303C7EBBD')

# INIZIO
print('#'*80)
print('@' + ' '*78 + '@')
print('@' + ' '*36 + 'INIZIO' + ' ' *36 + '@')
print('@' + ' '*78 + '@')
print('#'*80)
print
print

radice = '/var/nas1'

arr_lista_cart = os.listdir(radice)
#print arr_lista_cart

print
print('#'*80)
print('@' + ' '*78 + '@')
print('@' + ' '*20 + 'Cerco cartelle da escludere e ristampo' + ' '*20 + '@')
print('@' + ' '*78 + '@')
print('#'*80)
print

a = '00@ - Windows utility'
b = '00@ - FILM'

arr_lista_cart.remove(a)
arr_lista_cart.remove(b)

print('OK')

print
print('#'*80)
print('@' + ' '*78 + '@')
print('@' + ' '*14 + 'Cerco le serie su thetvdb.com e stampo il responso' + ' '*14 + '@')
print('@' + ' '*78 + '@')
print('#'*80)
print

for s in arr_lista_cart:
	print('- Cerco %s' % s)
	result = db.search(s, 'it', False)
	if len(result) > 0:
		print('TOVATO')
		for show in result:
			stringa = '   Nome: %s' % show.SeriesName
			print(stringa)
			stringa = '   Stagioni: %i' % len(show)
			print(stringa)
	else:
		print('NON TROVATA')
		

#print arr_lista_cart

# FINE
print
print
print('#'*80)
print('@' + ' '*78 + '@')
print('@' + ' '*37 + 'FINE' + ' ' *37 + '@')
print('@' + ' '*78 + '@')
print('#'*80)
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

	
