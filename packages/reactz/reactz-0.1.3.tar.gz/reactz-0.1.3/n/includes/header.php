<?php 
// Определяем корневой каталог проекта
$root_path = realpath($_SERVER["DOCUMENT_ROOT"]) . '/test/';

// Включаем функции и базу данных с использованием абсолютного пути
include_once $root_path . 'includes/functions.php';
include_once $root_path . 'config/database.php'; 
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Система заявок</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/test/assets/css/style.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/test/index.php">Система заявок</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <?php if (isLoggedIn()): ?>
                        <li class="nav-item">
                            <a class="nav-link" href="/test/dashboard.php">Главная</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/test/new_request.php">Новая заявка</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/test/my_requests.php">Мои заявки</a>
                        </li>
                        <?php if (isAdmin()): ?>
                            <li class="nav-item">
                                <a class="nav-link" href="/test/admin/index.php">Админ панель</a>
                            </li>
                        <?php endif; ?>
                        <li class="nav-item">
                            <a class="nav-link" href="/test/logout.php">Выход (<?php echo $_SESSION['username']; ?>)</a>
                        </li>
                    <?php else: ?>
                        <li class="nav-item">
                            <a class="nav-link" href="/test/login.php">Вход</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="/test/register.php">Регистрация</a>
                        </li>
                    <?php endif; ?>
                </ul>
            </div>
        </div>
    </nav>
    
    <div class="container mt-4">
        <?php displayMessage(); ?>