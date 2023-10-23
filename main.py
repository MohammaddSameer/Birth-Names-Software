#!/usr/bin/env python3

# Libraries
import os
import sys
import getopt
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ethnicolr import census_ln
import ethnicolr


def view_name_popularity_over_years(df, province):
  while True:
    name = input("Enter a name to view its popularity over the years: ")
    if name.strip() == "":
      print("Please enter a name.")
      continue
    else:
      break

  name_data = df[df['NAME'] == name.upper()]

  if len(name_data) == 0:
    print(f"No data found for name '{name}'.")

  if len(name_data) == 0:
    return


  fig, ax = plt.subplots()
  for sex in ['F', 'M']:
    sex_data = name_data[name_data['SEX'] == sex]
    if len(sex_data) > 0:
      x = sex_data['YEAR']
      y = sex_data['COUNT']
      ax.plot(x, y, label=f'{sex} Count')
  ax.legend()
  ax.set_xlabel('Year')
  ax.set_ylabel(f"Number of babies named {name} ")
  ax.set_title(f"Popularity of name '{name}' over the years")

  # create the subfolder if it doesn't exist
  if not os.path.exists(f"{province}_graphs"):
    os.makedirs(f"{province}_graphs")

  # save the plot in the subfolder
  plt.savefig(f"{province}_graphs/{name}.png")
  plt.show()


def count_ratio(df):
    # Calculate the percentage of females in the 'SEX' column
    user_year = input("Enter the year: ")
    year_mask = df['YEAR'].astype(str) == user_year
    year_df = df[year_mask]

    if len(year_df) == 0:
        print("No data available for the selected year.")
        return

    num_females = (year_df['SEX'] == 'F').sum()
    total_people = len(year_df)
    percentage_females = num_females / total_people 
    percentage_males = (total_people - num_females) / total_people 
    ratio_ftom = percentage_females / percentage_males

    print(f"The ratio of female to male births is {ratio_ftom:.2f}:1")
    if percentage_females > percentage_males:
        print(f"More girls were born in {user_year} ")
    elif percentage_males > percentage_females:
        print("More boys were born in {user_year} ")
    else:
        print("Equal number of boys and girls were born")
    print(f"Percentage of females: {percentage_females:.2%}")
    print(f"Percentage of males: {percentage_males:.2%}")


def age_gen_group(df):

  grouped = df.groupby('NAME')['COUNT'].sum().reset_index()
  sorted_names = grouped.sort_values('COUNT', ascending=False)

  old_count = 0
  bb_count = 0
  gx_count = 0
  mil_count = 0
  gz_count = 0
  ga_count = 0

  for year in df['YEAR']:
    if int(year) <= 1946:
      old_count += 1
    elif 1946 <= int(year) <= 1964:
      bb_count += 1
    elif 1965 <= int(year) <= 1980:
      gx_count += 1
    elif 1981 <= int(year) <= 1996:
      mil_count += 1
    elif 1997 <= int(year) <= 2012:
      gz_count += 1
    elif 2013 <= int(year):
      ga_count += 1

  old_percent = (old_count / len(df['YEAR'])) * 100
  bb_percent = (bb_count / len(df['YEAR'])) * 100
  gx_percent = (gx_count / len(df['YEAR'])) * 100
  mil_percent = (mil_count / len(df['YEAR'])) * 100
  gz_percent = (gz_count / len(df['YEAR'])) * 100
  ga_percent = (ga_count / len(df['YEAR'])) * 100

  print("\nThe Percentages are as follows:\n")

  print(f"Old :{old_percent:.2f} %")
  print(f"Baby boomers : {bb_percent:.2f} %")
  print(f"Gen X : {gx_percent:.2f} %")
  print(f"Millenials : {mil_percent:.2f} %")
  print(f"Gen Z : {gz_percent:.2f} %")
  print(f"Gen Alpha : {ga_percent:.2f} %")




