<?php
require_once 'Migration.php';

class AdvClickRecordMig extends Migration
{
    public function migration()
    {
        $day = date('Ymd', strtotime("-3 day"));
        $this->MySQLDump('wx_adv_click_record_' . $day, $day);
    }
}


$c = new AdvClickRecordMig();
$c->migration();