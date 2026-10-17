/* ============================================================
   設計書の図（Mermaid）の初期化（Phase 30-1）
   - 図は <figure class="diagram"> の中に <pre class="mermaid"> で文字で書く
   - 配色は style.css の変数（--diag-* 等）から読み、ライト / ダークで同じ設定を使う。
     テーマが切り替わったら描き直す
   - 「拡大」ボタンで全画面の枠を開き、svg-pan-zoom で拡大・縮小・移動する
   - <figure class="diagram" data-wide> は図を縮めず、枠の中で横スクロールさせる
   - AWS アイコンは aws-icons.js（window.DOCS_AWS_ICONS）を aws: の名前で使う
   - 描画の状態を <html data-diagrams="pending|ready|error"> に出す
     （tools/docs_check.py が描画完了を待つために使う）
   - 読み込みは vendor の mermaid.min.js・svg-pan-zoom.min.js・aws-icons.js の後に置く
     （どれも <script> で読む 1 ファイル版。file:// で直接開いても動く）
   ============================================================ */
(function () {
  'use strict';

  var root = document.documentElement;
  var blocks = Array.prototype.slice.call(document.querySelectorAll('pre.mermaid'));
  if (!blocks.length) return;
  root.setAttribute('data-diagrams', 'pending');

  var DARK_QUERY = '(prefers-color-scheme: dark)';
  var sources = blocks.map(function (pre) { return pre.textContent; });
  var canvases = [];
  var renderCount = 0;
  var zoomDialog = null;
  var zoomInstance = null;

  function cssVar(name) {
    return getComputedStyle(root).getPropertyValue(name).trim();
  }

  /* 図の配色・字体の設定（ここ 1 か所だけで決める） */
  function mermaidConfig() {
    var dark = window.matchMedia(DARK_QUERY).matches;
    return {
      startOnLoad: false,
      securityLevel: 'strict',
      theme: 'base',
      darkMode: dark,
      fontFamily: getComputedStyle(document.body).fontFamily,
      themeVariables: {
        darkMode: dark,
        fontFamily: getComputedStyle(document.body).fontFamily,
        fontSize: '14px',
        background: cssVar('--bg'),
        textColor: cssVar('--text'),
        primaryColor: cssVar('--diag-box'),
        primaryBorderColor: cssVar('--diag-box-border'),
        primaryTextColor: cssVar('--diag-text'),
        secondaryColor: cssVar('--diag-emph'),
        secondaryBorderColor: cssVar('--diag-emph-border'),
        secondaryTextColor: cssVar('--diag-text'),
        tertiaryColor: cssVar('--diag-box-alt'),
        tertiaryBorderColor: cssVar('--diag-box-alt-border'),
        tertiaryTextColor: cssVar('--diag-text'),
        lineColor: cssVar('--diag-line'),
        mainBkg: cssVar('--diag-box'),
        nodeBorder: cssVar('--diag-box-border'),
        clusterBkg: cssVar('--bg'),
        clusterBorder: cssVar('--border-strong'),
        edgeLabelBackground: cssVar('--bg'),
        noteBkgColor: cssVar('--warn-bg'),
        noteBorderColor: cssVar('--warn-border'),
        noteTextColor: cssVar('--text'),
        actorBkg: cssVar('--diag-box'),
        actorBorder: cssVar('--diag-box-border'),
        actorTextColor: cssVar('--diag-text'),
        signalColor: cssVar('--diag-line'),
        signalTextColor: cssVar('--text'),
        labelBoxBkgColor: cssVar('--diag-box-alt'),
        labelBoxBorderColor: cssVar('--diag-box-alt-border'),
        attributeBackgroundColorOdd: cssVar('--bg'),
        attributeBackgroundColorEven: cssVar('--bg-subtle')
      },
      flowchart: { useMaxWidth: true, htmlLabels: true },
      sequence: { useMaxWidth: true },
      er: { useMaxWidth: true },
      state: { useMaxWidth: true },
      architecture: { useMaxWidth: true }
    };
  }

  /* 図 1 枚ぶりの枠（描画先・ツールバー）を用意する */
  function prepare(pre, index) {
    var canvas = document.createElement('div');
    canvas.className = 'diagram-canvas';
    pre.hidden = true;
    pre.insertAdjacentElement('afterend', canvas);

    var figure = pre.closest('figure.diagram');
    if (figure) {
      var bar = document.createElement('div');
      bar.className = 'diagram-toolbar';
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'diagram-zoom-open';
      button.textContent = '拡大';
      button.setAttribute('aria-label', '図を拡大して見る');
      button.addEventListener('click', function () { openZoom(index); });
      bar.appendChild(button);
      figure.insertBefore(bar, figure.firstChild);
    }
    return canvas;
  }

  function showError(canvas, error) {
    canvas.className = 'diagram-canvas diagram-error';
    canvas.textContent = '図を描けませんでした: ' + ((error && error.message) || String(error));
  }

  /* 横に広い図（data-wide）は縮めずに元の幅で置き、枠の中で横スクロールさせる */
  function applyWidth(canvas) {
    var figure = canvas.closest('figure.diagram');
    var svg = canvas.querySelector('svg');
    if (!svg || !figure || !figure.hasAttribute('data-wide')) return;
    var box = svg.viewBox && svg.viewBox.baseVal;
    svg.style.maxWidth = 'none';
    if (box && box.width) svg.setAttribute('width', String(Math.ceil(box.width)));
  }

  async function renderAll() {
    var mermaid = window.mermaid;
    if (!mermaid) {
      canvases.forEach(function (canvas) {
        showError(canvas, 'mermaid.min.js を読み込めていない');
      });
      root.setAttribute('data-diagrams-errors', String(canvases.length));
      root.setAttribute('data-diagrams', 'error');
      return;
    }
    root.setAttribute('data-diagrams', 'pending');
    mermaid.initialize(mermaidConfig());
    var errors = 0;
    renderCount += 1;
    for (var i = 0; i < canvases.length; i++) {
      var canvas = canvases[i];
      try {
        var result = await mermaid.render('docs-diagram-' + renderCount + '-' + i, sources[i]);
        canvas.className = 'diagram-canvas';
        canvas.innerHTML = result.svg;
        if (result.bindFunctions) result.bindFunctions(canvas);
        applyWidth(canvas);
      } catch (error) {
        errors += 1;
        showError(canvas, error);
      }
    }
    root.setAttribute('data-diagrams-count', String(canvases.length));
    root.setAttribute('data-diagrams-errors', String(errors));
    root.setAttribute('data-diagrams', errors ? 'error' : 'ready');
  }

  /* ---- 拡大表示（svg-pan-zoom） ---- */
  function ensureDialog() {
    if (zoomDialog) return zoomDialog;
    zoomDialog = document.createElement('dialog');
    zoomDialog.className = 'diagram-zoom';
    zoomDialog.innerHTML =
      '<div class="diagram-zoom-bar"><span class="diagram-zoom-hint">' +
      'ドラッグで移動・ホイールか右下のボタンで拡大縮小</span>' +
      '<button type="button" class="diagram-zoom-close">閉じる</button></div>' +
      '<div class="diagram-zoom-body"></div>';
    zoomDialog.querySelector('.diagram-zoom-close').addEventListener('click', function () {
      zoomDialog.close();
    });
    zoomDialog.addEventListener('close', function () {
      if (zoomInstance) { zoomInstance.destroy(); zoomInstance = null; }
      zoomDialog.querySelector('.diagram-zoom-body').innerHTML = '';
    });
    document.body.appendChild(zoomDialog);
    return zoomDialog;
  }

  function openZoom(index) {
    var source = canvases[index] && canvases[index].querySelector('svg');
    if (!source) return;
    var dialog = ensureDialog();
    var body = dialog.querySelector('.diagram-zoom-body');
    var svg = source.cloneNode(true);
    svg.removeAttribute('style');
    svg.setAttribute('width', '100%');
    svg.setAttribute('height', '100%');
    body.innerHTML = '';
    body.appendChild(svg);
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
    if (typeof window.svgPanZoom === 'function') {
      zoomInstance = window.svgPanZoom(svg, {
        controlIconsEnabled: true,
        fit: true,
        center: true,
        minZoom: 0.5,
        maxZoom: 20,
        zoomScaleSensitivity: 0.3
      });
    }
  }

  function start() {
    var mermaid = window.mermaid;
    if (mermaid && window.DOCS_AWS_ICONS && typeof mermaid.registerIconPacks === 'function') {
      mermaid.registerIconPacks([{ name: 'aws', icons: window.DOCS_AWS_ICONS }]);
    }
    canvases = blocks.map(prepare);
    renderAll();
    var mql = window.matchMedia(DARK_QUERY);
    var rerender = function () { renderAll(); };
    if (mql.addEventListener) mql.addEventListener('change', rerender);
    else if (mql.addListener) mql.addListener(rerender);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
