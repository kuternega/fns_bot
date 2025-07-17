<?php
//http://localhost/dashboard/test/telegramm%20bot/admin.php
function dbconnect(){
  $user = 'telegramm_bot';
  $pass = '9hH][7E1O8g*kV8c';
  $db = new PDO('mysql:host=localhost;dbname=telegramm_bot', $user, $pass, array(PDO::ATTR_PERSISTENT => true));
  return $db;
}
$is_good_bot = false;
if (!empty($_SERVER['PHP_AUTH_USER']) && !empty($_SERVER['PHP_AUTH_PW'])){
  $login = $_SERVER['PHP_AUTH_USER'];
  $pass = md5(md5($_SERVER['PHP_AUTH_PW'].'jdfkm3ks25d'));
  $db=dbconnect();
  try {
    $stmt = $db->prepare("SELECT ID FROM bots where login = :login AND pass = :pass");
    $stmt->bindParam(':login', $login);
    $stmt->bindParam(':pass', $pass);
    $stmt->execute();
    $botID=$stmt->fetchColumn();
  }
  catch(PDOException $e){
    print('Error : ' . $e->getMessage());
    exit();
  }
  if(empty(!$botID)){
    $is_good_bot = true;
  }
}



if(!$is_good_bot){
  header('HTTP/1.1 401 Unanthorized');
  header('WWW-Authenticate: Basic realm="My site"');
  print('<h1>401 Требуется авторизация</h1>');
  exit();
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
  $db = dbconnect();
  try{
    switch ((int)$_POST['code']) {
      case 1:
        $stmt = $db->prepare("SELECT ID FROM customer where ID = :ID");
        $stmt->bindParam(':ID', $_POST['customer_id']);
        $stmt->execute();
        $customerID=$stmt->fetchColumn();
        if(empty($customerID)){
          //$stmt = $db->prepare("INSERT INTO customer (ID, fio, email, tax_region) VALUES(:ID, :fio, :email, :tax_region);");
          $stmt = $db->prepare("INSERT INTO customer (ID, fio, email) VALUES(:ID, :fio, :email);");
          $stmt->bindParam(':ID', $_POST['customer_id']);
          $stmt->bindParam(':fio', $_POST['fio']);
          $stmt->bindParam(':email', $_POST['email']);
          //$stmt->bindParam(':tax_region', $_POST['tax_region']);
          $stmt->execute();
        }
        else{
          //$stmt = $db->prepare("UPDATE customer SET fio = :fio, email = :email, tax_region = :tax_region WHERE ID=:ID;");
          $stmt = $db->prepare("UPDATE customer SET fio = :fio, email = :email WHERE ID=:ID;");
          $stmt->bindParam(':ID', $_POST['customer_id']);
          $stmt->bindParam(':fio', $_POST['fio']);
          $stmt->bindParam(':email', $_POST['email']);
          //$stmt->bindParam(':tax_region', $_POST['tax_region']);
          $stmt->execute();
        }
        $stmt = $db->prepare("INSERT INTO consultation (customer_id, status) VALUES(:customer_id, 'Поступила');");
        $stmt->bindParam(':customer_id', $_POST['customer_id']);
        $stmt->execute();
        print($db->lastInsertId());        
        break;
      case 2:
        $stmt = $db->prepare("UPDATE consultation SET status = 'в работе не оплачен', emp_id = :emp_id WHERE ID = :ID;");
        $stmt->bindParam(':emp_id', $_POST['emp_id']);
        $stmt->bindParam(':ID', $_POST['ID']);
        $stmt->execute();    
        break;
      case 3:
        $stmt = $db->prepare("UPDATE consultation SET status = :status WHERE ID = :ID;");
        $stmt->bindParam(':status', $_POST['status']);
        $stmt->bindParam(':ID', $_POST['ID']);
        $stmt->execute();       
        break;
      case 4: 
        $stmt = $db->prepare("UPDATE consultation SET status = :status, consultation_log = :consultation_log WHERE ID = :ID;");
        $stmt->bindParam(':status', $_POST['status']);
        $stmt->bindParam(':consultation_log', $_POST['consultation_log']);
        $stmt->bindParam(':ID', $_POST['ID']);
        $stmt->execute();        
        break;
      case 50:
        $stmt = $db->prepare("SELECT file_name FROM log_files where file_name = :file_name");
        $stmt->bindParam(':file_name', $_POST['file_name']);
        $stmt->execute();
        $file_name=$stmt->fetchColumn();
        $answer=1;
        if(empty($file_name))
          $answer=0;
        print($answer);
        break;
      case 5:
        $stmt = $db->prepare("INSERT INTO log_files (file_name, file) VALUES(:file_name, :file);");
        $stmt->bindParam(':file_name', $_POST['file_name']);
        $stmt->bindParam(':file', $_POST['file']);
        $stmt->execute();
        break;
      case 6: 
        $stmt = $db->prepare("SELECT consultation_log, customer_id, emp_id FROM consultation where ID = :ID");
        $stmt->bindParam(':ID', $_POST['ID']);
        $stmt->execute();
        $consultation=$stmt->fetchColumn();
        $answer['consultation_log']=strip_tags($consultation['consultation_log']);
        $stmt = $db->prepare("SELECT fio  FROM customer where ID = :ID");
        $stmt->bindParam(':ID', $consultation['customer_id']);
        $stmt->execute();
        $answer['customer_name']=strip_tags($stmt->fetchColumn());
        $stmt = $db->prepare("SELECT first_name, last_name  FROM emp where ID = :ID");
        $stmt->bindParam(':ID', $consultation['emp_id']);
        $stmt->execute();
        $answer['emp_name']=$stmt->fetchColumn();
        $answer['emp_name']=strip_tags($answer['emp_name']['first_name'] .' '. $answer['emp_name']['last_name']);
        print(json_decode($answer));
        break;
      case 7:  
        $stmt = $db->prepare("SELECT file FROM log_files where file_name = :file_name");
        $stmt->bindParam(':file_name', $_POST['file_name']);
        $stmt->execute();
        $file=$stmt->fetchColumn();   
        print($file);    
        break;
    }
  }
  catch(PDOException $e){
    print('Error : ' . $e->getMessage());
    exit();
  }
}
?>