# DocEmul
A Toolkit to Generate Structured Historical Documents
(This repository is still under construction. Please let us know if you find any issues...)

# Repository description 
In this dropbox link (https://www.dropbox.com/sh/2bxfeacrg6s19rj/AADzyLlNUoj91W1eKSBfWJ1Ya?dl=0) it is possible to access to all data. Please create a local dir DATA and download all data from the in the local dir DATA.

After the downloading, in DATA you can find some generated files for two different datasets (Esposalles, Brandenburg). In particular, you can find the extracted background (BACKGROUND), the generated text files over a transparent background (TEXT) and genereted structured documents (GENERATED) 
### handwritten
In this directory you can find some fonts downloaded from http://www.dafont.com/it/


## Esposalles
It is possible to emulate the generation of documents for the dataset Esposalles. Running the script test_generate_esposalles.py it will be possible to generate documents following the Esposalles model. It will build the synthetic dataset into the local directory "GENERATED/Esposalles/test". After that, it will augment the generated dataset with some data augmentation techiniques into the local directory "GENERATED/Esposalles/test_augmented".

## Brandenburg
It is possible to emulate the generation of documents for the dataset Esposalles. Running the script test_generate_brandenburg.py it will be possible to generate documents following the Brandenburg model (branden2.xml). It will build the synthetic dataset (only text over a transparent background)  into the local directory "GENERATED/Brandenburg/test".
