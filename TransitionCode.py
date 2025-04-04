import os 
import argparse as ag
import sys 

# renaming code in the v1 branch: 07-april-25 7:18 AM   
parser=ag.ArgumentParser(description="This is the transition folder code")
parser.add_argument("--parentPath", required=True, help="Enter the path!")
args=parser.parse_args()

#=========================================UDF's=========================================
def entriesCheck(mylist):
    
    mylist.sort()
    expected = set(range(0,mylist[-1]+1))
    actual=set(mylist)
    missing_numbers = expected - actual  # Find missing numbers
    
    if not missing_numbers:
        #print(f"All entries are present from {mylist[0]} to {len(mylist)}!")
        return True
    else:
        #print(f"Missing folders: {sorted(missing_numbers)}")
        return sorted(missing_numbers)       
    
def renamingFolderinTransitionFolder(old_path,transition_path,newlist,count):
    try:
        #old_path=old_path
        new_path=os.path.join(transition_path,f"{newlist[count]}")
        os.rename(old_path,new_path)
        print(f"Renamed '{old_path}' to '{new_path}' ")
    except:
        print("Issue in 'renamingFolderinTransitionFolder': ")
        print(f"cannot rename '{old_path}' to '{new_path}' ")
        print("Breaking the loop.")
        sys.exit()

def renamingFolderinParentPath(fullpath,parentPath,newlist,count):
    #print(old_path)
    try:
        #old_path=fullpath       
        new_path=os.path.join(parentPath,f"{newlist[count]}")
        os.rename(fullpath,new_path)
        #print(old_path)
        #print(new_path)
        print(f"Renamed '{fullpath}' to '{new_path}' ")
    except:
        print("Issue in 'renamingFolder' ")

def findingFolderNames(path):
    number=[]
    print(f"Finding Folder names in {path}")
    for folder in os.listdir(path):
        fullpath=os.path.join(path,folder)
        if os.path.isdir(fullpath) and folder.isdigit():
            number.append(int(folder))
    number.sort()
    return number

def firstTwoCases(path,number):
    '''
    This function renames the first two folders in the parentPath to '0' and '1'.
    '''
    number.sort()
    if number[0]!=0: 
        print("Folders do NOT begin with 0!")
        old_path=os.path.join(path,f"{number[0]}")   
        #print(old_path)
        new_path=os.path.join(path,"0")
        #print(new_path)
        os.rename(old_path,new_path)           
        print(f"Folder number {number[0]} has been renamed to 0")
        number[0]=0
        #number.sort()
        

        old_path=os.path.join(path,f"{number[1]}")   
        #print(old_path)
        new_path=os.path.join(path,"1")
        #print(new_path)
        os.rename(old_path,new_path)
        print(f"Folder number {number[1]} has been renamed to 1")
        number[1]=1
        number.sort()
        
    elif number[0]==0:
        if number[1]==1:
            print("Folder begins with 0 and next folder starts with 1!")
            #print(number)
        else:
            number[1]=2
            old_path=os.path.join(path,f"{number[1]}")            
            new_path=os.path.join(path,"1")
            os.rename(old_path,new_path )   
            print(f"Folder number {number[1]} has been renamed to 1")
            number.sort()

def movingTransitionPathFolders(transitionFolder,parentPath):
    print(f"Moving Folders from {transitionFolder} to {parentPath}")
    count=0
    old_path=[]
    new_path=[]

    try:
        for folderNumber in os.listdir(transitionFolder):
            src_path=os.path.join(transitionFolder,folderNumber)
            dest_path=os.path.join(parentPath,folderNumber)
        
            if os.path.isdir(src_path):  # Only move folders
                os.rename(src_path, dest_path)
                print(f"Moved Folder number {folderNumber} to {parentPath}")
                count+=1
        print(f"Total {count} folders moved from {transitionFolder} to {parentPath}")
    except:
        print("Error occured in 'movingTransitionPathFolders' ")

def checkingEmptyFolder(path):
    print("Checking empty folders (if any)!")
    count=0
    emptyFolder=[]
    for folder in os.listdir(path):
        fullpath=os.path.join(path,folder)
        if os.path.isdir(fullpath) and folder.isdigit():
            if not os.listdir(fullpath):           
                emptyFolder.append(fullpath)
    
    if not emptyFolder:
        print(f"No empty folder found in {path}")
    else:
        for fullpath in emptyFolder:
            try:
                os.rmdir(fullpath)
                print(f"{fullpath} is empty & removed!")
                count+=1
            except:
                print(f"{fullpath} could NOT be removed!")            
    
        print(f"Total {count} empty folder deleted from {path}")

def entriesCheckinTP(numoffoldersinparentFolder,mylist):
    
    mylist.sort()
    
    '''
    before 03-apr-25:
    expected = set(range(numoffoldersinparentFolder[-1],len(numoffoldersintransFolder)+numoffoldersinparentFolder[-1]+1 ))
    actual=set(numoffoldersintransFolder)
    '''
    
    #after 03-apr-25:
    expected = set(range(numoffoldersinparentFolder[-1],len(mylist)+numoffoldersinparentFolder[-1]+1 ))
    actual=set(mylist)

    missing_numbers = expected - actual  # Find missing numbers
    
    if not missing_numbers:
        #print(f"All entries are present from {mylist[0]} to {len(mylist)}!")
        return True
    else:
        #print(f"Missing folders: {sorted(missing_numbers)}")
        return sorted(missing_numbers)
    
