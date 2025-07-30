<?php
include_once 'includes/header.php';
checkLogin();

// Проверяем ID заявки
if (!isset($_GET['id']) || !is_numeric($_GET['id'])) {
    redirectWithMessage('my_requests.php', "Некорректный ID заявки", 'danger');
}

$request_id = (int)$_GET['id'];

// Получаем информацию о заявке
$stmt = $pdo->prepare("
    SELECT r.* 
    FROM requests r
    WHERE r.id = ? AND (r.user_id = ? OR ? = 'admin')
");
$stmt->execute([$request_id, $_SESSION['user_id'], $_SESSION['role']]);

if ($stmt->rowCount() == 0) {
    redirectWithMessage('my_requests.php', "Заявка не найдена или у вас нет доступа к ней", 'danger');
}

$request = $stmt->fetch(PDO::FETCH_ASSOC);
?>

<div class="row">
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Заявка #<?php echo $request['id']; ?></h1>
            <div>
                <a href="<?php echo isAdmin() ? 'admin/view_requests.php' : 'my_requests.php'; ?>" class="btn btn-outline-secondary">Назад к списку</a>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mb-0"><?php echo htmlspecialchars($request['title']); ?></h5>
                    <span class="badge bg-<?php echo $request['status'] == 'completed' ? 'success' : ($request['status'] == 'rejected' ? 'danger' : ($request['status'] == 'in_progress' ? 'warning' : 'info')); ?>">
                        <?php echo getRequestStatusName($request['status']); ?>
                    </span>
                </div>
            </div>
            <div class="card-body">
                <h6 class="card-subtitle mb-3 text-muted">
                    Создано: <?php echo date('d.m.Y H:i', strtotime($request['created_at'])); ?>
                    <?php if ($request['created_at'] != $request['updated_at']): ?>
                        | Обновлено: <?php echo date('d.m.Y H:i', strtotime($request['updated_at'])); ?>
                    <?php endif; ?>
                </h6>
                
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-subtitle mb-2 text-muted">Описание заявки:</h6>
                        <p class="card-text"><?php echo nl2br(htmlspecialchars($request['description'])); ?></p>
                    </div>
                </div>
                
                <?php if (isAdmin() && $request['status'] != 'completed' && $request['status'] != 'rejected'): ?>
                <div class="mt-4">
                    <form action="admin/update_request.php" method="post" class="row">
                        <input type="hidden" name="request_id" value="<?php echo $request['id']; ?>">
                        <div class="col-md-4">
                            <select name="status" class="form-select">
                                <option value="new" <?php echo $request['status'] == 'new' ? 'selected' : ''; ?>>Новая</option>
                                <option value="in_progress" <?php echo $request['status'] == 'in_progress' ? 'selected' : ''; ?>>В обработке</option>
                                <option value="completed" <?php echo $request['status'] == 'completed' ? 'selected' : ''; ?>>Выполнена</option>
                                <option value="rejected" <?php echo $request['status'] == 'rejected' ? 'selected' : ''; ?>>Отклонена</option>
                            </select>
                        </div>
                        <div class="col-md-8">
                            <button type="submit" class="btn btn-primary">Обновить статус</button>
                        </div>
                    </form>
                </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</div>

<?php include_once 'includes/footer.php'; ?>