# DocEmul
A Toolkit to Generate Structured Historical Documents

# Repository description 
In EXAMPLES you can find some generated files for two different datasets (Esposalles, Brandenburg). In particular, you can find the extracted background (BACKGROUND), the generated text files over a transparent background (TEXT) and genereted structured documents (GENERATED) 


## Esposalles
It is possible to emulate the generation of documents for the dataset Esposalles. Running the script test_generate_esposalles.py it will be possible to generate documents following the Esposalles model. It will build the synthetic dataset into the local directory "GENERATED/Esposalles/test". After that, it will augment the generated dataset with some data augmentation techiniques into the local directory "GENERATED/Esposalles/test_augmented".

## Brandenburg
It is possible to emulate the generation of documents for the dataset Esposalles. Running the script test_generate_brandenburg.py it will be possible to generate documents following the Brandenburg model (branden2.xml). It will build the synthetic dataset (only text over a transparent background)  into the local directory "GENERATED/Brandenburg/test".
