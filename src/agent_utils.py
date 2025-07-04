from langchain_ollama import ChatOllama
seed = 0
headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }


def load_model():
    model = ChatOllama(
    model="gemma3:12b",
    temperature=0,
    headers=headers,
    options={},
    template="",
    json=True,
    stream=False,
    seed=seed,
)
    return model
