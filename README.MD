# Fisco

WORK IN PROGRESS

Fisco is a DSL built for automatic data extraction from documents stored as images and performing operations on it, which can be use to fasten the process of copying data from documents in physical formats.

At frst, it was created using Lark as a parsing toolkit. But the final version can be found in the folder [UPDATED-FROM-SCRATH](https://github.com/senpainikolay/PBL-DSL/tree/main/UPDATED-FROM-SCRATH), where the parser was built in Python from scratch, using the recursive descent method. 

This DSL can:
 - Extract Data from images and transform it into structured data (dataframes)
 - Perform computtions on dataframes (mode, mean, max, min, standard deviation, percentage, mean, sum)
 - Plot dataframes (displot, countplot, lmplot, scatterplot, barplot)
