<?php
// Определяем корневой каталог проекта
$root_path = realpath($_SERVER["DOCUMENT_ROOT"]) . '/test/';

// Включаем header с использованием абсолютного пути 
include_once $root_path . 'includes/header.php';

// Проверка на администратора
if (!isset($_SESSION['role']) || $_SESSION['role'] != 'admin') {
    header('Location: ../dashboard.php');
    exit;
}

// Получаем статистику по всем заявкам
$stmt = $pdo->prepare("
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) as new_count,
        SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_count,
        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_count,
        SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected_count
    FROM requests
");
$stmt->execute();
$stats = $stmt->fetch(PDO::FETCH_ASSOC);

// Последние 5 новых заявок
$stmt = $pdo->prepare("
    SELECT r.*, u.username
    FROM requests r
    JOIN users u ON r.user_id = u.id
    WHERE r.status = 'new'
    ORDER BY r.created_at DESC
    LIMIT 5
");
$stmt->execute();
$new_requests = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Количество пользователей
$stmt = $pdo->prepare("SELECT COUNT(*) as user_count FROM users WHERE role = 'user'");
$stmt->execute();
$user_count = $stmt->fetch(PDO::FETCH_ASSOC)['user_count'];
?>

<div class="row">
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Админ панель</h1>
        </div>
        
        <div class="row">
            <div class="col-md-3">
                <div class="card text-white bg-primary mb-3">
                    <div class="card-body text-center">
                        <h5 class="card-title">Всего заявок</h5>
                        <p class="card-text display-4"><?php echo $stats['total']; ?></p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-info mb-3">
                    <div class="card-body text-center">
                        <h5 class="card-title">Новых заявок</h5>
                        <p class="card-text display-4"><?php echo $stats['new_count']; ?></p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-warning mb-3">
                    <div class="card-body text-center">
                        <h5 class="card-title">В обработке</h5>
                        <p class="card-text display-4"><?php echo $stats['in_progress_count']; ?></p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-success mb-3">
                    <div class="card-body text-center">
                        <h5 class="card-title">Пользователей</h5>
                        <p class="card-text display-4"><?php echo $user_count; ?></p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Новые заявки</h5>
                        <a href="view_requests.php" class="btn btn-sm btn-primary">Все заявки</a>
                    </div>
                    <div class="card-body">
                        <?php if (count($new_requests) > 0): ?>
                            <div class="table-responsive">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Пользователь</th>
                                            <th>Заголовок</th>
                                            <th>Дата создания</th>
                                            <th>Действия</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($new_requests as $request): ?>
                                        <tr>
                                            <td><?php echo $request['id']; ?></td>
                                            <td><?php echo htmlspecialchars($request['username']); ?></td>
                                            <td><?php echo htmlspecialchars($request['title']); ?></td>
                                            <td><?php echo date('d.m.Y H:i', strtotime($request['created_at'])); ?></td>
                                            <td>
                                                <a href="../view_request.php?id=<?php echo $request['id']; ?>" class="btn btn-sm btn-info">Просмотр</a>
                                            </td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        <?php else: ?>
                            <p class="text-center">Нет новых заявок.</p>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Быстрые действия</h5>
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <a href="view_requests.php" class="btn btn-outline-primary">Управление заявками</a>
                            <a href="manage_users.php" class="btn btn-outline-primary">Управление пользователями</a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Статистика</h5>
                    </div>
                    <div class="card-body">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Всего заявок
                                <span class="badge bg-primary rounded-pill"><?php echo $stats['total']; ?></span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Новые заявки
                                <span class="badge bg-info rounded-pill"><?php echo $stats['new_count']; ?></span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                В обработке
                                <span class="badge bg-warning rounded-pill"><?php echo $stats['in_progress_count']; ?></span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Выполненные заявки
                                <span class="badge bg-success rounded-pill"><?php echo $stats['completed_count']; ?></span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Отклоненные заявки
                                <span class="badge bg-danger rounded-pill"><?php echo $stats['rejected_count']; ?></span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include_once $root_path . 'includes/footer.php'; ?>