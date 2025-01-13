import pandas as pd


######################################################################################################################
def get_model_results(df,model_name):
    df2 = pd.DataFrame(columns=['model','best C','best \u03B3','best K','ACC','MCC','precision','recall','F1-score'])
    results = []
    for item,row in df.iterrows():
        best_c = list((df['best C'].mode()))
        if len(best_c) > 1:
            best_c = min(best_c)
        else:
            best_c= best_c[0]
        best_gamma =  list((df['best \u03B3'].mode()))
        if len(best_gamma) > 1:
            if 'scale' in best_gamma:
                best_gamma = 'scale'
            else:
                best_gamma = min(best_gamma)
        else:
            best_gamma = best_gamma[0]
        best_K = list((df['best K'].mode()))
        if len(best_K) > 1:
            diff_lst = []
            for k in best_K:
                diff = abs(int(k)-23)
                diff_lst.append(diff)
            best_K = best_K[diff_lst.index(min(diff_lst))]
        else:
            best_K = best_K[0]
        ACC_mean = df['ACC test'].mean()
        ACC_se = df['ACC test'].sem()
        MCC_mean = df['MCC test'].mean()
        MCC_se = df['MCC test'].sem()
        precision_mean = df['precision'].mean()
        precision_se = df['precision'].sem()
        recall_mean = df['recall'].mean()
        recall_se = df['recall'].sem()
        f1_mean = df['F1-score'].mean()
        f1_se = df['F1-score'].sem()
    
    results.append({'model':model_name,'best C':best_c,'best \u03B3':best_gamma,'best K':best_K,'ACC':f"{ACC_mean:.{2}f} ± {ACC_se:.{2}f}",'MCC':f"{MCC_mean:.{2}f} ± {MCC_se:.{2}f}",'precision':f"{precision_mean:.{2}f} ± {precision_se:.{2}f}",'recall':f"{recall_mean:.{2}f} ± {recall_se:.{2}f}",'F1-score':f"{f1_mean:.{2}f} ± {f1_se:.{2}f}"})
    df2 = pd.concat([df2,pd.DataFrame(results)],ignore_index=True)
    return df2
    
    
    

