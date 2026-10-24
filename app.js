(() => {
  const books = window.BOOKS || [];
  const grid = document.querySelector('#books');
  const input = document.querySelector('#search');
  const count = document.querySelector('#count');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  const palette = ['#40564c', '#97543d', '#3d5365', '#807147', '#6d4851', '#575c43'];
  const nodes = books.map((book, i) => {
    const li = document.createElement('li'); li.className = 'book';
    const cover = document.createElement('div'); cover.className = 'cover'; cover.setAttribute('aria-hidden', 'true');
    const fallback = document.createElement('div'); fallback.className = 'fallback'; fallback.style.setProperty('--jacket', palette[i % palette.length]);
    const ornament = document.createElement('span'); ornament.className = 'ornament'; ornament.textContent = '✦';
    const jacketTitle = document.createElement('strong'); jacketTitle.textContent = book.title;
    const jacketAuthor = document.createElement('small'); jacketAuthor.textContent = book.author;
    fallback.append(ornament, jacketTitle, jacketAuthor); cover.append(fallback);
    if (book.cover) {
      const img = document.createElement('img'); img.src = book.cover; img.alt = ''; img.loading = i < 12 ? 'eager' : 'lazy'; img.decoding = 'async'; img.width = 200; img.height = 300;
      img.addEventListener('load', () => { fallback.hidden = true; });
      img.addEventListener('error', () => { img.remove(); fallback.hidden = false; }); cover.append(img);
    }
    const title = document.createElement('h2'); title.textContent = book.title;
    const author = document.createElement('p'); author.className = 'author'; author.textContent = book.author;
    li.append(cover, title, author);
    return { li, text: normalize(`${book.title} ${book.author}`) };
  });
  grid.append(...nodes.map(n => n.li));
  function filter() {
    const terms = normalize(input.value).split(' ').filter(Boolean);
    let visible = 0;
    for (const node of nodes) { node.li.hidden = !terms.every(term => node.text.includes(term)); if (!node.li.hidden) visible++; }
    count.textContent = terms.length ? `${visible} of ${books.length} books` : `${books.length} books on the shelf`;
    document.querySelector('#empty').hidden = visible !== 0;
  }
  input.addEventListener('input', filter);
  document.querySelector('#reset').addEventListener('click', () => { input.value = ''; filter(); input.focus(); });
  input.addEventListener('keydown', event => { if (event.key === 'Escape') { input.value = ''; filter(); } });
  filter();
})();
