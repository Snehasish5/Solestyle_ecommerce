# SoleStyle — Shoe E-Commerce Platform

A full-stack, premium e-commerce web application for shoes built with **Vanilla HTML/CSS/JavaScript**, **FastAPI**, **MongoDB Atlas**, and **Razorpay Payments**.

---

## 📸 Features

| Feature | Description |
|---|---|
| 🔐 **Secure Auth** | JWT-based login & registration with bcrypt password hashing |
| 🛍️ **Product Catalog** | Browse, search, filter and sort shoes |
| ❤️ **Wishlist** | Save products for later |
| 🛒 **Cart** | Add, update quantity, remove items |
| 💳 **Razorpay Checkout** | Secure payment with signature verification |
| 📦 **Order Management** | View order history and cancel orders |
| ⭐ **Reviews** | Star ratings and written reviews |
| 🗄️ **MongoDB Atlas** | Cloud-hosted database with indexing |
| 📱 **Responsive** | Fully responsive dark-themed UI |

---

## 🏗️ Project Structure

```
E-commerce/
├── backend/                    # FastAPI application
│   ├── main.py                 # App entry point, CORS, routers
│   ├── config.py               # Environment settings (pydantic-settings)
│   ├── database.py             # Motor async MongoDB connection + indexes
│   ├── seed.py                 # Populates DB with 12 sample shoes + demo user
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (not committed to git)
│   ├── models/                 # Pydantic request/response models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   ├── routes/                 # API route handlers
│   │   ├── auth.py             # /api/auth — register, login, /me
│   │   ├── products.py         # /api/products — CRUD, search, reviews
│   │   ├── cart.py             # /api/cart — add, update, remove, clear
│   │   ├── wishlist.py         # /api/wishlist — add, remove, list
│   │   └── orders.py           # /api/orders — place, verify, list, cancel
│   └── utils/
│       └── security.py         # bcrypt hashing + JWT helpers
│
└── frontend/                   # Static HTML/CSS/JS site
    ├── index.html              # Homepage — hero, featured shoes, new arrivals
    ├── products.html           # Shop listing — filters, sorting, pagination
    ├── product-detail.html     # Product page — gallery, size/color, reviews
    ├── cart.html               # Shopping cart
    ├── checkout.html           # Checkout — address form + Razorpay modal
    ├── orders.html             # Order history
    ├── wishlist.html           # Saved shoes
    ├── login.html              # Sign in
    ├── register.html           # Create account
    ├── contact.html            # Contact page
    ├── faq.html                # FAQ page
    ├── privacy-policy.html     # Privacy policy
    ├── returns.html            # Returns policy
    ├── shipping-policy.html    # Shipping policy
    ├── terms-of-service.html   # Terms of service
    ├── css/
    │   ├── global.css          # Design tokens, layout, buttons, badges, forms
    │   ├── navbar.css          # Navigation bar styles
    │   └── components.css      # Product cards, cart items, order cards etc.
    └── js/
        ├── api.js              # Fetch wrapper + all API methods (Auth/Cart/etc.)
        ├── utils.js            # Helpers: formatPrice, renderStars, createProductCard
        └── navbar.js           # Navbar controller — badges, search, user area
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI 0.116, Uvicorn 0.35 |
| **Database** | MongoDB Atlas (Motor 3.7 async driver) |
| **Auth** | JWT (`python-jose`) + bcrypt (`passlib`) |
| **Payments** | Razorpay SDK 2.0 — server-side order + HMAC signature verify |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (ES2020) |
| **Design** | Dark glassmorphism theme, CSS variables, responsive grid |
| **Validation** | Pydantic v2 |
| **Config** | `pydantic-settings` + `.env` file |

---

## ⚙️ Prerequisites

- **Python 3.11+**
- **MongoDB Atlas** account (free tier works perfectly)
- **Razorpay** account with API key + secret
- A static file server to serve `frontend/` (VS Code Live Server or Python `http.server`)

---

## 🚀 Setup & Running

### 1. Clone the Repository

```bash
git clone <repo-url>
cd E-commerce
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # PowerShell
# OR
.\.venv\Scripts\activate.bat        # Command Prompt
```

### 3. Install Backend Dependencies

```powershell
pip install -r backend\requirements.txt
```

### 4. Configure Environment Variables

Edit `backend/.env` with your credentials:

```env
# MongoDB Atlas (replace with your connection string)
MONGODB_URL=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/sole_ecommerce

# JWT
JWT_SECRET=your_long_random_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=7

# Razorpay
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret

# App
APP_NAME=SoleStyle
FRONTEND_URL=http://127.0.0.1:5500
```

### 5. Seed the Database

Populates MongoDB with **12 sample shoe products** and a **demo user account**:

```powershell
cd backend
python seed.py
```

**Demo credentials:**
- Email: `demo@solestyle.com`
- Password: `demo1234`

### 6. Start the Backend API

```powershell
# From the E-commerce root directory
uvicorn backend.main:app --reload --port 8000
```

- **API Docs (Swagger UI):** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

### 7. Serve the Frontend

```powershell
cd frontend
python -m http.server 5500
```

Open your browser at **http://127.0.0.1:5500**

> 💡 Alternatively, open `frontend/index.html` with VS Code's **Live Server** extension.

---

## 🔌 API Reference

### Authentication — `/api/auth`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Create new user account |
| `POST` | `/api/auth/login` | Login — returns JWT token |
| `GET` | `/api/auth/me` | Get current user profile |

### Products — `/api/products`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/products` | List products (search, filter, sort, paginate) |
| `GET` | `/api/products/featured` | Featured products |
| `GET` | `/api/products/new-arrivals` | New arrival products |
| `GET` | `/api/products/{id}` | Product detail |
| `POST` | `/api/products` | Create product *(auth required)* |
| `PUT` | `/api/products/{id}` | Update product *(auth required)* |
| `DELETE` | `/api/products/{id}` | Delete product *(auth required)* |
| `GET` | `/api/products/{id}/reviews` | List product reviews |
| `POST` | `/api/products/{id}/reviews` | Submit review *(auth required)* |

