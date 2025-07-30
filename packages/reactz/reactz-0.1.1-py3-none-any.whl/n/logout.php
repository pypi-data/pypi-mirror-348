<?php
include_once 'includes/functions.php';

// Удаляем данные сессии
session_start();
session_unset();
session_destroy();

// Перенаправляем на страницу входа
header('Location: login.php');
exit;
?>