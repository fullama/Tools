#!/usr/bin/env python2.7

import csv
import sys
import subprocess

if len(sys.argv) == 1:
    sys.exit('\n ************ \n usage: in dir with project dumps - prepforcircos.py [tumourcount] ./pro* \n ************ \n')

tumourcount = sys.argv[1]
filesin = sys.argv[2:]

print tumourcount
print filesin

for x in filesin:
    sampleno = (((x.split("a.txt"))[0]).split("_"))[-1]
    outfilename = sampleno + "_TumourCount_" + tumourcount + "_for_circos.txt"
    outfile = open(outfilename, "w+")

    rearrangements = open(x, 'rU')
    rg = csv.reader(rearrangements, delimiter='\t')

    for line in rg:
        if len(line) > 25:
            # inversions
            if line[18] == '1' or line[18] == '8':
                outfile.write("hs" + line[8] + "\t" + line[9] + "\t" + line[10] + "\t"  + "hs" + line[12] + "\t" + line[13] + "\t" + line[14] + "\t" + "color=blue" + "\n")
            # deletions
            elif line[18] == '2':
                outfile.write("hs" + line[8] + "\t" + line[9] + "\t" + line[10] + "\t"  + "hs" + line[12] + "\t" + line[13] + "\t" + line[14] + "\t" + "color=red" + "\n")
            # tandemduplications
            elif line[18] == '4':
                outfile.write("hs" + line[8] + "\t" + line[9] + "\t" + line[10] + "\t"  + "hs" + line[12] + "\t" + line[13] + "\t" + line[14] + "\t" + "color=green" + "\n")
            # translocations
            elif line[18] == '32':
                outfile.write("hs" + line[8] + "\t" + line[9] + "\t" + line[10] + "\t"  + "hs" + line[12] + "\t" + line[13] + "\t" + line[14] + "\t" + "color=black" + "\n")

    outfile.write("\n")
    outfile.close()

##################################################################################

    # circos conf file
    circosfilename = sampleno + "_TumourCount_" + tumourcount + ".conf"
    circosfile = open(circosfilename, "w+")

    conffile = '''
    <colors>
    <<include /nfs/team78pc10/af14/programs/Circos/colors.conf>>
    </colors>

    <fonts>
    <<include /nfs/team78pc10/af14/programs/Circos/fonts.conf>>
    </fonts>

    <<include /nfs/team78pc10/af14/programs/Circos/ideogram.conf>>

    #tick marks and numbers
    <<include /nfs/team78pc10/af14/programs/Circos/ticks.conf>>

    <<include /nfs/team78pc10/af14/programs/Circos/housekeeping.conf>> 

    karyotype   = /nfs/team78pc10/af14/programs/Circos/karyotype.human.hg19.txt

    <image>
    dir   = /nfs/team78pc10/af14/circosrunningarea
    file  = {0}.png
    24bit = yes
    png   = yes
    svg   = no

    # radius of inscribed circle in image
    radius         = 1500p
    background     = white

    # by default angle=0 is at 3 o'clock position
    angle_offset   = -90
    #angle_orientation = counterclockwise
    auto_alpha_colors = yes
    auto_alpha_steps  = 1
    </image>

    chromosomes_units           = 1000000
    chromosomes_display_default = yes
    chromosomes       = hs11;hs20; hs6; hs2; hs3; hs12; hs16 # only if chromosomes_display_default is set to no


    <links>

    <link breaks>
    #the links showing rearrangements
    bezier_radius_purity = 0.8
    show         = yes
    thickness    = 10
    file         = {0}_for_circos.txt
    radius        = 0.95r
    bezier_radius = 0.2r

    </link>

    </links>
    '''.format(sampleno + "_TumourCount_" + tumourcount)

    circosfile.write(conffile)
    circosfile.close()

    subprocess.call(["circos", "-conf", circosfilename])
    subprocess.call(["rm", circosfilename])
    subprocess.call(["rm", outfilename])
