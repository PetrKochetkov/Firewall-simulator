<?php
$n = $i = $argv[1] ?? 5;

while ($i--) {
    echo str_repeat(' ', $i).str_repeat('* ', $n - $i)."\n";
}