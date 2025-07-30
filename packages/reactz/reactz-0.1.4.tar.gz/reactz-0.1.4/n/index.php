<?php
session_start();
require_once 'db.php';

if(isset($_SESSION['user_id'])) {
    if(isset($_SESSION['is_admin']) && $_SESSION['is_admin']) {
        header("Location: admin.php");
    } else {
        header("Location: requests.php");
    }
    exit;
} else {
    header("Location: login.php");
    exit;
}
?>