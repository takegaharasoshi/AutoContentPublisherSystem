/* ============================================================
   課題・アイデア一覧のカード表示（Phase 24-2）
   - 対象は table[data-cards] のみ。行の内容は表のセルをそのまま使い、
     PC 用・スマホ用の文章を二重管理しない
   - data-card-extra="2,3,8"（1 始まりの列番号）の列を「補足」として
     初期状態でたたみ、行ごとのボタンで開閉する（複数行を同時に開ける・状態は保存しない）
   - 表からカードへの見た目の切り替えは CSS（768 CSS px 未満）が行う。
     本スクリプトが動かない場合も、PC 幅では元の表、狭い画面では全項目を
     展開したカードとして読める
   - 外部依存なし（このファイル 1 本だけを読み込む）
   ============================================================ */
(function () {
  'use strict';

  var NARROW_QUERY = '(max-width: 767.98px)';
  var mql = window.matchMedia(NARROW_QUERY);
  /* hidden="until-found"（ブラウザー内検索で自動的に開く隠し方）が使えるか。
     使えない環境では通常の hidden にフォールバックする（開閉は同じく動く）。 */
  var untilFound = 'onbeforematch' in document.documentElement;
  var rows = [];

  function textOf(el) {
    return (el.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function labelsOf(table) {
    var heads = table.querySelectorAll('thead th');
    var labels = [];
    for (var i = 0; i < heads.length; i++) {
      labels.push(textOf(heads[i]));
    }
    return labels;
  }

  function extraIndexesOf(table) {
    var map = {};
    var raw = table.getAttribute('data-card-extra') || '';
    raw.split(',').forEach(function (part) {
      var n = parseInt(part, 10);
      if (n > 0) {
        map[n] = true;
      }
    });
    return map;
  }

  function prepareRow(tr, labels, extraIndexes) {
    var cells = tr.children;
    var extras = [];
    var names = [];
    var main = 0;
    for (var i = 0; i < cells.length; i++) {
      var td = cells[i];
      if (td.tagName !== 'TD' && td.tagName !== 'TH') {
        continue;
      }
      if (labels[i] && !td.hasAttribute('data-label')) {
        td.setAttribute('data-label', labels[i]);
      }
      if (extraIndexes[i + 1]) {
        td.classList.add('card-extra');
        extras.push(td);
        if (labels[i]) {
          names.push(labels[i]);
        }
      } else {
        td.classList.add('card-main');
        main += 1;
      }
    }
    if (!extras.length || !main) {
      return;
    }

    /* トグルは行の末尾に専用セルを足して置く（既存セルの文面を汚さない）。
       PC 幅ではこのセルを CSS で非表示にするため、表の列は増えない。 */
    var cell = document.createElement('td');
    cell.className = 'card-toggle-cell';
    cell.setAttribute('data-card-generated', '1');
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'card-toggle';
    cell.appendChild(button);
    tr.appendChild(cell);

    var row = { tr: tr, extras: extras, button: button, names: names.join('・'), open: false };
    rows.push(row);

    button.addEventListener('click', function () {
      row.open = !row.open;
      sync(row);
    });
    extras.forEach(function (td) {
      /* ブラウザー内検索が hidden="until-found" を開いたときに表示状態を合わせる */
      td.addEventListener('beforematch', function () {
        row.open = true;
        sync(row);
      });
    });
    sync(row);
  }

  function setHidden(row, hidden) {
    row.extras.forEach(function (td) {
      if (hidden) {
        td.setAttribute('hidden', untilFound ? 'until-found' : '');
      } else {
        td.removeAttribute('hidden');
      }
    });
  }

  function sync(row) {
    var narrow = mql.matches;
    setHidden(row, narrow && !row.open);
    if (row.tr.classList.toggle) {
      row.tr.classList.toggle('is-open', row.open);
    }
    row.button.setAttribute('aria-expanded', row.open ? 'true' : 'false');
    row.button.textContent = row.open
      ? '− 補足を閉じる'
      : '＋ 補足' + (row.names ? '（' + row.names + '）' : '');
  }

  function syncAll() {
    rows.forEach(sync);
  }

  /* CSS が古いまま（ブラウザーのキャッシュ）だとカード表示にならず、
     24-1 の列幅対策も効かない。狭い画面で表のままなら気づけるように知らせる。 */
  function warnIfStaleStyle(table) {
    if (!mql.matches || !table) {
      return;
    }
    if (window.getComputedStyle(table).display === 'block') {
      return;
    }
    if (document.getElementById('docs-cards-stale')) {
      return;
    }
    var box = document.createElement('div');
    box.id = 'docs-cards-stale';
    box.className = 'warn';
    box.textContent =
      'スタイルシートが古い可能性があります（ブラウザーのキャッシュ）。'
      + 'ページを再読み込みしてください。表が読みにくいまま変わらない場合は、'
      + 'キャッシュを消してから開き直してください。';
    var container = document.querySelector('.container') || document.body;
    container.insertBefore(box, container.firstChild);
  }

  function setup() {
    var tables = document.querySelectorAll('table[data-cards]');
    for (var t = 0; t < tables.length; t++) {
      var table = tables[t];
      var labels = labelsOf(table);
      var extraIndexes = extraIndexesOf(table);
      var trs = table.querySelectorAll('tbody > tr');
      for (var r = 0; r < trs.length; r++) {
        prepareRow(trs[r], labels, extraIndexes);
      }
    }
    warnIfStaleStyle(tables[0]);
    if (mql.addEventListener) {
      mql.addEventListener('change', syncAll);
    } else if (mql.addListener) {
      mql.addListener(syncAll);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup);
  } else {
    setup();
  }
})();
