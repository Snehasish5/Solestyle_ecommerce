// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'info', duration = 3500) {
  const container = document.getElementById('toast-container') || createToastContainer();

  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: 'ℹ️',
  };

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type] || icons.info}</span>
    <span class="toast-message">${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('toast-out');
    toast.addEventListener('animationend', () => toast.remove());
  }, duration);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  document.body.appendChild(container);
  return container;
}

// ===== AUTH HELPERS =====
function getToken() {
  return localStorage.getItem('auth_token');
}

function getUser() {
  const u = localStorage.getItem('user');
  return u ? JSON.parse(u) : null;
}

function isLoggedIn() {
  return !!getToken();
}

function saveAuth(token, user) {
  localStorage.setItem('auth_token', token);
  localStorage.setItem('user', JSON.stringify(user));
}

function clearAuth() {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user');
}

function requireAuth(redirectTo = 'login.html') {
  if (!isLoggedIn()) {
    sessionStorage.setItem('redirect_after_login', window.location.href);
    window.location.href = redirectTo;
    return false;
  }
  return true;
}

// ===== FORMAT HELPERS =====
function formatPrice(amount) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
  }).format(amount);
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function getDiscountPercent(original, current) {
  if (!original || original <= current) return 0;
  return Math.round(((original - current) / original) * 100);
}

// ===== STARS =====
function renderStars(rating, showCount = false, count = 0) {
  const full = Math.floor(rating);
  const hasHalf = rating % 1 >= 0.5;
  let html = '<span class="stars">';
  for (let i = 1; i <= 5; i++) {
    if (i <= full) html += '★';
    else if (i === full + 1 && hasHalf) html += '½';
    else html += '<span class="star-empty">★</span>';
  }
  html += '</span>';
  if (showCount) html += ` <span style="color:var(--text-muted);font-size:0.8em">(${count})</span>`;
  return html;
}

// ===== FALLBACK IMAGE =====
const FALLBACK_SHOE_IMAGE = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'%3E%3Crect width='400' height='400' fill='%2312121f'/%3E%3Ctext x='50%25' y='42%25' dominant-baseline='middle' text-anchor='middle' font-size='72'%3E👟%3C/text%3E%3Ctext x='50%25' y='65%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-weight='bold' font-size='16' fill='%23a855f7'%3ESoleStyle Footwear%3C/text%3E%3C/svg%3E";

// ===== PRODUCT CARD =====
function createProductCard(product) {
  const discount = getDiscountPercent(product.original_price, product.price);
  const isWishlisted = getWishlistIds().includes(product.id);
  const imgUrl = (product.images && product.images.length > 0 && product.images[0]) ? product.images[0] : FALLBACK_SHOE_IMAGE;

  return `
    <div class="product-card" data-id="${product.id}">
      <div class="product-card-image">
        <a href="product-detail.html?id=${product.id}">
          <img src="${imgUrl}"
               alt="${product.name}"
               loading="lazy"
               onerror="this.onerror=null;this.src='${FALLBACK_SHOE_IMAGE}'">
        </a>
        <div class="product-card-badges">
          ${discount > 0 ? `<span class="badge badge-sale">${discount}% OFF</span>` : ''}
          ${product.is_new_arrival ? '<span class="badge badge-new">NEW</span>' : ''}
          ${product.is_featured ? '<span class="badge badge-featured">⭐ FEATURED</span>' : ''}
        </div>
        <div class="product-card-actions">
          <button class="product-action-btn wishlist-toggle-btn ${isWishlisted ? 'wishlisted' : ''}"
                  data-id="${product.id}" title="${isWishlisted ? 'Remove from wishlist' : 'Add to wishlist'}">
            ${isWishlisted ? '❤️' : '🤍'}
          </button>
          <a href="product-detail.html?id=${product.id}" class="product-action-btn" title="Quick view">👁️</a>
        </div>
      </div>
      <div class="product-card-body">
        <div class="product-card-brand">${product.brand}</div>
        <div class="product-card-name" title="${product.name}">${product.name}</div>
        <div class="product-card-rating">
          ${renderStars(product.average_rating || 0)}
          <span>${(product.average_rating || 0).toFixed(1)} (${product.review_count || 0})</span>
        </div>
        <div class="product-card-footer">
          <div class="price-group">
            <span class="price-current">${formatPrice(product.price)}</span>
            ${product.original_price ? `<span class="price-original">${formatPrice(product.original_price)}</span>` : ''}
          </div>
          <button class="product-card-add-btn quick-add-btn"
                  data-id="${product.id}"
                  data-name="${product.name}"
                  title="Quick Add to Cart">+</button>
        </div>
      </div>
    </div>
  `;
}

// ===== WISHLIST LOCAL CACHE =====
function getWishlistIds() {
  const w = localStorage.getItem('wishlist_ids');
  return w ? JSON.parse(w) : [];
}

function setWishlistIds(ids) {
  localStorage.setItem('wishlist_ids', JSON.stringify(ids));
}

async function syncWishlistIds() {
  if (!isLoggedIn()) return;
  try {
    const data = await WishlistAPI.get();
    const ids = data.products.map(p => p.id);
    setWishlistIds(ids);
  } catch {}
}

async function toggleWishlist(productId, btn) {
  if (!requireAuth()) return;
  const ids = getWishlistIds();
  const isIn = ids.includes(productId);
  try {
    if (isIn) {
      await WishlistAPI.remove(productId);
      setWishlistIds(ids.filter(i => i !== productId));
      btn.classList.remove('wishlisted');
      btn.innerHTML = '🤍';
      btn.title = 'Add to wishlist';
      showToast('Removed from wishlist', 'info');
    } else {
      await WishlistAPI.add(productId);
      setWishlistIds([...ids, productId]);
      btn.classList.add('wishlisted');
      btn.innerHTML = '❤️';
      btn.title = 'Remove from wishlist';
      showToast('Added to wishlist! ❤️', 'success');
    }
    updateWishlistBadge();
  } catch (e) {
    showToast(e.message, 'error');
  }
}

// ===== CART COUNT BADGE =====
async function updateCartBadge() {
  const badge = document.getElementById('cart-badge');
  if (!badge || !isLoggedIn()) return;
  try {
    const data = await CartAPI.get();
    badge.textContent = data.total_items || 0;
    badge.style.display = data.total_items > 0 ? 'flex' : 'none';
  } catch {}
}

function updateWishlistBadge() {
  const badge = document.getElementById('wishlist-badge');
  if (!badge) return;
  const count = getWishlistIds().length;
  badge.textContent = count;
  badge.style.display = count > 0 ? 'flex' : 'none';
}

// ===== URL PARAMS =====
function getParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

// ===== DEBOUNCE =====
function debounce(fn, delay = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}
