import csv
import re
import requests
from xml.etree import ElementTree

base_url = 'http://papyrus.bib.umontreal.ca/oai/request'

verbe = 'ListRecords' # 
metadata_schema = 'oai_dc'
ensemble = 'col_1866_2991' # Faculté des arts et des sciences – Département de psychologie - Thèses et mémoires

requete = '?verb={0}&metadataPrefix={1}&set={2}'.format(verbe, metadata_schema, ensemble)

reponse = requests.get(base_url + requete)

racine = ElementTree.fromstring(reponse.content.decode('utf-8'))

records = racine[2]

tags = ['title','creator','contributor','description','date','type']

with open('theses.csv', 'w', newline = '', encoding = 'utf-8') as f:
    writer = csv.DictWriter(f, fieldnames = tags, delimiter = ",", quoting = csv.QUOTE_MINIMAL)
    writer.writeheader()
    for entree in records:
        newrec = dict.fromkeys(tags, None)
        for metadata in entree[1][0]:
            tag = re.sub('{[^>]+}', '', metadata.tag)
            if (tag in tags) and newrec[tag] is None:
                newrec[tag] = metadata.text
        writer.writerow(newrec)