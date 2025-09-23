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

    # print(data.info())

    # print(data.describe())

    # data.dropna(inplace=True)

    # data.drop_duplicates(inplace = True)

    data = data.drop_duplicates()

    data.drop(columns=['sheltercode', 
                       'identichipnumber', 
                       'deceaseddate', 
                       'returndate', 
                       'istrial', 
                       'intakedate', 
                       'returnedreason', 
                       'location', 
                       'movementtype', 
                       'isdoa'], inplace = True)

    le = LabelEncoder()
    # data['intakereason'] = le.fit_transform(data['intakereason'])
    # data['breedname'] = le.fit_transform(data['breedname'])
    # data['basecolour'] = le.fit_transform(data['basecolour'])
    # data['speciesname'] = le.fit_transform(data['speciesname'])
    # data['sexname'] = le.fit_transform(data['sexname'])
    # data['deceasedreason'] = le.fit_transform(data['deceasedreason'])

    data.dropna(inplace = True)
    # print(data.info())
    # print(data.describe())
    # print(data)

    return data

def exibirGraficoBarras(dados):
    print(f"Number of records: {len(dados)}")
    print(dados)
    dados_grouped = dados.groupby('basecolour').groups
    print(dados_grouped)
    lb = []
    vl = []
    for grp in dados_grouped:
        lb.append(str(grp))
        vl.append(len(dados_grouped[grp]))

    bar_colors = ['tab:red', 'tab:blue']
    plt.bar(lb, vl, color=bar_colors)
    plt.show()

CSVName = 'animal-data-1.csv'
print(CSVName)
data = loadData(CSVName)

# data_cats = data[data['speciesname'] == 'Cat'].copy()
# print(f"Total records: {len(data)}")
# print(f"Cat records: {len(data_cats)}")

# data_cats = prepareData(data_cats)
# exibirGraficoBarras(data_cats)

# data_dogs = data[data['speciesname'] == 'Dog'].copy()
# print(f"Total records: {len(data)}")
# print(f"Dog records: {len(data_dogs)}")

# data_dogs = prepareData(data_dogs)
# exibirGraficoBarras(data_dogs)