# LCM

## How to run the project
```bash
python --version
python -m venv venv
venv\Scripts\activate
pip install requirements.txt
```

Before you run the project you need to put in your local database these files in order:

- [SQL DDL File](docs/DDL.sql "SQLFileQuestion")
- [SQL IDXs File](docs/IDXs.sql "SQLFileQuestion")
- [SQL SPs File](docs/SPs.sql "SQLFileQuestion")
- [SQL TRGs File](docs/TRGs.sql "SQLFileQuestion")
- [SQL UDFs File](docs/UDFs.sql "SQLFileQuestion")
- [SQL VIEWs File](docs/VIEWs.sql "SQLFileQuestion")

Then you need to run ther insertions files:

- [ChampionsInsert](docs/insertions/championsInsert.py "inserts")
- [SkinsInsert](docs/insertions/skinsInsert.py "inserts")
- [ChestsWardsMaps](docs/insertions/chests&wardsInsert.sql "inserts")

Then you can actually run the project
```bash
python run.py
```
