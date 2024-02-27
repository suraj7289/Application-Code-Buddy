import logging
import os
from pypdf import PdfReader
from zipfile import ZipFile
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings(model_name="paraphrase-MiniLM-L6-v2")

def read_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def read_default(file_path):
    file_text = ""
    file_extension = file_path.split('.')[-1]
    try:
        with open(file_path, encoding="utf8") as f:
            file_text = f.read()
    except:
        logging.info(f'Unable to read file due to encoding error-  {file_path}')
        supported_files_msg = """As of now, chatbot supports pdf, .py, .json, .html, .css, .cs, .js, .java, .sql, 
    .yaml, .log, .bat, .sh file types."""
        return f'Unable to read file due to encoding error. Chatbot does not support {file_extension} file type.' \
               f'{supported_files_msg}'

    return file_text

def get_file_content(test_zipFile):
    zip_content_text = ""
    with ZipFile(test_zipFile, 'r') as zip_ref:
        target_path = zip_ref.filename.split('.')[0]
        zip_ref.extractall(target_path)
        files_list = [os.path.join(target_path, file_name) for file_name in zip_ref.namelist()]

    for file in files_list:
        fileText = ""
        file_name = os.path.basename(file)
        file_ext = file_name.split('.')[-1]
        if file_ext == 'pdf':
            file_content = file_name + ":\n" + read_pdf(file) + '\n*****************\n'
        else:
            file_content = file_name + ":\n" + read_default(file) + '\n*****************\n'

        zip_content_text += file_content

    return zip_content_text


