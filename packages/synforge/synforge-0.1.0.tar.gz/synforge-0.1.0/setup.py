from setuptools import setup, find_packages

setup(
    name="synforge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.1",
        "typing-extensions==4.12.2",
        "pydantic==2.10.6",
        "openai==1.63.2",
        "google-genai==1.2.0",
        "ipykernel==6.29.5",
        "langchain>=0.3.20",
        "langchain-community>=0.3.20",
        "langgraph==0.2.74",
        "pypdf==5.3.0",
        "faiss-cpu==1.10.0",
        "rank-bm25==0.2.2",
        "rich==13.9.4",
        "langchain-docling"
    ],
) 