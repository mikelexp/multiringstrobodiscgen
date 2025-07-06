# MultiRing Strobo Disc Generator

**[🇪🇸 Versión en Español](#multiring-strobo-disc-generator-1)**

A handy tool for creating custom stroboscopic discs to check if your turntables are spinning at the right speed. Perfect for vinyl nerds who want to make sure their 33⅓ RPM records are actually spinning at 33⅓ RPM.

**[📦 Download latest release](https://github.com/mikelexp/multiringstrobodiscgen/releases/latest)**

## Features

- **Multiple calibration rings** for different RPM speeds (16, 33⅓, 45, 78 RPM + custom 1-100 RPM)
- **Universal compatibility** with 50Hz and 60Hz power frequencies
- **Flexible visual patterns** - lines or dots with normal/double density
- **Presets system** - save, load, and manage your favorite configurations
- **Professional export** - SVG and PDF formats with standard page sizes
- **Custom labeling** - add text above and below the spindle
- **Live preview** with real-time updates
- **Bilingual interface** (English/Spanish) with automatic detection
- **Mathematical precision** - automatic calculations for optimal segments and spacing

## Interface

Clean tabbed layout with **Rings** setup, **Options** configuration, **Export** tools, and **Presets** management.

## Requirements

### System Requirements
- **Python**: 3.10, 3.11, or 3.12 (3.12 recommended for best Nuitka compatibility)
- **Operating System**: Linux, Windows

### Build Dependencies

#### openSUSE (Tumbleweed/Leap)
```bash
# Install Python 3.12 and development tools
sudo zypper install python312 python312-devel python312-pip
sudo zypper install gcc gcc-c++ make cmake git

# For PySide6 compilation
sudo zypper install libQt6Core6 libQt6Gui6 libQt6Widgets6
sudo zypper install qt6-base-devel

# Optional: ccache for faster repeated builds
sudo zypper install ccache
```

#### Ubuntu/Debian
```bash
# Install Python 3.12 and development tools
sudo apt update
sudo apt install python3.12 python3.12-dev python3.12-venv python3-pip
sudo apt install build-essential cmake git

# For PySide6 compilation
sudo apt install qt6-base-dev libgl1-mesa-dev

# Optional: ccache for faster repeated builds
sudo apt install ccache
```

#### Fedora/RHEL/CentOS
```bash
# Install Python 3.12 and development tools
sudo dnf install python3.12 python3.12-devel python3-pip
sudo dnf install gcc gcc-c++ make cmake git

# For PySide6 compilation
sudo dnf install qt6-qtbase-devel mesa-libGL-devel

# Optional: ccache for faster repeated builds
sudo dnf install ccache
```

#### Arch Linux
```bash
# Install Python 3.12 and development tools
sudo pacman -S python python-pip base-devel cmake git

# For PySide6 compilation
sudo pacman -S qt6-base

# Optional: ccache for faster repeated builds
sudo pacman -S ccache
```


#### Windows
1. **Install Python 3.12** from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
2. **Install Visual Studio Build Tools** from [Microsoft](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
   - Select "C++ build tools" workload
3. **Install Git** from [git-scm.com](https://git-scm.com/download/win)

## Installation

### Pre-built Packages

**[📦 Download from GitHub Releases](https://github.com/mikelexp/multiringstrobodiscgen/releases)**

Available formats:
- **Linux**: Standalone binary
- **Windows**: Standalone executable (.exe) and Windows installer

*Note: Linux packages (RPM/DEB) are planned for future releases.*


## Building from Source

**Note**: Generated executable files include the version and platform architecture in their filename (e.g., `multiringstrobodiscgen-v1.0.0-x86_64.bin` for Linux, `multiringstrobodiscgen-v1.0.0-x86_64.exe` for Windows).

### 1. Clone the Repository
```bash
git clone <repository-url>
cd multiringstrobodiscgen
```

### 2. Create Virtual Environment
```bash
# Linux
python3.12 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run Development Version
```bash
# Linux
./run.sh

# Windows
python start.py
```

### 5. Build Standalone Executable

#### Linux
```bash
chmod +x build-linux.sh
./build-linux.sh
```

The executable will be created in `dist/multiringstrobodiscgen-vX.X.X.bin`

**Note about Linux Dependencies**: The build script automatically detects and includes the `libgthread-2.0` library (required by PySide6) if available on the build system. This ensures the executable works on systems where this library might not be available. The script is cross-distribution compatible and will work on openSUSE, Ubuntu, Fedora, Arch Linux, and other distributions.


#### Windows
```powershell
# Make sure you can run PowerShell scripts (run as Administrator if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run the build script
.\build-windows.ps1
```

The executable will be created in `dist/multiringstrobodiscgen-vX.X.X.exe`

### Building Linux Packages

*Note: Linux package building (RPM/DEB) is planned for future releases and currently untested.*

## Usage

1. **Start the app**
2. **Choose language** in the "Options" tab (auto-detected by default)
3. **Add rings** in the "Rings" tab:
   - Pick your RPM (33⅓, 45, 78, whatever you need)
   - Choose your local frequency (50Hz or 60Hz)
   - Tweak ring depth and spacing
   - Lines or dots? Your call
   - Normal or double density
   - Make dots bigger if you want
4. **Set disc options** in the "Options" tab:
   - How big you want your disc
   - Spindle hole size
   - Ring spacing
   - Add custom text above and below the spindle
5. **Save it** in the "Export" tab:
   - SVG for printing or PDF for sharing
   - Pick your paper size

### Language Support

The interface automatically detects your system language and switches between English and Spanish. You can manually change the language in the "Options" tab - settings are saved automatically.

## Dependencies

- **PySide6**: Modern Qt6 bindings for Python
- **Nuitka**: Python-to-binary compiler
- **svgwrite**: SVG creation library
- **svglib**: SVG to other formats conversion
- **reportlab**: PDF generation

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

**You are free to:**
- Share: copy and redistribute the material in any medium or format
- Adapt: remix, transform, and build upon the material

**Under the following terms:**
- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **NonCommercial**: You may not use the material for commercial purposes
- **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original

For more details, see the [CC BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

# MultiRing Strobo Disc Generator

Una herramienta práctica para crear discos estroboscópicos y verificar que tus tocadiscos giren a la velocidad correcta. Perfecta para nerds del vinilo que quieren asegurarse de que sus discos de 33⅓ RPM realmente giren a 33⅓ RPM.

**[📦 Descargar última versión](https://github.com/user/MultiRingStroboDiscGen/releases/latest)**

## Características

- **Múltiples anillos de calibración** para diferentes velocidades (16, 33⅓, 45, 78 RPM + personalizado 1-100 RPM)
- **Compatibilidad universal** con frecuencias de 50Hz y 60Hz
- **Patrones visuales flexibles** - líneas o puntos con densidad normal/doble
- **Sistema de presets** - guarda, carga y administra tus configuraciones favoritas
- **Exportación profesional** - formatos SVG y PDF con tamaños de página estándar
- **Etiquetado personalizado** - agrega texto arriba y abajo del eje
- **Vista previa en tiempo real** con actualizaciones automáticas
- **Interfaz bilingüe** (inglés/español) con detección automática
- **Precisión matemática** - cálculos automáticos para segmentos y espaciado óptimos

## Interfaz

Diseño limpio con pestañas para configuración de **Anillos**, **Opciones**, herramientas de **Export** y gestión de **Presets**.

## Requisitos

### Requisitos del Sistema
- **Python**: 3.10, 3.11, o 3.12 (3.12 recomendado para mejor compatibilidad con Nuitka)
- **Sistema Operativo**: Linux, Windows

### Dependencias de Compilación

#### openSUSE (Tumbleweed/Leap)
```bash
# Instalar Python 3.12 y herramientas de desarrollo
sudo zypper install python312 python312-devel python312-pip
sudo zypper install gcc gcc-c++ make cmake git

# Para compilación de PySide6
sudo zypper install libQt6Core6 libQt6Gui6 libQt6Widgets6
sudo zypper install qt6-base-devel

# Opcional: ccache para compilaciones repetidas más rápidas
sudo zypper install ccache
```

#### Ubuntu/Debian
```bash
# Instalar Python 3.12 y herramientas de desarrollo
sudo apt update
sudo apt install python3.12 python3.12-dev python3.12-venv python3-pip
sudo apt install build-essential cmake git

# Para compilación de PySide6
sudo apt install qt6-base-dev libgl1-mesa-dev

# Opcional: ccache para compilaciones repetidas más rápidas
sudo apt install ccache
```

#### Fedora/RHEL/CentOS
```bash
# Instalar Python 3.12 y herramientas de desarrollo
sudo dnf install python3.12 python3.12-devel python3-pip
sudo dnf install gcc gcc-c++ make cmake git

# Para compilación de PySide6
sudo dnf install qt6-qtbase-devel mesa-libGL-devel

# Opcional: ccache para compilaciones repetidas más rápidas
sudo dnf install ccache
```

#### Arch Linux
```bash
# Instalar Python 3.12 y herramientas de desarrollo
sudo pacman -S python python-pip base-devel cmake git

# Para compilación de PySide6
sudo pacman -S qt6-base

# Opcional: ccache para compilaciones repetidas más rápidas
sudo pacman -S ccache
```


#### Windows
1. **Instalar Python 3.12** desde [python.org](https://www.python.org/downloads/)
   - Asegúrate de marcar "Add Python to PATH" durante la instalación
2. **Instalar Visual Studio Build Tools** desde [Microsoft](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
   - Selecciona la carga de trabajo "C++ build tools"
3. **Instalar Git** desde [git-scm.com](https://git-scm.com/download/win)

## Compilación desde el Código Fuente

### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd multiringstrobodiscgen
```

### 2. Crear Entorno Virtual
```bash
# Linux
python3.12 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Ejecutar Versión de Desarrollo
```bash
# Linux
./run.sh

# Windows
python start.py
```

### 5. Compilar Ejecutable Independiente

#### Linux
```bash
chmod +x build-linux.sh
./build-linux.sh
```

El ejecutable se creará en `dist/multiringstrobodiscgen-vX.X.X.bin`

**Nota sobre Dependencias en Linux**: El script de compilación detecta automáticamente e incluye la librería `libgthread-2.0` (requerida por PySide6) si está disponible en el sistema de compilación. Esto asegura que el ejecutable funcione en sistemas donde esta librería podría no estar disponible. El script es compatible con diferentes distribuciones y funcionará en openSUSE, Ubuntu, Fedora, Arch Linux, y otras distribuciones.


#### Windows
```powershell
# Asegúrate de poder ejecutar scripts de PowerShell (ejecutar como Administrador si es necesario)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ejecutar el script de compilación
.\build-windows.ps1
```

El ejecutable se creará en `dist/multiringstrobodiscgen-vX.X.X.exe`

## Uso

1. **Abre la app**
2. **Elige idioma** en la pestaña "Opciones" (se detecta automáticamente por defecto)
3. **Agrega anillos** en la pestaña "Rings":
   - Elige tu RPM (33⅓, 45, 78, lo que necesites)
   - Selecciona tu frecuencia local (50Hz o 60Hz)
   - Ajusta profundidad y espaciado
   - ¿Líneas o puntos? Tú decides
   - Densidad normal o doble
   - Haz los puntos más grandes si quieres
4. **Configura las opciones** en la pestaña "Opciones":
   - Qué tan grande quieres el disco
   - Tamaño del agujero del eje
   - Espaciado entre anillos
   - Agrega texto personalizado arriba y abajo del eje
5. **Guárdalo** en la pestaña "Export":
   - SVG para imprimir o PDF para compartir
   - Elige el tamaño de papel

## Dependencias

- **PySide6**: Enlaces modernos de Qt6 para Python
- **Nuitka**: Compilador de Python a binario
- **svgwrite**: Biblioteca de creación de SVG
- **svglib**: Conversión de SVG a otros formatos
- **reportlab**: Generación de PDF

## Licencia

Este proyecto está licenciado bajo la **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

**Eres libre de:**
- Compartir: copiar y redistribuir el material en cualquier medio o formato
- Adaptar: remezclar, transformar y construir sobre el material

**Bajo los siguientes términos:**
- **Atribución**: Debes dar el crédito apropiado, proporcionar un enlace a la licencia e indicar si se hicieron cambios
- **NoComercial**: No puedes usar el material para propósitos comerciales
- **CompartirIgual**: Si remezclas, transformas o construyes sobre el material, debes distribuir tus contribuciones bajo la misma licencia que el original

Para más detalles, consulta la [Licencia CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Contribuciones

¡Las contribuciones son bienvenidas! No dudes en enviar pull requests o abrir issues para bugs y solicitudes de características.