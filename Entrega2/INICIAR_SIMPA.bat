@echo off
chcp 65001 > nul
cls
color 0B
echo ================================================================
echo    SIMPA — SISTEMA INTELIGENTE DE MONITORAMENTO E PREDIÇÃO
echo                UniEVANGÉLICA — ENTREGA 2
echo ================================================================
echo.
echo [1/2] Abrindo o navegador automaticamente...
start "" "http://127.0.0.1:8000/"

echo [2/2] Iniciando o servidor Django na porta 8000...
echo.
echo ================================================================
echo   🌐 URLs Prontas para a Apresentação:
echo   • Painel Principal (HUD Escuro):  http://127.0.0.1:8000/
echo   • Módulo Analítico & Gráficos:    http://127.0.0.1:8000/analytics/
echo   • Locais de Aula e WhatsApp:      http://127.0.0.1:8000/comunidade/locais/
echo   • Fórum de Dúvidas:               http://127.0.0.1:8000/comunidade/duvidas/
echo ================================================================
echo.
echo Pressione Ctrl + C no teclado para encerrar o servidor.
echo.
python manage.py runserver 127.0.0.1:8000
pause
