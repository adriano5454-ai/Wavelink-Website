(() => {
  'use strict';
  const tabs = [...document.querySelectorAll('.platform-choice')];
  const panels = [...document.querySelectorAll('.platform-panel')];
  const tablist = document.querySelector('.platform-tabs');
  if (tabs.length && panels.length && tablist) {
    tablist.setAttribute('role', 'tablist');
    tablist.setAttribute('aria-label', 'Explore Wavelink capabilities');
    tabs.forEach(tab => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', `panel-${tab.dataset.panel}`);
    });
    panels.forEach(panel => {
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', `tab-${panel.id.replace('panel-', '')}`);
      panel.tabIndex = 0;
    });
    const select = (id, focus = false, scroll = false) => {
      const selected = tabs.find(tab => tab.dataset.panel === id);
      if (!selected) return;
      tabs.forEach(tab => {
        const active = tab === selected;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
      });
      panels.forEach(panel => { panel.hidden = panel.id !== `panel-${id}`; });
      if (focus) selected.focus({preventScroll: true});
      if (scroll) tablist.scrollIntoView({block: 'start'});
    };
    const hashPanel = () => {
      const id = location.hash.replace(/^#panel-/, '');
      if (tabs.some(tab => tab.dataset.panel === id)) select(id);
    };
    const initial = location.hash.replace(/^#panel-/, '');
    select(tabs.some(tab => tab.dataset.panel === initial) ? initial : 'equipment');
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', event => {
        event.preventDefault();
        select(tab.dataset.panel);
      });
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index + tabs.length - 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) {
          event.preventDefault();
          tabs[next].focus();
        }
        if (event.key === ' ' || event.key === 'Enter') {
          event.preventDefault();
          select(tab.dataset.panel);
        }
      });
    });
    document.querySelectorAll('[data-show-panel]').forEach(link => {
      link.addEventListener('click', event => {
        event.preventDefault();
        select(link.dataset.showPanel, true, true);
        // Use a stable section anchor: the selected tab remains in this page.
        history.replaceState(null, '', `#panel-${link.dataset.showPanel}`);
      });
    });
    window.addEventListener('hashchange', hashPanel);
  }
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-navigation');
  if (menu && nav) {
    menu.hidden = false;
    const closeMenu = (focus = false) => {
      nav.classList.remove('is-open');
      menu.setAttribute('aria-expanded', 'false');
      if (focus) menu.focus();
    };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      nav.classList.toggle('is-open', open);
      menu.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
    });
    document.addEventListener('click', event => {
      if (!nav.contains(event.target) && !menu.contains(event.target)) closeMenu();
    });
    const desktop = window.matchMedia('(min-width:1151px)');
    desktop.addEventListener('change', () => closeMenu());
  }
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = String(new Date().getFullYear()); });
  document.querySelectorAll('[data-copy-email]').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', async () => {
      const status = document.querySelector('#copy-status');
      if (!status) return;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(button.dataset.copyEmail);
        status.textContent = 'Email address copied.';
      } catch (_) {
        status.textContent = 'Select the email address above and copy it manually.';
      }
    });
  });
  document.documentElement.classList.add('enhanced');
})();
