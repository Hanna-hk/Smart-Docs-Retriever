from exception import CustomException
from log import logging
import sys
import json
import numpy
import os
from sentence_transformers import SentenceTransformer
from data_loader import make_chunks
def indexer(file):
    try:
        if not(file.endswith(".json")):
            error = "Not JSON file. Can't index the data"
            raise CustomException(error, sys)
        logging.info("Reading the data")
        with open(file) as f:
            content = json.load(f)
        sentences = []
        for c in content:
            data = c.get("data", "")
            sentences.append(data)
        model = SentenceTransformer("all-MiniLM-L6-v2")
        logging.info("Encoding the data...")
        embeddings = model.encode(sentences)
        logging.info("Saving vectorized data...")
        output_path_npy = os.path.join(os.getcwd(), "data", "processed","vec_data.npy")
        numpy.save(output_path_npy, embeddings)
        logging.info(f"The data was indexed successfully! The shape of the numpy data: {embeddings.shape}")
        return output_path_npy
    except Exception as e:
        raise CustomException(e, sys)