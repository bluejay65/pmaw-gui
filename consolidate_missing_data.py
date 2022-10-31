import os
import csv

main_dict = {}

for filename in os.listdir(os.path.join(os.getcwd(), 'missing data')):
   with open((os.path.join(os.path.join(os.getcwd(), 'missing data'), filename)), 'r') as f:
      for line in csv.DictReader(f):
        main_dict[line['Date']] = line['Presence']

with open((os.path.join(os.path.join(os.getcwd(), 'missing data'), 'consolidated_data.csv')), 'w') as f:
   f.write('Date,Presence\n')
            
   for k,v in main_dict.items():
      f.write(k+','+v+'\n')
