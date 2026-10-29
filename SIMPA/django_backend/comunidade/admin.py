from django.contrib import admin
from .models import PerfilUsuario, TopicoDuvida, RespostaDuvida, LogNotificacaoWhatsApp


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("user", "telefone", "cidade", "curso", "notificacoes_whatsapp", "atualizado_em")
    search_fields = ("user__username", "user__email", "telefone", "curso")


@admin.register(TopicoDuvida)
class TopicoDuvidaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "disciplina_nome", "turma", "resolvido", "criado_em")
    list_filter = ("resolvido", "criado_em")
    search_fields = ("titulo", "conteudo", "autor__username")


@admin.register(RespostaDuvida)
class RespostaDuvidaAdmin(admin.ModelAdmin):
    list_display = ("topico", "autor", "eh_solucao", "criado_em")
    list_filter = ("eh_solucao", "criado_em")
    search_fields = ("conteudo", "autor__username")


@admin.register(LogNotificacaoWhatsApp)
class LogNotificacaoWhatsAppAdmin(admin.ModelAdmin):
    list_display = ("destinatario_nome", "destinatario_telefone", "tipo_notificacao", "status_envio", "criado_em")
    list_filter = ("status_envio", "tipo_notificacao", "criado_em")
    search_fields = ("destinatario_nome", "destinatario_telefone", "mensagem")
