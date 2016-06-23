
Releasing culturebank
==================

- Update the glottobank/Culturebank repository
- Run the checks on the data repos:
```
culturebank check
```
- Recreate the database
- Recompute coverage information running
```
cd culturebank/coverage
./coverage.sh
```
- Run the tests
