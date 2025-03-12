

def fuzzy_merge(df_1, df_2, col_1, col_2):
    df_2[col_2] = df_2[col_2].apply(str)
    df_1[col_1] = df_1[col_1].apply(str)

    df_2[col_1] = df_2[col_2]
    df_1 = df_1.drop_duplicates(subset=[col_1], keep='first')
    df_1["new"] = "1"

    list_1 = df_1[[col_1, "new"]]
    list_1["new"] = "1"
    list_2 = df_2[[col_2, col_1]]
    prvy_merge = list_1.merge(list_2, how='left', on=[col_1])
    prvy_merge.loc[prvy_merge[col_2].isna()==True, col_2]=""


    prvy_merge.loc[prvy_merge[col_2] =="", col_2] = prvy_merge[col_1].apply(lambda x: process.extractOne(x, df_2[col_2], scorer=fuzz.token_sort_ratio)[0])
    final =df_1.merge(prvy_merge, how='left', on=[col_1])
    
    final=final.merge(df_2, how='outer', on=col_2)
    return final