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

  const recoveryVersion = "20260720";
  const withRecoveryVersion = (value) => {
    if (!value) return value;
    const url = new URL(value, window.location.href);
    if (url.origin !== window.location.origin) return value;
    if (!url.pathname.startsWith("/media/") && !url.pathname.startsWith("/static/")) return value;
    url.searchParams.set("asset_retry", recoveryVersion);
    return url.href;
  };

  const recoverImage = (image) => {
    if (image.dataset.assetRetry === "true") return;
    const recoveredSrc = withRecoveryVersion(image.currentSrc || image.src);
    if (!recoveredSrc || recoveredSrc === image.src) return;
    image.dataset.assetRetry = "true";
    image.removeAttribute("srcset");
    image.src = recoveredSrc;
  };

  document.querySelectorAll("img").forEach((image) => {
    image.addEventListener("error", () => recoverImage(image), { once: true });
    if (image.complete && image.naturalWidth === 0) recoverImage(image);
  });

  document.querySelectorAll("video").forEach((video) => {
    video.addEventListener(
      "error",
      () => {
        if (video.dataset.assetRetry === "true") return;
        let changed = false;
        video.querySelectorAll("source[src]").forEach((source) => {
          const recoveredSrc = withRecoveryVersion(source.src);
          if (recoveredSrc && recoveredSrc !== source.src) {
            source.src = recoveredSrc;
            changed = true;
          }
        });
        if (video.src) {
          const recoveredSrc = withRecoveryVersion(video.src);
          if (recoveredSrc && recoveredSrc !== video.src) {
            video.src = recoveredSrc;
            changed = true;
          }
        }
        if (changed) {
          video.dataset.assetRetry = "true";
          video.load();
          const playPromise = video.autoplay ? video.play() : null;
          if (playPromise) playPromise.catch(() => {});
        }
      },
      { once: true }
    );
  });

  const lazyVideos = document.querySelectorAll("[data-lazy-video]");
  const loadVideo = (video) => {
    if (video.dataset.loaded === "true") return;
    video.querySelectorAll("source[data-src]").forEach((source) => {
      source.src = source.dataset.src;
      source.removeAttribute("data-src");
    });
    video.dataset.loaded = "true";
    video.load();
    const playPromise = video.play();
    if (playPromise) playPromise.catch(() => {});
  };

  if ("IntersectionObserver" in window) {
    const videoObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          loadVideo(entry.target);
          videoObserver.unobserve(entry.target);
        });
      },
      { rootMargin: "400px 0px", threshold: 0.01 }
    );
    lazyVideos.forEach((video) => videoObserver.observe(video));
  } else {
    lazyVideos.forEach(loadVideo);
  }

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
