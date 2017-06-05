<html>
<head>
    <link rel="apple-touch-icon" sizes="57x57" href="/img/apple-touch-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/img/apple-touch-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/img/apple-touch-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/img/apple-touch-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/img/apple-touch-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/img/apple-touch-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/img/apple-touch-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/img/apple-touch-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon-180x180.png">
    <link rel="icon" type="image/png" href="/img/favicon-32x32.png" sizes="32x32">
    <link rel="icon" type="image/png" href="/img/android-chrome-192x192.png" sizes="192x192">
    <link rel="icon" type="image/png" href="/img/favicon-96x96.png" sizes="96x96">
    <link rel="icon" type="image/png" href="/img/favicon-16x16.png" sizes="16x16">
    <link rel="manifest" href="/img/manifest.json">
    <link rel="mask-icon" href="/img/safari-pinned-tab.svg" color="#5bbad5">
    <link href="img/favicon.ico" rel="SHORTCUT ICON" />
    <meta name="msapplication-TileColor" content="#da532c">
    <meta name="msapplication-TileImage" content="/img/mstile-144x144.png">
    <meta name="theme-color" content="#ffffff">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" />
    <link rel="stylesheet" rev="stylesheet" href="style.css" type="text/css" media="screen" charset="utf-8" />
    <script src="jscolor.js"></script>
    <title>Aquarius</title>
    <script>
        var imageNr=0;
        setInterval(function(){document.getElementById('data').src = 'data.php?n='+(imageNr++);},60000);
        function SetLine(valore,linea){
            document.getElementById('command').src = 'update.php?value='+valore+'&riga='+linea;
        }
        function Upgrade(){
            var ask=confirm("Aggiornamento del sistema.\nSei sicuro?");
            if(ask){
                window.countdown=60;
                document.getElementById('command').src = 'upgrade.php';
                window.scrollTo(0, 0);
                setInterval(function(){
                                    window.countdown=window.countdown-1;
                                    document.getElementById('messaggio').innerHTML='<br/><center>Attendere '+countdown.toString()+' secondi...</center><br/><br/>';
                                    if (window.countdown==0){window.location = '/';}
                                },1000);
            }
        }        
    </script>
</head>
<?php
function GetLine($n){
    $handle = fopen("/home/pi/acquario.cfg", "r");
    if ($handle) {
        for ($i = 1; $i <= $n; $i++){
            $line = fgets($handle);
        }
        fclose($handle);
    }    
    return $line;
}
?>
<body>
    <div style="width:98%;background:navy;padding:5px;"><img id="logo" src="img/aquarius.png"/><div id="header" style="color:cyan;">Aquarius</div></div>
    <div id="messaggio" style="color:yellow;" class="pclear"><br/></div>
    <iframe id="data" src="data.php"></iframe>
    <br/><br/>
    <div class="maschera" style="width:180px;">
        <b>Ventilazione:</b><br/><br/>
        Avvia: <input style="float:right;" type="number" name="fan_start" min="0" max="35" onchange="SetLine(this.value,'1')" value=<?php echo$
        Ferma: <input style="float:right;" type="number" name="fan_stop" min="0" max="35" onchange="SetLine(this.value,'2')" value=<?php echo $
    </div>
    <div class="maschera" style="width:180px;">
        <b>Dosaggio cibo:</b><br/><br/>
        Inizio: <input style="width:110px;height:32px;float:right;" type="time" name="lunch_time" onchange="SetLine(this.value,'12')" value=<?$
        Fine: <input style="width:110px;height:32px;float:right;" type="time" name="elunch_time" onchange="SetLine(this.value,'13')" value=<?p$
    </div>
    <div class="pclear"><br/></div>
    <p style="margin-left:10px;"><b>Illuminazione</b></p>
    <div class="pclear"></div>
    <div class="maschera">
        <b>Alba</b><br/><br/>
        <input style="width:110px;" type="time" name="night_time"  onchange="SetLine(this.value,'5')"value=<?php echo GetLine(5); ?> /><br/>
        <input class="jscolor {value:'<?php echo substr(GetLine(6),1,6); ?>'}" onchange="SetLine(this.jscolor,'6')" style="width:110px;height:64px;font-size:0;opacity:1;" disabled>
    </div>
    <div class="maschera">
        <b>Giorno</b><br/><br/>
        <input style="width:110px;" type="time" name="night_time"  onchange="SetLine(this.value,'7')"value=<?php echo GetLine(7); ?> /><br/>
        <input class="jscolor {value:'<?php echo substr(GetLine(8),1,6); ?>'}" onchange="SetLine(this.jscolor,'8')" style="width:110px;height:64px;font-size:0;opacity:1;"" disabled>
    </div>
    <div class="maschera">
        <b>Tramonto</b><br/><br/>
        <input style="width:110px;" type="time" name="night_time"  onchange="SetLine(this.value,'9')"value=<?php echo GetLine(9); ?> /><br/>
        <input class="jscolor {value:'<?php echo substr(GetLine(10),1,6); ?>'}" onchange="SetLine(this.jscolor,'10')" style="width:110px;height:64px;font-size:0;opacity:1;"" disabled>
    </div>
    <div class="maschera">
        <b>Notte</b><br/><br/>
        <input style="width:110px;" type="time" name="night_time" onchange="SetLine(this.value,'3')" value=<?php echo GetLine(3); ?> /><br/>
        <input class="jscolor {value:'<?php echo substr(GetLine(4),1,6); ?>'}" onchange="SetLine(this.jscolor,'4')" style="width:110px;height:64px;font-size:0;opacity:1;"" disabled>
    </div>
    <iframe id="command" src="" style="display:none;"></iframe>
    <div class="pclear"><br/><br/><br/></div>
    <center><button type="button" class="button" onclick="Upgrade()">Aggiorna</button></center>
    <div class="pclear"><br/></div>
</body>
</html>
