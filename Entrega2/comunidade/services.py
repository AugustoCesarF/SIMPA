import json
import os
import re
import urllib.parse
import urllib.request
from .models import LogNotificacaoWhatsApp


class WhatsAppService:
    """
    IE03 — Serviço de Integração com o WhatsApp Business Cloud API (Meta).
    
    Conforme a documentação oficial da Meta:
    - O envio programático de mensagens diretas requer uma conta Meta for Developers,
      WABA (WhatsApp Business Account) e número de telefone registrado.
    - Mensagens iniciadas pelo sistema para usuários exigem uso de Templates pré-aprovados pela Meta.
    - A API oficial do Meta NÃO suporta envio programático de mensagens automáticas
      para grupos comunitários abertos. Para grupos, a política da Meta estabelece
      o compartilhamento do link de convite oficial do grupo (https://chat.whatsapp.com/...)
      ou canais de transmissão (Broadcast Channels).
    """

    API_VERSION = "v19.0"
    GRAPH_URL = f"https://graph.facebook.com/{API_VERSION}"

    def __init__(self):
        self.token = os.getenv("WHATSAPP_API_TOKEN", "")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        self.business_account_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")

    def is_configured(self) -> bool:
        """Verifica se as credenciais da Meta Cloud API estão presentes no ambiente."""
        return bool(self.token and self.phone_number_id)

    def sanitizar_telefone(self, telefone: str) -> str:
        """Limpa caracteres especiais e garante o formato internacional DDI + DDD + Número."""
        numeros = re.sub(r"\D", "", str(telefone))
        if len(numeros) in (10, 11) and not numeros.startswith("55"):
            numeros = "55" + numeros
        return numeros

    def gerar_link_compartilhamento(self, telefone: str, mensagem: str) -> str:
        """
        Gera link oficial para acionar o WhatsApp diretamente no navegador/celular.
        Formato suportado universalmente: https://api.whatsapp.com/send?phone=...&text=...
        """
        tel_limpo = self.sanitizar_telefone(telefone)
        msg_enc = urllib.parse.quote(mensagem)
        return f"https://api.whatsapp.com/send?phone={tel_limpo}&text={msg_enc}"

    def enviar_notificacao_risco(
        self,
        destinatario_nome: str,
        destinatario_telefone: str,
        aluno=None,
        turma=None,
        motivo_risco: str = "",
        recomendacao: str = "",
    ) -> dict:
        """
        Envia (ou registra conforme credenciais disponíveis) a notificação de apoio/risco acadêmico.
        """
        tel_limpo = self.sanitizar_telefone(destinatario_telefone)
        mensagem = (
            f"Olá, {destinatario_nome}! Aqui é do acompanhamento acadêmico SIMPA da UniEVANGÉLICA. "
            f"Identificamos um ponto de atenção no seu semestre: {motivo_risco or 'Desempenho acadêmico'}. "
            f"Recomendação: {recomendacao or 'Procure a tutoria ou o plantão de monitoria para agendar apoio individualizado.'}"
        )

        template_nome = "simpa_alerta_academico"
        log = LogNotificacaoWhatsApp(
            destinatario_nome=destinatario_nome,
            destinatario_telefone=tel_limpo,
            estudante=aluno,
            turma=turma,
            tipo_notificacao="ALERTA_RISCO",
            mensagem=mensagem,
            template_utilizado=template_nome,
        )

        link_direto = self.gerar_link_compartilhamento(tel_limpo, mensagem)

        if not self.is_configured():
            # Registro oficial de dependência externa: sem credenciais ativas, o SIMPA registra
            # com conformidade e informa a pendência de autorização do provedor externo Meta.
            log.status_envio = "PENDENTE_AUTORIZACAO_API"
            log.resposta_api = (
                "Credenciais Meta Cloud API (WHATSAPP_API_TOKEN ou WHATSAPP_PHONE_NUMBER_ID) "
                "não configuradas no .env. Notificação registrada localmente com sucesso."
            )
            log.save()

            return {
                "sucesso": True,
                "status": "PENDENTE_AUTORIZACAO_API",
                "mensagem": "Notificação registrada no SIMPA. Envio real aguardando credenciais ativas da Meta Cloud API.",
                "log_id": log.id,
                "destinatario": destinatario_nome,
                "telefone": tel_limpo,
                "link_acionamento_direto": link_direto,
                "dependencias_externas": [
                    "Conta Meta for Developers aprovada",
                    "WhatsApp Business Account (WABA) ativa",
                    "System User Access Token configurado em WHATSAPP_API_TOKEN",
                    "ID de número de telefone configurado em WHATSAPP_PHONE_NUMBER_ID",
                    "Template 'simpa_alerta_academico' previamente aprovado no painel da Meta",
                ],
            }

        # Quando as credenciais estiverem ativas, realiza chamada HTTP oficial via urllib (sem libs externas)
        try:
            url = f"{self.GRAPH_URL}/{self.phone_number_id}/messages"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": tel_limpo,
                "type": "text",
                "text": {"body": mensagem},
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            messages = data.get("messages", [])
            meta_id = messages[0].get("id", "") if messages else ""
            log.status_envio = "ENVIADO"
            log.meta_message_id = meta_id
            log.resposta_api = json.dumps(data)
            log.save()
            return {
                "sucesso": True,
                "status": "ENVIADO",
                "meta_message_id": meta_id,
                "log_id": log.id,
            }

        except Exception as e:
            log.status_envio = "ERRO_API"
            log.resposta_api = str(e)
            log.save()
            return {
                "sucesso": False,
                "status": "ERRO_API",
                "erro": str(e),
                "log_id": log.id,
            }
