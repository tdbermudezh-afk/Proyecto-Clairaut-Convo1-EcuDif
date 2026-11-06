# GUIA DE OPERACION Y REFERENCIA MATEMATICA
## Visualizador Computacional de Ecuaciones Diferenciales de Clairaut
**Curso:** Ecuaciones Diferenciales | **Modalidad:** CIPAS | **Convocatoria 1**

---

## 1. Fundamentacion Teorica de Clairaut

Una ecuacion diferencial de Clairaut es una ecuacion diferencial ordinaria de primer orden no lineal con la forma canonica:

$$y = x y' + f(y')$$

Adoptando la sustitucion usual de parametro diferencial:
$$p = y' = \frac{dy}{dx}$$

la ecuacion se reescribe como:
$$y = x p + f(p)$$

### Solucion General
Derivando respecto a $x$:
$$\frac{dy}{dx} = p + x \frac{dp}{dx} + f'(p) \frac{dp}{dx}$$
$$p = p + [x + f'(p)] \frac{dp}{dx} \implies [x + f'(p)] \frac{dp}{dx} = 0$$

Al considerar el factor $\frac{dp}{dx} = 0$, se obtiene $p = C$ (constante arbitraria). Sustituyendo en la ecuacion original:
$$y = C x + f(C)$$
Esta representa una **familia monoparametrica de lineas rectas** tangentes.

### Solucion Singular (Envolvente)
Al anular el factor diferencial:
$$x + f'(p) = 0$$
Despejando $p = p(x)$ y sustituyendo en $y = x p + f(p)$, se obtiene la **solucion singular**. Geometricamente, esta curva no contiene constantes arbitrarias y actua como la **envolvente** tangente en cada punto a una recta de la familia general.

---

## 2. Sintaxis y Operadores Simbolicos Admitidos

El software integra SymPy como motor de calculo analitico. Para ingresar expresiones en el campo de $f(p)$, debe utilizar la notacion estandar:

| Operacion | Sintaxis en Programa | Ejemplo de Entrada | Resultado Analitico |
| :--- | :--- | :--- | :--- |
| **Suma** | `+` | `p + 4` | $p + 4$ |
| **Resta** | `-` | `p - 3` | $p - 3$ |
| **Multiplicacion** | `*` *(siempre obligatoria)* | `3*p` | $3p$ |
| **Division** | `/` | `1/p` | $\frac{1}{p}$ |
| **Potencia** | `**` | `p**2`, `p**3` | $p^2$, $p^3$ |
| **Raiz Cuadrada** | `sqrt(p)` o `p**(1/2)` | `sqrt(p)` | $\sqrt{p}$ |
| **Exponencial** | `exp(p)` | `exp(p)` | $e^p$ |
| **Logaritmo Natural** | `log(p)` | `log(p)` | $\ln(p)$ |
| **Seno / Coseno** | `sin(p)`, `cos(p)` | `sin(p)` | $\sin(p)$ |

> **Nota:** No escriba `3p` ni `2p**2` sin asterisco. Debe escribirse siempre con operador explocito: `3*p` o `2*p**2`.

---

## 3. Descripcion de la Interfaz y Controles

