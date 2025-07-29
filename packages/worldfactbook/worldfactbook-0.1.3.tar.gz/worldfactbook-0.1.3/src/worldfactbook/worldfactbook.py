import json
import requests
import re
import html
import pathlib
import datetime
import urllib


class WorldFactbook():
    """A class to access data from the CIA World Factbook.

        Attributes:
            cache_folder (str or None): Optional folder path to cache data.
            use_cache (bool): Whether to use the cached data.
    """
    re_commas_outside_parenthesis = re.compile(",\n*(?=(?:[^()]*\([^()]*\))*[^()]*$)")
    re_percentage = re.compile("(\d+(\.\d+)?%)")
    re_parenthesis_and_content = re.compile("\(.*?\)")

    def __init__(self, cache_folder = None, use_cache = False):
        
        self.cache_folder = cache_folder
        self.use_cache = use_cache
        config_path = pathlib.Path(__file__).parent/ "world_factbook.json"
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        for key in config:
            setattr(self, key, config[key])

        self.source_information = {
            "name": "CIA World Factbook",
            "url": self.base_url,
            "copyright": "public domain",
            "accessed_on": datetime.date.today().isoformat(),
        }

    def get_url_data(self, url):
        if self.cache_folder:
            cache_path = pathlib.Path(self.cache_folder) / urllib.parse.quote(url)
            if self.use_cache and cache_path.exists():           
                with open(cache_path, "r") as cache_file:
                    return json.load(cache_file)
                
        response = requests.get(url)
        data = response.json()
        if self.cache_folder:
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_path, "w") as cache_file:
                json.dump(data, cache_file)
        return data
        

    def _deep_get(self, dict, keys):
        if not keys or dict is None:
            return dict
        return self._deep_get(dict.get(keys[0]), keys[1:])

    def get_field_country_comparison_data(self, field):
        formatted_data = {}
        field_country_comparison_url = "/".join(
            [
                self.base_url,
                self.data_path,
                self.field_path,
                field,
                self.country_comparison_path,
                self.data_file,
            ]
        )
        url_data = self.get_url_data(field_country_comparison_url)
        raw_data = self._deep_get(url_data, self.data_keys)
        for entry in self._deep_get(raw_data, self.country_comparison_entry_keys):
            place_name = self._deep_get(entry, self.country_comparison_place_name_keys)
            entry_fields = self._deep_get(entry, self.country_comparison_fields_keys)
            if entry_fields:
                field_value = self._deep_get(
                    entry_fields[0], self.country_comparison_value_keys
                )
                formatted_data[place_name] = html.unescape(field_value)
        return formatted_data

    def get_field_data(self, field):
        formatted_data = {}
        field_url = "/".join(
            [self.base_url, self.data_path, self.field_path, field, self.data_file]
        )
        url_data = self.get_url_data(field_url)
        raw_data = self._deep_get(url_data, self.data_keys)
        for entry in self._deep_get(raw_data, self.field_entry_keys):
            place_name = self._deep_get(entry, self.field_place_name_keys)
            field_value = self._deep_get(entry, self.field_value_keys)
            formatted_data[place_name] = html.unescape(field_value)
        return formatted_data

    def get_reference_data(self, reference):
        reference_url = "/".join(
            [
                self.base_url,
                self.data_path,
                self.references_path,
                reference,
                self.data_file,
            ]
        )
        url_data = self.get_url_data(reference_url)
        raw_data = self._deep_get(url_data, self.data_keys)
        entries = self._deep_get(raw_data, self.reference_entry_keys)
        return list(map(lambda entry: entry["fields"], entries))

    def field_to_percentage_data(self, field_data):
        return {
            place_name: self.string_to_percentage_data(field)
            for place_name, field in field_data.items()
        }
    
    def field_to_integer_data(self, field_data):
        return {
            place_name: int(field.strip() or 0)
            for place_name, field in field_data.items()
        }

    def string_to_percentage_data(self, input_string):
        substrings_and_note = self.string_to_list_of_strings_and_note(input_string)
        perecentage_data = list(
            map(
                lambda substring: self.substring_to_percentage_data(substring),
                substrings_and_note[0],
            )
        )
        note = substrings_and_note[1]
        return {"data": perecentage_data, "note": note}

    def string_to_list_of_strings_and_note(self, input_string):
        relevant_paragraph = input_string.split("<br>", 1)[0]

        list_and_note = relevant_paragraph.split(";", 1)

        list_of_strings = self.re_commas_outside_parenthesis.split(list_and_note[0])
        list_of_stripped_strings = list(
            map(lambda individual_string: individual_string.strip(), list_of_strings)
        )

        note = ""
        if len(list_and_note) > 1:
            note = list_and_note[1].replace("note -", "").strip()
        note_stripped = note.strip()

        return (list_of_stripped_strings, note_stripped)

    def substring_to_percentage_data(self, input_string):
        notes_with_parenthesis = self.re_parenthesis_and_content.findall(input_string)
        notes = list(map(lambda entry: entry[1:-1], notes_with_parenthesis))
        input_string_without_notes = self.re_parenthesis_and_content.sub(
            "", input_string
        )

        percentage_string_match = self.re_percentage.search(input_string_without_notes)
        fraction = None
        if percentage_string_match:
            percentage_string = percentage_string_match.group()
            fraction = float(percentage_string[:-1]) / 100
        input_string_without_notes_and_percentage = self.re_percentage.sub(
            "", input_string_without_notes
        )

        language = input_string_without_notes_and_percentage.strip()

        result = {"name": language, "fraction": fraction, "notes": notes}
        return result

    def get_languages_data(self):
        raw_language_data = self.get_field_data("languages")
        language_data = self.field_to_percentage_data(raw_language_data)
        return language_data

    def get_languages(self):
        languages_data = self.get_languages_data()
        languages = {
            country_name: {
                language["name"]: language["fraction"]
                for language in languages_with_notes["data"]
            }
            for country_name, languages_with_notes in languages_data.items()
        }
        return languages

    def get_populations(self):
        raw_population_data = self.get_field_country_comparison_data("population")
        populations = self.field_to_integer_data(raw_population_data)
        return populations

    def get_country_codes(self):
        country_data_codes = self.get_reference_data("country-data-codes")
        iso3_codes = {}
        for codes in country_data_codes:
            if codes[2] and "|" in codes[2]["value"]:
                iso3_codes[codes[0]["value"]] = codes[2]["value"].split("|")[1]
        return iso3_codes
    
    def get_language_codes(self):
        language_data_codes = self.get_reference_data("language-data-codes")
        iso693_2_codes = {}
        for codes in language_data_codes:
            iso693_2_codes[codes[0]["value"]] = codes[2]["value"]
        return iso693_2_codes

    def get_source_information(self):
        return self.source_information
