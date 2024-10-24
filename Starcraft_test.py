from dataclasses import dataclass
from matplotlib import pyplot as plt
import random
import numpy as np

path = 'C:/Users/jesus/OneDrive/Documents/Proyectos/Portfolio/Examen indio/reordernumber/SC2TGT_ListCorrupted'
path_clean = 'C:/Users/jesus/OneDrive/Documents/Proyectos/Portfolio/Examen indio/reordernumber/'

archivo = open(path, 'r',encoding= 'utf-8')
file = archivo.readlines()
  
class SCAIBot:

    def __init__(self):

        self.target_categories = []
        self.target_races = []
        self.target_priorities = []
        self.target_totalstatus = []
        self.target_designations = []

    def process(self):
        
            with open(path_clean + 'SC2TGT_ListClean' , 'r',encoding= 'utf-8') as f:
                for line in f.readlines():
                    (
                        target_designation, 
                        target_race, 
                        target_priority, 
                        target_shape, 
                        target_length, 
                        target_width, 
                        number_target_components, 
                        target_category, 
                        target_surveillance,
                        targe_type,
                        target_density,
                        target_mobility,
                        target_protection,
                        target_x_coordinate,
                        target_y_coordinate,
                        target_observer,
                        target_discovered_game_time,
                        target_health,
                        target_status,
                        target_point_value

                    ) = line.split(' ')
                    
                    self.target_categories.append(target_category)
                    self.target_races.append(target_race)
                    self.target_priorities.append(target_priority)
                    self.target_totalstatus.append(target_status)
                    self.target_designations.append(target_designation)


    def cleanCorruptedFile(self):

        result = []

        for line in file:

            if line.startswith('$%*@', 0, 4) and line.endswith('##**', -5, -1):
                result.append(line.replace('$%*@', '', 1).replace('##**', '', 1).strip())

            elif line.startswith('!!'):
                continue
            
            elif line.startswith('**##', 0, 5) and line.endswith('@*%$', -5, -1):
                result.append(line[::-1].replace('$%*@', '', 1).replace('##**', '', 1).strip())

        with open(path_clean + 'SC2TGT_ListClean' , 'w',encoding= 'utf-8') as f:
            f.write('\n'.join(result))

    
    def visualize_categories(self):
        
        number_tactical = dict((i, self.target_categories.count(i)) for i in self.target_categories)
        plt.pie(list(number_tactical.values()), labels = list(number_tactical.keys()), pctdistance= 1, autopct='%1.1f%%',  explode = [0, 0, 0.2], labeldistance=1.4 )
        plt.show()
    

    def visualizeRaces(self):
        
        number_race = dict((i, self.target_races.count(i)) for i in self.target_races)
        plt.pie(list(number_race.values()), labels = list(number_race.keys()), pctdistance= 1, autopct='%1.1f%%')
        plt.show()
     

    def visualizePriorities(self):
        
        number_priority = dict((i, self.target_priorities.count(i)) for i in self.target_priorities)
        plt.pie(list(number_priority.values()), labels = list(number_priority.keys()), pctdistance= 1, autopct='%1.1f%%', explode = [0.2, 0.2, 0.2], labeldistance=1.4)
        plt.show()
    

    def visualizeStatus(self):
        
        number_status = dict((i, self.target_totalstatus.count(i)) for i in self.target_totalstatus)
        plt.bar(range(3), number_status.values(), edgecolor= 'black', color=['blue','red','green'])
        plt.title('Target count by Status')
        plt.xticks(range(3), list(number_status.keys()), rotation=60)
        plt.ylabel('Target Counts')
        plt.ylim(min(number_status.values())-1, max(number_status.values())+50)
        plt.show()
    
    


    def analyzeTgtDesignations (self):
            number_AA = []
            number_AB = []
            number_AC = []
            number_AD = []
            number_AE = []
            number_AF = []
            target_designation_counts_values = []
            target_designation_keys = []


            number_designation = dict((i, self.target_designations.count(i)) for i in self.target_designations)
            for i in self.target_designations:

                if i.startswith('AA'): 
                    number_AA.append(self.target_designations.count(i))
                elif i.startswith('AB'): 
                    number_AB.append(self.target_designations.count(i))
                elif i.startswith('AC'): 
                    number_AC.append(self.target_designations.count(i))
                elif i.startswith('AD'): 
                    number_AD.append(self.target_designations.count(i))
                elif i.startswith('AB'): 
                    number_AE.append(self.target_designations.count(i))
                elif i.startswith('AF'): 
                    number_AF.append(self.target_designations.count(i))
            
            target_designation_counts_values = [sum(number_AA), sum(number_AB), sum(number_AC), sum(number_AD), sum(number_AE), sum(number_AF)]
            target_designation_keys = ['AA', 'AB',  'AC', 'AD', 'AE', 'AF' ]     
            target_designation_counts = dict([(target_designation_keys[0], target_designation_counts_values[0])])    
            print(target_designation_counts_values) 

            #diccionario = dict([("clave1", "valor1"), ("clave2", "valor2")])



    
                
        

            

     

bot = SCAIBot()
bot.cleanCorruptedFile()
bot.process()
#bot.visualize_categories()
#bot.visualizeRaces()
#bot.visualizePriorities()
#bot.visualizeStatus()
bot.analyzeTgtDesignations()


