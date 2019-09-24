def initializator_final_temp(genome,**args):
    if (len(iris_assignemnt.copy())-len(sample_list))<2:
        del sample_list[-1]
        genome.setInternalList(iris_assignemnt.copy())
        del sample_list[-1]
    else:
        import random
        list_1_1 = copy.deepcopy(temp_list_1)
        list_2_1 = copy.deepcopy(temp_list_2)
        list_3_1 = copy.deepcopy(temp_list_3)
        temp_genome = [0]*len(gd_req)

        b=list(range(len(list_3_1)))
        random.shuffle(b)

        for k in b:
            x = random.choice(list_3_1[k])
            a = random.choice(list_2_1[x])
            temp_genome[x] = a
            list_1_1.remove(a)
            if a not in list_1_1:
                for j in range(len(list_2_1)):
                    try:
                        list_2_1[j].remove(a)
                    except:
                        alpha = 0
        del(list_1_1,list_2_1,list_3_1)
        genome.setInternalList(temp_genome)

        
    
from pyevolve import Util
from random import randint as rand_randint
	
    

    
def mutator_allel_final(genome, **args):
    """ The mutator of G1DList, Allele Mutator
    
    To use this mutator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.
    
    """
    #list_1 = copy.deepcopy(temp_list_1)
    #list_2 = copy.deepcopy(temp_list_2)
    #list_3 = copy.deepcopy(temp_list_3)
    
    
    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * listSize
    
    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the G1DListMutatorAllele, you must specify the 'allele' parameter", TypeError)
    
    mutate_ind = list()
    which_gene = list()
    
    if mutations < 1.0:
        list_1 = copy.deepcopy(temp_list_1)
        list_2 = copy.deepcopy(temp_list_2)
        list_3 = copy.deepcopy(temp_list_3)
        mutations = 0
        for i in range(len(list_3)):
            if Util.randomFlipCoin(args["pmut"]):
                mutate_ind.append('True')
            else:
                mutate_ind.append('False')
        
        for i in range(len(mutate_ind)):
            if mutate_ind[i]=='False':
                for j in list_3[i]:
                    xyz = genome[j]
                    list_1.remove(xyz)
                    if xyz not in list_1:
                        for k in range(len(list_2)):
                            try:
                                list_2[k].remove(xyz)
                            except:
                                alpha = 0
        
        for i in range(len(mutate_ind)):
            if mutate_ind[i]=='True':
                for j in list_3[i]:
                    genome[j]=0
                x = random.choice(list_3[i])
                new_val = random.choice(list_2[x])
                genome[x] = new_val
                list_1.remove(new_val)
                if new_val not in list_1:
                    for k in range(len(list_2)):
                        try:
                            list_2[k].remove(new_val)
                        except:
                            alpha = 0
                mutations += 1
                        
            
    else:
        list_1 = copy.deepcopy(temp_list_1)
        list_2 = copy.deepcopy(temp_list_2)
        list_3 = copy.deepcopy(temp_list_3)
        
        for it in range(int(round(mutations))):
            which_gene.append(rand_randint(0, len(list_3)-1))
        
        for i in range(len(list_3)):
            if i in which_gene:
                mutate_ind.append('True')
            else:
                mutate_ind.append('False')
            
        for i in range(len(mutate_ind)):
            if mutate_ind[i]=='False':
                for j in list_3[i]:
                    xyz = genome[j]
                    list_1.remove(xyz)
                    if xyz not in list_1:
                        for k in range(len(list_2)):
                            try:
                                list_2[k].remove(xyz)
                            except:
                                alpha = 0
        
        for i in range(len(mutate_ind)):
            if mutate_ind[i]=='True':
                for j in list_3[i]:
                    genome[j]=0
                x = random.choice(list_3[i])
                new_val = random.choice(list_2[x])
                genome[x] = new_val
                list_1.remove(new_val)
                if new_val not in list_1:
                    for k in range(len(list_2)):
                        try:
                            list_2[k].remove(new_val)
                        except:
                            alpha = 0
    del(list_1,list_2,list_3)
    return int(mutations)

    
def initiator_callback_final_test(ga_engine):
    generation = ga.getCurrentGeneration()
    if generation == 1:
        testing_ga=ga.getPopulation()
        print(type(testing_ga))
        print(testing_ga)
        newPop = ga.getPopulation()
        newPop[0].setInternalList(iris_assignemnt)

        # CHANGE THE ENTIRE POPULATION "pop"
        newPop.evaluate()
        newPop.sort()
    return False

