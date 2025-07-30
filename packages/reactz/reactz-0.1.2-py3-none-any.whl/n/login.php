<?php
include_once 'includes/header.php';

// Для отладки
function debug_to_file($data, $append = true) {
    $file = 'debug_log.txt';
    $content = date('Y-m-d H:i:s') . " - " . print_r($data, true) . "\n";
    file_put_contents($file, $content, $append ? FILE_APPEND : 0);
}

// Если пользователь уже вошел, перенаправляем на дашборд
if (isLoggedIn()) {
    header('Location: dashboard.php');
    exit;
}

$errors = [];

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = sanitizeInput($_POST['username']);
    $password = $_POST['password'];
    
    // Проверка валидности данных
    if (empty($username)) {
        $errors[] = "Имя пользователя обязательно";
    }
    
    if (empty($password)) {
        $errors[] = "Пароль обязателен";
    }
    
    // Если нет ошибок, проверяем данные пользователя
    if (empty($errors)) {
        try {
            // Ищем пользователя в БД
            $stmt = $pdo->prepare("SELECT id, username, password, role FROM users WHERE username = ?");
            $stmt->execute([$username]);
            
            // Отладка
            debug_to_file("Username попытка входа: " . $username);
            debug_to_file("Найдено записей: " . $stmt->rowCount());
            
            if ($stmt->rowCount() > 0) {
                $user = $stmt->fetch(PDO::FETCH_ASSOC);
                debug_to_file("User данные: " . print_r($user, true));
                debug_to_file("Введенный пароль: " . $password);
                debug_to_file("Хеш в базе: " . $user['password']);
                
                // Проверяем пароль
                $password_verify_result = password_verify($password, $user['password']);
                debug_to_file("Результат проверки: " . ($password_verify_result ? 'true' : 'false'));
                
                if ($password_verify_result) {
                    // Сохраняем данные пользователя в сессии
                    $_SESSION['user_id'] = $user['id'];
                    $_SESSION['username'] = $user['username'];
                    $_SESSION['role'] = $user['role'];
                    
                    debug_to_file("Вход успешен, перенаправление на dashboard.php");
                    redirectWithMessage('dashboard.php', "Добро пожаловать, {$user['username']}!", 'success');
                } else {
                    $errors[] = "Неверный пароль";
                }
            } else {
                $errors[] = "Пользователь с таким именем не найден";
            }
        } catch (PDOException $e) {
            $errors[] = "Ошибка базы данных: " . $e->getMessage();
            debug_to_file("Ошибка PDO: " . $e->getMessage());
        }
    }
}
?>

<div class="login-form">
    <div class="card">
        <div class="card-header">
            <h3 class="text-center">Вход в систему</h3>
        </div>
        <div class="card-body">
            <?php if (!empty($errors)): ?>
                <div class="alert alert-danger">
                    <ul class="mb-0">
                        <?php foreach ($errors as $error): ?>
                            <li><?php echo $error; ?></li>
                        <?php endforeach; ?>
                    </ul>
                </div>
            <?php endif; ?>
            
            <form action="login.php" method="post">
                <div class="mb-3">
                    <label for="username" class="form-label">Имя пользователя</label>
                    <input type="text" class="form-control" id="username" name="username" value="<?php echo isset($username) ? $username : ''; ?>" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Пароль</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </div>
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary">Войти</button>
                </div>
            </form>
        </div>
        <div class="card-footer text-center">
            <p class="mb-0">Нет аккаунта? <a href="register.php">Зарегистрируйтесь</a></p>
        </div>
    </div>
</div>

<?php include_once 'includes/footer.php'; ?>