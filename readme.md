# Break!

## Aplicación Anti-suspensión para Windows

`Break!` es una aplicación de escritorio diseñada para evitar que el equipo con sistema operativo Windows entre en suspensión, se bloquee o se apague debido a la inactividad o políticas de grupo. Su propósito es mantener el equipo activo de forma continua.

---

## Funcionalidades

Las características principales de `Break!` son:

* **Evita Suspensión y Bloqueo**: Mantiene el estado de ejecución del sistema para prevenir la suspensión, el bloqueo de pantalla y la aplicación de políticas de grupo por inactividad.
* **Control de Activación**:
    * **Modo Manual**: Permite iniciar y detener la función de mantenimiento de actividad con un botón directo en la interfaz.
    * **Temporizador**: Configura un temporizador en minutos para controlar la duración de la activación del sistema. Al finalizar el tiempo, la función se detiene automáticamente.
* **Ejecución en Segundo Plano**: Al cerrar la ventana principal, la aplicación se minimiza automáticamente a la bandeja del sistema (área de notificación). Continúa ejecutándose en segundo plano. Para cerrar la aplicación completamente, se debe acceder a su icono en la bandeja del sistema y seleccionar la opción de salida.
* **Icono de Aplicación**: Utiliza un icono personalizado para su identificación en la barra de tareas y la bandeja del sistema.

---

## Uso e Implementación

### 1. Ejecución desde el Código Fuente

Para ejecutar la aplicación directamente desde el código Python:

* **Clonar Repositorio**:
    ```bash
    git clone [https://github.com/PseudoIA/break.git](https://github.com/PseudoIA/break.git)
    cd break
    ```
* **Instalar Dependencias**: Requiere Python 3.x. Instala `PyQt6`:
    ```bash
    pip install PyQt6
    ```
* **Ejecutar Script**:
    ```bash
    python "break demo.py"
    ```

### 2. Generación y Uso de Ejecutable

Para crear un archivo ejecutable (.exe) autónomo para Windows:

* **Instalar PyInstaller**:
    ```bash
    pip install pyinstaller
    ```
* **Compilar Aplicación**: Ejecutar desde el directorio que contiene `break demo.py` e `icon_break.ico`.
    ```bash
    pyinstaller --onefile --windowed --add-data "icon_break.ico;." --icon="icon_break.ico" "break demo.py"
    ```
    El ejecutable se encontrará en el subdirectorio `dist/`.

---

## 🛠️ Requisitos Técnicos

* **Sistema Operativo**: Windows.
* **Lenguaje**: Python 3.x (para ejecución desde código fuente).
* **Librerías Python**: `PyQt6`, `ctypes` (módulo estándar de Python para llamadas a la API de Windows).

---


<p align="center">
  Proyecto por PseudoIA
</p>