# Plantilla DTCG Format Module 2025.10 (tres capas locales) y plantilla de Component Reference Document (CRD)

El DTCG Format Module 2025.10 es un módulo de formato del Design Tokens Community Group, no un estándar W3C ni parte de su standards track. Este ejemplo usa esa versión como objetivo; no afirma validación contra schema. `Brand -> Alias -> Mapped` es una convención arquitectónica local. `$extensions.mode` también es una convención de este proyecto, no un mecanismo de modos universal de DTCG.

## 1. Ejemplo de `design-system/tokens/design-tokens.json` (DTCG Format Module 2025.10)

Ruta canónica relativa a la raíz del proyecto (`PROJECT-ROOT`): `PROJECT-ROOT/design-system/tokens/design-tokens.json`.

```json
{
  "brand": {
    "$description": "Colección privada según la convención local Brand -> Alias -> Mapped. Valores sin contexto semántico.",
    "color": {
      "cobalt-400": { "$value": { "colorSpace": "srgb", "components": [0.3764705882352941, 0.6470588235294118, 0.9803921568627451], "alpha": 1 }, "$type": "color" },
      "cobalt-600": { "$value": { "colorSpace": "srgb", "components": [0.14509803921568627, 0.38823529411764707, 0.9215686274509803], "alpha": 1 }, "$type": "color" },
      "cobalt-700": { "$value": { "colorSpace": "srgb", "components": [0.11372549019607843, 0.30588235294117646, 0.8470588235294118], "alpha": 1 }, "$type": "color" },
      "slate-100":  { "$value": { "colorSpace": "srgb", "components": [0.9725490196078431, 0.9803921568627451, 0.9882352941176471], "alpha": 1 }, "$type": "color" },
      "slate-150":  { "$value": { "colorSpace": "srgb", "components": [0.9450980392156862, 0.9607843137254902, 0.9764705882352941], "alpha": 1 }, "$type": "color" },
      "slate-200":  { "$value": { "colorSpace": "srgb", "components": [0.8862745098039216, 0.9098039215686274, 0.9411764705882353], "alpha": 1 }, "$type": "color" },
      "slate-800":  { "$value": { "colorSpace": "srgb", "components": [0.11764705882352941, 0.1607843137254902, 0.23137254901960785], "alpha": 1 }, "$type": "color" },
      "slate-850":  { "$value": { "colorSpace": "srgb", "components": [0.14901960784313725, 0.20392156862745098, 0.28627450980392155], "alpha": 1 }, "$type": "color" },
      "slate-900":  { "$value": { "colorSpace": "srgb", "components": [0.058823529411764705, 0.09019607843137255, 0.16470588235294117], "alpha": 1 }, "$type": "color" },
      "white":      { "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "alpha": 1 }, "$type": "color" }
    },
    "radius": {
      "sm": { "$value": { "value": 8, "unit": "px" }, "$type": "dimension" },
      "md": { "$value": { "value": 12, "unit": "px" }, "$type": "dimension" },
      "lg": { "$value": { "value": 16, "unit": "px" }, "$type": "dimension" },
      "xl": { "$value": { "value": 24, "unit": "px" }, "$type": "dimension" }
    }
  },
  "alias": {
    "$description": "Colección puente de la arquitectura local. Conecta identidad con roles transversales.",
    "primary": {
      "base": { "$value": "{brand.color.cobalt-600}", "$type": "color" },
      "hover": { "$value": "{brand.color.cobalt-700}", "$type": "color" },
      "dark-mode": { "$value": "{brand.color.cobalt-400}", "$type": "color" }
    }
  },
  "mapped": {
    "$description": "Colección pública en esta convención local; los modos se expresan mediante una extensión propia del proyecto.",
    "surface": {
      "canvas": {
        "$value": "{brand.color.slate-100}",
        "$type": "color",
        "$extensions": { "mode": { "light": "{brand.color.slate-100}", "dark": "{brand.color.slate-900}" } },
        "$description": "Fondo base de toda la pantalla; nunca usar en tarjetas elevadas ni botones."
      },
      "card": {
        "$value": "{brand.color.white}",
        "$type": "color",
        "$extensions": { "mode": { "light": "{brand.color.white}", "dark": "{brand.color.slate-800}" } },
        "$description": "Superficie de tarjetas y paneles de primer nivel sobre el canvas; no usar para el fondo de página."
      },
      "card-hover": {
        "$value": "{brand.color.slate-150}",
        "$type": "color",
        "$extensions": { "mode": { "light": "{brand.color.slate-150}", "dark": "{brand.color.slate-850}" } },
        "$description": "Superficie de tarjeta interactiva en estado hover o contenedor secundario sutil (paso 150)."
      }
    },
    "action": {
      "primary-bg": {
        "$value": "{alias.primary.base}",
        "$type": "color",
        "$extensions": { "mode": { "light": "{alias.primary.base}", "dark": "{alias.primary.dark-mode}" } },
        "$description": "Fondo exclusivo del CTA primario de la vista (presupuesto max 10%); no usar en botones secundarios."
      }
    }
  }
}
```

