# vcf-area-codes
Get area code counts from a .vcf contacts file

# How to run
1. Download `areacodes.py` and `requirements.txt` into a directory on your computer
2. Create a python virtual environment:
    - `python3 -m venv venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`
3. Run the script, passing your vcf file as an argument:
    - `python areacodes.py mycontacts.vcf`


You can use the `-v` option if you want to see more debugging details, and if you want the output to go somewhere other than `area_code_counts.csv`, you can supply an output filename using `-o`. See `python areacodes.py --help` for full help text.
