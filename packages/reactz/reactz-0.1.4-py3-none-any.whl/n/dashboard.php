<?php
include_once 'includes/header.php';
checkLogin();

// Получаем статистику по заявкам пользователя
$stmt = $pdo->prepare("
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) as new_count,
        SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_count,
        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_count,
        SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected_count
    FROM requests 
    WHERE user_id = ?
");
$stmt->execute([$_SESSION['user_id']]);
$stats = $stmt->fetch(PDO::FETCH_ASSOC);

// Получаем последние заявки пользователя
$stmt = $pdo->prepare("
    SELECT * FROM requests 
    WHERE user_id = ? 
    ORDER BY created_at DESC 
    LIMIT 5
");
$stmt->execute([$_SESSION['user_id']]);
$recent_requests = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<div class="row">
    <div class="col-md-12">
        <h1 class="mb-4">Панель управления</h1>
        
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
                        <h5 class="card-title">Новых</h5>
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
                        <h5 class="card-title">Выполнено</h5>
                        <p class="card-text display-4"><?php echo $stats['completed_count']; ?></p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mt-4">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Последние заявки</h5>
                <a href="new_request.php" class="btn btn-primary btn-sm">Создать новую заявку</a>
            </div>
            <div class="card-body">
                <?php if (count($recent_requests) > 0): ?>
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Заголовок</th>
                                    <th>Статус</th>
                                    <th>Дата создания</th>
                                    <th>Действия</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($recent_requests as $request): ?>
                                <tr>
                                    <td><?php echo $request['id']; ?></td>
                                    <td><?php echo htmlspecialchars($request['title']); ?></td>
                                    <td><span class="status-<?php echo $request['status']; ?>"><?php echo getRequestStatusName($request['status']); ?></span></td>
                                    <td><?php echo date('d.m.Y H:i', strtotime($request['created_at'])); ?></td>
                                    <td>
                                        <a href="view_request.php?id=<?php echo $request['id']; ?>" class="btn btn-sm btn-info">Просмотр</a>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                <?php else: ?>
                    <p class="text-center">У вас пока нет заявок. <a href="new_request.php">Создать заявку</a>.</p>
                <?php endif; ?>
            </div>
            <div class="card-footer text-center">
                <a href="my_requests.php" class="btn btn-outline-primary">Все мои заявки</a>
            </div>
        </div>
    </div>
</div>

<?php include_once 'includes/footer.php'; ?>