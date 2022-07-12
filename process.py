from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm

from tqdm.contrib.concurrent import process_map

import xlsxwriter

from predict import Category

category = Category(ontoserver_prefix="http://0.0.0.0:8080")


def write_results(mappings, xlsx_file_name='./output/prediction.xlsx'):
    with xlsxwriter.Workbook(xlsx_file_name) as workbook:

        worksheet = workbook.add_worksheet("Prediction")

        row = 0

        # Write header
        worksheet.write(0, 0, 'Reason')

        for i in range(1, 18):
            worksheet.write(0, i, 'Category')

        # Write output for terms
        for term, categories in tqdm(mappings, total=len(mappings)):
            row += 1

            worksheet.write(row, 0, term)

            if categories is not None:
                column = 1

                if type(categories) is str:
                    worksheet.write(row, column, categories.split("|")[1])
                else:
                    for c in categories:
                        worksheet.write(row, column, c[0].split("|")[1])
                        column += 1


if __name__ == "__main__":
    df = pd.read_csv('./input/Reasons_Freq.csv')

    mappings = process_map(category.get_category, df.Var1,
                           max_workers=5, chunksize=10)

    write_results(mappings)
