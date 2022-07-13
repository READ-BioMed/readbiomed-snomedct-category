from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm

from tqdm.contrib.concurrent import process_map

import xlsxwriter

from predict import Category

category = Category(ontoserver_prefix="http://100.100.0.4:8080")


category_name = {
    "Results reference set for GP/FP reason for encounter": "Results / Plans",
    "Active immunisation": "Immunisation",
    "Respiratory tract infection": "Infection- Resp",
    "Traumatic AND/OR non-traumatic injury": "Injury / Musculoskeletal",
    "Abdominal pain": "Abdominal pain",
    "pain": "Pain syndrome",
    "Constipation": "Constipation / Bowels",
    "Eye / vision finding": "Ophthalmology",
    "Ear, nose and throat finding": "ENT - other",
    "Asthma": "Asthma and Allergy",
    "Disorder of skin": "Dermatology",
    "Mental illness": "Mental Health",
    "Female genitalia finding": "Gynae.",
    "Gastroesophageal reflux disease": "Reflux / Colic",
    "Poor sleep pattern": "Constitutional",
    "Infection": "Infection - other",
                 "Development disorder": "Developmental / Behavioural"
}


def map_category_name(category):
    return category_name[category] if category in category_name else category


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
                    worksheet.write(
                        row, column, map_category_name(categories.split("|")[1].split("#")[0]))
                else:
                    for c in categories:
                        worksheet.write(
                            row, column, map_category_name(c[0].split("|")[1].split("#")[0]))
                        column += 1


if __name__ == "__main__":
    #df = pd.read_csv('./input/Reasons_Freq.csv')
    df = pd.read_csv('./input/Reasons_Freq.csv')
    #df = pd.read_csv('/MCRI/input/Reasons_Freq.csv')

    print('Annotating terms...')
    mappings = process_map(category.get_category, df.Var1,
                           max_workers=1, chunksize=10)

    print('Writing results to xlsx file')
    write_results(mappings)
