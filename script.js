/**
 * Portfolio Website - JavaScript
 * Author: Niels van Meijel
 */

// ============================================
// PROJECT DATA
// ============================================
const projects = [
  {
    title: "Airbus Fuel Leak Anomaly Detection",
    description: "Capstone project developing machine learning models to detect fuel system anomalies in aircraft using sensor data and time-series analysis.",
    tags: ["Python", "Machine Learning", "Time Series", "Anomaly Detection"],
    url: "https://github.com/nielsmeijel/capstone.airbus",
    featured: true
  },
  {
    title: "AirBnB Pricing Visualizations",
    description: "Interactive data visualizations exploring pricing patterns and factors influencing AirBnB listings across different markets.",
    tags: ["Python", "Data Visualization", "Pandas", "Matplotlib"],
    url: "https://github.com/nielsmeijel/", // TODO: Update with actual repository URL
    featured: false
  },
  {
    title: "Employee Attrition Classification",
    description: "Predictive modeling project to identify employees at risk of leaving, using classification algorithms and HR analytics.",
    tags: ["Python", "Classification", "Scikit-learn", "HR Analytics"],
    url: "https://github.com/nielsmeijel/", // TODO: Update with actual repository URL
    featured: false
  },
  {
    title: "Credit Card Fraud Classification",
    description: "Building robust fraud detection models using imbalanced learning techniques and ensemble methods on transaction data.",
    tags: ["Python", "Fraud Detection", "Imbalanced Learning", "SQL"],
    url: "https://github.com/nielsmeijel/", // TODO: Update with actual repository URL
    featured: true
  },
  {
    title: "Daily Recipe Web Scraper",
    description: "Automated web scraper that collects and organizes recipes from popular cooking websites into a structured database.",
    tags: ["Python", "Web Scraping", "BeautifulSoup", "Automation"],
    url: "https://github.com/nielsmeijel/", // TODO: Update with actual repository URL
    featured: false
  }
];

// ============================================
// DOM ELEMENTS
// ============================================
const body = document.body;
const navToggle = document.querySelector('.nav__toggle');
const navLinks = document.querySelector('.nav__links');
const themeToggle = document.querySelector('.theme-toggle');
const searchInput = document.querySelector('.projects__search-input');
const tagFilters = document.querySelectorAll('.tag-filter');
const projectsGrid = document.querySelector('.projects__grid');
const contactForm = document.querySelector('.contact-form');
const toast = document.querySelector('.toast');
const toastClose = document.querySelector('.toast__close');
const navLinkElements = document.querySelectorAll('.nav__link');

// ============================================
// THEME TOGGLE
// ============================================
function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  } else if (prefersDark) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
}

// ============================================
// MOBILE NAVIGATION
// ============================================
function toggleMobileNav() {
  navLinks.classList.toggle('open');
  
  // Update aria-expanded
  const isOpen = navLinks.classList.contains('open');
  navToggle.setAttribute('aria-expanded', isOpen);
}

function closeMobileNav() {
  navLinks.classList.remove('open');
  navToggle.setAttribute('aria-expanded', 'false');
}

// ============================================
// SCROLLSPY
// ============================================
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  
  const observerOptions = {
    rootMargin: '-20% 0px -80% 0px',
    threshold: 0
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        
        navLinkElements.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }, observerOptions);
  
  sections.forEach(section => observer.observe(section));
}

// ============================================
// REVEAL ANIMATIONS
// ============================================
function initRevealAnimations() {
  const revealElements = document.querySelectorAll('.reveal');
  
  const observerOptions = {
    rootMargin: '0px 0px -100px 0px',
    threshold: 0.1
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  revealElements.forEach(element => observer.observe(element));
}

// ============================================
// PROJECTS RENDERING & FILTERING
// ============================================
let activeTag = 'All';
let searchQuery = '';

function getAllTags() {
  const tagSet = new Set();
  projects.forEach(project => {
    project.tags.forEach(tag => tagSet.add(tag));
  });
  return Array.from(tagSet).sort();
}

function filterProjects() {
  let filtered = [...projects];
  
  // Filter by search query
  if (searchQuery) {
    const query = searchQuery.toLowerCase();
    filtered = filtered.filter(project => 
      project.title.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query) ||
      project.tags.some(tag => tag.toLowerCase().includes(query))
    );
  }
  
  // Filter by tag
  if (activeTag !== 'All') {
    filtered = filtered.filter(project => 
      project.tags.some(tag => tag.toLowerCase() === activeTag.toLowerCase())
    );
  }
  
  // Sort: featured first
  filtered.sort((a, b) => {
    if (a.featured && !b.featured) return -1;
    if (!a.featured && b.featured) return 1;
    return 0;
  });
  
  return filtered;
}

