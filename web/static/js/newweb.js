(function () {
  const header = document.querySelector("[data-newweb-header]");
  const drawer = document.querySelector("[data-newweb-drawer]");
  const menuButton = document.querySelector("[data-newweb-menu]");
  const closeButton = document.querySelector("[data-newweb-close]");
  const backToTop = document.querySelector("[data-newweb-top]");

  const setHeader = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 28);
    if (backToTop) backToTop.classList.toggle("is-visible", window.scrollY > 520);
  };

  const openDrawer = () => {
    if (!drawer) return;
    drawer.removeAttribute("inert");
    drawer.classList.add("is-open");
    drawer.setAttribute("aria-hidden", "false");
    menuButton?.setAttribute("aria-expanded", "true");
    document.body.classList.add("nw-menu-open");
    window.setTimeout(() => closeButton?.focus(), 100);
  };

  const closeDrawer = () => {
    if (!drawer) return;
    drawer.classList.remove("is-open");
    drawer.setAttribute("aria-hidden", "true");
    drawer.setAttribute("inert", "");
    menuButton?.setAttribute("aria-expanded", "false");
    document.body.classList.remove("nw-menu-open");
    menuButton?.focus();
  };

  menuButton && menuButton.addEventListener("click", openDrawer);
  closeButton && closeButton.addEventListener("click", closeDrawer);
  drawer && drawer.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeDrawer));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && drawer?.classList.contains("is-open")) closeDrawer();
  });
  backToTop && backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  window.addEventListener("scroll", setHeader, { passive: true });
  setHeader();

  const revealItems = document.querySelectorAll(
    ".nw-section-label, .nw-who-grid, .nw-stats, .nw-project-copy, .nw-project-lanes article > div, .nw-grid-head, .nw-card-grid article, .nw-board-grid article, .nw-insight-list a, .nw-contact > *"
  );
  revealItems.forEach((item) => item.classList.add("nw-reveal"));

  if (!("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.18 }
  );

  revealItems.forEach((item) => observer.observe(item));

  const statObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.querySelectorAll("[data-count]").forEach((counter) => {
          const target = Number(counter.dataset.count || 0);
          const start = performance.now();
          const duration = 1200;

          const tick = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            counter.textContent = Math.round(target * eased).toLocaleString("en-US") + "+";
            if (progress < 1) requestAnimationFrame(tick);
          };

          requestAnimationFrame(tick);
        });
        statObserver.unobserve(entry.target);
      });
    },
    { threshold: 0.4 }
  );

  document.querySelectorAll("[data-newweb-stats]").forEach((stats) => statObserver.observe(stats));
})();