def callback_final(ga_engine):
    list_1 = temp_list_1
    l = ga_engine.bestIndividual().genomeList
    z = l.count(0)
    list_1 = list(filter(lambda x: x!=0, list_1))
    
    if z<=min(zero_list):
        for i in range(z):
            list_1.append(0)
    else:
        for i in range(min(zero_list)):
            list_1.append(0)
    zero_list.append(z)
    return False

charlie = list()

Gen_time_taken = list()
#S = dt.datetime.now()

def callback_agent_count(ga_engine):
    global E
    global S
    E = dt.datetime.now()
    Gen_time = (E - S)
    Gen_time_taken.append(Gen_time)
    list_agent = agent_asign_list
    l = ga.bestIndividual().genomeList
    z = len(l) - l.count(0)
    list_agent.append(z)
    #print(z)
    pd.DataFrame(list_agent).to_excel("list_agent_"+time_label+'.xlsx')
    beta = ga.bestIndividual().genomeList
    charlie.append(beta)
    pd.DataFrame(charlie).to_excel('genome_test'+time_label+'.xlsx')
    S = dt.datetime.now()
import datetime as dt

def convergence1(ga):
    timenow=dt.datetime.now()
    temp=str(timenow-timeold).split(":")
    delta=int(temp[0])*60+int(temp[1])
    if delta > 45:
        return True
    else:
        return False   


# In[7]:
 
## Latest crossover function

