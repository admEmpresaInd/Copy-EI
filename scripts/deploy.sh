#!/usr/bin/env bash
# =============================================================================
# Deploy Script - Copy EI
# =============================================================================
# Automates: git add -u -> commit -> push -> Vercel production deploy
#
# Usage:
#   bash scripts/deploy.sh "feat: minha mensagem de commit"
#   bash scripts/deploy.sh                 # uses default commit message
#
# Flow:
#   1. git add -u       (apenas arquivos ja rastreados — evita incluir lixo)
#   2. git commit -m    (usa mensagem passada ou padrao)
#   3. git push origin master
#   4. npx vercel --prod
# =============================================================================

set -u  # Treat unset variables as errors; DO NOT use -e so we can handle steps

# -----------------------------------------------------------------------------
# Cores para output legivel
# -----------------------------------------------------------------------------
if [ -t 1 ]; then
  C_RESET="\033[0m"
  C_BOLD="\033[1m"
  C_GREEN="\033[32m"
  C_YELLOW="\033[33m"
  C_RED="\033[31m"
  C_BLUE="\033[34m"
  C_CYAN="\033[36m"
else
  C_RESET=""; C_BOLD=""; C_GREEN=""; C_YELLOW=""; C_RED=""; C_BLUE=""; C_CYAN=""
fi

step() {
  printf "\n${C_BOLD}${C_CYAN}==> %s${C_RESET}\n" "$1"
}

ok() {
  printf "${C_GREEN}[OK]${C_RESET} %s\n" "$1"
}

warn() {
  printf "${C_YELLOW}[WARN]${C_RESET} %s\n" "$1"
}

fail() {
  printf "${C_RED}[FAIL]${C_RESET} %s\n" "$1"
  exit 1
}

info() {
  printf "${C_BLUE}[INFO]${C_RESET} %s\n" "$1"
}

# -----------------------------------------------------------------------------
# Argumentos
# -----------------------------------------------------------------------------
DEFAULT_MSG="chore: deploy $(date +'%Y-%m-%d %H:%M')"
COMMIT_MSG="${1:-$DEFAULT_MSG}"

# -----------------------------------------------------------------------------
# Banner
# -----------------------------------------------------------------------------
printf "${C_BOLD}${C_CYAN}"
cat <<'BANNER'
+------------------------------------------------------------+
|  Copy EI - Deploy Pipeline                                 |
|  git add -u -> commit -> push -> vercel --prod             |
+------------------------------------------------------------+
BANNER
printf "${C_RESET}\n"

info "Commit message: ${C_BOLD}${COMMIT_MSG}${C_RESET}"

# -----------------------------------------------------------------------------
# Pre-flight: garantir que estamos num repo git
# -----------------------------------------------------------------------------
step "Pre-flight checks"
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  fail "Not a git repository. Run this from inside 'D:/Copy EI'."
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
info "Branch atual: ${C_BOLD}${BRANCH}${C_RESET}"

# -----------------------------------------------------------------------------
# 1. git add -u (apenas arquivos ja rastreados)
# -----------------------------------------------------------------------------
step "1/4 git add -u (staged tracked changes)"
if git add -u; then
  STAGED_COUNT=$(git diff --cached --name-only | wc -l | tr -d ' ')
  if [ "${STAGED_COUNT}" = "0" ]; then
    warn "Nenhuma mudanca em arquivos rastreados. Pulando commit/push."
    SKIP_COMMIT=1
  else
    ok "${STAGED_COUNT} arquivo(s) staged"
    git diff --cached --name-status | sed 's/^/     /'
    SKIP_COMMIT=0
  fi
else
  fail "git add -u falhou"
fi

# -----------------------------------------------------------------------------
# 2. git commit
# -----------------------------------------------------------------------------
if [ "${SKIP_COMMIT:-0}" = "0" ]; then
  step "2/4 git commit"
  if git commit -m "${COMMIT_MSG}"; then
    ok "Commit criado"
  else
    fail "git commit falhou"
  fi
else
  info "Sem mudancas para commitar. Seguindo direto para o push + deploy."
fi

# -----------------------------------------------------------------------------
# 3. git push origin <branch>
# -----------------------------------------------------------------------------
step "3/4 git push origin ${BRANCH}"
if git push origin "${BRANCH}"; then
  ok "Push para origin/${BRANCH} concluido"
else
  fail "git push falhou — verifique autenticacao/remote"
fi

# -----------------------------------------------------------------------------
# 4. Vercel production deploy
# -----------------------------------------------------------------------------
step "4/4 Vercel production deploy"
info "Executando: npx vercel --prod"
if npx vercel --prod; then
  ok "Deploy Vercel disparado com sucesso"
else
  fail "Deploy Vercel falhou — verifique 'npx vercel login' e 'npx vercel link'"
fi

# -----------------------------------------------------------------------------
# Resumo final
# -----------------------------------------------------------------------------
printf "\n${C_BOLD}${C_GREEN}"
cat <<'DONE'
+------------------------------------------------------------+
|  Deploy completo. Tudo pronto.                             |
+------------------------------------------------------------+
DONE
printf "${C_RESET}\n"

exit 0
