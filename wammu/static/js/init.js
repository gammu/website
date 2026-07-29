"use strict";

const navigationBreakpoint = window.matchMedia("(max-width: 68rem)");

function setExpandedState(details) {
  const summary = details.querySelector(":scope > summary");
  if (summary) {
    summary.setAttribute("aria-expanded", details.open ? "true" : "false");
  }
}

function closeMenu(details, restoreFocus = false) {
  if (!details.open) {
    return;
  }

  details.open = false;
  setExpandedState(details);
  if (restoreFocus) {
    details.querySelector(":scope > summary")?.focus();
  }
}

function initializeNavigation() {
  const navigation = document.querySelector(".site-navigation");
  const menus = Array.from(document.querySelectorAll("[data-menu]"));

  function updateNavigationLayout(event) {
    if (!navigation) {
      return;
    }

    if (event.matches) {
      navigation.open = false;
    } else {
      navigation.open = true;
    }
    setExpandedState(navigation);
  }

  if (navigation) {
    setExpandedState(navigation);
    navigation.addEventListener("toggle", () => setExpandedState(navigation));
    updateNavigationLayout(navigationBreakpoint);
    navigationBreakpoint.addEventListener("change", updateNavigationLayout);
  }

  for (const menu of menus) {
    setExpandedState(menu);
    menu.addEventListener("toggle", () => {
      setExpandedState(menu);
      if (!menu.open) {
        return;
      }

      for (const otherMenu of menus) {
        if (otherMenu !== menu) {
          closeMenu(otherMenu);
        }
      }
    });
  }

  document.addEventListener("click", (event) => {
    for (const menu of menus) {
      if (!menu.contains(event.target)) {
        closeMenu(menu);
      }
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }

    const openMenu = menus.findLast((menu) => menu.open);
    if (openMenu) {
      event.preventDefault();
      closeMenu(openMenu, true);
    }
  });
}

function initializeAntispamFields() {
  for (const form of document.querySelectorAll("[data-antispam-form]")) {
    if (form.elements.irobot) {
      continue;
    }

    const input = document.createElement("input");
    input.type = "hidden";
    input.name = "irobot";
    input.value = "nospam";
    form.append(input);
  }
}

function initializeLightbox() {
  const dialog = document.querySelector("[data-lightbox-dialog]");
  const links = Array.from(document.querySelectorAll("[data-lightbox-link]"));

  if (!dialog || links.length === 0 || typeof dialog.showModal !== "function") {
    return;
  }

  const image = dialog.querySelector("[data-lightbox-image]");
  const caption = dialog.querySelector("[data-lightbox-caption]");
  const previousButton = dialog.querySelector("[data-lightbox-previous]");
  const nextButton = dialog.querySelector("[data-lightbox-next]");
  let activeLink = null;
  let activeGroup = [];
  let activeIndex = 0;

  function displayLink(link) {
    const thumbnail = link.querySelector("img");
    activeIndex = activeGroup.indexOf(link);
    image.src = link.href;
    image.alt = thumbnail?.alt || "";
    caption.textContent = link.dataset.caption || thumbnail?.alt || "";
    const hasMultipleImages = activeGroup.length > 1;
    previousButton.hidden = !hasMultipleImages;
    nextButton.hidden = !hasMultipleImages;
  }

  function move(offset) {
    activeIndex =
      (activeIndex + offset + activeGroup.length) % activeGroup.length;
    displayLink(activeGroup[activeIndex]);
  }

  for (const link of links) {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      activeLink = link;
      const groupName = link.dataset.lightboxGroup || "";
      activeGroup = links.filter(
        (candidate) => (candidate.dataset.lightboxGroup || "") === groupName,
      );
      displayLink(link);
      dialog.showModal();
    });
  }

  previousButton.addEventListener("click", () => move(-1));
  nextButton.addEventListener("click", () => move(1));

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });

  dialog.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" && activeGroup.length > 1) {
      event.preventDefault();
      move(-1);
    } else if (event.key === "ArrowRight" && activeGroup.length > 1) {
      event.preventDefault();
      move(1);
    }
  });

  dialog.addEventListener("close", () => {
    image.removeAttribute("src");
    activeLink?.focus();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initializeNavigation();
  initializeAntispamFields();
  initializeLightbox();
});
