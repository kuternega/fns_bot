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
        Telegramm ID:<br />
        <input name="ID" <?php if ($errors['ID']) {print 'class="error"';} ?> value="<?php print $form_val['ID']; ?>" />
      </label><br />
       <label>
        Имя:<br />
        <input name="first_name" <?php if ($errors['first_name']) {print 'class="error"';} ?> value="<?php print $form_val['first_name']; ?>" />
      </label><br />
      <label>
        Фамилия:<br />
        <input name="last_name" <?php if ($errors['last_name']) {print 'class="error"';} ?> value="<?php print $form_val['last_name']; ?>" />
      </label><br />
      <label>
        Отчество:<br />
        <input name="father_name" <?php if ($errors['father_name']) {print 'class="error"';} ?> value="<?php print $form_val['father_name']; ?>" />
      </label><br />
   
      <input type="hidden" name="csrf_token" value="<?php print $token; ?>">
      <input type="submit" value="Отправить" />
    </form>
  </div>
</body>
</html>
