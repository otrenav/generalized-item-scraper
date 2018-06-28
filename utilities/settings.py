
import pytz


class Settings:

    def __init__(self, settings, name=None):
        self.settings = settings
        self._name = name

    @property
    def base_url(self):
        return self._site_settings['base_url']

    @property
    def names(self):
        return list(self.settings['sites'].keys())

    @property
    def name(self):
        return self._name

    @property
    def random_proxies(self):
        return self.settings['random_proxies']

    @property
    def random_user_agents(self):
        return self.settings['random_user_agents']

    @property
    def save_html(self):
        return self.settings['save_html']

    @property
    def timezone(self):
        return pytz.timezone(self.settings['timezone'])

    @property
    def search_fields(self):
        return self._site_settings.get('search', {}).get('fields', {})

    @property
    def search_field_keys(self):
        return list(self._site_settings
                    .get('search', {}).get('fields', {}).keys())

    @property
    def item_fields(self):
        return self._site_settings['item']['fields']

    @property
    def item_field_keys(self):
        return list(self._site_settings['item']['fields'].keys())

    @property
    def required_fields(self):
        return self.settings['required_fields']

    @property
    def first_item_selectors_key(self):
        is_xpath = self._site_settings['search'].get('first_item')
        return 'first_item' if is_xpath else 'first_item_css'

    @property
    def first_item_selectors(self):
        if not self.site_has_item_specification():
            return None
        return self._site_settings['search'][self.first_item_selectors_key]

    @property
    def auto_redirected_key(self):
        is_xpath = self._site_settings['search'].get('auto_redirected')
        return 'auto_redirected' if is_xpath else 'auto_redirected_css'

    @property
    def auto_redirected_selectors(self):
        if self.site_has_auto_redirected_selectors():
            return self._site_settings['search'][self.auto_redirected_key]
        return None

    @property
    def double_hop_key(self):
        is_xpath = self._site_settings['search'].get('double_hop')
        return 'double_hop' if is_xpath else 'double_hop_css'

    @property
    def double_hop_selectors(self):
        if self.site_has_double_hop_selectors():
            return self._site_settings['search'][self.double_hop_key]
        return None

    @property
    def use_search(self):
        return 'search' in self._site_settings.keys()

    @property
    def search_query(self):
        return self._site_settings['search']['query']

    @property
    def search_file(self):
        return self.settings['search_strings']['file']

    @property
    def direct_item_url(self):
        return self.settings['search_strings']['direct_item_url']

    @property
    def search_string(self):
        return self.settings['search_strings']['search_string']

    @property
    def use_on(self):
        return self.settings['search_strings']['use_on']

    @property
    def avoid_on(self):
        return self.settings['search_strings']['avoid_on']

    @property
    def search_sample(self):
        return self.settings['search_strings']['sample']

    @property
    def javascript(self):
        return self._site_settings.get('javascript', False)

    @property
    def mongo(self):
        return 'mongo' in self.settings.keys()

    @property
    def cookies(self):
        return self._site_settings.get('cookies', [])

    @property
    def headless(self):
        return self._site_settings.get('headless', True)

    @property
    def _site_settings(self):
        if not self._name:
            raise ValueError('Global settings instance (without `name`)')
        return self.settings['sites'][self.name]

    def site_has_item_specification(self):
        search_keys = self._site_settings.get('search', {}).keys()
        return (
            'first_item' in search_keys or
            'first_item_css' in search_keys
        )

    def site_has_auto_redirected_selectors(self):
        search_keys = self._site_settings['search'].keys()
        return (
            'auto_redirected' in search_keys or
            'auto_redirected_css' in search_keys
        )

    def site_has_double_hop_selectors(self):
        search_keys = self._site_settings['search'].keys()
        return (
            'double_hop' in search_keys or
            'double_hop_css' in search_keys
        )
