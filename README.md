[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

Insert b-factor values from a text file into a PDB file.

## Usage

The b-factor values need to be specified in a text file using the format
```<chain_id> <seq_id> <bfac>``` like in the following example:

```
A  10  0.1
B  10  0.2
A  88  -5.1
``` 

A copy of the input PDB with the given b-factor values can
the be created using

```insert-bfactor.py -p <input.pdb> -b <bfac_file> -o <output.pdb> -d 1.0```

The flag ```-d``` sets a default value which is applied to residues not
specified in the b-factor file as well as to hetero atoms.

For a detailed explanation of all options call ```insert-bfactor.py -h ```.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE)
file for details.
