# Catálogo de Paletas Completas (100-900 + 150) y Mapeo Dual-Theme

## 1. Paleta Arquetipo Técnico / Clínico / SaaS (Azul Cobalto `Hue 220°` + Neutrales Fríos Tintados)

| Paso | Primary (Cobalt `220°`) | Neutral Tintado (HEX de catálogo; S HSB varía por paso) | Success (Emerald `152°`) | Warning (Amber `38°`) | Danger (Crimson `352°`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`100`** | `#EFF6FF` | `#F8FAFC` | `#ECFDF5` | `#FFFBEB` | `#FFF1F2` |
| **`150`** | `#DBEAFE` | `#F1F5F9` | `#D1FAE5` | `#FEF3C7` | `#FFE4E6` |
| **`200`** | `#BFDBFE` | `#E2E8F0` | `#A7F3D0` | `#FDE68A` | `#FECDD3` |
| **`300`** | `#93C5FD` | `#CBD5E1` | `#6EE7B7` | `#FCD34D` | `#FDA4AF` |
| **`400`** | `#60A5FA` | `#94A3B8` | `#34D399` | `#FBBF24` | `#FB7185` |
| **`500`** | `#3B82F6` | `#64748B` | `#10B981` | `#F59E0B` | `#F43F5E` |
| **`600`** | `#2563EB` | `#475569` | `#059669` | `#D97706` | `#E11D48` |
| **`700`** | `#1D4ED8` | `#334155` | `#047857` | `#B45309` | `#BE123C` |
| **`800`** | `#1E40AF` | `#1E293B` | `#065F46` | `#92400E` | `#9F1239` |
| **`900`** | `#1E3A8A` | `#0F172A` | `#064E3B` | `#78350F` | `#881337` |

## 2. Paleta Arquetipo Editorial / Orgánico / Bienestar (Terracota `Hue 18°` + Neutrales Piedra Cálidos)

| Paso | Primary (Terracotta `18°`) | Neutral Cálido (HEX de catálogo; S HSB varía por paso) | Accent Secundario (Sage `145°`) |
| :--- | :--- | :--- | :--- |
| **`100`** | `#FDF4F0` | `#FAF8F5` | `#F2F7F4` |
| **`150`** | `#FBE8DF` | `#F3EFEA` | `#E4EFE9` |
| **`200`** | `#F5CEBD` | `#E6E0D6` | `#C8DFD2` |
| **`300`** | `#EBA88C` | `#D1C7B8` | `#9FC5B0` |
| **`400`** | `#DF7E57` | `#A89B89` | `#72A68A` |
| **`500`** | `#CE5A2E` | `#786D5F` | `#4D8568` |
| **`600`** | `#B0461F` | `#574E43` | `#3B6B52` |
| **`700`** | `#8E3617` | `#3E372F` | `#2E5440` |
| **`800`** | `#6B2812` | `#27221D` | `#223D2F` |
| **`900`** | `#4A1C0D` | `#161310` | `#16281F` |

## 3. Mapeo Semántico Dual-Theme en CSS (`Light Mode` vs `Dark Mode` por Elevación de Luminancia)

El ejemplo CSS selecciona la paleta fría Cobalt/Slate de la tabla 1. Para probar la cálida, sustituye solo los primitivos `--primary-*` y `--neutral-*` declarados aquí por los HEX correspondientes de la tabla 2; los roles semánticos pueden permanecer iguales.

```css
:root,
[data-theme="light"] {
  /* Primitivos usados en este ejemplo: paleta fría Cobalt/Slate, tabla 1. */
  --primary-300: #93C5FD;
  --primary-400: #60A5FA;
  --primary-600: #2563EB;
  --primary-700: #1D4ED8;
  --neutral-100: #F8FAFC;
  --neutral-150: #F1F5F9;
  --neutral-200: #E2E8F0;
  --neutral-300: #CBD5E1;
  --neutral-400: #94A3B8;
  --neutral-500: #64748B;
  --neutral-600: #475569;
  --neutral-700: #334155;
  --neutral-800: #1E293B;
  --neutral-900: #0F172A;

  /* 60% Superficies Dominantes */
  --surface-canvas: var(--neutral-100);
  --surface-subtle: var(--neutral-150);
  /* 30% Estructura y Elevación */
  --surface-card: #FFFFFF;
  --surface-elevated: #FFFFFF;
  --border-subtle: var(--neutral-200);
  /* Para bordes esenciales de UI: >= 3:1 en las superficies claras de este ejemplo. No se aplica a todo borde decorativo. */
  --border-strong: var(--neutral-500);
  --text-primary: var(--neutral-900);     /* Contraste > 15:1 */
  --text-secondary: var(--neutral-600);   /* Contraste > 5.7:1 */
  --text-muted: var(--neutral-500);       /* Contraste > 4.5:1 */
  /* 10% Acento Interactivo */
  --action-primary: var(--primary-600);
  --action-primary-hover: var(--primary-700);
  --action-primary-fg: #FFFFFF;
}

[data-theme="dark"] {
  /* En Dark Mode, mayor elevación = mayor luminancia de superficie */
  --surface-canvas: var(--neutral-900);   /* Nivel 0: Más oscuro (#0F172A, nunca #000000) */
  --surface-subtle: #162033;              /* Nivel 1: Sección secundaria */
  --surface-card: var(--neutral-800);     /* Nivel 2: Tarjeta elevada (#1E293B) */
  --surface-elevated: var(--neutral-700); /* Nivel 3: Modal / Popover (#334155) */
  --border-subtle: rgba(255, 255, 255, 0.08);
  /* 0.40 mantiene >= 3:1 sobre las cuatro superficies oscuras listadas; para bordes esenciales, no todos los decorativos. */
  --border-strong: rgba(255, 255, 255, 0.40);
  --text-primary: var(--neutral-100);     /* Blanco suavizado (#F8FAFC) sin halación */
  --text-secondary: var(--neutral-300);
  --text-muted: var(--neutral-300);
  /* Acento desaturado (paso 400/500) para evitar vibración óptica */
  --action-primary: var(--primary-400);
  --action-primary-hover: var(--primary-300);
  --action-primary-fg: var(--neutral-900);
}
```
