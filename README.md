# world-carver
Application for DM's and Worldbuilders to carve their perfect world

# Uruchomienie projektu lokalnie

Projekt składa się z dwóch głównych części:

* **backend** — Django, PostgreSQL, Redis, Celery i Flower uruchamiane przez Docker Compose,
* **frontend** — dwie niezależne aplikacje React + Vite (`web` i `admin`) zarządzane przez `pnpm` i Turborepo, uruchamiane lokalnie poza Dockerem.

## Wymagania

Przed uruchomieniem projektu należy mieć zainstalowane:

* Docker + Docker Compose,
* Node.js,
* pnpm,
* Git.

Wersja `pnpm` powinna odpowiadać wartości zdefiniowanej w głównym `package.json`:

```json
"packageManager": "pnpm@X.Y.Z"
```

Wersję można sprawdzić poleceniem:

```bash
pnpm --version
```

## 1. Konfiguracja zmiennych środowiskowych

Backend korzysta z plików znajdujących się w:

```text
.envs/
└── local/
    ├── api/
    │   └── .env
    └── db/
        └── .env
```

### Baza danych

Plik:

```text
.envs/local/db/.env
```

powinien zawierać między innymi:

```env
POSTGRES_DB=world_carver
POSTGRES_USER=postgres
POSTGRES_PASSWORD=...
```

### Django API

Plik:

```text
.envs/local/api/.env
```

powinien zawierać konfigurację połączenia z bazą:

```env
DATABASE_NAME=world_carver
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=...
DATABASE_HOST=carver-db
DATABASE_PORT=5432
```

W środowisku Docker jako host bazy należy używać nazwy serwisu:

```text
carver-db
```

a nie `localhost`.

Analogicznie Redis jest dostępny dla pozostałych kontenerów pod nazwą:

```text
redis
```

## 2. Instalacja zależności frontendu

Z poziomu głównego katalogu projektu:

```bash
pnpm install
```

Polecenie instaluje zależności całego workspace, w tym:

```text
apps/admin
apps/web
packages/ui
```

Nie należy wykonywać osobnego `npm install` w poszczególnych aplikacjach.

Projekt korzysta ze wspólnego lockfile:

```text
pnpm-lock.yaml
```

## 3. Uruchomienie backendu

Z głównego katalogu projektu:

```bash
docker compose -f docker-compose-local.yml up --build
```

Uruchamiane są między innymi:

```text
carver-db
redis
api
carver-worker
carver-beat
carver-flower
```

Po poprawnym uruchomieniu API powinno być dostępne pod:

```text
http://localhost:8000
```

Flower:

```text
http://localhost:5557
```

Przy kolejnych uruchomieniach, jeśli nie zmieniły się Dockerfile ani zależności Pythona, wystarczy:

```bash
docker compose -f docker-compose-local.yml up
```

### Uruchomienie w tle

Opcjonalnie backend można uruchomić w tle:

```bash
docker compose -f docker-compose-local.yml up -d
```

Logi można wtedy obserwować przez:

```bash
docker compose -f docker-compose-local.yml logs -f
```

lub np. tylko API:

```bash
docker compose -f docker-compose-local.yml logs -f api
```

## 4. Uruchomienie frontendów

Frontendy uruchamiamy lokalnie z głównego katalogu repozytorium:

```bash
pnpm dev
```

Turborepo uruchomi task `dev` dla aplikacji znajdujących się w workspace.

Docelowo dostępne są:

```text
Web:
http://localhost:3000

Admin:
http://localhost:3001
```

### Uruchomienie tylko jednej aplikacji

Panel użytkownika:

```bash
pnpm --filter @world-carver/web dev
```

Panel administracyjny:

```bash
pnpm --filter @world-carver/admin dev
```

Jest to przydatne, jeśli podczas pracy nie są potrzebne oba frontendy.

## 5. Standardowy workflow podczas developmentu

Najwygodniej pracować na dwóch terminalach.

### Terminal 1 — backend

```bash
docker compose -f docker-compose-local.yml up
```

### Terminal 2 — frontend

```bash
pnpm dev
```

Po uruchomieniu środowisko wygląda następująco:

```text
http://localhost:3000
    └── React / Vite — panel użytkownika

http://localhost:3001
    └── React / Vite — panel administracyjny

http://localhost:8000
    └── Django API

http://localhost:5557
    └── Flower
```

PostgreSQL, Redis oraz procesy Celery działają wewnątrz Docker Compose.

## 7. Zatrzymanie projektu

Frontend zatrzymujemy przez:

```text
Ctrl + C
```

Backend:

```text
Ctrl + C
```

jeśli Compose działa na pierwszym planie.

Kontenery można również zatrzymać poleceniem:

```bash
docker compose -f docker-compose-local.yml down
```

Nie usuwa ono danych PostgreSQL zapisanych w volume.

## 8. Reset lokalnej bazy danych

Jeżeli potrzebne jest całkowite usunięcie lokalnej bazy:

```bash
docker compose -f docker-compose-local.yml down -v
```

Następne:

```bash
docker compose -f docker-compose-local.yml up --build
```

utworzy bazę od początku.

**Uwaga:** `down -v` usuwa dane znajdujące się w Docker volumes.

## 9. Zmiana zależności

### Python

Po zmianie:

```text
apps/api/requirements.txt
```

należy przebudować obrazy backendu:

```bash
docker compose -f docker-compose-local.yml build --no-cache
```

a następnie:

```bash
docker compose -f docker-compose-local.yml up
```

### Frontend

Po zmianie któregoś `package.json`:

```text
package.json
apps/admin/package.json
apps/web/package.json
packages/ui/package.json
```

należy wykonać z root projektu:

```bash
pnpm install
```

## 10. Struktura aplikacji frontendowych

Frontend jest zarządzany jako monorepo:

```text
apps/
├── api/
├── admin/
└── web/

packages/
└── ui/
```

`admin` i `web` są niezależnymi aplikacjami React.

Wspólne komponenty interfejsu znajdują się w:

```text
packages/ui
```

i mogą być używane przez oba frontendy jako:

```ts
import { Button } from "@world-carver/ui";
```

Logika biznesowa i funkcjonalności specyficzne dla aplikacji powinny pozostawać odpowiednio w:

```text
apps/admin
```

lub:

```text
apps/web
```

## Szybkie uruchomienie

Przy poprawnie skonfigurowanym projekcie do rozpoczęcia pracy wystarczą dwa polecenia:

```bash
# terminal 1
docker compose -f docker-compose-local.yml up

# terminal 2
pnpm dev
```

Po ich wykonaniu backend, baza danych, Redis, Celery oraz oba frontendy są gotowe do lokalnego developmentu.
