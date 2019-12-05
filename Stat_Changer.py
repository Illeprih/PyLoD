import psutil
import time
import os
import config
import Edit_Memory
import Battle
import LoDDict
import Static_Address
import GUI
import threading


def get_pid():
    process_name = "ePSXe.exe"
    for process in psutil.process_iter():
        if process.name() == process_name:
            return process.pid

def run():
    while True:
        while Edit_Memory.read_address(config.static_address.encounter_value) != 41215:
            print(Edit_Memory.read_address([0xb1e488, 2]))
            time.sleep(1)
        time.sleep(1)
        config.battle = Battle.Battle(config.static_address)
        if config.options.monster_change:
            i = 0
            for monster in config.battle.monster_list:
                monster.write_stat("hp", config.dictionary.stat_list[config.battle.monster_ID_list[i]].max_hp)
                monster.write_stat("max_hp", config.dictionary.stat_list[config.battle.monster_ID_list[i]].max_hp)
                monster.write_stat("atk", config.dictionary.stat_list[config.battle.monster_ID_list[i]].atk)
                monster.write_stat("og_atk", config.dictionary.stat_list[config.battle.monster_ID_list[i]].atk)
                monster.write_stat("mat", config.dictionary.stat_list[config.battle.monster_ID_list[i]].mat)
                monster.write_stat("og_mat", config.dictionary.stat_list[config.battle.monster_ID_list[i]].mat)
                monster.write_stat("df", config.dictionary.stat_list[config.battle.monster_ID_list[i]].df)
                monster.write_stat("og_df", config.dictionary.stat_list[config.battle.monster_ID_list[i]].df)
                monster.write_stat("mdf", config.dictionary.stat_list[config.battle.monster_ID_list[i]].mdf)
                monster.write_stat("og_mdf", config.dictionary.stat_list[config.battle.monster_ID_list[i]].mdf)
                monster.write_stat("spd", config.dictionary.stat_list[config.battle.monster_ID_list[i]].spd)
                monster.write_stat("og_spd", config.dictionary.stat_list[config.battle.monster_ID_list[i]].spd)
                monster.write_stat("a_av", config.dictionary.stat_list[config.battle.monster_ID_list[i]].a_av)
                monster.write_stat("m_av", config.dictionary.stat_list[config.battle.monster_ID_list[i]].m_av)
                monster.write_stat("p_immune", config.dictionary.stat_list[config.battle.monster_ID_list[i]].p_immune)
                monster.write_stat("m_immune", config.dictionary.stat_list[config.battle.monster_ID_list[i]].m_immune)
                monster.write_stat("p_half", config.dictionary.stat_list[config.battle.monster_ID_list[i]].p_half)
                monster.write_stat("m_half", config.dictionary.stat_list[config.battle.monster_ID_list[i]].m_half)
                monster.write_stat("e_immune", config.dictionary.stat_list[config.battle.monster_ID_list[i]].e_immune)
                monster.write_stat("e_half", config.dictionary.stat_list[config.battle.monster_ID_list[i]].e_half)
                monster.write_stat("stat_res", config.dictionary.stat_list[config.battle.monster_ID_list[i]].stat_res)
                monster.write_stat("death_res", config.dictionary.stat_list[config.battle.monster_ID_list[i]].death_res)
                i += 1
        if config.options.drop_change:
            if config.options.drop_change_defined:
                i = 0
                for monster in config.battle.monster_unique_ID_list:
                    Edit_Memory.write_address(config.static_address.exp[i], config.dictionary.stat_list[monster].exp)
                    Edit_Memory.write_address(config.static_address.gold[i], config.dictionary.stat_list[monster].gold)
                    Edit_Memory.write_address(config.static_address.item_drop[i], config.dictionary.stat_list[monster]
                                              .drop_item)
                    Edit_Memory.write_address(config.static_address.drop_chance[i], config.dictionary.stat_list[monster]
                                              .drop_chance)
                    i += 1
            else:
                i = 0
                for monster in config.battle.monster_unique_ID_list:
                    if monster in [325, 301, 287, 266, 300]:  # Drake, Gehrich, Greham, Kongol II, Mapi II
                        Edit_Memory.write_address(config.static_address.drop_chance[i], 100)
                    i += 1

        while Edit_Memory.read_address(config.static_address.encounter_value) == 41215:
            for monster in range(len(config.battle.monster_list)):
                print('{}\t\tElement: {}\t\tHP: {}\t\tMax HP: {}\t\tATK: {}\t\tMAT: {}\t\tDEF: {}\t\tMDF: {}'
                      '\t\tA-AV: {} \t\tM-AV: {}\t\tSpeed: {}\t\tTurn: {}'
                      '\nEXP: {}\t\tGold: {}\t\tItem Drop: {}\t\tDrop Chance: {}%'
                      .format(config.dictionary.stat_list[config.battle.monster_ID_list[monster]].name,
                              config.dictionary.num2element[config.battle.monster_list[monster].read_stat("element")],
                              config.battle.monster_list[monster].read_stat("hp"),
                              config.battle.monster_list[monster].read_stat("max_hp"),
                              config.battle.monster_list[monster].read_stat("atk"),
                              config.battle.monster_list[monster].read_stat("mat"),
                              config.battle.monster_list[monster].read_stat("df"),
                              config.battle.monster_list[monster].read_stat("mdf"),
                              config.battle.monster_list[monster].read_stat("a_av"),
                              config.battle.monster_list[monster].read_stat("m_av"),
                              config.battle.monster_list[monster].read_stat("spd"),
                              config.battle.monster_list[monster].read_stat("turn"),
                              config.battle.monster_list[monster].read_drop("exp"),
                              config.battle.monster_list[monster].read_drop("gold"),
                              config.dictionary.num2item[config.battle.monster_list[monster].read_drop("item_drop")],
                              config.battle.monster_list[monster].read_drop("drop_chance")))
            print('\n\n\n\n\n')
            time.sleep(1)


class Options:
    def __init__(self):
        self.mod = 'Base'
        self.monster_change = True
        self.drop_change = True
        self.drop_change_defined = True
        self.dragoon_change = True
        self.emulator = 'ePSXe 1.9'


config.cwd = os.getcwd()
config.pid = get_pid()
config.options = Options()
config.dictionary = LoDDict.LoDDict()
config.static_address = Static_Address.StaticAddresses()


gui = threading.Thread(target=GUI.start)
script = threading.Thread(target=run, daemon=True)
script.start()
gui.start()

