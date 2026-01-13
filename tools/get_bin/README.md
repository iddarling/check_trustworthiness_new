tools/get_bin usage

Drop any PDF or XLSX files containing BIN or IIN numbers into this directory and run one of the helper scripts.

Scripts:
- `get_bins.py` — scans the directory for `.pdf` and `.xlsx` files, extracts 12-digit BIN/IIN matches, deduplicates (keeps up to 50) and saves to `../data/bin_list.txt`.
- `get_bins_xlsx.py` — only processes `.xlsx` files and saves all unique BINs to `../data/bin_list.txt`.

Notes:
- Both scripts write the results to the canonical `data/bin_list.txt` file in the project root.
- The scripts attempt to delete processed files in the directory after extraction. You may want to disable that if you prefer to keep originals.
- To run the scripts locally: `python tools/get_bin/get_bins.py` or `python tools/get_bin/get_bins_xlsx.py`.
- Make sure `openpyxl` and `pdfplumber` are installed (see `requirements.txt`).
