#!/bin/bash
(head -10 && tail -10) < "input/motion.tsv" |
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo $line | python3 command-line.py --mode "48h" &> output.log
done

