import pandas as pd
file = "test_data/exam_2022_08_24/exam_2022_08_24.csv"
df = pd.read_csv(file, quotechar='"', delimiter=',',  engine='c', on_bad_lines='warn', skipinitialspace=True)
df.to_excel("test_results_few_shot_220824.xlsx", index=False)