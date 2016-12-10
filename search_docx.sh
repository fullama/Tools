#!/bin/bash
PROG=`basename $0`

if [ $# -eq 0 ]
then
  echo "Usage: $PROG string file.docx [file.docx...]"
  exit 1
fi

findme="$1"
shift

for file in $@
do
  unzip -p "$file" | grep -q "$findme"
  [ $? -eq 0 ] && echo "$file"
done
