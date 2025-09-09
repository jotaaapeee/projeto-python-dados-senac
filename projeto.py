import re
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
    def parse_animal_age(age_value):
        if pd.isna(age_value):
            return pd.NA
        text = str(age_value).lower().strip()

        text = re.sub(r"[\.,]$", "", text)

        years_match = re.search(r"(\d+)\s*year", text)
        months_match = re.search(r"(\d+)\s*month", text)
        years = int(years_match.group(1)) if years_match else 0
        months = int(months_match.group(1)) if months_match else 0
        value = float(f"{years}.{months}")
        return value

    if 'animalage' in data.columns:
        data['animalage'] = data['animalage'].apply(parse_animal_age)

    print(data.info())

    print(data.describe())

    data.drop_duplicates(inplace = True)

    data.dropna(inplace=True)

    data.drop(columns=[], inplace = True)

    print(data)

    return data

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
print('=========================')
print(data['animalage'])
print('=========================')
print(data)
# graphData(data)