/**
 * main.js
 * Handles mobile navigation overlay and scroll interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Page Transition: Fade in on load
    // Adding the class triggers the CSS opacity transition from 0 to 1
    document.body.classList.add('page-loaded');

    // --- Mobile Navigation Logic ---
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileOverlay = document.querySelector('.mobile-overlay');

    if (menuToggle && mobileOverlay) {
        menuToggle.addEventListener('click', () => {
            mobileOverlay.classList.toggle('active');

            const icon = menuToggle.querySelector('.menu-icon');
            if (mobileOverlay.classList.contains('active')) {
                icon.style.backgroundColor = 'transparent';
                icon.style.setProperty('--before-transform', 'rotate(45deg) translateY(0)');
                icon.style.setProperty('--after-transform', 'rotate(-45deg) translateY(0)');
            } else {
                icon.style.backgroundColor = 'var(--text-color)';
                icon.style.removeProperty('--before-transform');
                icon.style.removeProperty('--after-transform');
            }
        });
    }

    const mobileLinks = document.querySelectorAll('.mobile-nav-links a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileOverlay.classList.remove('active');
            const icon = menuToggle.querySelector('.menu-icon');
            if (icon) icon.style.backgroundColor = 'var(--text-color)';
        });
    });

    // --- Sticky Navbar Refinement ---
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        // If we scroll down more than 50px, add the scrolled class
        if (window.scrollY > 50) {
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
    });

    // --- Scroll-Triggered Animations ---
    // Select elements to animate. We dynamically add the base animation class.
    const elementsToAnimate = document.querySelectorAll('h1, h2, h3, p:not(.meta), .card, .image-placeholder, .skill-category, .btn, img');

    // Add base class to elements that don't have it yet
    elementsToAnimate.forEach(el => {
        // Exclude elements in the header or overlay to avoid weird initial states
        if (!el.closest('header') && !el.closest('.mobile-overlay') && !el.closest('footer')) {
            el.classList.add('animate-on-scroll');
        }
    });

    // Set up the Intersection Observer
    const observerOptions = {
        root: null, // viewport
        rootMargin: '0px 0px -10% 0px', // Trigger slightly after it enters the bottom of the screen
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add 'is-visible' class to trigger CSS transition
                entry.target.classList.add('is-visible');
                // Unobserve once animated so it doesn't repeat unnecessarily
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with the base class
    const animatableElements = document.querySelectorAll('.animate-on-scroll');
    animatableElements.forEach(el => observer.observe(el));

    // Stagger skills list items
    const skillLists = document.querySelectorAll('.skill-category ul');
    skillLists.forEach(ul => {
        const items = ul.querySelectorAll('li');
        items.forEach((li, index) => {
            // Add the class if not already added
            li.classList.add('animate-on-scroll');
            // Stagger the transition delay based on index
            li.style.transitionDelay = `${index * 0.1}s`;
            observer.observe(li);
        });
    });

    // --- Carousel Center Active Logic ---
    const carousel = document.querySelector('.carousel');
    const carouselItems = document.querySelectorAll('.carousel-item');

    if (carousel && carouselItems.length > 0) {
        const updateActiveItem = () => {
            const carouselCenter = carousel.getBoundingClientRect().left + carousel.clientWidth / 2;
            let closestItem = null;
            let minDistance = Infinity;

            carouselItems.forEach(item => {
                const itemRect = item.getBoundingClientRect();
                const itemCenter = itemRect.left + itemRect.width / 2;
                const distance = Math.abs(carouselCenter - itemCenter);

                if (distance < minDistance) {
                    minDistance = distance;
                    closestItem = item;
                }
                item.classList.remove('active');
            });

            if (closestItem) {
                closestItem.classList.add('active');
            }
        };

        carousel.addEventListener('scroll', updateActiveItem);
        window.addEventListener('resize', updateActiveItem);

        // Ensure it runs after layout
        setTimeout(updateActiveItem, 100);
        setTimeout(updateActiveItem, 500);
    }
});
