import pyarrow.parquet as pq
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class retriever():
    def __init__(self):
        parquet_file = pq.ParquetFile('rawdata/test-00000-of-00001.parquet')
        self.alldb = parquet_file.read().to_pandas()
        labeltable = self.alldb.loc[self.alldb['label']==1]
        unique_qid = labeltable['question_id'].unique()
        loader = CSVLoader(file_path='text.csv',source_column="answer",encoding = 'UTF-8',csv_args={
            # 'delimiter': ',',
            # 'fieldnames': ['question_id', 'question', 'document_title', 'answer','label']
        })
        embeddings = HuggingFaceEmbeddings()
        docdata = loader.load()
        self.vector = FAISS.from_documents(docdata, embeddings)
    def getTitle(self,idx):
        return self.alldb.iloc[idx]['document_title']
    def retrieve_doc(self,k, query):
        ret = self.vector.as_retriever(search_kwargs={"k": k}).get_relevant_documents(query)
        return ret
    def retrieve_alldocs(self,k,query):
        ret = self.retrieve_doc(k,query)
        retlist = []
        for item in ret:
            doc = item.metadata['source']
            title = self.getTitle(item.metadata['row'])
            retlist.append({
                'title':title,
                "content":doc
            })
        return retlist

def retrieve_doc(k, query):
    ret = vector.as_retriever(search_kwargs={"k": k}).get_relevant_documents(query)
    return ret

def get_precision(gtlist, prelist):
    count = 0
    for item in prelist:
        if(item in gtlist):
            count += 1
    return count / len(prelist)

def get_recall(gtlist, prelist):
    count = 0
    for item in gtlist:
        if(item in prelist):
            count += 1
    return count / len(gtlist)

def get_AP(m,gtlist,query):
    all = 0
    for k in range(1,m+1):
        ret_docs = retrieve_doc(k,query)
        prelist = [item.metadata['row'] for item in ret_docs]
        precision = get_precision(gtlist, prelist)
        all+=precision
    return all/m  

def fetch_AP(gtlist,query):
    N = 500
    ret_docs = retrieve_doc(N,query)
    prelist = [item.metadata['row'] for item in ret_docs]
    rem = len(gtlist)
    idx = 0
    plist = []
    while(rem > 0 and idx<N):
        prerow = prelist[idx]
        if(prerow in gtlist):
            plist.append((len(plist)+1)/(idx+1))
            rem -= 1
        else:
            idx += 1
    if(rem > 0):
        print("error")
    return sum(plist)/len(plist)

def get_mAP(labeltable,unique_qid):
    n = len(unique_qid)
    allAP = 0
    for i in range(n):
        qid = unique_qid[i]
        labelpd = labeltable[labeltable['question_id'] == qid]
        gtlist = labelpd.index
        query = labelpd.iloc[0]['question']
        inputm = len(gtlist)
        AP = fetch_AP(gtlist,query)
        allAP += AP
    return allAP/n

def get_RatK(labeltable, unique_qid, m):
    n = len(unique_qid)
    allR = 0
    for i in range(n):
        qid = unique_qid[i]
        labelpd = labeltable[labeltable['question_id'] == qid]
        gtlist = labelpd.index
        query = labelpd.iloc[0]['question']
        ret_docs = retrieve_doc(m,query)
        prelist = [item.metadata['row'] for item in ret_docs]
        recall = get_recall(gtlist, prelist)
        allR += recall 
    return allR / n


def get_PatK(labeltable,unique_qid,m):
    n = len(unique_qid)
    allP = 0
    for i in range(n):
        qid = unique_qid[i]
        labelpd = labeltable[labeltable['question_id'] == qid]
        gtlist = labelpd.index
        query = labelpd.iloc[0]['question']
        ret_docs = retrieve_doc(m,query)
        prelist = [item.metadata['row'] for item in ret_docs]
        precision = get_precision(gtlist, prelist)
        allP += precision
    return allP/n
        