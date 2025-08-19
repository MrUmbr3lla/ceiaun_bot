set dotenv-filename := ".env"
set dotenv-load := true

# Aliases
alias upr := up-recreate
alias upbr := up-build-recreate
alias imgprun := image-prune
alias pre := run-pre-commit
alias repre := reinstall-pre-commit

default:
    @just --list --unsorted

# Docker compose command
_docker *args="":
    docker compose -f docker-compose.yml {{ args }}

# Docker command
docker *args:
    @just _docker {{ args }}

# Docker compose up
up *flags="":
    @just docker up {{ flags }}

# Docker compose up with --force-recreate argument
up-recreate:
    @just docker up --force-recreate

# Docker compose up with --build and --force-recreate argument
up-build-recreate *flags="":
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