def name_rank(name, year):
    provinces = ['NB', 'NS', 'alberta']
    name = name.upper()
    found = False
    
    for province in provinces:
        filename = f'{province}Out.csv'
        df = pd.read_csv(filename)
        df = df[df['YEAR'] == year]  

        if name in df['FIRST NAME'].values and \
           any(df[df['FIRST NAME'] == name]['SEX'] == 'M'):
            df = df[df['SEX'] == 'M'] 
            df = df.sort_values('COUNT', ascending=False) 
            df = df.reset_index(drop=True)
            rank = df.index[df['FIRST NAME'] == name].tolist()[0] + 1  
            print(f'{name} ranked #{rank} in {province} in {year}.')
            found = True
        elif name in df['FIRST NAME'].values and \
             any(df[df['FIRST NAME'] == name]['SEX'] == 'F'):
            df = df[df['SEX'] == 'F'] 
            df = df.sort_values('COUNT', ascending=False) 
            df = df.reset_index(drop=True)
            rank = df.index[df['FIRST NAME'] == name].tolist()[0] + 1  
            print(f'{name} ranked #{rank} in {province} in {year}.')
            found = True
        else:
            print(f'{name} was not found in {province} in {year}.')
    
    if not found:
        print(f'{name} does not appear in any province in {year}.')



def view_top_X_names(df):
  grouped = df.groupby('NAME')['COUNT'].sum().reset_index()
  sorted_names = grouped.sort_values('COUNT', ascending=False)
  merged = pd.merge(sorted_names[['NAME', 'COUNT']], df[['NAME', 'SEX']], on='NAME', how='left')
  unique_names = merged.drop_duplicates('NAME')

  while True:
    try:
      x = int(input("Enter the number of top names to display: "))
      if x <= 0:
        print("Please enter a positive number.")
      elif x > len(unique_names):
        print(f"Only {len(unique_names)} unique names available in the data. Please enter a smaller number.")
      else:
        break
    except ValueError:
      print("Please enter a valid integer.")

  unique_names = unique_names.head(x)
  unique_names['RANK'] = range(1, len(unique_names) + 1)
  top_names = unique_names[['RANK', 'SEX', 'NAME', 'COUNT']].to_string(index=False)
  print(top_names)


def view_top_names(df):
  grouped = df.groupby('NAME')['COUNT'].sum().reset_index()
  sorted_names = grouped.sort_values('COUNT', ascending=False)
  merged = pd.merge(sorted_names[['NAME', 'COUNT']], df[['NAME', 'SEX']], on='NAME', how='left')
  unique_names = merged.drop_duplicates('NAME').head(10)
  unique_names['RANK'] = range(1, 11)
  top_names = unique_names[['RANK', 'SEX', 'NAME', 'COUNT']].to_string(index=False)
  print(top_names)


def view_top_names_for_year(df):
  min_year, max_year = df['YEAR'].min(), df['YEAR'].max()

  while True:
    year = input(f"Enter a year between {min_year} and {max_year} to view top names: ")
    if year.isdigit():
      year = int(year)
      if year >= min_year and year <= max_year:
        break
    print("Invalid input. Please enter a valid year.")

  df_for_year = df[df['YEAR'] == year]
  grouped = df_for_year.groupby('NAME')['COUNT'].sum().reset_index()
  sorted_names = grouped.sort_values('COUNT', ascending=False)
  unique_names = sorted_names.drop_duplicates('NAME').head(10)
  unique_names['RANK'] = range(1, 11)
  top_names = unique_names[['RANK', 'NAME', 'COUNT']].to_string(index=False)
  print(f"\nTop 10 names for year {year}:")
  print(top_names)



