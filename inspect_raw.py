file_path = "data/raw/VNIR_data.csv"

with open(file_path, "r", encoding="cp1252") as file:
    for i in range(10):
        line = file.readline()
        print(f"\nLine {i + 1}:")
        print(repr(line))