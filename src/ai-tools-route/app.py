import json
import os
from logging import basicConfig, info, error

from extract.extractor import Extractor
from tags.classifier import Classifier


def main():
    info("Classification")
    classifier = Classifier()

    input1 = "போடா"
    response = classifier.classify(input1)
    info(input1 + ": " + json.dumps(response))

    input2 = "போங்க"
    response = classifier.classify(input2)
    info(input2 + ": " + json.dumps(response))

    info("Extraction")
    extractor = Extractor()

    input3 = "Hello! I am Prakash Mani, 37 years old. I am a software engineer with 15 years of experience in Python and Java. I live in Attur, Salem. I have my friend Subin, who is 35 years old and works as a data scientist. My wife named Nithya, who is 35 years old and works as a product manager."
    response = extractor.extract(input3)
    info(input3 + ": \n" + json.dumps(response))


def configure_logging():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(project_root, "app.log")
    basicConfig(level="INFO", format='%(asctime)s %(levelname)s %(message)s', filename=log_file, filemode='w')


if __name__ == "__main__":
    configure_logging()
    try:
        info("******* Tooling & Extraction Learning *******")
        main()
    except Exception as e:
        error(f"Error occurred while running the application: {e}", exc_info=True)
