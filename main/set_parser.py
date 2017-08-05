import re
import sqlite3
import pokemon as poke

def get_name(line):
    """
    first line is in the form
    `nickname (name) (gender) @ item`
    nickname and gender may or may not be in it
    """
    regex = r'[\w\s-]+(?=\))'
    p = re.compile(regex)
    search = p.search(line)
    if search == None:
        at = line.find(' @')
        return line[:at]
    if search.group() in ['M','F']:
        paren = line.find(' (')
        return line[:paren]
    start = search.start()
    end = search.end()
    return line[start:end]

def get_item(line):
    stripped = line.strip()
    p = re.compile(r'@ ')
    search = p.search(stripped)
    start = search.end()
    return stripped[start:]

def get_ability(line):
    stripped = line.strip()
    p = re.compile(r'Ability: ')
    search = p.search(line)
    start = search.end()
    return stripped[start:]

def get_evs_ivs(line):
    """
    ev/iv lines are in the form
    `{E/I}Vs: x1 Stat / ... / xn Stat`
    """
    line = line[5:].strip() # drop 'EVs: ' at the beginning
    spl = line.split(' / ')
    num = re.compile(r'\d+')
    vals = [int(num.match(s).group()) for s in spl]
    string = re.compile(r'\D+')
    stats = [string.search(s).group().strip() for s in spl]
    out = {stat: val for stat, val in zip(stats,vals)}
    return out

def get_nature(line):
    end = line.find(' Nature')
    return line[:end]

def get_move(line):
    """
    - move
    """
    line = line[2:].strip()
    return line

def parse_set(set_):
    lines = (set_.strip()).split('\n')
    name = get_name(lines[0])
    item = get_item(lines[0])
    ability = get_ability(lines[1])
    evs = get_evs_ivs(lines[2])
    nature = get_nature(lines[3])
    i = 4
    try:
        ivs = get_evs_ivs(lines[4])
        i = 5
    except AttributeError:
        ivs = None
    moves = [get_move(lines[n]) for n in range(i, len(lines))]
    pkmn = poke.Pokemon(name, item, ability, evs, nature, moves, ivs)
    return pkmn

def save_set(pkmn):
    conn = sqlite3.connect('resources/sets.db')
    set_name = input('name of set: ')
    evs = pkmn.evs_ivs_tuple(pkmn.evs)
    ivs = pkmn.evs_ivs_tuple(pkmn.ivs)
    moves = pkmn.moves
    with conn:
        c = conn.cursor()
        c.execute('DROP TABLE Sets')
        c.execute('CREATE TABLE IF NOT EXISTS Sets(Pokemon text, Name UNIQUE text, Item text, Ability text, Nature text, EVs text, IVs text, Move1 text, Move2 text, Move3 text, Move4 text)')
        c.execute('INSERT INTO Sets Values(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT IGNORE', (pkmn.name, set_name, pkmn.item, pkmn.ability, pkmn.nature, str(evs), str(ivs)) + tuple(move for move in moves))

def retrieve_set(set_name, pkmn_name):
    conn = sqlite3.connect('resources/sets.db')
    with conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Sets WHERE Pokemon=? AND Name=?', (pkmn_name, set_name))
        row = c.fetchall()
    if row == []:
        print('{0} has no set named {1}'.format(pkmn_name, set_name))
        return None
    else:
        """
        species, set name, item, ability, nature, evs, ivs, moves
        """
        data = row[0]
        item = data[2]
        ability = data[3]
        nature = data[4]
        evs = data[5].replace('(','').replace(')','').split(', ')
        evs = {stat: int(ev) for stat, ev in zip(poke.stat_names, evs)}
        ivs = data[6].replace('(','').replace(')','').split(', ')
        ivs = {stat: int(iv) for stat, iv in zip(poke.stat_names, ivs)}
        moves = [data[i] for i in range(7,len(data))]
        return poke.Pokemon(pkmn_name, item, ability, evs, nature, moves, ivs)

def read_paste():
    print('paste your set:')
    lines = ''
    for i in range(9):
        lines+=input()+"\n"
    print()
    return lines
