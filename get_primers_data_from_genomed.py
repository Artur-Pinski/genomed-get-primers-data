import argparse  # for parsing command-line arguments
import getpass   # for prompting the user for their password
import pandas as pd  # for creating and manipulating the DataFrame containing the primer data
import time  # for pausing the script while the website loads information

import selenium  # for interacting with the website using a webdriver
from selenium.webdriver.common.by import By  # for locating elements on the webpage

def genomed_get_primers_data(username: str, pathway: str) -> pd.DataFrame:
    """
    This function logs in to the genomed website, iterates through the list of orders, extracts ID, 
    name, sequence,  price, Tm [°C], length, scale [µmol], purification, and remarks for each order, 
    and returns the data as a pandas dataframe.

    Parameters:
    username (str): The username to use to log in to the website.
    password (str): The password to use to log in to the website.
    pathway (str): The absolute pathway for Chrome drivers.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the ID, name, sequence, and price of each primer. 
    """
    # Get the password from the user
    password = getpass.getpass(prompt="Enter your password: ")
    
    try:
        # Initialize the webdriver and navigate to the website
        driver = webdriver.Chrome(executable_path=pathway)
        driver.get('https://www.genomed.pl/index.php/pl/moje-konto/oligonukleotydy')

        # Locate the login form elements
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "passwd")
        login_button = driver.find_element(By.CLASS_NAME, "pole_submit")

        # Fill in the login form and submit it
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        data = []
        data2 = []
        list_orders = []

        # Locate all the elements using their class name
        elements = driver.find_elements(By.CLASS_NAME, "span_rozwin")
        # Iterate through the elements
        for element in elements:    
        # Extract the element's ID
            element_id = element.get_attribute("id")
            list_orders.append(element_id)

        for orders in list_orders[:2]:

            # Click the element to expand it
            button = driver.find_element(By.ID, orders)
            button.click()

            # Find all elements containing the ID, name, sequence, and price of the primer
            id_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'ID:')]/b")
            tm_elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'Tm =')]")

            for tm_element in tm_elements:      
                data2.append(tm_element.text.split('\n'))

            for id_element in id_elements:            
                # Extract the text from the element
                data.append(id_element.text)


            button_element = driver.find_element(By.XPATH, "//a[@class='span_nie']")
            button_element.click()
        # Wait for the information to load (replace this with the appropriate waiting mechanism for your use case)
            time.sleep(1)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:    
        driver.quit()
    
    # Create a list of lists, with each inner list containing 4 elements
    primers_list_of_lists = [data[i:i+4] for i in range(0, len(data), 4)]

    # Create a DataFrame from the list of lists, with column names 'ID', 'Name', 'Sequence', and 'Price [zł]'
    primers_df = pd.DataFrame(primers_list_of_lists, columns=['ID', 'Name', 'Sequence', 'Price [zł]'])

    # Create a DataFrame from the list of lists, with column names 'Tm [°C]', 'Length', 'Scale [µmol]', 'Purification', and 'Remarks'
    additional_info_df = pd.DataFrame(data2, columns=['Tm [°C]', 'Length', 'Scale [µmol]', 'Purification', 'Remarks'])

    # Merge the two DataFrames into a single DataFrame
    merged_df = pd.concat([primers_df, additional_info_df], axis=1)
    
    return merged_df

def clean_genomed_primers_data(merged_df: pd.DataFrame) -> pd.DataFrame:
    """ This function cleans and converts the 'Price [zł]', 'Tm [°C]', 'Length', 'Scale [µmol]', 'Purification',
    and 'Remarks' columns of the DataFrame generated by get_primers_data_from_genomed function, 
    and returns the modified DataFrame.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to be cleaned and modified.

    Returns:
    pandas.DataFrame: The modified DataFrame. """

    try:
        # Replace ' zł' in the 'Price [zł]' column with an empty string, and convert the resulting values to float type
        merged_df['Price [zł]'] = merged_df['Price [zł]'].apply(lambda x: float(x.replace(' zł', '')))

        # Extract the floating-point number from the 'Tm [°C]' column and convert the resulting values to float type
        merged_df['Tm [°C]'] = merged_df['Tm [°C]'].str.extract('(\d+\.\d+)').astype(float)

        # Extract the integer from the 'Length' column and convert the resulting values to int type
        merged_df['Length'] = merged_df['Length'].str.extract('(\d+)').astype(int)

        # Extract the floating-point number from the 'Scale [µmol]' column and convert the resulting values to float type
        merged_df['Scale [µmol]'] = merged_df['Scale [µmol]'].str.extract('(\d+\.\d+)').astype(float)

        # Replace 'oczyszczanie: ' in the 'Purification' column with an empty string
        merged_df['Purification'] = merged_df['Purification'].apply(lambda x: x.replace('oczyszczanie: ', ''))

        # Replace 'Uwagi: ' in the 'Remarks' column with an empty string
        merged_df['Remarks'] = merged_df['Remarks'].apply(lambda x: x.replace('Uwagi:', ''))

        # Save the DataFrame to an Excel file
        merged_df.to_excel('genomed_primers.xlsx')
    
    except Exception as e:
        print(f"Error occurred: {e}")
    
    return merged_df  

def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--pathway", help="Absolute pathway for the Chrome driver executable")
    args = parser.parse_args()

    # Prompt the user for their username
    username = input("Enter your username: ")
    # Use the pathway provided as a command-line argument, or the default value if not provided
    pathway = args.pathway or r"chromedriver.exe"

    # Call the genomed_get_primers_data function and pass it the username, pathway, and password
    genomed_primers = genomed_get_primers_data(username=username, pathway=pathway)

    clean_genomed_primers = clean_genomed_primers_data(genomed_primers)
    # Print the resulting DataFrame
    
    return clean_genomed_primers
if __name__ == '__main__':
    main()
        
