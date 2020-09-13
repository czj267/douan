<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
<table style="table-layout: fixed;">
    <tbody>
    <?php
    ini_set('display_errors','On');
    $db = new PDO("mysql:host=localhost;dbname=douban", 'root', 'root');

    $stat = $db->query("select * from rent where is_del = 0 order by a_updated_at desc limit 1000");
    foreach ($stat->fetchAll(PDO::FETCH_ASSOC) as $row) {
        $up = date("d H:i:s",strtotime($row['a_updated_at']));
        echo <<<tr
            <tr>
                <td><a style="text-decoration: none;" href="https://www.douban.com/group/topic/{$row['a_id']}" target="_blank">{$row['title']}</a></td>
                <td>{$up}</td>
                <td style="width: 60px;"><button onclick="del_item(this,'{$row['id']}')">删除</button></td>
            </tr>
tr;

    } ?>
    </tbody>
</table>
<script src="/jq-2.0.js"></script>
<script>
    function del_item(obj,id) {
        fetch('/op.php?op=del&id=' + id).then(res => {
            $(obj).parent().parent().remove()
        })
    }
</script>
</body>
</html>

