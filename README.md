# Create a matrix with the closest concept category using a set of predefined categories

## Installation

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