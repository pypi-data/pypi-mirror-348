# XSD2RDF

[![License](https://img.shields.io/badge/license-EUPL_1.2-blue)](http://data.europa.eu/eli/dec_impl/2017/863/oj)

A tool to convert XML Schema (XSD) files into various RDF formats (SHACL, OWL, SKOS) with integrated validation capabilities.

## Overview

XSD2RDF allows you to convert XML Schema definitions into:

- **SHACL** (Shapes Constraint Language) for RDF data validation
- **OWL** (Web Ontology Language) for ontology representation
- **SKOS** (Simple Knowledge Organization System) for concept schemes and taxonomies

## Features

- Convert XSD to SHACL, OWL, and SKOS based on integrated principles
- SHACL shape constraints are linked to SKOS concept schemes when applicable
- Handle complex XSD structures (choices, unions, complex types, enumerations, etc.)
- SHACL shapes are validated according to SHACL-SHACL

This repository also includes a validation script to check RDF data against the generated SHACL shapes and SKOS concepts.

## Installation

### From PyPI

```bash
pip install xsd2rdf
```

### From Source

```bash
git clone https://github.com/YourUsername/xsd2rdf.git
cd xsd2rdf
python -m pip install poetry
poetry install
```

## Basic Usage

Convert an XSD file to all RDF formats (SHACL, OWL, SKOS):

```bash
python -m xsd2rdf -x path/to/schema.xsd
```

This generates the following files:

- `schema.xsd.shape.ttl` (SHACL shapes)
- `schema.xsd.owl.ttl` (OWL ontology)
- `schema.xsd.*.skos.ttl` (SKOS concept schemes, one file per enumeration)

With custom output directory:

```bash
python -m xsd2rdf  -x path/to/schema.xsd -o output/directory
```

Using a custom abbreviations file:

```bash
python -m xsd2rdf -x path/to/schema.xsd -a path/to/abbreviations.txt
```

The abbreviations file should contain one abbreviation per line. These abbreviations will be preserved as uppercase when creating human-readable labels from camelCase or PascalCase strings.

## Validation

This feature is only available from source as it is meant for development purposes.

Prerequisites:

- Create sample data for validation `schema.xsd.shape.ttl` in the same directory as the xsd file

To validate RDF data against SHACL shapes with SKOS concepts:

```bash
python shacl-validation.py path/to/schema.xsd
```

This will:

1. Load the data from `schema.xsd.sample.ttl`
2. Include all related SKOS files (`schema.xsd.*.skos.ttl`)
3. Perform validation using the generated SHACL shapes (`schema.xsd.shape.ttl`)
4. Report results in the command line

## Example

Converting an XSD file with enumerations:

```bash
python -m xsd2rdf xsd2rdf -x comparison/enumerations.xsd
```

Validating data using generated shapes and concepts:

```bash
python shacl-validation.py comparison/enumerations.xsd
```

## License

EUPL 1.2
