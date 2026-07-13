(function () {
  const preloader = document.getElementById("preloader");
  const pageStartedAt = Date.now();
  const currentPageUrl = window.location.href;
  const attributionParams = new URLSearchParams(window.location.search);
  const projectName = document.body.dataset.projectName || "";
  const marketingConfig = window.HIG_TRACKING || {};
  const trackingEnabled = document.body.dataset.trackingEnabled !== "no";
  const shouldShowPreloader = document.body.dataset.showPreloader === "yes";
  const preloaderSeenKey = "hig_home_preloader_seen";

  const hidePreloader = function () {
    if (!preloader) return;
    try {
      window.sessionStorage.setItem(preloaderSeenKey, "yes");
    } catch (error) {}
    preloader.classList.add("is-hidden");
    window.setTimeout(function () {
      preloader.remove();
    }, 500);
  };

  if (preloader && shouldShowPreloader) {
    let alreadySeen = false;
    try {
      alreadySeen = window.sessionStorage.getItem(preloaderSeenKey) === "yes";
    } catch (error) {}
    if (alreadySeen) {
      hidePreloader();
    } else {
      window.setTimeout(hidePreloader, 1300);
      window.setTimeout(hidePreloader, 2500);
      window.addEventListener("load", function () {
        window.setTimeout(hidePreloader, 250);
      });
    }
  } else {
    hidePreloader();
  }

  if (trackingEnabled) setupConsent();
  setupMobileMenu();
  setupReveal();
  setupHeaderAndBackToTop();
  setupVideoSound();
  setupGalleries();
  setupMaps();
  if (trackingEnabled) {
    setupLeadForms();
    setupClicks();
    setupScrollDepth();
    setupPageExitTiming();

    let sessionStartedSent = false;
    try {
      sessionStartedSent = window.sessionStorage.getItem("hig_session_started_sent") === "yes";
    } catch (error) {}
    if (!sessionStartedSent) {
      trackEvent("session_started", { page_url: currentPageUrl, first_landing_page: currentPageUrl });
      try { window.sessionStorage.setItem("hig_session_started_sent", "yes"); } catch (error) {}
    }
    trackEvent("page_view", { page_url: currentPageUrl });
    if (["project", "project-detail-page"].includes(document.body.dataset.pageType)) {
      trackEvent("project_view", { page_url: currentPageUrl, project_name: projectName });
      if (window.fbq && getCookie("hig_marketing_consent") === "yes") {
        window.fbq("track", "ViewContent", { content_name: projectName });
      }
    }
  }

  function setupConsent() {
    const banner = document.getElementById("cookie-consent");
    const consent = getCookie("hig_marketing_consent");
    if (consent === "yes") {
      loadMarketingScripts();
      return;
    }
    if (consent === "no") return;
    if (banner) banner.classList.remove("hidden");

    document.querySelector("[data-consent-accept]")?.addEventListener("click", function () {
      setCookie("hig_marketing_consent", "yes", 180);
      banner?.classList.add("hidden");
      loadMarketingScripts();
    });
    document.querySelector("[data-consent-decline]")?.addEventListener("click", function () {
      setCookie("hig_marketing_consent", "no", 30);
      banner?.classList.add("hidden");
    });
  }

  function setupMobileMenu() {
    const button = document.querySelector("[data-mobile-menu-toggle]");
    const menu = document.getElementById("mobile-menu");
    if (!button || !menu) return;
    button.addEventListener("click", function () {
      const open = menu.classList.toggle("hidden") === false;
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  function loadMarketingScripts() {
    if (marketingConfig.gtm) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
      injectScript("https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(marketingConfig.gtm));
    }
    if (marketingConfig.metaPixel && !window.fbq) {
      window.fbq = function () {
        window.fbq.callMethod ? window.fbq.callMethod.apply(window.fbq, arguments) : window.fbq.queue.push(arguments);
      };
      if (!window._fbq) window._fbq = window.fbq;
      window.fbq.push = window.fbq;
      window.fbq.loaded = true;
      window.fbq.version = "2.0";
      window.fbq.queue = [];
      injectScript("https://connect.facebook.net/en_US/fbevents.js");
      window.fbq("init", marketingConfig.metaPixel);
      window.fbq("track", "PageView");
    }
  }

  function setupReveal() {
    const revealItems = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) {
      revealItems.forEach(function (item) { item.classList.add("is-visible"); });
      return;
    }
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.14 }
    );
    revealItems.forEach(function (item, index) {
      item.style.transitionDelay = Math.min(index * 45, 220) + "ms";
      observer.observe(item);
    });
  }

  function setupHeaderAndBackToTop() {
    const header = document.getElementById("site-header");
    const backToTop = document.getElementById("back-to-top");
    function update() {
      const scrolled = window.scrollY > 120;
      header?.classList.toggle("is-hidden", scrolled);
      backToTop?.classList.toggle("is-visible", window.scrollY > 700);
    }
    update();
    window.addEventListener("scroll", update, { passive: true });
    backToTop?.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  function setupVideoSound() {
    document.querySelectorAll("[data-video-sound-toggle]").forEach(function (button) {
      const section = button.closest("section");
      const video = section?.querySelector(".js-audio-video");
      if (!video) return;
      button.addEventListener("click", function () {
        video.muted = !video.muted;
        if (!video.muted) video.play().catch(function () {});
        button.querySelector(".sound-off")?.classList.toggle("hidden", !video.muted);
        button.querySelector(".sound-on")?.classList.toggle("hidden", video.muted);
      });
    });
  }

  function setupGalleries() {
    document.querySelectorAll("[data-gallery-carousel]").forEach(function (gallery) {
      const images = (gallery.dataset.galleryImages || "").split("|").filter(Boolean);
      const img = gallery.querySelector("img");
      if (!img || images.length < 2) return;
      let index = 0;
      function show(nextIndex) {
        index = (nextIndex + images.length) % images.length;
        gallery.classList.add("is-flipping");
        window.setTimeout(function () {
          img.src = images[index];
        }, 180);
        window.setTimeout(function () {
          gallery.classList.remove("is-flipping");
        }, 430);
      }
      gallery.addEventListener("mousemove", function (event) {
        const rect = gallery.getBoundingClientRect();
        const x = event.clientX - rect.left;
        if (x > rect.width * 0.68 && !gallery.dataset.cooldown) {
          gallery.dataset.cooldown = "1";
          show(index + 1);
          window.setTimeout(function () { delete gallery.dataset.cooldown; }, 650);
        } else if (x < rect.width * 0.32 && !gallery.dataset.cooldown) {
          gallery.dataset.cooldown = "1";
          show(index - 1);
          window.setTimeout(function () { delete gallery.dataset.cooldown; }, 650);
        }
      });
      gallery.parentElement?.querySelectorAll("[data-gallery-thumb]").forEach(function (thumb) {
        thumb.addEventListener("click", function () {
          show(parseInt(thumb.dataset.galleryThumb || "0", 10));
        });
      });
    });
  }

  function setupMaps() {
    document.querySelectorAll(".project-map").forEach(function (mapEl) {
      if (!window.L) return;
      const lat = parseFloat(mapEl.dataset.lat);
      const lng = parseFloat(mapEl.dataset.lng);
      const zoom = parseInt(mapEl.dataset.zoom || "15", 10);
      if (Number.isNaN(lat) || Number.isNaN(lng)) return;
      const map = L.map(mapEl).setView([lat, lng], zoom);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      const title = mapEl.dataset.title || "HIG Development";
      const description = mapEl.dataset.description || "";
      L.marker([lat, lng]).addTo(map).bindPopup("<strong>" + escapeHtml(title) + "</strong><br>" + escapeHtml(description));
      let tracked = false;
      ["zoomstart", "dragstart", "popupopen", "click"].forEach(function (eventName) {
        map.on(eventName, function () {
          if (tracked) return;
          tracked = true;
          trackEvent("map_interaction", { page_url: currentPageUrl, project_name: projectName, metadata: { interaction: eventName } });
        });
      });
    });
  }

  function setupLeadForms() {
    const params = new URLSearchParams(window.location.search);
    document.querySelectorAll("[data-lead-form]").forEach(function (form) {
      const eventIdInput = form.querySelector('[name="event_id"]');
      if (eventIdInput && !eventIdInput.value) {
        eventIdInput.value = window.crypto?.randomUUID ? window.crypto.randomUUID() : createEventId();
      }
      ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (key) {
        const input = form.querySelector('[name="' + key + '"]');
        if (input) input.value = params.get(key) || "";
      });
      form.addEventListener("focusin", function () {
        trackEvent("lead_form_start", { page_url: currentPageUrl, project_name: projectName });
      }, { once: true });
      form.addEventListener("submit", function () {
        if (window.fbq && getCookie("hig_marketing_consent") === "yes") {
          window.fbq("track", "Lead", {}, { eventID: eventIdInput?.value || "" });
        }
      });
    });
  }

  function setupClicks() {
    document.addEventListener("click", function (event) {
      const link = event.target.closest("a,button");
      if (link) {
        trackEvent("cta_click", {
          page_url: currentPageUrl,
          project_name: projectName,
          metadata: { text: link.textContent.trim().slice(0, 80), href: link.href || "" }
        });
      }
    });
  }

  function setupScrollDepth() {
    const milestones = [25, 50, 75, 100];
    const sent = {};
    window.addEventListener("scroll", function () {
      const doc = document.documentElement;
      const depth = Math.min(100, Math.round(((doc.scrollTop + window.innerHeight) / doc.scrollHeight) * 100));
      milestones.forEach(function (milestone) {
        if (depth >= milestone && !sent[milestone]) {
          sent[milestone] = true;
          trackEvent("scroll_depth", { page_url: currentPageUrl, project_name: projectName, metadata: { depth: milestone } });
        }
      });
    }, { passive: true });
  }

  function setupPageExitTiming() {
    let timingSent = false;
    function sendTiming() {
      if (timingSent) return;
      timingSent = true;
      const duration = Math.max(1, Math.round((Date.now() - pageStartedAt) / 1000));
      trackEvent("page_view", {
        page_url: currentPageUrl,
        project_name: projectName,
        metadata: { duration_seconds: duration, timing_event: "page_exit" }
      });
    }
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") sendTiming();
    });
    window.addEventListener("pagehide", sendTiming);
  }

  function trackEvent(eventType, payload) {
    if (!trackingEnabled) return;
    const attribution = {};
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (key) {
      attribution[key] = attributionParams.get(key) || "";
    });
    const body = JSON.stringify(Object.assign({ event_type: eventType }, attribution, payload || {}));
    if (navigator.sendBeacon) {
      navigator.sendBeacon("/tracking/event/", new Blob([body], { type: "application/json" }));
      return;
    }
    fetch("/tracking/event/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body,
      keepalive: true
    }).catch(function () {});
  }

  function createEventId() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (char) {
      const random = Math.random() * 16 | 0;
      const value = char === "x" ? random : (random & 0x3 | 0x8);
      return value.toString(16);
    });
  }

  function injectScript(src) {
    const script = document.createElement("script");
    script.async = true;
    script.src = src;
    document.head.appendChild(script);
  }

  function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = name + "=" + encodeURIComponent(value) + "; expires=" + expires + "; path=/; SameSite=Lax";
  }

  function getCookie(name) {
    return document.cookie.split("; ").reduce(function (result, pair) {
      const parts = pair.split("=");
      return parts[0] === name ? decodeURIComponent(parts[1] || "") : result;
    }, "");
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (char) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" })[char];
    });
  }
})();
