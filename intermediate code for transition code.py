import os

def processingTransitionPath(transition_path):
    print("=" * 20, "Processing Transition Folder", "=" * 20)
    print(f"Detecting missing folders and renaming them in {transition_path}")

    # Checking for any empty folders and deleting them!
    checkingEmptyFolder(parentPath)

    # Finding the number of folders in the parent and transition folders
    numoffoldersinparentFolder = sorted(findingFolderNames(parentPath))
    numoffoldersintransFolder = sorted(findingFolderNames(transition_path))

    print(f"Total folder(s) in {parentPath}: {len(numoffoldersinparentFolder)}")
    print(f"Total folder(s) in {transition_path}: {len(numoffoldersintransFolder)}")

    if not numoffoldersintransFolder:
        print("Transition folder is empty!")
        return

    print(f"Existing names in {transition_path}:", numoffoldersintransFolder)

    if entriesCheckinTP(numoffoldersinparentFolder, numoffoldersintransFolder):
        print(f"All entries are in order from {numoffoldersintransFolder[0]} to {numoffoldersintransFolder[-1]}!")
    else:
        intermediateList(numoffoldersintransFolder, transition_path)
        finalList(numoffoldersinparentFolder, transition_path)
        movingTransitionPathFolders(transition_path, parentPath)


def intermediateList(numoffoldersintransFolder, transition_path):
    """Handles intermediate renaming of folders in the transition path."""
    newlist = list(range(numoffoldersintransFolder[-1] + 1, len(numoffoldersintransFolder) + numoffoldersintransFolder[-1] + 1))
    
    print(f"Proposed Intermediate names: {newlist}")
    print("Giving new Intermediate folder names...")

    renameFolders(numoffoldersintransFolder, newlist, transition_path)
    print(f"Done renaming Intermediate folder(s) in {transition_path}")


def finalList(numoffoldersinparentFolder, transition_path):
    """Handles final renaming of folders in the transition path."""
    numoffoldersintransFolder = sorted(findingFolderNames(transition_path))
    newlist = list(range(len(numoffoldersinparentFolder), len(numoffoldersinparentFolder) + len(numoffoldersintransFolder)))

    print(f"Proposed Final (folder) names: {newlist}")
    print(f"Total folder names: {len(newlist)}")
    print("Giving new Final folder names...")

    renameFolders(numoffoldersintransFolder, newlist, transition_path)
    print(f"Done renaming Final folder(s) in {transition_path}")


def renameFolders(old_folders, new_names, transition_path):
    """Renames folders in transition path based on a new naming scheme."""
    for count, folder in enumerate(old_folders):
        old_path = os.path.join(transition_path, f"{folder}")
        if os.path.isdir(old_path):
            renamingFolderinTransitionFolder(old_path, transition_path, new_names, count)