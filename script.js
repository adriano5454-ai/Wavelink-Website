/* Wavelink website 2.3.0. Static, dependency-free progressive enhancement.
 * No API calls, analytics, account state or storage. Previews are local illustrations.
 */
(() => {
  'use strict';

  const header = document.querySelector('.site-header');
  const navigation = document.querySelector('#site-nav');
  const menuButton = document.querySelector('.menu-toggle');
  const mobileViewport = window.matchMedia('(max-width: 959px)');

  if (header && navigation && menuButton) {
    const closeMenu = (restoreFocus = false) => {
      navigation.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', 'Open navigation');
      if (restoreFocus && mobileViewport.matches) menuButton.focus();
    };

    const updateNavigation = () => {
      closeMenu();
      menuButton.hidden = !mobileViewport.matches;
    };

    // Add enhancement only after the controls are found and initialised.
    header.classList.add('navigation-ready');
    updateNavigation();
    if (typeof mobileViewport.addEventListener === 'function') {
      mobileViewport.addEventListener('change', updateNavigation);
    } else {
      // Compatibility fallback for browsers with the older MediaQueryList API.
      mobileViewport.addListener(updateNavigation);
    }

    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') !== 'true';
      navigation.classList.toggle('is-open', open);
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    });

    navigation.addEventListener('click', event => {
      const link = event.target.closest('a');
      if (!link) return;
      const wasOpen = menuButton.getAttribute('aria-expanded') === 'true';
      closeMenu();
      const href = link.getAttribute('href') || '';
      if (wasOpen && href.startsWith('#')) {
        const target = document.getElementById(href.slice(1));
        if (target) {
          // Move focus into the selected section, not into a now-hidden menu.
          target.setAttribute('tabindex', '-1');
          target.focus({ preventScroll: true });
        }
      } else if (wasOpen && link.target === '_blank') {
        menuButton.focus();
      }
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        closeMenu(true);
      }
    });
    document.addEventListener('click', event => {
      if (!header.contains(event.target)) closeMenu();
    });
    header.addEventListener('focusout', event => {
      if (!header.contains(event.relatedTarget)) closeMenu();
    });
  }

  /** Enable a self-contained, keyboard-operable tab group with manual activation.
   * Arrow keys/Home/End move focus; Enter/Space select. There is no auto-rotation.
   */
  document.querySelectorAll('[data-tabs]').forEach(group => {
    const tablist = group.querySelector('[role="tablist"]');
    if (!tablist) return;
    const tabs = [...tablist.querySelectorAll('[role="tab"]')];
    const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
    if (!tabs.length || panels.some(panel => !panel || !group.contains(panel))) return;

    const activate = selectedTab => {
      const selectedIndex = tabs.indexOf(selectedTab);
      if (selectedIndex < 0) return;
      tabs.forEach((tab, index) => {
        const selected = index === selectedIndex;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        panels[index].hidden = !selected;
      });
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        switch (event.key) {
          case 'ArrowRight': next = (index + 1) % tabs.length; break;
          case 'ArrowLeft': next = (index - 1 + tabs.length) % tabs.length; break;
          case 'Home': next = 0; break;
          case 'End': next = tabs.length - 1; break;
          default: return; // Native button Enter/Space behaviour activates the tab.
        }
        event.preventDefault();
        tabs.forEach((item, i) => { item.tabIndex = i === next ? 0 : -1; });
        tabs[next].focus();
      });
    });
    // Platform overview and module cards open their matching capability view.
    // Their ordinary #platform links still work without JavaScript.
    document.querySelectorAll('[data-preview]').forEach(link => {
      const target = tabs.find(tab => tab.id === `tab-${link.dataset.preview}`);
      if (!target) return;
      link.addEventListener('click', () => {
        activate(target);
        // Put keyboard focus on the selected control, not a hidden panel.
        target.focus({ preventScroll: true });
      });
    });
    tablist.hidden = false;
    activate(tabs.find(tab => tab.getAttribute('aria-selected') === 'true') || tabs[0]);
  });

  const emailButton = document.querySelector('[data-copy-email]');
  const copyStatus = document.querySelector('#copy-status');
  if (emailButton && copyStatus) {
    emailButton.hidden = false;
    let clearStatusTimer;
    emailButton.addEventListener('click', async () => {
      const email = emailButton.dataset.copyEmail;
      if (!email) return;
      clearTimeout(clearStatusTimer);
      emailButton.disabled = true;
      try {
        if (!navigator.clipboard || !window.isSecureContext) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(email);
        copyStatus.textContent = 'Email address copied.';
      } catch {
        // Local-file previews and denied clipboard permission still have a mailto link.
        copyStatus.textContent = 'Please select and copy the email address above.';
      } finally {
        emailButton.disabled = false;
      }
      clearStatusTimer = window.setTimeout(() => { copyStatus.textContent = ''; }, 9000);
    });
  }

  document.querySelectorAll('[data-year]').forEach(element => {
    element.textContent = String(new Date().getFullYear());
  });
})();
