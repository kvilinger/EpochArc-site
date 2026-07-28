export function setupPageToc() {
  const nav = document.querySelector('[data-page-toc]');
  if (!nav) return;

  const entries = Array.from(nav.querySelectorAll('a[href^="#"]'))
    .map((link) => {
      const id = decodeURIComponent(link.getAttribute('href').slice(1));
      return { id, link, target: document.getElementById(id) };
    })
    .filter(({ link, target }) => {
      if (target) return true;
      link.remove();
      return false;
    });

  if (!entries.length) {
    nav.closest('.rail-toc-card')?.remove();
    return;
  }

  let activeId = '';
  let ticking = false;

  function setActive(id) {
    if (!id || id === activeId) return;
    activeId = id;
    let activeLink = null;
    entries.forEach(({ id: entryId, link }) => {
      const isActive = entryId === id;
      link.classList.toggle('active', isActive);
      if (isActive) {
        activeLink = link;
        link.setAttribute('aria-current', 'location');
      } else {
        link.removeAttribute('aria-current');
      }
    });

    const rail = nav.closest('.page-rail');
    if (rail && activeLink && rail.scrollHeight > rail.clientHeight) {
      const railRect = rail.getBoundingClientRect();
      const linkRect = activeLink.getBoundingClientRect();
      if (linkRect.top < railRect.top + 8) {
        rail.scrollTop -= railRect.top + 8 - linkRect.top;
      } else if (linkRect.bottom > railRect.bottom - 8) {
        rail.scrollTop += linkRect.bottom - railRect.bottom + 8;
      }
    }
  }

  function updateActiveSection() {
    ticking = false;
    const activationLine = Math.min(180, window.innerHeight * 0.24);
    let current = entries[0];

    for (const entry of entries) {
      if (entry.target.getBoundingClientRect().top <= activationLine) {
        current = entry;
      } else {
        break;
      }
    }

    const atPageEnd = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 8;
    setActive(atPageEnd ? entries[entries.length - 1].id : current.id);
  }

  function requestUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateActiveSection);
  }

  entries.forEach(({ id, link }) => {
    link.addEventListener('click', () => setActive(id));
  });

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  updateActiveSection();
}
