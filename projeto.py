import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

def loadData(CSVName):
    data = None
    try:
        data = pd.read_csv(CSVName, sep = ',', encoding = 'utf8')
    except:
        print('Error: Data not loaded')
    
    return data

def prepareData(data):

    print(data.info())

    print(data.describe())

    data.drop_duplicates(inplace = True)

    data.dropna(inplace=True)

    data.drop(columns=[], inplace = True)

    print(data)

def graphData(data):
    plt.figure(figsize=(10, 6))
    plt.hist(data['animalage'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribuição de Idade dos Animais')
    plt.xlabel('Idade')
    plt.ylabel('Frequência')
    plt.show()

CSVName = 'animal-data-1.csv'
print(CSVName)
data = loadData(CSVName)
print(data)
data = prepareData(data)
print(data)
graphData(data)