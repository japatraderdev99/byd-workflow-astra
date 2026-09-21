---
type: engineering-standard
status: canonico
---

# Automação segura com PSD

## O que automatizar

Automatizar somente ações repetitivas e estruturalmente conhecidas:

- abrir PSD de trabalho;
- buscar grupos por nome;
- trocar Smart Object identificado;
- atualizar texto em camada conhecida;
- ativar/desativar grupo conhecido;
- ajustar opacidade de camada de contraste existente;
- exportar JPEG;
- registrar resultado por arquivo.

## O que não automatizar sem piloto

- enquadramento de carro entre formatos;
- perspectiva/direção de veículo;
- quebras de texto diferentes;
- posicionamento de rodapé em PSD com estrutura desconhecida;
- qualquer elemento cuja camada não tenha sido validada no piloto.

## Padrão de script

1. Definir entrada e saída explicitamente.
2. Trabalhar sobre cópia ou abrir a origem sem salvar alterações.
3. Localizar camada pelo nome e falhar com mensagem clara se ela não existir.
4. Exportar para nome determinístico.
5. Gravar log `arquivo|OK` ou `arquivo|ERRO|detalhe`.
6. Rodar primeiro em uma peça por formato.
7. Fazer QA da saída antes de rodar todo o lote.

## Regras de preservação

- Nunca sobrescrever o PSD original.
- Nunca converter texto em pixels para acelerar o lote.
- Não usar coordenadas fixas como única regra sem validar bounds da camada.
- Para logo e rodapé, usar bounds reais do ativo depois de qualquer deslocamento.
