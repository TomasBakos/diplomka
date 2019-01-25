<?php
  include('data.php');

  function connect(){
    if ($link = mysql_connect('localhost', 'bakos18', 'mooxe')) {
		  if (mysql_select_db('bakos18', $link)) {
			 mysql_query("SET CHARACTER SET 'utf8'", $link); 
			 return $link;
		  } else {
       echo "Nepodarilo sa vybrat databazu";
			 return false;
		  }
	  } else {
      echo "Nepodarilo sa spojit s databazovym serverom";
		  return false;
	  }
  }

  function hlavicka($titulok){
  ?>
    <!DOCTYPE html>
    <html>
    <head>
    <link href="style.css" rel="stylesheet">
    <meta charset="utf-8">
    <title>Evidencia Hackerov</title>
    </head>
 
    <body>
 
    <header>
    <h1><?php echo $titulok;?></h1>
    </header>
  <?php
  }
  
  function navigacia(){
  ?>
    <nav>
    <p><a href="index.php">Index</a> <a href="zoznam.php">Zoznam</a> <a href="eviduj.php">Eviduj</a> <a href="uprava.php">Úprava</a></p>
    </nav>
  <?php    
  }
  
  function paticka(){
  ?>
    <footer>
    <p>vytvoril: <em>Tomáš Bakoš</em></p>
    </footer>
  <?php  
  }
  
  function novinky(){
  ?>
    <aside>
      <p>Pridajte sa do nasej evidencie uz teraz !</p>
    </aside>
  <?php   
  }

  function init (){
  session_start();
  global $zoznam;
  if (!(isset ($_SESSION['pole']))) {
    $_SESSION['pole'] = $zoznam;
  }
  }

  function vypis_upravu (){
     vypis_hackerov_uprava();
     echo "<input type='submit' name='zmaz' value='Zmaz !'>
          <input type='submit' name='uprav' value='Uprav !'>
          </form>";      
  }
  
  function jednoslovo($slovo){
    $slovo = addslashes(strip_tags(trim($slovo)));
    $pom = explode(' ',$slovo);
    return (count($pom) == 1);
  } 
  
  function jecislo($cislo){
  $cislo = addslashes(strip_tags(trim($cislo)));
    for ($i = 0; $i < strlen($cislo); $i++){
      if (!(is_numeric($cislo[$i]))){
        return false;
      }
    }
    return true;  
  }
  
  function pridaj_hackera() {
    if ($link = connect()) {
      $sql = "INSERT 
              INTO hacker_zoznam 
              SET nick='" . $_POST['nick'] . "',
              specializacia='" . $_POST['spec'] . "',
              sikovnost='" . $_POST['sik'] . "',
              poc_prich='" . $_POST['prich'] . "'";
      $result = mysql_query($sql, $link);
      if ($result) {
        // podarilo sa vykonať dopyt
        echo "Úspešne ste pridali hackera";
      } else {
        // nepodarilo sa vykonat dopyt
        echo "Nepodarilo sa vykonat dopyt";
        }
    mysql_close($link);
  } else {
    // nepodarilo sa spojit s databazovym serverom
    echo "Nepodarilo sa spojit s databazovym serverom";
  }
  }
  
  function vypis_hackerov() {
  if ($link = connect()) {
      $sql = "SELECT * 
            FROM  hacker_zoznam 
            LEFT JOIN hacker_elita
            ON hacker_zoznam.ID=hacker_elita.ID 
            LIMIT 0 , 30"; 
    $result = mysql_query($sql, $link);
    if ($result) {
      // podarilo sa vykonať dopyt
      echo "<table>
            <tr><th>Nick</th><th>Specializacia</th><th>Sikovnost</th><th>Pocet Prichyteni</th><th>Kvalita</th></tr>";
      while ($row = mysql_fetch_assoc($result)) {
        echo "<tr>"
        echo "<td>" . $row['nick']. "</td>";
        echo "<td>" . $row['specializacia'] . "</td>";
        echo "<td>" . $row['sikovnost']. "</td>";
        echo "<td>" . $row['poc_prich']. "</td>";
        echo "<td>" . $row['kvalita'] . "</td>";
        echo "</tr>"
      }
      echo "</table>"
      } else {
        // nepodarilo sa vykonat dopyt
        echo "Nepodarilo sa vykonat dopyt";
        }
    mysql_close($link);
  } else {
    // nepodarilo sa spojit s databazovym serverom
    echo "Nepodarilo sa spojit s databazovym serverom";
    }
  }
  
  function vypis_hackerov_uprava() {
  ?>
	    <form method="post">
  <?php
	   if ($link = connect()) {
		    $sql="SELECT * 
              FROM `hacker_zoznam`
              LIMIT 0 , 30"; // definuj dopyt
  	    $result = mysql_query($sql, $link); // vykonaj dopyt
        if ($result) {
			   // podarilo sa vykonat dopyt
			   echo '<p>'; 
			   while ($row = mysql_fetch_assoc($result)) { 			
    		    echo '<input type="radio" name="id" value="'. $row['ID'] .'">' . $row['nick'] . "<br>\n";
			   } 
			   echo '</p>';  
  	   } else {
			   // nepodarilo sa vykonat dopyt
    	   echo "Nepodarilo sa vykonat dopyt";
        }
        mysql_close($link);
	   } else {
		    // nepodarilo sa spojit s databazovym serverom
		    echo "Nepodarilo sa spojit s databazovym serverom";
	   }
   ?>
  <?php  
  }   
 
  function zmaz_hackera() {
      if ($link = connect()) {
		    $sql="DELETE 
              FROM hacker_zoznam
              WHERE ID='" . $_POST['id'] ."'"; // definuj dopyt
  	    $result = mysql_query($sql, $link); // vykonaj dopyt
        if ($result) {
			   // podarilo sa vykonat dopyt
			   echo "Uspesne ste vymazali hackera"; 
  	   } else {
			   // nepodarilo sa vykonat dopyt
    	   echo "Nepodarilo sa vykonat dopyt";
        }
        mysql_close($link);
	   } else {
		    // nepodarilo sa spojit s databazovym serverom
		    echo "Nepodarilo sa spojit s databazovym serverom";;
	   }        
  }
  
  function uprava_hackera() {
      if ($link = connect()) {
         $sql = "UPDATE hacker_zoznam 
         SET nick='" . $_POST['nick'] . "', 
         specializacia='" . $_POST['spec'] . "', 
         sikovnost='" . $_POST['sik'] . "', 
         poc_prich='" . $_POST['prich'] . "'
         WHERE ID='" . $_POST['id'] . "'";
         $result = mysql_query($sql, $link); // vykonaj dopyt
         if ($result) {
          // podarilo sa vykonat dopyt
          echo "Úspešne ste pridali hackera";
        } else {
          // nepodarilo sa vykonat dopyt
          echo "Nepodarilo sa vykonat dopyt";
          }
      mysql_close($link);
      } else {
        // nepodarilo sa spojit s databazovym serverom
        echo "Nepodarilo sa spojit s databazovym serverom";
      }    
  }
  
?>