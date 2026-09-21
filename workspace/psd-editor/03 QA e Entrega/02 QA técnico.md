---
type: checklist
status: canonico
---

# QA técnico

## Conferir para cada JPG

- formato JPEG;
- modo RGB;
- dimensões exatas;
- limite de peso, quando houver;
- checksum SHA-256;
- arquivo abre corretamente.

```bash
sips -g pixelWidth -g pixelHeight -g format arquivo.jpg
shasum -a 256 arquivo.jpg
```

## Manifesto mínimo

```json
{
  "file": "marca_modelo_formato_1920x913_v1.jpg",
  "dimensions": [1920, 913],
  "mode": "RGB",
  "bytes": 000000,
  "sha256": "..."
}
```

## Regras

- Checksum confirma integridade, não aprova design.
- Nunca redimensionar sem proporção para atingir um formato.
- Se houver limite de 500 KB, reduzir qualidade de JPEG progressivamente e reinspecionar artefatos antes de aceitar.
