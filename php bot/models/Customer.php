<?php

class Customer
{
  public $ID;
  public $fio;
  public $email;
  //public $tax_region;
  public $db;


  //function __construct($ID,$fio=NULL,$tax_region=NULL)
  function __construct($ID,$fio=NULL)
  {
    if($ID==NULL){
      $this->ID = '';
      $this->fio = '';
      $this->email = '';
      //$this->tax_region = '';
      $this->db=dbconnect();
    }
    else{
      $this->ID = $ID;
      $this->fio = $fio;
      $this->email = $email;
      //$this->tax_region = $tax_region;
      $this->db=dbconnect();
    }
  }


  function to_array(){
    $arr['ID'] = $this->ID;
    $arr['fio'] = $this->fio;
    $arr['email'] = $this->email;
    //$arr['tax_region'] = $this->tax_region;
    return $arr;
  }


function no_errors()
  {
    $errors['ID'] = '0';
    $errors['fio'] = '0';
    $errors['email'] = '0';
    //$errors['tax_region'] = '0';
    return $errors;
  }


  function errors_check()
  {
    $errors['ID'] = '0';
    $errors['fio'] = '0';
    $errors['email'] = '0';
    //$errors['tax_region'] = '0';
    $errors['error'] = FALSE;
    if (empty($_POST['ID'])){
      $errors['ID'] = '1';
      $errors['error'] = TRUE;
      $this->ID = '';
    }
    else if (!empty($_COOKIE['PK'])){
      $errors['ID'] = '0';
      $errors['error'] = FALSE;
      $this->ID = $_COOKIE['PK'];
    }
    else
      $this->ID = $_POST['ID'];
    if (empty($_POST['fio'])){
      $errors['fio'] = '1';
      $errors['error'] = TRUE;
      $this->fio = '';
    }
    else
      $this->fio = $_POST['fio'];
     if (empty($_POST['email'])){
      $errors['email'] = '1';
      $errors['error'] = TRUE;
      $this->email = '';
    }
    else
      $this->email = $_POST['email'];
    //if (empty($_POST['tax_region'])){
    //  $errors['tax_region'] = '1';
    //  $errors['error'] = TRUE;
    //  $this->tax_region = '';
    //}
    //else
    //  $this->tax_region = $_POST['tax_region'];    
    return $errors;
  }


  function load()
  {
    try {
      $stmt = $this->db->prepare("SELECT * FROM customer where ID = :ID");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->execute();
      $data=$stmt->fetch();
      $this->fio = $data['fio'];
      $this->email = $data['email'];
      //$this->tax_region = $data['tax_region'];
    }
    catch(PDOException $e){
      print('Error : ' . $e->getMessage());
      exit();
    }    
  }


  function add()
  {
    try {
      //$stmt = $this->db->prepare("INSERT INTO customer (ID, fio, email, tax_region) VALUES(:ID, :fio, :email, :tax_region);");
      $stmt = $this->db->prepare("INSERT INTO customer (ID, fio, email) VALUES(:ID, :fio, :email);");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->bindParam(':fio', $this->fio);
      $stmt->bindParam(':email', $this->email);
      //$stmt->bindParam(':tax_region', $this->tax_region);
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
      //$stmt = $this->db->prepare("UPDATE customer SET fio = :fio, email = :email, tax_region = :tax_region WHERE ID=:ID;");
      $stmt = $this->db->prepare("UPDATE customer SET fio = :fio, email = :email WHERE ID=:ID;");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->bindParam(':fio', $this->fio);
      $stmt->bindParam(':email', $this->email);
      //$stmt->bindParam(':tax_region', $this->tax_region);
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
      $stmt = $this->db->prepare("DELETE FROM customer WHERE ID = :ID");
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
      <caption>Клиенты</caption>
      <tr>
        <th>ID</th>
        <th>ФИО</th>
        <th>Способ связи</th>
      <tr>';
      $stmt = $db->prepare("DESC customer");      
      $stmt->execute();
      $columns=array();
      $column=$stmt->fetchColumn();
      for($i=0;$column!=false;$i++){
        $columns[$i]=$column;
        $column=$stmt->fetchColumn();
      }
      $stmt = $db->prepare("SELECT * FROM customer");         
      $stmt->execute();
      $line=array();
      for($line=$stmt->fetch();!empty($line);$line=$stmt->fetch()){
        print'<tr>';
        $PK=$columns[0];        
        foreach ($columns as $col) {
          print'<td>'.$line[$col].'</td>';    
        }
        print '<form action="" method="POST">
                 <input name="PK" value="'.strip_tags($line[$PK]).'" hidden>
                 <input name="csrf_token" value="'.$token.'" hidden>
                 <td><input type="submit" name="change" value="Изменить"></td>
               <td class="delete"><input type="submit" name="delete" value="Удалить"></td>
              </form>';
        print'<tr>';
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