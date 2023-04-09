"""
Description:
 Generates a CSV reports containing all married couples in
 the Social Network database.

Usage:
 python marriage_report.py
"""
import os
import sqlite3
from create_db import get_script_dir
import pandas as pd


def main():
    global db_path
    db_path = os.path.join(get_script_dir(), 'social_network.db')

    # Query DB for list of married couples
    married_couples = get_married_couples()

    # Save all married couples to CSV file
    csv_path = os.path.join(get_script_dir(), 'married_couples.csv')
    save_married_couples_csv(married_couples, csv_path)


def get_married_couples():
    """Queries the Social Network database for all married couples.

    Returns:
        list: (name1, name2, start_date) of married couples 
    """

    con = sqlite3.connect(db_path)

    cur = con.cursor()

    # all_relationships_query = """
    #                         SELECT person1.name, person2.name, start_date FROM relationships
    #                         JOIN people person1 ON person1_id = person1.id
    #                         JOIN people person2 ON person2_id = person2.id
    #                     """

    all_relationships_query = """
                            SELECT p1.name as Person1, p2.name as Person2, relationships.start_date FROM people p1, people p2, relationships 
                            WHERE p1.id = relationships.person1_id 
                            AND p2.id = relationships.person2_id 
                            AND relationships.type = 'spouse'
                        """

    # Execute the query and get all results
    cur.execute(all_relationships_query)

    all_relationships = cur.fetchall()
    con.close()

    # # Print sentences describing each relationship
    for person1, person2, start_date in all_relationships:
        print(f'{person1} is married to {person2} since {start_date}.')

    return all_relationships


def save_married_couples_csv(married_couples, csv_path):
    """Saves list of married couples to a CSV file, including both people's 
    names and their wedding anniversary date  

    Args:
        married_couples (list): (name1, name2, start_date) of married couples
        csv_path (str): Path of CSV file
    """
    df = pd.DataFrame(married_couples, columns=[
                      'Person 1', 'Person 2', 'Anniversary'])
    df.to_csv(csv_path, header=True, index=False)


if __name__ == '__main__':
    main()
