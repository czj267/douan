<?php
$op = $_GET['op'];
$id = $_GET['id'];
$db = new PDO("mysql:host=localhost;dbname=douban", 'root', 'root');

switch ($op) {
    case 'del':
        $res = $db->exec("update rent set is_del = 1 where id = {$id} limit 1");
        var_dump($res);
        echo json_encode(['code' => 0]);
        break;
}