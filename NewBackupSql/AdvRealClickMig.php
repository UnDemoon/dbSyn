<?php
require_once 'Migration.php';

class AdvRealClickMig extends Migration
{
    public function migration()
    {
        $day = date('Ymd', strtotime("-3 day"));
        $this->MySQLDump('wx_adv_real_click_' . $day, $day);
    }
}


$c = new AdvRealClickMig();
//$c->migration();
// 这个表没用 zhangyue 20200227