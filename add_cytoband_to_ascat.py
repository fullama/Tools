__author__ = 'anthonyfullam'

import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=('''\
        Takes ASCAT output file and modifies it to add an event descriptor
    '''))

parser.add_argument('-f', '--ASCATfile', help='ASCAT file', metavar='')
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit('\n \n Need to provide an ASCAT file! \n \n')

file_name = args.ASCATfile
output_file = args.ASCATfile.split('.csv')[0] + '_events.csv'


cytobands = pd.read_csv('cytoBand.txt', delimiter="\t",
                        names=['Chromosome',
                               'Start_band',
                               'End_band',
                               'Band_name',
                               'Stain'])

ascatfile = pd.read_csv(file_name,
                        names=['segment_number',
                               'Chromosome',
                               'Start_CNregion',
                               'End_CNregion',
                               'Norm_total_CN',
                               'Norm_minor_allele_CN',
                               'Tumour_total_CN',
                               'Tumour_minor_allele_CN'])
ascatfile['event'] = ""


def definewindow(workingframe):
    lregion = workingframe[(workingframe.Start_band > start_cn_change)]
    if len(lregion) == 0:
        lindex = workingframe.index[-1]
    else:
        lindex = lregion.index[0] - 1

    uregion = workingframe[(workingframe.End_band < end_cn_change)]
    if len(uregion) == 0:
        uindex = workingframe.index[0]
    else:
        uindex = uregion.index[-1] + 1

    return lindex, uindex


for index, row in ascatfile.iterrows():
    if row.Norm_total_CN == row.Tumour_total_CN and row.Norm_minor_allele_CN == row.Tumour_minor_allele_CN:
        cnevent = ""
    elif row.Norm_total_CN < row.Tumour_total_CN:
        cnevent = 'gain'
    elif row.Norm_total_CN > row.Tumour_total_CN:
        cnevent = 'del'
    else:
        cnevent = 'change'

    start_cn_change, end_cn_change = row.Start_CNregion, row.End_CNregion
    one_chromosome_frame = cytobands[cytobands.Chromosome == row['Chromosome']]
    start_index, end_index = definewindow(one_chromosome_frame)
    start_band = one_chromosome_frame.ix[start_index]['Band_name']
    end_band = one_chromosome_frame.ix[end_index]['Band_name']
    if cnevent == "":
        ascatfile.loc[index,'event'] = ""
    else:
        if start_band == end_band:
            ascatfile.loc[index,'event'] = '{0}({1})'.format(cnevent,start_band)
        else:
            ascatfile.loc[index,'event'] = '{0}({1}-{2})'.format(cnevent,start_band,end_band)

ascatfile.to_csv(output_file)
