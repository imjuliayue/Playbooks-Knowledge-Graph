# Description of Data:

-----------------------

### ROOT

`PostconditionsWTechDescr.csv` --- n rows, 3 columns
- rows containing: Postcondition ID, Postcondition Description, Technique Description

`PreconditionsWTechDescr.csv` --- ^^^

------------------------

### DI-R50_Data FOLDER

*Files coresponding to the randomly selected 50 Detect and Isolate techniques*

`DI-R50_Post-StringExtract.json` --- 1 row, 1 column
- All raw strings (not processed) combined into a single list ([["Expression", ["Predicates"...], ["Variables"...], ["Descriptions"]],...])

`DI-R50_Pre-StringExtract.json` --- ^^^




`DI-R50_Post-Processed.csv` --- n rows, 5 columns
- Processed strings, each row corresponds to: 1) [Cond ID, Cond Descr, Context], 2) Expression, 3) [Predicates], 4) [Variables], and 5) [Descriptions]

`DI-R50_Post-Processed.csv` --- ^^^
