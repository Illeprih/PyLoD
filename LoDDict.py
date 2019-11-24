import csv


class LoDDict:
    def __init__(self, cwd, folder):
        self.num2element = {0: 'None', 1: 'Water', 2: 'Earth', 4: 'Dark', 8: 'Non-Elemental', 16: 'Thunder',
                            32: 'Light', 64: 'Wind', 128: 'Fire'}
        self.element2num = {'None': 0, 'Water': 1, 'Earth': 2, 'Dark': 4, 'Non-Elemental': 8, 'Thunder': 16,
                            'Light': 32, 'Wind': 64, 'Fire': 128}
        self.num2item = {}
        self.item2num = {}
        with open(cwd + "/Mods/" + folder + "/Item_List.txt", 'r') as file:
            i = 0
            for line in file:
                self.num2item[i] = line[:-1]
                self.item2num[line[:-1]] = i
                i += 1
        self.stat_list = {}
        del line
        with open(cwd + "/Mods/" + folder + "/Monster_Data.csv", 'r') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                if i > 0:
                    self.stat_list[int(row[0])] = self.StatList(row[1:], self.element2num, self.item2num)
                i += 1
        self.dragoon_list = {}
        with open(cwd + "/Mods/" + folder + "/Dragoon_Stats.csv", 'r') as file:
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
            self.DAT = int(stat_list[0])
            self.DDEF = int(stat_list[1])
            self.DMAT = int(stat_list[2])
            self.DMDEF = int(stat_list[3])

    class StatList:
        def __init__(self, stat_list, element2num, item2num):
            self.name = stat_list[0]
            self.element = element2num[stat_list[1]]
            self.max_HP = int(stat_list[2])
            self.ATK = int(stat_list[3])
            self.MAT = int(stat_list[4])
            self.DF = int(stat_list[5])
            self.MDF = int(stat_list[6])
            self.SPD = int(stat_list[7])
            self.A_AV = int(stat_list[8])
            self.M_AV = int(stat_list[9])
            self.P_Immune = int(stat_list[10])
            self.M_Immune = int(stat_list[11])
            self.P_Half = int(stat_list[12])
            self.M_Half = int(stat_list[13])
            self.E_Immune = int(stat_list[14])
            self.E_Half = int(stat_list[15])
            self.Status_Resist = int(stat_list[16])
            self.Death_Resist = int(stat_list[17])
            self.EXP = int(stat_list[18])
            self.Gold = int(stat_list[19])
            self.Drop_Item = item2num[stat_list[20]]
            self.Drop_Chance = int(stat_list[21])


class StaticAddresses:
    emulator_dict = {'ePSXe 1.9': 0xA579A0, 'ePSXe 2.0.5': 0x15F2020}
    emulator_m_dict = {'ePSXe 1.9': -0x7F5B42C4, 'ePSXe 2.0.5': 0x17963BC}
    emulator_c_dict = {'ePSXe 1.9': -0x7F5A8558, 'ePSXe 2.0.5': -0x7EA0DED8}
    encounter_value = [0xC6AE8, 2]
    encounter_ID = [0xBB0F8, 2]
    m_point = [0xC66FC, 4]
    c_point = [0xBC1D8, 4]
    monster_list = [[0x1CF910, 2], [0x1CF918, 2], [0x1CF920, 2], [0x1CF928, 2], [0x1CF930, 2]]
    disc = [0xBC058, 1]
    party_count = [0xC6760, 1]
    monster_count = [0xC6768, 1]
    character_slot = [[0xBAC50, 1], [0xBAC54, 1], [0xBAC58, 1]]
    unique_slot = [[0x5E53A, 2], [0x5E6E2, 2], [0x5E88A, 2]]
    item_drop = [[0x5E531, 1], [0x5E6D9, 1], [0x5E881, 1]]
    drop_chance = [[0x5E530, 1], [0x5E6D8, 1], [0x5E880, 1]]
    exp = [[0x5E52C, 2], [0x5E6D4, 2], [0x5E87C, 2]]
    gold = [[0x5E52E, 2], [0x5E6D6, 2], [0x5E87E, 2]]

    def __init__(self, emulator):
        self.emulator_offset = self.emulator_dict[emulator]
        self.m_calc = self.emulator_m_dict[emulator]
        self.c_calc = self.emulator_c_dict[emulator]
        self.encounter_value[0] = self.encounter_value[0] + self.emulator_offset
        self.encounter_ID[0] = self.encounter_ID[0] + self.emulator_offset
        self.m_point[0] = self.m_point[0] + self.emulator_offset
        self.c_point[0] = self.c_point[0] + self.emulator_offset
        for address in range(len(self.monster_list)):
            self.monster_list[address][0] = self.monster_list[address][0] + self.emulator_offset
        self.disc[0] = self.disc[0] + self.emulator_offset
        self.party_count[0] = self.party_count[0] + self.emulator_offset
        self.monster_count[0] = self.monster_count[0] + self.emulator_offset
        for address in range(len(self.character_slot)):
            self.character_slot[address][0] = self.character_slot[address][0] + self.emulator_offset
        for address in range(len(self.unique_slot)):
            self.unique_slot[address][0] = self.unique_slot[address][0] + self.emulator_offset
        for address in range(len(self.item_drop)):
            self.item_drop[address][0] = self.item_drop[address][0] + self.emulator_offset
        for address in range(len(self.drop_chance)):
            self.drop_chance[address][0] = self.drop_chance[address][0] + self.emulator_offset
        for address in range(len(self.exp)):
            self.exp[address][0] = self.exp[address][0] + self.emulator_offset
        for address in range(len(self.gold)):
            self.gold[address][0] = self.gold[address][0] + self.emulator_offset

