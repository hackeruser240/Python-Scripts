import os
import sys
import argparse as ag
import pandas as pd
import fnmatch

parser=ag.ArgumentParser(description= '''
This script help in renaming media (images or video) in a given directory!
'''  )

parser.add_argument("--path", required=True, type=str, help='Enter the directory in which you want your images or videos renamed')
parser.add_argument("--media", required=True, type=str, choices=['images','videos'], help='Select the type fo media.')
args=parser.parse_args()

# --------------------------------UDF's--------------------------------

def findMedia(media,directory):
    if media in ['images' , 'image']:
        extensions = ('*.jpg', '*.jpeg', '*.png')
    elif media in ['video' , 'videos']:
        extensions = ('*.mp4', '*.mpeg', '*.mkv')
    else:
        print("Enter the correct media")
        sys.exit(1) # Exit if media type is incorrect

    number_names, extension1 =[],[]
    string_names, extension2= [],[]

    all_files=os.listdir(directory)

    for a in extensions:
        for filename in fnmatch.filter(os.listdir(directory), a):
            name = os.path.splitext(filename)[0]  # Get filename without extension
            ext = os.path.splitext(filename)[1]

            if name.isdigit():
                number_names.append( int(name) )
                extension1.append( ext )
            else:
                string_names.append( name )
                extension2.append( ext )

    df_numbers=pd.DataFrame( {"Filenames":number_names,"Extensions":extension1} )
    df_strings=pd.DataFrame( {"Filenames":string_names,"Extensions":extension2} )
    print(f"Total {len(all_files) - len(number_names) - len(string_names)} non-{media} file(s) are present in the directory!")
    return df_numbers,df_strings  # Return both lists

def findingBreakingPoint(mylist):
    # Ensure list is not empty and has at least two elements for comparison
    if len(mylist) < 2:
        return -1 # Indicate no breaking point for small lists

    for u in range (len(mylist) - 1): # Iterate up to len-2 to avoid index out of bounds
        if mylist[u+1] == mylist[u]+1:
            pass
        else:
            print(f"The loop breaks at mylist[{u}] : { mylist[u]} ")
            print(f"The loop breaks at mylist[{u+1}] : { mylist[u+1]} ")
            breakingPoint=u
            return breakingPoint
    return len(mylist) - 1 # If no break, return the last index

def renamingFiles(numbers, strings, final, path): # Added path as argument
    src,dst=[],[]
    # Determine the starting index for renaming.
    # We always iterate through the 'final' DataFrame from the beginning
    # and use its 'New names' column for the destination.
    # The 'result' variable from original code was causing confusion.

    try:
        # We need to iterate over all entries in the final DataFrame
        # as 'New names' are already prepared for all of them.
        for count,i in enumerate(range( len(final) ) ):
            original_filename = str(final.loc[i,'Filenames']) + final.loc[i,'Extensions']
            new_filename = str(final.loc[i,'New names']) + final.loc[i,'Extensions']

            current_src_path = os.path.join(path, original_filename)
            current_dst_path = os.path.join(path, new_filename)

            # Skip renaming if source and destination are already the same
            if current_src_path == current_dst_path:
                print(f"Skipping: {current_src_path} is already correctly named as {current_dst_path}")
                continue

            print(f" {current_src_path} renamed to {current_dst_path} ")
            os.rename(current_src_path, current_dst_path)

    except Exception as e:
        print(f" 'numbers' and 'strings' have lengths of {len(numbers)} and {len(strings)} respectively.")
        print(f" final has {len(final)} length ")
        print("="*80)
        print(e)

def renamingStrings(numbers_df, strings_df, starting_point_for_strings):
    # Ensure 'strings_df' is not an empty DataFrame before proceeding
    if strings_df.empty:
        return strings_df

    for i in range( len(strings_df) ):
        strings_df.loc[i,'New names']= starting_point_for_strings + i

    strings_df[ 'New names' ]=strings_df[ 'New names' ].astype("Int64")
    print("="*20)
    print("Strings df after renaming:")
    print(strings_df.head())
    return strings_df

#----------------------------------Main----------------------------------

path=rf'{args.path}'
media=rf'{args.media}'
numbers,strings=findMedia(media,path)

print("="*20)
print("Dataframe 'numbers' initial:")
print(numbers.head())
print("="*20)
print("Dataframe 'strings' initial:")
print(strings.head())

max_existing_number = 0
if not numbers.empty:
    # Sorting the numeric list:
    number_sorted=numbers.sort_values(by='Filenames',ascending=True,ignore_index=True)
    numbers=number_sorted

    # Generate a new list of names ensuring uniqueness and continuity
    # The problematic logic was here, assuming a simple breakpoint.
    # Instead, we should find the maximum existing number and continue from there.

    # Identify existing numeric filenames
    existing_numeric_names = set(numbers['Filenames'].tolist())

    new_names_for_numbers = []
    current_expected_number = 1
    # First, try to keep existing sequential numbers if they are correct
    for index, row in numbers.iterrows():
        if row['Filenames'] == current_expected_number:
            new_names_for_numbers.append(current_expected_number)
            current_expected_number += 1
        else:
            # If there's a gap or mis-ordered number, assign the next available sequential number
            while current_expected_number in existing_numeric_names:
                current_expected_number += 1
            new_names_for_numbers.append(current_expected_number)
            current_expected_number += 1

    numbers['New names'] = new_names_for_numbers
    print("="*20)
    print("Dataframe 'numbers' with 'New names':")
    print(numbers.head(len(numbers))) # Print all numbers for verification

    if not numbers.empty:
        max_existing_number = numbers['New names'].max()
else:
    print("There are no numeric filenames in the given path!")
    max_existing_number = 0 # If no numeric files, start string numbering from 1


# Dealing with the strings:
# The starting point for renaming string files should be the number AFTER the highest
# new name assigned to a numeric file.
starting_point_for_strings = max_existing_number + 1

if strings.empty:
    print("Not processing any string names!")
else:
    # Pass the calculated starting point to renamingStrings
    strings = renamingStrings(numbers, strings, starting_point_for_strings)

# Combing both df's i.e. numbers and strings

final=pd.DataFrame()

if numbers.empty and strings.empty:
    print("No media files found to rename.")
elif numbers.empty:
    final=strings
elif strings.empty:
    final=numbers
else: # Both numbers and strings exist
    final=pd.concat([numbers,strings],ignore_index=True)
    # Ensure 'New names' column is integer type in the combined DataFrame
    final['New names'] = final['New names'].astype("Int64")

# Sort final DataFrame by 'New names' to ensure correct processing order
if not final.empty:
    final = final.sort_values(by='New names', ascending=True, ignore_index=True)

print("="*20)
print("Final combined df: \n")
print(final.head( len(final) ))

# Finally renaming the files:
# No need for a breakpoint in 'final' for renaming anymore, as 'New names' are designed to be sequential.
renamingFiles(numbers, strings, final, path) # Pass path to renamingFiles