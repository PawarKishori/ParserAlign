import pandas as pd
import glob
import re
from collections import Counter as counter

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
		flag_overall = 0
		for i in range(n):
			flag = 0
			if df.iloc[i]['Word']=="yA" or df.iloc[i]['Word']=="aWavA" or df.iloc[i]['Word']=="Ora" or df.iloc[i]['Word']=="waWA":
				str1 = f_name+'\t'+str(i+1)+'\t'+df.iloc[i]['Word']+'\n'
				conj = df.iloc[i]['Word']
				parent = df.iloc[i]['PARENT']
				for j in range(n):
					if df.iloc[j]['PARENT']==parent and df.iloc[j]['REL']=='conj' and i!=j:
						flag = 1
						flag_overall = 1
						break
				if flag == 0:
					for j in range(n):
						if df.index[j] == parent and df.iloc[j]['REL'] == 'conj':
							flag = 2
							flag_overall = 1
							break		
				if flag==1:
					parent_rel = df.iloc[i]['REL']
					g_parent = df.iloc[parent-1]['PARENT']
					g_parent_rel = df.iloc[parent-1]['REL']
					df.at[i+1, 'PARENT'] = g_parent
					df.at[i+1, 'REL'] = g_parent_rel
					df.at[parent, 'PARENT'] = i+1
					if conj=='Ora':
						rel='conjunction'
					else:
						rel='disjunction'
					df.at[parent, 'REL'] = rel
					for k in range(n):
						if df.iloc[k]['PARENT'] == parent and df.iloc[k]['REL'] == 'conj':
							df.at[k+1,'PARENT']=i+1
							df.at[k+1,'REL']=rel
				if flag==2:
					g_parent_rel = df.iloc[parent-1]['REL']
					g_parent = df.iloc[parent-1]['PARENT']
					g_g_parent = df.iloc[g_parent-1]['PARENT']
					g_g_relation = df.iloc[g_parent-1]['REL']
					df.at[i+1, 'PARENT'] = g_g_parent
					df.at[i+1, 'REL'] = g_g_relation
					df.at[g_parent, 'PARENT'] = i+1
					if conj=='Ora':
						rel='conjunction'
					else:
						rel='disjunction'
					df.at[g_parent, 'REL'] = rel
					for k in range(n):
						if df.iloc[k]['PARENT'] == g_parent and df.iloc[k]['REL'] == 'conj':
							df.at[k+1, 'PARENT'] = i+1
							df.at[k+1, 'REL'] = rel
		if flag_overall==1:
			df.to_csv(path_des, sep = '\t',header=False)
			f.write(f_name+'\n')
	f.close()

	# path1 = path+'/*/E_conll_parse'
	# files = sorted(glob.glob(path1))
	# log = path+'/cc_log-eng.dat'
	# f = open(log, "w+")
	# for name in files:
	# 	res = re.split(r'/', name)
	# 	f_name = res[-2]
	# 	path_des = path+'/'+f_name+'/cc_resolved_eng.dat'
	# 	df = pd.read_csv(name , sep='\t', names = ['Word','ROOT','POS','2','3','PARENT','REL','4','5'])
	# 	a= len(counter(df.index).keys())
	# 	n = df.shape[0]
	# 	if a==n:
	# 		flag_overall = 0
	# 		for i in range(n):
	# 			flag = 0
	# 			if df.iloc[i]['ROOT']=="and" or df.iloc[i]['ROOT']=="but" or df.iloc[i]['ROOT']=="or":
	# 				str1 = f_name+'\t'+str(i+1)+'\t'+df.iloc[i]['Word']+'\n'
	# 				conj = df.iloc[i]['ROOT']
	# 				parent = df.iloc[i]['PARENT']
	# 				for j in range(n):
	# 					if df.iloc[j]['PARENT']==parent and df.iloc[j]['REL']=='conj' and i!=j:
	# 						flag = 1
	# 						flag_overall = 1
	# 						break
	# 				if flag==1:
	# 					parent_rel = df.iloc[i]['REL']
	# 					g_parent = df.iloc[parent-1]['PARENT']
	# 					g_parent_rel = df.iloc[parent-1]['REL']
	# 					df.at[i+1, 'PARENT'] = g_parent
	# 					df.at[i+1, 'REL'] = g_parent_rel
	# 					df.at[parent, 'PARENT'] = i+1
	# 					if conj=='or':
	# 						rel='disjunction'
	# 					else:
	# 						rel='conjunction'
	# 					df.at[parent, 'REL'] = rel
	# 					for k in range(n):
	# 						if df.iloc[j]['PARENT']==parent and df.iloc[k]['REL'] == 'conj':
	# 							df.at[j+1,'PARENT']=i+1
	# 							df.at[j+1,'REL']=rel
	# 		if flag_overall==1:
	# 			df.to_csv(path_des, sep = '\t',header=False)
	# 			f.write(f_name+'\n')
	# 	else:
	# 		print("more than 1 tree in"+f_name)
	# f.close()

def main():
	cc_resolve()
main()	