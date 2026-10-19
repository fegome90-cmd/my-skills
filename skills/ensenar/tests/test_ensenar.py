"""
Pruebas estáticas de la skill ensenar.

Cubren: frontmatter, enlaces locales, coherencia de la escala de estados
entre SKILL.md y el registro YAML, idioma, ausencia de contexto privado,
forma de los evals y entrada en el README.

Ejecutar: python3 -m pytest skills/ensenar/tests -v
      o:  python3 -m unittest discover -s skills/ensenar/tests -v
"""

import json
import re
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parent.parent
SKILL_MD = SKILL_DIR / "SKILL.md"
RECETAS = SKILL_DIR / "references" / "recetas-por-dominio.md"
EVIDENCIA = SKILL_DIR / "references" / "evidencia-y-fuentes.md"
EVALS = SKILL_DIR / "evals" / "evals.json"
ACTIVACION = SKILL_DIR / "evals" / "activacion.json"

ESCALA = {
    "estado_inmediato": ["expuesto", "practicado", "criterio_cumplido"],
    "retencion": ["no_evaluada", "parcial", "lograda"],
    "transferencia": ["no_evaluada", "parcial", "lograda"],
}


def leer(ruta):
    return ruta.read_text(encoding="utf-8")


def frontmatter(texto):
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    assert m, "SKILL.md no abre con frontmatter YAML"
    return m.group(1)


def bloque_yaml(texto):
    m = re.search(r"```yaml\n(.*?)```", texto, re.S)
    assert m, "no hay bloque yaml en recetas-por-dominio.md"
    campos = {}
    for linea in m.group(1).splitlines():
        if not linea.strip():
            continue
        clave, _, resto = linea.partition(":")
        valor, _, comentario = resto.partition("#")
        campos[clave.strip()] = (valor.strip(), comentario.strip())
    return campos


def tabla_escala(texto):
    """Devuelve {dimensión: [estados]} desde la tabla de la sección 5."""
    seccion = texto.split("## 5.", 1)[1].split("\n## ", 1)[0]
    escala, actual = {}, None
    for linea in seccion.splitlines():
        if not linea.startswith("|") or "---" in linea or "Dimensión" in linea:
            continue
        celdas = [c.strip() for c in linea.strip("|").split("|")]
        if celdas[0]:
            actual = celdas[0].strip("`")
            escala[actual] = []
        escala[actual] += re.findall(r"`([a-z_]+)`", celdas[1])
    return escala


class TestFrontmatter(unittest.TestCase):
    def setUp(self):
        self.fm = frontmatter(leer(SKILL_MD))

    def test_nombre_coincide_con_directorio(self):
        self.assertRegex(self.fm, rf"(?m)^name: {SKILL_DIR.name}$")

    def test_campos_requeridos(self):
        for campo in ("description:", "license: MIT", "author:", "version:"):
            self.assertIn(campo, self.fm)

    def test_version_semver(self):
        self.assertRegex(self.fm, r'version: "\d+\.\d+\.\d+"')

    def test_descripcion_incluye_casos_negativos(self):
        self.assertIn("No la actives", self.fm)


class TestEnlaces(unittest.TestCase):
    def test_enlaces_relativos_existen(self):
        for md in [SKILL_MD, RECETAS, EVIDENCIA]:
            for destino in re.findall(r"\]\(([^)#]+)\)", leer(md)):
                if destino.startswith("http"):
                    continue
                self.assertTrue((md.parent / destino).exists(), f"{md.name} -> {destino}")

    def test_skill_enlaza_ambas_referencias(self):
        texto = leer(SKILL_MD)
        self.assertIn("references/recetas-por-dominio.md", texto)
        self.assertIn("references/evidencia-y-fuentes.md", texto)


class TestEscala(unittest.TestCase):
    def test_tabla_de_skill_coincide_con_escala(self):
        self.assertEqual(tabla_escala(leer(SKILL_MD)), ESCALA)

    def test_registro_yaml_usa_la_misma_escala(self):
        campos = bloque_yaml(leer(RECETAS))
        for dimension, estados in ESCALA.items():
            self.assertIn(dimension, campos)
            valor, comentario = campos[dimension]
            self.assertEqual(valor, estados[0], f"{dimension} debe partir en el estado mínimo")
            self.assertEqual([e.strip() for e in comentario.split("/")], estados)

    def test_sin_etiquetas_fuera_de_escala(self):
        for md in [SKILL_MD, RECETAS]:
            texto = leer(md)
            for viejo in ("observed_", "not_assessed", "desempeño_inmediato", "introducido"):
                self.assertNotIn(viejo, texto, f"{md.name} conserva «{viejo}»")
        # «consolidado» solo puede aparecer en la prohibición explícita.
        self.assertEqual(leer(SKILL_MD).count("consolidado"), 1)


