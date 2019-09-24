# NP-Hard-Problems
Using Genetic Algorithm to optimize an Inventory Prioritization Problem

The code tries to optimise work allocation in any operations business where we have conflicting paramters such as
1. TAT
2. Availablity of an Agent
3. Skillset of an Agent
4. Work Item specific constraints 

In this use case, we try to optimize the following constraints 
"age"  : How long a work item has been pending
"skill_requirement"  The type of skill required to complete this task -- SOme type of code
"TAT_breach_IND"  : Has the TAT been breached or not
'High_priority_int' : Is is a high priority job or not 
"TAT_breach1_ind" : Will we TAT get breached in 1 day 
"TAT_breach2_ind" : WIll the TAT get breached in 2 days 
