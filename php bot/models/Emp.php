<?php

class Emp
{
  public $ID;
  public $first_name;
  public $last_name;
  public $father_name;
  public $db;


  function __construct($ID,$first_name=NULL,$last_name=NULL,$father_name=NULL)
  {
    if($ID==NULL){
      $this->ID = '';
      $this->first_name = '';
      $this->last_name = '';
      $this->father_name = '';
      $this->db=dbconnect();
    }
    else{
      $this->ID = $ID;
      $this->first_name = $first_name;
      $this->last_name = $last_name;
      $this->father_name = $father_name;
      $this->db=dbconnect();
      }
  }


  function to_array(){
    $arr['ID'] = $this->ID;
    $arr['first_name'] = $this->first_name;
    $arr['last_name'] = $this->last_name;
    $arr['father_name'] = $this->father_name;
    return $arr;
  }

  function no_errors()
  {
    $errors['ID'] = '0';
    $errors['first_name'] = '0';
    $errors['last_name'] = '0';
    $errors['father_name'] = '0';
    return $errors;
  }


function errors_check()
  {
    $errors['ID'] = '0';
    $errors['first_name'] = '0';
    $errors['last_name'] = '0';
    $errors['father_name'] = '0'; 
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

    if (empty($_POST['first_name'])){
      $errors['first_name'] = '1';
      $errors['error'] = TRUE;
      $this->first_name = '';
    }
    else
      $this->first_name = $_POST['first_name'];
    if (empty($_POST['last_name'])){
      $errors['last_name'] = '1';
      $errors['error'] = TRUE;
      $this->last_name = '';
    }
    else
      $this->last_name = $_POST['last_name'];

    if (empty($_POST['father_name'])){
      $errors['father_name'] = '1';
      $errors['error'] = TRUE;
      $this->father_name = '';
    }
    else
      $this->father_name = $_POST['father_name']; 
    return $errors;
  }


  function load()
  {
    try {
      $stmt = $this->db->prepare("SELECT * FROM emp where ID = :ID");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->execute();
      $data=$stmt->fetch();
      $this->first_name = $data['first_name'];
      $this->last_name = $data['last_name'];
      $this->father_name = $data['father_name'];
    }
    catch(PDOException $e){
      print('Error : ' . $e->getMessage());
      exit();
    }    
  }


  function add()
  {
    try {
      $stmt = $this->db->prepare("INSERT INTO emp (ID, first_name, last_name, father_name) VALUES(:ID, :first_name, :last_name, :father_name);");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->bindParam(':first_name', $this->first_name);
      $stmt->bindParam(':last_name', $this->last_name);
      $stmt->bindParam(':father_name', $this->father_name);
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
      $stmt = $this->db->prepare("UPDATE emp SET first_name = :first_name, last_name = :last_name, father_name = :father_name WHERE ID=:ID;");
      $stmt->bindParam(':ID', $this->ID);
      $stmt->bindParam(':first_name', $this->first_name);
      $stmt->bindParam(':last_name', $this->last_name);
      $stmt->bindParam(':father_name', $this->father_name);
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
      $stmt = $this->db->prepare("DELETE FROM emp WHERE ID = :ID");
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
      <caption>Операторы</caption>
      <tr>
        <th>ID</th>
        <th>Имя</th>
        <th>Фамилия</th>
        <th>Отчество</th>
      <tr>';
      $stmt = $db->prepare("DESC emp");      
      $stmt->execute();
      $columns=array();
      $column=$stmt->fetchColumn();
      for($i=0;$column!=false;$i++){
        $columns[$i]=$column;
        $column=$stmt->fetchColumn();
      }
      $stmt = $db->prepare("SELECT * FROM emp");         
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
