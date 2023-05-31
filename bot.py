# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import os
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

import openai
os.environ["OPENAI_API_BASE"]="https://ai-frameowrk-test-ari-001.openai.azure.com/"
os.environ["OPENAI_API_KEY"]="d81d1f166b8b40dd938530878d12a2f6"
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base= "https://ai-frameowrk-test-ari-001.openai.azure.com/"
openai.api_key="d81d1f166b8b40dd938530878d12a2f6"

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    def __init__(self):
        llm = AzureChatOpenAI(deployment_name="gpt-35-turbo", temperature=0, openai_api_version="2023-03-15-preview")
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", chunk_size=1)
        text_loader_kwargs={'encoding': 'utf-8'}
        loader = DirectoryLoader('./data/qna/', glob="*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
		
        documents = loader.load()
        text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        db = FAISS.from_documents(documents=docs, embedding=embeddings)
        self.qa = RetrievalQA.from_llm(llm=llm,
												   retriever=db.as_retriever(),
												   return_source_documents=True)

	   
	   
    async def on_message_activity(self, turn_context: TurnContext): 
        query = turn_context.activity.text
        result = self.qa({"query": query})
        await turn_context.send_activity(f"{result['result']}")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
