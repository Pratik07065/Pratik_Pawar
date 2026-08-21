/* ==========================================================================
   Pratik Pawar Portfolio - Main JS Architecture & GSAP Animations
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide Icons
  if (window.lucide) {
    lucide.createIcons();
  }

  // 1. Scroll Progress Bar & Back to Top
  const progressBar = document.getElementById('scroll-progress');
  const backToTopBtn = document.getElementById('back-to-top');

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (window.scrollY / totalHeight) * 100;
    if (progressBar) {
      progressBar.style.width = `${progress}%`;
    }

    if (backToTopBtn) {
      if (window.scrollY > 400) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    }
  });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // 2. Custom Cursor (Desktop Only)
  if (window.innerWidth > 1024) {
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    const follower = document.createElement('div');
    follower.className = 'custom-cursor-follower';

    document.body.appendChild(cursor);
    document.body.appendChild(follower);

    let mouseX = 0, mouseY = 0;
    let followerX = 0, followerY = 0;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.left = `${mouseX}px`;
      cursor.style.top = `${mouseY}px`;
    });

    function animateCursor() {
      followerX += (mouseX - followerX) * 0.15;
      followerY += (mouseY - followerY) * 0.15;
      follower.style.left = `${followerX}px`;
      follower.style.top = `${followerY}px`;
      requestAnimationFrame(animateCursor);
    }
    animateCursor();

    const hoverableElements = document.querySelectorAll('a, button, .glass-card, .filter-btn, .project-card');
    hoverableElements.forEach(el => {
      el.addEventListener('mouseenter', () => document.body.classList.add('hovered'));
      el.addEventListener('mouseleave', () => document.body.classList.remove('hovered'));
    });
  }

  // 3. Navbar Blur on Scroll
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // 4. Mobile Navigation Toggle
  const navToggle = document.getElementById('nav-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  const mobileBackdrop = document.getElementById('mobile-backdrop');
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');

  function toggleMobileNav() {
    mobileNav.classList.toggle('open');
    mobileBackdrop.classList.toggle('active');
  }

  if (navToggle) {
    navToggle.addEventListener('click', toggleMobileNav);
  }
  if (mobileBackdrop) {
    mobileBackdrop.addEventListener('click', toggleMobileNav);
  }
  mobileLinks.forEach(link => {
    link.addEventListener('click', toggleMobileNav);
  });

  // 5. Particle Canvas Animation
  const canvas = document.getElementById('particles-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let particles = [];
    
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    class Particle {
      constructor() {
        this.reset();
      }
      reset() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 0.5;
        this.speedX = (Math.random() - 0.5) * 0.4;
        this.speedY = (Math.random() - 0.5) * 0.4;
        this.opacity = Math.random() * 0.5 + 0.2;
      }
      update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
          this.reset();
        }
      }
      draw() {
        ctx.fillStyle = `rgba(124, 92, 255, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    const particleCount = Math.min(Math.floor(window.innerWidth / 15), 80);
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    function animateParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(p => {
        p.update();
        p.draw();
      });
      requestAnimationFrame(animateParticles);
    }
    animateParticles();
  }

  // 6. Skill Category Filter
  const filterBtns = document.querySelectorAll('.filter-btn');
  const skillCards = document.querySelectorAll('.skill-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');
      skillCards.forEach(card => {
        if (filter === 'all' || card.getAttribute('data-category') === filter) {
          card.style.display = 'flex';
          gsap.fromTo(card, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.3, clearProps: 'opacity,transform' });
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // 7. Project Detail Modal Handler
  const modalOverlay = document.getElementById('project-modal');
  const modalContainer = document.getElementById('modal-content');
  const modalCloseBtn = document.getElementById('modal-close');

  function openProjectModal(slug) {
    if (!modalOverlay || !modalContainer) return;
    
    modalContainer.innerHTML = '<div style="text-align: center; padding: 50px;"><div class="pulse-dot" style="margin: 0 auto 20px auto;"></div><p style="color: var(--text-muted);">Loading project details...</p></div>';
    modalOverlay.classList.add('active');

    fetch(`/projects/${slug}/`, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(res => res.json())
    .then(data => {
      let techPills = data.technologies.map(t => `<span class="tech-tag">${t}</span>`).join('');
      let featureItems = data.features.map(f => `<li style="margin-bottom: 8px; color: var(--text-muted);"><span style="color: var(--accent-secondary); margin-right: 8px;">✓</span>${f}</li>`).join('');
      let statBoxes = data.statistics.map(s => `
        <div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: var(--radius-md); text-align: center;">
          <div style="font-size: 1.4rem; font-weight: 700; color: var(--accent-secondary);">${s.value}</div>
          <div style="font-size: 0.8rem; color: var(--text-muted);">${s.label}</div>
        </div>
      `).join('');

      let linksHtml = '';
      if (data.github_url) {
        linksHtml += `<a href="${data.github_url}" target="_blank" rel="noopener" class="btn btn-outline"><i data-lucide="github"></i> View GitHub Repo</a>`;
      }
      if (data.live_demo_url) {
        linksHtml += `<a href="${data.live_demo_url}" target="_blank" rel="noopener" class="btn btn-primary"><i data-lucide="external-link"></i> Live Demo</a>`;
      }

      modalContainer.innerHTML = `
        <div style="margin-bottom: 24px;">
          <span class="section-badge">${data.category}</span>
          <h2 style="font-size: 2.2rem; margin-top: 10px; margin-bottom: 16px;">${data.title}</h2>
          <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px;">${techPills}</div>
        </div>

        ${statBoxes ? `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 16px; margin-bottom: 30px;">${statBoxes}</div>` : ''}

        <div style="margin-bottom: 30px;">
          <h3 style="font-size: 1.2rem; margin-bottom: 10px; color: var(--accent-secondary);">Overview & Solution</h3>
          <p style="color: var(--text-muted); line-height: 1.7;">${data.detailed_description || data.short_description}</p>
        </div>

        ${data.problem_statement ? `
        <div style="margin-bottom: 30px;">
          <h3 style="font-size: 1.2rem; margin-bottom: 10px; color: var(--accent-primary);">Problem Statement</h3>
          <p style="color: var(--text-muted); line-height: 1.7;">${data.problem_statement}</p>
        </div>` : ''}

        ${featureItems ? `
        <div style="margin-bottom: 30px;">
          <h3 style="font-size: 1.2rem; margin-bottom: 12px; color: var(--accent-secondary);">Key Features & Capabilities</h3>
          <ul style="list-style: none; padding-left: 0;">${featureItems}</ul>
        </div>` : ''}

        <div style="display: flex; gap: 16px; margin-top: 40px; flex-wrap: wrap;">
          ${linksHtml}
        </div>
      `;

      if (window.lucide) {
        lucide.createIcons();
      }
    })
    .catch(err => {
      modalContainer.innerHTML = '<p style="color: #ff5555;">Failed to load project details.</p>';
    });
  }

  document.querySelectorAll('.view-project-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const slug = btn.getAttribute('data-slug');
      openProjectModal(slug);
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
    });
  }
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
      }
    });
  }

  // 8. Robust GSAP Animations & ScrollTrigger with clearProps
  if (typeof gsap !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    // Hero Entrance
    gsap.fromTo('.hero-content > *', 
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 1, stagger: 0.12, ease: 'power3.out', clearProps: 'opacity,transform' }
    );

    gsap.fromTo('.avatar-wrapper', 
      { opacity: 0, scale: 0.8 },
      { opacity: 1, scale: 1, duration: 1.2, ease: 'back.out(1.7)', delay: 0.2, clearProps: 'opacity,transform' }
    );

    // Section Reveals (Safe fromTo with clearProps)
    const sections = document.querySelectorAll('.section-reveal');
    sections.forEach(sec => {
      gsap.fromTo(sec, 
        { opacity: 0, y: 40 },
        {
          scrollTrigger: {
            trigger: sec,
            start: 'top 88%',
            toggleActions: 'play none none none'
          },
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: 'power3.out',
          clearProps: 'opacity,transform'
        }
      );
    });

    // Scoped Grid Card Animations (Each Grid Animates Its Own Cards)
    document.querySelectorAll('.projects-grid, .certs-grid, .skills-grid, .achievements-grid').forEach(grid => {
      const cards = grid.querySelectorAll('.glass-card, .skill-card, .project-card, .achievement-card');
      if (cards.length > 0) {
        gsap.fromTo(cards, 
          { opacity: 0, y: 30 },
          {
            scrollTrigger: {
              trigger: grid,
              start: 'top 88%',
              toggleActions: 'play none none none'
            },
            opacity: 1,
            y: 0,
            duration: 0.6,
            stagger: 0.08,
            ease: 'power2.out',
            clearProps: 'opacity,transform'
          }
        );
      }
    });

    // Metric Counter Animation
    document.querySelectorAll('.count-up').forEach(counter => {
      const targetStr = counter.getAttribute('data-count');
      const target = parseFloat(targetStr);
      if (!isNaN(target)) {
        ScrollTrigger.create({
          trigger: counter,
          start: 'top 88%',
          onEnter: () => {
            let obj = { val: 0 };
            gsap.to(obj, {
              val: target,
              duration: 2,
              ease: 'power1.out',
              onUpdate: () => {
                counter.innerText = Math.floor(obj.val) + (targetStr.includes('%') ? '%' : (targetStr.includes('+') ? '+' : ''));
              }
            });
          }
        });
      }
    });

    // Refresh ScrollTrigger after window load and direct hash navigation
    window.addEventListener('load', () => {
      ScrollTrigger.refresh();
    });
  }

  // Safety Fallback: Ensure all elements are visible if JS execution/ScrollTrigger miscalculates
  setTimeout(() => {
    document.querySelectorAll('.section-reveal, .glass-card, .project-card, .skill-card').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight + 100) {
        el.style.opacity = '1';
        el.style.transform = 'none';
      }
    });
    if (typeof ScrollTrigger !== 'undefined') {
      ScrollTrigger.refresh();
    }
  }, 400);
});
