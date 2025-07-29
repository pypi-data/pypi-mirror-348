#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024-2025 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import defaultdict
import argparse

import pandas as pd
import numpy as np


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=str,
        help="Path to mcp tsv file to find inflection points",
    )
    parser.add_argument("-s", "--sample", required=True, type=str, help="Sample ID")
    parser.add_argument("-o", "--output", required=True, type=str, help="Output path")

    args = parser.parse_args()

    path = args.input
    sample = args.sample
    output = args.output

    return path, sample, output


def find_mcp_inf_points(mcp_df):
    """
    Find inflection points from an mcp_df file output by "assess_mcp_proportions_MERGED.py"

    Takes the list of average mcp conservations and gets the derivative of the curve
    Keep any points of the derivative where value is above the 80th percentile

    Outputs a dictionary with key-val pairs where vals are lists:
        'strand' -> strand list
        'inf_point' -> inf_point list

    """

    inf_point_dict = defaultdict(list)
    start_indices = [int(i) for i in mcp_df.columns.tolist()]

    for i in range(len(mcp_df)):  # Loop through both possible strands of the mcp_df
        strand = mcp_df.index[i]
        props = mcp_df.iloc[i].tolist()
        props = [-val for val in props]

        prop_diff = np.diff(props) / np.diff(start_indices)  # Get the derivative
        infl_points = np.where(prop_diff > np.percentile(prop_diff, 80))[
            0
        ]  # Grab points above 80th percentile

        for ind in infl_points:
            inf_point = start_indices[ind]

            if (
                inf_point < 10 or inf_point > 20
            ):  # Rule to facilitate results - won't accept
                continue  # points below index 10 or above index 20
                # 10 means a cutoff of 15 and 20 a cutoff of 25
                # literature points to no primers existing that are
                # shorter or bigger  than these lengths

            inf_point_dict["strand"].append(strand)
            inf_point_dict["inf_point"].append(inf_point)

    return inf_point_dict


def main():

    path, sample, output = parse_args()

    mcp_df = pd.read_csv(path, sep="\t", index_col=0)  # Read mcp_df
    inf_point_dict = find_mcp_inf_points(mcp_df)  # Generate inflection points dict

    if len(inf_point_dict) > 0:  # If the inf_point_dict isn't empty..
        inf_point_df = pd.DataFrame.from_dict(
            inf_point_dict
        )  # .. turn it into a dataframe
        inf_point_df.to_csv(
            f"{output}/{sample}_inf_points.tsv", sep="\t", index=False
        )  # ..save it to a .tsv file

    else:  # If it is empty..
        fw = open(f"{output}/{sample}_inf_points.tsv", "w")  # ..make an empty file
        fw.close()


if __name__ == "__main__":
    main()
