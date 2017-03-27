<?php 
//$output = shell_exec('/home/pi/script/rpi.py');
$output = '<html><body style="margin:0;padding:0;">';
$temp = '22.3';
$output = $output . '<p style="color:white;font-size:18px;">'.date("d/m/Y H:i").'</p>';
$output = $output . '<p style="color:white;margin:0;padding:0;font-size:18px;">Temperatura acqua:<br/><span style="color:white;font-size:32px;"><b>'.$temp.'°C</b></span></p>';
$output = $output . '</html></body>';
echo $output;
?>