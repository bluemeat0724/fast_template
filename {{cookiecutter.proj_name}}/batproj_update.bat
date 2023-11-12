@echo off
git add .
git commit -m 'update'
git push
setlocal
set "SERVER=root@{{cookiecutter.dev_host}}"
set "COMMAND=bash {{cookiecutter.proj_name}}/sh_devrun.sh"

ssh -p 5022 %SERVER% "sudo su -c '%COMMAND%'"
endlocal