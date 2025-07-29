import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import concurrent.futures
import warnings
import pickle
warnings.filterwarnings('ignore')
import json
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


class P_RAGKnowledgeBase:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(embedding_model_name) #将文本转换为向量表示的模型
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        ) #定义文本分割器
        self.vector_db = None
        self.chunks = []

    def build_from_pdf(self, file_path):
        # PDF提取文本
        text = self._extract_text_from_pdf(file_path)
        # 分割文本块
        self.chunks  = self.text_splitter.split_text(text)
        # 生成嵌入向量
        embeddings = self.embedding_model.encode(self.chunks)
        # 创建向量数据库
        dimension = embeddings.shape[1]
        self.vector_db = faiss.IndexFlatL2(dimension)
        self.vector_db.add(np.array(embeddings).astype('float32'))


    def _extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

class P_RAGRetriever:
    def __init__(self, knowledge_base, openai_client, top_k=3):
        self.knowledge_base = knowledge_base
        self.client = openai_client
        self.top_k = top_k

    def retrieve(self, query):
        # 将查询转换为向量
        query_embedding = self.knowledge_base.embedding_model.encode([query])

        # 在向量数据库中搜索
        distances, indices = self.knowledge_base.vector_db.search(
            np.array(query_embedding).astype('float32'),
            self.top_k
        )

        return indices[0]

