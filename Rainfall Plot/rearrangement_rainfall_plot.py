#!/usr/bin/env python
"""Create Rainfall plots from BEDPE files.

Author: Anthony Fullam
Email: fullama@tcd.ie
"""
import sys
import pandas as pd
import numpy as np
from numpy import inf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


if len(sys.argv) == 1:
    sys.exit('Need to provide a bedpe file and output directory')

input_file = sys.argv[1]
output_directory = sys.argv[2]
rgtype_to_remove = sys.argv[3]

BEDPE_FILE = pd.read_table(input_file,
                           skip_blank_lines=True,
                           header=0,
                           dtype={'# chr1': str,
                                  'start1': int,
                                  'chr2': str,
                                  'start2': int,
                                  'strand1': str,
                                  'strand2': str,
                                  'sample': str})
# BEDPE_FILE = BEDPE_FILE[BEDPE_FILE.start1 != 'start1']

# Dictionary of chromosome lengths
chrs = {'1': 249250621,
        '2': 243199373,
        '3': 198022430,
        '4': 191154276,
        '5': 180915260,
        '6': 171115067,
        '7': 159138663,
        '8': 146364022,
        '9': 141213431,
        '10': 135534747,
        '11': 135006516,
        '12': 133851895,
        '13': 115169878,
        '14': 107349540,
        '15': 102531392,
        '16': 90354753,
        '17': 81195210,
        '18': 78077248,
        '19': 59128983,
        '20': 63025520,
        '21': 48129895,
        '22': 51304566,
        'X': 155270560,
        'Y': 59373566}


def determine_rg_type(strand1, strand2, chr1, chr2):
    """Determine the rgtype for strand information."""
    if chr1 != chr2:
        return 'translocation'
    elif strand1 != strand2:
        return 'inversion'
    elif strand1 == "+" and strand2 == "+":
        return 'deletion'
    elif strand1 == "-" and strand2 == "-":
        return 'tandem_dup'

BEDPE_FILE['RG_TYPE'] = BEDPE_FILE.apply(
    lambda row: determine_rg_type(row['strand1'],
                                  row['strand2'],
                                  row['# chr1'],
                                  row['chr2'],), axis=1)

if rgtype_to_remove == 'all_rgs':
    print(rgtype_to_remove)
elif rgtype_to_remove == 'nonpass':
    print("Removing rgs that havent passed brass2")
    BEDPE_FILE = BEDPE_FILE[BEDPE_FILE.assembly_score != '_']
else:
    try:
        BEDPE_FILE = BEDPE_FILE[BEDPE_FILE.RG_TYPE != rgtype_to_remove]
    except IndexError:
        sys.exit('''That rg_type doesnt exist, use one of:
                    deletion
                    inversion
                    translocation
                    tandem_dup''')

merge1 = BEDPE_FILE[['sample', '# chr1', 'start1', 'RG_TYPE']].copy()
merge1.columns = ['sample_name', 'chromosome', 'position', 'rg_type']
merge2 = BEDPE_FILE[['sample', 'chr2', 'start2', 'RG_TYPE']].copy()
merge2.columns = ['sample_name', 'chromosome', 'position', 'rg_type']

result = merge1.append(merge2)
result['sample_name'] = result.sample_name.str.split(',').str.get(0)

result.sort_values(['chromosome', 'position'], inplace=True)

result = result.reset_index(drop=True)

for x in chrs:
    fig = plt.figure()
    ax1 = plt.subplot2grid((3, 1), (0, 0), colspan=3, rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0), colspan=3, sharex=ax1)

    working_chromosome = result[result.chromosome == x]

    if len(working_chromosome.index) != 0:
        position_list = working_chromosome.position
        distance_between_rearrangements = position_list.diff()
        log_distance_between_rearrangements = np.log(distance_between_rearrangements)
        log_distance_between_rearrangements[log_distance_between_rearrangements == -inf] = 0
        position_list = position_list.drop(position_list.tail(1).index)
        log_distance_between_rearrangements = (
            log_distance_between_rearrangements.drop(
                log_distance_between_rearrangements.head(1).index))
        use_colors = {'inversion': '#FF7676',
                      'deletion': '#F6F49D',
                      'translocation': '#5DAE8B',
                      'tandem_dup': '#466C95'}

        ax1.scatter(position_list, log_distance_between_rearrangements,
                    c=[use_colors[rgtype] for rgtype in working_chromosome.rg_type],
                    linewidths=.1,
                    marker='o',
                    alpha=.75)
        ax1.set_xlim([0, chrs[x]])
        ax1.set_ylim([-1, max(log_distance_between_rearrangements) + 1])
        ax1.set_title('Chromosome ' + x)
        ax1.set_ylabel('log(distance)')
        ax1.get_xaxis().set_visible(False)
        ax1.plot()

        for sample in np.unique(working_chromosome.sample_name,):
            persamplechromosome = working_chromosome[working_chromosome.sample_name == sample]
            hist, binedges = np.histogram(persamplechromosome.position,
                                          int(chrs[x] / 1000000),
                                          range=(0.0, chrs[x]))
            left = binedges[:-1]
            newframe = np.where(hist == 0, 0, 1)
            try:
                totalframe = totalframe + newframe
            except NameError:
                totalframe = newframe

        ax2.bar(left,
                totalframe,
                linewidth=2,
                edgecolor='#E85285')
        ax2.set_xlabel('Chromosome Position')
        ax2.set_ylabel('Number of samples')
        del totalframe
        fig.subplots_adjust(hspace=0)
        plt.tight_layout()

        inversion = mpatches.Patch(fc='#FF7676',
                                   ls='solid',
                                   edgecolor='black')
        deletion = mpatches.Patch(fc='#F6F49D',
                                  ls='solid',
                                  edgecolor='black')
        translocation = mpatches.Patch(fc='#5DAE8B',
                                       ls='solid',
                                       edgecolor='black')
        tandem_dup = mpatches.Patch(fc='#466C95',
                                    ls='solid',
                                    edgecolor='black')
        lgd = ax1.legend(handles=[inversion,
                                  deletion,
                                  translocation,
                                  tandem_dup],
                         labels=['Inversion',
                                 'Deletion',
                                 'Translocation',
                                 'Tandem Dup'],
                         bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        plt.savefig(output_directory + 'chr' + x + ".pdf",
                    dpi=300,
                    bbox_extra_artists=(lgd,),
                    bbox_inches='tight')
        plt.close()
