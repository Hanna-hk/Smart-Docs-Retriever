"""
Scans a folder, reads TXT files, and splits them into chunks.
"""
import os
import datetime
import re
import json
import sys
from exception import CustomException
from log import logging
def make_chunks(directory):
    info = []
    logging.info("Reading files...")
    try:
        for file in os.listdir(directory):
            if file.endswith(".txt"):
                file_path = os.path.join(directory, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    chunks = content.split("\n\n")
                    id_chunk = "data_chunk_"
                    i = 0
                    for chunk in chunks:
                        if len(chunk) > 20:
                            chunk=re.sub(r'\n', ' ', chunk)
                            error = re.search(r"E-\d{3}", chunk)
                            metadata = {}
                            warnings =["warning", "danger", "caution", "injury"]
                            if chunk.upper().startswith("SECTION"):
                                metadata={
                                        "type: ": "header",
                                        "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    }
                            elif error:
                                metadata={
                                    "type: ":"error",
                                    "priority: ":"high",
                                    "code: ": error.group(0)
                                }
                            elif any(word in chunk.lower() for word in warnings):
                                metadata={
                                    "type: ":"warning",
                                    "priority: ":"critical"
                                }
                            else:
                                metadata={
                                    "type: ":"info"
                                }
                            info.append({
                                "id": id_chunk+str(i),
                                "source: ": file,
                                "data: ": chunk,
                                "metadata": metadata
                                }
                            )
                            i+=1
        output_path = directory+"processed/data.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        logging.info("JSON file with cleaned data has been created")
    except Exception as e:
        raise CustomException(e,sys)

if __name__ == "__main__":
    data_path = os.path.join(os.getcwd(), "data", "raw")
    make_chunks(data_path)