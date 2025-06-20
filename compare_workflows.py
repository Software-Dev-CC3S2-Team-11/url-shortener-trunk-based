import subprocess
import os

# Repositorios que queremos comparar
repos = {
    "Git Flow": "url-shortener-git-flow",
    "Trunk-Based": "url-shortener-trunk-based-1"
}

# Archivo donde se guardará el reporte
reporte_path = "reports/workflow_comparison.md"


def ejecutar_git(repo, comandos):
    return subprocess.check_output(["git", "-C", repo] + comandos,
                                   text=True).strip()


def listar_ramas(repo):
    salida = ejecutar_git(repo, ["branch", "-r"])
    ramas = []
    for linea in salida.splitlines():
        if "->" not in linea:
            ramas.append(linea.strip())
    return ramas


def contar_commits(repo):
    ramas = listar_ramas(repo)
    conteo = {}
    for r in ramas:
        total = ejecutar_git(repo, ["rev-list", "--count", r])
        conteo[r] = int(total)
    return conteo


def contar_merges(repo):
    ramas = listar_ramas(repo)
    conteo = {}
    for r in ramas:
        log = ejecutar_git(repo, ["log", r, "--merges", "--pretty=oneline"])
        conteo[r] = len(log.splitlines()) if log else 0
    return conteo


def crear_reporte(info):
    os.makedirs(os.path.dirname(reporte_path), exist_ok=True)
    with open(reporte_path, "w", encoding="utf-8") as f:
        f.write("# Comparación de Workflows\n\n")
        for nombre, datos in info.items():
            f.write(f"## {nombre}\n\n")
            f.write("### Merges por rama\n")
            for rama, cantidad in datos["merges"].items():
                f.write(f"- `{rama}`: {cantidad} merges\n")
            f.write("\n")
            f.write("### Commits por rama\n")
            for rama, cantidad in datos["commits"].items():
                f.write(f"- `{rama}`: {cantidad} commits\n")
            f.write("\n")


def main():
    resultados = {}
    for nombre, ruta in repos.items():
        resultados[nombre] = {
            "merges": contar_merges(ruta),
            "commits": contar_commits(ruta)
        }
    crear_reporte(resultados)


if __name__ == "__main__":
    main()
