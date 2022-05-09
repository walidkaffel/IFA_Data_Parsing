# -*- coding: utf-8 -*-
"""
Created on Sun May  8 18:22:50 2022

@author: walid
"""

import parameters as param
import os
import glob
import pandas as pd
import re


def exports_extraction(xfile, xsheet):

    
    product = xsheet.split('Exports')[0].strip()
    if product == 'Phosphoric Acid':
        product = 'PA'
    year = re.findall("[0-9]{4}",xfile)[0]

    print(product, '--', year)
    
    df_export = pd.read_excel(xfile, xsheet, header=4)
    df_export = df_export.rename(mapper={df_export.columns[0]:'Importer'}, axis=1)
    df_export = df_export.drop([0, 1], axis=0)
    df_export = df_export.drop(labels=df_export.columns[-4:], axis=1)
    df_export = df_export.drop(labels=df_export.columns[1:3], axis=1)
    df_export = df_export[df_export['Importer'].notnull()]
    df_export = df_export[df_export['Importer'].apply(lambda x : ((x.find('Total') == -1) & (x.find('Variation') == -1)))]

    subtotal_selector = df_export[['Importer', df_export.columns[-1]]]
    subtotal_importers_selector = subtotal_selector[subtotal_selector[df_export.columns[-1]].isnull()]['Importer'].values
    subtotal_importers_selector_index = subtotal_selector[subtotal_selector[df_export.columns[-1]].isnull()]['Importer'].index.values
    subtotal_sum_selector_index = subtotal_selector[subtotal_selector['Importer'] == 'Subtotal']['Importer'].index.values

    df_export['Region_Importer'] = df_export['Importer']
    selector = 0
    for ind in df_export.index:
        if selector < len(subtotal_sum_selector_index):
            if ind <= subtotal_sum_selector_index[selector]:
                df_export.loc[ind, ['Region_Importer']] = subtotal_importers_selector[selector]

            if ind == subtotal_sum_selector_index[selector]:
                selector += 1



    df_export = df_export.drop(subtotal_importers_selector_index, axis=0)
    df_export.loc[subtotal_sum_selector_index, ['Importer']] = subtotal_importers_selector


    df_export = df_export.reset_index(drop=True)
    various_selector = df_export.loc[df_export['Importer']=='Various',].index
    for elt in various_selector:
        df_export.loc[elt, ['Importer']] = df_export.loc[elt, ['Importer']] + ' ' + df_export.loc[elt+1, ['Importer']]

    df_export['Product'] = product
    df_export['Year'] = year
    df_export = df_export.set_index(['Region_Importer', 'Importer', 'Product', 'Year']).stack().reset_index()
    df_export = df_export.rename(mapper={df_export.columns[-1]:'Value', df_export.columns[-2]:'Exporter'}, axis=1)
    
    df_export = df_export[df_export['Value'] > 1]
    df_export = df_export.rename(mapper={df_export.columns[4]:'Country'}, axis=1)
    
    df_export['Type'] = 'Export'
    
    df_export = df_export[['Country', 'Type', 'Year', 'Product','Region_Importer', 'Importer', 'Value']]
    
    df_export = df_export.rename(mapper={df_export.columns[5]:'Partner'}, axis=1)
    df_export = df_export.rename(mapper={df_export.columns[4]:'Region_Partner'}, axis=1)
    
    return df_export



result = pd.DataFrame()

list_of_files = glob.glob(param.extracted_files_repo+'/*')
for xfile in list_of_files:
    xls = pd.ExcelFile(xfile)
 
    for elt_sheet in xls.sheet_names:
        if elt_sheet.find('Exports') != -1:

            result = result.append(exports_extraction(xfile, elt_sheet))

result