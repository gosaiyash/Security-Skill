#!/usr/bin/env bash
# Read-only repository discovery for the web-app-security skill.
# Makes no network calls and modifies nothing. Prints file names and match counts, not secret values.
# Usage: scripts/inventory.sh [path]   (default: current directory)
set -u
ROOT="${1:-.}"
cd "$ROOT" || { echo "cannot cd to $ROOT" >&2; exit 1; }
EXCL='-not -path */node_modules/* -not -path */.git/* -not -path */vendor/* -not -path */dist/* -not -path */build/* -not -path */.venv/* -not -path */venv/*'

section() { printf '\n== %s ==\n' "$1"; }
found() { find . -type f $EXCL \( "$@" \) 2>/dev/null | head -50; }

section "Manifests and lockfiles"
found -name package.json -o -name package-lock.json -o -name yarn.lock -o -name pnpm-lock.yaml \
  -o -name requirements*.txt -o -name Pipfile* -o -name pyproject.toml -o -name poetry.lock \
  -o -name go.mod -o -name go.sum -o -name Cargo.toml -o -name Cargo.lock -o -name pom.xml \
  -o -name 'build.gradle*' -o -name Gemfile* -o -name composer.json -o -name composer.lock -o -name '*.csproj'

section "Containers, IaC, CI/CD"
found -iname 'Dockerfile*' -o -name 'docker-compose*.y*ml' -o -name '*.tf' -o -name 'Chart.yaml' \
  -o -path './.github/workflows/*' -o -name '.gitlab-ci.yml' -o -name Jenkinsfile -o -name 'azure-pipelines.yml' \
  -o -name 'serverless.y*ml' -o -name 'nginx*.conf' -o -name '.dockerignore'

section "Config and env files (names only; values not read)"
found -name '.env*' -o -name '*.pem' -o -name '*.key' -o -name 'config*.y*ml' -o -name 'settings*.py' -o -name 'application*.properties'

section "API specs and schemas"
found -name 'openapi*' -o -name 'swagger*' -o -name '*.graphql' -o -name '*.gql' -o -name '*.proto'

section "Tests and security tooling present"
found -name '.semgrep*' -o -name '.gitleaks*' -o -name '.trivyignore' -o -name 'codeql*' -o -name '.pre-commit-config.yaml' \
  -o -name 'SECURITY.md' -o -name 'security.txt' -o -name 'dependabot.yml' -o -name 'renovate.json' | head -20
printf 'test files (approx): '; find . -type f $EXCL \( -name '*test*' -o -name '*spec*' \) 2>/dev/null | wc -l

count() { # label, regex
  n=$(grep -rEIl --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=vendor --exclude-dir=dist \
      --exclude-dir=build --exclude-dir=.venv --exclude-dir=venv -e "$2" . 2>/dev/null | wc -l)
  printf '%-34s %s file(s)\n' "$1" "$n"
}

section "Route / entry-point indicators (file counts)"
count "Express/Koa/Fastify routes"    '(app|router)\.(get|post|put|patch|delete)\('
count "Flask/FastAPI decorators"      '@(app|router|bp|blueprint)\.(route|get|post|put|patch|delete)'
count "Django urls"                   'urlpatterns|path\('
count "Spring mappings"               '@(Get|Post|Put|Delete|Request)Mapping'
count "Rails routes"                  'Rails\.application\.routes|resources :'
count "ASP.NET controllers"           '\[Http(Get|Post|Put|Delete)|MapGet\(|MapPost\('
count "GraphQL"                       'graphql|GraphQLSchema|typeDefs'
count "WebSocket"                     'WebSocket|socket\.io|ws://|wss://'
count "Webhooks"                      '[Ww]ebhook'

section "Auth / session indicators (file counts)"
count "JWT"                           'jsonwebtoken|jwt\.|PyJWT|JwtSecurityToken|jose'
count "OAuth/OIDC"                    'oauth|openid|oidc|passport|authlib'
count "Password hashing"              'bcrypt|argon2|scrypt|pbkdf2'
count "CSRF handling"                 'csrf|xsrf'
count "CORS config"                   'cors|Access-Control-Allow-Origin'

section "Risky-pattern leads (file counts; confirm manually)"
count "Dynamic code/exec"             'eval\(|exec\(|child_process|os\.system|subprocess|Runtime\.getRuntime|shell=True'
count "Raw SQL / string-built"        'execute\(f|raw\(|SELECT .*\+|query\(`'
count "HTML sinks"                    'innerHTML|dangerouslySetInnerHTML|v-html|\|safe|Html\.Raw'
count "Unsafe deserialization"        'pickle\.loads|yaml\.load\(|ObjectInputStream|unserialize|BinaryFormatter'
count "TLS verification disabled"     'verify=False|rejectUnauthorized: *false|InsecureSkipVerify'
count "Weak crypto"                   'md5|sha1|Math\.random|ECB'
count "File upload"                   'multipart|upload|FileField|multer'
count "Outbound HTTP (SSRF review)"   'requests\.(get|post)|axios|fetch\(|HttpClient|urllib|http\.Get'
count "Possible hard-coded secrets"   '(api[_-]?key|secret|passwd|password|token)[\"'\'' ]*[:=][\"'\'' ]*[A-Za-z0-9/+_-]{12,}'

printf '\nDone. Counts are leads, not findings. Mark undiscovered areas as UNKNOWN in the report.\n'
