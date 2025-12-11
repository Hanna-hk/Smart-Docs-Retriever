"""
Scans a folder, reads TXT files, splits them into chunks and writes to JSON file.
"""
import os
import datetime
import re
import json
import sys
from exception import CustomException
from log import logging
from enum import Enum

# As we have 4 types of data, we can create an enum class for better readability and easier maintenance
class typesOfData(Enum):
    INFO=0
    ERROR=1
    HEADER=2
    WARNING = 3

def make_chunks(directory):
    information = []
    logging.info("Reading files...")
    try:
        for file in os.listdir(directory):
            if file.endswith(".txt"):
                file_path = os.path.join(directory, file)

                with open(file_path, "r") as f:
                    content = f.read()
                    chunks = content.split("\n\n")
                    id_chunk = re.sub(r".txt", '', file)+"_data_chunk_"
                    i = 0

                    for chunk in chunks:
                        if len(chunk) > 60:
                            chunk=re.sub(r'\n', ' ', chunk)

                            # Warnings always contain those words
                            warnings =["warning", "danger", "caution", "injury"]
                            # An error message always starts with "E-some digits"
                            error = re.search(r"E-\d{3}", chunk)

                            typeOfData = typesOfData.INFO.name

                            # Headers always start with SECTION
                            if chunk.upper().startswith("SECTION"):
                                typeOfData = typesOfData.HEADER.name
                            elif error:
                                typeOfData=typesOfData.ERROR.name
                            elif any(word in chunk.lower() for word in warnings):
                                typeOfData=typesOfData.WARNING.name

                            # The metadata for all types of chunks
                            metadata = {
                                "id": id_chunk+str(i),
                                "source": file,
                                "type":typeOfData,
                                "title":chunk.split("\n")[0],
                                "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }

                            information.append({
                                "data": chunk,
                                "metadata": metadata,
                                }
                            )
                            i+=1

        logging.info("Saving data to the JSON file...")
        output_path = os.path.join(os.getcwd(), "data", "processed","data.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(information, f, indent=2, ensure_ascii=False)
        logging.info("JSON file with cleaned data has been created")

        return output_path
    
    except Exception as e:
        raise CustomException(e,sys)