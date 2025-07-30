<?php
// Определяем корневой каталог проекта
$root_path = realpath($_SERVER["DOCUMENT_ROOT"]) . '/test/';

// Включаем функции и config с использованием абсолютного пути
include_once $root_path . 'includes/functions.php';
include_once $root_path . 'config/database.php';

// Проверка на администратора
if (!isset($_SESSION['role']) || $_SESSION['role'] != 'admin') {
    header('Location: ../dashboard.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (!isset($_POST['request_id']) || !is_numeric($_POST['request_id'])) {
        redirectWithMessage('../admin/view_requests.php', "Некорректный ID заявки", 'danger');
    }
    
    $request_id = (int)$_POST['request_id'];
    $status = $_POST['status'];
    
    // Проверка статуса
    $valid_statuses = ['new', 'in_progress', 'completed', 'rejected'];
    if (!in_array($status, $valid_statuses)) {
        redirectWithMessage("../view_request.php?id=$request_id", "Некорректный статус", 'danger');
    }
    
    try {
        // Обновляем статус заявки
        $stmt = $pdo->prepare("UPDATE requests SET status = ? WHERE id = ?");
        $stmt->execute([$status, $request_id]);
        
        redirectWithMessage("../view_request.php?id=$request_id", "Статус заявки успешно обновлен", 'success');
    } catch (PDOException $e) {
        redirectWithMessage("../view_request.php?id=$request_id", "Ошибка базы данных: " . $e->getMessage(), 'danger');
    }
} else {
    redirectWithMessage('../admin/view_requests.php', "Некорректный метод запроса", 'danger');
}
?>