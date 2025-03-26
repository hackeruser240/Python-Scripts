import win32com.client

# File paths
word_file = r"C:\Users\HP\OneDrive\Documents\Word Macro Prob\1Z0-1123-25.docm"
macro_file = r"C:\Users\HP\OneDrive\Documents\Word Macro Prob\Macro_DirectCertifyQA.txt"  

# Read the macro from the text file
with open(macro_file, "r", encoding="utf-8") as file:
    macro_code = file.read()

# Open Word
word = win32com.client.Dispatch("Word.Application")
word.Visible = True  # Show Word for debugging

# Open the Word document
doc = word.Documents.Open(word_file)

try:
    # Inject the VBA macro
    vb_component = word.VBE.ActiveVBProject.VBComponents("ThisDocument")
    vb_component.CodeModule.AddFromString(macro_code)

    # Run the macro
    word.Run("DirectCertifyQA")

    # Optional: Save the document after execution
    # doc.Save()

except Exception as e:
    print(f"Error: {e}")

# Optional: Close Word (comment out if you want to see changes before closing)
word.Quit()