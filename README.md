# JADParser
""" consists of
- JADP.py == the table def parser returns nds {}
-- format of tuples in nds
---table [ tna=' ', [colna [ iskey?=y/n , desc=' ', ["FK" [ tableName, ColName, LOVTableName, LOVColname, LOVKeyVal ]] ]]

- JADPx.py
-- executes and saves JADP nds into file

- SQLDataDict.py
-- creates tables in SQLite for data dictionary
--- see file for format

- SQLMaker.py (nds) 
-- creates tables from JADP nds

- SQLScreenMaker.py
-- creates simple entry and review screens from JADP nds
