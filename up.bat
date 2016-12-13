: @echo off
git config --global user.email qgbcs1@gmail.com
git config --global user.name QGB
git remote add q https://github.com/qgb/qpsu
git remote add cq https://coding.net/u/qgb/p/QPSU/git
git add -A
git commit -m %*
git push cq master 
git push q master 