set dotenv-filename := "ceiaun_bot/.env"
set dotenv-load := true

src_dir := "ceiaun_bot"

# Aliases
alias upd := up-dev
alias updb := up-dev-build
alias updbr := up-dev-build-recreate
alias imgprun := image-prune
alias pre := run-pre-commit
alias repre := reinstall-pre-commit

default:
    @just --list --unsorted

# Docker

_docker *args="":
    docker compose -f {{ src_dir }}/docker-compose.yml {{ args }}

# Docker command for development
docker *args:
    @just _docker {{ args }}

# Docker compose up for development
up-dev *flags="":
    @just docker up {{ flags }}

# Docker compose up for development with --build argument
up-dev-build:
    @just docker up --build

# Docker compose up for development with --build and --force-recreate argument
up-dev-build-recreate *flags="":
    @just docker up --build --force-recreate {{ flags }}

# Remove dangling docker image
image-prune:
    docker image rm $(docker image ls -f 'dangling=true' -q)

# Run pre-commit
run-pre-commit:
    pre-commit run --all-files -v

# Reinstall pre-commit
reinstall-pre-commit:
    pre-commit uninstall
    pre-commit install --hook-type pre-commit --hook-type pre-push
