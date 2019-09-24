# # Library Imports


import logging
import random
import math
import copy
from collections import Counter

# Data Prep Libraries
import datetime as dt
import pandas as pd
import numpy as np

# GA Imports and Settings
import pyevolve
from pyevolve import G1DList, GSimpleGA, Selectors, Statistics, Crossovers, Util,Initializators, Mutators, Consts, DBAdapters, GAllele



pyevolve.logEnable()


from future.builtins import range
from random import randint as rand_randint, choice as rand_choice
from random import random as rand_random

#### Calling UDFs for GA

from GA_functions import *




# coding: utf-8

# 

# In[1]:



# The code tries to optimise work allocation in any operations business where we have conflicting paramters such as
# 1. TAT
# 2. Availablity of an Agent
# 3. Skillset of an Agent
# 4. Work Item specific constraints 

# In this use case, we try to optimize the following constraints 
# "age"  : How long a work item has been pending
# "skill_requirement"  The type of skill required to complete this task -- SOme type of code
# "TAT_breach_IND"  : Has the TAT been breached or not
# 'High_priority_int' : Is is a high priority job or not 
# "TAT_breach1_ind" : Will we TAT get breached in 1 day 
# "TAT_breach2_ind" : WIll the TAT get breached in 2 days 


############### Initialize number of generations, populations and objective_run_id

gen_var=200
pop_var=100
objective_of_run="Case2_2018_1800_45mins"+"Gen"+str(gen_var)+"POP"+str(pop_var)


# In[2]:


# System Imports


# In[3]:


agent_data = pd.read_csv("agent_base_table.csv")

agent = agent_data[["id","id_wb","score"]]
agent.columns = ['agent_id', 'skill_number', 'overall_scoring']




agent_dict = recur_dictify(agent)


# In[4]:


agent_data.head()

agent_avail = agent_data[["id","AVAILABILITY_new"]].drop_duplicates()
agent_avail["AVAILABILITY_new"] = agent_avail["AVAILABILITY_new"].astype(int)
agent_avail = recur_dictify(agent_avail)

gd_req_data = pd.read_csv("table_work_item_Unassigned.csv")
gd_req_data.head()

#wb_mapping = pd.read_csv("wb_mapping.csv")
#gd_req_data = pd.merge(gd_req_data, wb_mapping,  how='left' , left_on='OWNER', right_on='WorkBasket')

gd_req = gd_req_data[["REQ_REF_NBR","PR_AGE","id_wb","TAT_breach",'same_day','TAT_breach_1day', 'TAT_breach_2day']]
gd_req.columns = ["work_item","age","skill_requirement","TAT_breach_IND",'High_priority_int',"TAT_breach1_ind","TAT_breach2_ind"]


grouped = agent.groupby("skill_number")
skill_matrix = grouped.agent_id.apply(lambda x: pd.Series(data=x.values)).unstack()
skill_matrix["a"] = 0
skill_matrix = skill_matrix.fillna(0)

iris_assignemnt_csv = pd.read_csv("R2_iris_output_9may.csv")
iris_assignemnt=iris_assignemnt_csv["Employee_ID"].values.tolist()


# # Data Prep

# In[5]:


# temp_list_1 is a list with DLA_IDs repeated the same number of times as is the availability
temp_list_1 = list()

for i in agent_avail:
    for j in range(agent_avail[i]):
        temp_list_1.append(i)

for i in range(len(gd_req)):
    temp_list_1.append(0)

    
    
    
# temp_list_2 is a list of list that represent the possible values each work_item can take
temp_list_2=list()

for i in np.array(gd_req["skill_requirement"]):
    # You can even add an object to the list
    try:
        b = [int(x) for x in list(skill_matrix.loc[i].unique())]
    except:
        b=[0]
    temp_list_2.append(b)


temp = pd.DataFrame({'work_item':list(gd_req['work_item']),'ind':list(gd_req.index)})

temp_grouped = temp.groupby("work_item")
ind_markings = temp_grouped.ind.apply(lambda x: pd.Series(data=x.values)).unstack()



# 
temp_list_3 = list()

for i in range(len(ind_markings)):
    temp_list_3.append([int(x) for x in ind_markings.iloc[i,:].unique()[~np.isnan(ind_markings.iloc[i,:].unique())]])
    
agent_asign_list = list()


# In[6]:


#initialiser_global=0
sample_list=[0]*len(iris_assignemnt)



# In[ ]:


import time
time.ctime()
import re
time_label=re.sub(r'[^0-9]',"_",str(dt.datetime.now()))+"_Case2"
time_label


# In[ ]:


Start = dt.datetime.now()
S = dt.datetime.now()

genome = G1DList.G1DList(len(gd_req))

setOfAlleles = GAllele.GAlleles()
for i in np.array(gd_req["skill_requirement"]):
   # You can even add an object to the list
   try:
       b = skill_matrix.loc[i].unique()
   except:
       b=[0]
   a = GAllele.GAlleleList(b)
   setOfAlleles.add(a)

genome.setParams(allele=setOfAlleles)


genome.mutator.set(mutator_allel_final)
#genome.initializator.set(Initializators.G1DListInitializatorAllele)
genome.initializator.set(initializator_final_temp)
genome.crossover.set(crossover_uniform_final_all)
# The evaluator function (objective function)
genome.evaluator.set(obj_test_all)
#ga.setElitism(True)
# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRankSelector)
ga.stepCallback.set(callback_agent_count)
#ga.stepCallback.set(initiator_callback_final)
timeold=dt.datetime.now()
ga.setGenerations(gen_var)
ga.setMinimax(Consts.minimaxType["minimize"])
ga.setPopulationSize(pop_var)
#ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
ga.terminationCriteria.set(convergence1)
ga.setMultiProcessing(True,False,48)
#ga.setElitism(True)
#ga.evolve(freq_stats=1)
ga.elitism=True

## Gen time taken


# Do the evolution, with stats dump
# frequency of 10 generations
time.ctime()
sqlite_adapter = DBAdapters.DBSQLite(identify="gen_10_pop_"+time_label, resetDB=True, resetIdentify=True, frequency=1, commit_freq = 1)
#sqlite_adapter.setStatsGenFreq(1)
ga.setDBAdapter(sqlite_adapter) 
ga.evolve(1)
pd.DataFrame(Gen_time_taken).to_excel('Gen_time_taken'+time_label+'.xlsx')

##ga.evolve(freq_stats=1)

###%run pyevolve_graph.py -i gen_10_pop_500_02_03_2018_16_00_overnight1_initial -1 -o graph_gen_10_pop_500_02_03_2018_16_00_overnight_initial -e pdf

#sqlite_adapter.open(ga)
#sqlite_adapter.insert(ga)
#sqlite_adapter.commitAndClose() 

End = dt.datetime.now()
ga.bestIndividual()

out = ga.bestIndividual()
assign_list = []
for i in range(len(out)):
    assign_list.append(out[i])

#pd.DataFrame(assign_list).to_excel('final_test_5.xlsx')
"""
gen.append(t)
time_taken.append(End-Start)
score.append(ga.bestIndividual().getRawScore())
"""


# In[ ]:


### MAtrix genration for comparison between iris and GA


# In[12]:


############ This thr final allocation of work items after the process achieves global maxima

ga_assignment=pd.Series(ga.bestIndividual().genomeList)

base_table_comparison=gd_req_data.copy()


base_table_comparison["GA_assignment"]=ga_assignment

