<?php
session_start();
require_once 'db.php';

$error = '';
$success = isset($_GET['success']) ? $_GET['success'] : false;

if($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    $stmt = $db->prepare("SELECT id, password, role FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch();
    
    if($user && password_verify($password, $user['password'])) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $username;
        $_SESSION['is_admin'] = ($user['role'] == 'admin');
        
        if($user['role'] == 'admin') {
            header("Location: admin.php");
        } else {
            header("Location: requests.php");
        }
        exit;
    } else {
        $error = 'Неверный логин или пароль';
    }
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <div class="card">
            <h2>Вход в систему</h2>
            
            <?php if($success): ?>
                <div class="alert alert-success">
                    <p>Регистрация успешна! Теперь вы можете войти.</p>
                </div>
            <?php endif; ?>
            
            <?php if($error): ?>
                <div class="alert alert-error">
                    <p><?= $error ?></p>
                </div>
            <?php endif; ?>
            
            <form method="POST" class="form">
                <div class="form-group">
                    <label for="username">Логин:</label>
                    <input type="text" id="username" name="username">
                </div>
                
                <div class="form-group">
                    <label for="password">Пароль:</label>
                    <input type="password" id="password" name="password">
                </div>
                
                <button type="submit" class="btn btn-primary">Войти</button>
            </form>
            
            <div class="card-footer">
                <p>Ещё не зарегистрированы? <a href="register.php">Регистрация</a></p>
            </div>
        </div>
    </div>
</body>
</html>