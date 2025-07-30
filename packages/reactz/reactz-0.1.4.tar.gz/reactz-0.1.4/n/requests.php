<?php
session_start();
require_once 'db.php';

if(!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit;
}

$stmt = $db->prepare("
    SELECT r.*, s.name as service_name 
    FROM requests r
    LEFT JOIN services s ON r.service_id = s.id
    WHERE r.user_id = ? 
    ORDER BY r.created_at DESC
");
$stmt->execute([$_SESSION['user_id']]);
$requests = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мои заявки | Клининговый сервис</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>Мои заявки</h1>
            <a href="logout.php" class="logout-btn">Выйти</a>
        </header>
        
        <div class="card">
            <div class="card-header">
                <a href="create_request.php" class="btn">Создать новую заявку</a>
            </div>
            
            <?php if(isset($_GET['success'])): ?>
                <div class="alert alert-success">
                    <p>Заявка успешно создана!</p>
                </div>
            <?php endif; ?>
            
            <?php if(empty($requests)): ?>
                <div class="empty-state">
                    <p>У вас пока нет заявок.</p>
                    <p>Создайте новую заявку, чтобы заказать услугу клининга.</p>
                </div>
            <?php else: ?>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>№</th>
                                <th>Дата создания</th>
                                <th>Услуга</th>
                                <th>Адрес</th>
                                <th>Дата и время</th>
                                <th>Статус</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach($requests as $index => $request): ?>
                                <tr>
                                    <td><?= $index + 1 ?></td>
                                    <td><?= date('d.m.Y H:i', strtotime($request['created_at'])) ?></td>
                                    <td>
                                        <?php 
                                        if($request['service_id']) {
                                            echo htmlspecialchars($request['service_name']);
                                        } else {
                                            echo htmlspecialchars($request['custom_service']);
                                        }
                                        ?>
                                    </td>
                                    <td><?= htmlspecialchars($request['address']) ?></td>
                                    <td><?= date('d.m.Y H:i', strtotime($request['service_date'])) ?></td>
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