function renderProjects() {
  const filtered = filterProjects();
  
  if (filtered.length === 0) {
    projectsGrid.innerHTML = `
      <div class="projects__empty">
        <p>No projects found matching your criteria.</p>
      </div>
    `;
    return;
  }
  
  projectsGrid.innerHTML = filtered.map((project, index) => `
    <article class="project-card reveal ${project.featured ? 'featured' : ''}" style="--index: ${index}">
      ${project.featured ? `
        <span class="project-card__featured">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          Featured
        </span>
      ` : ''}
      <h3 class="project-card__title">${project.title}</h3>
      <p class="project-card__description">${project.description}</p>
      <div class="project-card__tags">
        ${project.tags.map(tag => `<span class="project-card__tag">${tag}</span>`).join('')}
      </div>
      <a href="${project.url}" target="_blank" rel="noopener noreferrer" class="project-card__link" aria-label="Open ${project.title} repository">
        Open repository
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
          <polyline points="15 3 21 3 21 9"/>
          <line x1="10" y1="14" x2="21" y2="3"/>
        </svg>
      </a>
    </article>
  `).join('');
  
  // Re-initialize reveal animations for new cards
  setTimeout(() => {
    const newCards = projectsGrid.querySelectorAll('.project-card.reveal');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -50px 0px', threshold: 0.1 });
    
    newCards.forEach(card => observer.observe(card));
  }, 10);
}

function handleSearch(e) {
  searchQuery = e.target.value.trim();
  renderProjects();
}

function handleTagFilter(e) {
  const button = e.target.closest('.tag-filter');
  if (!button) return;
  
  activeTag = button.dataset.tag;
  
  tagFilters.forEach(btn => {
    btn.classList.remove('active');
    btn.setAttribute('aria-pressed', 'false');
  });
  button.classList.add('active');
  button.setAttribute('aria-pressed', 'true');
  
  renderProjects();
}

// ============================================
// CONTACT FORM & TOAST
// ============================================
function showToast() {
  toast.classList.add('show');
  
  // Auto-hide after 5 seconds
  setTimeout(hideToast, 5000);
}

function hideToast() {
  toast.classList.remove('show');
}

function handleContactSubmit(e) {
  e.preventDefault();
  showToast();
  e.target.reset();
}

// ============================================
// EVENT LISTENERS
// ============================================
function initEventListeners() {
  // Theme toggle
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }
  
  // Mobile nav toggle
  if (navToggle) {
    navToggle.addEventListener('click', toggleMobileNav);
  }
  
  // Close mobile nav on link click
  navLinkElements.forEach(link => {
    link.addEventListener('click', closeMobileNav);
  });
  
  // Close mobile nav on outside click
  document.addEventListener('click', (e) => {
    if (navLinks.classList.contains('open') && 
        !navLinks.contains(e.target) && 
        !navToggle.contains(e.target)) {
      closeMobileNav();
    }
  });
  
  // Search input
  if (searchInput) {
    searchInput.addEventListener('input', handleSearch);
  }
  
  // Tag filters
  tagFilters.forEach(button => {
    button.addEventListener('click', handleTagFilter);
  });
  
  // Contact form
  if (contactForm) {
    contactForm.addEventListener('submit', handleContactSubmit);
  }
  
  // Toast close
  if (toastClose) {
    toastClose.addEventListener('click', hideToast);
  }
  
  // Keyboard navigation for toast
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && toast.classList.contains('show')) {
      hideToast();
    }
  });
}

// ============================================
// INITIALIZATION
// ============================================
function init() {
  initTheme();
  renderProjects();
  initEventListeners();
  initScrollSpy();
  initRevealAnimations();
}

// Run when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
