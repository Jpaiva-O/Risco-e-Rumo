# Risco e Rumo

Site estático da Risco & Rumo, publicado no Vercel.

- `index.html` contém a página principal, incluindo seus estilos e scripts.
- `index-7.html` mantém o endereço da versão publicada anteriormente. Seu conteúdo deve permanecer igual ao de `index.html`.

## Visualizar localmente

Não é necessário instalar dependências ou executar uma compilação. Na raiz do projeto, execute:

```sh
python3 -m http.server 8000
```

Acesse `http://localhost:8000/` no navegador.

## Publicação

No Vercel, use o projeto na raiz do repositório como um site estático, sem comando de build ou diretório de saída personalizado. O branch `main` é a origem das publicações em produção. Depois de editar a página, atualize também `index-7.html` antes de publicar.