Los valores de tipo `color` usan objetos sRGB con componentes normalizados entre 0 y 1; los de tipo `dimension` usan `{ "value": número, "unit": "px" }`. Las referencias de alias permanecen como strings de referencia. Los valores dentro de `$extensions.mode` siguen la convención local y no se presentan como valores de token definidos por DTCG.

## 2. Tabla de radios (relaciones de referencia para inset uniforme)

Usa la relación $R_{\text{ext}} = R_{\text{int}} + p$ solo cuando el inset uniforme y la intención de geometría concéntrica correspondan. Son ejemplos; no una norma universal para radios anidados.

| Contexto de Anidamiento | Radio Interno ($R_{\text{int}}$) | Inset uniforme del Contenedor ($p$) | Radio Externo ($R_{\text{ext}}$) |
| :--- | :--- | :--- | :--- |
| **Segmented Control / Tabs** (Botón dentro de pista) | `6px` | `4px` | **`10px`** |
| **Card Compacta** con botón o miniatura interna | `8px` (`--radius-sm`) | `12px` | **`20px`** |
| **Card Estándar** con imagen o bloque interno | `8px` (`--radius-sm`) | `16px` (`--space-micro`) | **`24px`** (`--radius-xl`) |
| **Modal / Bento Card Amplia** con panel interno | `12px` (`--radius-md`) | `24px` (`--space-card-padding`) | **`36px`** |

## 3. Plantilla de Component Reference Document (`CRD-<ComponentName>.md`)

```markdown
# CRD: <ComponentName>

## 1. Intención Semántica (1 Línea)
<Para qué sirve este componente y cuándo NO debe usarse en favor de otro.>

## 2. Anatomía y Geometría
- **Contenedor Raíz**: `display: flex`, `padding: var(--space-micro)` (`16px` Desktop y Mobile), `border-radius: var(--radius-xl)` (`24px`).
- **Slot / Hijo Interno**: `border-radius: var(--radius-sm)` (`8px`) -> Para este inset uniforme, $24 = 8 + 16$.

## 3. Contrato de Propiedades (5 Propiedades)
| Propiedad | Tipo | Valores / Defecto | Descripción |
| :--- | :--- | :--- | :--- |
| `intent` | `Variant` | `primary \| secondary \| ghost \| danger` (`primary`) | Jerarquía visual del componente |
| `size` | `Variant` | `sm (32px) \| md (40px) \| lg (48px)` (`md`) | Altura elegida según la rejilla y requisitos aplicables |
| `label` | `Text` | `string` | Etiqueta visible con Vertical Trim |
| `hasLeadingIcon` | `Boolean` | `false` | Muestra/oculta el slot de icono izquierdo |
| `leadingIcon` | `Instance Swap` | `<Icon />` | Icono SVG de `16px`/`20px` |
| `contentSlot` | `Slot` | `ReactNode / Frame` | Área flexible para composición libre sin crear nuevas variantes |

## 4. Mapeo de Tokens (`Mapped`) por Estado
| Estado | Background | Text / Icon | Border / Ring |
| :--- | :--- | :--- | :--- |
| `default` | `action/primary-bg` | `action/primary-fg` | `transparent` |
| `hover` | `action/primary-hover` | `action/primary-fg` | `transparent` |
| `focus-visible` | `action/primary-bg` | `action/primary-fg` | `2px solid focus/ring` (`offset: 2px`) |
| `disabled` | `surface/disabled` | `text/disabled` | `border/subtle` (`opacity: 0.5`) |
```
