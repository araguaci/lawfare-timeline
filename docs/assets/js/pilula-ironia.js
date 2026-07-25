/**
 * Pílula de Ironia — integração Jekyll (lawfare-timeline)
 * Chama o workflow n8n existente (ver README do pilula-de-ironia, seção 4).
 *
 * IMPORTANTE: troque WEBHOOK_URL pela URL real do seu webhook n8n ativo.
 * O corpo enviado (`corpo`) já vem truncado e higienizado pelo include
 * botao-pilula.html — nunca envie o dossiê investigativo completo aqui.
 */
(function () {
  const WEBHOOK_URL = 'https://SEU-N8N-DOMINIO/webhook/pilula-ironia';

  const btn = document.getElementById('gerar-pilula-btn');
  if (!btn) return;

  const opcoes = document.getElementById('pilula-opcoes');
  const resultDiv = document.getElementById('pilula-resultado');
  const selAutor1 = document.getElementById('pilula-autor1');
  const selAutor2 = document.getElementById('pilula-autor2');
  const selAcidez = document.getElementById('pilula-acidez');

  // Primeiro clique: revela as opções em vez de gerar direto
  let opcoesReveladas = false;

  btn.addEventListener('click', async function () {
    if (!opcoesReveladas) {
      opcoes.hidden = false;
      opcoesReveladas = true;
      btn.textContent = '🧪 Confirmar e gerar';
      return;
    }

    await gerarPilula();
  });

  async function gerarPilula() {
    const autores = [selAutor1.value];
    if (selAutor2.value) autores.push(selAutor2.value);

    const payload = {
      id: Number(btn.dataset.id),
      titulo: btn.dataset.titulo,
      corpo: btn.dataset.corpo,
      autores: autores,
      acidez: Number(selAcidez.value),
    };

    btn.disabled = true;
    const textoOriginal = btn.textContent;
    btn.textContent = 'Gerando...';
    resultDiv.hidden = true;

    try {
      const res = await fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error('Falha na resposta do webhook: ' + res.status);

      const data = await res.json();

      resultDiv.hidden = false;
      resultDiv.innerHTML =
        '<blockquote class="pilula-texto">"' +
        escapeHtml(data.pilula_ironia) +
        '"</blockquote>' +
        '<p class="pilula-autoria">— ' +
        escapeHtml(data.autoria) +
        ' · ' +
        escapeHtml(data.acidez) +
        '</p>' +
        '<button type="button" id="copiar-pilula" class="btn-pilula-secundario">Copiar</button>';

      document.getElementById('copiar-pilula').addEventListener('click', function () {
        navigator.clipboard.writeText(data.pilula_ironia);
        this.textContent = 'Copiado ✓';
        setTimeout(() => (this.textContent = 'Copiar'), 2000);
      });
    } catch (err) {
      resultDiv.hidden = false;
      resultDiv.innerHTML =
        '<p class="pilula-erro">Não foi possível gerar a pílula agora. Tente novamente em instantes.</p>';
      console.error('Erro ao gerar pílula de ironia:', err);
    } finally {
      btn.disabled = false;
      btn.textContent = textoOriginal === 'Gerando...' ? '🧪 Confirmar e gerar' : textoOriginal;
    }
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
})();
