document.addEventListener('DOMContentLoaded', () => {
    if ('scrollRestoration' in history) {
        history.scrollRestoration = 'manual';
    }
    window.addEventListener('load', () => {
        window.scrollTo(0, 0);
    });

    const openingOverlay = document.getElementById('opening-overlay');
    const openingLogo = document.getElementById('opening-logo');
    const mainContent = document.getElementById('main-content');
    const heroCatchphraseElement = document.querySelector('.hero-catchphrase');
    const hamburgerButton = document.querySelector('.hamburger-button');
    const fullscreenNav = document.querySelector('.fullscreen-nav');
    const navLiElements = document.querySelectorAll('.fullscreen-nav-links li');
    const fullscreenNavLinks = document.querySelectorAll('.fullscreen-nav-link');
    const scrollToTopBtn = document.getElementById('scrollToTopBtn');
    const scrollHeader = document.querySelector('.scroll-header');
    const scrollTriggers = document.querySelectorAll('.js-scroll-trigger');
    const currentYearCopyrightSpan = document.getElementById('current-year-copyright');

    function handleOpeningAnimation() {
        if (!openingOverlay || !openingLogo || !mainContent) {
            if(mainContent) mainContent.style.opacity = '1';
            if(openingOverlay) openingOverlay.style.display = 'none';
            return;
        }
        setTimeout(() => { openingLogo.style.opacity = '1'; }, 100);
        setTimeout(() => {
            openingOverlay.style.opacity = '0';
            setTimeout(() => {
                openingOverlay.style.display = 'none';
                mainContent.style.opacity = '1';
                if (heroCatchphraseElement) {
                    setTimeout(startCatchphraseAnimation, 500);
                }
            }, 500);
        }, 1800);
    }

    function startCatchphraseAnimation() {
        if (!heroCatchphraseElement || heroCatchphraseElement.classList.contains('animated-started')) return;
        heroCatchphraseElement.style.visibility = 'visible';
        heroCatchphraseElement.classList.add('animated-started');
        let originalHTML = heroCatchphraseElement.innerHTML;
        let newHTML = '';
        let isTag = false;
        for (let i = 0; i < originalHTML.length; i++) {
            const char = originalHTML[i];
            if (char === '<') isTag = true;
            if (isTag) {
                newHTML += char;
            } else {
                if (char.trim() === '') {
                    newHTML += char;
                } else {
                    newHTML += `<span>${char}</span>`;
                }
            }
            if (char === '>') isTag = false;
        }
        heroCatchphraseElement.innerHTML = newHTML;
        heroCatchphraseElement.querySelectorAll('span').forEach((span, index) => {
            span.style.animationDelay = `${index * 0.07}s`;
        });
        heroCatchphraseElement.classList.add('animated');
    }

    function toggleMenu() {
        if (!hamburgerButton || !fullscreenNav || !navLiElements) return;
        const isOpen = fullscreenNav.classList.contains('is-open');
        const backgroundDelay = isOpen ? (navLiElements.length - 1) * 0.08 : 0;
        fullscreenNav.style.transitionDelay = `${backgroundDelay}s`;
        navLiElements.forEach((li, index) => {
            const delay = isOpen ? (navLiElements.length - 1 - index) * 0.08 : index * 0.08;
            li.style.transitionDelay = `${delay}s`;
        });
        hamburgerButton.classList.toggle('is-active');
        fullscreenNav.classList.toggle('is-open');
        document.body.classList.toggle('no-scroll');
    }

    function handleNavLinkClick(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (!targetId.startsWith('#')) return;
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            const offset = 0;
            const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top: targetPosition, behavior: 'smooth' });
        }
    }

    function handleScroll() {
        if (scrollToTopBtn) {
            if (window.scrollY > 200) { scrollToTopBtn.classList.add('show'); }
            else { scrollToTopBtn.classList.remove('show'); }
        }
        if (scrollHeader) {
            if (window.scrollY > 1) {
                scrollHeader.style.top = '0';
            } else {
                scrollHeader.style.top = `calc(-1 * ${getComputedStyle(scrollHeader).height} - 10px)`;
            }
        }
    }

    if (scrollTriggers.length > 0) {
        const observerOptions = { root: null, rootMargin: '0px', threshold: 0.1 };
        const observerCallback = (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-active');
                    observer.unobserve(entry.target);
                }
            });
        };
        const scrollObserver = new IntersectionObserver(observerCallback, observerOptions);
        scrollTriggers.forEach(trigger => scrollObserver.observe(trigger));
    }

    handleOpeningAnimation();

    if (hamburgerButton && fullscreenNav) {
        hamburgerButton.addEventListener('click', toggleMenu);
    }
    
    if (fullscreenNavLinks.length > 0) {
        fullscreenNavLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                if (fullscreenNav.classList.contains('is-open')) {
                    toggleMenu();
                }
                setTimeout(() => {
                    handleNavLinkClick.call(this, e);
                }, 400); 
            });
        });
    }
    
    window.addEventListener('scroll', handleScroll);
    
    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener('click', () => { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    }
    
    if (currentYearCopyrightSpan) {
        currentYearCopyrightSpan.textContent = new Date().getFullYear();
    }
});