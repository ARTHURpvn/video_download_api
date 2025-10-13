import logging
import secrets
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Optional

from ..services.google_auth import auth_service
from ..models.schemas import CookiesUploadResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["authentication"])

# Armazenar estados temporários (em produção, usar Redis ou banco de dados)
pending_auth_states = {}

@router.get("/login")
async def login_with_google():
    """
    Inicia o fluxo de autenticação OAuth com Google
    Redireciona o usuário para a página de login do Google
    """
    try:
        # Verificar se OAuth está configurado
        if not auth_service.is_configured():
            logger.error("❌ Tentativa de login sem credenciais configuradas")
            raise HTTPException(
                status_code=500,
                detail="OAuth não configurado. Configure GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET nas variáveis de ambiente."
            )

        # Gerar estado único para segurança
        state = secrets.token_urlsafe(32)

        # Obter URL de autorização
        authorization_url, _ = auth_service.get_authorization_url(state)

        # Salvar estado temporariamente
        pending_auth_states[state] = True

        logger.info(f"🔐 Redirecionando usuário para login do Google")

        # Redirecionar para página de login do Google
        return RedirectResponse(url=authorization_url)

    except Exception as e:
        logger.error(f"❌ Erro ao iniciar login: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar autenticação: {str(e)}")


@router.get("/callback")
async def auth_callback(
    code: str = Query(..., description="Código de autorização do Google"),
    state: str = Query(..., description="Estado de segurança"),
    error: Optional[str] = Query(None, description="Erro retornado pelo Google")
):
    """
    Callback do OAuth - processa o retorno do Google após login
    """
    try:
        # Verificar se houve erro
        if error:
            logger.error(f"❌ Erro do Google: {error}")
            raise HTTPException(status_code=400, detail=f"Erro na autenticação: {error}")

        # Verificar estado de segurança
        if state not in pending_auth_states:
            logger.error("❌ Estado inválido ou expirado")
            raise HTTPException(status_code=400, detail="Estado de autenticação inválido")

        # Remover estado usado
        del pending_auth_states[state]

        # Trocar código por tokens
        logger.info("🔄 Trocando código por tokens...")
        credentials = auth_service.exchange_code_for_tokens(code, state)

        # Gerar cookies a partir das credenciais
        logger.info("🍪 Gerando cookies do YouTube...")
        cookies_content = auth_service.get_youtube_cookies_from_credentials(credentials)

        # Salvar credenciais (usar user_id do token em produção)
        user_id = secrets.token_urlsafe(16)
        auth_service.save_credentials(user_id, credentials)

        logger.info(f"✅ Autenticação bem-sucedida! User ID: {user_id}")

        # Retornar página HTML que envia os cookies para o frontend
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Autenticação Concluída</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    text-align: center;
                    padding: 2rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }}
                .success {{
                    font-size: 4rem;
                    margin-bottom: 1rem;
                }}
                h1 {{
                    margin: 0 0 1rem 0;
                }}
                p {{
                    margin: 0.5rem 0;
                    opacity: 0.9;
                }}
                .loader {{
                    border: 4px solid rgba(255, 255, 255, 0.3);
                    border-top: 4px solid white;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 1rem auto;
                }}
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success">✅</div>
                <h1>Autenticação Concluída!</h1>
                <p>Cookies do YouTube capturados com sucesso</p>
                <div class="loader"></div>
                <p>Fechando janela e enviando dados...</p>
            </div>
            
            <script>
                // Enviar cookies para o frontend via postMessage
                if (window.opener) {{
                    window.opener.postMessage({{
                        type: 'youtube_auth_success',
                        userId: '{user_id}',
                        cookies: `{cookies_content}`,
                        message: 'Autenticação concluída com sucesso!'
                    }}, '*');
                    
                    // Fechar janela após 2 segundos
                    setTimeout(() => {{
                        window.close();
                    }}, 2000);
                }} else {{
                    // Se não tiver opener, salvar no localStorage
                    localStorage.setItem('youtube_cookies', `{cookies_content}`);
                    localStorage.setItem('youtube_user_id', '{user_id}');
                    
                    setTimeout(() => {{
                        window.location.href = '/';
                    }}, 2000);
                }}
            </script>
        </body>
        </html>
        """

        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)

    except Exception as e:
        logger.error(f"❌ Erro no callback: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erro ao processar callback: {str(e)}")


@router.get("/cookies/{user_id}")
async def get_user_cookies(user_id: str):
    """
    Retorna os cookies salvos de um usuário autenticado
    """
    try:
        # Carregar credenciais
        credentials = auth_service.load_credentials(user_id)

        if not credentials:
            raise HTTPException(status_code=404, detail="Credenciais não encontradas. Faça login novamente.")

        # Gerar cookies
        cookies_content = auth_service.get_youtube_cookies_from_credentials(credentials)

        return {
            "status": "success",
            "cookies": cookies_content,
            "message": "Cookies recuperados com sucesso"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao recuperar cookies: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar cookies: {str(e)}")


@router.get("/status")
async def auth_status():
    """
    Verifica o status da configuração de autenticação
    """
    import os

    has_client_id = bool(os.getenv("GOOGLE_CLIENT_ID"))
    has_client_secret = bool(os.getenv("GOOGLE_CLIENT_SECRET"))

    return {
        "configured": has_client_id and has_client_secret,
        "client_id_set": has_client_id,
        "client_secret_set": has_client_secret,
        "message": "OAuth configurado" if (has_client_id and has_client_secret) else "Configure GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET nas variáveis de ambiente"
    }
