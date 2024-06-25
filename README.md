# OV-Compromis

## Project Overview

**OV-Compromis** is an initiative by **Ahmed, Aladin, Hugo, Jean-Baptiste & Clement**, aimed at generating specific summaries from sales agreements. The project employs different technologies including **LLM** (Language Models), **RAG** (Retrieval-Augmented Generation) and the **LangChain** library.

For further information on these principles, refer to the following documentation:


- [Mistral LLM](https://docs.mistral.ai/)
- [Chroma](https://docs.trychroma.com/guides/embeddings)
- [LangChain](https://www.langchain.com/)



## Installation


### VS Code

- **Installation**: Download and install from [Visual Studio Code](https://code.visualstudio.com/).
- **Extensions**: Python, Pylance, Code Runner

### Install Python

For this project, you need at least [Python 3.11](https://www.python.org/downloads/).

### Install Poetry

- **Installation**: Install Poetry by following the instructions on [the Poetry website](https://python-poetry.org/docs/).


## Project Configuration

To install the project on your dedicated VS Code repository, you need to go through the following steps:


- Open a new terminal and execute the following command :


```bash
git clone https://github.com/hugues-04/OV-Project.git 
cd OV-project
```

- Once this is done and you have all the files uploaded in your folder, **create a ".env"** file which you will fill with your mistral keys as follows:

```bash
MIXTRAL_API_BASE= "<your_api_base>"
MIXTRAL_API_KEY= "<your_api_key>"
```

- Then, execute in the terminal shell :

```bash
cd .\Compromis_de_vente\ 
```

```bash
poetry install 
```

- Finally, to visualize the project, run :

```bash
poetry run streamlit run 📋_synthesizer.py 
```

### Project Status

The project is currently in development. <br>
If you have any suggestions, feel free to contact us at jean-baptiste.cheze@openvalue.fr or clement.teulier@openvalue.fr  .<br>
 Good luck!