import pandas as pd
file = "test_results_exam_2024_01_28.csv"
df = pd.read_csv(file, quotechar='"', delimiter=',',  engine='c', on_bad_lines='warn', skipinitialspace=True)
df.to_excel("test_results_exam_2024_01_28_excel.xlsx", index=False)