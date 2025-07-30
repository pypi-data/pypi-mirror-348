# PDF Word Counter

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![PyPI](https://img.shields.io/pypi/v/pdf-word-counter)](https://pypi.org/project/pdf-word-counter/)

A tool to search PDF files for specific words and generate frequency statistics.
Supports both PyPDF2 and pdfminer.six backends, with output to Astropy or Pandas formats.


## Features
- Case-sensitive/insensitive search
- Unicode text normalization (NFC, NFD, NFKC, NFKD)
- Parallel processing using threads
- Output to Astropy tables or Pandas DataFrames
- Select specific pages or page ranges
- CLI and Python API
- Filename parsing to extract metadata
- Optional columns and sorting

## Installation

Basic installation:
```bash
pip install pdf-word-counter
```

Full installation (with all optional dependencies):
```bash
pip install pdf-word-counter[miner]    # + pdfminer.six
pip install pdf-word-counter[astropy]  # + Astropy Tables
pip install pdf-word-counter[full]     # All extras
```

## Coomand Line Usage 

### Basic Example
```bash
# Count words in all PDFs (case-insensitive) and print table
pdf-word-counter "AI,ML" papers/*.pdf --show

```

#### Advanced Examples
```
# Search pages 1-5 with Unicode normalization
pdf-word-counter "café" doc.pdf --pages 1-5 --unicode --form NFKC

# Case-sensitive search with 4 parallel workers
pdf-word-counter "Python" docs/*.pdf --case --workers 4

# Case-sensitive search with pdfminer
pdf-word-counter "Python" docs/*.pdf --case --miner --outfile counts.csv

# Extract project names from filenames like "ProjectX_2023.pdf"
pdf-word-counter "algorithm" *.pdf --dsep "{'_': {'project': 0}}" 
```

#### CLI Options

| Option           | Description                                               |
| ---------------- | --------------------------------------------------------- |
| `words`          | Comma-separated list of words to search for               |
| `pdfs`           | List of PDF files or glob patterns                        |
| `--case`         | Case-sensitive search                                     |
| `--pages`        | Pages to include, e.g. `"1,3-5"`                          |
| `--miner`        | Use `pdfminer.six` backend instead of `PyPDF2`            |
| `--pprint N`     | Log progress every N pages (PyPDF2 only)                  |
| `--unicode`      | Normalize Unicode text before search                      |
| `--form FORM`    | Unicode normalization form (`NFC`, `NFD`, `NFKC`, `NFKD`) |
| `--outfile FILE` | Save the output table to a file                           |
| `--show`         | Print the table to stdout                                 |
| `--sort COLUMNS` | Comma-separated list of columns to sort by                |
| `--workers N`    | Number of parallel workers (default: 1)                   |
| `--backend`      | Output backend: `pandas` or `astropy`                     |
| `--ppdf N`       | Log progress every N files (serial mode)                  |
| `--log-level`    | Logging level: `DEBUG`, `INFO`, etc.                      |


#### Filename Parsing Options

| Option   | Description                                                                                                                                                                                                                    |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--dsep` | Dictionary to extract metadata from filenames by splitting them. For example: `"{'_': {'project': 1}}"` will split filenames by underscores (`_`) and extract the second element (index 1) into a new column called `project`. |
| `--year` | Attempt to extract a 4-digit year from the filename and add it as a new column.                                                                                                                                                |
| `--ext`  | Keep the file extension in the `filename` column (by default, it is removed).                                                                                                                                                  |


#### Output Column Toggles

| Option     | Description                     |
| ---------- | ------------------------------- |
| `--nfile`  | Omit the filename column        |
| `--npages` | Omit the number-of-pages column |



### Python API
```python
from pdf_word_counter import search_pdfs

results = search_pdfs(
    ["document1.pdf", "document2.pdf"],
    ["word1", "word2"],
    output_file="results.csv",
    show=True,
    sort_cols=["count"],
    ignore_case=True,
    use_pdfminer=False,
    workers=4,
)
```

## License
MIT

## How to Cite
This code was used in the research published as:

García-Benito, Rubén (2025). **Beyond Universality: Cultural Diversity in Music and Its Implications for Sound Design and Sonification**. *Audio Mostly & ICAD Joint Conference (AM.ICAD 2025)*. Association for Computing Machinery, June 30 – July 4, 2025, Coimbra, Portugal

If you use this software in your research or adaptations, please cite the above paper and this repository accordingly.
