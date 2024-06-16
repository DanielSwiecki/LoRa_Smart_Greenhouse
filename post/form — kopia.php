<?php
// Connect to the MySQL database
$mysqlserverhost = "localhost";
$database_name = "test";
$username_mysql = "root";
$password_mysql = "";

function connect_to_mysqli($mysqlserverhost, $username_mysql, $password_mysql, $database_name){
    $connect = mysqli_connect($mysqlserverhost, $username_mysql, $password_mysql, $database_name);
    if (!$connect) {
        die("Connection failed: ". mysqli_connect_error());
    }
    return $connect;    
}

function saveDataAndSensorValuesToFile($rawData, $sensorValues) {
    // Determine the current user's desktop path
    $desktopPath = getenv('USERPROFILE'). '\\Desktop\\log_helium.txt';

    // Encode the sensor values as a JSON string
    $sensorValuesJson = json_encode($sensorValues);

    // Combine the raw data and sensor values JSON into a single string
    $combinedData = $rawData. "\n\n". $sensorValuesJson;

    // Append the combined data to the log file on the desktop
    file_put_contents($desktopPath, $combinedData, FILE_APPEND);
}



// Check if the request method is POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $connection = connect_to_mysqli($mysqlserverhost, $username_mysql, $password_mysql, $database_name);

    // Get the raw POST data
    $rawPostData = file_get_contents("php://input");

    $jsonArray = json_decode($rawPostData, true);

    // Check if decoding was successful and if "data" key exists
if ($jsonArray!== null && isset($jsonArray['data'])) {
    // Extract the "data" value
    $encodedData = $jsonArray['data'];

    // Decode the Base64 encoded data
    $decodedData = base64_decode($encodedData);



    // Extract the temperature, humidity, etc. from the ASCII data
    $sensorValues = [];
    for ($i = 0; $i < strlen($decodedData); $i += 4) {
        $hexValue = substr($decodedData, $i, 4);
        $decimalValue = hexdec($hexValue);
        $sensorValues[] = $decimalValue;
    }

    // Save the raw data to a file
    saveDataAndSensorValuesToFile($rawPostData, $sensorValues);

    // Scale and round temperature and humidity
    $scaledSensorValues = [
        round($sensorValues[0] / 100, 2), // Temperature
        round($sensorValues[1] / 100, 2), // Humidity
        $sensorValues[2], // TVOC
        $sensorValues[3], // eCO2
        $sensorValues[4], // Soil Moisture
        $sensorValues[5]  // Light
    ];

   // Insert the scaled sensor values into the database
$stmt = $connection->prepare("INSERT INTO table_form (temperature, humidity, tvoc, eco2, soil_moisture, light) VALUES (?,?,?,?,?,?)");
$stmt->bind_param("ddddii", $scaledSensorValues[0], $scaledSensorValues[1], $sensorValues[2], $sensorValues[3], $sensorValues[4], $sensorValues[5]);

if ($stmt->execute()) {
    echo "<h2><font color=blue>New record added to database.</font></h2>";
} else {
    echo "Error: ". $stmt->error;
}
$stmt->close();
mysqli_close($connection);
}
} else {
    // Handle cases other than POST requests
    echo "This script only accepts POST requests.";
}
?>
