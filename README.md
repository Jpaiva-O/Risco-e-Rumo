# Risco e Rumo

Site estático da Risco & Rumo, publicado no Vercel.

- `index.html` contém a página principal, incluindo seus estilos e scripts.
- `index-7.html` mantém o endereço da versão publicada anteriormente. Seu conteúdo deve permanecer igual ao de `index.html`.

## Visualizar localmente

Não é necessário instalar dependências ou executar uma compilação. Na raiz do projeto, execute:

```sh
python3 -m http.server 8000
```

Acesse `http://localhost:8000/` no navegador. Depois de editar `index.html`, use `cp index.html index-7.html` para atualizar também a cópia local.

## Publicação

O branch `main` é a origem das publicações automáticas de produção no Vercel. O site é estático e não depende de um servidor local ligado.

Nas configurações do projeto Vercel, o diretório de saída é `.` e o comando de build é:

```sh
test -s index.html && grep -qi '<html' index.html && cp -f index.html index-7.html
```

O comando impede uma publicação sem uma página HTML principal e gera a rota antiga a partir da página principal. Uma falha de build não deve substituir a última publicação de produção bem-sucedida. Se adicionar um `vercel.json` ou alterar a estrutura do site, preserve ou adapte essa verificação, pois o arquivo pode sobrescrever as configurações do projeto.

## Disponibilidade

**O monitor agendado ainda não está ativado.** O modelo em `monitoring/website-availability.yml.example` pode ser instalado por alguém com permissão para criar workflows no GitHub: copie seu conteúdo para `.github/workflows/website-availability.yml` no branch `main`. Depois, confirme na aba Actions que o workflow **Website availability** executou com sucesso.

Quando ativado, ele verificará aproximadamente a cada 15 minutos se a página principal e `/index-7.html` respondem com HTTP 200 e contêm a identificação do site. Os resultados ficarão registrados na aba Actions. Para receber avisos por e-mail, [configure as notificações do GitHub Actions](https://docs.github.com/en/subscriptions-and-notifications/how-tos/managing-github-actions-notifications) na conta responsável pela agenda. Se a identidade do site mudar, atualize a verificação em `scripts/check-uptime.sh`.

Os agendamentos do GitHub são de melhor esforço: podem atrasar ou ser perdidos e, em repositórios públicos sem atividade, podem ser desativados após 60 dias. Essa verificação não evita quedas nem substitui um monitor externo independente para alertas críticos.

Para testar a verificação localmente, execute:

```sh
python3 -m unittest discover -s tests -v
```