**Product query parameters:**

| Param | Example | Description |
|---|---|---|
| `search` | `?search=nike` | Full-text search |
| `category` | `?category=men` | men / women / kids / unisex |
| `sub_category` | `?sub_category=running` | running / casual / sports / formal |
| `brand` | `?brand=Nike` | Brand filter |
| `size` | `?size=9` | UK size filter |
| `min_price` | `?min_price=3000` | Minimum price (₹) |
| `max_price` | `?max_price=10000` | Maximum price (₹) |
| `is_featured` | `?is_featured=true` | Featured only |
| `is_new_arrival` | `?is_new_arrival=true` | New arrivals only |
| `sort_by` | `?sort_by=price_asc` | newest / price_asc / price_desc / rating |
| `page` | `?page=2` | Page number |
| `limit` | `?limit=12` | Results per page |

### Cart — `/api/cart`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/cart` | Get current user's cart |
| `POST` | `/api/cart/add` | Add item to cart |
| `PUT` | `/api/cart/update` | Update item quantity |
| `DELETE` | `/api/cart/remove` | Remove single item |
| `DELETE` | `/api/cart/clear` | Clear entire cart |

### Wishlist — `/api/wishlist`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/wishlist` | Get wishlist |
| `POST` | `/api/wishlist/add/{product_id}` | Add to wishlist |
| `DELETE` | `/api/wishlist/remove/{product_id}` | Remove from wishlist |
| `GET` | `/api/wishlist/check/{product_id}` | Check if item is wishlisted |

### Orders — `/api/orders`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/orders` | Get order history |
| `POST` | `/api/orders/create-razorpay-order` | Create Razorpay payment order |
| `POST` | `/api/orders/verify-payment` | Verify HMAC signature + place order |
| `PUT` | `/api/orders/{id}/cancel` | Cancel an order |

---

## 💳 Razorpay Payment Flow

```
User clicks "Pay Now"
      ↓
POST /api/orders/create-razorpay-order   ← backend creates Razorpay order
      ↓
Razorpay Checkout Modal opens in browser
      ↓
User completes payment (UPI / Card / Net Banking)
      ↓
handler(response) called with payment_id + signature
      ↓
POST /api/orders/verify-payment          ← backend verifies HMAC-SHA256 signature
      ↓
Order saved to MongoDB, cart cleared, stock reduced
      ↓
Redirect to /orders.html
```

---

## 🎨 Design System

The frontend uses a **dark glassmorphism theme** with CSS custom properties defined in `frontend/css/global.css`:

| Token | Value | Usage |
|---|---|---|
| `--accent-primary` | `#7c3aed` | Purple — primary actions |
| `--accent-secondary` | `#a855f7` | Light purple — text accents |
| `--accent-gold` | `#fbbf24` | Gold — featured badges |
| `--bg-primary` | `#0a0a12` | Page background |
| `--bg-card` | `#12121f` | Card backgrounds |
| `--success` | `#10b981` | In-stock, new badge |
| `--error` | `#ef4444` | Errors, sale badge |

**Badges** use frosted dark glass containers with vivid neon borders for high contrast on any background color (yellow, white, or dark images).

**Image fallback**: A self-contained inline SVG data URI (`FALLBACK_SHOE_IMAGE` in `utils.js`) renders instantly without any external network request when product images fail to load.

---

## 🗄️ Database Collections

| Collection | Description |
|---|---|
| `users` | User accounts (hashed passwords, JWT auth) |
| `products` | Shoe catalog with images, sizes, colors, reviews |
| `carts` | Per-user cart items |
| `wishlists` | Per-user saved products |
| `orders` | Placed orders with Razorpay payment info |

**Indexes** are auto-created on startup via `create_indexes()` in `database.py`:
- `products.name` — text search
- `products.brand`, `products.category` — filter performance
- `carts.user_id`, `orders.user_id` — user-specific queries

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| **CORS error** | Ensure `FRONTEND_URL` in `.env` matches your frontend origin. `http://127.0.0.1:5500` is allowed by default. |
| **MongoDB connection failed** | Verify `MONGODB_URL` is correct and your IP is whitelisted in Atlas Network Access. |
| **Images not loading** | Brand CDN URLs may be region-blocked. Run `python seed.py` to use Unsplash URLs. |
| **JWT errors** | Ensure `JWT_SECRET` is set and consistent. Tokens expire after 7 days. |
| **Razorpay modal not opening** | Confirm `RAZORPAY_KEY_ID` starts with `rzp_test_` for test mode or `rzp_live_` for live. |
| **Import errors running seed** | Run from the `backend/` directory: `cd backend && python seed.py` |

---

## 📄 License

This project does not include an explicit license file. All rights reserved.