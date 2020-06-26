# DocEmul
A Toolkit to Generate Structured Historical Documents
(This repository is still under construction. Please let us know if you find any issues...)
##
This toolkit is presented in the paper "DocEmul: a Toolkit to Generate Structured Historical Documents" (https://arxiv.org/abs/1710.03474) in  Proceedings of the 14th International Conference on Document Analysis and Recognition (ICDAR), 2017.
It has been proposed to generate structured synthetic documents emulating the actual document production process. Synthetic documents can be used to train systems to perform document analysis tasks. The toolkit is able to generate synthetic collections and also perform data augmentation to create a larger trainable dataset. It includes one method to extract the page background from real pages which can be used as a substrate where records can be written on the basis of variable structures and using cursive fonts. Moreover, it is possible to extend the synthetic collection by adding random noise, page rotations, and other visual variations.
In the experiments we address the record counting task on handwritten structured collections containing a limited number of examples. More detailed experiments and results for the record counting task are presented in the paper "Deep neural networks for record counting in historical handwritten documents" (https://doi.org/10.1016/j.patrec.2017.10.023
) published on Pattern Recognition Letters journal.

Please, contact us if you want to collaborate to our project in order to extend the software capability. 
In the future works we will add also a structural ground truth to train a model for record detection. 
Keep in touch to help us in this tasks.

## Data repo
It is possible to find more data at a dropbox link (https://www.dropbox.com/sh/gx93qumgbvp2ipe/AABUbsexdJg-GuyJbRbNXGdsa?dl=0). In this `<repo>` there are some generated examples by using the proposed toolkit. In particular, there are examples from two collection used in the experiments.
in `<repo>/Data` you can find some generated files for two different datasets (Esposalles, Brandenburg). In particular, you can find the extracted background (`<repo>/Data/<dataset>/Background.zip`) used to generate synthetic files; the generated text files over a transparent background (`<repo>/Data/<dataset>/Text`); the genereted synthetic documents (`<repo>/Data/<dataset>/Generated`).

## Repository description

### Document structure
There are several XML files to describe the document structure. This files are used also in the experiments proposed in the research.

### Text data
In the text files there are the data used to write text during the production process.

### Fonts
Before to start the generation process, you need to download from `http://www.dafont.com/` the used fonts for the experiments.
Run the script `python download_font.py` which creates the directory `handwritten`. Here you can find some fonts downloaded from `http://www.dafont.com/` and used to generate the synthetic data for the experiments.

# Generation process

## Pre-requisites
- Python 3
- `pip install -r py-requirements.txt`

## Esposalles
It is possible to emulate the generation of documents for the dataset Esposalles.

### Download background images
Run the script to download images from our repository.

`sh Data/Esposalles/download_extract_background_files.sh`

After that, you can find some background images into `Data/Esposalles/Background`

### Generate synthetic pages
Run the script to generate some synthetic image with data augmentation using:

`python generate_esposalles_images.py`

Try to modify the script to generate more pages.

If you need more instructions to define the document structure, please, contact us and we will glad to help you..

## Brandenburg
It is possible to emulate the generation of documents for the dataset Brandenburg. Running the script `python test_generate_brandenburg.py` it will be possible to generate documents following the Brandenburg model (`branden2.xml`). It will build the synthetic dataset (only text over a transparent background)  into the local directory `GENERATED/Brandenburg/test`.

# Citing DocEmul

If you find DocEmul useful in your research, please consider citing:

@article{CAPOBIANCO2017,
title = "Deep neural networks for record counting in historical handwritten documents",
journal = "Pattern Recognition Letters",
year = "2017",
issn = "0167-8655",
doi = "https://doi.org/10.1016/j.patrec.2017.10.023",
url = "http://www.sciencedirect.com/science/article/pii/S0167865517303914",
author = "Samuele Capobianco and Simone Marinai",
keywords = "Handwritten documents, Convolutional neural networks, Synthetic document generation, Record counting"
}
