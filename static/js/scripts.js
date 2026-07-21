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

    const travelMap = document.querySelector('[data-travel-map]');
    if (travelMap) {
      const language = document.documentElement.lang;
      const categoryLabel = (value) => ({ personal: language === 'fr' ? 'Personnel' : 'Personal travel', education: language === 'fr' ? 'Études' : 'Education', professional: language === 'fr' ? 'Travail' : 'Professional', lived: language === 'fr' ? 'Lieux vécus' : 'Lived' })[value];
      const categoryLabels = (values) => values.map(categoryLabel).join(' · ');
      const normaliseCategories = (item) => {
        const categories = item.categories || [item.category === 'personal-travel' ? 'personal' : item.category];
        return { ...item, categories, category: categories.includes('lived') ? 'lived' : categories.includes('professional') ? 'professional' : categories.includes('education') ? 'education' : 'personal' };
      };
      const visualKey = (categories) => {
        const visualCategories = categories.filter((category) => category !== 'education');
        return (visualCategories.length ? visualCategories : ['lived']).sort().join('-');
      };
      const palette = { personal: [123, 86, 187], professional: [35, 111, 189], lived: [45, 151, 99] };
      const makePattern = (key) => {
        const categories = key.split('-'); const size = 32; const data = new Uint8Array(size * size * 4);
        for (let y = 0; y < size; y += 1) for (let x = 0; x < size; x += 1) {
          const stripe = categories.length === 1 ? 0 : Math.floor((x + y) / 6) % categories.length;
          const [red, green, blue] = palette[categories[stripe]];
          const offset = (y * size + x) * 4; data[offset] = red; data[offset + 1] = green; data[offset + 2] = blue; data[offset + 3] = 190;
        }
        return { width: size, height: size, data };
      };
      const loadMapLibre = () => new Promise((resolve, reject) => {
        if (window.maplibregl) return resolve(window.maplibregl);
        const script = document.createElement('script'); script.src = `${document.documentElement.dataset.staticRoot || '/static'}/vendor/maplibre-gl.js`; script.onload = () => window.maplibregl ? resolve(window.maplibregl) : reject(new Error('Map library unavailable')); script.onerror = () => reject(new Error('Map library could not load')); document.head.append(script);
      });
      const startMap = async () => {
        try {
          const [maplibregl, travel, world] = await Promise.all([loadMapLibre(), fetch(travelMap.dataset.travelData).then((r) => r.json()), fetch(travelMap.dataset.worldData).then((r) => r.json())]);
          const countries = travel.countries.map(normaliseCategories);
          travelMap.closest('figure')?.querySelectorAll('figcaption li').forEach((item, index) => {
            const country = countries[index];
            if (country) item.textContent = `${language === 'fr' ? country.name_fr : country.name_en} · ${categoryLabels(country.categories)}`;
          });
          const selectedNames = new Set(countries.map((item) => item.name_en));
          const aliases = { 'United States': 'USA', 'United Kingdom': 'England', 'South Korea': 'South Korea', 'Czechia': 'Czech Republic', 'Serbia': 'Republic of Serbia' };
          const polygons = { type: 'FeatureCollection', features: world.features.filter((feature) => selectedNames.has(feature.properties.name) || Object.values(aliases).includes(feature.properties.name)).map((feature) => { const country = countries.find((item) => item.name_en === feature.properties.name || aliases[item.name_en] === feature.properties.name); const categories = country?.categories || ['personal']; return { ...feature, properties: { ...feature.properties, category: country?.category || 'personal', categories: categories.join(','), style_key: visualKey(categories) } }; }) };
          const points = { type: 'FeatureCollection', features: travel.places.map((place) => { const item = normaliseCategories(place); return { type: 'Feature', properties: { ...item, categories: item.categories.join(','), category_label: categoryLabels(item.categories) }, geometry: { type: 'Point', coordinates: [item.longitude, item.latitude] } }; }) };
          const map = new maplibregl.Map({ container: travelMap, style: 'https://tiles.openfreemap.org/styles/liberty', center: [12, 35], zoom: 1.1, attributionControl: true });
          map.addControl(new maplibregl.NavigationControl(), 'top-right'); map.addControl(new maplibregl.FullscreenControl(), 'top-right');
          const bounds = new maplibregl.LngLatBounds(); points.features.forEach((feature) => bounds.extend(feature.geometry.coordinates));
          const fit = () => map.fitBounds(bounds, { padding: 52, maxZoom: 4, duration: reducedMotion ? 0 : 500 });
          const showWorld = () => map.fitBounds([[-180, -58], [180, 82]], { padding: 28, duration: 0 });
          map.on('load', () => {
            const patternKeys = [...new Set(polygons.features.map((feature) => feature.properties.style_key))];
            patternKeys.forEach((key) => map.addImage(`travel-${key}`, makePattern(key)));
            const fillPattern = ['match', ['get', 'style_key']]; patternKeys.forEach((key) => fillPattern.push(key, `travel-${key}`)); fillPattern.push(`travel-${patternKeys[0]}`);
            map.addSource('travel-countries', { type: 'geojson', data: polygons }); map.addSource('travel-places', { type: 'geojson', data: points });
            map.addLayer({ id: 'travel-country-fill', type: 'fill', source: 'travel-countries', paint: { 'fill-pattern': fillPattern, 'fill-opacity': .72 } });
            map.addLayer({ id: 'travel-country-line', type: 'line', source: 'travel-countries', paint: { 'line-color': '#ffffff', 'line-width': 1.2 } });
            map.addLayer({ id: 'travel-place', type: 'circle', source: 'travel-places', paint: { 'circle-radius': 7, 'circle-color': ['match', ['get', 'category'], 'lived', '#2d9763', 'professional', '#236fbd', 'education', '#2d9763', '#7b56bb'], 'circle-stroke-color': '#fff', 'circle-stroke-width': 2 } });
            const popup = new maplibregl.Popup({ closeButton: true, closeOnClick: true });
            map.on('click', 'travel-place', (event) => { const p = event.features[0].properties; popup.setLngLat(event.lngLat).setHTML(`<strong>${p.city}</strong><br>${p.category_label}<br>${p.period}<br>${language === 'fr' ? p.label_fr : p.label_en}`).addTo(map); });
            map.on('click', 'travel-country-fill', (event) => { const name = event.features[0].properties.name; const country = countries.find((item) => item.name_en === name || aliases[item.name_en] === name); popup.setLngLat(event.lngLat).setHTML(`<strong>${language === 'fr' ? country.name_fr : country.name_en}</strong><br>${categoryLabels(country.categories)}`).addTo(map); });
            ['travel-place', 'travel-country-fill'].forEach((id) => { map.on('mouseenter', id, () => map.getCanvas().style.cursor = 'pointer'); map.on('mouseleave', id, () => map.getCanvas().style.cursor = ''); }); showWorld();
            const legend = document.createElement('p'); legend.className = 'map-legend'; legend.innerHTML = `<span class="map-legend-work">${categoryLabel('professional')}</span><span class="map-legend-lived">${categoryLabel('lived')}</span><span class="map-legend-personal">${categoryLabel('personal')}</span><span class="map-legend-multiple">${language === 'fr' ? 'Hachures : plusieurs motifs' : 'Stripes: multiple reasons'}</span>`; travelMap.before(legend);
            document.querySelectorAll('[data-map-filter]').forEach((button) => button.addEventListener('click', () => { const value = button.dataset.mapFilter; const filter = value === 'all' ? null : ['in', value, ['get', 'categories']]; map.setFilter('travel-country-fill', filter); map.setFilter('travel-country-line', filter); map.setFilter('travel-place', filter); document.querySelectorAll('[data-map-filter]').forEach((item) => item.classList.toggle('is-active', item === button)); }));
            document.querySelector('[data-map-fit]')?.addEventListener('click', fit);
          });
        } catch (_) { travelMap.classList.add('map-unavailable'); travelMap.textContent = language === 'fr' ? 'La carte n’a pas pu être chargée. Consultez la liste accessible ci-dessous.' : 'The map could not load. Please use the accessible list below.'; }
      };
      new IntersectionObserver((entries, observer) => { if (entries.some((entry) => entry.isIntersecting)) { observer.disconnect(); startMap(); } }, { rootMargin: '300px' }).observe(travelMap);
    }

    const lists = document.querySelectorAll('.publications-shell ul');
    lists.forEach((list) => {
      const heading = list.previousElementSibling?.textContent || '';
      const type = /Journal|revue/i.test(heading) ? 'paper' : /Conference|Conférence/i.test(heading) ? 'conference' : /Book|ouvrage/i.test(heading) ? 'book' : /Patent|Brevet/i.test(heading) ? 'patent' : /Thesis|Thèse/i.test(heading) ? 'thesis' : 'media';
      [...list.children].forEach((entry) => {
        entry.dataset.publicationType = type;
        entry.dataset.publicationYear = entry.textContent.match(/\b(?:19|20)\d{2}\b/)?.[0] || '0';
      });
      [...list.children].sort((a, b) => Number(b.dataset.publicationYear) - Number(a.dataset.publicationYear)).forEach((entry) => list.append(entry));
      [...list.querySelectorAll('.reference-item')].forEach((entry) => {
        const summary = entry.querySelector('.reference-title');
        const meta = entry.querySelector('.publication-meta');
        if (summary && meta && !summary.querySelector('.reference-scan-meta')) {
          const scanMeta = document.createElement('span');
          scanMeta.className = 'reference-scan-meta';
          scanMeta.textContent = meta.textContent.replace(/\s+/g, ' ').trim();
          summary.append(scanMeta);
        }
      });
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

    const dialog = document.querySelector('[data-media-dialog]');
    const container = document.querySelector('[data-media-container]');
    const title = document.querySelector('[data-media-title]');
    const close = document.querySelector('[data-media-close]');
    let mediaTrigger = null;
    const closeMedia = () => dialog?.close();
    const openMedia = (kind, source, label, trigger) => {
      if (!dialog || !container || !source) return;
      mediaTrigger = trigger;
      if (title) title.textContent = label || (kind === 'video' ? 'Video' : 'Image');
      const element = document.createElement(kind === 'video' ? 'iframe' : 'img');
      if (kind === 'video') {
        element.src = `${source}?autoplay=1`;
        element.title = label || '';
        element.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
        element.allowFullscreen = true;
      } else {
        element.src = source;
        element.alt = label || '';
        element.className = 'media-dialog-image';
      }
      container.replaceChildren(element);
      dialog.showModal();
      close?.focus();
    };
    document.querySelectorAll('[data-video-button]').forEach((button) => button.addEventListener('click', () => {
      openMedia('video', button.dataset.videoSrc, button.dataset.videoTitle, button);
    }));
    document.querySelectorAll('.project-visual').forEach((image) => {
      image.classList.add('is-zoomable');
      image.tabIndex = 0;
      image.setAttribute('role', 'button');
      image.setAttribute('aria-label', `${image.alt}. ${document.documentElement.lang === 'fr' ? 'Agrandir l’image' : 'Open larger image'}`);
      const showImage = () => openMedia('image', image.currentSrc || image.src, image.alt, image);
      image.addEventListener('click', showImage);
      image.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); showImage(); }
      });
    });
    close?.addEventListener('click', closeMedia);
    dialog?.addEventListener('click', (event) => { if (event.target === dialog) closeMedia(); });
    dialog?.addEventListener('close', () => {
      container?.replaceChildren();
      mediaTrigger?.focus();
      mediaTrigger = null;
    });

    document.querySelectorAll('[data-contact-form]').forEach((form) => form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const status = form.querySelector('[data-contact-status]');
      const button = form.querySelector('button[type="submit"]');
      const french = document.documentElement.lang === 'fr';
      if (button) button.disabled = true;
      if (status) status.textContent = french ? 'Envoi en cours…' : 'Sending…';
      try {
        const response = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        if (!response.ok) throw new Error('Form submission failed');
        form.reset();
        if (status) status.textContent = french ? 'Merci, votre message a bien été envoyé.' : 'Thank you, your message has been sent.';
      } catch (_) {
        if (status) status.textContent = french ? 'L’envoi a échoué. Réessayez dans un instant.' : 'Sending failed. Please try again shortly.';
      } finally { if (button) button.disabled = false; }
    }));
  });
})();
