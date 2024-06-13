<?php
$link = mysqli_connect("localhost", "scott", "tiger", "instytut");

if (!$link) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}

$sql = "SELECT * FROM pracownicy";
$result = $link->query($sql);
?>
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Lista pracowników</title>
</head>
<body>
    <h1>Pracownicy</h1>
    <table border="1">
        <tr><th>ID_PRAC</th><th>NAZWISKO</th></tr>
        <?php
        while ($row = $result->fetch_assoc()) {
            echo "<tr><td>{$row['ID_PRAC']}</td><td>{$row['NAZWISKO']}</td></tr>";
        }
        ?>
    </table>
    <a href="form06_post.php">Dodaj nowego pracownika</a>
</body>
</html>
<?php
$result->free();
mysqli_close($link);
?>
