README: html_to_csv.py

This script takes an html version of the Canadian Light list and returns a csv of it's contents, with additional columns for identification 
of ATONs(aids to navigation). 

As the individual html documents are region specific, and not standardized, the script must be modified based on the region/html doc.
To figure out how to modify, turn the html into a csv using pd.read_html and see what it returns, go from there. 

To return different identifiers modify the "#find keywords and create new columns for aton identification" section. 
