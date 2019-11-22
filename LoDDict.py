import csv


class LoDDict:
    def __init__(self, cwd, folder):
        self.num2element = {1: 'Water', 2: 'Earth', 4: 'Dark', 8: 'Non-Elemental', 16: 'Thunder', 32: 'Light',
                            64: 'Wind', 128: 'Fire'}
        self.element2num = {'Water': 1, 'Earth': 2, 'Dark': 4, 'Non-Elemental': 8, 'Thunder': 16, 'Wind': 32,
                            'Light': 64, 'Fire': 128}
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
            del row
        del file

    class StatList:
        def __init__(self, stat_list, element2num, item2num):
            self.name = stat_list[0]
            self.max_HP = int(stat_list[1])
            self.element = element2num[stat_list[2]]
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
        encounter_value = [0xB1E488, 2]
        encounter_ID = [0xB12A98, 2]
        m_point = [0xB1E09C, 4]
        c_point = [0xB13B78, 4]
        monster_list = [[0xC272B0, 2], [0xC272B8, 2], [0xC272C0, 2], [0xC272C8, 2], [0xC272D0, 2]]
        disc = [0xB139F8, 1]
        party_count = [0xB1E100, 1]
        monster_count = [0xB1E108, 1]
        character_slot = [[0xB125F0, 1], [0xB125F4, 1], [0xB125F8, 1]]
        unique_slot = [[0xAB5EDA, 2], [0xAB6082, 2], [0xAB622A, 2]]
        item_drop = [[0xAB5ED1, 1], [0xAB6079, 1], [0xAB6221, 1]]
        drop_chance = [[0xAB5ED0, 1], [0xAB6078, 1], [0xAB6220, 1]]
        exp = [[0xAB5ECC, 2], [0xAB6074, 2], [0xAB621C, 2]]
        gold = [[0xAB5ECE, 2], [0xAB6076, 2], [0xAB621E, 2]]
        emulator_offset = 0

        def __init__(self, emulator_offset):
            self.encounter_value[0] = self.encounter_value[0] + emulator_offset
            self.encounter_ID[0] = self.encounter_ID[0] + emulator_offset
            self.m_point[0] = self.m_point[0] + emulator_offset
            self.c_point[0] = self.c_point[0] + emulator_offset
            self.monster_list = [[0xC272B0, 2], [0xC272B8, 2], [0xC272C0, 2], [0xC272C8, 2], [0xC272D0, 2]]
            self.disc[0] = self.disc[0] + emulator_offset
            self.party_count[0] = self.party_count[0] + emulator_offset
            self.monster_count[0] = self.monster_count[0] + emulator_offset
            self.character_slot = [[0xB125F0, 1], [0xB125F4, 1], [0xB125F8, 1]]
            self.unique_slot = [[0xAB5EDA, 2], [0xAB6082, 2], [0xAB622A, 2]]
            self.item_drop = [[0xAB5ED1, 1], [0xAB6079, 1], [0xAB6221, 1]]
            self.drop_chance = [[0xAB5ED0, 1], [0xAB6078, 1], [0xAB6220, 1]]
            self.exp = [[0xAB5ECC, 2], [0xAB6074, 2], [0xAB621C, 2]]
            self.gold = [[0xAB5ECE, 2], [0xAB6076, 2], [0xAB621E, 2]]


class StaticAddresses:
    encounter_value = [0xB1E488, 2]
    encounter_ID = [0xB12A98, 2]
    m_point = [0xB1E09C, 4]
    c_point = [0xB13B78, 4]
    monster_list = [[0xC272B0, 2], [0xC272B8, 2], [0xC272C0, 2], [0xC272C8, 2], [0xC272D0, 2]]
    disc = [0xB139F8, 1]
    party_count = [0xB1E100, 1]
    monster_count = [0xB1E108, 1]
    character_slot = [[0xB125F0, 1], [0xB125F4, 1], [0xB125F8, 1]]
    unique_slot = [[0xAB5EDA, 2], [0xAB6082, 2], [0xAB622A, 2]]
    item_drop = [[0xAB5ED1, 1], [0xAB6079, 1], [0xAB6221, 1]]
    drop_chance = [[0xAB5ED0, 1], [0xAB6078, 1], [0xAB6220, 1]]
    exp = [[0xAB5ECC, 2], [0xAB6074, 2], [0xAB621C, 2]]
    gold = [[0xAB5ECE, 2], [0xAB6076, 2], [0xAB621E, 2]]

    def __init__(self, emulator_offset):
        self.encounter_value[0] = self.encounter_value[0] + emulator_offset
        self.encounter_ID[0] = self.encounter_ID[0] + emulator_offset
        self.m_point[0] = self.m_point[0] + emulator_offset
        self.c_point[0] = self.c_point[0] + emulator_offset
        for address in range(len(self.monster_list)):
            self.monster_list[address][0] = self.monster_list[address][0] + emulator_offset
        self.disc[0] = self.disc[0] + emulator_offset
        self.party_count[0] = self.party_count[0] + emulator_offset
        self.monster_count[0] = self.monster_count[0] + emulator_offset
        for address in range(len(self.character_slot)):
            self.character_slot[address][0] = self.character_slot[address][0] + emulator_offset
        for address in range(len(self.unique_slot)):
            self.unique_slot[address][0] = self.unique_slot[address][0] + emulator_offset
        for address in range(len(self.item_drop)):
            self.item_drop[address][0] = self.item_drop[address][0] + emulator_offset
        for address in range(len(self.drop_chance)):
            self.drop_chance[address][0] = self.drop_chance[address][0] + emulator_offset
        for address in range(len(self.exp)):
            self.exp[address][0] = self.exp[address][0] + emulator_offset
        for address in range(len(self.gold)):
            self.gold[address][0] = self.gold[address][0] + emulator_offset

