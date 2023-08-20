def cargar_documento(archivo):
    import os
    nombre, extension = os.path.splitext(archivo)
    if extension == '.pdf':
        from langchain.document_loaders import PyPDFLoader
        print(f'Cargando {archivo}...')
        loader = PyPDFLoader(archivo)
    elif extension == '.docx':
        from langchain.document_loaders import Docx2txtLoader
        print(f'Loading {archivo}...')
        loader = Docx2txtLoader(archivo)
    elif extension == '.csv':
        from langchain.document_loaders.csv_loader import CSVLoader
        print(f'Loading {archivo}...')
        loader = CSVLoader(archivo)    
    else:
        print('El formato de documento no es soportado!')
        return None
    
    data = loader.load()
    return data

def fragmentar(data, chunk_size):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter =RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=50)
    fragmentos = text_splitter.split_documents(data)
    return fragmentos

def costo_embedding(texts):
    import tiktoken
    enc =  tiktoken.encoding_for_model('text-embedding-ada-002')
    total_tokens = sum([len(enc.encode(page.page_content))for page in texts])
    print(f'Total Tokens: {total_tokens}')
    print(f'Embedding Cost in USD: {total_tokens / 1000 * 0.0001:.5f}')

