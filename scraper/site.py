
from utilities.settings import Settings


class Site:

    def __init__(self, name, settings):
        self._settings = Settings(settings, name)
        self._check_required_fields()

    @property
    def settings(self):
        return self._settings

    def _check_required_fields(self):
        # if self._settings.site_has_item_specification():
        #     keys_to_check = self.settings.item_field_keys
        #     fields_to_check = self.settings.item_fields
        # else:
        #     keys_to_check = self.settings.search_field_keys
        #     fields_to_check = self.settings.search_fields
        # for field in self.settings.required_fields:
        #     if self._invalid_field(field, keys_to_check, fields_to_check):
        #         raise ValueError("Invalid required field ({})".format(field))
        pass

    def _invalid_field(self, field, keys_to_check, fields_to_check):
        return field not in keys_to_check or not fields_to_check[field]
