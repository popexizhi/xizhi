ls -1 testdata| xargs -i sed -i "s/$/ {}/g" testdata/{}
cat testdata/* > now.log
vim -S ue.vim now.log
