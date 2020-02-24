<?php
require_once 'Migration.php';

class ConsumerReportMig extends Migration
{
    public function migration()
    {
        $threeDayDate = date('Ymd', strtotime("-3 day"));
        $this->MySQLDump('wx_consumer_report_' . $threeDayDate, $threeDayDate);
    }
}


$c = new ConsumerReportMig();
$c->migration();