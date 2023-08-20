import pinecone
import os
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

openai_api_key = os.getenv('OPENAI_API_KEY')


def borrar_indices(index_name='todos'):
    pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'), environment=os.environ.get('PINECONE_ENV'))

    if index_name == 'todos':
        indexes = pinecone.list_indexes()
        print('Borrando los indices...')
        for index in indexes:
            pinecone.delete_index(index)
        return 'Index borrado ' + index_name + ' Listo!'
    else:
        print(f'Borrando el indice {index_name}...', end='')
        pinecone.delete_index(index_name)
        return 'Index borrado ' + index_name + ' Listo!'


def creando_vectores(index_name, fragmentos):
    import pinecone
    from langchain.vectorstores import Pinecone
    from langchain.embeddings.openai import OpenAIEmbeddings

    embeddings = OpenAIEmbeddings()

    pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'),
                  environment=os.environ.get('PINECONE_ENV'))

    if index_name in pinecone.list_indexes():
        print(f'El índice {index_name} ya existe. Cargando los embeddings ... ', end='')
        vectores = Pinecone.from_existing_index(index_name, embeddings)
        print('Ok')
        mensaje = f'El índice {index_name} ya existe. Cargando los embeddings ... Ok'
    else:
        print(f'Creando el índice {index_name} y los embeddings ...', end='')
        pinecone.create_index(index_name, dimension=1536, metric='cosine')
        vectores = Pinecone.from_documents(fragmentos, embeddings, index_name=index_name)
        print('Ok')
        mensaje = f'Creando el índice {index_name} y los embeddings ...OK'
    return vectores, mensaje


def consulta_con_memoria(vectores, pregunta, memoria=[]):
    from langchain.chains import ConversationalRetrievalChain
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(temperature=1)
    retriever = vectores.as_retriever(search_type='similarity', search_kwargs={'k': 40})

    crc = ConversationalRetrievalChain.from_llm(llm, retriever)
    respuesta = crc({'question': pregunta, 'chat_history': memoria})
    memoria.append((pregunta, respuesta['answer']))

    return respuesta, memoria


def consultas(index, pregunta):
    from langchain.chains import RetrievalQA
    from langchain.chat_models import ChatOpenAI
    # switch back to normal index for langchain
    model_name = 'text-embedding-ada-002'
    text_field = "text"
    #inicializamos pinecone
    pinecone.init(api_key=os.environ.get('PINECONE_API_KEY'),
                  environment=os.environ.get('PINECONE_ENV'))
    #Definimos embeddings para que se carguen
    embed = OpenAIEmbeddings(
        model=model_name,
        openai_api_key=openai_api_key
    )
    #pide la informacion que esta en el indice de pinecone
    index = pinecone.Index(index)
    #Llama el vector
    vectorstore = Pinecone(
        index, embed.embed_query, text_field)

    llm = ChatOpenAI(openai_api_key=openai_api_key, model='gpt-3.5-turbo', temperature=0.7)

    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 40})

    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    answer = chain.run(pregunta)
    return answer