git.exe config --global user.email qgbcs1@gmail.com
git.exe config --global user.name QGB
   
git.exe config --global core.filemode false
git.exe config --global credential.helper store
   
git.exe remote add q https://github.com/qgb/qpsu
git.exe remote add cq https://coding.net/u/qgb/p/QPSU/git
git.exe add -A
git.exe commit -m %*
git.exe push cq master 
git.exe push q master 