<?php session_start(); ?>
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset='UTF-8' />
    <title>PHP</title>
</head>
<body>
    <?php
    require_once("funkcje.php");
    if (!isset($_SESSION['zalogowany']) || $_SESSION['zalogowany'] != 1) {
        header("Location: index.php");
    }
    echo "Zalogowano: " . $_SESSION['zalogowanyImie'];
    ?>
    <form action="index.php" method="POST">
        <input type="submit" name="wyloguj" value="Wyloguj">
    </form>

    <form action="user.php" method="POST" enctype="multipart/form-data">
        <fieldset>
            <legend>Prześlij plik</legend>
            <input type="file" name="plik" required><br>
            <input type="submit" name="upload" value="Prześlij">
        </fieldset>
    </form>

    <?php
    if (isset($_POST['upload'])) {
        $target_dir = "uploads/";
        $target_file = $target_dir . basename($_FILES["plik"]["name"]);
        if (move_uploaded_file($_FILES["plik"]["tmp_name"], $target_file)) {
            echo "Plik ". basename($_FILES["plik"]["name"]). " został przesłany.";
        } else {
            echo "Wystąpił błąd podczas przesyłania pliku.";
        }
    }
    ?>

    <a href="index.php">Powrót do strony głównej</a>
</body>
</html>
