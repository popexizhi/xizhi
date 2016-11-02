ls -1 testdata| xargs -i sed -i "s/$/ {}/g" testdata/{}
