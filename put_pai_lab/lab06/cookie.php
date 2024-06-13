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
    if (isset($_GET['utworzCookie'])) {
        $czas = test_input($_GET['czas']);
        setcookie("nazwa", "wartość", time() + $czas, "/");
        echo "Cookie zostało utworzone na $czas sekund.";
    }
    ?>
    <a href="index.php">Wstecz</a>
</body>
</html>
