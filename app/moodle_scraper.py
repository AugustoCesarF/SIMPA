"""
moodle_scraper.py

Faz login no AVA (Moodle) da UniEVANGÉLICA usando sessão autenticada
e extrai dados (notas, cursos, frequência) via parsing de HTML.

IMPORTANTE:
- Isso NÃO é uma API oficial. É scraping autenticado.
- Guarde as credenciais em variáveis de ambiente, nunca no código.
- Não faça requisições em loop apertado — o AVA pode bloquear o IP/conta
  por comportamento anômalo. Use cache (ver main.py).
"""

import os
import re
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup

AVA_BASE_URL = "https://avagrad.unievangelica.edu.br"
LOGIN_URL = f"{AVA_BASE_URL}/login/index.php"
DASHBOARD_URL = f"{AVA_BASE_URL}/my/"
GRADES_OVERVIEW_URL = f"{AVA_BASE_URL}/grade/report/overview/index.php"

# Headers "de navegador" pra reduzir chance de bloqueio por bot
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


class MoodleAuthError(Exception):
    """Erro ao autenticar no AVA (credenciais inválidas, captcha, etc.)."""


@dataclass
class MoodleSession:
    """Encapsula uma sessão autenticada no Moodle."""

    session: requests.Session = field(default_factory=requests.Session)
    logged_in: bool = False

    def login(self, username: str, password: str) -> None:
        self.session.headers.update(HEADERS)

        # 1. Pega a página de login pra extrair o logintoken (anti-CSRF do Moodle)
        resp = self.session.get(LOGIN_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        token_input = soup.find("input", {"name": "logintoken"})
        logintoken = token_input["value"] if token_input else ""

        # 2. Envia o form de login
        payload = {
            "username": username,
            "password": password,
            "logintoken": logintoken,
        }
        resp = self.session.post(LOGIN_URL, data=payload, timeout=15)
        resp.raise_for_status()

        # 3. Confirma que logou de fato (Moodle redireciona pro /my/ se OK;
        #    se falhar, a página de login volta com uma div de erro)
        if "login/index.php" in resp.url or "loginerrors" in resp.text:
            raise MoodleAuthError(
                "Falha no login do AVA — verifique usuário/senha ou se há captcha."
            )

        self.logged_in = True

    def get_grades_overview(self) -> list[dict]:
        """Retorna notas por curso a partir da página 'Visão geral das notas'."""
        if not self.logged_in:
            raise MoodleAuthError("Chame login() antes de buscar dados.")

        resp = self.session.get(GRADES_OVERVIEW_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        rows = []
        table = soup.find("table", {"class": re.compile("generaltable")})
        if not table:
            return rows

        for tr in table.find_all("tr")[1:]:  # pula cabeçalho
            cols = tr.find_all("td")
            if len(cols) < 2:
                continue
            curso = cols[0].get_text(strip=True)
            nota = cols[1].get_text(strip=True)
            if curso:
                rows.append({"curso": curso, "nota": nota})

        return rows

    def get_courses(self) -> list[dict]:
        """Retorna a lista de cursos/disciplinas matriculadas."""
        if not self.logged_in:
            raise MoodleAuthError("Chame login() antes de buscar dados.")

        resp = self.session.get(DASHBOARD_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        courses = []
        # Moodle geralmente usa <a> com href contendo /course/view.php?id=
        for link in soup.find_all("a", href=re.compile(r"/course/view\.php\?id=\d+")):
            nome = link.get_text(strip=True)
            href = link["href"]
            match = re.search(r"id=(\d+)", href)
            course_id = match.group(1) if match else None
            if nome and course_id:
                courses.append({"id": course_id, "nome": nome, "url": href})

        # remove duplicados mantendo ordem
        seen = set()
        unique = []
        for c in courses:
            if c["id"] not in seen:
                seen.add(c["id"])
                unique.append(c)
        return unique


def fetch_all_data(username: str, password: str) -> dict:
    """Função de conveniência: loga e busca tudo de uma vez."""
    ms = MoodleSession()
    ms.login(username, password)
    return {
        "cursos": ms.get_courses(),
        "notas": ms.get_grades_overview(),
    }


if __name__ == "__main__":
    # Teste manual local — nunca deixe credenciais hardcoded em produção
    user = os.environ.get("AVA_USERNAME")
    pwd = os.environ.get("AVA_PASSWORD")
    if not user or not pwd:
        raise SystemExit("Defina AVA_USERNAME e AVA_PASSWORD nas variáveis de ambiente.")

    data = fetch_all_data(user, pwd)
    print(data)
