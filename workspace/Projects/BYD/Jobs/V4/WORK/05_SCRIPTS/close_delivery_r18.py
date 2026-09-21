#!/usr/bin/env python3
"""Close local R18 delivery after promotion; preserve all historical manifests."""
import datetime as dt
import hashlib
import json
from collections import Counter
from pathlib import Path

REFUSE_OVERWRITE = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / '.mkroot').exists())
V4 = ROOT / 'Projects/BYD/Jobs/V4'
QA = V4 / 'WORK/04_QA'

def read(p):
    return json.loads(p.read_text())

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def main():
    target = QA / 'manifest.json'
    if target.exists():
        raise RuntimeError('REFUSE_OVERWRITE_MANIFEST')
    promoted = read(QA / 'production-r18/manifest_r18.json')
    structural = read(QA / 'production-r18/structural7.json')
    if promoted['count'] != 140 or structural['pass'] != 7:
        raise RuntimeError('FINAL_GATES_NOT_CLOSED')
    counts = Counter()
    rows = []
    for row in promoted['files']:
        file = V4 / row['output_file']
        if not file.is_file() or sha(file) != row['sha256']:
            raise RuntimeError('FINAL_HASH_MISMATCH|' + str(file.relative_to(V4)))
        counts[row['format']] += 1
        rows.append({**row, 'staging_file': row['file'], 'file': row['output_file']})
    actual = list((V4 / 'OUTPUT/2026-09-20-r18').rglob('*'))
    actual = [p for p in actual if p.is_file()]
    if len(actual) != 140 or any(p.suffix != '.png' for p in actual) or len(counts) != 7 or set(counts.values()) != {20}:
        raise RuntimeError('OUTPUT_SCOPE_MISMATCH')
    now = dt.datetime.now().astimezone()
    start = dt.datetime.fromisoformat('2026-09-19T12:05:22.103668-03:00')
    wall = (now-start).total_seconds()
    report = V4 / 'WORK/RELATORIO_FINAL.md'
    text = report.read_text()
    text = text.replace('R18_AGUARDA_QA_ESTRUTURAL_E_PROMOCAO_LOCAL', 'R18_CONCLUIDO_LOCAL')
    text = text.replace('Este é o registro operacional vivo. Não declara aprovação humana ou do cliente,\npromoção, entrega externa, nem encerra o job.', 'Produção local encerrada: 140 PNGs promovidos após QA e sete PSDs editáveis validados. Não declara aprovação humana final, aprovação comercial/jurídica ou entrega externa.')
    text = text.replace('| Fim do job | — | `null`: ocorrerá somente após os gates finais e a promoção, se houver. |', f'| Fim da produção local | Manifesto canônico | `{now.isoformat()}`. |')
    text = text.replace('| Duração total | — | `null`: não inferir a partir de intervalos de parede nem somar etapas aninhadas. |', f'| Janela de parede documentada | Início até fechamento | {wall / 3600:.3f} h; inclui espera e interrupções. Tempo ativo total não medido. |')
    text = text.replace('`diagnose_move` prepara a v2 com esse mapeamento corrigido.', 'a v2 corrigiu esse mapeamento e concluiu 7/7 PASS, vinculados aos hashes atuais e às 280 provas nativas.')
    text = text.replace('## Gates restantes\n\n1. Concluir QA estrutural v2 dos sete PSDs e obter 7/7 PASS.\n2. Só então promover para `OUTPUT/2026-09-20-r18/`; a promoção continua local\n   e não equivale a envio externo.', '## Fechamento local\n\nQA estrutural v2: **7/7 PASS**. Promoção concluída em `OUTPUT/2026-09-20-r18/`: **140 PNGs, 20 por formato**, com SHA-256 conferido após cópia. Somente PNGs na pasta de saída. Manifesto canônico: `WORK/04_QA/manifest.json`.\n\nRestam para veiculação as decisões comerciais indicadas acima. Não houve envio externo. Photoshop encerrado sem documentos de produção e lock liberado.')
    report.write_text(text)
    (V4 / 'RELATORIO_FINAL.md').write_text('# Relatório final BYD V4 — R18\n\n**Produção local concluída:** 140 PNGs (20 ofertas × 7 formatos), sete PSDs editáveis, QA técnico 140/140, revisão visual Astra 140/140 e QA estrutural 7/7.\n\n- [Relatório completo, tempos, decisões e pendências](WORK/RELATORIO_FINAL.md)\n- [PNGs finais locais](OUTPUT/2026-09-20-r18/)\n- [Galeria de revisão](WORK/04_QA/production-r18/REVISAO_PRODUCAO_R18.html)\n- [Templates editáveis e fichas](WORK/01_TEMPLATES/2026-09-20-r17/)\n- [Instruções de reuso](WORK/REUSO_TEMPLATES.md)\n- [Manifesto com hashes](WORK/04_QA/manifest.json)\n\nA revisão visual é do Astra, não aprovação humana final. As divergências comerciais dos inputs permanecem registradas para validação antes da veiculação. Nenhum envio externo foi realizado.\n')
    with (V4 / 'WORK/06_LOGS/DIARIO.md').open('a') as f:
        f.write(f'\n\n## {now.isoformat()} — encerramento local R18\n\nR20 concluiu seis PSDs e 240 provas de aplicação em 727056 ms; somados ao strip R17, 280 testes nativos válidos. Reuso R18: três PNGs de 1920x1080 em 77320 ms, 3/3 pixels idênticos. QA estrutural v1 preservado com falsos FAIL de prefixos; v2 corrigiu somente a leitura exata car-/cond- e fechou 7/7 PASS. Promoção local: 140 PNGs, 20 por formato, SHA verificado após cópia, sem PSD ou documento em OUTPUT. Manifesto canônico e relatório final fechados. Ficha micro clarificou alinhamento e legal oculto; snapshot anterior preservado, hashes atuais dos documentos no manifesto canônico. INPUT 48/48 contra baseline observado; nenhuma entrega externa. Janela de parede {wall:.3f}s, incluindo interrupções; custo financeiro e tempo ativo total não medidos.\n')
    docs = [V4 / 'RELATORIO_FINAL.md', report, V4 / 'WORK/REUSO_TEMPLATES.md', V4 / 'WORK/00_MATRIZ/layout_adjustments_r18.json']
    docs += sorted((V4 / 'WORK/01_TEMPLATES/2026-09-20-r17').glob('*.md'))
    result = {**promoted, 'schema': 'byd-v4-canonical-delivery-r18/v1', 'closed_at': now.isoformat(), 'files': rows, 'counts_by_format': dict(counts), 'job_start': start.isoformat(), 'documented_wall_window_seconds': wall, 'active_total_seconds': None, 'financial_cost': None, 'templates_manifest': 'WORK/04_QA/production-r18/templates_manifest_r18.json', 'structural_qa': 'WORK/04_QA/production-r18/structural7.json', 'reuse_qa': 'WORK/04_QA/reuse_validation_r18.json', 'input_integrity': 'WORK/04_QA/input_integrity_final_r18.json', 'visual_review': 'WORK/04_QA/production-r18/head_visual_review.json', 'current_supporting_documents': [{'file': str(p.relative_to(V4)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in docs], 'supporting_document_revision_note': 'Micro ficha clarified LEFT price anchor and hidden legal; earlier snapshot retained in WORK/04_QA/fichas-r18_history. Historical template manifest retained unchanged.'}
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('OK|CLOSED_LOCAL_R18|140_PNG|7_PSD|HASHES_VERIFIED')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('ERRO|CLOSE_R18|' + str(e))
        raise
