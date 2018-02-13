
# coding: utf-8

# In[36]:


import csv

with open("C:\\Users\\binod\\Desktop\\Statistical_Learning\\Data_Insight_Challegen\\2018\\by_date\\itcont_2018_20171118_20180113.txt", "r") as file_pipe:
    with open("C:\\Users\\binod\\Desktop\\Statistical_Learning\\Data_Insight_Challegen\\2018\\by_date\\MT.csv",'w') as file_comma:
        csv.writer(file_comma, delimiter = ',').writerows(csv.reader(file_pipe, delimiter = '|'))


# In[37]:


import pandas as pd
df = pd.read_csv("C:\\Users\\binod\\Desktop\\Statistical_Learning\\Data_Insight_Challegen\\2018\\by_date\\MT.csv", header=None)


# In[38]:


len(df)


# In[39]:


df.columns


# In[40]:


name=["CMTE_ID", "AMNDT_IND", "RPT_TP", "TRANSACTION_PGI", "IMAGE_NUM", "TRANSACTION_TP", "ENTITY_TP", "NAME", "CITY", "STATE", "ZIP_CODE","EMPLOYER", "OCCUPATION", "TRANSACTION_DT", "TRANSACTION_AMT",  "OTHER_ID", "TRAN_ID", "FILE_NUM", "MEMO_CD", "MEMO_TEXT" , "SUB_ID" ]


# In[41]:


df.columns = name


# In[42]:


dataframe = df[['CMTE_ID', "NAME" , "ZIP_CODE",  "TRANSACTION_DT", "TRANSACTION_AMT", "OTHER_ID"]]


# In[43]:


dataframe = dataframe.dropna(subset =[['ZIP_CODE','TRANSACTION_DT',"NAME","CMTE_ID", "TRANSACTION_AMT"]])


# In[44]:


len(dataframe)


# In[45]:


dataframe.head()


# In[46]:


dataframe['ZIP_CODE'] = dataframe['ZIP_CODE'].astype(str).str[0:5]


# In[47]:


dataframe['DONOR_ID'] = dataframe['NAME'].str.split().str[1]+dataframe['ZIP_CODE']


# In[48]:


dataframe['OTHER_ID'] = dataframe['OTHER_ID'].astype(str)


# In[49]:


len(dataframe)


# In[51]:


dataframe = dataframe[dataframe['OTHER_ID'] == 'nan']


# In[52]:


dataframe.OTHER_ID.unique()


# In[54]:


len(dataframe)


# In[55]:


dataframe.ZIP_CODE.nunique()


# In[56]:


df_try = dataframe.copy()


# In[57]:


df_try = df_try.reset_index()


# In[58]:


df_try = df_try.drop('index', 1)


# In[59]:


len(df_try)


# In[60]:


## Removing the donors that has only donated once.
filtered  = df_try.groupby('DONOR_ID').filter(lambda x: len(x) >=2)


# In[61]:


filtered = filtered.reset_index()



# In[62]:


filtered.drop('index',1, inplace = True)


# In[64]:


new_df = filtered[['CMTE_ID', 'DONOR_ID', "NAME", "ZIP_CODE", "TRANSACTION_AMT"]]
new_df = new_df[0:2000]


# In[65]:




import numpy as np
door = []
occurance_list = []
skip_list =[]
Transaction_amt = 0
count = 0
row = 1
for i in new_df.ZIP_CODE:
    for cmte,zipcode,transamt in zip(new_df.CMTE_ID,new_df.ZIP_CODE, new_df.TRANSACTION_AMT):
        if(i==zipcode) and (zipcode not in skip_list):
            
            if count ==0:
                Transaction_amt = transamt  + Transaction_amt
                occurance_list.extend((cmte,zipcode,"2018",transamt,Transaction_amt,count+1))
            else:
                occurance_list.extend((cmte,zipcode,"2018",np.percentile(np.array([ Transaction_amt,transamt]), 30),Transaction_amt+transamt,count))
                Transaction_amt = transamt+Transaction_amt                
                  
            count+=1
           # print(occurance_list)
            door.append(occurance_list)
            occurance_list=[]
                   
           
           
            
            
    skip_list.append(i)
    Transaction_amt = 0
    count = 0


# In[66]:


new_door = pd.DataFrame(door)


# In[67]:


new_names = ['CMT_ID', 'ZIP', 'YEAR', 'AMT1', "AMT2", "OCCURENCE"]


# In[68]:


new_door.columns = new_names


# In[69]:


new_door.to_csv(r'C:\\Users\\binod\\Desktop\\Statistical_Learning\\Data_Insight_Challegen\\2018\\by_date\\repeat_donors.txt', header = None, index = None, sep ='|', mode ='a')

