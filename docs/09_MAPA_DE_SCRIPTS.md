# 9. Mapa dos scripts e da sequência executada

O inventário completo está em data/script_inventory.csv, com hash e classificação. Marcadores de guarda não substituem revisão. Nenhum script de produção foi executado neste handoff.

| Família | Artefatos centrais | Papel |
|---|---|---|
| Intake | intake_psd_tools.py, mapear_ofertas_estrutural.py, extrair_tipografia_psd.py | estrutura e matriz; ver nomes reais no inventário |
| Pilotos | build_p01 a build_p12, patch_p13 a patch_p18 | tentativas preservadas, não caminho de reuso |
| Escala | build_production_r03/r10 | gera lotes, mas não representa sozinho o final |
| Patches | patch_controle_r14/r16 | correções pontuais de conteúdo/posição |
| Assembly | assemble_r11_v4.py | reúne saídas da escala e correções |
| Estado PSD | recapture_templates_r17/r19/r20.jsx | reparar comps; R19 falhou, R17 parcial + R20 final |
| Fechamento | final_spec_r18.py, consolidate_head_r18.py, promote_production_r18.py, close_delivery_r18.py | liga evidências, templates e PNGs |
| Reuso | render_canonical_v2.jsx | único renderer canônico indicado no fechamento |
| Métricas | production_timings_r18.py, audit_process_metrics_r18.py | tempos e telemetria do case |

O runbook não manda repetir essa sequência: ela inclui falhas, patches e destinos já existentes. Para reuso, copiar o renderer e pedido; para construir outro caso, refatorar explicitamente as regras e validar novos pilotos.
