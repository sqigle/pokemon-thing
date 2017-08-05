import sqlite3

stat_names = ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']
default_ivs = {stat: 31 for stat in stat_names}

class Pokemon():
    def __init__(self, name, item, ability, evs, nature, moves, ivs):
        self.name = name
        self.item = item
        self.ability = ability
        self.evs = evs
        self.nature = nature
        if ivs == None:
            self.ivs = default_ivs
        else:
            self.ivs = ivs
        self.moves = moves
        if self.is_valid():
            pass
        else:
            pass

    def print_self(self):
        print('name:',self.name)
        print('item:', self.item)
        print('ability:',self.ability)
        print('evs:',self.evs)
        print('nature:',self.nature)
        print('ivs:',self.ivs)
        print('moves:',self.moves)

    def search_self(self):
        name = self.name
        conn = sqlite3.connect('resources/pokemon.db')
        with conn:
            c = conn.cursor()
            c.execute('SELECT * FROM Pokemon WHERE Name=?', (name,))
            rows = c.fetchall()
        if rows == []:
            print('{0} is not a pokemon'.format(name))
            return None
        return rows

    def can_learn(self,move):
        name = self.name
        data = self.search_self()
        try:
            dex_no = data[0][0]
        except TypeError:
            return None
        lookup_term = move.replace(' ', '').lower()
        learnset = open('resources/learnsets/{0}.csv'.format(dex_no),'r')
        with learnset:
            for line in learnset:
                if lookup_term in line:
                    return True
                else:
                    print('{0} cannot learn {1}'.format(name, move))
                    return False

    def check_ability(self):
        name = self.name
        ability = self.ability
        data = self.search_self()
        if ability in data[0]:
            return True
        else:
            print('{0} cannot have the ability {1}'.format(name, ability))

    def verify_ev_total(self):
        evs = self.evs
        if sum(evs.values()) > 508:
            print('ev total exceeds 508')
            return False
        else:
            return True

    def check_ivs(self):
        ivs = self.ivs
        i = 0
        for key in ivs.keys():
            if ivs[key] > 31:
                print('{0} iv exceeds 31'.format(key))
                i += 1
        return i <= 0

    def is_valid(self):
        try:
            checks = [self.check_ability, self.check_ivs, self.verify_ev_total]
            passed = [False, False, False]
            for check in checks:
                i = checks.index(check)
                if check():
                    passed[i] = True
            moves = self.moves
            move_checks = [self.can_learn(move) for move in moves]
            passed += move_checks
            return False not in passed
        except TypeError:
            return False

    def evs_ivs_tuple(self, vals):
        lst = 6 * [0]
        for stat in stat_names:
            i = stat_names.index(stat)
            if stat in vals.keys():
                lst[i] = vals[stat]
        if vals == self.ivs:
            for stat in stat_names:
                i = stat_names.index(stat)
                if stat not in vals.keys():
                    lst[i] = 31
        return tuple(lst)
