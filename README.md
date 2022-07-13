# Reason annotation

## Installation

### Log into quay.io -- required to download the ontoserver

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

### Build the application docker

```
docker build  --no-cache -t readbiomed/mcri_rfv .
```

### Start the application docker

The input and output folders need to be specified.

```
bash start-application-docker.sh $INPUT $OUTPUT
```

### Process data using the application in docker

```
docker exec -it rfv_predict bash process.sh
```

## Data generation - required if data needs to be updated


Download the UMLS Metathesaurus and install, we have tested UMLS 2020AA.
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