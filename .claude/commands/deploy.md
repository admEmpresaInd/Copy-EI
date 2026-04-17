---
description: Commit, push e deploy Vercel em um so comando
argument-hint: "[mensagem de commit]"
allowed-tools: Bash
---

# /deploy — Pipeline de Deploy Copy EI

Executa o fluxo completo de deploy do projeto **Copy EI**:

1. `git add -u` — staged apenas arquivos ja rastreados
2. `git commit -m "$ARGUMENTS"` — commit com a mensagem informada (ou padrao se vazio)
3. `git push origin master` — envia para o remote
4. `npx vercel --prod` — deploy em producao na Vercel

## Uso

```
/deploy                              # mensagem padrao com timestamp
/deploy feat: atualiza landing page  # mensagem customizada
/deploy fix: corrige link quebrado
```

## Execucao

Rode o script de deploy com a mensagem fornecida (ou vazia para usar o padrao):

!`bash "D:/Copy EI/scripts/deploy.sh" "$ARGUMENTS"`

## Observacoes

- Funciona exclusivamente dentro de `D:\Copy EI` (remote `admEmpresaInd/Copy-EI`, branch `master`).
- O script usa `git add -u` (nao `-A`) para evitar commitar arquivos nao rastreados acidentalmente.
  Se voce adicionou **arquivos novos**, faca `git add <arquivo>` antes de rodar `/deploy`.
- Se nao houver mudancas staged, o script pula o commit/push e apenas dispara o deploy Vercel —
  util para re-deployar o estado atual do remote.
- Todas as etapas mostram status claro com `[OK]` / `[WARN]` / `[FAIL]`.
- Em caso de falha em qualquer etapa, o script aborta imediatamente e mostra o erro.

## Equivalente manual

```bash
cd "D:/Copy EI"
git add -u
git commit -m "sua mensagem"
git push origin master
npx vercel --prod
```
