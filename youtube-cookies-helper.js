/**
 * Helper para extrair cookies do YouTube do navegador do cliente
 * e converter para o formato Netscape que o yt-dlp espera
 */

/**
 * Extrai todos os cookies do domínio youtube.com
 * @returns {Promise<string>} Cookies em formato Netscape
 */
export async function getYouTubeCookies() {
  try {
    // Verificar se a API de cookies está disponível (apenas funciona em extensões ou contextos específicos)
    if (typeof document.cookie === 'undefined') {
      console.warn('⚠️ Cookies não disponíveis neste contexto');
      return null;
    }

    // Pegar cookies do documento atual (se estiver em youtube.com)
    const cookies = document.cookie;

    if (!cookies) {
      console.warn('⚠️ Nenhum cookie encontrado');
      return null;
    }

    // Converter para formato Netscape
    const netscapeCookies = convertToNetscapeFormat(cookies);

    return netscapeCookies;
  } catch (error) {
    console.error('❌ Erro ao extrair cookies:', error);
    return null;
  }
}

/**
 * Converte cookies do formato JavaScript para Netscape
 * @param {string} cookieString - String de cookies no formato "name=value; name2=value2"
 * @returns {string} Cookies no formato Netscape
 */
function convertToNetscapeFormat(cookieString) {
  const lines = ['# Netscape HTTP Cookie File'];

  // Separar cookies individuais
  const cookies = cookieString.split('; ');

  cookies.forEach(cookie => {
    const [name, value] = cookie.split('=');
    if (name && value) {
      // Formato Netscape: domain, flag, path, secure, expiration, name, value
      lines.push(`.youtube.com\tTRUE\t/\tFALSE\t0\t${name}\t${value}`);
    }
  });

  return lines.join('\n');
}

/**
 * Função para fazer requisição com cookies automáticos
 * @param {string} url - URL do vídeo do YouTube
 * @param {object} options - Opções adicionais (quality, format, audio_only)
 * @returns {Promise<Response>}
 */
export async function fetchVideoInfoWithCookies(url, options = {}) {
  // Tentar obter cookies
  const cookies = await getYouTubeCookies();

  // Fazer requisição para o backend
  const response = await fetch('http://localhost:8000/video/info', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      cookies_content: cookies,
      ...options
    }),
  });

  return response;
}

/**
 * Função para download com cookies automáticos
 * @param {string} url - URL do vídeo do YouTube
 * @param {object} options - Opções adicionais (quality, format, audio_only)
 * @returns {Promise<Response>}
 */
export async function downloadVideoWithCookies(url, options = {}) {
  // Tentar obter cookies
  const cookies = await getYouTubeCookies();

  // Fazer requisição para o backend
  const response = await fetch('http://localhost:8000/video/download-stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: url,
      cookies_content: cookies,
      quality: options.quality || 'best',
      format: options.format || 'mp4',
      audio_only: options.audio_only || false,
    }),
  });

  return response;
}

