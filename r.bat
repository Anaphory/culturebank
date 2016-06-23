SET PGPASSWORD=blodig1kuk
dropdb -U postgres culturebank
createdb -U postgres culturebank
REM psql -U postgres -f pldb.sql linc
..\python culturebank/scripts/initializedb.py development.ini --module culturebank
REM > ntserr.log
pserve --reload development.ini
