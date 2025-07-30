<?php
session_start();
require_once 'db.php';

if(!isset($_SESSION['is_admin']) || !$_SESSION['is_admin']) {
    header("Location: login.php");
    exit;
}

if($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['update_status'])) {
    $request_id = $_POST['request_id'] ?? 0;
    $status = $_POST['status'] ?? '';
    $cancel_reason = $_POST['cancel_reason'] ?? '';
    
    if($status == 'отменено' && empty($cancel_reason)) {
        $status_error = "Укажите причину отмены";
    } else {
        $stmt = $db->prepare("UPDATE requests SET status = ?, cancel_reason = ? WHERE id = ?");
        $stmt->execute([
            $status, 
            $status == 'отменено' ? $cancel_reason : null, 
            $request_id
        ]);
        header("Location: admin.php?updated=1");
        exit;
    }
}

$stmt = $db->prepare("
    SELECT r.*, u.fullname, u.phone, s.name as service_name
    FROM requests r 
    JOIN users u ON r.user_id = u.id 
    LEFT JOIN services s ON r.service_id = s.id
    ORDER BY r.created_at DESC
");
$stmt->execute();
$requests = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Панель администратора</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container-fluid">
        <header class="header">
            <h1>Панель администратора</h1>
            <a href="logout.php" class="btn btn-sm btn-danger">Выйти</a>
        </header>
        
        <?php if(isset($_GET['updated'])): ?>
            <div class="alert alert-success">
                <p>Статус заявки успешно обновлен.</p>
            </div>
        <?php endif; ?>
        
        <?php if(isset($status_error)): ?>
            <div class="alert alert-error">
                <p><?= $status_error ?></p>
            </div>
        <?php endif; ?>
        
        <div class="card">
            <h2>Управление заявками</h2>
            
            <?php if(empty($requests)): ?>
                <div class="empty-state">
                    <p>Заявок пока нет.</p>
                </div>
            <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Дата создания</th>
                                <th>ФИО</th>
                                <th>Телефон</th>
                                <th>Адрес</th>
                                <th>Услуга</th>
                                <th>Дата и время</th>
                                <th>Оплата</th>
                                <th>Статус</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach($requests as $request): ?>
                                <tr>
                                    <td><?= $request['id'] ?></td>
                                    <td><?= date('d.m.Y H:i', strtotime($request['created_at'])) ?></td>
                                    <td><?= htmlspecialchars($request['fullname']) ?></td>
                                    <td><?= htmlspecialchars($request['phone']) ?></td>
                                    <td><?= htmlspecialchars($request['address']) ?></td>
                                    <td>
                                        <?php 
                                        if($request['service_id']) {
                                            echo htmlspecialchars($request['service_name']);
                                        } else {
                                            echo htmlspecialchars($request['custom_service']);
                                        }
                                        ?>
                                    </td>
                                    <td><?= date('d.m.Y H:i', strtotime($request['service_date'])) ?></td>
                                    <td><?= htmlspecialchars($request['payment_type']) ?></td>
                                    <td>
                                        <span class="status status-<?= strtolower($request['status']) ?>">
                                            <?= htmlspecialchars($request['status']) ?>
                                        </span>
                                        <?php if($request['status'] == 'отменено' && $request['cancel_reason']): ?>
                                            <div class="tooltip">
                                                <span class="info-icon">i</span>
                                                <span class="tooltip-text"><?= htmlspecialchars($request['cancel_reason']) ?></span>
                                            </div>
                                        <?php endif; ?>
                                    </td>
                                    <td>
                                        <form method="POST" class="status-form">
                                            <input type="hidden" name="request_id" value="<?= $request['id'] ?>">
                                            <select name="status" class="status-select">
                                                <option value="новая" <?= $request['status'] == 'новая' ? 'selected' : '' ?>>новая</option>
                                                <option value="в работе" <?= $request['status'] == 'в работе' ? 'selected' : '' ?>>в работе</option>
                                                <option value="выполнено" <?= $request['status'] == 'выполнено' ? 'selected' : '' ?>>выполнено</option>
                                                <option value="отменено" <?= $request['status'] == 'отменено' ? 'selected' : '' ?>>отменено</option>
                                            </select>
                                            <div class="cancel-reason" id="cancel_reason_<?= $request['id'] ?>" style="display: <?= $request['status'] == 'отменено' ? 'block' : 'none' ?>; margin-top: 5px;">
                                                <input type="text" name="cancel_reason" placeholder="Причина отмены" value="<?= htmlspecialchars($request['cancel_reason'] ?? '') ?>">
                                            </div>
                                            <button type="submit" name="update_status" class="btn btn-sm">Обновить</button>
                                        </form>
                                        <script>
                                            document.querySelector('form[request_id="<?= $request['id'] ?>"] select[name="status"]').addEventListener('change', function() {
                                                document.getElementById('cancel_reason_<?= $request['id'] ?>').style.display = 
                                                    this.value === 'отменено' ? 'block' : 'none';
                                            });
                                        </script>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>