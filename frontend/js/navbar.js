// ===== NAVBAR INITIALIZATION =====
function initNavbar() {
  // Scroll effect
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // Active link highlight
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Hamburger menu
  const hamburger = document.getElementById('nav-hamburger');
  const mobileMenu = document.getElementById('nav-mobile');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      mobileMenu.classList.toggle('open');
    });
    // Close mobile menu on link click
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        hamburger.classList.remove('open');
        mobileMenu.classList.remove('open');
      });
    });
  }

  // Search
  const searchInput = document.getElementById('nav-search-input');
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && searchInput.value.trim()) {
        window.location.href = `products.html?search=${encodeURIComponent(searchInput.value.trim())}`;
      }
    });
  }

  // User state
  renderUserNav();

  // Badges
  updateCartBadge();
  updateWishlistBadge();
  if (isLoggedIn()) syncWishlistIds().then(() => updateWishlistBadge());
}

function renderUserNav() {
  const userArea = document.getElementById('nav-user-area');
  if (!userArea) return;
  const user = getUser();

  if (user) {
    const initials = user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    userArea.innerHTML = `
      <div class="nav-user-menu" id="nav-user-menu">
        <button class="nav-user-btn" id="nav-user-btn">
          <div class="nav-user-avatar">${initials}</div>
          <span>${user.name.split(' ')[0]}</span>
          <span>▾</span>
        </button>
        <div class="nav-dropdown">
          <div class="nav-dropdown-item" style="color:var(--text-muted);font-size:0.75rem;cursor:default">${user.email}</div>
          <div class="nav-dropdown-divider"></div>
          <a href="orders.html" class="nav-dropdown-item">My Orders</a>
          <a href="wishlist.html" class="nav-dropdown-item">Wishlist</a>
          <div class="nav-dropdown-divider"></div>
          <div class="nav-dropdown-item" id="logout-btn" style="color:var(--error)">Sign Out</div>
        </div>
      </div>
    `;

    document.getElementById('logout-btn')?.addEventListener('click', () => {
      clearAuth();
      setWishlistIds([]);
      showToast('Signed out successfully', 'info');
      setTimeout(() => window.location.href = 'index.html', 1000);
    });

    const menu = document.getElementById('nav-user-menu');
    const btn = document.getElementById('nav-user-btn');
    btn?.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.classList.toggle('open');
    });
    document.addEventListener('click', () => menu?.classList.remove('open'));

  } else {
    userArea.innerHTML = `
      <div class="nav-auth-btns">
        <a href="login.html" class="btn btn-secondary btn-sm">Sign In</a>
        <a href="register.html" class="btn btn-primary btn-sm">Sign Up</a>
      </div>
    `;
  }
}
