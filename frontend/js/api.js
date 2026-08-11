const API_BASE = "http://127.0.0.1:8000";

/**
 * Core fetch wrapper with auth header injection and error handling.
 */
async function apiFetch(path, options = {}) {
  const token = localStorage.getItem('auth_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    // Token expired or invalid - log out
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    if (!window.location.pathname.includes('login')) {
      showToast('Session expired. Please log in again.', 'warning');
      setTimeout(() => { window.location.href = 'login.html'; }, 1500);
    }
    throw new Error('Unauthorized');
  }

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const msg = data.detail || data.message || `Error ${res.status}`;
    throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }

  return data;
}

// ===== Auth API =====
const AuthAPI = {
  register: (data) => apiFetch('/api/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => apiFetch('/api/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  me: () => apiFetch('/api/auth/me'),
};

// ===== Products API =====
const ProductsAPI = {
  list: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return apiFetch(`/api/products/?${qs}`);
  },
  get: (id) => apiFetch(`/api/products/${id}`),
  featured: () => apiFetch('/api/products/featured'),
  newArrivals: () => apiFetch('/api/products/new-arrivals'),
  getReviews: (id) => apiFetch(`/api/products/${id}/reviews`),
  addReview: (id, data) => apiFetch(`/api/products/${id}/reviews`, { method: 'POST', body: JSON.stringify(data) }),
};

// ===== Cart API =====
const CartAPI = {
  get: () => apiFetch('/api/cart/'),
  add: (data) => apiFetch('/api/cart/add', { method: 'POST', body: JSON.stringify(data) }),
  update: (product_id, size, color, quantity) => apiFetch(
    `/api/cart/item/${product_id}?size=${encodeURIComponent(size)}&color=${encodeURIComponent(color)}`,
    { method: 'PUT', body: JSON.stringify({ quantity }) }
  ),
  remove: (product_id, size, color) => apiFetch(
    `/api/cart/item/${product_id}?size=${encodeURIComponent(size)}&color=${encodeURIComponent(color)}`,
    { method: 'DELETE' }
  ),
  clear: () => apiFetch('/api/cart/clear', { method: 'DELETE' }),
};

// ===== Wishlist API =====
const WishlistAPI = {
  get: () => apiFetch('/api/wishlist/'),
  add: (id) => apiFetch(`/api/wishlist/add/${id}`, { method: 'POST' }),
  remove: (id) => apiFetch(`/api/wishlist/remove/${id}`, { method: 'DELETE' }),
  check: (id) => apiFetch(`/api/wishlist/check/${id}`),
};

// ===== Orders API =====
const OrdersAPI = {
  createRazorpayOrder: (data) => apiFetch('/api/orders/create-razorpay-order', { method: 'POST', body: JSON.stringify(data) }),
  verifyPayment: (data) => apiFetch('/api/orders/verify-payment', { method: 'POST', body: JSON.stringify(data) }),
  list: () => apiFetch('/api/orders/'),
  get: (id) => apiFetch(`/api/orders/${id}`),
  cancel: (id) => apiFetch(`/api/orders/${id}/cancel`, { method: 'PUT' }),
};
