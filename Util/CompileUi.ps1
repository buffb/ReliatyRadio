$files = Get-ChildItem  *.ui
foreach ($f in $files){
    $f.BaseName
    pyuic5 -x $f.Name > "$($f.BaseName).py"
}