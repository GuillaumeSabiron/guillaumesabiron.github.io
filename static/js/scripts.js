/*!
* Start Bootstrap - Resume v7.0.6 (https://startbootstrap.com/theme/resume)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-resume/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

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
