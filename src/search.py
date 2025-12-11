import numpy
from log import logging
from exception import CustomException
import json
import sys
import os
from db_logger import RequestLogger
import re
from indexer import indexer
from data_loader import make_chunks
from sentence_transformers import SentenceTransformer, util
class Searcher:
    def __init__(self, data_file, numpy_file, request):
        if not(data_file.endswith(".json") and numpy_file.endswith(".npy")):
            error1 = "Incorrect types of files"
            raise CustomException(error1, sys)
        with open(data_file) as f:
            self.data = json.load(f)
        self.data_numpy = numpy.load(numpy_file)
        if len(self.data) != len(self.data_numpy):
            error2 = "The data in the json file is incompatible with the data in the numpy file"
            raise CustomException(error2,sys)
        logging.info("The data has been loaded successfully")
        self.request = re.sub(r'\s+', ' ', request).strip()
    def request_processing(self, threshold=0.25):
        model = SentenceTransformer("all-MiniLM-L6-v2")
        logging.info("The request has been transformed")
        encoded_req=model.encode(self.request)
        self.cosine = util.semantic_search(encoded_req, self.data_numpy, top_k=3)[0]
        logging.info("Cosine Similarity has been calculated")
        answers=[]
        for res in self.cosine:
            if(res['score']>threshold):
                answers.append(self.data[res['corpus_id']])
        log_r = RequestLogger()
        if answers==[]:
            logging.info("There are no answers for this request")
            log_r.insertRequest(self.request)
        else:
            logging.info("The most accurate answers were found and inserted into the database")
            best_ans = answers[0]
            top_id = best_ans.get('metadata', {}).get('id', 'unknown_id')
            top_score = self.cosine[0]['score']
            preview = best_ans.get('data', '')[:150]
            log_r.insertRequest(self.request, 
                                len(answers),
                                top_id, round(top_score,4),
                                preview
                                )
            return answers
if __name__=="__main__":
    try:
        data_path = os.path.join(os.getcwd(), "data", "raw")
        output_path_chunks = os.path.join(os.getcwd(), "data", "processed","data.json")
        output_path_npy = os.path.join(os.getcwd(), "data", "processed","vec_data.npy")
        if not (os.path.exists(output_path_chunks) or os.path.exists(output_path_npy)):
            output_path_chunks = make_chunks(data_path)
            output_path_npy=indexer(output_path_chunks)
        if len(sys.argv)>=2:
            search = Searcher(output_path_chunks, output_path_npy, sys.argv[1])
            search.request_processing()
        else:
            logging.info("There are no arguments")
    except Exception as e:
        raise CustomException(e, sys)