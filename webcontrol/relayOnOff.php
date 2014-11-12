<html>
  <body>

	<?php
	     if (isset($_POST['Relay1_On'])){
           shell_exec('./rfsn_ctl rfsn-demo1-rly.vip.gatech.edu on');
         }
         if (isset($_POST['Relay1_Off'])){
           shell_exec('./rfsn_ctl rfsn-demo1-rly.vip.gatech.edu off');
         }
         if (isset($_POST['Relay2_On'])){
           shell_exec('./rfsn_ctl rfsn-demo2-rly.vip.gatech.edu on');
         }
         if (isset($_POST['Relay2_Off'])){
           shell_exec('./rfsn_ctl rfsn-demo2-rly.vip.gatech.edu off');
         }
    ?>

  </body>
</html> 