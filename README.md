# Create a matrix with the closest concept category using a set of predefined categories

## Installation

### Set up the network

```
docker network create  --driver=bridge   --subnet=100.100.0.0/16   --gateway=100.100.0.1  rfv_ontoserver
```

### Ontoserver

Start the ontoserver docker

```
docker-compose up -d -f docker-compose-ontoserver.yml
```

Update the SNOMED CT ontology

```
docker exec ontoserver /index.sh -s sctau
```

### Application docker

### Start the application docker


```

```

### Process the data

docker exec -it rfv_predict bash start.sh

## Data generation - only required to regenerate the data

```bash

Download the UMLS Metathesaurus and install.
When installing the UMLS, you need to ensure that SNOMED CT is installed.

```
pip install jsonpickle
```

Clone the repository.

Set the folders for the UMLS files MRCONSO and MRREL

## Creating the mapping category data structure

### Create a catalogue of SNOMED CT concepts

```
python catalogue.py
```

### Create a graph of the hierarchy of SNOMED CT concepts

```
python hierarchy.py
```

### Create the mapping between SNOMED CT concepts and categories

Update the file path that contains the information about the categories.

Run

```
python ancestor.py
```

### Test

It is possible to test the data sets against Ontoserver output

```
python predict.py
```

It is possible to annotate a CSV file and generate a prediction Excel file running

```
python process.py
```