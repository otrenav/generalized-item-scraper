
import random
import pandas


class SearchStringsCSV:

    def __init__(self, settings):
        self.settings = settings

    def search_strings(self):
        s = self.settings
        data = pandas.read_csv(s.search_file).fillna('')
        avoid = data[s.avoid_on].str.contains(s.name, na=False)
        use = data[s.use_on].str.contains(s.name, na=False)
        all = data[s.use_on].str.contains('ALL', na=False)
        strings = list(data[s.search_string][(use | all) & ~avoid])
        if s.search_sample and len(strings) > s.search_sample:
            strings = random.sample(strings, s.search_sample)
        return strings

    def combinations(self):
        s = self.settings
        data = pandas.read_csv(s.search_file).fillna('')
        avoid = data[s.avoid_on].str.contains(s.name, na=False)
        use = data[s.use_on].str.contains(s.name, na=False)
        all = data[s.use_on].str.contains('ALL', na=False)
        strings = data[[s.search_string, s.direct_item_url]]
        strings = strings[(use | all) & ~avoid]
        strings = [
            {
                'search_string': row['SearchString'],
                'url': row['DirectURL']
            }
            for index, row in strings.iterrows()
        ]
        if s.search_sample and len(strings) > s.search_sample:
            strings = random.sample(strings, s.search_sample)
        return strings
