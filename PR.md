# HMS UI Polish – Professional

## Summary
This PR modernizes the HMS UI with a consistent, accessible Bootstrap 5 design and a light custom theme. It adds a semantic base layout with a sticky navbar, collapsible sidebar, centralized alerts/toasts, and shared macros for metric cards, avatars, and appointment rows. No database schemas or API endpoints were changed.

## What changed
- New semantic base layout with partials: `_navbar.html`, `_sidebar.html`, `_alerts.html`, `_footer.html`.
- New theme and JS: `static/css/theme.css`, `static/js/ui.js`.
- New Jinja macros: `templates/macros.html` (avatar, metric_card, appointment_row).
- Optional components: `templates/partials/availability.html`, `templates/partials/confirm_booking_modal.html` (prepared for patient booking).
- Dashboards updated:
  - `templates/admin/dashboard.html` → metric cards + improved table
  - `templates/doctor/dashboard.html` → shared appointment_row
  - `templates/patient/dashboard.html` → improved table, empty state, accessible actions

## Accessibility
- Color contrast for body text vs background using `--muted`/`--bg`.
- Visible focus outlines via `:focus-visible`.
- aria-labels on icon-only buttons and toggles; role="navigation" on navbar.
- Keyboard support: Esc clears navbar search; tooltips initialized for icons.

## Tiny backend changes
None. A context processor was NOT added. All counts used were already provided by existing routes.

## Testing steps
1. Install deps, init DB, run app
   - `pip install -r requirements.txt`
   - `python create_db.py`
   - `flask run`
2. Admin flow
   - Login `admin`/`admin123`
   - Visit Admin Dashboard; verify metric cards and recent appointments table
3. Doctor flow
   - Create a doctor via Admin → Doctors
   - Login as doctor; verify dashboard, open an appointment
4. Patient flow
   - Register a patient, login
   - Book appointment (existing page) and verify Patient Dashboard table + cancel icon
5. UI/UX checks
   - Navbar hamburger toggles sidebar on small screens
   - Tooltips appear on icon-only buttons
   - Focus outlines visible when tabbing

## Revert instructions
```
git checkout main
git branch -D ui/polish-professional
```

## Notes / TODOs (future)
- Wire the availability grid and confirm modal into `patient/book` page.
- Convert Admin Add/Edit Doctor form to modals on listing page.
- Optional: Add Chart.js chart to Admin dashboard using aggregated status counts.
