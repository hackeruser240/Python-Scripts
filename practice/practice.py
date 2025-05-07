import pandas as pd

def hello() -> pd.DataFrame:
    numbers: list[int]=list(range(10))
    text: str='Hello World! NUST'
    rev: slice = slice(None,None,-1)
    
    print(numbers[rev])
    print(text[rev])

if __name__=='__main__':
    hello()