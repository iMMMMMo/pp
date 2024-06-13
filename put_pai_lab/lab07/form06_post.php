<?php
session_start();
?>
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Dodaj pracownika</title>
</head>
<body>
    <form action="form06_redirect.php" method="POST">
        <fieldset>
            <legend>Dodaj pracownika</legend>
            <label for="id_prac">ID Pracownika:</label>
            <input type="text" name="id_prac" id="id_prac" required><br>
            <label for="nazwisko">Nazwisko:</label>
            <input type="text" name="nazwisko" id="nazwisko" required><br>
            <input type="submit" value="Wstaw">
            <input type="reset" value="Wyczyść">
        </fieldset>
    </form>
    <a href="form06_get.php">Lista pracowników</a>
    <?php
    if (isset($_SESSION['message'])) {
        echo $_SESSION['message'];
        unset($_SESSION['message']);
    }
    ?>
</body>
</html>
