#!/usr/bin/env python3
"""Insert b-factor values into a PDB file.

b-factor values need to be provided in a file with respective chain ID and
sequence ID. A copy of the PDB file containing the b-factor values is written
out.
"""

import argparse
import collections


def get_parser():
    """"Return a command line parser for this script."""
    parser = argparse.ArgumentParser(
        description="This script inserts provided b-factor values into a copy "
        "of a provided PDB file.")
    parser.add_argument(
        "-p",
        "--pdb",
        dest="pdb_file",
        required=True,
        help="The PDB file to which the b-factor values are added. This file "
        "won\'t be altered by this script.")
    parser.add_argument(
        "-b",
        "--b_factors",
        dest="b_factors_file",
        required=True,
        help="A file containing the b-factor values that are added to the PDB "
        "file. The file format is expected as <chain_id> <sequence_id> "
        "<b-factor>.")
    parser.add_argument(
        "-o",
        "--output_file",
        dest="output_file",
        required=True,
        help="The output PDB file produced by this script. It will be "
        "identical to the input PDB file but will contain the provided "
        "b-factor values.")
    parser.add_argument(
        "-d",
        "--default_value",
        dest="default_value",
        type=float,
        default="NaN",
        help="The default b-factor value used for residues with no b-factor "
        "value provided.")

    return parser


def create_bfac_dict(bfactor_file_name):
    """Return a dictionary mapping b-factor values to chain and sequence IDs.

    Keyword arguments:
    bfactor_file_name -- The path to the file containing the b-factor values.
    """
    # Initialize the dictionary, which is a dictionary of dictionaries.
    bfac_dict = collections.defaultdict(dict)

    # Parse the b-factors file and map b-factors to chain and sequence IDs.
    with open(bfactor_file_name) as bfac_file:
        # Filter out blank lines.
        lines = filter(None, (line.rstrip() for line in bfac_file))

        for line in lines:
            line = line.split()
            chain_id = line[0]
            seq_id = line[1]
            bfac = float(line[2])
            bfac_dict[chain_id][seq_id] = bfac

    return bfac_dict


def insert_bfac_into_pdb(pdb, bfac_dict, default_value):
    """Return a list of lines representing the PDB file with inserted b-factor
    values.

    Insert the provided b-factor values provided into the provided PDB and
    return a copy of the PDB with the inserted b-factor values. If no b-factor
    value was provided for certain residues, insert the provided default value.

    Keyword arguments:
    pdb -- The PDB into which the b-factor values should be inserted.
    bfac_dict -- Dictionary that maps chain and sequence IDs to b-factor
    values.
    default_value -- Default b-factor value for residues that are not in the
    dictionary.
    """
    new_pdb = []
    for line in pdb:
        # Check if the current line is an atom line. If yes, add the b-factor
        # value. Otherwise leave the line unaltered. For hetero atoms, use the
        # default b-factor value.
        if line[0:6] == "ATOM  ":
            chain_id = line[20:22].strip()
            seq_id = line[23:26].strip()

            # If no b-factor value was provided use the default value.
            bfac_provided = chain_id in bfac_dict and seq_id in bfac_dict[
                chain_id]
            bfac = bfac_dict[chain_id][
                seq_id] if bfac_provided else default_value

            new_pdb.append("{prefix}{bfac:6.2f}{suffix}".format(
                prefix=line[:60], bfac=bfac, suffix=line[66:]))
        elif line[0:6] == "HETATM":
            new_pdb.append("{prefix}{bfac:6.2f}{suffix}".format(
                prefix=line[:60], bfac=default_value, suffix=line[66:]))
        else:
            new_pdb.append(line)

    return new_pdb


def main(args):
    """"Add the b-factor values to the PDB file and write the resulting file.

    Keyword arguments:
    args -- Command line arguments setting input and output files as well as
    behavior.
    """
    # Create a dictionary to map the b-factor values to corresponding residues.
    dictionary = create_bfac_dict(args.b_factors_file)

    # Read the provided PDB file and store its lines.
    with open(args.pdb_file) as pdb_file:
        pdb = pdb_file.readlines()

    # Insert the b-factor values into the PDB lines and write the PDB file.
    insert_bfac_into_pdb(pdb, dictionary, args.default_value)
    new_pdb = "".join(
        insert_bfac_into_pdb(pdb, dictionary, args.default_value))
    with open(args.output_file, "w") as output_file:
        output_file.write(new_pdb)


if __name__ == "__main__":
    # Parse the command line and assign the passed arguments.
    parser = get_parser()
    args = parser.parse_args()

    # Read b-factors and PDB and write the PDB containing the b-factor values.
    main(args)
