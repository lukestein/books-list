(() => {
  const books = window.BOOKS || [];
  document.querySelector('#updated-month').textContent = window.LIBRARY_META?.updatedMonth || 'October 2026';
  const grid = document.querySelector('#books');
  const input = document.querySelector('#search');
  const count = document.querySelector('#count');
  const clearButton = document.querySelector('#clear-search');
  let authorReturn = null;
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
      const img = document.createElement('img'); img.src = book.cover; img.alt = ''; img.loading = i >= books.length - 12 ? 'eager' : 'lazy'; img.decoding = 'async'; img.width = 200; img.height = 300;
      img.addEventListener('load', () => { fallback.hidden = true; });
      img.addEventListener('error', () => { img.remove(); fallback.hidden = false; }); cover.append(img);
    }
    const number = document.createElement('span'); number.className = 'book-number';
    number.textContent = String(i + 1); number.setAttribute('aria-label', `Book ${i + 1}`);
    const title = document.createElement('h2'); title.textContent = book.title;
    if (book.reread) {
      const marker = document.createElement('sup'); marker.className = 'reread';
      const link = document.createElement('a'); link.href = '#reread-note'; link.textContent = '*'; link.setAttribute('aria-label', 'Re-read; see note');
      const lastSpace = book.title.lastIndexOf(' ');
      title.textContent = book.title.slice(0, lastSpace + 1);
      const ending = document.createElement('span'); ending.className = 'title-ending';
      ending.textContent = book.title.slice(lastSpace + 1);
      marker.append(link); ending.append(marker); title.append(ending);
    }
    const author = document.createElement('p'); author.className = 'author';
    const authors = book.authors || [book.author];
    authors.forEach((name, index) => {
      if (index) author.append(index === authors.length - 1 ? ' & ' : ', ');
      const authorButton = document.createElement('button'); authorButton.type = 'button'; authorButton.textContent = name;
      authorButton.setAttribute('aria-label', `Filter books by ${name}`);
      authorButton.addEventListener('click', () => {
        if (!normalize(input.value)) {
          authorReturn = { button: authorButton, offset: authorButton.getBoundingClientRect().top };
        }
        input.value = name; filter();
        document.querySelector('.toolbar').scrollIntoView({ block: 'start' });
      });
      author.append(authorButton);
    });
    li.append(cover, number, title, author);
    return { li, reread: Boolean(book.reread), text: normalize(`${book.title} ${book.author} ${authors.join(' ')}`) };
  });
  grid.append(...nodes.slice().reverse().map(n => n.li));
  function filter() {
    const terms = normalize(input.value).split(' ').filter(Boolean);
    let visible = 0;
    let visibleReread = false;
    for (const node of nodes) {
      node.li.hidden = !terms.every(term => node.text.includes(term));
      if (!node.li.hidden) { visible++; visibleReread ||= node.reread; }
    }
    document.querySelector('#reread-note').hidden = !visibleReread;
    count.textContent = terms.length ? `${visible} of ${books.length} books` : `${books.length} books`;
    clearButton.hidden = input.value.length === 0;
    document.querySelector('#empty').hidden = visible !== 0;
  }
  input.addEventListener('input', () => {
    if (!input.value && authorReturn) clearSearch();
    else filter();
  });
  function clearSearch() {
    const returnTo = authorReturn;
    authorReturn = null;
    input.value = ''; filter();
    if (returnTo) {
      // Let input editing finish before moving focus and restoring the gallery.
      requestAnimationFrame(() => {
        // Follow the original book even if the viewport changed while filtering.
        returnTo.button.focus({ preventScroll: true });
        window.scrollBy({ top: returnTo.button.getBoundingClientRect().top - returnTo.offset, behavior: 'instant' });
      });
    } else input.focus({ preventScroll: true });
  }
  clearButton.addEventListener('click', clearSearch);
  document.querySelector('#reset').addEventListener('click', clearSearch);
  input.addEventListener('keydown', event => { if (event.key === 'Escape') { event.preventDefault(); clearSearch(); } });
  filter();
})();
