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
    for u in range (len(mylist)):
        if mylist[u+1] == mylist[u]+1:
            pass
        else:            
            print(f"the loop breaks at mylist[{u}] : { mylist[u]} ")
            print(f"the loop breaks at mylist[{u+1}] : { mylist[u+1]} ")
            breakingPoint=u
            break
    return breakingPoint

def renamingFiles(breakpoint2,numbers,strings,final):
    src,dst=[],[]
    result=0
    if len(numbers)!=0 and len(strings)!=0:
        result=result+1
    elif len(numbers)!=0:
        result=result
    elif len(strings)!=0:
        result =breakpoint2
    
    try:
        if len(numbers)+len(strings)  == len(final):
            for count,i in enumerate(range( result , len(final) ) ):
                #print(i)
                src.append( os.path.join(rf'{path}',str(final.loc[i,'Filenames']) + final.loc[i,'Extensions']) )
                dst.append( os.path.join(rf'{path}',str(final.loc[i,'New names']) + final.loc[i,'Extensions']) )
                print(f" {src[count]} renamed to {dst[count]} ")
                #print(f"{src[i]} renamed to {dst[i]}")
                os.rename(src[count],dst[count])
        else:
            print('hello')
    except Exception as e:
        print(f" 'numbers' and 'strings' have lengths of {len(numbers)} and {len(strings)} respectively. Some values are missing! ")
        print(f" final has {len(final)} length ")
        print(f" numbers has {len(numbers)} length ")
        print(f" strings has {len(strings)} length ")
        print("="*80)
        print(e)

def renamingStrings(numbers,strings):
    if len(numbers)==0:
        er=0
    else:
        er=numbers.iloc[-1]['New names']
    
    for i in range( len(strings) ):
        #print(i)
        strings.loc[i,'New names']= er + (i+1)
    
    strings[ 'New names' ]=strings[ 'New names' ].astype("Int64")
    print("="*20)
    print("Strings df:")
    print(strings.head())

#----------------------------------Main----------------------------------


path=rf'{args.path}'
media=rf'{args.media}'
numbers,strings=findMedia(media,path)

print("="*20)
print("Dataframe: ",numbers.head())
print("="*20)
print("Dataframe: ",strings.head())

if len(numbers)==0:
    print("There are no numeric filenames in the given path!")
elif len(numbers)!=0:
    #Sorting the numeric list:
    number_sorted=numbers.sort_values(by='Filenames',ascending=True,ignore_index=True)
    numbers=number_sorted
    breakpoint1=findingBreakingPoint( numbers['Filenames'] )

    #
    new_list=numbers['Filenames'][:breakpoint1].tolist()
    for i in range( breakpoint1+1,len(numbers)+1 ):
        new_list.append(i)
        breakpoint1 += 1 

    try:
        numbers['New names']=new_list # attaching the sorted list in the 'numbers' df. in a new column.
        #numbers.head( len(numbers) )
    except:
        print ("Both data types do not have same length! Some entries are missing!")

#Dealing with the strings:
# if the 'numbers' is empty, set the inital value to 1 otherwise last entry of 'numbers'

if len(strings)==0:
    print("Not processing any string names!")
    pass
else: 
    renamingStrings(numbers,strings)

#Combing both df's i.e. numbers and strings

final=pd.DataFrame()

if len(numbers)==0:
    final=strings
elif len(strings)==0:
    final=numbers
elif len(numbers) !=0 and len(strings)!=0:
    final=pd.concat([numbers,strings],ignore_index=True)
    final['New names'].astype("Int64")

print("Final combined df: \n")
print(final.head( len(final) ))

#Finally renaming the files:

breakpoint2=findingBreakingPoint(final['Filenames'])
renamingFiles(breakpoint2,numbers,strings,final)