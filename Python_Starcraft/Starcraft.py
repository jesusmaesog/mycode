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
        self.target_type = []

    def process(self):
        
        #abrimos el archivo que nos da las líneas limpias del archivo y nos da todas las líneas en formato texto con el método readlines.
        #en la variable total lines te guarda cada una de las líneas donde cada elemento de la lista es una lista. Al contarlas todas con len
        #me da el total de líneas y me las guardo en la variable self.target_designation_counts_values
            with open(path_clean + 'SC2TGT_ListClean' , 'r',encoding= 'utf-8') as f:
                total_lines = f.readlines()
                self.target_designation_counts_values = len(total_lines)

                #entrando al for para ver linea a linea y sacamos una tupla para cada uno de los elementos contenidos en cada una de las lineas

                for line in total_lines:
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
                        target_type,
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
                    self.target_type.append(target_type)
                    

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
 

        number_designation = dict((i, self.target_designations.count(i)) for i in self.target_designations)
        number_target_type = dict((i, self.target_type.count(i)) for i in self.target_type)
                
        self.target_designations_type = dict()
        type_designations = ['A' + str(chr(ord('A') + i)) for i in range(0, 6)]
                
        for n, i in enumerate(self.target_designations):
            for type in type_designations:
                if self.target_designations[n].startswith(type): 
                    if type not in self.target_designations_type:
                        self.target_designations_type[type] = dict()
                            
                    else:
                        if self.target_type[n] not in self.target_designations_type[type]:
                            self.target_designations_type[type][self.target_type[n]] = 0
                        else:
                            self.target_designations_type[type][self.target_type[n]] += 1
                


        number_priority = dict((i, self.target_priorities.count(i)) for i in self.target_priorities)
        self.target_priorities_type = dict()

                    
        for n, i in enumerate(self.target_priorities):
            for type in type_designations:
                if self.target_designations[n].startswith(type): 
                    if type not in self.target_priorities_type:
                        self.target_priorities_type[type] = dict()
                    
                    else:
                        if self.target_priorities[n] not in self.target_priorities_type[type]:
                            self.target_priorities_type[type][self.target_priorities[n]] = 0
                                    
                        else:
                            self.target_priorities_type[type][self.target_priorities[n]] += 1

                            
        number_race = dict((i, self.target_races.count(i)) for i in self.target_races)
                
        self.target_races_type = dict()
        self.target_races_type['Zerg'] = dict()
        self.target_races_type['Protoss'] = dict()
        zergs = []
        protoss = []
        keys = []
                

                
        for n, i in enumerate(self.target_races):
            for type in sorted(type_designations):
                if self.target_races[n].startswith(type): 
                    if type not in self.target_races_type:
                        self.target_races_type[self.target_races[n]][type] = dict()
                    
                    else:
                        if self.target_races[n] not in self.target_races_type[type]:
                            self.target_races_type[self.target_races[n]][type] = 0
                                    
                        else:
                            self.target_races_type[self.target_races[n]][type] += 1
                        print(self.target_races_type)
        '''                
        for n, i in enumerate(self.target_races_type):
            for race in self.target_races_type[n]:
                for type in sorted(self.target_priorities_type):
        '''



bot = SCAIBot()
bot.cleanCorruptedFile()
bot.process()
bot.visualize_categories()
bot.visualizeRaces()
bot.visualizePriorities()
bot.visualizeStatus()
#bot.analyzeTgtDesignations()

'''
            for type in sorted(self.target_priorities_type):
                for k in self.target_races_type[type].keys():
                    if k == 'Zerg':
                        zergs.append(self.target_races_type[type][k])
                    elif k == 'Protoss':
                        protoss.append(self.target_races_type[type][k])

            keys = sorted(self.target_priorities_type.keys())
'''
            
            
            


      
                    #print(type)
                    #print(self.target_races_type[type])
                    #if 'Zerg' in race:
                    #        print(type + ': ' + str(self.target_races_type[race][type])+ ' ', end='')
                    #print()

                    #print('TARGET PRIORITY COUNTS ' + type + ' DESIGNATED TARGETS\n  ', end = '')
                    #for k in self.target_priorities_type[type].keys():
                    #    print(str(k) + ':' + str(self.target_priorities_type[type][k]) + ' ', end = '')
                    #print('')
   
            
           


@dataclass
class SC2Target:

    designation: str
    race: str
    priority: str
    shape: str
    length: int
    width: int
    components: int
    status: str
    pvalue: int
    health: int
    mobility: str
    protection: str
    density: str
    discovered: int
    discoverdBy: str
    coordinate_x: int
    coordinate_y: int
    ttype: str
    surveillance: bool
    category: str
    





#print('ZERG TARGETS: \n', dict([sorted(self.target_priorities_type.keys()), zergs]))
                #los zergs son los valores y con los type como llaves hacer un diccionario e imprimirlo por pantalla y lo mismo para los protoss


                
                #print(str(k) + ':' + str(self.target_races_type[type][k]) + ' ', end = '')
                #print('ZERG TARGETS: \n', str(type + ':'), str(self.target_races_type[type][k]))
                #print(sorted(self.target_races_type.keys()))
'''
            for type in sorted(self.target_races_type):
                print(sorted(self.target_races_type.keys()), self.target_races_type.values())
'''                
            

'''


                            for type in self.target_priorities_type:
                                print('TARGET PRIORITY COUNTS ' + type + ' DESIGNATED TARGETS\n  ', end = '')
                                for k in self.target_priorities_type[type].keys():
                                    print(str(k) + ':' + str(self.target_priorities_type[type][k]) + ' ', end = '')
                                print('')

'''

            # print('Total Targets:', self.target_designation_counts_values, '\n') 
            # print('TARGET DESIGNATION COUNTS\n  ', end='')

            # self.target_designations_type_count = dict((i, sum(self.target_designations_type[i].values())) for i in sorted(self.target_designations_type))

            # for k in self.target_designations_type_count:
            #     print(str(k) + ': ' + str( self.target_designations_type_count[k]) + ' ', end = '')
            # print('\n')

            # for type in self.target_designations_type:
            #     print('TARGET TYPE COUNTS ' + type + ' DESIGNATED TARGETS\n  ', end = '')
            #     for k in self.target_designations_type[type].keys():
            #             print(str(k) + ':' + str(self.target_designations_type[type][k]) + ' ', end = '')
            #     print('')
            
            
'''
            for type in sorted(self.target_priorities_type):
                print('TARGET PRIORITY COUNTS ' + type + ' DESIGNATED TARGETS\n  ', end = '')
                for k in self.target_priorities_type[type].keys():
                     print(str(k) + ':' + str(self.target_priorities_type[type][k]) + ' ', end = '')
                print('')
'''