import config


class StaticAddresses:
    emulator_dict = {'ePSXe 1.9': 0xA579A0, 'ePSXe 2.0.5': 0x16C2020}
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

    def __init__(self):
        self.emulator_offset = self.emulator_dict[config.options.emulator]
        self.m_calc = self.emulator_m_dict[config.options.emulator]
        self.c_calc = self.emulator_c_dict[config.options.emulator]
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

