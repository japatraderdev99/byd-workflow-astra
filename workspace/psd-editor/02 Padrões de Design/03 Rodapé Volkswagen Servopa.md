---
type: design-standard
brand: Volkswagen Servopa
status: aprovado
---

# Rodapé Volkswagen Servopa

## Padrão aprovado

- Degradê preto único, progressivo e contínuo até a base.
- Linha branca separadora em dois segmentos: ela **não pode atravessar o símbolo VW**.
- Símbolo VW inteiro, com respiro visual à esquerda e à direita.
- Servopa e legal à esquerda dentro da margem segura.
- Selo “Desacelere” inteiro e em margem segura à direita.
- Sem faixa preta sólida, bloco opaco, salto horizontal ou corte de logo.

## Execução confiável

1. Localizar o rodapé-base no PSD de referência e suas camadas originais.
2. Aproveitar a geometria e os ativos existentes.
3. Se o degradê precisar ser reconstruído, usar uma máscara com alfa monotônico: transparência no início da área e escurecimento contínuo até a base.
4. Calcular o ponto de interrupção da linha a partir dos limites reais do logo, depois de qualquer reposicionamento.
5. Desenhar dois segmentos de linha e deixar folga ao redor do símbolo.
6. Inspecionar o rodapé ampliado e na prancha completa antes de exportar o lote.

## Falhas conhecidas e prevenção

| Falha | Causa | Prevenção |
|---|---|---|
| Linha corta o VW | Linha única em toda a largura | Usar dois segmentos com gap calculado pelo logo. |
| Degradê com faixa/gap | Sobreposição de retângulo e máscara ou parada na opacidade | Usar uma única máscara contínua; ocultar a faixa anterior. |
| Selo corta letra | Posição fora da margem | Reposicionar usando bounds do ativo, não percepção em zoom. |
| Rodapé deslocado | Reaproveitamento de posição de outro formato | Validar o rodapé para cada formato. |
