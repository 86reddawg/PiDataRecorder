PiDataRecorder
==============

Continuous measurement/display of temp/humidity
Requires flot <http://www.flotcharts.org/> for web graph display

Create an sqlite3 database "recorder.db" and setup a table like:
create table data(temp INTEGER, relhum INTEGER, abshum INTEGER, stamp DATETIME default CURRENT_TIMESTAMP);

When PiDataRecorder is ran, it will collect temperature, percent humidity, and timestamp.  Script will then
calculate absolute humidity, and dump data into database.

index.php looks for any recordings and lists the days it finds data.  Clicking on the day button will
then request JSON data through recorder.php and display in the graph window.
