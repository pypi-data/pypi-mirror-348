<?php
include_once 'includes/header.php';

// Если пользователь уже вошел, перенаправляем на дашборд
if (isLoggedIn()) {
    header('Location: dashboard.php');
    exit;
}
?>

<div class="row mt-5">
    <div class="col-md-8 offset-md-2 text-center">
        <div class="card">
            <div class="card-body">
                <h1 class="display-4 mb-4">Добро пожаловать в систему заявок</h1>
                <p class="lead">Наша система поможет вам создавать и отслеживать заявки.</p>
                <hr class="my-4">
                <p>Для работы с системой необходимо авторизоваться или зарегистрироваться.</p>
                <div class="mt-4">
                    <a href="login.php" class="btn btn-primary me-2">Вход</a>
                    <a href="register.php" class="btn btn-outline-primary">Регистрация</a>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include_once 'includes/footer.php'; ?>