<?php
session_start();

function isLoggedIn() {
    return isset($_SESSION['user_id']);
}

function isAdmin() {
    return isset($_SESSION['role']) && $_SESSION['role'] == 'admin';
}

function checkLogin() {
    if (!isLoggedIn()) {
        header('Location: login.php');
        exit;
    }
}

function checkAdmin() {
    if (!isAdmin()) {
        header('Location: dashboard.php');
        exit;
    }
}

function sanitizeInput($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

function redirectWithMessage($location, $message, $type = 'success') {
    $_SESSION['message'] = $message;
    $_SESSION['message_type'] = $type;
    header("Location: $location");
    exit;
}

function displayMessage() {
    if (isset($_SESSION['message'])) {
        $type = isset($_SESSION['message_type']) ? $_SESSION['message_type'] : 'info';
        echo '<div class="alert alert-' . $type . '">' . $_SESSION['message'] . '</div>';
        unset($_SESSION['message']);
        unset($_SESSION['message_type']);
    }
}

function getRequestStatusName($status) {
    $statuses = [
        'new' => 'Новая',
        'in_progress' => 'В обработке',
        'completed' => 'Выполнена',
        'rejected' => 'Отклонена'
    ];
    
    return isset($statuses[$status]) ? $statuses[$status] : 'Неизвестно';
}
?>