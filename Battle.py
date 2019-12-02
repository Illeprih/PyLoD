import Edit_Memory
import config


def get_offset(static_addresses):
    disc_offset = {1: 0xD80, 2: 0x0, 3: 0x1458, 4: 0x1B0}
    char_offset = {1: 0x180, 2: -0x180, 3: 0x420, 4: 0x540, 5: 0x180, 6: 0x350, 7: 0x2F0, 8: -0x180}
    if Edit_Memory.read_address(static_addresses.party_count) == 3:
        party_offset = char_offset[Edit_Memory.read_address(static_addresses.character_slot[1])] \
                       + char_offset[Edit_Memory.read_address(static_addresses.character_slot[2])]
    else:
        party_offset = 0
    return disc_offset[Edit_Memory.read_address(static_addresses.disc)] - party_offset


class Battle:
    def __init__(self, static_addresses):
        self.encounter_ID = Edit_Memory.read_address(static_addresses.encounter_ID)
        self.m_point = Edit_Memory.read_address(static_addresses.m_point) + static_addresses.m_calc
        self.c_point = Edit_Memory.read_address(static_addresses.c_point) + static_addresses.c_calc
        self.monster_count = Edit_Memory.read_address(static_addresses.monster_count)
        self.monster_ID_list = []
        for monster in range(self.monster_count):
            address = list(static_addresses.monster_list[monster])
            address[0] += get_offset(static_addresses)
            self.monster_ID_list.append(Edit_Memory.read_address(address))
        self.monster_unique_ID_list = []
        for monster in range(len(list(set(self.monster_ID_list)))):
            self.monster_unique_ID_list.append(Edit_Memory.read_address(static_addresses.unique_slot[monster]))
        self.monster_list = []
        for monster in range(self.monster_count):
            self.monster_list.append(self.MonsterAddress(self.m_point, monster))

    class MonsterAddress:
        def __init__(self, m_point, monster):
            self.hp = m_point - monster * 0x388, 2
            self.max_hp = m_point + 0x8 - monster * 0x388, 2
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
            self.stat_res = m_point + 0x1C - monster * 0x388, 1
            self.death_res = m_point + 0x0C - monster * 0x388, 1
            self.unique_index = m_point + 0x264 - monster * 0x388, 1

        def read_stat(self, stat):
            return Edit_Memory.read_address(getattr(self, stat))

        def read_drop(self, drop):
            return Edit_Memory.read_address(getattr(config.static_address, drop)
                                            [Edit_Memory .read_address(self.unique_index)])

        def write_stat(self, stat, value):
            Edit_Memory.write_address(getattr(self, stat), value)

