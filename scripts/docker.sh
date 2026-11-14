#!/usr/bin/env bash
# Linux/macOS: bash scripts/docker.sh preparar|iniciar|parar|exportar-offline
set -euo pipefail
cd "$(dirname "$0")/.."
command -v docker >/dev/null || { echo 'Instale/inicie Docker com Compose v2.' >&2; exit 1; }
[[ "$(docker info --format '{{.OSType}}')" == linux ]] || { echo 'Use conteineres Linux.' >&2; exit 1; }
docker compose version

checksum() {
    if command -v sha256sum >/dev/null; then sha256sum "$1" | cut -d ' ' -f 1
    else shasum -a 256 "$1" | cut -d ' ' -f 1; fi
}

case "${1:-}" in
    preparar)
        if [[ "${2:-}" == --offline ]]; then
            [[ -f offline/manifest.json && -f offline/imagens.tar ]] || { echo 'Pacote offline ausente.' >&2; exit 1; }
            expected=$(sed -n 's/.*"sha256"[[:space:]]*:[[:space:]]*"\([a-f0-9]*\)".*/\1/p' offline/manifest.json)
            [[ -n "$expected" && "$(checksum offline/imagens.tar)" == "$expected" ]] || { echo 'Hash invalido.' >&2; exit 1; }
            expected_arch=$(sed -n 's/.*"architecture"[[:space:]]*:[[:space:]]*"\([a-z0-9_]*\)".*/\1/p' offline/manifest.json)
            arch=$(docker info --format '{{.Architecture}}')
            [[ "$arch" != x86_64 ]] || arch=amd64
            [[ "$arch" != aarch64 ]] || arch=arm64
            [[ "$arch" == "$expected_arch" ]] || { echo 'Pacote de outra arquitetura.' >&2; exit 1; }
            docker load -i offline/imagens.tar
        else
            docker build --pull -t unifica-portal:demo .
            docker pull quay.io/keycloak/keycloak:26.8.2
        fi
        docker run --rm --user "$(id -u):$(id -g)" --mount "type=bind,source=$PWD,target=/workspace" --workdir /workspace --entrypoint python unifica-portal:demo scripts/configurar_demo.py
        docker compose config --quiet
        echo 'Preparado. Use: bash scripts/docker.sh iniciar'
        ;;
    iniciar)
        [[ -f .demo/app.env ]] || { echo 'Execute preparar primeiro.' >&2; exit 1; }
        docker compose up -d --no-build --pull never --wait --wait-timeout 360
        echo 'Portal: http://localhost:5000 | Keycloak: http://localhost:8081'
        ;;
    parar)
        docker compose stop
        ;;
    exportar-offline)
        mkdir -p offline
        arch=$(docker image inspect unifica-portal:demo --format '{{.Architecture}}')
        [[ "$arch" == "$(docker image inspect quay.io/keycloak/keycloak:26.8.2 --format '{{.Architecture}}')" ]] || { echo 'Imagens de arquiteturas diferentes.' >&2; exit 1; }
        docker save -o offline/imagens.tar unifica-portal:demo quay.io/keycloak/keycloak:26.8.2
        printf '{"architecture":"%s","sha256":"%s"}\n' "$arch" "$(checksum offline/imagens.tar)" > offline/manifest.json
        echo 'Pacote offline exportado. Nao copie .demo, .env, .venv ou .git.'
        ;;
    *)
        echo 'Uso: bash scripts/docker.sh preparar [--offline] | iniciar | parar | exportar-offline' >&2
        exit 1
        ;;
esac