def crossover_uniform_final_all(genome, **args):
    """ The G1DList Uniform Crossover

    Each gene has a 50% chance of being swapped between mom and dad

    """ 
    list_3_3 = copy.deepcopy(temp_list_3)

    sister = None
    brother = None
    gMom = args["mom"]
    gDad = args["dad"]

    sister = gMom.clone()
    brother = gDad.clone()
    sister.resetStats()
    brother.resetStats()

    temp_brother = copy.deepcopy(brother)
    temp_sister = copy.deepcopy(sister)

    for i in range(len(list_3_3)):
        if Util.randomFlipCoin(Consts.CDefG1DListCrossUniformProb):
            for j in list_3_3[i]:
                temp = temp_sister[j]
                temp_sister[j] = temp_brother[j]
                temp_brother[j] = temp
                
    
    brother_list = list(pd.unique(temp_brother.genomeList))
    brother_list.remove(0)
    
    for i in brother_list:
        if temp_brother.genomeList.count(i)>agent_avail[i]:
            breach_count = temp_brother.genomeList.count(i)-agent_avail[i]
            indexes = [y for y, x in enumerate(temp_brother.genomeList) if x == i]
            agent_loc_ind_list = [0]*len(gd_req)
            TAT_ind_list = [0]*len(gd_req)
            same_day_ind_list = [0]*len(gd_req)
            day_1_compl = [0]*len(gd_req)
            day_2_compl = [0]*len(gd_req)
            for j in indexes:
                agent_loc_ind_list[j]=1
            for j in indexes:
                TAT_ind_list[j] = gd_req['TAT_breach_IND'][j]*17
            for j in indexes:
                same_day_ind_list[j] = gd_req['High_priority_int'][j]*2
            for j in indexes:
                day_1_compl[j] = gd_req['TAT_breach1_ind'][j]*11
            for j in indexes:
            	day_2_compl[j] = gd_req['TAT_breach2_ind'][j]*7   	
            remove_list = [v + w + x + y + z for v, w, x, y, z in zip(agent_loc_ind_list, same_day_ind_list, day_2_compl, day_1_compl, TAT_ind_list)]
            one_count = remove_list.count(1)
            one_index = [y for y, x in enumerate(remove_list) if x == 1]
            three_count = remove_list.count(3)
            three_index = [y for y, x in enumerate(remove_list) if x == 3]
            eight_count = remove_list.count(8)
            eight_index = [y for y, x in enumerate(remove_list) if x == 8]
            twelve_count = remove_list.count(12)
            twelve_index = [y for y, x in enumerate(remove_list) if x == 12]
            ten_count = remove_list.count(10)
            ten_index = [y for y, x in enumerate(remove_list) if x == 10]
            fourteen_count = remove_list.count(14)
            fourteen_index = [y for y, x in enumerate(remove_list) if x == 14]
            eighteen_count = remove_list.count(18)
            eighteen_index = [y for y, x in enumerate(remove_list) if x == 18]            
            twenty_count = remove_list.count(20)
            twenty_index = [y for y, x in enumerate(remove_list) if x == 20]
            if breach_count<=one_count:
                for j in range(breach_count):
                    remove_index = random.choice(one_index)
                    temp_brother[remove_index]=0
                    one_index.remove(remove_index)
            elif one_count<breach_count<=(one_count + three_count):
                for j in one_index:
                    temp_brother[j]=0
                breach_count = breach_count-one_count
                for j in range(breach_count):
                    remove_index = random.choice(three_index)
                    temp_brother[remove_index]=0
                    three_index.remove(remove_index)
            elif (one_count + three_count)<breach_count<=(one_count + three_count + eight_count):
                for j in one_index:
                    temp_brother[j]=0
                for j in three_index:
                    temp_brother[j]=0
                breach_count = breach_count-(one_count+three_count)
                for j in range(breach_count):
                    remove_index = random.choice(eight_index)
                    temp_brother[remove_index]=0
                    eight_index.remove(remove_index)
            elif (one_count + three_count + eight_count)<breach_count<=(one_count + three_count + eight_count + twelve_count):
                for j in one_index:
                    temp_brother[j]=0
                for j in three_index:
                    temp_brother[j]=0
                for j in eight_index:
                    temp_brother[j]=0                    
                breach_count = breach_count-(one_count+three_count+eight_count)
                for j in range(breach_count):
                    remove_index = random.choice(twelve_index)
                    temp_brother[remove_index]=0
                    twelve_index.remove(remove_index)    
            elif (one_count + three_count + eight_count + twelve_count)<breach_count<=(one_count + three_count + eight_count + twelve_count + ten_count):
                for j in one_index:
                    temp_brother[j]=0
                for j in three_index:
                    temp_brother[j]=0
                for j in eight_index:
                    temp_brother[j]=0       
                for j in twelve_index:
                    temp_brother[j]=0                     
                breach_count = breach_count-(one_count+three_count+eight_count+twelve_count)
                for j in range(breach_count):
                    remove_index = random.choice(ten_index)
                    temp_brother[remove_index]=0
                    ten_index.remove(remove_index)
            elif (one_count + three_count + eight_count + twelve_count + ten_count)<breach_count<=(one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count):
                for j in one_index:
                    temp_brother[j]=0
                for j in three_index:
                    temp_brother[j]=0
                for j in eight_index:
                    temp_brother[j]=0       
                for j in twelve_index:
                    temp_brother[j]=0    
                for j in ten_index:
                    temp_brother[j]=0
                breach_count = breach_count-(one_count+three_count+eight_count+twelve_count+ten_count)
                for j in range(breach_count):
                    remove_index = random.choice(fourteen_index)
                    temp_brother[remove_index]=0
                    fourteen_index.remove(remove_index)                    
            elif (one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count)<breach_count<=(one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count + eighteen_count):
                for j in one_index:
                    temp_brother[j]=0
                for j in three_index:
                    temp_brother[j]=0
                for j in eight_index:
                    temp_brother[j]=0       
                for j in twelve_index:
                    temp_brother[j]=0    
                for j in ten_index:
                    temp_brother[j]=0
                for j in fourteen_index:
                    temp_brother[j]=0                    
                breach_count = breach_count-(one_count+three_count+eight_count+twelve_count+ten_count+fourteen_count)
                for j in range(breach_count):
                    remove_index = random.choice(eighteen_index)
                    temp_brother[remove_index]=0
                    eighteen_index.remove(remove_index) 
            elif (one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count + eighteen_count)<breach_count<=(one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count + eighteen_count + twenty_count):
                print("7")
                for j in one_index:
                    temp_brother[j]=0
                for j in three_index:
                    temp_brother[j]=0
                for j in eight_index:
                    temp_brother[j]=0       
                for j in twelve_index:
                    temp_brother[j]=0    
                for j in ten_index:
                    temp_brother[j]=0
                for j in fourteen_index:
                    temp_brother[j]=0 
                for j in eighteen_index:
                    temp_brother[j]=0                 
                breach_count = breach_count-(one_count+three_count+eight_count+twelve_count+ten_count+fourteen_count+eighteen_count)
                print(breach_count)
                for j in range(breach_count):
                    remove_index = rand_choice(twenty_index)
                    temp_brother[remove_index]=0
                    twenty_index.remove(remove_index)                      
                                        
    sister_list = list(pd.unique(temp_sister.genomeList))
    sister_list.remove(0)
    for i in sister_list:
        if temp_sister.genomeList.count(i)>agent_avail[i]:
            print("Rainu")
            breach_count = temp_sister.genomeList.count(i)-agent_avail[i]
            indexes = [y for y, x in enumerate(temp_sister.genomeList) if x == i]
            agent_loc_ind_list = [0]*len(gd_req)
            TAT_ind_list = [0]*len(gd_req)
            same_day_ind_list = [0]*len(gd_req)
            day_1_compl = [0]*len(gd_req)
            day_2_compl = [0]*len(gd_req)
            for j in indexes:
                agent_loc_ind_list[j]=1
            for j in indexes:
                TAT_ind_list[j] = gd_req['TAT_breach_IND'][j]*17
            for j in indexes:
                same_day_ind_list[j] = gd_req['High_priority_int'][j]*2
            for j in indexes:
            	day_1_compl[j] = gd_req['TAT_breach1_ind'][j]*11
            for j in indexes:
            	day_2_compl[j] = gd_req['TAT_breach2_ind'][j]*7   	
            remove_list = [v + w + x + y + z for v, w, x, y, z in zip(agent_loc_ind_list, same_day_ind_list, day_2_compl, day_1_compl, TAT_ind_list)]
            one_count = remove_list.count(1)
            one_index = [y for y, x in enumerate(remove_list) if x == 1]
            three_count = remove_list.count(3)
            three_index = [y for y, x in enumerate(remove_list) if x == 3]
            eight_count = remove_list.count(8)
            eight_index = [y for y, x in enumerate(remove_list) if x == 8]
            twelve_count = remove_list.count(12)
            twelve_index = [y for y, x in enumerate(remove_list) if x == 12]
            ten_count = remove_list.count(10)
            ten_index = [y for y, x in enumerate(remove_list) if x == 10]
            fourteen_count = remove_list.count(14)
            fourteen_index = [y for y, x in enumerate(remove_list) if x == 14]
            eighteen_count = remove_list.count(18)
            eighteen_index = [y for y, x in enumerate(remove_list) if x == 18]               
            twenty_count = remove_list.count(20)
            twenty_index = [y for y, x in enumerate(remove_list) if x == 20]
            if breach_count<=one_count:
                for j in range(breach_count):
                    remove_index = random.choice(one_index)
                    temp_sister[remove_index]=0
                    one_index.remove(remove_index)
            elif one_count<breach_count<=(one_count + three_count):
                for j in one_index:
                    temp_sister[j]=0
                breach_count = breach_count-one_count
                for j in range(breach_count):
                    remove_index = random.choice(three_index)
                    temp_sister[remove_index]=0
                    three_index.remove(remove_index)
            elif (one_count + three_count)<breach_count<=(one_count + three_count + eight_count):
                for j in one_index:
                    temp_sister[j]=0
                for j in three_index:
                    temp_sister[j]=0
                breach_count = breach_count-(one_count+three_count)
                for j in range(breach_count):
                    remove_index = random.choice(eight_index)
                    temp_sister[remove_index]=0
                    eight_index.remove(remove_index)
            elif (one_count + three_count + eight_count)<breach_count<=(one_count + three_count + eight_count + twelve_count):
                for j in one_index:
                    temp_sister[j]=0
                for j in three_index:
                    temp_sister[j]=0
                for j in eight_index:
                    temp_sister[j]=0                    
                breach_count = breach_count-(one_count+three_count+eight_count)
                for j in range(breach_count):
                    remove_index = random.choice(twelve_index)
                    temp_sister[remove_index]=0
                    twelve_index.remove(remove_index)    
            elif (one_count + three_count + eight_count + twelve_count)<breach_count<=(one_count + three_count + eight_count + twelve_count + ten_count):
                for j in one_index:
                    temp_sister[j]=0
                for j in three_index:
                    temp_sister[j]=0
                for j in eight_index:
                    temp_sister[j]=0       
                for j in twelve_index:
                    temp_sister[j]=0                     
                breach_count = breach_count-(one_count+three_count+eight_count+twelve_count)
                for j in range(breach_count):
                    remove_index = random.choice(ten_index)
                    temp_sister[remove_index]=0
                    ten_index.remove(remove_index)
            elif (one_count + three_count + eight_count + twelve_count + ten_count)<breach_count<=(one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count):
                for j in one_index:
                    temp_sister[j]=0
                for j in three_index:
                    temp_sister[j]=0
                for j in eight_index:
                    temp_sister[j]=0       
                for j in twelve_index:
                    temp_sister[j]=0    
                for j in ten_index:
                    temp_sister[j]=0
                breach_count = breach_count-(one_count+three_count+eight_count+twelve_count+ten_count)
                for j in range(breach_count):
                    remove_index = random.choice(fourteen_index)
                    temp_sister[remove_index]=0
                    fourteen_index.remove(remove_index)                    
            elif (one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count)<breach_count<=(one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count + eighteen_count):
                for j in one_index:
                    temp_sister[j]=0
                for j in three_index:
                    temp_sister[j]=0
                for j in eight_index:
                    temp_sister[j]=0       
                for j in twelve_index:
                    temp_sister[j]=0    
                for j in ten_index:
                    temp_sister[j]=0
                for j in fourteen_index:
                    temp_sister[j]=0                    
                breach_count = breach_count-(one_count+three_count+eight_count+twelve_count+ten_count+fourteen_count)
                for j in range(breach_count):
                    remove_index = random.choice(eighteen_index)
                    temp_sister[remove_index]=0
                    eighteen_index.remove(remove_index)             
            elif (one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count + eighteen_count)<breach_count<=(one_count + three_count + eight_count + twelve_count + ten_count + fourteen_count + eighteen_count + twenty_count):
                print("7")
                for j in one_index:
                    temp_sister[j]=0
                for j in three_index:
                    temp_sister[j]=0
                for j in eight_index:
                    temp_sister[j]=0       
                for j in twelve_index:
                    temp_sister[j]=0    
                for j in ten_index:
                    temp_sister[j]=0
                for j in fourteen_index:
                    temp_sister[j]=0 
                for j in eighteen_index:
                    temp_sister[j]=0                 
                breach_count = breach_count-(one_count+three_count+eight_count+twelve_count+ten_count+fourteen_count+eighteen_count)
                print(breach_count)
                for j in range(breach_count):
                    remove_index = rand_choice(twenty_index)
                    temp_sister[remove_index]=0
                    twenty_index.remove(remove_index)  
    sister = temp_sister
    brother = temp_brother

    del(list_3_3)
    return (sister, brother)


