#!/usr/bin/env bash
for pdf in data/new/*.pdf
do
    echo "Processing $pdf file..."
    pdf2htmlEX --zoom 1.3 $pdf
done
