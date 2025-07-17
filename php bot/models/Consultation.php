<?php

class Consultation
{
  public $ID;
  public $customer;
  public $emp;
  public $status;
  public $consultation_log;
  public $db;


  function __construct($ID,$customer=NULL,$emp=NULL,$status=NULL,$consultation_log=NULL)
  {
  	if($ID==NULL){
  		$this->ID = '';
	    $this->customer = '';
	    $this->emp = '';
	    $this->status = '';
	    $this->consultation_log = '';
	    $this->db=dbconnect();
  	}
  	else{
	    $this->ID = $ID;
	    $this->customer = new Customer($customer);
	    $this->emp = new Emp($emp);
	    $this->status = $status;
	    $this->consultation_log = $consultation_log;
	    $this->db=dbconnect();
	  }
  }


  function to_array(){
    $arr['ID'] = $this->ID;
    $arr['customer_id'] = $this->customer->ID;
    $arr['emp_id'] = $this->emp->ID;
    $arr['status'] = $this->status;
    return $arr;
  }


  function no_errors()
  {
    $errors['ID'] = '0';
    $errors['customer_id'] = '0';
    $errors['emp_id'] = '0';
    $errors['status'] = '0';
    return $errors;
  }


function errors_check()
  {
    $errors['customer_id'] = '0';
    $errors['emp_id'] = '0';
    $errors['status'] = '0';
    $errors['error'] = FALSE;
    $this->ID = $_COOKIE['PK'];
    if (empty($_POST['customer_id'])){
      $errors['customer_id'] = '1';
      $errors['error'] = TRUE;
      $this->customer = new Customer('');
    }
    else
      $this->customer = new Customer($_POST['customer_id']);
    if (empty($_POST['emp_id'])){
      $errors['emp_id'] = '1';
      $errors['error'] = TRUE;
      $this->emp = new Emp('');
    }
    else
      $this->emp = new Emp($_POST['emp_id']);

    if (empty($_POST['status'])){
      $errors['status'] = '1';
      $errors['error'] = TRUE;
      $this->status = '';
    }
    else
      $this->status = $_POST['status']; 
    return $errors;
  }

  function load()
  {
    try {
      $stmt = $this->db->prepare("SELECT * FROM Consultation where ID = :ID");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->execute();
      $data=$stmt->fetch();
      $this->status = $data['status'];
      $this->consultation_log = $data['consultation_log'];
      $this->customer = new Customer($data['customer_id']);
      $this->emp = new Emp($data['emp_id']);
      $this->customer->load();
      $this->emp->load();
    }
    catch(PDOException $e){
      print('Error : ' . $e->getMessage());
      exit();
    }    
  }


  function add()
  {
    try {
      $stmt = $this->db->prepare("INSERT INTO consultation (customer_id, emp_id, status, consultation_log) VALUES (:customer_id, :emp_id, :status, :consultation_log);");
      $stmt->bindParam(':customer_id', $this->customer->ID);
      $stmt->bindParam(':emp_id',  $this->emp->ID);
      $stmt->bindParam(':status', $this->status);
      $stmt->bindParam(':consultation_log', $this->consultation_log);
      $stmt->execute();
    }
    catch(PDOException $e){
      print('Error : ' . $e->getMessage());
      exit();
    }    
  }


  function update()
  {
    try {
      $stmt = $this->db->prepare("UPDATE consultation SET customer_id = :customer_id, emp_id = :emp_id, status = :status WHERE ID=:ID;");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->bindParam(':customer_id', $this->customer->ID);
      $stmt->bindParam(':emp_id',  $this->emp->ID);
      $stmt->bindParam(':status', $this->status);
      $stmt->execute();
    }    
    catch(PDOException $e){
      print('Error : ' . $e->getMessage());
      exit();
    }
  }


  function delete()
  {
    try {
      $stmt = $this->db->prepare("SELECT consultation_log FROM Consultation where ID = :ID");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->execute();
      $data=$stmt->fetch();
      $log_str = $data['consultation_log'];
      $log_arr=explode('', $log_str);
      foreach ($log_arr as $i => $message) {  
        $log_arr[$i]=explode('', $message);
      }
      $file_type=['изображение','видео','документ','голосовое','аудио','анимация'];
      foreach ($log_arr as $message) {
        if(in_array($message[1], $file_type)){
          $file_name=$message[2];  
          $stmt = $this->db->prepare("DELETE FROM log_files WHERE file_name = :file_name");
          $stmt->bindParam(':file_name', $file_name);
          $stmt->execute();
        }
      }

      $stmt = $this->db->prepare("DELETE FROM consultation WHERE ID = :ID");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->execute();
    }
    catch(PDOException $e){
      print('Error : ' . $e->getMessage());
      exit();
    }
  }


  public static function print_all($db, $token)
  {
    try {    
      print '<table border="1">
      <caption>Консультации</caption>
      <tr>
        <th>ID</th>
        <th>Клиент</th>
        <th>Оператор</th>
        <th>Статус</th>
      <tr>';      
      $stmt = $db->prepare("SELECT * FROM consultation LEFT JOIN customer ON consultation.customer_id=customer.id LEFT JOIN emp ON consultation.emp_id=emp.id");      
      $stmt->execute();
      $line=array();
      for($line=$stmt->fetch();!empty($line);$line=$stmt->fetch()){
        print'<tr>';
        $PK='0';
        print'<td>'.$line[0].'</td>';
        print'<td>'.$line[6].'(id='.$line['customer_id'].')'.'</td>';  
        print'<td>'.$line['first_name'].' '.$line['last_name'].'(id='.$line['emp_id'].')'.'</td>';
        $status=$line['status'];
        print'<td>'.$status.'</td>
        <form action="" method="POST">
          <input name="PK" value="'.$line[$PK].'" hidden>
          <input name="csrf_token" value="'.$token.'" hidden>
          <td><input type="submit" name="show_log" value="Посмотреть лог"></td>
          <td><input type="submit" name="change" value="Изменить"></td>
          <td class="delete"><input type="submit" name="delete" value="Удалить"></td>
        </form>
        <tr>';
      }
      print '</table>';
      }
    catch(PDOException $e){
      print('Error : ' . $e->getMessage());
      exit();
    }
  }



}

?>
