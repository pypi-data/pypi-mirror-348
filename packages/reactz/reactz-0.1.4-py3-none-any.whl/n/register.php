<?php
session_start();
require_once 'db.php'; 

$errors = [];

if($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';
    $fullname = trim($_POST['fullname'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $email = trim($_POST['email'] ?? '');

    if(empty($username)) $errors[] = "Введите логин";
    if(strlen($password) < 6) $errors[] = "Пароль должен быть от 6 символов";
    if(empty($fullname)) $errors[] = "Введите ФИО";
    if(empty($phone)) $errors[] = "Введите телефон";
    if(empty($email)) $errors[] = "Введите email";

    if(empty($errors)) {
        $stmt = $db->prepare("SELECT id FROM users WHERE username = ?");
        $stmt->execute([$username]);
        if($stmt->rowCount() > 0) $errors[] = "Логин уже занят";
    }
    
    if(empty($errors)) {
        $hash = password_hash($password, PASSWORD_DEFAULT);
        $stmt = $db->prepare("INSERT INTO users (username, password, fullname, phone, email) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$username, $hash, $fullname, $phone, $email]);
        
        header("Location: login.php?success=1");
        exit;
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Регистрация</h1>
    
    <?php if(!empty($errors)): ?>
        <div class="error">
            <?php foreach($errors as $error): ?>
                <p><?= $error ?></p>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
    
    <form method="POST">
        <label>Логин:
            <input type="text" name="username" value="<?= htmlspecialchars($username ?? '') ?>">
        </label>
        
        <label>Пароль (минимум 6 символов):
            <input type="password" name="password">
        </label>
        
        <label>ФИО:
            <input type="text" name="fullname" value="<?= htmlspecialchars($fullname ?? '') ?>">
        </label>
        
        <label>Телефон:
            <input type="text" name="phone" value="<?= htmlspecialchars($phone ?? '') ?>">
        </label>
        
        <label>Email:
            <input type="email" name="email" value="<?= htmlspecialchars($email ?? '') ?>">
        </label>
        
        <button type="submit">Зарегистрироваться</button>
    </form>
    
    <p style="text-align: center; margin-top: 20px;">
        <a href="login.php">Уже зарегистрированы? Войти</a>
    </p>
</body>
</html>