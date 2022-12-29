# Scraping Primers Data from Genomed Website

This script scrapes data about primers from the [Genomed website](http://www.genomed.pl) and save the data in a Pandas DataFrame and an Excel file. The data includes the ID, name, sequence, and price of each primer, as well as their Tm [°C], length, scale [µmol], purification, and remarks.

## Functionality

* `get_primers_data_from_genomed`: This function takes in a username and pathway as arguments and returns a Pandas DataFrame with the data about the primers. The user is prompted to enter their password in a secured way.
* `clean_genomed_primers_data`: This function takes in a DataFrame from get_primers_data_from_genomed as an argument and modifies the 'Price [zł]', 'Tm [°C]', 'Length', 'Scale [µmol]', 'Purification', and 'Remarks' columns of the DataFrame. The modified DataFrame and Excel file (genomed_primers.xlsx) are then returned by the function.
* `main`: This is the main function that ties everything together. It prompts the user for their username, calls `get_primers_data_from_genomed` and `clean_genomed_primers_data`, and saves the resulting DataFrame and Excel file.

## Dependencies
This function requires the following dependencies:

* `getpass`: for prompting the user for their password.
* `time`: for pausing the script while the website loads information.
* `argparse`: for parsing command-line arguments.
* `pandas`: for creating and manipulating the DataFrame containing the primer data.
* `selenium`: for interacting with the website using a webdriver.
* `time`: is used to for pausing the script while the website loads information, to ensure that all data is properly retrieved

It is also necessary to have the [Chrome webdriver](https://chromedriver.chromium.org/downloads) installed and the path to the executable specified in the pathway parameter.

## How to run

You can simply run the script without any additional arguments. The default pathway is set to the current directory, which assumes that the Chrome driver executable (chromedriver.exe) is located in the same directory as the script. If you want to run the script with a different pathway, you can use the `--pathway` option followed by the desired path: `python get_primers_data_from_genomed_test.py --pathway '/path/to/chromedriver'`
