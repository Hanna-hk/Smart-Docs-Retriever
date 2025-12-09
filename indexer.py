from exception import CustomException
from log import logging
import sys
import json
import numpy
import os
from sentence_transformers import SentenceTransformer
def indexer(file):
    try:
        if(file.endswith(".json")):
            logging.info("Reading the data")
            with open(file) as f:
                content = json.load(f)
            sentences = []
            vec_d=[]
            for c in content:
                data = c.get("data", "")
                sentences.append(data)
            model = SentenceTransformer("all-MiniLM-L6-v2")
            logging.info("Encoding the data...")
            embeddings = model.encode(sentences)
            emb_list = embeddings.tolist()
            for i in range(len(emb_list)):
                vec_d.append({
                    "vectorized_data": emb_list[i],
                    "metadata": content[i].get("metadata", "")
                })
            output_path = os.path.join(os.getcwd(), "data", "processed","indexed_data.json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            logging.info("Saving vectorized data...")
            with open(output_path, "w") as f:
                json.dump(vec_d, f, indent=2, ensure_ascii=False)
            output_path_npy = os.path.join(os.getcwd(), "data", "processed","vec_data.npy")
            numpy.save(output_path_npy, embeddings)
            logging.info("The data was indexed successfully")
        else:
            logging.warning("Not JSON file. Can't index the data")
    except Exception as e:
        raise CustomException(e, sys)
if __name__=="__main__":
    data_path = os.path.join(os.getcwd(), "data", "processed","data.json")
    indexer(data_path)