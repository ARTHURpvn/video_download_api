import os
import json
import logging
from typing import Optional, Dict
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import tempfile

logger = logging.getLogger(__name__)

class GoogleAuthService:
    """Serviço para autenticação OAuth com Google e captura de cookies do YouTube"""

    def __init__(self):
        # Verificar se as credenciais estão configuradas
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        # DEBUG: Log para verificar se está carregando
        logger.info(f"🔍 DEBUG - Client ID carregado: {client_id[:20] if client_id else 'None'}...")
        logger.info(f"🔍 DEBUG - Client Secret carregado: {'Sim' if client_secret else 'Não'}")

        if not client_id or not client_secret:
            logger.error("❌ GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET não configurados!")
            logger.error("Configure as variáveis de ambiente antes de usar OAuth")

        self.client_config = {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }

        self.scopes = [
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/youtube.readonly'
        ]

    def is_configured(self) -> bool:
        """Verifica se as credenciais OAuth estão configuradas"""
        return (self.client_config["web"]["client_id"] is not None and
                self.client_config["web"]["client_secret"] is not None)

    def get_authorization_url(self, state: str = None) -> tuple[str, str]:
        """
        Gera URL de autenticação do Google
        Returns: (authorization_url, state)
        """
        # Validar configuração antes de gerar URL
        if not self.is_configured():
            raise ValueError(
                "OAuth não configurado. Configure GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET "
                "nas variáveis de ambiente."
            )

        try:
            flow = Flow.from_client_config(
                self.client_config,
                scopes=self.scopes,
                redirect_uri=self.client_config["web"]["redirect_uris"][0]
            )

            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )

            logger.info(f"✅ URL de autenticação gerada: {authorization_url}")
            return authorization_url, state

        except Exception as e:
            logger.error(f"❌ Erro ao gerar URL de autenticação: {e}")
            raise

    def exchange_code_for_tokens(self, code: str, state: str = None) -> Credentials:
        """
        Troca o código de autorização por tokens de acesso
        """
        try:
            flow = Flow.from_client_config(
                self.client_config,
                scopes=self.scopes,
                redirect_uri=self.client_config["web"]["redirect_uris"][0],
                state=state
            )

            flow.fetch_token(code=code)
            credentials = flow.credentials

            logger.info("✅ Tokens obtidos com sucesso")
            return credentials

        except Exception as e:
            logger.error(f"❌ Erro ao trocar código por tokens: {e}")
            raise

    def get_youtube_cookies_from_credentials(self, credentials: Credentials) -> str:
        """
        Converte credenciais OAuth em cookies no formato Netscape para yt-dlp
        """
        try:
            # Extrair tokens
            access_token = credentials.token
            refresh_token = credentials.refresh_token if hasattr(credentials, 'refresh_token') else None

            # Criar cookies no formato Netscape
            cookies_lines = ['# Netscape HTTP Cookie File']

            # Adicionar cookie de autenticação principal
            if access_token:
                cookies_lines.append(
                    f".youtube.com\tTRUE\t/\tTRUE\t0\tAUTH\t{access_token}"
                )
                cookies_lines.append(
                    f".youtube.com\tTRUE\t/\tTRUE\t0\tSAPISID\t{access_token[:40]}"
                )
                cookies_lines.append(
                    f".youtube.com\tTRUE\t/\tTRUE\t0\t__Secure-3PAPISID\t{access_token[:40]}"
                )

            cookies_content = '\n'.join(cookies_lines)
            logger.info("✅ Cookies gerados a partir das credenciais OAuth")

            return cookies_content

        except Exception as e:
            logger.error(f"❌ Erro ao gerar cookies: {e}")
            raise

    def save_credentials(self, user_id: str, credentials: Credentials) -> str:
        """
        Salva credenciais do usuário em arquivo temporário
        Returns: caminho do arquivo
        """
        try:
            # Criar diretório para credenciais se não existir
            creds_dir = os.path.join(tempfile.gettempdir(), 'youtube_downloader_creds')
            os.makedirs(creds_dir, exist_ok=True)

            # Salvar credenciais
            creds_file = os.path.join(creds_dir, f"{user_id}.json")

            with open(creds_file, 'w') as f:
                json.dump({
                    'token': credentials.token,
                    'refresh_token': credentials.refresh_token if hasattr(credentials, 'refresh_token') else None,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes
                }, f)

            logger.info(f"✅ Credenciais salvas: {creds_file}")
            return creds_file

        except Exception as e:
            logger.error(f"❌ Erro ao salvar credenciais: {e}")
            raise

    def load_credentials(self, user_id: str) -> Optional[Credentials]:
        """
        Carrega credenciais salvas do usuário
        """
        try:
            creds_dir = os.path.join(tempfile.gettempdir(), 'youtube_downloader_creds')
            creds_file = os.path.join(creds_dir, f"{user_id}.json")

            if not os.path.exists(creds_file):
                logger.warning(f"⚠️ Credenciais não encontradas para user_id: {user_id}")
                return None

            with open(creds_file, 'r') as f:
                creds_data = json.load(f)

            credentials = Credentials(
                token=creds_data['token'],
                refresh_token=creds_data.get('refresh_token'),
                token_uri=creds_data['token_uri'],
                client_id=creds_data['client_id'],
                client_secret=creds_data['client_secret'],
                scopes=creds_data['scopes']
            )

            logger.info(f"✅ Credenciais carregadas para user_id: {user_id}")
            return credentials

        except Exception as e:
            logger.error(f"❌ Erro ao carregar credenciais: {e}")
            return None


# Instância global do serviço
auth_service = GoogleAuthService()
