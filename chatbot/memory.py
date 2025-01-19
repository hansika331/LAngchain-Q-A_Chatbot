from langchain import HuggingFaceHub

def get_huggingface_response(question: str, api_token: str = None) -> str:
    llm_huggingface = HuggingFaceHub(
        repo_id="google/flan-t5-large",
        model_kwargs={"temperature": 0.7, "max_length": 64},
        huggingfacehub_api_token=api_token
    )
    response = llm_huggingface.invoke(question)
    return response
