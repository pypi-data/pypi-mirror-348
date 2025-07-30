<?php
include_once 'includes/header.php';
checkLogin();

// Определяем текущую страницу
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$per_page = 10;
$offset = ($page - 1) * $per_page;

// Получаем общее количество заявок пользователя
$stmt = $pdo->prepare("SELECT COUNT(*) as count FROM requests WHERE user_id = ?");
$stmt->execute([$_SESSION['user_id']]);
$total = $stmt->fetch(PDO::FETCH_ASSOC)['count'];
$total_pages = ceil($total / $per_page);

// Получаем заявки для текущей страницы - вот здесь ошибка
// Заменяем параметры ? на конкретные значения для LIMIT и OFFSET
$stmt = $pdo->prepare("
    SELECT * FROM requests 
    WHERE user_id = ? 
    ORDER BY created_at DESC 
    LIMIT " . $per_page . " OFFSET " . $offset
);
$stmt->execute([$_SESSION['user_id']]);
$requests = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<div class="row">
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Мои заявки</h1>
            <a href="new_request.php" class="btn btn-primary">Создать заявку</a>
        </div>
        
        <?php if (count($requests) > 0): ?>
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Заголовок</th>
                            <th>Статус</th>
                            <th>Дата создания</th>
                            <th>Последнее обновление</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($requests as $request): ?>
                        <tr>
                            <td><?php echo $request['id']; ?></td>
                            <td><?php echo htmlspecialchars($request['title']); ?></td>
                            <td><span class="status-<?php echo $request['status']; ?>"><?php echo getRequestStatusName($request['status']); ?></span></td>
                            <td><?php echo date('d.m.Y H:i', strtotime($request['created_at'])); ?></td>
                            <td><?php echo date('d.m.Y H:i', strtotime($request['updated_at'])); ?></td>
                            <td>
                                <a href="view_request.php?id=<?php echo $request['id']; ?>" class="btn btn-sm btn-info">Просмотр</a>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
            
            <?php if ($total_pages > 1): ?>
                <nav aria-label="Навигация по страницам">
                    <ul class="pagination justify-content-center">
                        <?php if ($page > 1): ?>
                            <li class="page-item">
                                <a class="page-link" href="?page=<?php echo $page - 1; ?>">Предыдущая</a>
                            </li>
                        <?php endif; ?>
                        
                        <?php for ($i = 1; $i <= $total_pages; $i++): ?>
                            <li class="page-item <?php echo $i == $page ? 'active' : ''; ?>">
                                <a class="page-link" href="?page=<?php echo $i; ?>"><?php echo $i; ?></a>
                            </li>
                        <?php endfor; ?>
                        
                        <?php if ($page < $total_pages): ?>
                            <li class="page-item">
                                <a class="page-link" href="?page=<?php echo $page + 1; ?>">Следующая</a>
                            </li>
                        <?php endif; ?>
                    </ul>
                </nav>
            <?php endif; ?>
        <?php else: ?>
            <div class="alert alert-info">
                <p class="text-center">У вас пока нет заявок. <a href="new_request.php">Создать заявку</a>.</p>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include_once 'includes/footer.php'; ?>