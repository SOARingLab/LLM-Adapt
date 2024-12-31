from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from PyPDF2 import PdfMerger


def rag_topk_chunk(query, k):
    folder_path = './supporting_document_e'
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    merger = PdfMerger()

    for pdf in pdf_files:
        pdf_path = os.path.join(folder_path, pdf)
        merger.append(pdf_path)

    output_pdf = './supporting_document_e/merged_output.pdf'
    merger.write(output_pdf)
    merger.close()

    loader = PyPDFLoader('./supporting_document_e/merged_output.pdf')

    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 50,
    )

    docs = text_splitter.split_documents(pages)

    # print(len(docs))

    model_name = "sentence-transformers/sentence-t5-large"
    embedding = HuggingFaceEmbeddings(model_name=model_name)
    vectorstore_hf = Chroma.from_documents(documents=docs, embedding=embedding , collection_name="huggingface_embed")

    result = vectorstore_hf.similarity_search(query, k)  # Document,用.text转为str
    # print(result)
    return result
