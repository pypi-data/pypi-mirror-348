# CIP — Cifra de Integridade Primal

A CIP (Cifra de Integridade Primal) é um sistema de autenticação vetorial baseado em projeção espectral sobre a estrutura dos números primos.  
Ela não utiliza criptografia clássica, não exige chaves secretas, e oferece integridade absoluta dos dados — mesmo diante de alterações microscópicas (como a inversão de 1 bit).

Este pacote implementa o núcleo funcional da CIP para uso local ou em notebooks Python, com todas as funções internas deliberadamente acessíveis.

> A estrutura espectral da função $\Delta_\pi(x)$ não é uma hipótese: ela é observável, replicável, transformada e gravada nos zeros da função zeta de Riemann.  
> Este código é uma janela prática para essa estrutura. Explore, teste, compare.  
> A música dos primos é real.

---

## Módulo principal

Para começar, basta importar:

`import cip`

As principais funções estão disponíveis diretamente:

- `cip.cifrar`
- `cip.decifrar`
- `cip.assinar`
- `cip.verificar`

---

## Funcionalidades Principais

| Função       | Descrição                                                                 |
|--------------|---------------------------------------------------------------------------|
| `cifrar`     | Cifra os dados projetando cada bloco em base harmônica derivada de $\Delta_\pi(x)$. |
| `decifrar`   | Reconstrói os dados originais a partir dos vetores projetados.            |
| `assinar`    | Gera assinaturas SHA-256 das projeções espectrais de cada bloco.          |
| `verificar`  | Verifica a integridade espectral bloco a bloco a partir das assinaturas.  |

---

## Sobre o Offset

A base vetorial da CIP depende de um parâmetro chamado `offset`, que determina qual trecho do vetor Δπ(x) será usado na projeção.

- Por padrão, o `offset` é aleatório a cada operação, garantindo unicidade e segurança.
- Para aplicações reprodutíveis (como assinaturas públicas), use `fixar_offset=True`.
- Em contextos confidenciais, o `offset` não deve ser incluído no arquivo `.npz`, sendo transmitido separadamente.

---

## Características Técnicas

- Estrutura espectral baseada em $\Delta_\pi(x) = \pi(x) − 2 \cdot \pi(x/2)$, sem uso direto da função zeta.
- Matriz harmônica simétrica construída via cossenos sobre $\Delta_\pi(x)$.
- Projeção vetorial reversível com autovetores de matriz hermitiana.
- Assinatura vetorial com SHA-256 aplicada à projeção (não aos dados crus).
- Funciona com qualquer dado binário: `.txt`, `.pdf`, `.mp3`, `.png`, etc.
- Protocolo sem segredo, sem chave privada, sem fatoração ou curva elíptica.
- Resistente à computação quântica.

---

## Exemplo de uso

Suponha que você tenha um arquivo binário qualquer:

1. Leitura:

`dados = open("documento.pdf", "rb").read()`

2. Cifragem e assinatura:

`pacote = cip.cifrar(dados)`  
`assinaturas, chave = cip.assinar(dados)`

3. Verificação de integridade:

`cip.verificar(dados, assinaturas, offset=chave["offset"])`

---

## Exportação e reimportação (uso avançado)

As funções de empacotamento e carregamento são internas, mas estão disponíveis:

- Para exportar:  
  `cip._internals._empacotar_para_envio(pacote, "documento_cifrado.npz", incluir_offset=False)`

- Para carregar e decifrar:  
  `pacote_npz = cip._internals._carregar_para_decifrar("documento_cifrado.npz")`  
  `cip.decifrar({**pacote_npz, "offset": chave["offset"]})`

> Essas funções são prefixadas com `_` porque são internas, mas estão acessíveis para quem desejar auditá-las ou automatizar o processo.

---

## Uso Avançado: Vetores Alternativos

Por padrão, a CIP utiliza o vetor $\Delta_\pi(x)$ como base harmônica.  
Pesquisadores podem substituir esse vetor por qualquer sequência real para análise comparativa.

Exemplos:

- \Delta_\mathrm{Li}(x) = \mathrm{Li}(x) − 2 \cdot \mathrm{Li}(x/2)
- Ruído gaussiano, exponenciais, sequências artificiais

Basta passar seu vetor como `delta_array=...` ao chamar `cip.cifrar`.

---

## Teste você mesmo — no Google Colab

Quer ver a CIP detectar a corrupção de um único bit com prova vetorial e visual?

Acesse o notebook interativo completo:  
[Abrir no Google Colab](https://colab.research.google.com/github/costaalv/projeto-delta/blob/main/notebooks/demo_cip.ipynb)

Ele mostra:

- Cifragem e assinatura reais
- Verificação de integridade
- Alteração de 1 bit
- Gráfico vetorial da diferença espectral

---

## Licença

MIT — Livre para uso, estudo e modificação com atribuição.

---

## Autor

**Alvaro Costa**  
Auditor Fiscal da Receita Estadual de São Paulo  
Cientista de Dados — Fundador do Projeto DELTA  
São Paulo, Brasil

Projeto DELTA — Dual Eigenvalue Lattice for Transformative Arithmetic  
Repositório oficial: [github.com/costaalv/projeto-delta](https://github.com/costaalv/projeto-delta)

---

**Integridade sem segredo. Confiança sem cripto. Veracidade sem violabilidade.**

