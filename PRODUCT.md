# PropertyNest — Product Document

## What is PropertyNest?

PropertyNest is a property rental management platform where tenants can search for rental homes, apply to rent them, and manage their leases — all from a single web application. Landlords can list their properties, review applications, and manage maintenance requests. Administrators oversee the entire platform, approving new sellers and managing users.

## Who is it for?

| Role | Description |
|---|---|
| **Tenant / Buyer** | Someone looking to rent a home. They can browse properties, apply for rentals, book appointments, and raise maintenance requests after moving in. |
| **Seller / Landlord** | A property owner who lists their homes for rent. They review applications, approve tenants, and handle maintenance. |
| **Admin** | A platform administrator who approves new seller registrations, manages users, and oversees all properties and appointments. |

## What each screen does

### 1. Landing Page (`/`)
The homepage of PropertyNest. Shows a hero section with a call-to-action, property highlights, and navigation to search or login. This is the first thing any visitor sees.

### 2. Login / Register Page (`/login`)
Users can create a new account or sign in to an existing one. New users are automatically assigned the "TENANT" role. Passwords must be at least 8 characters. After login, a JWT token is stored in the browser for authenticated requests.

### 3. Property Search Page (`/properties`)
A searchable, filterable list of all published rental properties. Users can filter by city, property type, rent range, and sort by newest or rent price. Each property is shown as a card with key details.

### 4. Property Detail Page (`/properties/:id`)
Shows full details of a single property including description, amenities, images, owner info, and monthly rent. Tenants can submit a rental application or book an appointment to tour the property from this page.

### 5. Tenant Dashboard (`/dashboard`)
A personalized dashboard for logged-in tenants. Shows:
- **My Applications**: All rental applications the tenant has submitted, with their current status (Pending, Approved, Rejected)
- **My Leases**: Active lease agreements after an application is approved
- **My Appointments**: Scheduled property tours or support calls, with video call links for confirmed appointments
- **Maintenance Requests**: Requests submitted for issues in rented properties

### 6. Seller / Owner Dashboard (`/dashboard` for SELLER role)
When a user has the SELLER role, their dashboard additionally shows:
- **My Properties**: All properties they have listed
- **Received Applications**: Applications from tenants wanting to rent their properties, with Approve/Reject buttons
- **Owner Appointments**: Appointment requests from tenants

### 7. Admin Dashboard (`/dashboard` for ADMIN role)
Full platform management for administrators:
- **All Users**: View and delete user accounts
- **All Properties**: View, approve, or reject property listings
- **Seller Requests**: Review and approve/reject new seller registrations
- **All Appointments**: View and confirm/reject/complete all appointments across the platform

### 8. Become a Seller Page (`/become-seller`)
A form where tenants can apply to become a property seller. They fill in their personal details, property information, upload ownership documents and property images. After submission, an admin reviews and approves or rejects the request.

## What each API does

### Authentication (`/api/auth`)
- **Register**: Creates a new user with hashed password and assigns TENANT role
- **Login**: Validates credentials and returns a JWT access token
- **Get Profile**: Returns the current user's details and roles

### Properties (`/api/properties`)
- **List**: Returns all published properties with optional filters (city, type, rent range, availability, sort order). Merges PostgreSQL data with MongoDB details (descriptions, amenities, images)
- **Create**: Sellers create a new property listing (starts in PENDING status awaiting admin approval)
- **Get Detail**: Returns full property info including owner details and MongoDB extras
- **Update**: Owners update their own listings. Admins can approve/reject/archive properties
- **Delete**: Removes property from both PostgreSQL and MongoDB
- **Upload Images**: Saves property images to disk and stores URLs in MongoDB

### Applications (`/api/applications`)
- **Submit**: Tenants apply to rent a specific property. System checks the property is published and available, and prevents duplicate applications
- **List**: Returns applications filtered by user role — tenants see their own, sellers see applications for their properties
- **Approve**: When a seller approves an application, the system automatically rejects all other pending applications for that property AND creates a lease
- **Reject**: Seller rejects with a mandatory reason
- **Delete**: Tenants can withdraw pending applications

### Seller Requests (`/api/seller-requests`)
- **Submit**: Tenants submit a form with documents to become a property seller
- **List**: Users see their own requests, admins see all
- **Approve**: Admin approves — the user gets the SELLER role and a property is automatically created and published
- **Reject**: Admin rejects with a reason
- **Delete**: Users can withdraw pending requests

### Leases (`/api/leases`)
- **List**: Returns all leases for the current user (as tenant or owner)
- **Create**: Automatically generated when an application is approved. Sets start/end dates based on the application's move-in date and lease duration

### Maintenance (`/api/maintenance`)
- **Create**: Tenants raise maintenance requests linked to their lease, property, and tenant ID
- **List**: Filtered by user role — tenants see their own, owners see requests for their properties
- **Update Status**: Owners/admins update status (Open → In Progress → Resolved → Closed) with a mandatory comment
- **Upload Images**: Attach photos of the issue

### Appointments (`/api/appointments`)
- **Book**: Tenants schedule a property tour or support call. If linked to a property, the system automatically finds the owner
- **List**: Filtered by role — tenants see their bookings, owners see requests for their properties, admins see everything
- **Confirm**: Admin/owner confirms an appointment and a Jitsi video call URL is automatically generated
- **Reject**: Requires a reason
- **Delete**: Users can cancel pending appointments

## Key Business Rules

1. **New users start as TENANT** — they must apply to become a SELLER
2. **Properties start as PENDING** — admin must approve before they appear in search
3. **Approving an application auto-rejects all others** for that property and auto-creates a lease
4. **Approving a seller request auto-creates** the SELLER role and publishes their property
5. **Confirmed appointments auto-generate** a unique Jitsi video call link
6. **Only PENDING items can be modified or deleted** — once approved/rejected, they are locked
7. **File uploads** (ownership docs, property images, gov IDs) are saved to disk with UUID-prefixed names to prevent collisions
