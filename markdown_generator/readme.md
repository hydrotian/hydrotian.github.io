# Jupyter notebook markdown generator

These .ipynb files are Jupyter notebook files that convert a TSV containing structured data about talks (`talks.tsv`) or presentations (`presentations.tsv`) into individual markdown files that will be properly formatted for the academicpages template. The notebooks contain a lot of documentation about the process. The .py files are pure python that do the same things if they are executed in a terminal, they just don't have pretty documentation.

# Added by Tian
For publications, which is only used here acturally, add new publication info into `add_new_pub_here.csv` file, following the first row as a template. After generating the `.md` files for each publication, move the new entries to the backup file `pub_backup.csv`, leave the first row there for future reference.

- if you don't remove the entries to backup, then next time, the `.md` file will be regenrated, overwrite the files for these publications. 