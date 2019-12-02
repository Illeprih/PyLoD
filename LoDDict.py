import csv
import config


class LoDDict:
    def __init__(self):
        self.num2element = {0: 'None', 1: 'Water', 2: 'Earth', 4: 'Dark', 8: 'Non-Elemental', 16: 'Thunder',
                            32: 'Light', 64: 'Wind', 128: 'Fire'}
        self.element2num = {'None': 0, 'Water': 1, 'Earth': 2, 'Dark': 4, 'Non-Elemental': 8, 'Thunder': 16,
                            'Light': 32, 'Wind': 64, 'Fire': 128}
        self.num2item = {}
        self.item2num = {}
        with open(config.cwd + "/Mods/" + config.options.mod + "/Item_List.txt", 'r') as file:  # Creates two dictionaries for items
            i = 0                                                            # one with IDs as key and names as text
            for line in file:                                                # and vice-versa
                self.num2item[i] = line[:-1]
                self.item2num[line[:-1]] = i
                i += 1
        self.stat_list = {}
        del line
        with open(config.cwd + "/Mods/" + config.options.mod + "/Monster_Data.csv", 'r') as file: # Creates a dictionary
            reader = csv.reader(file, delimiter=',', quotechar='"')             # stat_list[monster ID] with name
            i = 0                                                               # and stats as attributes for every ID
            for row in reader:
                if i > 0:
                    self.stat_list[int(row[0])] = self.StatList(row[1:], self.element2num, self.item2num)
                i += 1
        self.dragoon_list = {}
        with open(config.cwd + "/Mods/" + config.options.mod + "/Dragoon_Stats.csv", 'r') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                if i > 0:
                    self.dragoon_list[i-1] = {1: self.DragoonList(row[1:5]), 2: self.DragoonList(row[5:9]),
                                              3: self.DragoonList(row[9:13]), 4: self.DragoonList(row[13:17]),
                                              5: self.DragoonList(row[17:21])}
                i += 1
            del row
        del file

    class DragoonList:
        def __init__(self, stat_list):
            self.D_AT = int(stat_list[0])
            self.D_DF = int(stat_list[1])
            self.D_MAT = int(stat_list[2])
            self.D_MDF = int(stat_list[3])

    class StatList:
        def __init__(self, stat_list, element2num, item2num):
            self.name = stat_list[0]
            self.element = element2num[stat_list[1]]
            self.max_hp = int(stat_list[2])
            self.atk = int(stat_list[3])
            self.mat = int(stat_list[4])
            self.df = int(stat_list[5])
            self.mdf = int(stat_list[6])
            self.spd = int(stat_list[7])
            self.a_av = int(stat_list[8])
            self.m_av = int(stat_list[9])
            self.p_immune = int(stat_list[10])
            self.m_immune = int(stat_list[11])
            self.p_half = int(stat_list[12])
            self.m_half = int(stat_list[13])
            self.e_immune = element2num[stat_list[14]]
            self.e_half = element2num[stat_list[15]]
            self.stat_res = int(stat_list[16])
            self.death_res = int(stat_list[17])
            self.exp = int(stat_list[18])
            self.gold = int(stat_list[19])
            self.drop_item = item2num[stat_list[20]]
            self.drop_chance = int(stat_list[21])


