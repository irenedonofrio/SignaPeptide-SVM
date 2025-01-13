import numpy as np
import pandas as pd
import sklearn
#! conda install biopython -y
from Bio.SeqUtils.ProtParam import ProteinAnalysis


def feature_extraction(df, K, global_comp=False, hp=False, hp_global= False, charge=False, h_tendency=False, transmem_tendency = False,glob_transmem_tendency=False):
    '''This function accepts a dataframe containing protein sequences as input. Depending on the specified boolean variables, 
     it extracts relevant features from the data, preparing them for use as input for a Support Vector Machine (SVM).'''
  
    features_lst = list()
    label_lst = list()

    # Define feature names based on the hp parameter
    base_feature_names = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    feature_names = base_feature_names
    if global_comp:
        feature_names += ['Arem', 'Crem', 'Drem', 'Erem', 'Frem', 'Grem', 'Hrem', 'Irem', 'Krem', 'Lrem', 'Mrem', 'Nrem', 'Prem', 'Qrem', 'Rrem', 'Srem', 'Trem', 'Vrem', 'Wrem', 'Yrem']
    if hp:
        feature_names += ['max_hp', 'pos_max_hp', 'avg_hp']
    if hp_global:
        feature_names += ['global_avg_hp']
    if charge:
        feature_names += ['max_charge', 'pos_max_charge', 'av_charge']
    if h_tendency:
        feature_names += ['max_hten', 'pos_max_hten', 'av_hten']
    if transmem_tendency:
        feature_names += ['max_transmem_ten', 'pos_max_transmem_ten', 'av_transmem_ten']
    if glob_transmem_tendency:
        feature_names += ['glob_max_transmem_ten', 'glob_pos_max_transmem_ten', 'glob_av_transmem_ten']

    for item,row in df.iterrows():   
        if pd.isnull(row['Signal peptide']):
            label_lst.append(0)
        else:
            label_lst.append(1)
        #sequence padding to include the edges in the hp calcululus, the number of X to add is (w-1)//2
        window = 7
        padding = (window -1)/2 
        window_ch = 5
        padding_ch = (window_ch -1)/2 
        window_tm = 19
        padding_tm = (window_tm -1)/2 
        
        s = ProteinAnalysis('X'*int(padding)+row['Sequence'][0:int(K)]+'X'*int(padding))
        res_fr = s.get_amino_acids_percent()
        features_vector = np.array(list(res_fr.values()))

        if global_comp or hp or hp_global or charge or h_tendency or transmem_tendency or glob_transmem_tendency:
            additional_values = []

            if global_comp:
                s_rem = ProteinAnalysis('X'*int(padding)+row['Sequence'][int(K):]+'X'*int(padding))
                rem_res_fr = s_rem.get_amino_acids_percent() 
                additional_values.extend(list(rem_res_fr.values()))

            if hp:
                #hydrophobicty profile of the first K residues (add the X to the kd scal to avoid the warnings)
                
                kd = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
                "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
                "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
                "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2,'X':0,'Z':0}
                hp = s.protein_scale(kd, window,1)
                m = np.max(hp)
                m_scaled = ((m-(-4.5))/(4.5-(-4.5))) * (1 - 0) + 0 #scaling (MinMax)
                m_index = hp.index(m)
                m_position = m_index/int(K)
                av = sum(hp)/len(hp)
                av_scaled = ((av-(-4.5))/(4.5-(-4.5))) * (1 - 0) + 0  #scaling (MinMax)
                additional_values.extend([m_scaled, m_position, av_scaled])
            
            if hp_global:
                kd = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
                "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
                "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
                "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2,'X':0,'Z':0}
                s_glob = ProteinAnalysis('X'*int(padding)+row['Sequence']+'X'*int(padding))
                hp_glob = s_glob.protein_scale(kd,26,1)
                av_glob = sum(hp_glob)/len(hp_glob)
                av_glob_scaled = ((av_glob-(-4.5))/(4.5-(-4.5))) * (1 - 0) + 0  #scaling (MinMax)
                additional_values.extend([av_glob_scaled])
                
            if charge:
                ch_scale = {"A": 0, "R": 1, "N": 0, "D": 0, "C": 0,
            "Q": 0, "E": 0, "G": 0, "H": 1, "I": 0,
            "L": 0, "K": 1, "M": 0, "F": 0, "P": 0,
            "S": 0, "T": 0, "W": 0, "Y": 0, "V": 0,'X':0,'Z':0, 'U':0} 
                s_ch = ProteinAnalysis('X'*int(padding_ch)+row['Sequence'][0:int(K)]+'X'*int(padding_ch))
                ch = s_ch.protein_scale(ch_scale, window_ch,1)
                m_ch = np.max(ch)
                m_ch_index = ch.index(m_ch)
                m_ch_position = m_ch_index/int(K)
                av_ch = sum(ch)/len(ch)
                #charge_features = np.array([m_ch,m_ch_position,av_ch])
                additional_values.extend([m_ch,m_ch_position,av_ch])

            if h_tendency:
                cf_h = {"A":1.42, "R":0.98, "N":0.67, "D":1.01, "C": 0.70, "Q":1.11, "E":1.51, "G":0.57, "H":1.00, "I":1.08,
                        "L":1.21, "K":1.16, "M":1.45, "F":1.13, "P":0.57, "S":0.77, "T":0.83, "W":1.08, "Y":0.69, "V":1.06,'X':0,'Z':0,'U':0}
                
                h_ten = s.protein_scale(cf_h,window)
                m_hten = np.max(h_ten)
                m_hten_scaled = ((m_hten-(0.57))/(1.51-(0.57))) * (1 - 0) + 0 #scaling (MinMax)
                m_hten_index = h_ten.index(m_hten)
                m_hten_position = m_hten_index/int(K)
                av_hten = sum(h_ten)/len(h_ten)
                av_hten_scaled = ((av_hten-(0.57))/(1.51-(0.57))) * (1 - 0) + 0 #scaling (MinMax)
                additional_values.extend([m_hten_scaled,m_hten_position,av_hten_scaled])

            if transmem_tendency:
                transmem =  {"A": 0.38,"R": -2.57,"N": -1.62,"D": -3.27,"C": -0.3,"Q": -1.84,"E": -2.9,"G": -0.19,"H": -1.44,"I": 1.97,"L": 1.82,"K": -3.46,"M": 1.4,"F": 1.98,"P": -1.44,"S": -0.53,"T": -0.32,"W": 1.53,"Y": 0.49,"V": 1.46,'Z':0,'U':0,'X':0}
                s_tm = ProteinAnalysis('X'*int(padding_tm)+row['Sequence'][int(K):]+'X'*int(padding_tm))
                transmem_ten = s_tm.protein_scale(transmem,window_tm)
                m_transmem_ten = np.max(transmem_ten)
                m_transmem_ten_scaled = ((m_transmem_ten-(-3.46))/(1.98-(-3.46))) * (1 - 0) + 0 #scaling (MinMax)
                m_transmem_ten_index = transmem_ten.index(m_transmem_ten)
                m_transmem_ten_position =m_transmem_ten_index/int(K)
                av_transmem_ten = sum(transmem_ten)/len(transmem_ten)
                av_transmem_ten_scaled = ((av_transmem_ten-(-3.46))/(1.98-(-3.46))) * (1 - 0) + 0 #scaling (MinMax)
                additional_values.extend([m_transmem_ten_scaled,m_transmem_ten_position,av_transmem_ten_scaled])

            if glob_transmem_tendency:
                s_rem = ProteinAnalysis('X'*int(padding)+row['Sequence'][int(K):]+'X'*int(padding))
                transmem =  {"A": 0.38,"R": -2.57,"N": -1.62,"D": -3.27,"C": -0.3,"Q": -1.84,"E": -2.9,"G": -0.19,"H": -1.44,"I": 1.97,"L": 1.82,"K": -3.46,"M": 1.4,"F": 1.98,"P": -1.44,"S": -0.53,"T": -0.32,"W": 1.53,"Y": 0.49,"V": 1.46,'Z':0,'U':0,'X':0}
                glob_transmem_ten = s_rem.protein_scale(transmem,window)
                glob_m_transmem_ten = np.max(glob_transmem_ten)
                glob_m_transmem_ten_scaled = ((glob_m_transmem_ten-(-3.46))/(1.98-(-3.46))) * (1 - 0) + 0 #scaling (MinMax)
                glob_m_transmem_ten_index = glob_transmem_ten.index(glob_m_transmem_ten)
                glob_m_transmem_ten_position =glob_m_transmem_ten_index/int(K)
                glob_av_transmem_ten = sum(glob_transmem_ten)/len(glob_transmem_ten)
                glob_av_transmem_ten_scaled = ((glob_av_transmem_ten-(-3.46))/(1.98-(-3.46))) * (1 - 0) + 0 #scaling (MinMax)
                additional_values.extend([glob_m_transmem_ten_scaled,glob_m_transmem_ten_position,glob_av_transmem_ten_scaled])



            
            features_vector = np.hstack((features_vector, additional_values))
                
        features_lst.append(features_vector)
    
    #features_set = np.vstack(features_lst)
    features_set = np.array(features_lst)
    features_set = np.vstack((feature_names, features_set))
    return(features_set,label_lst)   