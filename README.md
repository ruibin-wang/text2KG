# text2KG


This project tends to build a pipeline for converting free text to a knowledge graph. There are three parts to this project: entity extraction, relationship extraction and graph construction.


* For the entity and relation extraction part, we use the OpenIE Java package, the details will be shown as follows.

* For building a knowledge graph we choose the Neo4j to provide visual and efficient data management.



## Build the OpenIE server

1. clone the OpenIE project to the local file
    ```
    git clone git@github.com:dair-iitd/OpenIE-standalone.git
    ```

2. follow the instruction of the Readme.md file to build the environment.

    * download the standalone jar for BONIE from [here](https://github.com/dair-iitd/OpenIE-standalone/releases/download/v5.0/BONIE.jar) and place it inside a `lib` folder(create the `lib` folder parallel to the `src` folder).

    * download the standalone jar for CALMIE from [here](https://github.com/dair-iitd/OpenIE-standalone/releases/download/v5.0/ListExtractor.jar) and place it inside the `lib` folder.

    * Download the Language Model file from [here](https://drive.google.com/file/d/0B-5EkZMOlIt2cFdjYUJZdGxSREU/view?usp=sharing&resourcekey=0-X_oNJ6r24s_anMGbKKRdQw) and place it inside a data folder(create the `data` folder parallel to the `src` folder)

    * `openie` uses java-8-openjdk, just use conda to install Java package in the environment.

    ```
    conda install -c "bioconda/label/cf201901" java-jdk
    ```

3. Running as HTTP Server

    **Notice: keep the server running in the background.**

    OpenIE 5.1 can be run as a server. For this, server port is required as an argument.
    ```
    java -jar openie-assembly.jar --httpPort 8000
    ```
        
    To run the server with memory options.
    ```
    java -Xmx10g -XX:+UseConcMarkSweepGC -jar openie-assembly.jar --httpPort 8000
    ```
        
    To get an extraction from the server use the POST request on '/getExtraction' address. The sentence will go in the body of HTTP request. An example of curl request.
    ```
    curl -X POST http://localhost:8000/getExtraction -d 'The U.S. president Barack Obama gave his speech on Tuesday to thousands of people.'
    ```
    The response is a JSON list of extractions.

## Create the virtual environment

* create the virtual environment on the server

```python
conda create --name text2KG python=3.8
pip install pyopenie
conda install -c "bioconda/label/cf201901" java-jdk
```

* create the virtual environment on the local pc
```python
conda create --name text2KG python=3.8
pip install paramiko
pip install py2neo
pip install neo4jupyter
```


## Build the knowledge graph

* This project used Neo4j to provide visual and efficient data management.

* First, create a project in the local path with Neo4j, and remember the host address and password. 

* Open the project in a new browser

* Run the code 
    ```
    python test_demo.py
    ```

## Notice:

1. This java package and model are huge, you need to run it on a server with ample storage.

2. Run the HTTP server first, then create the virtual environment


## Examples

1. Case1 - normal test

    text = "Jack and Jill visited India, Japan and South Korea."

    output = List(0.88 (Jill; visited; South Korea), 0.88 (Jill; visited; Japan), 0.88 (Jill; visited; India), 0.88 (Jack; visited; South Korea), 0.88 (Jack; visited; Japan), 0.88 (Jack; visited; India))

    * knowledge graph picture

    <center class="half">
    <img src=./picture/Figure1.png width = 70%>
    </center>

2. Case2 - normal test

    text = "Jack visited India, Japan and South Korea, but Jill only visited India and China"

    output = List(0.86 (Jill; visited; China), 0.86 (Jill; visited; India), 0.88 (Jack; visited; South Korea), 0.88 (Jack; visited; Japan), 0.88 (Jack; visited; India))

    * knowledge graph picture

    <center class="half">
    <img src=./picture/Figure2.png width = 70%>
    </center>


3. Case3 - normal test

    text = "Jack visited India, Japan and South Korea, but Jill did not visit Japan, he visited India and China"

    output = List(0.85 Context(he visited,List([21, 31))):(Jack; visited; Japan), 0.85 Context(he visited,List([27, 37))):(Jack; visited; South Korea), 0.88 (Jack; visited; Japan), 0.85 Context(he visited,List([21, 31))):(Jack; visited; India), 0.44 (he; visited; China), 0.85 Context(he visited,List([27, 37))):(Jill; did not visit; Japan), 0.44 (he; visited; India))


    * knowledge graph picture

    <center class="half">
    <img src=./picture/Figure3.png width = 70%>
    </center>


    We can see two points which need to be improved from the picture, 
    
    * this model can not firgure out the negative word and treats the words "did not visit" as a relationship.

    * this model can not map "he" to the subject "Jill".















