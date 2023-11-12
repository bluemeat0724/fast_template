# Step1
pwd
cd {{cookiecutter.proj_dir}} && git stash
cd {{cookiecutter.proj_dir}} && git pull

docker restart {{cookiecutter.proj_name}} || true
