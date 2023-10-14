import gradio as gr
import chromadb
import pandas as pd

client = chromadb.PersistentClient(path="db/movies")

collection = client.get_collection(
        name="movie_reviews"
    )

def exec_query(input):
  
    
    res = collection.query(
        query_texts=input,
        n_results=10,
        include=["metadatas",'documents', 'distances'],
    )

    for k, v in enumerate(res.items()):
        if v[0] == "metadatas":
            df = pd.json_normalize(v[1][0])    

    docs = []
    plots = []
    for k, v in enumerate(res.items()):
        if v[0] == "documents":
            for a, b in enumerate(v[1]):
                for d in b:
                    plots.append(d)            

    for p in plots:
        docs.append(p)                    

    df["Plot"] = pd.Series(docs)

    dist = []
    distances = []
    for k, v in enumerate(res.items()):
        if v[0] == "distances":
            for a, b in enumerate(v[1]):
                for d in b:
                    distances.append(round(d,2))            

    for p in distances:
        dist.append(p)                    

    df["Distance"] = pd.Series(dist)    

    #df2 = df.assign(Plot= docs)
#    df = pd.DataFrame(res)
    new_cols = "Title", "Distance", "ReleaseYear", "Genre", "Director", "Plot", "Cast"
    df=df.reindex(columns=new_cols)
    return df

'''
with gr.Blocks() as demo:
    with gr.Row():
        gr.Interface(fn=exec_query,
                     inputs=gr.Textbox(lines=2, pplaceholder="Question here"),
                     outputs="dataframe",)
    with gr.Row():
        outputs="dataframe"

'''
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            inputs=gr.Textbox(lines=2, label="Search Criteria")
            text_button = gr.Button("Submit")
        with gr.Column():
            gr.Examples(["wall street, stock market, fraud", "Spaceships, aliens, and heroes saving America"], inputs, exec_query)
    with gr.Row():
        outputs=gr.Dataframe(row_count=(5, "dynamic"), wrap=True, overflow_row_behaviour="paginate", height=800)
        
    
    text_button.click(exec_query, inputs=inputs, outputs=outputs)

demo.launch()