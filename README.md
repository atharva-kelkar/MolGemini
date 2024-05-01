# MolGemini

A chat bot that helps you with your protein structure analysis needs.

### Getting started

#### Installing required packages

For running the scripts in this repository, install the following packages

```bash
conda install -c conda-forge google-cloud-platform
conda install -c conda-forge mdtraj mdanalysis
```

#### Registering with Google Cloud

To get started, register on Google Cloud make a Google Cloud Project. You can follow the instructions in [this video](https://www.youtube.com/watch?v=tCpGtGKZKQc)

Once you have the json key downloaded, use the following command to export it as an environment variable

`export GOOGLE_APPLICATION_CREDENTIALS="<path_to_json>"`

### Using MolGemini

You can try out MolGemini simply launch the chat interface using

`python chat_script.py`

### Functionalities

MolGemini interfaces with the Protein Data Bank and uses Gemini's code-writing ability to calculate any property for any protein, given its PDB ID.
