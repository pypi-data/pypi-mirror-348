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

// Получаем фильтр
$search = isset($_GET['search']) ? sanitizeInput($_GET['search']) : '';

// Определяем текущую страницу
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$per_page = 10;
$offset = ($page - 1) * $per_page;

// Строим запрос с учетом фильтра
$sql = "SELECT u.*, 
               (SELECT COUNT(*) FROM requests WHERE user_id = u.id) as request_count 
        FROM users u 
        WHERE 1=1";
$params = [];

if (!empty($search)) {
    $sql .= " AND (u.username LIKE ? OR u.email LIKE ?)";
    $params[] = "%$search%";
    $params[] = "%$search%";
}

// Добавляем сортировку
$sql .= " ORDER BY u.username ASC";

// Получаем общее количество записей с фильтром
$stmt = $pdo->prepare(str_replace("u.*, (SELECT COUNT(*) FROM requests WHERE user_id = u.id) as request_count", "COUNT(*) as count", $sql));
$stmt->execute($params);
$total = $stmt->fetch(PDO::FETCH_ASSOC)['count'];
$total_pages = ceil($total / $per_page);

// Добавляем лимит для пагинации - не используем параметры для LIMIT и OFFSET
$sql .= " LIMIT " . $per_page . " OFFSET " . $offset;

// Получаем список пользователей
$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$users = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<div class="row">
    <div class="col-md-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Управление пользователями</h1>
            <a href="index.php" class="btn btn-outline-secondary">Вернуться в админ панель</a>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Поиск пользователей</h5>
            </div>
            <div class="card-body">
                <form action="" method="get" class="row g-3">
                    <div class="col-md-10">
                        <input type="text" class="form-control" id="search" name="search" value="<?php echo $search; ?>" placeholder="Имя пользователя или email">
                    </div>
                    <div class="col-md-2">
                        <button type="submit" class="btn btn-primary w-100">Поиск</button>
                    </div>
                </form>
            </div>
        </div>
        
        <?php if (count($users) > 0): ?>
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Имя пользователя</th>
                            <th>Email</th>
                            <th>Роль</th>
                            <th>Дата регистрации</th>
                            <th>Заявки</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($users as $user): ?>
                        <tr>
                            <td><?php echo $user['id']; ?></td>
                            <td><?php echo htmlspecialchars($user['username']); ?></td>
                            <td><?php echo htmlspecialchars($user['email']); ?></td>
                            <td><?php echo $user['role'] == 'admin' ? '<span class="badge bg-danger">Администратор</span>' : '<span class="badge bg-secondary">Пользователь</span>'; ?></td>
                            <td><?php echo date('d.m.Y H:i', strtotime($user['created_at'])); ?></td>
                            <td>
                                <?php echo $user['request_count']; ?>
                                <?php if ($user['request_count'] > 0): ?>
                                    <a href="view_requests.php?search=<?php echo urlencode($user['username']); ?>" class="btn btn-sm btn-outline-info ms-2">Просмотр</a>
                                <?php endif; ?>
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
                                <a class="page-link" href="?page=<?php echo $page - 1; ?>&search=<?php echo $search; ?>">Предыдущая</a>
                            </li>
                        <?php endif; ?>
                        
                        <?php for ($i = 1; $i <= $total_pages; $i++): ?>
                            <li class="page-item <?php echo $i == $page ? 'active' : ''; ?>">
                                <a class="page-link" href="?page=<?php echo $i; ?>&search=<?php echo $search; ?>"><?php echo $i; ?></a>
                            </li>
                        <?php endfor; ?>
                        
                        <?php if ($page < $total_pages): ?>
                            <li class="page-item">
                                <a class="page-link" href="?page=<?php echo $page + 1; ?>&search=<?php echo $search; ?>">Следующая</a>
                            </li>
                        <?php endif; ?>
                    </ul>
                </nav>
            <?php endif; ?>
        <?php else: ?>
            <div class="alert alert-info">
                <p class="text-center">Пользователи не найдены.</p>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php include_once $root_path . 'includes/footer.php'; ?>