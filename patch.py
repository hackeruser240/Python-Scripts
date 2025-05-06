'''
Fixes the filenames

Attaches the preceding folder name in each individual CSV file
Case specific. Wouldn't work for every single case. Snippets can be taken.
'''
import os

basepath=r"C:\Users\HP\JupyterNotebooks\Yelp\Data\Apartments"

def hello():
        
        for item in folder_path:
            print(f"\n{item}")
            files=os.listdir(item)
            
            for file in files:
                
                if file=='First three PC characters.csv':
                    pass
                else:
                    print('\n')
                    old_name=os.path.join(item,file)
                    city_name=item.split('\\')[-1]
                    
                    temp=f"{city_name}_{file}"
                    new_name=os.path.join(item,temp)

                    print("old_name: ",old_name)
                    print("new_name: ",new_name)
                    os.rename(old_name,new_name)

            print(f"Done with {city_name}")

try:
    folder_names=os.listdir(basepath)
    folder_path=[ os.path.join(basepath,name) for name in folder_names]

    #print(f"\n{folder_path}")
    
    hello()
    
except Exception as e:
    print(e)