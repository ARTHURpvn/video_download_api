from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    return {"message": "YouTube Video Downloader API", "docs": "/docs"}

@router.get("/health")
async def health_check():
    """Endpoint de health check para verificar se a API está funcionando"""
    return {"status": "healthy", "message": "API está funcionando"}

@router.options("/video/info")
@router.options("/video/download")
@router.options("/downloads")
@router.options("/downloads/{filename}")
async def options_handler():
    """Manipula requisições OPTIONS para CORS"""
    return {"message": "OK"}

@router.get("/debug/common-errors")
async def list_common_errors():
    """Lista os principais erros 400 e suas possíveis soluções"""
    return {
        "common_400_errors": {
            "1. Video unavailable": {
                "causes": [
                    "Vídeo privado ou removido",
                    "Vídeo com restrição de idade",
                    "Vídeo com restrição geográfica",
                    "URL inválida ou malformada"
                ],
                "solutions": [
                    "Verificar se o vídeo existe no YouTube",
                    "Tentar com URL diferente (youtu.be vs youtube.com)",
                    "Usar VPN se for restrição geográfica"
                ]
            },
            "2. Sign in to confirm your age": {
                "causes": [
                    "Vídeo com restrição de idade",
                    "YouTube requer login"
                ],
                "solutions": [
                    "Usar configurações diferentes no yt-dlp",
                    "Tentar com cliente Android/iOS"
                ]
            },
            "3. HTTP Error 403: Forbidden": {
                "causes": [
                    "YouTube detectou bot/automação",
                    "Rate limiting",
                    "Headers HTTP inadequados"
                ],
                "solutions": [
                    "Usar user-agent realista",
                    "Adicionar delays entre requisições",
                    "Usar diferentes player clients (Android, iOS)"
                ]
            },
            "4. Extraction failed": {
                "causes": [
                    "Mudanças na API do YouTube",
                    "yt-dlp desatualizado",
                    "Formato não disponível"
                ],
                "solutions": [
                    "Atualizar yt-dlp",
                    "Tentar formatos diferentes",
                    "Usar fallback strategies"
                ]
            },
            "5. This live event has ended": {
                "causes": [
                    "Tentativa de baixar live stream que acabou",
                    "Vídeo ainda sendo processado"
                ],
                "solutions": [
                    "Aguardar processamento completo",
                    "Tentar novamente mais tarde"
                ]
            }
        },
        "troubleshooting_steps": [
            "1. Testar URL no navegador primeiro",
            "2. Verificar se é URL válida do YouTube",
            "3. Tentar com /video/diagnose endpoint",
            "4. Verificar logs do servidor",
            "5. Testar com vídeos públicos simples primeiro"
        ]
    }
