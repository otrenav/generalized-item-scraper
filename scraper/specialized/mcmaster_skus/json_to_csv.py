
import sys
import json
import pandas

file_name = sys.argv[1]
json_file = './{}.json'.format(file_name)
csv_file = './{}.csv'.format(file_name)

print(json_file)
print(csv_file)

data = json.load(open(json_file))
clean_data = []

for page in data:
    for link in page['links']:
        clean_data.append([
            page['landing'],
            page['timestamp'],
            page['heading'],
            link['sku'],
            link['price_landing'],
            link['url']
        ])

columns = ['landing', 'timestamp', 'heading', 'sku', 'price_landing', 'url']
df = pandas.DataFrame(clean_data, columns=columns)
df.to_csv(csv_file, index=False)

print("Done.")
