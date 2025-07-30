"""
PDF Word Frequency Counter

A tool to search PDF files for specific words and generate frequency statistics.
Supports both PyPDF2 and pdfminer.six backends, with output to Astropy or Pandas formats.

Features:
- Case-sensitive/insensitive word search
- Unicode text normalization
- Multi-threaded processing
- Page-range selection

Example usage:
  pdf-word-counter "word1,word2" documents/*.pdf --outfile results.csv
  pdf-word-counter "research" paper.pdf --pages "1-5" --case --miner

Author: Rubén García-Benito @ IAA-CSIC
License: MIT
Last update: 2025-05-01

Allow ``python -m pdf_word_counter`` to run the CLI.
"""
from .cli import main

if __name__ == "__main__":  # pragma: no cover
    main()