class TestTeoriaAntesQueEjemplos(unittest.TestCase):
    def setUp(self):
        texto = leer(SKILL_MD)
        self.seccion3 = texto.split("## 3.", 1)[1].split("\n## ", 1)[0]

    def capas(self):
        return re.findall(r"(?m)^\d\. \*\*([^:*]+):?\*\*", self.seccion3)

    def test_concepto_y_formalizacion_preceden_al_ejemplo(self):
        capas = self.capas()
        concepto = capas.index("Construcción del concepto")
        formalizacion = capas.index("Formalización")
        ejemplo = capas.index("Ejemplo trabajado mínimo")
        self.assertLess(concepto, ejemplo)
        self.assertLess(formalizacion, ejemplo)

    def test_regla_explicita_teoria_antes_que_ejemplos(self):
        self.assertIn("**Teoría antes que ejemplos.**", self.seccion3)
        self.assertIn("nunca termines un turno con solo ejemplos", self.seccion3)

    def test_recetas_empiezan_por_el_concepto(self):
        encabezado = next(l for l in leer(RECETAS).splitlines() if l.startswith("| Dominio"))
        columnas = [c.strip() for c in encabezado.strip("|").split("|")]
        self.assertEqual(columnas[1], "Concepto (primero)")
        self.assertEqual(columnas[2], "Primer ejemplo")

    def test_hay_eval_de_teoria_antes_que_ejemplos(self):
        nombres = [e["name"] for e in json.loads(leer(EVALS))["evals"]]
        self.assertIn("teoria-antes-que-ejemplos", nombres)


class TestIdioma(unittest.TestCase):
    ANGLICISMOS = r"\b(feedback|scores?|shapes|plugins?|readback|quiz|baseline|draft)\b"

    def test_claves_yaml_en_espanol_y_ascii(self):
        claves = bloque_yaml(leer(RECETAS)).keys()
        ingles = {"session", "learning", "goal", "topic", "sources", "learner",
                  "attempts", "misconceptions", "next", "step", "retention", "transfer"}
        for clave in claves:
            self.assertTrue(clave.isascii(), clave)
            self.assertFalse(set(clave.split("_")) & ingles, clave)

    def test_sin_anglicismos_en_prosa(self):
        for md in [SKILL_MD, RECETAS, EVIDENCIA]:
            # Los títulos de artículos citados quedan en su idioma original.
            prosa = re.sub(r"\*[^*]+\*", "", leer(md))
            self.assertIsNone(re.search(self.ANGLICISMOS, prosa, re.I), md.name)

    def test_responde_en_idioma_del_aprendiz(self):
        self.assertIn("Responde en el idioma del aprendiz", leer(SKILL_MD))


class TestSinContextoPrivado(unittest.TestCase):
    def test_no_menciona_documentos_personales(self):
        privados = ["Qwen", "Pegado text", "ChatGPT", "Education Workflow",
                    "pstack", "biblioteca personal", "Kahoot", "Ace Quiz"]
        for ruta in SKILL_DIR.rglob("*.md"):
            texto = leer(ruta)
            for termino in privados:
                self.assertNotIn(termino, texto, f"{ruta.name}: {termino}")


class TestEvals(unittest.TestCase):
    def test_evals_bien_formados(self):
        datos = json.loads(leer(EVALS))
        self.assertEqual(datos["skill_name"], SKILL_DIR.name)
        ids = [e["id"] for e in datos["evals"]]
        self.assertEqual(len(ids), len(set(ids)))
        for e in datos["evals"]:
            for campo in ("id", "name", "prompt", "expected_output", "files"):
                self.assertIn(campo, e)
            for archivo in e["files"]:
                self.assertTrue((SKILL_DIR / archivo).exists(), archivo)

    def test_evals_cubren_los_cuatro_modos(self):
        texto = leer(EVALS)
        for modo in ("tutoría en vivo", "evaluación", "remediación", "material de estudio"):
            self.assertIn(f"Modo {modo}", texto)

    def test_activacion_balanceada_y_sin_duplicados(self):
        casos = json.loads(leer(ACTIVACION))
        positivos = [c for c in casos if c["should_trigger"]]
        negativos = [c for c in casos if not c["should_trigger"]]
        self.assertGreaterEqual(len(positivos), 5)
        self.assertGreaterEqual(len(negativos), 5)
        consultas = [c["query"] for c in casos]
        self.assertEqual(len(consultas), len(set(consultas)))


class TestReadme(unittest.TestCase):
    def test_readme_lista_la_skill_y_el_conteo(self):
        readme = leer(REPO_ROOT / "README.md")
        self.assertIn(f"(skills/{SKILL_DIR.name}/SKILL.md)", readme)
        total = sum(1 for d in (REPO_ROOT / "skills").iterdir() if (d / "SKILL.md").exists())
        self.assertIn(f"reúne {total} paquetes", readme)


if __name__ == "__main__":
    unittest.main()
