<?php
//http://localhost/dashboard/test/telegramm%20bot/admin.php
include('models/Emp.php');
include('models/Customer.php');
include('models/Consultation.php');
function dbconnect(){
  $user = 'telegramm_bot';
  $pass = '9hH][7E1O8g*kV8c';
  $db = new PDO('mysql:host=localhost;dbname=telegramm_bot', $user, $pass, array(PDO::ATTR_PERSISTENT => true));
  return $db;
}
$is_admin = false;
if (!empty($_SERVER['PHP_AUTH_USER']) && !empty($_SERVER['PHP_AUTH_PW'])){
  $login = $_SERVER['PHP_AUTH_USER'];
  $pass = md5(md5($_SERVER['PHP_AUTH_PW'].'jdfkm3ks25d'));
  $db=dbconnect();
  try {
    $stmt = $db->prepare("SELECT ID FROM admins where login = :login AND pass = :pass");
    $stmt->bindParam(':login', $login);
    $stmt->bindParam(':pass', $pass);
    $stmt->execute();
    $adminID=$stmt->fetchColumn();
  }
  catch(PDOException $e){
    print('Error : ' . $e->getMessage());
    exit();
  }
  if(empty(!$adminID)){
    $is_admin = true;
  }
}

if(!$is_admin){
  header('HTTP/1.1 401 Unanthorized');
  header('WWW-Authenticate: Basic realm="My site"');
  print('<h1>401 Требуется авторизация</h1>');
  exit();
}

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
  if(!empty($_COOKIE['show_log'])){
    print '<form action="" method="POST">
      <input name="cancel" type="submit" value="Назад">
    </form>
    Для просмотра лога перейдите по ссылке <a href="">aaaaaa</a></br>
    В Telegramm боте введите комманду</br><b> command</b></br>Затем введите ID консультации</br><b>'.$_COOKIE['PK'].'</b></br>Затем введите логин и пароль этой учетной записи администратора';
    exit;
  }
  session_start();
  $token= uniqid();
  $_SESSION['csrf_token'] = $token;
  if(!empty($_COOKIE['change_smth'])||!empty($_COOKIE['add'])){
    $form_val = array();
    $errors = array();
    $form_val = unserialize($_COOKIE['form_val']);
    foreach ($form_val as $key => $value) {
      $form_val[$key]=strip_tags($value);
    }
    $table = empty($_COOKIE['table']) ? '' : strip_tags($_COOKIE['table']);
    $errors = unserialize($_COOKIE['errors']);
    switch ($table) {
      case 'customer':
        include('forms/customer_form.php');
        break;  
      case 'emp':
        include('forms/emp_form.php');
        break;
      case 'consultation':
        include('forms/consultation_form.php');
        break;    
    }      
    exit();
  } 


  $error = empty($_COOKIE['table']);
  $table = $error? "" : $_COOKIE['table'];
  print '
  <!DOCTYPE html>

  <html lang="ru" >
  <head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="style.css">
    <title></title>
  </head>
  <body>';
  print'<form action="" method="POST" class="radio_tables">
    <div>
      <label><input type="radio" name="table" value="customer"';if (!$error&&$table=='customer') print 'checked="checked"';print'>
        Клиенты</label>
      <label><input type="radio" name="table" value="emp"';if (!$error&&$table=='emp') print 'checked="checked"';print'>
        Операторы</label>
      <label><input type="radio" name="table" value="consultation"';if (!$error&&$table=='consultation') print 'checked="checked"';print'>
        Консультации</label><br />
    </div>  
    <input name="csrf_token" value="'.$token.'" hidden>
    <input type="submit" value="Открыть" />
  </form>';
  
  if(!$error){
    $db = dbconnect();
    switch ($table) {
      case 'customer':
        Customer::print_all($db, $token);
        break;
      case 'emp':
        Emp::print_all($db, $token);
        break;
      case 'consultation':
        Consultation::print_all($db, $token);
        break;
    }
    if($table!='consultation'){
      print'<form action="" method="POST" class="add"> 
        <input name="csrf_token" value="'.$token.'" hidden>
        <input name="add" value="1" hidden>
        <input type="submit" value="Добавить" />
      </form>';
    }
  }
}
//если метод POST
else{
  if (!empty($_POST['table'])){ 
    setcookie('table', $_POST['table'], time()+3600*24);
  }
  $table = $_COOKIE['table'];
  if(!empty($_POST['cancel'])){
    setcookie('show_log', '', 100);
    setcookie('PK', '', 100);
    setcookie('add', '', 100);
    setcookie('change_smth', '', 100);
    header('Location: admin.php');
    setcookie('form_val', '', 100);
    setcookie('errors', '', 100);
    exit();
  }


  if(!empty($_COOKIE[session_name()]) &&
      session_start() && $_SESSION['csrf_token'] == $_POST['csrf_token']){
    //если была нажата кнопка "изменить" или "добавить"
    if(!empty($_COOKIE['change_smth'])||!empty($_COOKIE['add'])){
      switch ($table) {
        case 'customer':
          $model = new Customer(NULL);
          break;
        case 'emp':
          $model = new Emp(NULL);
          break;
        case 'consultation':
          $model = new Consultation(NULL);
          break;
      }
      $errors = $model->errors_check();
      $form_val = $model->to_array();

      if($errors['error']){
        setcookie('errors', serialize($errors), time()+3600*24);
        setcookie('form_val', serialize($form_val), time()+3600*24);

        header('Location: admin.php');
      }
      else{//если ошибок не было

        if(!empty($_COOKIE['add']))       
          $model->add();
        if(!empty($_COOKIE['change_smth']))          
          $model->update();
        setcookie('errors', '', 100);
        setcookie('form_val', '', 100);
        setcookie('change_smth', '', 100);
        setcookie('PK', '', 100);
        setcookie('add', '', 100);
      }
    }//конец "изменить"
  


    if(!empty($_POST['change'])||!empty($_POST['add'])){
      if(!empty($_POST['change'])){
        setcookie('change_smth', 1, time()+3600*24);
        $PK = $_POST['PK'];
        switch ($table) {
          case 'customer':
            $model = new Customer($PK);
            break;
          case 'emp':
            $model = new Emp($PK);
            break;
          case 'consultation':
            $model = new Consultation($PK);            
            break;
        }
        $model->load();
        setcookie('form_val', serialize($model->to_array()), time()+3600*24);
        setcookie('PK', $_POST['PK'], time()+3600*24);
      }
      if(!empty($_POST['add'])){
        setcookie('add', 1, time()+3600*24);
        switch ($table) {
          case 'customer':
            $model = new Customer(NULL);
            break;
          case 'emp':
            $model = new Emp(NULL);
            break;
          case 'consultation':
            $model = new Consultation(NULL);
            break;
        }
        setcookie('form_val', serialize($model->to_array()), time()+3600*24);
      }
      $errors=$model->no_errors();      
      setcookie('errors', serialize($errors), time()+3600*24);
      header('Location: admin.php');
      exit();
    }




    if(!empty($_POST['delete'])){
      $PK = $_POST['PK'];
      switch ($table) {
        case 'customer':
          $model = new Customer($PK);
          break;
        case 'emp':
          $model = new Emp($PK);
          break;
        case 'consultation':
          $model = new Consultation($PK);
          break;
      }
      $model->delete();
      setcookie('PK', 1, 100);
    }

    if(!empty($_POST['show_log'])){
      setcookie('PK', $_POST['PK'], time()+3600*24);
      setcookie('show_log', 1, time()+3600*24);
    }

    header('Location: admin.php');
  }
}
?>