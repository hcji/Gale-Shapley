# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 09:00:30 2019

@author: jihon
"""

import random
import pandas as pd


def create_sample(man_num, women_num, diaosi = True):
    #设置男女生喜好样本
    if diaosi:
        women_num += 1
        man = pd.DataFrame( [['w'+str(i) for i in random.sample(range(1,women_num+1),women_num)] \
                              for i in range(man_num+1)],
                            index = ['m'+str(i) for i in range(1,man_num+2)],
                            columns = ['level'+str(i) for i in range(1,women_num+1)]
                            )
    else:
        man = pd.DataFrame( [['w'+str(i) for i in random.sample(range(1,women_num+1),women_num)] \
                              for i in range(man_num)],
                            index = ['m'+str(i) for i in range(1,man_num+1)],
                            columns = ['level'+str(i) for i in range(1,women_num+1)]
                            )

    women = pd.DataFrame( [['m'+str(i) for i in random.sample(range(1,man_num+1),man_num)] \
                          for i in range(women_num)],
                        index = ['w'+str(i) for i in range(1,women_num+1)],
                        columns = ['level'+str(i) for i in range(1,man_num+1)]
                        )
    if diaosi:
        women['level'+str(man_num+1)] = 'm'+str(man_num+1)
        
    return (man, women)


def create_mapping_table(man,women):
    man_ismapping = pd.DataFrame({
            'man_id':man.index,
            'target':'n',
            'love_level':0,
            'range':0
            }).set_index('man_id')
    women_ismapping = pd.DataFrame({
            'women_id':women.index,
            'target':'n',
            'love_level':0,
            'range':0
            }).set_index('women_id')
    return (man_ismapping, women_ismapping)


def calc_standard(man, women, man_ismapping, women_ismapping):
    level_num = 0
    print('==============================开始模拟求婚过程==============================')
    while man_ismapping['love_level'].min() == 0:
        level_num += 1
        print('==============================开始第{}天婚姻配对=============================='.format(level_num))
        u_mapping_man = man_ismapping[man_ismapping.target == 'n'].index.tolist()
        if level_num < 2:
            level_col = 'level' + str(level_num)
            man_choose = man[man.index.isin(u_mapping_man)][level_col].to_frame().reset_index()
            man_choose.columns = ['man_id', 'women_id']
            man_choose['range'] = 1
        else:
            m_id = u_mapping_man
            l = []
            for man_id in m_id:
                col_n = int(man_ismapping[man_ismapping.index == man_id].range[0])
                level_col = 'level' + str(col_n + 1)
                women_id = man[man.index == man_id][level_col][0]
                rg = col_n + 1
                l.append([man_id, women_id, rg])
            man_choose = pd.DataFrame(l, columns=['man_id', 'women_id', 'range'])
                
        for r in range(0, len(man_choose)):
            relationship = man_choose[man_choose.index == r]
            m = [i for i in relationship['man_id']][0]
            w = [i for i in relationship['women_id']][0]
            find = women[women.index == w].unstack().reset_index()
            find.columns = ['level', 'women_id', 'man_id']
            find = int([i for i in find[find['man_id'] == m]['level']][0].split('level')[1])
            o_love_level = [i for i in women_ismapping[women_ismapping.index == w]['love_level']][0]
            rg = [i for i in relationship['range']][0]
            if o_love_level == 0:
                women_ismapping.loc[w, 'love_level'] = find
                women_ismapping.loc[w, 'target'] = m
                women_ismapping.loc[w, 'range'] = level_num
                man_ismapping.loc[m, 'love_level'] = rg
                man_ismapping.loc[m, 'target'] = w
                man_ismapping.loc[m, 'range'] = rg
            elif o_love_level > find:
                m_o = women_ismapping.loc[w, 'target']
                man_ismapping.loc[m_o, 'love_level'] = 0
                man_ismapping.loc[m_o, 'target'] = 'n'
                man_ismapping.loc[m, 'love_level'] = rg
                man_ismapping.loc[m, 'target'] = w
                man_ismapping.loc[m, 'range'] = rg
                women_ismapping.loc[w, 'love_level'] = find
                women_ismapping.loc[w, 'target'] = m
                women_ismapping.loc[w, 'range'] = level_num
            else:
                man_ismapping.loc[m, 'range'] = rg
                pass
    print('==============================婚姻配对完成==============================')
    print('共进行了{}次牵线搭桥，在第{}天举办集体婚礼。'.format(level_num, level_num + 1))
    return man_ismapping, women_ismapping


if __name__ == '__main__':
    man_num = 100
    women_num = 100
    man, women = create_sample(man_num, women_num)
    man_ismapping, women_ismapping = create_mapping_table(man, women)
    result = calc_standard(man, women, man_ismapping, women_ismapping)