from Edit_Memory import *
import psutil
import time
import os
from LoDDict import *


def get_pid():
    process_name = "ePSXe.exe"
    for process in psutil.process_iter():
        if process.name() == process_name:
            return process.pid


def get_offset():
    party_count = read_address(pid, static_addresses.party_count)
    disc_offset = {1: 0xD80, 2: 0x0, 3: 0x1458, 4: 0x1B0}
    char_offset = {1: 0x180, 2: -0x180, 3: 0x420, 4: 0x540, 5: 0x180, 6: 0x350, 7: 0x2F0, 8: -0x180}
    if party_count == 3:
        slot2 = read_address(pid, static_addresses.character_slot[1])
        slot3 = read_address(pid, static_addresses.character_slot[2])
        print(slot2)
        print(slot3)
        party_offset = char_offset[slot2] + char_offset[slot3]
    else:
        party_offset = 0

    return disc_offset[read_address(pid, static_addresses.disc)] - party_offset


class Battle:
    def __init__(self):
        self.encounter_ID = read_address(pid, static_addresses.encounter_ID)
        self.m_point = read_address(pid, static_addresses.m_point) + static_addresses.m_calc
        self.c_point = read_address(pid, static_addresses.c_point) + static_addresses.c_calc
        print(hex(self.c_point))
        self.monster_count = read_address(pid, static_addresses.monster_count)
        self.monster_ID_list = []
        for monster in range(self.monster_count):
            address = list(static_addresses.monster_list[monster])
            address[0] += get_offset()
            self.monster_ID_list.append(read_address(pid, address))
        self.monster_unique_ID_list = []
        for monster in range(len(list(set(self.monster_ID_list)))):
            self.monster_unique_ID_list.append(read_address(pid, static_addresses.unique_slot[monster]))
        self.monster_addresses = []
        for monster in range(self.monster_count):
            self.monster_addresses.append(MonsterAddress(self.m_point, monster))

    def write(self):
        if options.monster_change == 1:
            i = 0
            for monster in self.monster_ID_list:
                write_address(pid, battle.monster_addresses[i].HP, dictionary.stat_list[monster].max_HP)
                write_address(pid, battle.monster_addresses[i].Max_HP, dictionary.stat_list[monster].max_HP)
                write_address(pid, battle.monster_addresses[i].element, dictionary.stat_list[monster].element)
                write_address(pid, battle.monster_addresses[i].display_element,
                              dictionary.stat_list[monster].element)
                write_address(pid, battle.monster_addresses[i].atk, dictionary.stat_list[monster].ATK)
                write_address(pid, battle.monster_addresses[i].og_atk, dictionary.stat_list[monster].ATK)
                write_address(pid, battle.monster_addresses[i].mat, dictionary.stat_list[monster].MAT)
                write_address(pid, battle.monster_addresses[i].og_mat, dictionary.stat_list[monster].MAT)
                write_address(pid, battle.monster_addresses[i].df, dictionary.stat_list[monster].DF)
                write_address(pid, battle.monster_addresses[i].og_df, dictionary.stat_list[monster].DF)
                write_address(pid, battle.monster_addresses[i].mdf, dictionary.stat_list[monster].MDF)
                write_address(pid, battle.monster_addresses[i].og_mdf, dictionary.stat_list[monster].MDF)
                write_address(pid, battle.monster_addresses[i].spd, dictionary.stat_list[monster].SPD)
                write_address(pid, battle.monster_addresses[i].og_spd, dictionary.stat_list[monster].SPD)
                write_address(pid, battle.monster_addresses[i].a_av, dictionary.stat_list[monster].A_AV)
                write_address(pid, battle.monster_addresses[i].m_av, dictionary.stat_list[monster].M_AV)
                write_address(pid, battle.monster_addresses[i].p_immune, dictionary.stat_list[monster].P_Immune)
                write_address(pid, battle.monster_addresses[i].m_immune, dictionary.stat_list[monster].M_Immune)
                write_address(pid, battle.monster_addresses[i].p_half, dictionary.stat_list[monster].P_Half)
                write_address(pid, battle.monster_addresses[i].m_half, dictionary.stat_list[monster].M_Half)
                write_address(pid, battle.monster_addresses[i].e_immune, dictionary.stat_list[monster].E_Immune)
                write_address(pid, battle.monster_addresses[i].e_half, dictionary.stat_list[monster].E_Half)
                write_address(pid, battle.monster_addresses[i].status_res,
                              dictionary.stat_list[monster].Status_Resist)
                write_address(pid, battle.monster_addresses[i].death_res,
                              dictionary.stat_list[monster].Death_Resist)
                i += 1
        if options.drop_change == 1:
            i = 0
            for monster in self.monster_unique_ID_list:
                write_address(pid, static_addresses.exp[i], dictionary.stat_list[monster].EXP)
                write_address(pid, static_addresses.gold[i], dictionary.stat_list[monster].Gold)
                write_address(pid, static_addresses.item_drop[i], dictionary.stat_list[monster].Drop_Item)
                write_address(pid, static_addresses.drop_chance[i], dictionary.stat_list[monster].Drop_Chance)
                i += 1

    def read(self):
        monster_list = []
        for monster in range(len(self.monster_ID_list)):
            monster_list.append(Monster(monster))

        while read_address(pid, static_addresses.encounter_value) == 41215:
            print('\n\n\n')
            for monster in range(self.monster_count):
                monster_list[monster].read(monster)
                print('{}\t\tElement: {}\t\tHP: {}\t\tMax HP: {}\t\tATK: {}\t\tMAT: {}\t\tDEF: {}\t\tMDEF: {}'
                      '\t\tA-AV: {} \t\tM-AV: {}\t\tSpeed: {}\t\tTurn: {}\t\tItem Drop: {}\t\tDrop Chance: {}%'.format
                      (dictionary.stat_list[self.monster_ID_list[monster]].name,
                       dictionary.num2element[monster_list[monster].element], monster_list[monster].HP,
                       monster_list[monster].Max_HP, monster_list[monster].atk, monster_list[monster].mat,
                       monster_list[monster].df, monster_list[monster].mdf, monster_list[monster].a_av,
                       monster_list[monster].m_av, monster_list[monster].spd, monster_list[monster].turn,
                       dictionary.num2item[monster_list[monster].item_drop], monster_list[monster].drop_chance))
                print('P_Immune: {}\t\t M_Immune: {}\t\t P_Half: {}\t\t M_Half: {}\t\tE_Immune: {}\t\t E_Half: {}'
                      '\t\tStatus Resist: {}\t\tDeath Resist: {}\t\tExp: {}\t\tGold: {}'
                      .format(monster_list[monster].p_immune, monster_list[monster].m_immune,
                              monster_list[monster].p_half, monster_list[monster].m_half,
                              monster_list[monster].e_immune, monster_list[monster].e_half,
                              monster_list[monster].status_res, monster_list[monster].death_res,
                              monster_list[monster].exp, monster_list[monster].gold))

            time.sleep(1)


