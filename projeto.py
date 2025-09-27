import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

le = LabelEncoder()

def loadData(CSVName):
    data = None
    try:
        data = pd.read_csv(CSVName, sep = ',', encoding = 'utf8')
    except:
        print('Error: Data not loaded')
    
    return data

def parseAnimalAge(age_value):
    if pd.isna(age_value):
        return pd.NA

    text = str(age_value).lower().strip()
    text = re.sub(r"[\.,]$", "", text)

    years_match = re.search(r"(\d+)\s*year", text)
    months_match = re.search(r"(\d+)\s*month", text)

    years = int(years_match.group(1)) if years_match else 0
    months = int(months_match.group(1)) if months_match else 0

    if years == 0:
        value = round(months / 12, 2)
    else:
        value = years

    if value < 0 or value > 25:
        return pd.NA

    return value

def normalizeBreed(breedname):
    if pd.isna(breedname):
        return "Unknown"

    breedname = breedname.lower().strip()

    if "mix" in breedname or "/" in breedname:
        return "Mixed Breed"

    breed_map = {
        "domestic short hair": "Domestic Shorthair",
        "domestic shorthair": "Domestic Shorthair",
        "domestic medium hair": "Domestic Mediumhair",
        "domestic mediumhair": "Domestic Mediumhair",
        "domestic long hair": "Domestic Longhair",
        "domestic longhair": "Domestic Longhair",
        "siamese": "Siamese",
        "maine coon": "Maine Coon",
        "manx": "Manx",
        "bengal": "Bengal",
        "snowshoe": "Snowshoe",
        "british shorthair": "British Shorthair",
        "calico": "Calico",
    }

    for key, value in breed_map.items():
        if key in breedname:
            return value

    return breedname.title() #capitaliza as palavras

def normalizeColour(breedcolour):
    if pd.isna(breedcolour):
        return "Unknown"

    breedcolour = breedcolour.lower().strip()
    breedcolour = breedcolour.replace("/", " and ").replace("&", " and ")

    combo_map = {
        ("black", "white"): "Black and White",
        ("black", "brown"): "Black and Brown",
        ("black", "grey"): "Black and Grey",
        ("grey", "white"): "Grey and White",
        ("brown", "white"): "Brown and White",
        ("orange", "white"): "Orange and White",
        ("buff", "white"): "Buff and White",
    }

    for (c1, c2), label in combo_map.items():
        if c1 in breedcolour and c2 in breedcolour:
            return label

    pattern_map = {
        "tortie": "Tortoiseshell",
        "tortoiseshell": "Tortoiseshell",
        "torbie": "Torbie",
        "calico": "Calico",
    }

    for key, value in pattern_map.items():
        if key in breedcolour:
            return value

    return breedcolour.title() #capitaliza as palavras

def cleanDataset(data):
    data = data.copy()
    data["breedname"] = data["breedname"].apply(normalizeBreed)
    data["basecolour"] = data["basecolour"].apply(normalizeColour)

    return data

def prepareData(data):
    if 'animalage' in data.columns:
        data['animalage'] = data['animalage'].apply(parseAnimalAge)

    data = cleanDataset(data)

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
    
    data['intakereason'] = le.fit_transform(data['intakereason'])
    data['breedname'] = le.fit_transform(data['breedname'])
    data['basecolour'] = le.fit_transform(data['basecolour'])
    data['speciesname'] = le.fit_transform(data['speciesname'])
    data['sexname'] = le.fit_transform(data['sexname'])

    data.dropna(inplace = True)
    
    return data

def prepareDataWithoutLabelEncoder(data):
    if 'animalage' in data.columns:
        data['animalage'] = data['animalage'].apply(parseAnimalAge)

    data = cleanDataset(data)

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

    data.dropna(inplace = True)

    return data

def gerarBoxplot(data):
    fig, ax = plt.subplots()
    ax.set_ylabel('Boxplot variáveis de raça')

    for n, col in enumerate(data.columns):
        if col == 'breedname':
            ax.boxplot(data[col], positions=[n+1])

    plt.title("Boxplot da coluna ...")
    plt.ylabel("Valores")
    plt.show()

