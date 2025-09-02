import pandas as pd

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

CSVName = 'animal-data-1.csv'
print(CSVName)
data = loadData(CSVName)
print(data)
data = prepareData(data)
print(data)
