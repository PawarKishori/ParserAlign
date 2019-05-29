import pandas as pd
import glob
import re

def cc_resolve():
    path = input ("Enter file name: ")                  #path of parent folder like upto GeoE01_tmp
    path1 = path+'/*/hindi_dep_parser_original.dat'
    files = sorted(glob.glob(path1))
    log = path+'/cc_log-hindi.dat'
    f = open(log, "w+")
    for name in files:
        res = re.split(r'/', name)
        f_name = res[-2]
        path_des = path+'/'+f_name+'/cc_resolved_hindi.dat'
        df = pd.read_csv(name , sep='\t', names = ['Word','1','POS','2','3','PARENT','REL','4','5'])
        n = df.shape[0]
        flag = 0
        for i in range(n):
            if df.iloc[i]['Word']=="yA" or df.iloc[i]['Word']=="aWavA" or df.iloc[i]['Word']=="Ora" or df.iloc[i]['Word']=="waWA":
                str1 = f_name+'\t'+str(i+1)+'\t'+df.iloc[i]['Word']+'\n'
                f.write(str1)
                flag = 1
                conj = df.iloc[i]['Word']
                parent = df.iloc[i]['PARENT']
                g_parent = df.iloc[parent-1]['PARENT']
                parent_rel = df.iloc[i]['REL']
                g_parent_rel = df.iloc[parent-1]['REL']
                df.at[i+1, 'PARENT'] = g_parent
                df.at[i+1, 'REL'] = g_parent_rel
                df.at[parent, 'PARENT'] = i+1
                if conj=='Ora':
                	rel='conjunction'
                else:
                	rel='disjunction'
                df.at[parent, 'REL'] = rel
                for j in range(n):
                    if df.iloc[j]['PARENT']==parent:
                        df.at[j+1,'PARENT']=i+1
                        df.at[j+1,'REL']=rel
        if flag==1:             
            df.to_csv(path_des, sep = '\t',header=False)
            f.write('\n')
    f.close()

    path1 = path+'/*/E_conll_parse'
    files = sorted(glob.glob(path1))
    log = path+'/cc_log-eng.dat'
    f = open(log, "w+")
    for name in files:
        res = re.split(r'/', name)
        f_name = res[-2]
        path_des = path+'/'+f_name+'/cc_resolved_eng.dat'
        df = pd.read_csv(name , sep='\t', names = ['Word','Root','POS','2','3','PARENT','REL','4','5'])
        n = df.shape[0]
        flag = 0
        for i in range(n):
            if df.iloc[i]['Root']=="and" or df.iloc[i]['Root']=="but" or df.iloc[i]['Root']=="or":
                str1 = f_name+'\t'+str(i+1)+'\t'+df.iloc[i]['Word']+'\n'
                f.write(str1)
                flag = 1
                conj = df.iloc[i]['Word']
                parent = df.iloc[i]['PARENT']
                g_parent = df.iloc[parent-1]['PARENT']
                parent_rel = df.iloc[i]['REL']
                g_parent_rel = df.iloc[parent-1]['REL']
                df.at[i+1, 'PARENT'] = g_parent
                df.at[i+1, 'REL'] = g_parent_rel
                df.at[parent, 'PARENT'] = i+1
                if conj=='or':
                    rel='disjunction'
                else:
                    rel='conjunction'
                df.at[parent, 'REL'] = rel
                for j in range(n):
                    if df.iloc[j]['PARENT']==parent:
                        df.at[j+1,'PARENT']=i+1
                        df.at[j+1,'REL']=rel
        if flag==1:             
            df.to_csv(path_des, sep = '\t',header=False)
            f.write('\n')
    f.close()

def main():
    cc_resolve() 

main()       