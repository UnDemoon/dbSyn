<?php
require_once 'Migration.php';

class SceneRecordAppidMig extends Migration
{
    public function migration()
    {
        $threeDayDate = date('Ymd', strtotime("-8 day"));
        $this->MySQLDump('wx_scene_record_appid_' . $threeDayDate, $threeDayDate);
    }
}


$c = new SceneRecordAppidMig();
$c->migration();