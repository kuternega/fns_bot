<!DOCTYPE html>

<html lang="ru" >
<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="style.css">
    <title></title>
</head>
<body>
  <div>
    <?php 
    if (!empty($messages)) {
      foreach($messages as $message){
        print $message;
      }
    }
    ?>
  </div>
  <form action="" method="POST">
      <input name="cancel" type="submit" value="Отмена">
    </form>
  <div id="form">
    <form action=""
      method="POST">
       <label>
        Telegramm ID клиента:<br />
        <input name="customer_id" <?php if ($errors['customer_id']) {print 'class="error"';} ?> value="<?php print $form_val['customer_id']; ?>" />
      </label><br />
      <label>
        Telegramm ID оператора:<br />
        <input name="emp_id" <?php if ($errors['emp_id']) {print 'class="error"';} ?> value="<?php print $form_val['emp_id']; ?>" />
      </label><br />
      <label>
        Статус:<br />
        <input name="status" <?php  if ($errors['status']) {print 'class="error"';} ?> value="<?php print $form_val['status']; ?>" />
      </label><br />
      <input type="hidden" name="csrf_token" value="<?php print $token; ?>">
      <input type="submit" value="Отправить" />
    </form>
  </div>
</body>
</html>
