
import settings_sites as s

SETTINGS = {
    'save_html': False,
    'random_proxies': False,
    'random_user_agents': True,
    'timezone': 'America/Mexico_City',
    'search_strings': {
        'file': 'inputs/search-strings-full.csv',
        'search_string': 'SearchString',
        'direct_item_url': 'DirectURL',
        'avoid_on': 'AvoidOn',
        'use_on': 'UseOn',
        'sample': None
    },
    'mongo': {
        'db': 'flatfooted',
        'host': 'localhost',
        'port': 27017
    },
    'required_fields': [
        'name',
        'price'
    ],
    'sites': {
        #
        # Standard
        #
        # 'AMZN': s.AMZN,
        # 'CDW': s.CDW,
        # 'FAST': s.FAST,
        # 'BUNZL': s.BUNZL,
        # 'PCMI': s.PCMI,
        # 'HDSS': s.HDSS,
        # 'CNXN': s.CNXN,
        # 'GI': s.GI,
        # 'CP': s.CP,
        # 'MM': s.MM,
        #
        # Cookies
        #
        'ORLY': s.ORLY,
        #
        # JavaScript
        #
        # 'ZORO': s.ZORO,
        # 'GWW': s.GWW,
        # 'NSIT': s.NSIT,
        # 'STAPLES': s.STAPLES,
        # 'ESND': s.ESND,
        #
        # Search Page
        #
        # 'TECD': s.TECD,
        #
        # Double-hops
        #
        # 'MSM': s.MSM,
        # 'AZO': s.AZO
    }
}
