#!/bin/bash

FILE1="$1"
FILE2="$2"

# xmllintで整形（インデント、改行を統一）
xmllint --format "$FILE1" > ./formatted1.xml
xmllint --format "$FILE2" > ./formatted2.xml

diff ./formatted1.xml ./formatted2.xml > diff_output.txt

if [[ $? -eq 0 ]]; then
  echo "整形後のXMLに差分はありません。"
else
  echo "整形後のXMLに差分があります:"
  cat diff_output.txt
fi
