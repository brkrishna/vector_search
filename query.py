import chromadb
import json

client = chromadb.PersistentClient(path="db/movies")

collection = client.get_collection(
        name="movie_reviews"
    )

res = collection.query(
    query_texts=["Spaceships, aliens, and heroes saving America",],
    n_results=3,
    include=["metadatas",'documents', 'distances'],
)
# dict = []

# for k, v in enumerate(res.items()):
#     #print(k, v )
#     if v[0] == "metadatas":
#         for a, b in enumerate(v[1][0], start=1):
#             details = b
#             dict = json.dumps(v[1][0], indent=2)

print(res)
docs = []
plots = []
c = {}
for k, v in enumerate(res.items()):
    if v[0] == "documents":
        for a, b in enumerate(v[1]):
            for d in b:
                plots.append(d)

for p in plots:
    docs.append({"Plot":p})

#print(dict)
print(docs)
'''
details = {}
for i, d in enumerate(res.items(), start=1):
    print(i, d)
    if d[0] == "metadatas":
        for j,k in enumerate(d[1][0], start=1):
            details = k
            print(f"Title: {details['Title']}, Genre: {details['Genre']}")
            print(details)


json_data = []
for r in res:
    json_data.append(dict(zip(r)))

print(json.dumps(json_data))
'''