def processingParentPath(parentPath):
    print("="*20,"Processing Parent Path","="*20)
    print(f"Detecting missing folders and renaming them in {parentPath}")

    #Checking for any empty folders and deleting them
    checkingEmptyFolder(parentPath)

    #Finding current folder names in parentPath
    number=findingFolderNames(parentPath)
    print("Existing folder names: ",number)

    #Checking if all the folders in parentPath are consistent or not
    result=entriesCheck(number)
    if result==True:
        print(f"All entries are in order from {number[0]} to {number[-1]}!")
    else:
        print(f"Missing folders in the Parent path: {result}")
        
        #Generating a new/proposed list for the folders in parent path
        newlist=[]
        for i in range(0,len(number)):
            newlist.append(i)
        print("Proposed new (folder) names:",newlist)
        
        #Special cases for the first and second folder!
        firstTwoCases(parentPath,number)
        
        for count,folder_number in enumerate(number):
            fullpath=os.path.join(parentPath,f"{folder_number}")
            if folder_number==0 or folder_number==1:        
                #this is because both of these cases have been dealt above
                pass
            if count<len(newlist)-1:
                renamingFolderinParentPath(fullpath,parentPath,newlist,count)
            elif count==len(newlist)-1: 
                renamingFolderinParentPath(fullpath,parentPath,newlist,count)
        
        print(f"Folders have been successfully processed in '{parentPath}' ")

def processingTransitionPath(transition_path):
    print("="*20,"Processing Transition Folder","="*20)
    print(f"Detecting missing folders and renaming them in {transition_path}")

    #Checking for any empty folders and deleting them!
    checkingEmptyFolder(parentPath)

    #number=[]
    numoffoldersinparentFolder=[]
    numoffoldersintransFolder=[]

    #finding the number of folders in the parent folder
    numoffoldersinparentFolder=findingFolderNames(parentPath)

    #finding the number of folders in the transition folder
    numoffoldersintransFolder=findingFolderNames(transition_path)

    numoffoldersinparentFolder.sort()
    numoffoldersintransFolder.sort()

    print(f"Total folder(s) in {parentPath}: {len(numoffoldersinparentFolder)}")
    print(f"Total folder(s) in {transition_path}: {len(numoffoldersintransFolder)}")


    if numoffoldersintransFolder == []:
        print("Transition folder is empty!")

    else:
        print(f"Existing names in {transition_path}:",numoffoldersintransFolder)
        result=entriesCheckinTP(numoffoldersinparentFolder,numoffoldersintransFolder)
        
        if result==True:
            print(f"All entries are in order from {numoffoldersintransFolder[0]} to {numoffoldersintransFolder[-1]}!")
        else:
            #print(f"Missing folders in the Transition path: {result}")
            
            #==========================Intermediate List==========================
            def intermediateList():
                newlist=[]
                for i in range( numoffoldersintransFolder[-1]+1 , (len(numoffoldersintransFolder)+numoffoldersintransFolder[-1]+1) ):
                    newlist.append(i)
                
                print(f"Proposed Intermediate names: {newlist}")
                
                print("Giving new Intermeidate folder names..")
                
                for count,folder in enumerate(numoffoldersintransFolder):
                    old_path=os.path.join(transition_path,f"{folder}")
                    if os.path.isdir(old_path) and count<len(newlist)-1:
                        renamingFolderinTransitionFolder(old_path,transition_path,newlist,count)    
                    elif os.path.isdir(old_path) and count==len(newlist)-1:
                        renamingFolderinTransitionFolder(old_path,transition_path,newlist,count)
                        print(f"Done renaming Intermediate folder(s) in {transition_path}")

            intermediateList()
            
            #==========================Final List==========================
            
            def finalList():
                #finding the number of folders in the transition folder
                numoffoldersintransFolder=findingFolderNames(transition_path)

                newlist=[]
                for i in range(len(numoffoldersinparentFolder),len(numoffoldersinparentFolder)+len(numoffoldersintransFolder)):
                    newlist.append(i)
                
                print(f"Proposed Final (folder) names: {newlist}")
                print(f"Total folder names: {len(newlist)}")

                print("Giving new Final folder names..")
            
                for count,folder in enumerate(numoffoldersintransFolder):
                    old_path=os.path.join(transition_path,f"{folder}")
                    print(f"old_path:{old_path}")
                    print(f"count:{count}")
                    
                    if os.path.isdir(old_path) and count<len(newlist)-1:
                        renamingFolderinTransitionFolder(old_path,transition_path,newlist,count)
                        print("here1")    
                    elif os.path.isdir(old_path) and count==len(newlist)-1:
                        renamingFolderinTransitionFolder(old_path,transition_path,newlist,count)
                        print("here2")         
                        print(f"Done renaming Final folder(s) in {transition_path}")

            finalList()
            movingTransitionPathFolders(transition_path,parentPath)

#==================================Getting Inputs==================================

#parentPath=r"E:\Images\0Z"
parentPath=rf"{args.parentPath}"
transition_path=os.path.join(parentPath,'Inter')

#==================================Processing Parent Path==================================

processingParentPath(parentPath)

#==================================Processing Transition Path==================================
processingTransitionPath(transition_path)