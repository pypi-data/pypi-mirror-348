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

import argparse
from collections import defaultdict

import pandas as pd
import numpy as np

from mgnify_pipelines_toolkit.analysis.amplicon.amplicon_utils import (
    get_read_count,
    build_cons_seq,
    build_mcp_cons_dict_list,
    fetch_mcp,
)
from mgnify_pipelines_toolkit.constants.thresholds import MCP_MAX_LINE_COUNT


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=str,
        help="Path to fastq file to assess mcps",
    )
    parser.add_argument("-s", "--sample", required=True, type=str, help="Sample ID")
    parser.add_argument(
        "-st",
        "--strand",
        required=True,
        choices=["FR", "F", "R"],
        help="F: Forward, R: Reverse",
    )
    parser.add_argument("-o", "--output", required=True, type=str, help="Output path")

    args = parser.parse_args()

    path = args.input
    sample = args.sample
    strand = args.strand
    output = args.output

    return path, sample, strand, output


def find_mcp_props_for_sample(path, rev=False):
    """
    Generate mcp proportions in a stepwise and windowed manner for a fastq file.

    For a continuous range of starting indices (2 to 25), generate mcps of window size of 5 bases.
    Calculate the average conservation of the most common base at each index of a window.
    The resulting list of mcp conservations can be considered a conservation curve and used to
    identify inflection points where the conservation suddenly changes.

    Output a dictionary where:
        key -> an index starting point e.g. base 10
        val -> the average conservation of the most common base for the mcp window goign from base 10 to 15 (inclusive)
    """

    res_dict = defaultdict(float)
    start_range = range(2, 25, 1)  # Range of starting indices

    print(f"Processing {path}")

    mcp_len = 5  # length of generated mcps

    for start in start_range:

        end = (
            start + mcp_len - 1
        )  # compute the final index for the mcp (inclusive). Indices are of base 1 not 0.

        read_count = get_read_count(
            path, file_type="fastq"
        )  # get read count for fastq file

        max_line_count = None
        if read_count > MCP_MAX_LINE_COUNT:
            max_line_count = MCP_MAX_LINE_COUNT

        mcp_count_dict = fetch_mcp(
            path, end, start, rev, max_line_count
        )  # get MCP count dict
        mcp_cons_list = build_mcp_cons_dict_list(
            mcp_count_dict, mcp_len
        )  # list of base conservation dicts for mcps
        cons_seq, cons_conf = build_cons_seq(
            mcp_cons_list, read_count, max_line_count=max_line_count
        )  # get list of max base conservations for each index

        res_dict[start] = np.mean(cons_conf)  # compute the mean

    return res_dict


def concat_out(fwd_out="", rev_out=""):
    """
    Generate Pandas dataframe out of mcp dictionary.

    Output looks like this (when both F and R are requested):
        2	3	4
    F	0.7814975041597337	0.8736772046589019	0.9434276206322796
    R	0.9010981697171381	0.9082861896838601	0.90369384359401

    Columns are the starting indices. Row labels are the strand.
    """

    total_res_dict = defaultdict(list)
    df_ind = []

    # Check if fwd strand was requested
    if fwd_out != "":
        [total_res_dict[key].append(fwd_out[key]) for key in fwd_out.keys()]
        df_ind.append("F")

    # Check if rev strand was requested
    if rev_out != "":
        [total_res_dict[key].append(rev_out[key]) for key in rev_out.keys()]
        df_ind.append("R")

    res_df = pd.DataFrame.from_dict(total_res_dict)
    res_df.index = df_ind

    return res_df


def main():

    path, sample, strand, output = parse_args()

    res_df = ""

    # TODO: match-case statement is python 3.10>. We are currently locking the version
    # at version 3.9. The day we bump the version we should replace these if statements
    # with a match-case block.

    if strand == "FR":
        fwd_out = find_mcp_props_for_sample(path)
        rev_out = find_mcp_props_for_sample(path, rev=True)
        res_df = concat_out(fwd_out, rev_out)
    elif strand == "F":
        fwd_out = find_mcp_props_for_sample(path)
        res_df = concat_out(fwd_out)
    elif strand == "R":
        rev_out = find_mcp_props_for_sample(path, rev=True)
        res_df = concat_out(rev_out=rev_out)
    else:
        print(
            "Incorrect strand input. Should be F for forward, R for reverse, or FR for both."
        )
        exit(1)

    # Save resulting dataframe to a tsv file
    res_df.to_csv(f"{output}/{sample}_mcp_cons.tsv", sep="\t")


if __name__ == "__main__":
    main()
