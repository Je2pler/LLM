# Teaching AI to Teach AI – APML Tutor
The aim of this project is to crate a chatbot that can answer questions about the course 1RT705 Advanced Probabilistic Machine Learning at Uppsala university. 

## Table of Contents
 - [Installing](#installing)
 - [Running the Chat Bot](#running-the-chat-bot)
 - [Training the Chat Bot](#training-the-chat-bot)

## Installing
This section will cover steps to install and configure the app as well as downloading the dataset. 

### Acquiring Prerequisites
1. (optional) Create a virtual enviroment by running ``python -m venv .venv`` and activating it. 
   - Windows: ``.venv\Scripts\activate``
   - Linux/MacOS ``.venv/bin/activate``

2. Install all required packages with ``pip install -r requirements.txt``. 

### Adding the gemini API key
Add ``API_KEY`` by creating the file ``.streamlit/secrets.toml`` file and adding the following contents: 
```
[gemini]
api_key="<your API key here>"
```

The API-key can be aquired from [Google AI Studio](https://aistudio.google.com/). 

### Downloading the Vector Datase Contents
The contents of the vector database is too large to fit on git. To add it to your local repository, download [this zip file](https://drive.google.com/file/d/1xQxFR54ikSYHL9si9SfqCWufk0NgsXaV/view?usp=sharing) and copy the ``.db`` directory into the the top directory of your repository. 

It is also possible to generate the database by running the training script, see section [Traing the Chat Bot](#training-the-chat-bot). Note that this is expected to take 1-2 hours with GPU accerlation enabled. 

## Running the Chat Bot
There are several versions of the chatbot:

- RAG and fewshot ``streamlit run rag+fewshot.py``
- fewshot only ``streamlit run fewshot.py``
- RAG only ``steramlit run rag.py``
- Naive model with context ``streamlit run naive+context.py``

## Training the Chat Bot
This secion convers how to extract text and equations from a pdf and encoding the vector database. 

### Downlaoding the Book
The book used was [*Bayesian Reasoning and Machine Learning*](http://web4.cs.ucl.ac.uk/staff/D.Barber/textbook/090310.pdf) by David Barber. Put the file in the top directory and name it ``APML-book.pdf``. 

### Converting the PDF to LaTeX
Since the book contains a lot of equations, *normal* text extraction would not yield satisfactory results. To convert the book into LaTeX, run the python script [``rag_training/pdf2latex.py``](rag_training/pdf2latex.py). 

### Encoding the Vector Database
Provided you've completed the previoud step, run the python script [``rag_training/training.py``](rag_training/training.py). 
