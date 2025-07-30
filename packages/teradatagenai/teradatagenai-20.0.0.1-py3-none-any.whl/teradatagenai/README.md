## Teradata Package for Generative-AI

`teradatagenai` is a Generative AI package developed by Teradata.
It offers a comprehensive suite of APIs designed for a wide range of text analytics applications 
and seamless access to the Enterprise Vector Store.
With `teradatagenai`, users can seamlessly process and analyze text data from various sources,
including emails, academic papers, social media posts, and product reviews.
This enables users to gain insights with precision and depth that rival or surpass human analysis.

For community support, please visit the [Teradata Community](https://support.teradata.com/community?id=community_forum&sys_id=14fe131e1bf7f304682ca8233a4bcb1d).

For Teradata customer support, please visit [Teradata Support](https://support.teradata.com/csm).

Copyright 2025, Teradata. All Rights Reserved.

### Table of Contents
* [Documentation](#documentation)
* [Release Notes](#release-notes)
* [Installation and Requirements](#installation-and-requirements)
* [Using the Teradata Python Package for Generative AI](#using-the-teradata-python-package-for-generative-ai)
* [License](#license)

## Documentation
General product information, including installation instructions, is available in the [Teradata Documentation website](https://docs.teradata.com/search/documents?query=Python+package+for+Generative-AI&sort=last_update&virtual-field=title_only&content-lang=en-US).

## Release Notes
### Version 20.00.00.01
* ##### New Features/Functionality
  * ##### Vector Store
    * Teradata Enterprise Vector Store is designed to store, index, and search high-dimensional vector embeddings efficiently.
    * `teradatagenai` provides the below python APIs to easily access and manage vector store and build their own NL applications using Vantage as the foundational compute/storage engine.
      * The following operations can be done:        
        * `VSManager`: Contains methods to manage vector Store.
          * `health`: Perform health check for the vector store service.
          * `list`: List all the vector stores.
          * `list_sessions`: List all the active sessions of the vector store service.
          * `disconnect`: Disconnect from the database session.
          * `list_patterns`: List all available patterns for creating metadata-based vector store.
        * `VectorStore`: Contains methods to do operations on Vector Store.
          * `create`: Creates a Vector Store.
          * `update`: Updates a Vector Store.
          * `destroy`: Destorys a Vector Store.
          * `similarity_search`: Performs similarity search in interactive/batch mode in the Vector Store for the input question
          * `prepare_response`: Prepare a natural language response to the user using the input question and similarity_results provided by VectorStore.similarity_search() method using interactive/batch mode.
          * `ask`: Performs similarity search in the vector store for the input question followed by preparing a natural language response to the user using interactive/batch mode.
          * `get_details`: Get details of the vector store.
          * `get_objects`: Get the list of objects in the metadata-based vector store.
          * `get_batch_results`: Retrieves the results when `similarity_search`, `prepare_response` and `ask` is triggered in batch mode.
          * `status`: Checks the status of the below operations: `create`, `destroy` and `update`.
        * `VSPattern`: Create/Manage patterns which provides a way to select tables/views and columns using simple regular expressions which can be used while creating metadata-based Vector Store.
          * Following operations are supported:
            * `create`: Creates a pattern by specifying the `pattern_string`.
            * `get`: Gets the list of objects that matches the `pattern_string`.
            * `delete`: Deletes the pattern.
  * ##### InDb TextAnalytics Functions
    * This version supports the integration of TextAnalyticsAI InDB functions, enabling seamless access to  LLM services like AWS Bedrock, Azure OpenAI, Google Gemini for a wide array of text analytics tasks, including:
      * KeyPhrase Extraction
      * PII (Personally Identifiable Information) Entity Recognition
      * Masking PII Information
      * Language Detection
      * Language Translation
      * Text Summarization
      * Entity Recognition
      * Sentiment Analysis 
      * Text Classification 
      * Text Embeddings 
      * Asking LLM

### Version 20.00.00.00
* `teradatagenai 20.00.00.00` marks the first release of the package.
* This version supports the integration of Hugging Face models into Teradata Vantage through the BYO LLM offering, enabling seamless utilization of these models for a wide array of text analytics tasks.
    * KeyPhrase Extraction
    * PII (Personally Identifiable Information) Entity Recognition
    * Masking PII Information
    * Language Detection
    * Language Translation
    * Text Summarization
    * Entity Recognition
    * Sentiment Analysis 
    * Text Classification 
    * Text Embeddings 
    * Sentence Similarity
* The package also features a versatile `task` function capable of performing any task supported by the underlying language model (LLM). This function is highly adaptable and can be customized to meet specific requirements. Refer to the [example](#get-embeddings-and-similarity-score-for-employee-data-and-articles) for more details on its usage.

## Installation and Requirements
### Package Requirements:
* Python 3.9 or later

Note: 32-bit Python is not supported.

### Minimum System Requirements:
* Windows 7 (64Bit) or later
* macOS 10.9 (64Bit) or later
* Red Hat 7 or later versions
* Ubuntu 16.04 or later versions
* CentOS 7 or later versions
* SLES 12 or later versions
* VantageCloud Lake on AWS with Open Analytics Framework in order to use Teradata’s BYO LLM offering.
### Minimum Database Requirements
* Teradata Vantage with database release 20.00 or later 

### Installation

Use pip to install the Teradata Python Package for Generative AI

Platform       | Command
-------------- | ---
macOS/Linux    | `pip install teradatagenai`
Windows        | `python -m pip install teradatagenai`

When upgrading to a new version of the `teradatagenai`, you may need to use pip install's `--no-cache-dir` option to force the download of the new version.

Platform       | Command
-------------- | ---
macOS/Linux    | `pip install --no-cache-dir -U teradatagenai`
Windows        | `python -m pip install --no-cache-dir -U teradatagenai`

## Using the Teradata Python Package for Generative AI:

Your Python script must import the `teradatagenai` package in order to use the Teradata Python Package for Generative AI. Let us walkthrough some examples to gain a better understanding. We need a common setup to load the data and import the required packages.

### Common Setup

```python
# Import the modules and create a teradataml DataFrame.
import os
import teradatagenai
from teradatagenai import TeradataAI, TextAnalyticsAI, load_data
from teradataml import DataFrame

load_data('employee', 'employee_data')
data = DataFrame('employee_data')
df_reviews = data.select(["employee_id", "employee_name", "reviews"])
df_articles = data.select(["employee_id", "employee_name", "articles"])

# Define the base directory and script path.
base_dir = os.path.dirname(teradatagenai.__file__)
sentence_similarity_script = os.path.join(base_dir, 'example-data', 'sentence_similarity.py')
```

### Analyze Sentiment of Food Reviews

In this example, we will be using the `analyze_sentiment` API to analyze the sentiment of food reviews in the `reviews` column of a `teradataml` DataFrame.

#### Using the Hugging Face model `distilbert-base-uncased-emotion`. 

```python
# Define the model name and arguments for the Hugging Face model.
model_name = 'bhadresh-savani/distilbert-base-uncased-emotion'
model_args = {
    'transformer_class': 'AutoModelForSequenceClassification',
    'task': 'text-classification'
}

# Create a TeradataAI object with the specified model.
llm = TeradataAI(api_type="hugging_face", model_name=model_name, model_args=model_args)
```

```python
# Create a TextAnalyticsAI object.
obj = TextAnalyticsAI(llm=llm)
obj.analyze_sentiment(column='reviews', data=df_reviews, delimiter="#")
```
#### Using AWS Bedrock model `anthropic.claude-v2`.

```python
# Define AWS Bedrock environment variables.
os.environ["AWS_DEFAULT_REGION"] = "<Enter AWS Region>"
os.environ["AWS_ACCESS_KEY_ID"] = "<Enter AWS Access Key ID>"
os.environ["AWS_SECRET_ACCESS_KEY"] = "<Enter AWS Secret Key>"
os.environ["AWS_SESSION_TOKEN"] = "<Enter AWS Session key>"

# Create a TeradataAI object with the specified model.
llm = TeradataAI(api_type="aws", model_name="anthropic.claude-v2")
```

```python
# Create a TextAnalyticsAI object.
obj = TextAnalyticsAI(llm=llm)
obj.analyze_sentiment(column='reviews', data=df_reviews, accumulate="reviews")
```
#### Using Azure OpenAI model `gpt-3.5-turbo`.

```python
# Define Azure OpenAI environment variables.
os.environ["AZURE_OPENAI_API_KEY"] = "<azure OpenAI API key>"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://****.openai.azure.com/"
os.environ["AZURE_OPENAI_API_VERSION"] = "2000-11-35"
os.environ["AZURE_OPENAI_DEPLOYMENT_ID"] = "<azure OpenAI engine name>"

# Create a TeradataAI object with the specified model.
llm = TeradataAI(api_type="azure", model_name="gpt-3.5-turbo")
```

```python
# Create a TextAnalyticsAI object.
obj = TextAnalyticsAI(llm=llm)
obj.analyze_sentiment(column='reviews', data=df_reviews, accumulate="reviews")
```
#### Using Google model `gemini-1.5-pro-001`.

```python
# Define Google Cloud environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "<gcp access token>"
os.environ["GOOGLE_CLOUD_PROJECT"] = "<gcp project name>"
os.environ["GOOGLE_CLOUD_REGION"] = "us-central1"

# Create a TeradataAI object with the specified model.
llm = TeradataAI(api_type="gcp", model_name="gemini-1.5-pro-001")
```

```python
# Create a TextAnalyticsAI object.
obj = TextAnalyticsAI(llm=llm)
obj.analyze_sentiment(column='reviews', data=df_reviews, accumulate="reviews")
```

### Get Embeddings and Similarity Score for Employee Data and Articles

In this example, we will use the `task` API to perform two tasks: generating embeddings and calculating similarity scores using the Hugging Face model `all-MiniLM-L6-v2`.

#### Generate Embeddings for Employee Reviews

We will generate embeddings for employee reviews from the `articles` column of a `teradataml` DataFrame using the Hugging Face model `all-MiniLM-L6-v2`.

```python
# Define the script path for embeddings.
embeddings_script = os.path.join(base_dir, 'example-data', 'embeddings.py')

# Construct the returns argument based on the user script.
returns = OrderedDict([('text', VARCHAR(512))])
_ = [returns.update({"v{}".format(i+1): VARCHAR(1000)}) for i in range(384)]

# Use the task API to generate embeddings.
llm.task(
    column="articles",
    data=df_articles,
    script=embeddings_script,
    returns=returns,
    libs='sentence_transformers',
    delimiter='#'
)
```

#### Calculate Similarity Score

We will calculate the similarity score between employee data and articles using the Hugging Face model `all-MiniLM-L6-v2`.

```python
# Define the model name and arguments for the Hugging Face model.
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model_args = {
    'transformer_class': 'AutoModelForSequenceClassification',
    'task': 'text-similarity'
}

# Create a TeradataAI object with the specified model.
llm = TeradataAI(api_type="hugging_face", model_name=model_name, model_args=model_args)

# Use the task API to get the similarity score.
llm.task(
    column=["employee_data", "articles"],
    data=data,
    script=sentence_similarity_script,
    libs='sentence_transformers',
    returns={
        "column1": "VARCHAR(10000)",
        "column2": "VARCHAR(10000)",
        "similarity_score": "VARCHAR(10000)"
    },
    delimiter="#"
)
```

## License
Use of the Teradata Python package for Generative-AI is governed by the *License Agreement for the Teradata Python package for Generative-AI*. 
After installation, the `LICENSE` and `LICENSE-3RD-PARTY.pdf` files are located in the `teradatagenai` directory of the Python installation directory.
