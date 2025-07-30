<?php
session_start();
require_once 'db.php';

if(!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit;
}

$errors = [];

$stmt = $db->prepare("SELECT phone FROM users WHERE id = ?");
$stmt->execute([$_SESSION['user_id']]);
$user = $stmt->fetch();

$stmt = $db->prepare("SELECT id, name FROM services");
$stmt->execute();
$services = $stmt->fetchAll();

if($_SERVER['REQUEST_METHOD'] == 'POST') {
    $title = trim($_POST['title'] ?? '');
    $description = trim($_POST['description'] ?? '');
    $address = trim($_POST['address'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $date = $_POST['date'] ?? '';
    $time = $_POST['time'] ?? '';
    $service_id = $_POST['service_id'] ?? '';
    $custom_service = trim($_POST['custom_service'] ?? '');
    $payment_type = $_POST['payment_type'] ?? '';
    
    // Валидация
    if(empty($title)) $errors[] = "Укажите тему заявки";
    if(empty($description)) $errors[] = "Добавьте описание";
    if(empty($address)) $errors[] = "Введите адрес";

    $phone_digits = preg_replace('/\D/', '', $phone);
    if(strlen($phone_digits) < 10) {
        $errors[] = "Введите корректный номер телефона (минимум 10 цифр)";
    }
    
    if(empty($date) || empty($time)) $errors[] = "Выберите дату и время";
    if(empty($service_id) && empty($custom_service)) $errors[] = "Выберите услугу или опишите свою";
    if(empty($payment_type)) $errors[] = "Выберите способ оплаты";
    
    if(empty($errors)) {
        if(strlen($phone_digits) == 11 && ($phone_digits[0] == '7' || $phone_digits[0] == '8')) {
            $formatted_phone = '+7(' . substr($phone_digits, 1, 3) . ')-' . 
                              substr($phone_digits, 4, 3) . '-' . 
                              substr($phone_digits, 7, 2) . '-' . 
                              substr($phone_digits, 9, 2);
        } else {
            $formatted_phone = $phone;
        }
        
        $service_date = $date . ' ' . $time . ':00';
        
        $stmt = $db->prepare("
            INSERT INTO requests 
            (user_id, title, description, address, phone, service_date, service_id, custom_service, payment_type) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ");
        $stmt->execute([
            $_SESSION['user_id'],
            $title,
            $description,
            $address,
            $formatted_phone,
            $service_date,
            $service_id ?: null,
            $custom_service,
            $payment_type
        ]);
        
        header("Location: requests.php?success=1");
        exit;
    }
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Создание заявки</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <h2>Создание заявки</h2>
                <a href="requests.php" class="btn btn-sm">Назад к заявкам</a>
            </div>
            
            <?php if(!empty($errors)): ?>
                <div class="alert alert-error">
                    <?php foreach($errors as $error): ?>
                        <p><?= $error ?></p>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>
            
            <form method="POST" class="form">
                <div class="form-group">
                    <label for="title">Тема заявки:</label>
                    <input type="text" id="title" name="title" value="<?= htmlspecialchars($title ?? '') ?>">
                </div>
                
                <div class="form-group">
                    <label for="description">Описание:</label>
                    <textarea id="description" name="description" rows="4"><?= htmlspecialchars($description ?? '') ?></textarea>
                </div>
                
                <div class="form-group">
                    <label for="address">Адрес:</label>
                    <input type="text" id="address" name="address" value="<?= htmlspecialchars($address ?? '') ?>">
                </div>
                
                <div class="form-group">
                    <label for="phone">Телефон:</label>
                    <input type="text" id="phone" name="phone" value="<?= htmlspecialchars($phone ?? $user['phone']) ?>">
                </div>
                
                <div class="form-row">
                    <div class="form-group flex-1">
                        <label for="date">Дата:</label>
                        <input type="date" id="date" name="date" value="<?= htmlspecialchars($date ?? '') ?>">
                    </div>
                    
                    <div class="form-group flex-1">
                        <label for="time">Время:</label>
                        <input type="time" id="time" name="time" value="<?= htmlspecialchars($time ?? '') ?>">
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="service_id">Вид услуги:</label>
                    <select id="service_id" name="service_id">
                        <option value="">Выберите услугу</option>
                        <?php foreach($services as $service): ?>
                            <option value="<?= $service['id'] ?>" <?= isset($service_id) && $service_id == $service['id'] ? 'selected' : '' ?>>
                                <?= htmlspecialchars($service['name']) ?>
                            </option>
                        <?php endforeach; ?>
                        <option value="other" <?= isset($service_id) && $service_id == 'other' ? 'selected' : '' ?>>Иная услуга</option>
                    </select>
                </div>
                
                <div id="custom_service_block" class="form-group" style="display: none;">
                    <label for="custom_service">Опишите услугу:</label>
                    <textarea id="custom_service" name="custom_service" rows="3"><?= htmlspecialchars($custom_service ?? '') ?></textarea>
                </div>
                
                <div class="form-group">
                    <label>Способ оплаты:</label>
                    <div class="radio-group">
                        <label>
                            <input type="radio" name="payment_type" value="Наличные" <?= isset($payment_type) && $payment_type == 'Наличные' ? 'checked' : '' ?>>
                            Наличные
                        </label>
                        <label>
                            <input type="radio" name="payment_type" value="Банковская карта" <?= isset($payment_type) && $payment_type == 'Банковская карта' ? 'checked' : '' ?>>
                            Банковская карта
                        </label>
                    </div>
                </div>
                
                <button type="submit" class="btn btn-primary">Отправить заявку</button>
            </form>
        </div>
    </div>

    <script>
        const serviceSelect = document.getElementById('service_id');
        const customServiceBlock = document.getElementById('custom_service_block');
        
        serviceSelect.addEventListener('change', function() {
            customServiceBlock.style.display = this.value === 'other' ? 'block' : 'none';
        });

        if(serviceSelect.value === 'other') {
            customServiceBlock.style.display = 'block';
        }
    </script>
</body>
</html>