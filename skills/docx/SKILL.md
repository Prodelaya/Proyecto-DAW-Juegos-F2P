---
name: docx
description: >
  Crear, leer, editar y validar documentos Word (.docx), especialmente la memoria
  del Proyecto Final DAW siguiendo docs/00.5-Guia-Memoria-Proyecto.md.
  Trigger: cuando el usuario pida trabajar con Word, .docx, memoria del proyecto,
  informe, documentación formal, índice automático, portada, tablas, capturas,
  evidencias o entrega PDF derivada de un .docx.
license: Proprietary
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Crear o editar documentos Word `.docx`.
- Generar la memoria del Proyecto Final DAW en formato profesional.
- Adaptar contenido técnico del repositorio a una memoria académica.
- Insertar o reorganizar portada, índice, resumen, capítulos, tablas, capturas o anexos.
- Convertir un `.docx` a PDF para entrega final.
- Revisar formato, estructura o evidencias exigidas por `docs/00.5-Guia-Memoria-Proyecto.md`.

No usar para PDFs como fuente principal, hojas de cálculo, Google Docs ni tareas de código no relacionadas con documentos Word.

## Critical Patterns

### Formato obligatorio de la memoria DAW

Todo `.docx` de memoria del proyecto debe respetar:

| Regla | Valor |
|---|---|
| Extensión objetivo | 40–60 páginas, sin contar anexos |
| Fuente | Arial |
| Tamaño base | 11 pt |
| Interlineado | 1,25 |
| Márgenes | 2,5 cm |
| Alineación | Texto justificado |
| Entrega | PDF + enlaces a 2 vídeos, uno por alumno |
| Estructura | Homogénea en todos los capítulos |

### Estructura obligatoria recomendada

Usar esta secuencia salvo instrucción explícita del usuario:

1. Portada
2. Índice
3. Resumen ejecutivo
4. Introducción
5. Justificación, marco teórico, objetivos y alcance
6. Análisis y planificación del proyecto
7. Diseño del sistema
8. Desarrollo e implementación
9. Pruebas y validación
10. Despliegue y puesta en producción
11. Seguridad y protección de datos
12. Manual de usuario
13. Manual técnico
14. Conclusiones y líneas futuras
15. Bibliografía/Webgrafía
16. Anexos, opcional

### Distribución orientativa

| Apartado | Páginas aprox. | Evidencias mínimas |
|---|---:|---|
| Portada + índice + resumen | 2–4 | Portada, índice automático, resumen de 1 página |
| Introducción | 2–3 | Contexto, problema y alcance |
| Objetivos y alcance | 2–4 | Objetivo general, específicos, alcance/no alcance |
| Análisis y planificación | 8–12 | Requisitos, historias, casos de uso, Gantt, riesgos |
| Diseño | 8–12 | Arquitectura, ER, modelo de datos, UI/UX, API si aplica |
| Desarrollo | 10–15 | Estructura repo, decisiones, módulos, fragmentos de código |
| Pruebas | 4–6 | Plan, tabla de casos y evidencias |
| Despliegue, seguridad, manuales y conclusiones | 6–10 | Guía despliegue, RGPD básico, manuales, mejoras |

### Reglas de redacción

- Escribir la memoria en español formal y claro.
- No vender humo: cada afirmación técnica debe estar respaldada por código, docs, capturas o evidencias.
- Si el proyecto no tiene API pública, no inventarla: explicar la arquitectura real.
- Distinguir alcance de fuera de alcance para no prometer funcionalidades inexistentes.
- Incluir tablas para requisitos, historias de usuario, riesgos, casos de prueba y diccionario de datos.
- Los fragmentos de código deben ser seleccionados: 6–10 ejemplos, máximo 20–30 líneas cada uno, siempre explicados.
- Las pruebas necesitan evidencia concreta: pasos, resultado esperado, resultado real y capturas/logs si existen.

### Reglas técnicas docx-js

- Configurar página A4 explícitamente para documentos DAW.
- Usar Arial 11 pt como estilo base.
- Definir márgenes de 2,5 cm: aproximadamente `1417` DXA.
- Aproximar interlineado 1,25 con `spacing: { line: 300 }`.
- Justificar párrafos de contenido con `AlignmentType.JUSTIFIED`.
- Usar `HeadingLevel` para títulos incluidos en el índice automático.
- No usar bullets Unicode manuales; usar `LevelFormat.BULLET`.
- No usar `\n`; crear párrafos separados.
- Las tablas deben usar ancho DXA, `columnWidths` y ancho por celda.
- `PageBreak` debe ir dentro de un `Paragraph`.
- `ImageRun` requiere `type` y `altText` completo.

## Code Examples

### Documento base DAW con A4, Arial 11, márgenes 2,5 cm e índice

```javascript
const fs = require("fs");
const {
  AlignmentType,
  Document,
  HeadingLevel,
  Packer,
  Paragraph,
  TableOfContents,
  TextRun,
} = require("docx");

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22 }, // 11 pt
        paragraph: { spacing: { line: 300 }, alignment: AlignmentType.JUSTIFIED },
      },
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { font: "Arial", size: 32, bold: true },
        paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 0 },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { font: "Arial", size: 26, bold: true },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 },
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4 en DXA
          margin: { top: 1417, right: 1417, bottom: 1417, left: 1417 },
        },
      },
      children: [
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          alignment: AlignmentType.CENTER,
          children: [new TextRun("Memoria del Proyecto Final")],
        }),
        new TableOfContents("Índice", { hyperlink: true, headingStyleRange: "1-3" }),
        new Paragraph({ heading: HeadingLevel.HEADING_1, text: "Resumen ejecutivo" }),
        new Paragraph({ text: "Este proyecto desarrolla..." }),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => fs.writeFileSync("memoria.docx", buffer));
```

### Tabla de requisitos

```javascript
const { BorderStyle, ShadingType, Table, TableCell, TableRow, WidthType } = require("docx");

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9072, type: WidthType.DXA },
  columnWidths: [1200, 5000, 2872],
  rows: [
    new TableRow({
      children: ["ID", "Requisito", "Criterio de aceptación"].map(
        (text, index) => new TableCell({
          borders,
          width: { size: [1200, 5000, 2872][index], type: WidthType.DXA },
          shading: { fill: "D9EAF7", type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ text })],
        })
      ),
    }),
  ],
});
```

## Commands

```bash
# Instalar generador DOCX
npm install -g docx

# Extraer texto de un DOCX
pandoc --track-changes=all documento.docx -o salida.md

# Desempaquetar para edición XML
python scripts/office/unpack.py documento.docx unpacked/

# Reempaquetar y validar
python scripts/office/pack.py unpacked/ salida.docx --original documento.docx

# Validar DOCX generado
python scripts/office/validate.py salida.docx

# Convertir a PDF para entrega
python scripts/office/soffice.py --headless --convert-to pdf salida.docx
```

## Resources

- **Guía de memoria DAW**: `docs/00.5-Guia-Memoria-Proyecto.md`
- **Documentos existentes**: `Memoria-Proyecto-Final.docx`, `Memoria-Proyecto-Final_CORREGIDA_FINAL.docx`, `Memoria-Proyecto-Final_CORREGIDA_ROJO.docx`
- **Scripts Office**: `scripts/office/`
