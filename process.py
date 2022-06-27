import pandas as pd
import xlsxwriter

from predict import Category

if __name__ == "__main__":
    df = pd.read_csv('./input/Reasons_Freq.csv')

    category = Category()

    with xlsxwriter.Workbook('./output/prediction.xlsx') as workbook:

        worksheet = workbook.add_worksheet("Prediction")

        row = 0

        # Write header
        worksheet.write(0, 0, 'Reason')

        for i in range(1,18):
            worksheet.write(0, i, 'Category')

        # Write output for terms
        for r in df.itertuples():
            row += 1
            worksheet.write(row, 0, r.Var1)

            categories = category.get_category(r.Var1)

            if categories is not None:
                column = 1

                for c in categories:
                    worksheet.write(row, column, c[0].split("|")[1])
                    column += 1
