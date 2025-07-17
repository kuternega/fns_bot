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
        ФИО:<br />
        <input name="fio" <?php if ($errors['fio']) {print 'class="error"';} ?> value="<?php print $form_val['fio']; ?>" />
      </label><br />      
        Способ связи:<br />
        <input name="email" <?php if ($errors['email']) {print 'class="error"';} ?> value="<?php print $form_val['email']; ?>" />
      </label><br />
      <!-- 
      <label>
        Регион налоговой:<br />
        <input name="tax_region" <?php //if ($errors['tax_region']) {print 'class="error"';} ?> value="<?php //print $form_val['tax_region']; ?>" />
      </label><br />
      -->
   
      <input type="hidden" name="csrf_token" value="<?php print $token; ?>">
      <input type="submit" value="Отправить" />
    </form>
  </div>
</body>
</html>
