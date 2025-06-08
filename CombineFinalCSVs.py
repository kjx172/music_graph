import pandas as pd
from GraphData import visualize_data

foreign = pd.read_csv(r"CSV_GRAPHS\foreign\foreign.csv")
jazz = pd.read_csv(r"CSV_GRAPHS\jazz\jazz.csv")
misc = pd.read_csv(r"CSV_GRAPHS\misc\misc.csv")
mood = pd.read_csv(r"CSV_GRAPHS\mood\mood.csv")
old = pd.read_csv(r"CSV_GRAPHS\old\old.csv")
rb = pd.read_csv(r"CSV_GRAPHS\r&b\r&b.csv")
rap = pd.read_csv(r"CSV_GRAPHS\rap\rap.csv")
slow = pd.read_csv(r"CSV_GRAPHS\slow\slow.csv")

dfs = [foreign, jazz, misc, mood, old, rb, rap, slow]

combined_df = pd.concat((df for df in dfs), ignore_index=True)
combined_df.drop_duplicates()
combined_df.to_csv("final.csv", index=False)

visualize_data("final.csv")