def search_name():

  year_list = []
  sex_list = []
  name_list = []
  count_list = []
  province_list = []
  index = 0
  df = []
  gender_list = []
  name = input("Enter a name to search for: ")
  gender = input("Enter sex (M or F) to search for (Enter B to see both): ")
  if gender.upper() == 'M':
    gender_list.append(gender.upper())
  elif gender.upper() == 'F':
    gender_list.append(gender.upper())
  elif gender.upper() == 'B':
    gender_list.append('M')
    gender_list.append('F')
  else:
    print("Invalid input.")
    return
  year = input("Enter a year to search from (Enter 0 to see all years): ")
  if year.isdigit():
    year = int(year)
  if (year < 1900 or year > 2022) and year != 0:
    print("Invalid year.")
    return

  print(" ")

  name_found = 0
  files = ['albertaOut.csv', 'NBOut.csv', 'NSOut.csv']
  for file in files:
    if file == 'albertaOut.csv':
      province = 'Alberta'
    elif file == 'NBOut.csv':
      province = 'New Brunswick'
    elif file == 'NSOut.csv':
      province = 'Nova Scotia'

    with open(file) as csv_file:
      next(csv_file)
      csv_reader = csv.reader(csv_file, delimiter=',')
      for row in csv_reader:
        if year == 0:
          if (row[2].lower()) == name.lower() and row[1] in gender_list:
            year_list.append(int(row[0]))
            sex_list.append(row[1])
            name_list.append(row[2])
            count_list.append(int(row[3]))
            province_list.append(province)
            name_found = 1
        else:
          if (row[2].lower()
              ) == name.lower() and row[1] in gender_list and int(
                row[0]) == year:
            year_list.append(int(row[0]))
            sex_list.append(row[1])
            name_list.append(row[2])
            count_list.append(int(row[3]))
            province_list.append(province)
            name_found = 1

  if name_found > 0:
    data = {
      'PROVINCE': province_list,
      'YEAR': year_list,
      'SEX': sex_list,
      'NAME': name_list,
      'COUNT': count_list
    }
    df.append(pd.DataFrame(data))

    df[index] = df[index].sort_values(['PROVINCE', 'YEAR'], ascending=[True, True])
    print_name = df[index][['PROVINCE', 'YEAR', 'SEX', 'NAME', 'COUNT']].to_string(index=False)
    print(print_name)

    if year != 0:
      print("---------------------------------------------")
      name_rank(name, int(year))

    df2 = df[index].groupby("PROVINCE").agg(
      Count=pd.NamedAgg(column="COUNT", aggfunc="sum"))

    df3 = df[index].groupby("SEX").agg(
      Count=pd.NamedAgg(column="COUNT", aggfunc="sum"))
    
    print("---------------------------------------------")
    print("Summary of name count from each province:")
    print(" ")
    print(df2)

    print("---------------------------------------------")
    print("Summary of name count of each sex:")
    print(" ")
    print(df3)
  
  else:
    print("Name not found in any province.")


def view_dataframe(df):
  print(df)


def ethnicity_names(df):

  print(census_ln(df, 'NAME'))


def main():

  while True:
    print("\n*********************************************")
    print("Please select a province to view data from:")
    print("1. Alberta")
    print("2. New Brunswick")
    print("3. Nova Scotia")
    print("4. Name Search in all Provinces")
    print("5. Exit")
    print("*********************************************\n")

    choice = input("Enter your choice (1-5): ")
    if choice == "1":
      file = 'albertaOut.csv'
      province = 'Alberta'
    elif choice == "2":
      file = 'NBOut.csv'
      province = 'NewBrunswick'
    elif choice == "3":
      file = 'NSOut.csv'
      province = 'NovaScotia'
    elif choice == "4":
      file = ''
      search_name()
      continue
    elif choice == "5":
      print("Exiting program...")
      return
    else:
      print("Invalid choice. Please try again.")
      continue
    if not os.path.isfile(file):
      print(f"Error: {file} does not exist. Exiting program...")
      return

    year_list = []
    sex_list = []
    name_list = []
    count_list = []

    index = 0
    df = []
    if choice != "4":
      with open(file) as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
          year_list.append(int(row[0]))
          sex_list.append(row[1])
          name_list.append(row[2])
          count_list.append(int(row[3]))

      data = {
        'YEAR': year_list,
        'SEX': sex_list,
        'NAME': name_list,
        'COUNT': count_list
      }

      graph = pd.DataFrame(data)
      df.append(pd.DataFrame(data))

      df[index] = df[index].sort_values(['COUNT'], ascending=False)

      print("\n*********************************************")
      print("Please select an option:")
      print("1. View data frame")
      print("2. View top 10 names for a specified year")
      print("3. View top 10 names")
      print("4. View top X names")
      print("5. Possible ethnicity from names")
      print("6. Graph name popularity over the years")
      print("7. View the percentage of Generations")
      print("8. Female to male ratio ")
      print("9. Return to the main menu")
      print("*********************************************\n")

      option = input("Enter your choice (1-8): ")
      if option == "1":
        view_dataframe(df[index])
      elif option == "2":
        view_top_names_for_year(df[index])
      elif option == "3":
        print("\nTop 10 names for province:")
        view_top_names(df[index])
      elif option == "4":
        view_top_X_names(df[index])
      elif option == "6":
        view_name_popularity_over_years(graph, province)
      elif option == "7":
        age_gen_group(df[index])
      elif option == "8":
        count_ratio(df[index])
      elif option == "9":
        continue

      elif option == "5":
        ethnicity_names(df[index])
      else:
        print("Invalid choice. Please try again.")



if __name__ == "__main__":
  main()