def exibirGraficoBarrasBasecolour(type, dataWithoutLabelEncoder):
    title_map = {
        'cat': "Distribuição por cor de gatos",
        'dog': "Distribuição por raça de cachorros"
    }

    column_map = {
        'cat': "basecolour",
        'dog': "breedname"
    }

    column = column_map.get(type)
    title = title_map.get(type, "Distribuição")
    
    counts = dataWithoutLabelEncoder[column].value_counts().head(20)

    bar_colors = ['tab:red', 'tab:blue']
    plt.figure(figsize=(12,6))
    plt.title(title, fontsize=16, fontweight='bold')
    plt.bar(counts.index, counts.values, color=bar_colors)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def exibirGraficoBarrasSex(type, dataWithoutLabelEncoder):
    title_map = {
        'cat': "Distribuição por sexo de gatos",
        'dog': "Distribuição por sexo de cachorros"
    }

    title = title_map.get(type, "Distribuição")
    
    counts = dataWithoutLabelEncoder['sexname'].value_counts()

    bar_colors = ['tab:red', 'tab:blue']
    plt.figure(figsize=(12,6))
    plt.title(title, fontsize=16, fontweight='bold')
    plt.bar(counts.index, counts.values, color=bar_colors)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def exibirGraficoBarrasAge(type, df):
    title_map = {
        'cat': "Distribuição das idades de gatos",
        'dog': "Distribuição das idades de cachorros"
    }

    title = title_map.get(type, "Distribuição")
    
    df = df[(df['animalage'] >= 0) & (df['animalage'] <= 20)]
    df['animalage_group'] = pd.cut(
        df['animalage'],
        bins=[0, 0.5, 1, 2, 5, 10, 15, 20],
        labels=["0-6m","6-12m","1-2y","2-5y","5-10y","10-15y","15-20y"],
        right=False
    )

    counts = df['animalage_group'].value_counts().sort_index()
    
    bar_colors = ['tab:red', 'tab:blue']
    plt.figure(figsize=(12,6))
    plt.bar(counts.index, counts.values, color=bar_colors)
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel("Faixa etária")
    plt.ylabel("Número de animais")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def separarDados(data, type):

    if type == 'dog':
        Y = data['animalage', 'sexname', 'basecolour_normalized']
        X = data.drop(['breedname'],axis=1)
    else:
        Y = data['animalage', 'sexname', 'basecolour_normalized']
        X = data.drop(['basecolour'],axis=1)

    x_train, x_test, y_train, y_test = train_test_split(X, Y, 
                                                        test_size=0.3,
                                                        train_size=0.7, 
                                                        shuffle=True, 
                                                        random_state=42, 
                                                        stratify=Y)

    return x_train, x_test, y_train, y_test

CSVName = 'animal-data-1.csv'
data = loadData(CSVName)

data_without_label_encoder = prepareDataWithoutLabelEncoder(data)

if data_without_label_encoder is not None:

    data_cats = data[data['speciesname'] == 'Cat'].copy()
    data_cats_without_label_encoder = data_without_label_encoder[data_without_label_encoder['speciesname'] == 'Cat'].copy()
    # print(f"Total records: {len(data)}")
    # print(f"Cat records: {len(data_cats)}")

    data_cats = prepareData(data_cats)
    #exibirGraficoBarras(data_cats)

    data_dogs = data[data['speciesname'] == 'Dog'].copy()
    data_dogs_without_label_encoder = data_without_label_encoder[data_without_label_encoder['speciesname'] == 'Dog'].copy()
    # print(f"Total records: {len(data)}")
    # print(f"Dog records: {len(data_dogs)}")

    data_dogs = prepareData(data_dogs)

    print(exibirGraficoBarrasBasecolour('cat', data_cats_without_label_encoder))
    print(exibirGraficoBarrasAge('cat', data_cats_without_label_encoder))
    print(exibirGraficoBarrasSex('cat', data_cats_without_label_encoder))

    print(exibirGraficoBarrasBasecolour('dog', data_dogs_without_label_encoder))
    print(exibirGraficoBarrasAge('dog', data_dogs_without_label_encoder))
    print(exibirGraficoBarrasSex('dog', data_dogs_without_label_encoder))

    x_train, x_test, y_train, y_test = separarDados(data_cats, 'cat')
    x_train, x_test, y_train, y_test = separarDados(data_dogs, 'dog')

    # gerarBoxplot(data_cats_without_label_encoder)
    # gerarBoxplot(data_dogs_without_label_encoder)
    # gerarBoxplot(data_cats)
    # gerarBoxplot(data_dogs)
    # print(data_dogs['breedname'])
    # print(data_dogs_without_label_encoder['breedname'])