import csv
import io
import os
import zipfile
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from estudantes.models import Estudante
from turmas.models import Turma, LocalAula
from registros.models import RegistroAcademico


class Command(BaseCommand):
    help = "Importa os dados acadêmicos normalizados do dataset SIMPA para o PostgreSQL"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando importação do dataset SIMPA..."))

        # Localizar o arquivo zip
        candidatos = [
            Path(__file__).resolve().parent.parent.parent.parent.parent / "_recursos" / "Arquivos Dataset-20261022.zip",
            Path("C:/Users/augus/Projetos/SIMPA/_recursos/dataset mandados/Arquivos Dataset-20261022.zip"),
            Path("C:/Users/augus/OneDrive/Desktop/SIMPA/_recursos/Arquivos Dataset-20261022.zip"),
            Path(__file__).resolve().parent.parent.parent.parent.parent / "_recursos" / "Arquivos Dataset-20260920.zip",
        ]

        zip_path = None
        for c in candidatos:
            if c.exists():
                zip_path = c
                break

        if not zip_path:
            self.stderr.write("Arquivo do dataset não encontrado nos diretórios de recursos.")
            return

        self.stdout.write(f"Utilizando arquivo: {zip_path.name}")
        z = zipfile.ZipFile(zip_path)

        def ler_csv(nome_arquivo):
            content = z.read(nome_arquivo).decode("utf-8", errors="ignore")
            return list(csv.DictReader(io.StringIO(content)))

        with transaction.atomic():
            # 1. Cidades
            cidades_csv = ler_csv("CSV Normalizado/cidades.csv")
            mapa_cidades = {c["cidade_id"]: c["nome"] for c in cidades_csv}

            # 2. Docentes
            docentes_csv = ler_csv("CSV Normalizado/docentes.csv")
            mapa_docentes = {
                d["docente_id"]: (d.get("nome_sintetico") or d.get("nome") or f"Docente {d['docente_id']}")
                for d in docentes_csv
            }

            # 3. Disciplinas
            disciplinas_csv = ler_csv("CSV Normalizado/disciplinas.csv")
            mapa_disciplinas = {
                d["disciplina_id"]: {
                    "codigo": d["codigo"],
                    "nome": d["nome"],
                    "carga_horaria": int(d.get("carga_horaria", 60) or 60),
                }
                for d in disciplinas_csv
            }

            # 4. Locais de Aula (IE04)
            locais_criados = []
            salas_config = [
                ("Bloco A", "Sala 101", "1º Andar", 45, "Sala de Aula"),
                ("Bloco A", "Sala 102", "1º Andar", 45, "Sala de Aula"),
                ("Bloco B", "Lab IA 01", "2º Andar", 40, "Laboratório de Informática"),
                ("Bloco B", "Lab Redes 02", "2º Andar", 40, "Laboratório de Informática"),
                ("Bloco C", "Sala 204", "2º Andar", 50, "Sala de Aula"),
                ("Bloco F", "Auditório Central", "Térreo", 120, "Auditório"),
            ]
            for bloco, sala, andar, cap, tipo in salas_config:
                loc, _ = LocalAula.objects.get_or_create(
                    campus="UniEVANGÉLICA - Campus Sede",
                    bloco=bloco,
                    sala=sala,
                    defaults={
                        "andar": andar,
                        "cidade": "Anápolis",
                        "uf": "GO",
                        "capacidade": cap,
                        "tipo_espaco": tipo,
                    },
                )
                locais_criados.append(loc)

            # 5. Turmas
            turmas_csv = ler_csv("CSV Normalizado/turmas.csv")
            mapa_turmas = {}
            turmas_count = 0

            for i, t in enumerate(turmas_csv):
                turma_id = t["turma_id"]
                disc_info = mapa_disciplinas.get(t["disciplina_id"], {"codigo": f"DISC{t['disciplina_id']}", "nome": f"Disciplina {t['disciplina_id']}", "carga_horaria": 60})
                docente_nome = mapa_docentes.get(t.get("docente_id"), "Docente UniEVANGÉLICA")
                codigo_turma = t.get("codigo_turma") or f"T-{turma_id}"
                ano = t.get("ano_letivo", "2026")
                semestre = t.get("semestre_letivo", "1")
                periodo_str = f"{ano}/{semestre}"

                local_escolhido = locais_criados[i % len(locais_criados)] if locais_criados else None

                turma_obj, criada = Turma.objects.get_or_create(
                    codigo=codigo_turma,
                    defaults={
                        "nome": disc_info["nome"],
                        "curso": "Engenharia de Software / IA",
                        "periodo": periodo_str,
                        "professor": docente_nome,
                        "carga_horaria": disc_info["carga_horaria"],
                        "local_aula": local_escolhido,
                        "horario": "19:00 - 22:30",
                        "dia_semana": ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"][i % 5],
                        "link_grupo_whatsapp": f"https://chat.whatsapp.com/Turma-{codigo_turma}",
                    },
                )
                mapa_turmas[turma_id] = turma_obj
                if criada:
                    turmas_count += 1

            # 6. Alunos e Endereços
            alunos_csv = ler_csv("CSV Normalizado/alunos.csv")
            enderecos_csv = ler_csv("CSV Normalizado/enderecos_alunos.csv")
            mapa_cidade_aluno = {
                e["aluno_id"]: mapa_cidades.get(e.get("cidade_id"), "Anápolis")
                for e in enderecos_csv
            }

            mapa_alunos = {}
            alunos_count = 0

            for a in alunos_csv:
                aluno_id = a["aluno_id"]
                ra = a.get("codigo_academico") or f"RA{aluno_id}"
                nome = a.get("nome_sintetico") or f"Estudante {aluno_id}"
                d_nasc = a.get("data_nascimento") or None
                cidade_origem = mapa_cidade_aluno.get(aluno_id, "Anápolis")
                email = f"aluno{aluno_id}@aluno.simpa.edu.br"

                # Gerar CPF válido sintético determinístico
                n_str = str(aluno_id).zfill(9)
                d1 = sum(int(n_str[x]) * (10 - x) for x in range(9)) % 11
                d1 = 0 if d1 < 2 else 11 - d1
                d2 = (sum(int(n_str[x]) * (11 - x) for x in range(9)) + d1 * 2) % 11
                d2 = 0 if d2 < 2 else 11 - d2
                cpf_sintetico = f"{n_str}{d1}{d2}"

                estudante_obj, criado = Estudante.objects.get_or_create(
                    matricula=ra,
                    defaults={
                        "nome": nome,
                        "cpf": cpf_sintetico,
                        "data_nascimento": d_nasc,
                        "email": email,
                        "telefone": f"6299{str(aluno_id).zfill(7)}",
                        "curso": "Engenharia de Software / IA",
                    },
                )
                mapa_alunos[aluno_id] = estudante_obj
                if criado:
                    alunos_count += 1

            # 7. Mapear matriculas_curso -> aluno_id
            matriculas_csv = ler_csv("CSV Normalizado/matriculas_curso.csv")
            mapa_matr_para_aluno = {
                m["matricula_curso_id"]: mapa_alunos.get(m.get("aluno_id"))
                for m in matriculas_csv
            }

            # 8. Registros Acadêmicos (Notas e Frequência)
            registros_csv = ler_csv("CSV Normalizado/registros_academicos.csv")
            registros_count = 0

            for r in registros_csv:
                estudante_obj = mapa_matr_para_aluno.get(r.get("matricula_curso_id"))
                turma_obj = mapa_turmas.get(r.get("turma_id"))

                if not estudante_obj or not turma_obj:
                    continue

                # Adicionar estudante à turma (M2M)
                turma_obj.estudantes.add(estudante_obj)

                # Processar notas e respeitar valores NULL intencionais
                nota_raw = r.get("nota_final") or r.get("nota_parcial") or None
                nota_dec = None
                if nota_raw and str(nota_raw).strip():
                    try:
                        val = float(str(nota_raw).strip())
                        # Escala do dataset é 0-100; normalizar para 0-10 conforme padrão do modelo SIMPA
                        if val > 10.0:
                            val = val / 10.0
                        nota_dec = Decimal(str(round(val, 2)))
                    except (ValueError, TypeError):
                        nota_dec = None

                freq_raw = r.get("frequencia_percentual") or None
                freq_dec = None
                if freq_raw and str(freq_raw).strip():
                    try:
                        freq_dec = Decimal(str(round(float(str(freq_raw).strip()), 2)))
                    except (ValueError, TypeError):
                        freq_dec = None

                situacao = r.get("situacao", "EM_CURSO")
                periodo_str = turma_obj.periodo

                reg_obj, criado = RegistroAcademico.objects.get_or_create(
                    estudante=estudante_obj,
                    turma=turma_obj,
                    periodo=periodo_str,
                    defaults={
                        "nota": nota_dec,
                        "frequencia": freq_dec,
                        "situacao_original": situacao,
                        "observacoes": f"Tentativa {r.get('tentativa', '1')} | Status dataset: {situacao}",
                    },
                )
                if criado:
                    registros_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Importação concluída com sucesso!\n"
            f"- {alunos_count} novos estudantes cadastrados (Total no banco: {Estudante.objects.count()})\n"
            f"- {turmas_count} novas turmas cadastradas (Total no banco: {Turma.objects.count()})\n"
            f"- {len(locais_criados)} locais de aula configurados (Total no banco: {LocalAula.objects.count()})\n"
            f"- {registros_count} novos registros acadêmicos lançados (Total no banco: {RegistroAcademico.objects.count()})"
        ))