class Monster:
    def __init__(self, monster):
        self.unique_index = read_address(pid, battle.monster_addresses[monster].unique_index)
        self.item_drop = read_address(pid, static_addresses.item_drop[self.unique_index])
        self.exp = read_address(pid, static_addresses.exp[self.unique_index])
        self.gold = read_address(pid, static_addresses.gold[self.unique_index])
        self.drop_chance = read_address(pid, static_addresses.drop_chance[self.unique_index])
        self.element = read_address(pid, battle.monster_addresses[monster].element)
        self.HP = read_address(pid, battle.monster_addresses[monster].HP)
        self.Max_HP = read_address(pid, battle.monster_addresses[monster].Max_HP)
        self.atk = read_address(pid, battle.monster_addresses[monster].atk)
        self.mat = read_address(pid, battle.monster_addresses[monster].mat)
        self.df = read_address(pid, battle.monster_addresses[monster].df)
        self.mdf = read_address(pid, battle.monster_addresses[monster].mdf)
        self.a_av = read_address(pid, battle.monster_addresses[monster].a_av)
        self.m_av = read_address(pid, battle.monster_addresses[monster].m_av)
        self.spd = read_address(pid, battle.monster_addresses[monster].spd)
        self.turn = read_address(pid, battle.monster_addresses[monster].turn)
        self.p_immune = read_address(pid, battle.monster_addresses[monster].p_immune)
        self.m_immune = read_address(pid, battle.monster_addresses[monster].m_immune)
        self.p_half = read_address(pid, battle.monster_addresses[monster].p_half)
        self.m_half = read_address(pid, battle.monster_addresses[monster].m_half)
        self.e_immune = read_address(pid, battle.monster_addresses[monster].e_immune)
        self.e_half = read_address(pid, battle.monster_addresses[monster].e_half)
        self.status_res = read_address(pid, battle.monster_addresses[monster].status_res)
        self.death_res = read_address(pid, battle.monster_addresses[monster].death_res)

    def read(self, monster):
        self.element = read_address(pid, battle.monster_addresses[monster].element)
        self.HP = read_address(pid, battle.monster_addresses[monster].HP)
        self.Max_HP = read_address(pid, battle.monster_addresses[monster].Max_HP)
        self.atk = read_address(pid, battle.monster_addresses[monster].atk)
        self.mat = read_address(pid, battle.monster_addresses[monster].mat)
        self.df = read_address(pid, battle.monster_addresses[monster].df)
        self.mdf = read_address(pid, battle.monster_addresses[monster].mdf)
        self.a_av = read_address(pid, battle.monster_addresses[monster].a_av)
        self.m_av = read_address(pid, battle.monster_addresses[monster].m_av)
        self.spd = read_address(pid, battle.monster_addresses[monster].spd)
        self.turn = read_address(pid, battle.monster_addresses[monster].turn)
        self.p_immune = read_address(pid, battle.monster_addresses[monster].p_immune)
        self.m_immune = read_address(pid, battle.monster_addresses[monster].m_immune)
        self.p_half = read_address(pid, battle.monster_addresses[monster].p_half)
        self.m_half = read_address(pid, battle.monster_addresses[monster].m_half)
        self.e_immune = read_address(pid, battle.monster_addresses[monster].e_immune)
        self.e_half = read_address(pid, battle.monster_addresses[monster].e_half)
        self.status_res = read_address(pid, battle.monster_addresses[monster].status_res)
        self.death_res = read_address(pid, battle.monster_addresses[monster].death_res)


