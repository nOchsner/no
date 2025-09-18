import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv("./Netflix_Dataset.csv")


### Clean and preprocess some columns for visualization ###
# Drop unneeded columns
data = data.drop(['Title', 'Director', 'Cast', 'Description'], axis="columns")

# Convert the Release date to just a year
data['Release_Date'] = pd.to_datetime(data['Release_Date'], errors='coerce')
data['Year'] = data['Release_Date'].dt.year
data = data.drop('Release_Date', axis="columns")

# Convert Duration to int
def convert_duration(duration):
    if pd.isnull(duration):
        return None
    if "Season" in duration:
        return int(duration.split()[0])
    elif "min" in duration:
        return int(duration.split()[0])
    return None
data['Duration_Int'] = data['Duration'].apply(convert_duration)
data = data.drop('Duration', axis="columns")

# Create a separate series with data focusing on genre
genre_data = data['Type'].dropna()
genre_data = genre_data.str.split(', ').explode()



### Movies Vs TV Shows ###
plt.figure(figsize=(6,6))
data['Category'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title("Distribution of Movies vs TV Shows")
plt.ylabel("")
plt.show(block=False)


### Titles By Year ###
plt.figure(figsize=(10,5))
data['Year'].value_counts().sort_index().plot(kind='line', marker='o')
plt.title("Content Released per Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.show(block=False)


### Countries ###
plt.figure(figsize=(12,6))
data['Country'].value_counts().head(10).plot(kind='bar')
plt.title("Top 10 Content Producing Countries")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.show(block=False)


### Movie Ratings ###
plt.figure(figsize=(10,5))
data['Rating'].value_counts().plot(kind='bar')
plt.title("Distribution of Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show(block=False)


### Movie Durations ###
plt.figure(figsize=(10,5))
data[data['Category']=="Movie"]['Duration_Int'].dropna().plot(kind='hist', bins=20, edgecolor='black')
plt.title("Distribution of Movie Durations (in minutes)")
plt.xlabel("Duration (minutes)")
plt.ylabel("Frequency")
plt.show(block=False)


### Genre Info ###
# More cleaning
genre_data = data['Type'].dropna()
genre_data = genre_data.str.split(', ').explode()
genre_counts = genre_data.value_counts()
dropped_genres = [
    'International Movies', 
    'International TV Shows', 
    'British TV Shows', 
    'Korean TV Shows',
    'Movies',
    'TV Shows',
    'Spanish-Language TV Shows'
]
genre_counts = genre_counts.drop(dropped_genres, axis="rows")

# Merge Similar Genres
merge_map = {
    'TV Dramas': 'Dramas',

    'Romantic Movies': 'Romance',
    'Romantic TV Shows': 'Romance',

    'TV Comedies': 'Comedies',

    'Horror Movies': 'Horror',
    'TV Horror': 'Horror',

    'TV Action & Adventure': 'Action & Adventure',

    'TV Thrillers': 'Thrillers',

    'TV Sci-Fi & Fantasy': 'Sci-Fi & Fantasy',

    'Anime Features': 'Anime',
    'Anime Series': 'Anime',

    'Children & Family Movies': 'Family & Kids',
    "Kids' TV": 'Family & Kids',

    'Classic Movies': 'Classic & Cult',
    'Cult Movies': 'Classic & Cult',
    'Classic & Cult TV': 'Classic & Cult',

    'Stand-Up Comedy': 'Stand-Up Comedy',
    'Stand-Up Comedy & Talk Shows': 'Stand-Up Comedy'
}
genre_counts = genre_counts.rename(merge_map)
genre_counts = genre_counts .groupby(genre_counts.index).sum()


genre_counts_sorted = genre_counts.sort_values(ascending=True)

plt.figure(figsize=(10, 8))  
plt.barh(genre_counts_sorted.index, genre_counts_sorted.values, color='skyblue')


plt.title('Number of Titles per Genre', fontsize=16)
plt.xlabel('Number of Titles', fontsize=12)
plt.ylabel('Genre', fontsize=12)

for i, v in enumerate(genre_counts_sorted.values):
    plt.text(v + 10, i, str(v), va='center')

plt.tight_layout()
plt.show()


