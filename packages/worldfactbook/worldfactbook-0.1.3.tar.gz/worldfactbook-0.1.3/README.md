# WorldFactbook

**WorldFactbook** is a Python library that provides easy access to country-related data from the [**CIA World Factbook**](https://www.cia.gov/the-world-factbook/). It supports retrieving information about populations, languages, ISO codes, and more, with built-in caching for efficiency.

## Data Source
This project sources data from the **CIA World Factbook**, which is in the public domain. 
Please note that this project and its author are **not endorsed** by or affiliated with the authors of the Factbook.

The World Factbook 2024. Washington, DC: Central Intelligence Agency, 2024.
https://www.cia.gov/

## Features

- Fetch country data from the CIA World Factbook API  
- Retrieve language distribution, population, and ISO country codes  
- Supports caching to reduce redundant API calls  
- Processes and formats percentage-based data
- Provides lower level functions to access additonal fields  

## Installation

```sh
pip install worldfactbook
```

## Usage
```python
from worldfactbook import WorldFactbook

factbook = WorldFactbook(cache_folder="cache", use_cache=True)

# Get population data
populations = factbook.get_populations()
print(populations)

# Get language distribution
languages = factbook.get_languages()
print(languages)

# Get country ISO codes
country_codes = factbook.get_country_codes()
print(country_codes)

# Lower-level API calls
country_comparison_data = factbook.get_field_country_comparison_data("population")  # Get population comparison data
field_data = factbook.get_field_data("languages")  # Get field data like languages
reference_data = factbook.get_reference_data("country-data-codes")  # Get reference data for country codes
```
