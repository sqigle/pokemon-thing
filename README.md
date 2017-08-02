## damage calc for pokemon
so the plan is to make a damage 
calc for pokemon

this is my first major project using classes, 
databases, and webscraping so it will probably suck

here are my plans

main features:
* create and store sets from showdown format
* search and print sets
* calculate damage done by a pokemon with some set to a pokemon with some set

getting pokemon:
* scrape pokemon data from serebii
* get number, name, types, abilities, base stats, learnset

storing pokemon:
* use sqlite3 table with columns (number, name, type 1, type 2, ability 1, 2, 3, hp, ..., speed)
* dex number stored in 3 digits (eg 005)
* store learnset of each pokemon in resources/learnsets/<dex #>.csv

creating and storing sets:
* paste in showdown format
* use regex to get name, item, ability, evs, nature, ivs, and moves
* store in sqlite3 table with columns (set name, pokemon, item, ability, evs, nature, ivs, move 1, 2, 3, 4) 

calculating damage:
* requests in form set:<set> pokemon:<user> move:<move> @ set:<set> pokemon:<target> 
* create user with stats based on its set and target from its set
* use damage formula
