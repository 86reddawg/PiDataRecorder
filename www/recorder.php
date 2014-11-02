<?php
//Extract data from database in JSON format
    header('Content-type: application/json; charset=utf-8');
    function Grab($name) {
        if (isset($_GET[$name])){return $_GET[$name];}
        else {return NULL;}
    }
    $date = Grab('date');
    $db = new SQLite3('/home/pi/recorder.db');
    $results = $db->query("SELECT strftime('%s', stamp)*1000 as date, temp, relhum, abshum 
			    FROM data WHERE date(stamp) = '".$date."' ORDER BY date");
    $row = $results->fetchArray();
    echo "{\"label\":\"".$date."\",\"data\":";
    echo "[[".$row[0].",".$row[1].",".$row[2].",".$row[3]."]";

    while ($row = $results->fetchArray()) {
	echo ",[".$row[0].",".$row[1].",".$row[2].",".$row[3]."]";
    }
    echo "]}";
?>