from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

def qa_prompt():
    
    template = ChatPromptTemplate.from_messages([
        ("system", "Answer ONLY using the provided context. Do not hallucinate."),
        ("system", "If the context is not relevant, say: 'Information not found.'"),
        ("system", "Context:\n{related_context}"),
        ("human", "{question}")
    ])
    return template

def fallback_prompt():
    template = """
           Instruction:
              If the answer cannot be found in the provided documents,
              respond with the fallback message.

           Question:
             {question}

           Answer:
                The requested information is not available in the provided documents.
                Please ask a question related to the uploaded documents."""
    fallback_template = PromptTemplate.from_template(template)
    return fallback_template

def router_prompt():
    template = """
          You are a classifier.

          Your task is to classify the user question into one of two categories:

          1. POLICY → Questions related to company rules, HR policies, employee guidelines, leave, probation, workplace rules, etc.
          2. GENERAL → Questions about general knowledge, programming, AI, or anything not related to company documents.

          Rules:
            - Return ONLY one word: POLICY or GENERAL
            - Do NOT explain your answer

          Examples:

            Question: What is leave policy?
            Answer: POLICY

            Question: What is probation period?
            Answer: POLICY

            Question: What is Python?
            Answer: GENERAL

            Question: Explain artificial intelligence
            Answer: GENERAL

            Now classify:
            conversation history: {chat_history}
            Question: {question}
            Answer:"""
    router_template = PromptTemplate.from_template(template)
    return router_template
    
def llm_prompt():
    template = """
        You are a helpful assistant.Answer the user question clearly and concisely.If the question is unrelated to company policies, answaer normally from general knowledge.
        conversation history: {chat_history}
        Question:
        {question}
        Answer:
        """
    llm_template = PromptTemplate.from_template(template)
    return llm_template
        
    