La interfaz esta concebida bajo un tema negro de alto contraste (#000000 / #09090b) y sin elementos decorativos distractores:

### Panel Lateral Izquierdo
1. **Boton [?] Manual de Sintaxis y Uso**:
   - Despliega una ventana emergente de lectura rapida con todas las reglas de operacion y operadores sin necesidad de salir del aplicativo.
2. **Selector de Ejemplos de la Guia (ComboBox)**:
   - Permite cargar de forma inmediata las 5 ecuaciones requeridas por la guia academica:
     - $p^2$ *(Ejemplo obligatorio de la convocatoria)*
     - $p^3$
     - $1/p$
     - $p^2 + 1$
     - $\sqrt{p}$
     - Adicionales como $-p^2$ y $p^4$.
3. **Campo de Entrada `Expresion analitica libre f(p)`**:
   - Permite al usuario o docente ingresar cualquier expresion arbitraria durante la sustentacion y presionar `Enter` o el boton de calculo.
4. **Boton `Calcular y Graficar`**:
   - Dispara el procesamiento analitico y actualiza en tiempo real tanto la consola de procedimiento como el plano cartesiano.
5. **Casillas de Verificacion (Checkboxes)**:
   - **Familia general**: Oculta o muestra las 7 rectas correspondientes a los valores obligatorios $C \in \{-3, -2, -1, 0, 1, 2, 3\}$.
   - **Solucion singular envolvente**: Oculta o muestra la curva envolvente resaltada en trazo continuo y color carmesi.
   - **Cuadricula y ejes ortogonales**: Permite despejar el fondo para inspeccionar unicamente las trayectorias de curvas.
6. **Consola `Procedimiento Matematico Detallado`**:
   - Muestra paso a paso el cumplimiento estricto de los requisitos 1 al 9 de la guia de la convocatoria con formateo monoespaciado.

### Area Cartesiana Derecha
1. **Lienzo de Analisis Cartesiano**:
   - Fondo negro con alta precision numerica de 1000 puntos discretos.
   - Filtro automatico de asintotas en el origen (evita lineas espurias en funciones como $1/p$).
2. **Barra de Navegacion Integrada (Toolbar Matplotlib)**:
   - **Lupa**: Zoom rectangular sobre cualquier region del plano.
   - **Cruz de flechas**: Desplazamiento (pan) con el cursor.
   - **Disquete (Guardar)**: Permite exportar la grafica actual en alta resolucion (PNG, PDF, SVG) lista para incluir en el informe en PDF del CIPA.
3. **Boton `Restablecer Vista`**:
   - Devuelve la escala de los ejes a sus rangos estandar recomendados ($x \in [-6, 6]$, $y \in [-8, 8]$).

---

## 4. Desarrollo Completo de los Ejemplos de la Guia

### Ejemplo 1 (Obligatorio): $f(p) = p^2$
- **Ecuacion:** $y = x p + p^2$
- **Solucion General:** $y = C x + C^2$
- **Derivada:** $f'(p) = 2p$
- **Condicion Singular:** $x + 2p = 0 \implies p = -\frac{x}{2}$
- **Sustitucion:** $y = x\left(-\frac{x}{2}\right) + \left(-\frac{x}{2}\right)^2 = -\frac{x^2}{2} + \frac{x^2}{4}$
- **Solucion Singular:** $y = -\frac{x^2}{4}$ (Parabola envolvente con vertice en el origen).

### Ejemplo 2: $f(p) = p^3$
- **Ecuacion:** $y = x p + p^3$
- **Solucion General:** $y = C x + C^3$
- **Condicion:** $x + 3p^2 = 0 \implies p = \pm \sqrt{-\frac{x}{3}}$ (Valido para $x \le 0$)
- **Solucion Singular:** $y = \pm \frac{2\sqrt{3}}{9}(-x)^{3/2}$ (Parabola semicubica).

### Ejemplo 3: $f(p) = \frac{1}{p}$
- **Ecuacion:** $y = x p + \frac{1}{p}$
- **Solucion General:** $y = C x + \frac{1}{C}$
- **Condicion:** $x - \frac{1}{p^2} = 0 \implies p = \pm \frac{1}{\sqrt{x}}$ (Valido para $x > 0$)
- **Solucion Singular:** $y = \pm 2\sqrt{x}$ (Ramas parabolicas tangentes a las rectas en el primer y cuarto cuadrante).

### Ejemplo 4: $f(p) = p^2 + 1$
- **Ecuacion:** $y = x p + p^2 + 1$
- **Solucion General:** $y = C x + C^2 + 1$
- **Condicion:** $x + 2p = 0 \implies p = -\frac{x}{2}$
- **Solucion Singular:** $y = 1 - \frac{x^2}{4}$.

### Ejemplo 5: $f(p) = \sqrt{p}$
- **Ecuacion:** $y = x p + \sqrt{p}$
- **Solucion General:** $y = C x + \sqrt{C}$ (con $C \ge 0$)
- **Condicion:** $x + \frac{1}{2\sqrt{p}} = 0 \implies \sqrt{p} = -\frac{1}{2x}$ (Exige $x < 0$)
- **Solucion Singular:** $p = \frac{1}{4x^2} \implies y = x\left(\frac{1}{4x^2}\right) + \left(-\frac{1}{2x}\right) = -\frac{1}{4x}$ (Rama hiperbolica en el segundo cuadrante).

