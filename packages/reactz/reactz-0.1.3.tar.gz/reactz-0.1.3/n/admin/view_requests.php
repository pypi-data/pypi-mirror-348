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

// Получаем фильтры
$status = isset($_GET['status']) ? $_GET['status'] : '';
$search = isset($_GET['search']) ? sanitizeInput($_GET['search']) : '';

// Определяем текущую страницу
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$per_page = 10;
$offset = ($page - 1) * $per_page;

// Строим запрос с учетом фильтров
$sql = "SELECT r.*, u.username FROM requests r JOIN users u ON r.user_id = u.id WHERE 1=1";
$params = [];

if (!empty($status)) {
    $sql .= " AND r.status = ?";
    $params[] = $status;
}

if (!empty($search)) {
    $sql .= " AND (r.title LIKE ? OR u.username LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

// Добавляем сортировку
$sql .= " ORDER BY r.created_at DESC";

// Получаем общее количество записей с фильтром
$stmt = $pdo->prepare(str_replace("r.*, u.username", "COUNT(*) as count", $sql));
$stmt->execute($params);
$total = $stmt->fetch(PDO::FETCH_ASSOC)['count'];
$total_pages = ceil($total / $per_page);

// Добавляем лимит для пагинации - не используем параметры для LIMIT и OFFSET
$sql .= " LIMIT " . $per_page . " OFFSET " . $offset;

// Получаем список заявок
$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$requests = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<div class="row">
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Управление заявками</h1>
            <a href="index.php" class="btn btn-outline-secondary">Вернуться в админ панель</a>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Фильтры</h5>
            </div>
            <div class="card-body">
                <form action="" method="get" class="row g-3">
                    <div class="col-md-4">
                        <label for="status" class="form-label">Статус</label>
                        <select name="status" id="status" class="form-select">
                            <option value="">Все статусы</option>
                            <option value="new" <?php echo $status == 'new' ? 'selected' : ''; ?>>Новые</option>
                            <option value="in_progress" <?php echo $status == 'in_progress' ? 'selected' : ''; ?>>В обработке</option>
                            <option value="completed" <?php echo $status == 'completed' ? 'selected' : ''; ?>>Выполненные</option>
                            <option value="rejected" <?php echo $status == 'rejected' ? 'selected' : ''; ?>>Отклоненные</option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label for="search" class="form-label">Поиск</label>
                        <input type="text" class="form-control" id="search" name="search" value="<?php echo $search; ?>" placeholder="Заголовок или имя пользователя">
                    </div>
                    <div class="col-md-2 d-flex align-items-end">
                        <button type="submit" class="btn btn-primary w-100">Применить</button>
                    </div>
                </form>
            </div>
        </div>
        
        <?php if (count($requests) > 0): ?>
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Пользователь</th>
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
                            <td><?php echo htmlspecialchars($request['username']); ?></td>
                            <td><?php echo htmlspecialchars($request['title']); ?></td>
                            <td><span class="status-<?php echo $request['status']; ?>"><?php echo getRequestStatusName($request['status']); ?></span></td>
                            <td><?php echo date('d.m.Y H:i', strtotime($request['created_at'])); ?></td>
                            <td><?php echo date('d.m.Y H:i', strtotime($request['updated_at'])); ?></td>
                            <td>
                                <a href="../view_request.php?id=<?php echo $request['id']; ?>" class="btn btn-sm btn-info">Просмотр</a>
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
                                <a class="page-link" href="?page=<?php echo $page - 1; ?>&status=<?php echo $status; ?>&search=<?php echo $search; ?>">Предыдущая</a>
                            </li>
                        <?php endif; ?>
                        
                        <?php for ($i = 1; $i <= $total_pages; $i++): ?>
                            <li class="page-item <?php echo $i == $page ? 'active' : ''; ?>">
                                <a class="page-link" href="?page=<?php echo $i; ?>&status=<?php echo $status; ?>&search=<?php echo $search; ?>"><?php echo $i; ?></a>
                            </li>
                        <?php endfor; ?>
                        
                        <?php if ($page < $total_pages): ?>
                            <li class="page-item">
                                <a class="page-link" href="?page=<?php echo $page + 1; ?>&status=<?php echo $status; ?>&search=<?php echo $search; ?>">Следующая</a>
                            </li>
                        <?php endif; ?>
                    </ul>
                </nav>
            <?php endif; ?>
        <?php else: ?>
            <div class="alert alert-info">
                <p class="text-center">Заявки не найдены.</p>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include_once $root_path . 'includes/footer.php'; ?>