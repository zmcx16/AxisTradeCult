import os

def SymbolToPath(symbol, save_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(save_dir, "{}.csv".format(str(symbol)))

