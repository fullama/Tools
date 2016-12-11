#!/bin/bash

if [[ -z "$1" ]]
then
    echo
    echo "Usage Example:"
    echo
    echo "bash /nfs/team78pc20/af14/programs/scripts/run_rearrangement_rainfall_plot.sh ./outputarea/ 1140 inversion"
    echo
    echo "Argument1: output directory"
    echo
    echo "Argument2: Either a project number or a bedpefile"
    echo "    Must have these columns:"
    echo "                            # chr1"
    echo "                            start1"
    echo "                            chr2"
    echo "                            start2"
    echo "                            strand1"
    echo "                            strand2"
    echo "                            sample"
    echo
    echo "Argument3: (optional) An rg_type to leave out"
    echo "                     One of:"
    echo "                            deletion"
    echo "                            inversion"
    echo "                            translocation"
    echo "                            tandem_dup"
    echo "                     or use:"
    echo "                            nonpass"
    echo "                     to just use those that have passed brass2"
    echo
    exit
else
    output=$1
fi

if [[ -z "$2" ]]; then
    echo Usage:
    echo "Need to provide a bedpe file or a project number"
    echo
    exit
elif [[ "$2" =~ ^[0-9]+$ ]]; then
    find /nfs/cancer_ref01/nst_links/live/${2} -name *brass.annot.bedpe.gz | xargs -I {} zgrep --no-filename '# chr1' {} | head -n 1 > ${output}merged.txt
    find /nfs/cancer_ref01/nst_links/live/${2} -name *brass.annot.bedpe.gz | xargs -I {} zgrep -v --no-filename '# chr1' {}  >> ${output}merged.txt
    echo
    echo "Project Number:" $2
    bedpe=${output}merged.txt
else
    bedpe=$2
fi

if [[ -z "$3" ]]
then
    arg3="all_rgs"
    echo "Including all rearrangement types"
else
    arg3=$3
    echo "Not Including: " $arg3
fi

echo
echo "Bedpe_File:" $bedpe
echo "Output Directory:" $output
echo

#source activate /nfs/users/nfs_a/af14/miniconda2/envs/rainfall_env
unset PYTHONPATH
source /nfs/users/nfs_a/af14/pythonenvs/python3.4.0/bin/activate
python /nfs/team78pc20/af14/programs/scripts/rearrangement_rainfall_plot.py $bedpe $output $arg3
#source deactivate
deactivate