class MonsterAddress:
    def __init__(self, m_point, monster):
        self.HP = m_point - monster * 0x388, 2
        self.Max_HP = m_point + 0x8 - monster * 0x388, 2
        self.element = m_point + 0x6a - monster * 0x388, 1
        self.display_element = m_point + 0x14 - monster * 0x388, 1
        self.atk = m_point + 0x2c - monster * 0x388, 2
        self.og_atk = m_point + 0x58 - monster * 0x388, 2
        self.mat = m_point + 0x2E - monster * 0x388, 2
        self.og_mat = m_point + 0x5A - monster * 0x388, 2
        self.df = m_point + 0x30 - monster * 0x388, 2
        self.og_df = m_point + 0x5E - monster * 0x388, 2
        self.mdf = m_point + 0x32 - monster * 0x388, 2
        self.og_mdf = m_point + 0x60 - monster * 0x388, 2
        self.spd = m_point + 0x2A - monster * 0x388, 2
        self.turn = m_point + 0x44 - monster * 0x388, 2
        self.og_spd = m_point + 0x5C - monster * 0x388, 2
        self.a_av = m_point + 0x38 - monster * 0x388, 1
        self.m_av = m_point + 0x3A - monster * 0x388, 1
        self.p_immune = m_point + 0x10 - monster * 0x388, 1
        self.m_immune = m_point + 0x10 - monster * 0x388, 1
        self.p_half = m_point + 0x10 - monster * 0x388, 1
        self.m_half = m_point + 0x10 - monster * 0x388, 1
        self.e_immune = m_point + 0x1A - monster * 0x388, 1
        self.e_half = m_point + 0x18 - monster * 0x388, 1
        self.status_res = m_point + 0x1C - monster * 0x388, 1
        self.death_res = m_point + 0x0C - monster * 0x388, 1
        self.unique_index = m_point + 0x264 - monster * 0x388, 1


class Options:
    def __init__(self):
        self.mod = 'Base'
        self.monster_change = 1
        self.drop_change = 1
        self.emulator = 'ePSXe 2.0.5'


cwd = os.getcwd()
pid = get_pid()
options = Options()
dictionary = LoDDict(cwd, options.mod)
static_addresses = StaticAddresses(options.emulator)

while True:
    while read_address(pid, static_addresses.encounter_value) != 41215:
        time.sleep(1)
    time.sleep(1)
    battle = Battle()
    battle.write()
    battle.read()
