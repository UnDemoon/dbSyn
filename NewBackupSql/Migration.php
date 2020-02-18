<?php

require_once 'vendor/autoload.php';

use Medoo\Medoo;

class Migration extends Medoo
{

    public $config = [
        'servers'  => [
            'online'  => [
                'server'   => 'rm-bp11j7ex56770w4h40o.mysql.rds.aliyuncs.com',
                'username' => 'houyiroot',
                'password' => 'Qy634ce#43f189462',
            ],
            'online_ddl'  => [
                'server'   => 'rm-bp11j7ex56770w4h40o.mysql.rds.aliyuncs.com',
                'username' => 'hy_record_opt',
                'password' => 'houyi@record!Opt',
            ],
        ]
    ];

    public function __construct()
    {
    }

    public function MySQLDump($tableName, $time){
        if(!is_dir("/home/backup/{$time}")){
            mkdir("/home/backup/{$time}", 0777, TRUE);
        }
        $logPath = "/home/backup/{$time}/" . $tableName . '.sql';
        system("mysqldump -h{$this->config['servers']['online']['server']} -u{$this->config['servers']['online']['username']} -p{$this->config['servers']['online']['password']} minigame_stat {$tableName} > {$logPath}");

        if(file_exists($logPath)){

            $db = new Medoo([
                'database_type' => 'mysql',
                'database_name' => 'minigame_stat',
                'server'        => $this->config['servers']['online_ddl']['server'],
                'username'      => $this->config['servers']['online_ddl']['username'],
                'password'      => $this->config['servers']['online_ddl']['password'],
            ]);

            $db->drop($tableName);
        }
    }





}
