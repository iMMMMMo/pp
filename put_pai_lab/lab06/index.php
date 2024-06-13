<?php session_start(); ?>
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset='UTF-8' />
    <title>PHP</title>
</head>
<body>
    <h1>Nasz system</h1>
    <?php
    require_once("funkcje.php");
    if (isset($_POST['wyloguj'])) {
        $_SESSION['zalogowany'] = 0;
        session_destroy();
    }
    if (isset($_POST['zaloguj'])) {
        $login = test_input($_POST['login']);
        $haslo = test_input($_POST['haslo']);
        if ($login == $osoba1->login && $haslo == $osoba1->haslo) {
            $_SESSION['zalogowanyImie'] = $osoba1->imieNazwisko;
            $_SESSION['zalogowany'] = 1;
            header("Location: user.php");
        } elseif ($login == $osoba2->login && $haslo == $osoba2->haslo) {
            $_SESSION['zalogowanyImie'] = $osoba2->imieNazwisko;
            $_SESSION['zalogowany'] = 1;
            header("Location: user.php");
        } else {
            echo "Błędny login lub hasło";
        }
    }
    ?>
    <form action="logowanie.php" method="POST">
        <fieldset>
            <legend>Logowanie</legend>
            <label for="login">Login:</label>
            <input type="text" name="login" id="login" required><br>
            <label for="haslo">Hasło:</label>
            <input type="password" name="haslo" id="haslo" required><br>
            <input type="submit" name="zaloguj" value="Zaloguj">
        </fieldset>
    </form>

    <form action="cookie.php" method="GET">
        <fieldset>
            <legend>Utwórz cookie</legend>
            <label for="czas">Czas życia (sekundy):</label>
            <input type="number" name="czas" id="czas" required><br>
            <input type="submit" name="utworzCookie" value="Utwórz Cookie">
        </fieldset>
    </form>

    <?php
    if (isset($_COOKIE['nazwa'])) {
        echo "Wartość cookie: " . $_COOKIE['nazwa'];
    }
    ?>
</body>
</html>
