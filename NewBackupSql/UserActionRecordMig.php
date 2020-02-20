<?php
require_once './Migration.php';

class UserActionRecordMig extends Migration
{
    public function migration()
    {
        $day = date('Ymd', strtotime("-8 day"));
        $this->MySQLDump('wx_user_action_record_' . $day, $day);
    }
}


$c = new UserActionRecordMig();
$c->migration();