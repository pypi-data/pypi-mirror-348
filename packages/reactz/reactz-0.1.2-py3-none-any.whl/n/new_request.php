<?php
include_once 'includes/header.php';
checkLogin();

$errors = [];

// Проверяем существование пользователя
try {
    $stmt = $pdo->prepare("SELECT id FROM users WHERE id = ?");
    $stmt->execute([$_SESSION['user_id']]);
    
    if ($stmt->rowCount() == 0) {
        $errors[] = "Ошибка: Ваш профиль не найден. Пожалуйста, выйдите и войдите снова.";
        // Сохраняем информацию для отладки
        error_log("Пользователь с ID {$_SESSION['user_id']} не найден в базе данных. Логин: {$_SESSION['login']}");
    }
} catch (PDOException $e) {
    $errors[] = "Ошибка проверки профиля: " . $e->getMessage();
    error_log("Ошибка проверки профиля: " . $e->getMessage());
}

// Получаем список услуг из базы данных
try {
    $services = $pdo->query("SELECT * FROM services")->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    // Если таблица услуг не существует, создаем массив с базовыми услугами
    $services = [
        ['id' => 1, 'name' => 'Общий клининг'],
        ['id' => 2, 'name' => 'Генеральная уборка'],
        ['id' => 3, 'name' => 'Послестроительная уборка'],
        ['id' => 4, 'name' => 'Химчистка ковров'],
        ['id' => 5, 'name' => 'Химчистка мебели']
    ];
    
    // Создаем таблицу услуг и заполняем её
    try {
        $pdo->exec("CREATE TABLE IF NOT EXISTS services (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
        
        $stmt = $pdo->prepare("INSERT INTO services (name) VALUES (?)");
        foreach ($services as $service) {
            $stmt->execute([$service['name']]);
        }
    } catch (PDOException $e2) {
        $errors[] = "Не удалось создать таблицу услуг: " . $e2->getMessage();
    }
}

if ($_SERVER['REQUEST_METHOD'] == 'POST' && empty($errors)) {
    $title = sanitizeInput($_POST['title']);
    $description = sanitizeInput($_POST['description']);
    $address = sanitizeInput($_POST['address']);
    $phone = sanitizeInput($_POST['phone']);
    $service_date = sanitizeInput($_POST['service_date']);
    $service_time = sanitizeInput($_POST['service_time']);
    $service_datetime = $service_date . ' ' . $service_time . ':00';
    $service_id = isset($_POST['service_id']) && $_POST['service_id'] !== 'custom' ? intval($_POST['service_id']) : null;
    $custom_service = isset($_POST['custom_service']) ? sanitizeInput($_POST['custom_service']) : null;
    $payment_type = sanitizeInput($_POST['payment_type']);
    
    // Проверка валидности данных
    if (empty($title)) {
        $errors[] = "Заголовок обязателен";
    }
    
    if (empty($description)) {
        $errors[] = "Описание обязательно";
    }
    
    if (empty($address)) {
        $errors[] = "Адрес обязателен";
    }
    
    if (empty($phone)) {
        $errors[] = "Телефон обязателен";
    } elseif (!preg_match('/^\+7\(\d{3}\)\-\d{3}\-\d{2}\-\d{2}$/', $phone)) {
        $errors[] = "Телефон должен быть в формате +7(XXX)-XXX-XX-XX";
    }
    
    if (empty($service_date) || empty($service_time)) {
        $errors[] = "Дата и время получения услуги обязательны";
    }
    
    if ($service_id === null && empty($custom_service)) {
        $errors[] = "Если выбрана опция 'Иная услуга', необходимо указать описание услуги";
    }
    
    if (empty($payment_type)) {
        $errors[] = "Тип оплаты обязателен";
    }
    
    // Если нет ошибок, создаем заявку
    if (empty($errors)) {
        try {
            // Проверяем наличие колонок в таблице заявок
            $requiredColumns = ['address', 'phone', 'service_date', 'service_id', 'custom_service', 'payment_type', 'status'];
            $stmt = $pdo->query("DESCRIBE requests");
            $existingColumns = [];
            while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                $existingColumns[] = $row['Field'];
            }
            
            $missingColumns = array_diff($requiredColumns, $existingColumns);
            if (!empty($missingColumns)) {
                $errors[] = "В таблице requests отсутствуют необходимые колонки: " . implode(", ", $missingColumns);
                $errors[] = "Пожалуйста, запустите скрипт update_database.php для обновления структуры базы данных.";
                throw new Exception("Отсутствуют необходимые колонки в таблице requests");
            }
            
            // Создаем заявку
            $stmt = $pdo->prepare("
                INSERT INTO requests (user_id, title, description, address, phone, service_date, service_id, custom_service, payment_type, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'новая')
            ");
            
            $stmt->execute([
                $_SESSION['user_id'],
                $title,
                $description,
                $address,
                $phone,
                $service_datetime,
                $service_id,
                $service_id === null ? $custom_service : null,
                $payment_type
            ]);
            
            $request_id = $pdo->lastInsertId();
            
            redirectWithMessage('my_requests.php', "Заявка #$request_id успешно создана!", 'success');
        } catch (PDOException $e) {
            $errors[] = "Ошибка базы данных: " . $e->getMessage();
            // Сохраняем подробную информацию для отладки
            error_log("Ошибка создания заявки: " . $e->getMessage());
            error_log("user_id: {$_SESSION['user_id']}, service_id: $service_id");
        } catch (Exception $e) {
            // Ошибки уже добавлены в массив $errors
            error_log("Ошибка: " . $e->getMessage());
        }
    }
}
?>

<div class="request-form">
    <div class="card">
        <div class="card-header">
            <h3>Создание новой заявки</h3>
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
            
            <form action="new_request.php" method="post">
                <div class="mb-3">
                    <label for="title" class="form-label">Заголовок заявки</label>
                    <input type="text" class="form-control" id="title" name="title" value="<?php echo isset($title) ? htmlspecialchars($title) : ''; ?>" required>
                </div>
                
                <div class="mb-3">
                    <label for="description" class="form-label">Описание заявки</label>
                    <textarea class="form-control" id="description" name="description" rows="3" required><?php echo isset($description) ? htmlspecialchars($description) : ''; ?></textarea>
                </div>
                
                <div class="mb-3">
                    <label for="address" class="form-label">Адрес</label>
                    <input type="text" class="form-control" id="address" name="address" value="<?php echo isset($address) ? htmlspecialchars($address) : ''; ?>" required>
                </div>
                
                <div class="mb-3">
                    <label for="phone" class="form-label">Телефон (формат: +7(XXX)-XXX-XX-XX)</label>
                    <input type="text" class="form-control" id="phone" name="phone" placeholder="+7(XXX)-XXX-XX-XX" value="<?php echo isset($phone) ? htmlspecialchars($phone) : ''; ?>" required>
                </div>
                
                <div class="row mb-3">
                    <div class="col">
                        <label for="service_date" class="form-label">Дата получения услуги</label>
                        <input type="date" class="form-control" id="service_date" name="service_date" value="<?php echo isset($service_date) ? htmlspecialchars($service_date) : date('Y-m-d'); ?>" required>
                    </div>
                    <div class="col">
                        <label for="service_time" class="form-label">Время получения услуги</label>
                        <input type="time" class="form-control" id="service_time" name="service_time" value="<?php echo isset($service_time) ? htmlspecialchars($service_time) : '10:00'; ?>" required>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="service_id" class="form-label">Выберите вид услуги</label>
                    <select class="form-select" id="service_id" name="service_id" required>
                        <?php foreach ($services as $service): ?>
                            <option value="<?php echo $service['id']; ?>" <?php echo (isset($service_id) && $service_id == $service['id']) ? 'selected' : ''; ?>>
                                <?php echo htmlspecialchars($service['name']); ?>
                            </option>
                        <?php endforeach; ?>
                        <option value="custom" <?php echo (isset($service_id) && $service_id === null) ? 'selected' : ''; ?>>Иная услуга</option>
                    </select>
                </div>
                
                <div class="mb-3" id="custom_service_block" style="display: <?php echo (isset($service_id) && $service_id === null) ? 'block' : 'none'; ?>">
                    <label for="custom_service" class="form-label">Опишите требуемую услугу</label>
                    <textarea class="form-control" id="custom_service" name="custom_service" rows="3"><?php echo isset($custom_service) ? htmlspecialchars($custom_service) : ''; ?></textarea>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Выберите тип оплаты</label>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="payment_type" id="payment_cash" value="наличные" <?php echo (!isset($payment_type) || $payment_type == 'наличные') ? 'checked' : ''; ?>>
                        <label class="form-check-label" for="payment_cash">
                            Наличные
                        </label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="payment_type" id="payment_card" value="карта" <?php echo (isset($payment_type) && $payment_type == 'карта') ? 'checked' : ''; ?>>
                        <label class="form-check-label" for="payment_card">
                            Банковская карта
                        </label>
                    </div>
                </div>
                
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary">Отправить заявку</button>
                    <a href="dashboard.php" class="btn btn-outline-secondary">Отмена</a>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const serviceSelect = document.getElementById('service_id');
    const customServiceBlock = document.getElementById('custom_service_block');
    const customServiceInput = document.getElementById('custom_service');
    
    // Функция обработки изменения выбора услуги
    function handleServiceChange() {
        if (serviceSelect.value === 'custom') {
            customServiceBlock.style.display = 'block';
            customServiceInput.setAttribute('required', 'required');
        } else {
            customServiceBlock.style.display = 'none';
            customServiceInput.removeAttribute('required');
        }
    }
    
    // Вызываем функцию при загрузке и добавляем слушатель изменений
    handleServiceChange();
    serviceSelect.addEventListener('change', handleServiceChange);
    
    // Маска для телефона
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        // Проверяем, начинается ли номер с 7, если да - форматируем как +7
        if (value.startsWith('7') && value.length === 11) {
            value = value.substring(1); // Убираем ведущую 7
        }
        
        // Форматируем номер
        let formattedNumber = '';
        if (value.length > 0) {
            formattedNumber = '+7';
            if (value.length > 0) {
                formattedNumber += '(' + value.substring(0, Math.min(3, value.length));
            }
            if (value.length > 3) {
                formattedNumber += ')-' + value.substring(3, Math.min(6, value.length));
            }
            if (value.length > 6) {
                formattedNumber += '-' + value.substring(6, Math.min(8, value.length));
            }
            if (value.length > 8) {
                formattedNumber += '-' + value.substring(8, Math.min(10, value.length));
            }
        }
        
        e.target.value = formattedNumber;
    });
});
</script>

<?php include_once 'includes/footer.php'; ?>