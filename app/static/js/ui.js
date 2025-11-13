(function(){
  'use strict';

  // Tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

  // Sidebar toggle
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('sidebarToggle');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', ()=>{
      const isOpen = sidebar.classList.toggle('open');
      toggleBtn.setAttribute('aria-expanded', String(isOpen));
    });
  }

  // Clear search with Esc
  const search = document.getElementById('globalSearchInput');
  const clearBtn = document.getElementById('clearSearch');
  if (search && clearBtn) {
    clearBtn.addEventListener('click', ()=>{ search.value=''; search.focus(); });
    search.addEventListener('keydown', (e)=>{ if(e.key==='Escape'){ search.value=''; } });
  }

  // Availability slot handling
  const apptForm = document.querySelector('form[action$="/patient/book"], form[action=""]') || document.querySelector('form');
  const modalEl = document.getElementById('confirmBookingModal');
  const modal = modalEl ? new bootstrap.Modal(modalEl) : null;
  function formatDateISO(d){ return d.toISOString().slice(0,10); }

  if (apptForm) {
    const dateInput = apptForm.querySelector('input[type="date"][name="date"]');
    const timeInput = apptForm.querySelector('input[type="time"][name="time"]');
    const doctorSel = apptForm.querySelector('select[name="doctor_id"]');
    const slots = document.querySelectorAll('.availability .slot');

    // populate data-date for 7-day cards
    const base = new Date();
    document.querySelectorAll('.day-card').forEach((card, idx)=>{
      const d = new Date(base);
      d.setDate(base.getDate() + idx);
      const iso = formatDateISO(d);
      card.querySelectorAll('.slot').forEach(btn=>btn.dataset.date = iso);
      const header = card.querySelector('.small');
      if (header) header.textContent = d.toLocaleDateString(undefined, { weekday:'short', month:'short', day:'numeric' });
    });

    slots.forEach(btn=>{
      btn.addEventListener('click', ()=>{
        slots.forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        const d = btn.dataset.date; const t = btn.dataset.time;
        if (dateInput) dateInput.value = d;
        if (timeInput) timeInput.value = t;
        if (modal) {
          document.getElementById('confirmDoctor').textContent = doctorSel ? doctorSel.options[doctorSel.selectedIndex].text : '';
          document.getElementById('confirmDate').textContent = d;
          document.getElementById('confirmTime').textContent = t;
          modal.show();
        }
      });
    });

    const confirmBtn = document.getElementById('confirmBookingBtn');
    if (confirmBtn && modal) {
      confirmBtn.addEventListener('click', ()=>{ apptForm.submit(); });
    }
  }

  // Client-side validation (progressive enhancement)
  document.querySelectorAll('form').forEach(form=>{
    form.setAttribute('novalidate','');
    form.addEventListener('submit', (e)=>{
      if (!form.checkValidity()) { e.preventDefault(); e.stopPropagation(); }
      form.classList.add('was-validated');
    });
  });
})();
