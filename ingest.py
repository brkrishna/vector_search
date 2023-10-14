import chromadb
import json

client = chromadb.PersistentClient(path="db/movies")

try:
    client.delete_collection("movie_reviews")
except:
    pass

collection = client.get_or_create_collection(
        name="movie_reviews",
        metadata={"hnsw:space": "cosine"} # l2 is the default
    )


with open('wiki_movie_plots.json', encoding = 'utf8') as f:
    data = json.load(f)

plot = metainfo = []

counter = 1

for i, movie in enumerate(data, start=1):
    if movie["Origin"] in ('American','British','Canadian'):
        identityfield = []
        identityfield.append('"' + str(counter) + '"')
        collection.add(
            documents=movie["Plot"],
            metadatas={"ReleaseYear":movie["ReleaseYear"], 
            "Title":movie["Title"], 
            "Origin":movie["Origin"],
            "Director":movie["Director"],
            "Cast":movie["Cast"],
            "Genre":movie["Genre"],
            "WikiPage":movie["WikiPage"]
            },
            ids=identityfield
        )
        counter+=1

