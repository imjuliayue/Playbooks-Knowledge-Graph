# Description of Data:

-----------------------

## ROOT

`PostconditionsWTechDescr.csv` --- n rows, 3 columns
- rows containing: Postcondition ID, Postcondition Description, Technique Description

`PreconditionsWTechDescr.csv` --- ^^^

------------------------

## DI-R50_Data FOLDER

### Extraction SUBFOLDER

*Files coresponding to the randomly selected 50 Detect and Isolate techniques*

`DI-R50_Post-StringExtract.json` --- 1 row, 1 column
- All raw strings (not processed) combined into a single list ([["Expression", ["Predicates"...], ["Variables"...], ["Descriptions"]],...])

`DI-R50_Pre-StringExtract.json` --- ^^^




`DI-R50_Post-Processed.csv` --- n rows, 5 columns
- Processed strings, each row corresponds to: 1) [Cond ID, Cond Descr, Context], 2) Expression, 3) [Predicates], 4) [Variables], and 5) [Descriptions]

`DI-R50_Pre-Processed.csv` --- ^^^




`DI-R50_Post_Processed.pkl` --- n rows, 4 columns
- Processed strings, each row corresponds to: 1) Expressions, 2) [Predicates], 3) [Variables], and 4) [Descriptions]

`DI-R50_Pre_Processed.pkl` --- ^^^



`DI-R50_Post_Unique.csv` --- n rows, 5 columns
- Processed strings, each row corresponds to: 1) Expressions, 2) [Predicates], 3) [Variables], and 4) [Descriptions]
- CAVEAT: the predicates are ALL unique names (added number to end)

`DI-R50_Pre_Unique.csv` --- ^^^



`DI-R50_Post_Unique.pkl` --- n rows, 5 columns
- Processed strings, each row corresponds to: 1) Expressions, 2) [Predicates], 3) [Variables], and 4) [Descriptions]
- CAVEAT: the predicates are ALL unique names (added number to end)

`DI-R50_Pre_Unique.pkl` --- ^^^

### Clustering SUBFOLDER
`PostDI-R50_embeddings.txt` --- p rows, 1 column
- 
