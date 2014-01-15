ICD-9_Codes
===========

Basic tools to handle ICD-9/ICD-9CM Codes.
-----------

A version in Rich Text Format (RTF) of the 2011 edition is available for downloading from the Centers for Disease Control and Prevention's [(CDC)/FTP server](ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD9-CM/2011/)

Different datasets are provided, once for each subcategory of the ICD9 codes. More information can be found in the [Readme](ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD9-CM/2011/Readme12.txt)

Here we provide a conversion script and output for the DTAB12.ZIP (Tabular List of Diseases) file.

Download the file:

```bash
wget ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD9-CM/2011/Dtab12.zip
```

Unzip, convert to text:

```bash
unzip Dtab12.zip
textutil -convert txt Dtab12.rtf 
```

Run the conversion script:

```bash
python deseases_to_csv.py < Dtab12.txt  > Dtab12.csv
```