class P_chat_to_excel:
    def __init__(self,
                 name,
                 api_key ,
                 base_url):
        self.df = None
        self.api_key = api_key
        self.base_url = base_url
        self.client = OpenAI(
            api_key = api_key,
            base_url= base_url,
        )
        self.model = 'qwen-plus'
        self.name = name
        self.__tomb_directory = 'prompt_tomb'
        if os.path.exists(rf'prompt_tomb\{name}_tomb.pkl'):
            with open(rf'prompt_tomb\{name}_tomb.pkl', 'rb') as f:
                self.prompt = pickle.load(f)
        else:
            self.prompt = ''

    def excel_info(self,path,column):
        df = pd.read_excel(path)
        df_filter = df.filter(column)
        self.df = df_filter

    def data_parsing(self,column,truncate_word = '为您服务'):
        list_total = []
        self.df[column] = self.df[column].str.replace('excel单元格限制长度可能有截取：','')
        for x in self.df[column].tolist():
            trigger = False
            try:
                list_context = []
                for i in json.loads(x):
                    if not trigger:
                        if i['text'].find(truncate_word) > -1 and i['text'].find('为了更好') == -1:
                            trigger = True
                            dict_ = {}
                            dict_['role'] = i['role']
                            dict_['text'] = i['text']
                            list_context.append(dict_)
                        else:
                            pass
                    else:
                        dict_ = {}
                        dict_['role'] = i['role']
                        dict_['text'] = i['text']
                        list_context.append(dict_)
                list_total.append(list_context)
            except:
                list_total.append({})
        self.df[column] = list_total
        self.df = self.df[self.df[column] != '[]']
        print('解析完成')

    def concat(self,column):
        for i in column:
            self.df[f'column{i}'] = i + '：' + self.df[i]
        columns_to_combine = self.df.filter(regex='^column').columns
        self.df['combined'] = self.df[columns_to_combine].agg('；'.join, axis=1)
        self.df = self.df.drop(columns=columns_to_combine)

    def __save_to_hell(self):
        os.makedirs(self.__tomb_directory, exist_ok=True)
        with open(rf'prompt_tomb\{self.name}_tomb.pkl', 'wb') as f:
            pickle.dump(self.prompt, f)

    def data_sample(self,num):
        df_sample = self.df.sample(num)
        self.df_sample = df_sample
        print(f'已随机抽取{num}行，请调用df_sample属性查看')

    def info_collect(self,param = None):
        if param:
            if hasattr(self, param):
                replace = input(f'{param}:')
                setattr(self, param, replace)
            else:
                print(f'类中没有名为 {param} 的属性。')
        else:
            if len(self.prompt) == 0 :
                self.prompt = input('prompt（AI的人设）:\n')
            self.inquiry = input('inquiry（询问的内容）：\n')
            self.column = input('column（表格中的目标字段）：\n')
            self.result_column_name = input('result_column_name（结果字段的名称）：\n')
            self.file_path = input('file_path（结果保存到本地的地址）：\n')
        self.__save_to_hell()

    @property
    def prompt(self,str):
       self.prompt = str
       self.__save_to_hell()

    def __chat_single(self,sample = False,temperature = 0.7,top_p = 0.9,frequency_penalty=0.2,kb=None,top_k=3):
        self.kb = kb
        def chat_prepare(i):
            result = []
            input = f'这有一段文本：{i}。{self.inquiry}。'
            try:
                retriever = P_RAGRetriever(self.kb, self.client, top_k)
                relevant_indices = retriever.retrieve(input)
                # 获取相关文本块（需要保存文本块引用）
                context = "\n".join([kb.chunks[i] for i in relevant_indices])
                self.prompt += f'''# 知识库 请记住以下材料，他们可能对回答问题有帮助。{context}'''
            except:
                pass
            completion = self.client.chat.completions.create(
                model= self.model,
                messages=[
                    {'role': 'system', 'content': f'{self.prompt}'},
                    {'role': 'user', 'content': input}],
                temperature = temperature,
                top_p = top_p,
                frequency_penalty = frequency_penalty
            )
            reply = completion.choices[0].message.content
            result.append(reply)
            return result[0]
        if not sample:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(tqdm(executor.map(chat_prepare, self.df[self.column]), total=len(self.df[self.column])))
                self.results = results
            self.df[self.result_column_name] = results
            self.df.to_excel(self.file_path,index = False)
            print('done')
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(tqdm(executor.map(chat_prepare, self.df_sample[self.column]), total=len(self.df_sample[self.column])))
                self.results = results
            self.df_sample[self.result_column_name] = results
            self.df_sample.to_excel(self.file_path,index = False)
            print('done')

    def __chat_multiple(self,axis = 1,sample = False,temperature = 0.7,top_p = 0.9,frequency_penalty=0.2,kb=None,top_k=3):
        self.kb = kb
        columns = self.df.columns
        def chat_prepare(i):
            result = []
            input = f'这有一段文本：{i}。{self.inquiry}。'
            try:
                retriever = P_RAGRetriever(self.kb, self.client, top_k)
                relevant_indices = retriever.retrieve(input)
                # 获取相关文本块（需要保存文本块引用）
                context = "\n".join([kb.chunks[i] for i in relevant_indices])
                self.prompt += f'''# 知识库 请记住以下材料，他们可能对回答问题有帮助。{context}'''
            except:
                pass
            completion = self.client.chat.completions.create(
                model= self.model,
                messages=[
                    {'role': 'system', 'content': self.prompt},
                    {'role': 'user', 'content': input}],
                temperature = temperature,
                top_p = top_p,
                frequency_penalty = frequency_penalty
            )
            reply = completion.choices[0].message.content
            result.append(reply)
            return result[0]
        if axis == 1:
            for target_column in tqdm(columns):
                self.target_column = target_column
                if not sample:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(tqdm(executor.map(chat_prepare, self.df[self.target_column]), total=len(self.df[self.target_column])))
                        self.results = results
                    target_index = self.df.columns.get_loc(target_column)
                    self.df.insert(target_index + 1, f'{target_column}-{self.result_column_name}', results)
                    self.df.to_excel(self.file_path,index = False)
                    print('done')
                else:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(tqdm(executor.map(chat_prepare, self.df_sample[self.target_column]), total=len(self.df_sample[self.target_column])))
                        self.results = results
                    target_index = self.df_sample.columns.get_loc(target_column)
                    self.df_sample.insert(target_index + 1, f'{target_column}-{self.result_column_name}', results)
                    self.df_sample.to_excel(self.file_path,index = False)
                    print('done')
        else:
            self.results = []
            column_content = []
            for target_column in tqdm(columns):
                self.target_column = target_column
                if not sample:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(tqdm(executor.map(chat_prepare, self.df[self.target_column]), total=len(self.df[self.target_column])))
                        self.results.extend(results)
                    column_content.extend([target_column]*len(self.df[self.target_column]))
                else:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(tqdm(executor.map(chat_prepare, self.df_sample[self.target_column]), total=len(self.df_sample[self.target_column])))
                        self.results.extend(results)
                    column_content.extend([target_column]*len(self.df_sample[self.target_column]))
            pd.DataFrame({'目标内容':column_content,self.result_column_name: self.results}).to_excel(self.file_path,index = False)
            print('done')

    def chat(self,sample=False,axis=None,temperature = 0.7,top_p = 0.9,frequency_penalty=0.2,kb=None,top_k=3):
        if axis:
            self.__chat_multiple(axis = axis,sample = sample,temperature = temperature,top_p = top_p,frequency_penalty = frequency_penalty,kb = kb,top_k = top_k)
        else:
            self.__chat_single(sample = sample,temperature = temperature,top_p = top_p,frequency_penalty = frequency_penalty,kb = kb,top_k = top_k)





