<?php 
    $handle = file("/home/pi/acquario.cfg");
    $riga=intval($_GET['riga']);
    $valore=$_GET['value'];
    if ($riga==4 || $riga==6 || $riga==8 || $riga==10){$valore='#'.$valore;}
    $handle[$riga-1]=$valore."\n";
    $result=implode($handle);
    file_put_contents("/home/pi/acquario.cfg",$result);
?>