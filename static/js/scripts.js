/*!
* Start Bootstrap - Resume v7.0.6 (https://startbootstrap.com/theme/resume)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-resume/blob/master/LICENSE)
*/
//
// Scripts
// 

window.updateCurrentYear = function updateCurrentYear() {
    document.querySelectorAll('[data-current-year]').forEach((element) => {
        element.textContent = String(new Date().getFullYear());
    });
};

window.addEventListener('DOMContentLoaded', event => {

    window.updateCurrentYear();

    // Activate Bootstrap scrollspy on the main nav element
    const sideNav = document.body.querySelector('#sideNav');
    if (sideNav && window.bootstrap?.ScrollSpy) {
        new window.bootstrap.ScrollSpy(document.body, {
            target: '#sideNav',
            rootMargin: '0px 0px -40%',
        });
    }

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (navbarToggler && window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

function toggleDescription(target) {
    const desc = typeof target === 'string'
        ? document.getElementById(target)
        : target?.nextElementSibling;

    if (!desc) {
        return false;
    }

    const isHidden = window.getComputedStyle(desc).display === 'none';
    desc.style.display = isHidden ? 'block' : 'none';
    return false;
}

window.initializePublicationList = function initializePublicationList() {
    const publicationLists = document.querySelectorAll('.publications-shell ul');

    publicationLists.forEach((list) => {
        const sectionHeading = list.previousElementSibling?.textContent || '';
        const publicationType = sectionHeading.includes('Journal')
            ? 'paper'
            : sectionHeading.includes('Conference')
                ? 'conference'
                : sectionHeading.includes('Book chapters')
                    ? 'book'
                    : sectionHeading.includes('Thesis')
                        ? 'thesis'
                        : 'media';
        const entries = Array.from(list.querySelectorAll(':scope > li'));

        entries.forEach((entry) => {
            const meta = entry.querySelector('.publication-meta');
            const summary = entry.querySelector('.reference-title');
            const match = meta?.textContent.match(/\b(19|20)\d{2}\b/);
            const year = match ? Number(match[0]) : 0;

            entry.dataset.publicationYear = String(year);
            entry.dataset.publicationType = publicationType;

            if (summary && year && !summary.querySelector('.publication-year')) {
                const yearLabel = document.createElement('span');
                yearLabel.className = 'publication-year';
                yearLabel.textContent = String(year);
                summary.append(yearLabel);
            }
        });

        entries
            .sort((a, b) => Number(b.dataset.publicationYear) - Number(a.dataset.publicationYear))
            .forEach((entry) => list.append(entry));
    });

    const filters = document.querySelectorAll('[data-publication-filter]');
    filters.forEach((filter) => {
        if (filter.dataset.publicationFilterInitialized === 'true') return;

        filter.dataset.publicationFilterInitialized = 'true';
        filter.addEventListener('click', () => {
            const selectedType = filter.dataset.publicationFilter;

            document.querySelectorAll('.publications-shell li[data-publication-type]').forEach((entry) => {
                entry.hidden = selectedType !== 'all' && entry.dataset.publicationType !== selectedType;
            });

            publicationLists.forEach((list) => {
                const hasVisibleEntry = Array.from(list.children).some((entry) => !entry.hidden);
                list.hidden = !hasVisibleEntry;
                const heading = list.previousElementSibling;
                if (heading) heading.hidden = !hasVisibleEntry;
            });

            filters.forEach((button) => {
                const isActive = button === filter;
                button.classList.toggle('is-active', isActive);
                button.setAttribute('aria-pressed', String(isActive));
            });
        });
    });
};


function applyStyles() {
    const container = document.querySelector('.container-fluid.p-0');
    if (!container) {
        return;
    }
    container.style.maxWidth = '1000px';
    container.style.width = '100%';
    container.style.margin = '0 auto';
}

function createWorldProjection(element) {
    const width = element.offsetWidth || 960;
    const height = element.offsetHeight || 600;
    const scale = (width / (2 * Math.PI)) * 0.95;

    const projection = d3.geo.equirectangular()
        .center([0, 15])
        .scale(scale)
        .translate([width / 2, height / 2]);

    return {
        path: d3.geo.path().projection(projection),
        projection,
    };
}

window.initializeMap = function initializeMap() {
    const container = document.getElementById('map1');
    if (!container || typeof Datamap === 'undefined' || !window.COUNTRIES || !window.CITIES) {
        return;
    }

    if (container.__mapInstance) {
        window.removeEventListener('resize', container.__mapResizeHandler);
        container.__mapInstance = null;
        container.__mapResizeHandler = null;
        container.innerHTML = '';
    }

    const setProjection = function projectionFactory(element) {
        return createWorldProjection(element);
    };

    const map = new Datamap({
        scope: 'world',
        element: container,
        responsive: true,
        height: container.offsetHeight || 700,
        setProjection,
        fills: {
            defaultFill: '#D0D0D0',
            lived: '#7ec8e3',
            visited: '#6699CC',
            city: '#FC8050',
        },
        geographyConfig: {
            highlightOnHover: true,
            highlightFillColor: '#A0C0A0',
            highlightBorderColor: '#F0F0F0',
            popupOnHover: true,
            popupTemplate: function popupTemplate(geography) {
                return '<div class="hoverinfo"><b>' + geography.properties.name + '</b></div>';
            },
        },
        bubblesConfig: {
            borderWidth: 1,
            borderColor: '#FFFFFF',
            highlightOnHover: true,
            popupOnHover: true,
            popupTemplate: function bubbleTemplate(geo, data) {
                return "<div class='hoverinfo'>" + data.name + ":<br>" + data.date + "</div>";
            },
        },
        data: window.COUNTRIES,
    });

    map.bubbles(window.CITIES);

    map.options.setProjection = setProjection;

    const resizeHandler = function resizeHandler() {
        map.resize();
        map.bubbles(window.CITIES, { reset: true });
    };

    window.addEventListener('resize', resizeHandler);
    container.__mapInstance = map;
    container.__mapResizeHandler = resizeHandler;
    container.dataset.mapInitialised = 'true';
};
