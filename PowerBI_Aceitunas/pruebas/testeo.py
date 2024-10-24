import numpy as np
import pandas as pd

path = 'C:/Users/jesus/OneDrive/Documents/Proyectos/Portfolio/Aceitunas/Dataset/'

indice = list(np.arange(0,1158))

df = pd.read_csv(path + '20057000_aceitunas.csv', sep= ',')

dfsorted = df.sort_values(by= ['Provincia', 'Anyo', 'Mes'], ascending= True)

df = pd.DataFrame(dfsorted.values, index=[indice], columns = [df.columns])

df['Elasticity'] = np.zeros(len(df))

#print(np.dtype(df['Provincia']))

#print(df.head())





for i in range(0,len(df)):
    if int(i) < len(df): 
        try:
            elasticidad = abs(
                ((float(df.iloc[i+1]['Peso']) - float(df.iloc[i]['Peso'])) / float(df.iloc[i]['Peso'])) \
            / ((float(df.iloc[i+1]['Precio Medio']) - float(df.iloc[i]['Precio Medio'])) / float(df.iloc[i]['Precio Medio']))
            )
            df.at[i+1, 'Elasticity'] = elasticidad
            
            #print(df) 
        except ZeroDivisionError:
            pass
    
        
       
    print(df)

    df.to_csv('20057000_aceitunas2.csv', index= False, encoding='utf-8', sep=',', na_rep='Unknown')





























































# arr = np.array([{'eventDate': '2022-06-02', 'playtime': 4, 'status': 'trial'}, 
#  {'eventDate': '2022-06-01', 'playtime': 6, 'status': 'trial'}, 
#  {'eventDate': '2022-06-04', 'playtime': 10, 'status': 'subscription'}])

# for i in arr:
#     for k, v in i.items():
#         if k == 'status' and v == 'subscription': print(len(i))
            
# # list = np.arange(-109, 110)
# # target = int(input('Write a number: '))

# # for i in list: 
# #     if target == i: 
# #         print(np.where(list == target)) 
# #     else: print(-1)
# #     break

# # eventDate= date(input()) 
# # playtime= int(input()) 
# # status= str(input())

# #arr = np.array([dict (np.datetime64()), int(), str()])  

# # print(arr[2[:-1]])


# # Q2.
# # You are given an array(list) result that contains hashmaps(dicts). The key value pairs are as follows:
# # eventDate : DATE
# # Playtime : INTEGER
# # status : STRING

# # Find the difference in whole days between the minimum eventDate and the day the user status converted to subscription.
# # If there is no subscription status, return -1.

# # You must write an algorithm with Linear or better runtime complexity. 

# # Constraints:
# # status can only be trial or subscription
# # The array is not sorted 


# # Example -
# # Input:
# # [ {eventDate: ’2022-06-02’, playtime: 4, status: ‘trial’}, 
# # {eventDate: ’2022-06-01’, playtime: 6, status: ‘trial’}, 
# # {eventDate: ’2022-06-04’, playtime: 10, status: ‘subscription’} ]

# # Result:
# # 3

# #-----------------------------------------------------------------
# # Python

# # Q1.
# # Given a sorted array(list) of integers nums and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.

# # Bonus points for writing a runtime optimised algorithm.

# # Constraints:
# # The array is sorted
# # Elements will not be repeated
# # 2 <= nums.length <= 104
# # -109 <= nums[i] <= 109
# # -109 <= target <= 109
# # Only one valid answer exists.

# # Example:
# # Input: nums = [-7,-5, 2, 4, 7, 12], target = 7
# # Output: 4


# # For n in list
