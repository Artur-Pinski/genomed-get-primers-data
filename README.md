# Scraping Primers Data from Genomed Website

This script scrapes data about primers from the [Genomed website](http://www.genomed.pl) and save the data in a Pandas DataFrame and an Excel file. The data includes the ID, name, sequence, and price of each primer, as well as their Tm [°C], length, scale [µmol], purification, and remarks.

## Functionality
The script defines a function called `get_primers_data_from_genomed`, which takes in two arguments: `username` and `pathway`. The username is the user's login credentials for the Genomed website, while the pathway is the absolute pathway for the Chrome driver executable. Inside the function, the user is prompted to enter their password in a secured way. The function returns a Pandas DataFrame containing the data about the primers.

The `clean_genomed_primers_data` function takes in a `DataFrame` from `get_primers_data_from_genomed` function as an argument and modifies the 'Price [zł]', 'Tm [°C]', 'Length', 'Scale [µmol]', 'Purification', and 'Remarks' columns of the DataFrame. The modified DataFrame and Excel file are then returned by the function.

## Dependencies
This function requires the following dependencies:

* `getpass`: for prompting the user for their password.
* `selenium`: for interacting with the website using a webdriver.
* `pandas`: for creating and manipulating the DataFrame containing the primer data.
* `time`: for waiting during information loading.

It is also necessary to have the Chrome webdriver installed and the path to the executable specified in the pathway parameter.
