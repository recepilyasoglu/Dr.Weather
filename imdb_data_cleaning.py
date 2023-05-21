import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)

# Scraping edilen veri setini düzenlemek üzere ele aldık.
df_ = pd.read_csv("imdb_weather_data.csv")
df = df_.copy()

# Duplicated filmlere baktık.
duplicated_titles = df[df.duplicated(['Title'], keep=False)]
print(duplicated_titles)

# Duplicated filmleri düşürdük.
def clear_data(df):
    df = df.drop_duplicates(subset='Title', keep='first') # Duplicate filmleri kaldıralım.
    df = df.reset_index() # Veriyi düzenleyelim.
    df = df.drop(columns=['Unnamed: 0', 'index'])
    return df

df = clear_data(df)

# Verileri düzenledikten sonra yeni bir .csv dosyasına atadık.
df.to_csv('imdb_movies.csv')

# Düzenlenen .csv dosyasını ele aldık.
df = pd.read_csv("imdb_movies.csv")
df = df.drop(columns=['Unnamed: 0'])

# Elimizdeki veri sayısına baktık.
df.shape # (23375, 9)

# Eksik verilere baktık.
df.isnull().sum()

# Genre ve Rating değişkenleri projemizde önemli değişkenlerdir.
# Bu değişkenlerdeki null değerleri olan verileri çıkardık.
df.dropna(subset=["Genre", "Rating"], inplace=True)

# Elimizdeki veri sayısına baktık.
df.shape # (21125, 9)

df.isnull().sum()
# 1 Year değişkeni, 4 Director değişkeni ve 15254 Gross değişkeni eksik kaldı.

# Gross değişkeni projemizde bir şey ifade etmediği için NaN olan değerleri 0 ile doldurduk.
df["Gross"].head()
df["Gross"].fillna('0', inplace=True)
df["Gross"].head()

# Boş olan Director ve Year değişkenlerini düşürdük.
df.dropna(subset=["Director", "Year"], inplace=True)

df.shape # (21120, 9)

df["Weather"].value_counts()

# Verileri düzenledikten sonra .csv dosyasına atadık.
df.to_csv('imdb_movies.csv')