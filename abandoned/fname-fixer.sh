#!/bin/bash

SCRIPT=$(readlink -f $0)

usage () {
    echo "$SCRIPT [-h|--help] DIRECTORY";
    echo "Fix up the file names in the given directory."
    echo "Note: it works best when supplied with an absolute path."
    exit 1;
}

ARGS=`getopt -o "h" -l "help" -n "fname-fixer.sh" -- "$@"`
if [ $? -ne 0 ]; then
    # bad arguments found
    exit 1;
fi
eval set -- "$ARGS"

while true ; do
    case "$1" in
        -h|--help) usage ; shift ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done

SANITIZE="$(dirname $SCRIPT)/str-sanitize"

DIRECTORY="$(echo ${1} | sed 's@/$@@')"

RSYNC="rsync -ha --no-whole-file --inplace --remove-source-files"

echo "Fixing up filenames in \"${DIRECTORY}\"..."
echo "This will affect the following files: "
echo "$(ls -Q ${DIRECTORY}| sed 's@/$@@')"
read -p "Press enter to continue..."
for src in ${DIRECTORY}/*; do
    src_dir="$(dirname "${src}")"
    fname="$(basename "${src}")"
    dest="${src_dir}/$(${SANITIZE} ${fname})"
    echo "Fixing: ${src}"
    echo "  ${src} ${dest}.tmp"
    ${RSYNC} "${src}" "${dest}.tmp"
    echo "  ${dest}.tmp ${dest}"
    ${RSYNC} "${dest}.tmp" "${dest}"
done
