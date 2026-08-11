const API_BASE = "https://solestyle-ecommerce-two.vercel.app/api";

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
  register: (data) => apiFetch('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => apiFetch('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  me: () => apiFetch('/auth/me'),
};

// ===== Products API =====
const ProductsAPI = {
  list: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return apiFetch(`/products/?${qs}`);
  },
  get: (id) => apiFetch(`/products/${id}`),
  featured: () => apiFetch('/products/featured'),
  newArrivals: () => apiFetch('/products/new-arrivals'),
  getReviews: (id) => apiFetch(`/products/${id}/reviews`),
  addReview: (id, data) => apiFetch(`/products/${id}/reviews`, { method: 'POST', body: JSON.stringify(data) }),
};

// ===== Cart API =====
const CartAPI = {
  get: () => apiFetch('/cart/'),
  add: (data) => apiFetch('/cart/add', { method: 'POST', body: JSON.stringify(data) }),
  update: (product_id, size, color, quantity) => apiFetch(
    `/cart/item/${product_id}?size=${encodeURIComponent(size)}&color=${encodeURIComponent(color)}`,
    { method: 'PUT', body: JSON.stringify({ quantity }) }
  ),
  remove: (product_id, size, color) => apiFetch(
    `/cart/item/${product_id}?size=${encodeURIComponent(size)}&color=${encodeURIComponent(color)}`,
    { method: 'DELETE' }
  ),
  clear: () => apiFetch('/cart/clear', { method: 'DELETE' }),
};

// ===== Wishlist API =====
const WishlistAPI = {
  get: () => apiFetch('/wishlist/'),
  add: (id) => apiFetch(`/wishlist/add/${id}`, { method: 'POST' }),
  remove: (id) => apiFetch(`/wishlist/remove/${id}`, { method: 'DELETE' }),
  check: (id) => apiFetch(`/wishlist/check/${id}`),
};

// ===== Orders API =====
const OrdersAPI = {
  createRazorpayOrder: (data) => apiFetch('/orders/create-razorpay-order', { method: 'POST', body: JSON.stringify(data) }),
  verifyPayment: (data) => apiFetch('/orders/verify-payment', { method: 'POST', body: JSON.stringify(data) }),
  list: () => apiFetch('/orders/'),
  get: (id) => apiFetch(`/orders/${id}`),
  cancel: (id) => apiFetch(`/orders/${id}/cancel`, { method: 'PUT' }),
};
