#!/bin/bash

#***************************************************************
# This script takes a course download .zip from TUI and converts
# it to markdown notes then imports it into a dendron vault
#
# required arguments are <Course Number> and <Filename.zip>
#
# Example: converter.bash CSC123 'CSC123 download.zip'
#****************************************************************

scriptHome=${PWD}/temp
notesRoot=${PWD}/toImport/$1/
importRoot=${PWD}/toImport

echo "Unzipping the archive"
unzip -q "${2}" -d ${scriptHome}

#Loop through module* files, cut out the extras and then convert to md, then do it for syllabus files
#fix file names to final form at the same time
#first sed command cuts everything at the match and above, the second cuts the match and below
#iconv removes any stray unicode characters
echo "converting HTML files to MD..."
# cd $scriptHome/DW4Mod\ -\ Codes/EMPTY\ 4-MODULE\ HTML\ DOCS/Modules
# cd $scriptHome/4\ MODULE/Modules #mod for csc312
cd $scriptHome/CSC330/Modules #mod for csc316
for f in **/*.html; do
    fNum=${f:11:1}
    fname=${f:12}
    fname=${fname%.html}${fNum}.md
    fname=$(echo "$fname" | tr '[:upper:]' '[:lower:]')
    cat "$f" | \
    sed '1,/<div class="courseTitle">/d' | \
    sed '/<div class="footer">/,/<\/html>/d' | \
    pandoc --wrap=none --from html --to markdown_strict | \
    iconv -c -f utf-8 -t ascii > ${fname} #"${f%.html}${f:3:1}.md"
done
cd ../Syllabus
for f in *.html; do
    #echo "converting $f"
    cat "$f" | \
    sed '1,/<div class="grid_12">/d' | \
    sed '/<div class="syllabus_footer">/,/<\/html>/d' | \
    pandoc --wrap=none --from html --to markdown_strict | \
    iconv -c -f utf-8 -t ascii > "${f%.html}.md"
done

# create a new directory structure so that the dendron import has the correct structure
echo "making $1 directory structure..."
mkdir -p ${notesRoot}mod1 ${notesRoot}mod2 ${notesRoot}mod3 ${notesRoot}mod4 ${notesRoot}assets

# join the general files to create the root level index.md wtih a horizontal line between files
echo "Creating root index.md file"
cat CourseOverview.md <(echo -e '___\n') \
SignificanceOfCourse.md <(echo -e '___\n') \
LearningOutcomes.md <(echo -e '___\n') \
MaterialsAndBiblio.md \
>${notesRoot}index.md


echo "Moving files into directories..."
# Loop through the converted files and move them to the new directory structure
cd ../Modules
for f in *.md; do
    if [[ ${f} == *1.* ]]; then
        mv ${f} ${notesRoot}mod1
    elif [[ ${f} == *2.* ]]; then 
        mv ${f} ${notesRoot}mod2
    elif [[ ${f} == *3.* ]]; then 
        mv ${f} ${notesRoot}mod3
    elif [[ ${f} == *4.* ]]; then 
        mv ${f} ${notesRoot}mod4
    else      
        echo "File match failed $f"
    fi
done

echo "moving assets..."
mv ${scriptHome}/* ${notesRoot}assets/

echo "fixing asset links..."
#Loop through and cleanup the dirty local asset tag links
#first sed command changes the link to the asssets directory
#second sed command removes and trailing url data in the link
cd $notesRoot
for f in **/*.md; do
    sed -i '' -e 's:/content/enforced/10999-CSC310-MOD/Modules/Module[0-9]:../assets:g' -e 's:?_&.*):):g' ${f}
done

echo "creating module index files..."
for d in */ ; do
    if [[ ${d} != assets* ]]; then
        modNum=${d:3:1}
        cat ${d}home${modNum}.md <(echo -e '___\n') \
        ${d}objectives${modNum}.md <(echo -e '___\n') \
        ${d}background${modNum}.md <(echo -e '___\n') \
        >${d}index.md
        rm ${d}home${modNum}.md ${d}objectives${modNum}.md ${d}background${modNum}.md
    fi
done

#remove the orignal unzipped files
rm -rfd ${scriptHome}
echo "Conversion Complete..."

#create the dendron import config file
printf "src: ${notesRoot}\n\
vaultName: vault\n\
indexName: index.md" \
> ${notesRoot}configTest.yml

echo "importing to dendron..."
dendron importPod --podId dendron.markdown \
--wsRoot '/Users/tculpepp/Documents/repos/dendron' \
--config src=~/Downloads/CSC316/toImport,vaultName=vault,indexName=index.md
--config src=${importRoot},vaultName=vault,indexName=index.md

echo "Script complete, cleaning up..."
rm -rfd ${importRoot}
echo "Done"
