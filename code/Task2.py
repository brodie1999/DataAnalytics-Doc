import os
import pandas as pd 
import json 
import argparse
import pycountry
from pycountry_convert import country_alpha2_to_continent_code, convert_continent_code_to_continent_name, country_name_to_country_alpha2
from collections import defaultdict
import matplotlib
from matplotlib import pyplot as plt 

def load_country_to_map(mapPath):
    """
    Load country-to-contient mapping from a CSV file 
    :param map_path: path to the CSV file with country-to-continent mappings 
    :return: Dictionary mapping country codes to continents. 
    """
    map_df = pd.read_csv(mapPath)
    return map_df.set_index('alpha-2')['region'].to_dict()

def process_views_by_country(documentID, jsonPath):
    """
    Process JSON data to count document views by country for a specific document ID 
    :param docID: The unique identifier of the document to filter by. 
    :param jsonPath: Path to the JSON file. 
    :return: Dictionary with counts of views grouped by country 
    """
    country_views = defaultdict(int)

    with open(jsonPath, 'r') as file: 
        for line in file: 
            event = json.loads(line)
            if event.get("env_type") == "reader" and event.get("subject_doc_id") == documentID:
                country = event.get("visitor_country")
                if country: 
                    country_views[country] += 1
    return dict(country_views)

def process_views_by_continent(documentID, json_file):
    """
    Process a json file data to count document views by continent for 
    specific document ID 
    :param documentID: Unique identifier of the document
    :param json_file: path to json file 
    :return: Series with counts of views grouped by continent.    
    """
    # Get Continent views
    # First load in data from json file 
    # Allow data to be global in order to access its value later when mapping countries to continents
    global continent_data 
    try: 
        with open(json_file, 'r') as file:
            unparsed_data = file.read()
        jsonOBJ = unparsed_data.strip().split("\n")
        continent_data = [json.loads(obj) for obj in jsonOBJ]
    except FileNotFoundError: 
        print("File not found: {json_file} ")
    # Create list of countries 
    countries = [obj.get("visitor_country") for obj in continent_data if (obj.get("subject_doc_id") == documentID)]

    #Create list of all continents and map countries to continents
    #i.e. Brazil => South America etc...
    continents = [convert_continent_code_to_continent_name(country_alpha2_to_continent_code(country)) for country in countries]
    return pd.Series(continents).value_counts()

# Plot bar chart 
def plot_chart(data, title, xlabel, ylabel):

    # Test Plotting logic 

    """
    Plot bart chart from the data obtained 
    data: Dictionary containing labels and counts to plot 
    title: Title of Bar Chart 
    xlabel: Label for the x-axis 
    ylabel: Label for the y-axis 
    """

    if not data: 
        print("No Data available to plot...")
        return     
    try: 
        data, counts = zip(*data.items())
        fig = plt.figure(figsize=(10, 5))
        plt.bar(data, counts, linewidth=2)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig("BarChart.png") # Save bar chart to file 
        plt.show()
    except ValueError: 
        print("Error: Please check input structure")
        return
    except Exception as e: 
        print(f"Error occured during plotting...", e)