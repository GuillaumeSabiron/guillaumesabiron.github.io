(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ready = (callback) => document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', callback)
    : callback();

  ready(() => {
    document.querySelectorAll('[data-current-year]').forEach((element) => {
      element.textContent = String(new Date().getFullYear());
    });

    const savedScroll = sessionStorage.getItem('portfolio-language-scroll');
    if (savedScroll && !window.location.hash) {
      sessionStorage.removeItem('portfolio-language-scroll');
      window.scrollTo({ top: Number(savedScroll), behavior: reducedMotion ? 'auto' : 'instant' });
    }
    document.querySelectorAll('.language-switcher a').forEach((link) => link.addEventListener('click', () => {
      sessionStorage.setItem('portfolio-language-scroll', String(window.scrollY));
    }));

    const lists = document.querySelectorAll('.publications-shell ul');
    lists.forEach((list) => {
      const heading = list.previousElementSibling?.textContent || '';
      const type = /Journal|revue/i.test(heading) ? 'paper' : /Conference|Conférence/i.test(heading) ? 'conference' : /Book|ouvrage/i.test(heading) ? 'book' : /Patent|Brevet/i.test(heading) ? 'patent' : /Thesis|Thèse/i.test(heading) ? 'thesis' : 'media';
      [...list.children].forEach((entry) => {
        entry.dataset.publicationType = type;
        entry.dataset.publicationYear = entry.textContent.match(/\b(?:19|20)\d{2}\b/)?.[0] || '0';
      });
      [...list.children].sort((a, b) => Number(b.dataset.publicationYear) - Number(a.dataset.publicationYear)).forEach((entry) => list.append(entry));
    });
    document.querySelectorAll('[data-publication-filter]').forEach((button) => button.addEventListener('click', () => {
      const selected = button.dataset.publicationFilter;
      document.querySelectorAll('.publications-shell li[data-publication-type]').forEach((entry) => { entry.hidden = selected !== 'all' && entry.dataset.publicationType !== selected; });
      lists.forEach((list) => {
        const visible = [...list.children].some((entry) => !entry.hidden);
        list.hidden = !visible;
        if (list.previousElementSibling) list.previousElementSibling.hidden = !visible;
      });
      document.querySelectorAll('[data-publication-filter]').forEach((item) => {
        const active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      });
    }));

    const requestedPaper = new URLSearchParams(window.location.search).get('paper');
    if (requestedPaper) {
      const selected = [...document.querySelectorAll('.reference-item')].find((item) => item.querySelector('.reference-title')?.textContent.trim() === requestedPaper);
      if (selected) {
        selected.open = true;
        selected.scrollIntoView({ block: 'center', behavior: reducedMotion ? 'auto' : 'smooth' });
      }
    }

    const menuButton = document.querySelector('[data-menu-button]');
    const menu = document.querySelector('[data-site-menu]');
    if (menuButton && menu) {
      const closeMenu = () => { menu.classList.remove('is-open'); menuButton.setAttribute('aria-expanded', 'false'); };
      menuButton.addEventListener('click', () => {
        const isOpen = menu.classList.toggle('is-open');
        menuButton.setAttribute('aria-expanded', String(isOpen));
      });
      menu.querySelectorAll('a[href^="#"]').forEach((link) => link.addEventListener('click', closeMenu));
      document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeMenu(); });
    }

    const backToTop = document.querySelector('[data-back-to-top]');
    if (backToTop) {
      const updateBackToTop = () => backToTop.classList.toggle('is-visible', window.scrollY > 500);
      window.addEventListener('scroll', updateBackToTop, { passive: true });
      updateBackToTop();
      backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' }));
    }

    const dialog = document.querySelector('[data-video-dialog]');
    const container = document.querySelector('[data-video-container]');
    const close = document.querySelector('[data-video-close]');
    document.querySelectorAll('[data-video-button]').forEach((button) => button.addEventListener('click', () => {
      if (!dialog || !container) return;
      const iframe = document.createElement('iframe');
      iframe.src = `${button.dataset.videoSrc}?autoplay=1`;
      iframe.title = button.dataset.videoTitle || '';
      iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;
      container.replaceChildren(iframe);
      dialog.showModal();
    }));
    const closeVideo = () => { dialog?.close(); container?.replaceChildren(); };
    close?.addEventListener('click', closeVideo);
    dialog?.addEventListener('close', () => container?.replaceChildren());
  });
})();
