# Step1
pwd
cd {{cookiecutter.proj_name}} && git stash
cd {{cookiecutter.proj_name}} && git pull

docker restart {{cookiecutter.proj_name}} || true