# In[8]:


def obj_test_all(list):
    a = np.array(list.genomeList)

     ### DLA Assigned
    c = a[...,np.newaxis]
    ## Unassigned_gd
    c2=np.array(c==0)
    ## Assigned work_item
    c3=np.array(c!=0)
    temp_array=np.concatenate((np.asarray(gd_req.copy()),c),axis=1)
    temp_array12=np.concatenate((temp_array,c3),axis=1)

    temp_array1=np.concatenate((temp_array12,c2),axis=1)
    ###work_item	age	skill_requirement	TAT_breach_IND	High_priority_int	TAT_breach1_ind	TAT_breach2_ind Employee_ID assigned unassign 

    a=np.where(gd_req["TAT_breach_IND"]==0,1,0)
    c = a[...,np.newaxis]
    ###work_item	age	skill_requirement	TAT_breach_IND	High_priority_int	TAT_breach1_ind	TAT_breach2_ind Employee_ID assigned unassign no_TAT
    temp_array11=np.concatenate((temp_array1,c),axis=1)
    ##########################################################################################################
    ######### Adding new objective functions##################
    a=np.where(gd_req["TAT_breach1_ind"]==0,1,0)
    c = a[...,np.newaxis]
    ###work_item	age	skill_requirement	TAT_breach_IND	High_priority_int	TAT_breach1_ind	TAT_breach2_ind Employee_ID assigned unassign no_TAT no_TAT1
    temp_array111=np.concatenate((temp_array11,c),axis=1)

    a=np.where(gd_req["TAT_breach2_ind"]==0,1,0)
    c = a[...,np.newaxis]
    ###work_item	age	skill_requirement	TAT_breach_IND	High_priority_int	TAT_breach1_ind	TAT_breach2_ind Employee_ID assigned unassign no_TAT no_TAT1 no TAT2
    temp_array1111=np.concatenate((temp_array111,c),axis=1)

    a=np.where(gd_req["High_priority_int"]==0,1,0)
    c = a[...,np.newaxis]
    ###work_item	age	skill_requirement	TAT_breach_IND	High_priority_int	TAT_breach1_ind	TAT_breach2_ind Employee_ID assigned unassign no_TAT no_TAT1 no TAT2 no_sameday
    temp_array11=np.concatenate((temp_array1111,c),axis=1)


    ### Assigned is filtered table for only assigned Employee_IDs
    assigned=temp_array11[temp_array11[:,7]!=0]

    ### penalties
    ##TAT_breach_IND
    f1=len(temp_array11[(temp_array11[:,3]!=0) & (temp_array11[:,9]!=0)])*12500
    ###no_TAT_breach
    f2=len(temp_array11[(temp_array11[:,10]!=0) & (temp_array11[:,9]!=0)])*500


    ### rewards
    ## FIFO
    f9 = sum(temp_array11[:,8]*temp_array11[:,1]*2+1000)*(-1)
    ## PRiorty
    f10= sum(map(lambda x,y : agent_dict[x][y] ,assigned[:,7],assigned[:,2]))*(-1)
    ##f1+f2+f3+f4+f5+f6+f7+f8+f9+f10+ 1000000000000
    return f1+f2+f9+f10+ 1000000000000
