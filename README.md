# artifact-replay-lock

## Français

Verrouiller les entrées et dépendances d’un rejeu par empreintes.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m artifact_replay_lock examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Enregistre ou vérifie les octets exacts des entrées de rejeu, refuse les traversées de chemin et liens symboliques, détecte les changements observables pendant la lecture et compare quelques métadonnées de runtime explicitement choisies. La CLI résout root relatif depuis le manifeste JSON.

### Limites

Empreintes locales, pas signature, installation de dépendances, exécution de rejeu ou certification SLSA. Enregistrer sans empreinte attendue n’est pas vérifier ; aucun contenu de fichier n’est affiché.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Lock replay inputs and dependencies with hashes.

Synthetic data; no network access or secret required.

```sh
python -m artifact_replay_lock examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Records or verifies exact replay-input bytes, rejects traversal and symlinks, detects observable changes during reading and compares explicitly selected runtime metadata. CLI resolves relative root from the JSON manifest.

### Limits

Local hashes, not signatures, dependency installation, replay execution or SLSA certification. Recording without an expected hash is not verification; no file content is displayed.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Fijar entradas y dependencias de reproducción con huellas.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m artifact_replay_lock examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Registra o verifica bytes exactos de entradas, rechaza recorrido de rutas y enlaces simbólicos, detecta cambios observables durante lectura y compara metadatos de runtime elegidos. CLI resuelve root relativo desde manifiesto JSON.

### Límites

Huellas locales, no firmas, instalación de dependencias, ejecución de reproducción ni certificación SLSA. Registrar sin huella esperada no verifica; no muestra contenido de archivos.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://slsa.dev/spec/v1.2/provenance
