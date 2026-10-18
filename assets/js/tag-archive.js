(function () {
  function slugify(value) {
    return String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
  }

  function tagFromLocation() {
    const params = new URLSearchParams(window.location.search);
    if (params.get("t")) return slugify(params.get("t"));
    const parts = window.location.pathname.replace(/\/+$/, "").split("/");
    if (parts[1] === "tags" && parts[2] && parts[2] !== "index.html") {
      return slugify(decodeURIComponent(parts[2]));
    }
    return "";
  }

  function splitTags(raw) {
    return String(raw || "")
      .split(",")
      .map(function (item) {
        return item.trim();
      })
      .filter(Boolean);
  }

  function matchesTag(entry, wanted) {
    return splitTags(entry.tags).some(function (tag) {
      return slugify(tag) === wanted;
    });
  }

  function el(name, className, text) {
    const node = document.createElement(name);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function renderCloud(root, entries) {
    const counts = {};
    entries.forEach(function (entry) {
      splitTags(entry.tags).forEach(function (tag) {
        const slug = slugify(tag);
        if (!slug) return;
        if (!counts[slug]) counts[slug] = { label: tag, slug: slug, n: 0 };
        counts[slug].n += 1;
      });
    });
    const list = Object.keys(counts)
      .map(function (key) {
        return counts[key];
      })
      .filter(function (item) {
        return item.n > 1;
      })
      .sort(function (a, b) {
        return b.n - a.n || a.label.localeCompare(b.label, "pt-BR");
      });

    root.innerHTML = "";
    const wrap = el("div", "d-flex flex-wrap mx-xl-2");
    wrap.id = "tags";
    list.forEach(function (item) {
      const box = el("div");
      const link = el("a", "tag", item.label + " ");
      link.href = "/tags/" + encodeURIComponent(item.slug) + "/";
      link.appendChild(el("span", "text-muted", String(item.n)));
      box.appendChild(link);
      wrap.appendChild(box);
    });
    root.appendChild(wrap);
  }

  function renderList(root, wanted, entries) {
    const hits = entries.filter(function (entry) {
      return matchesTag(entry, wanted);
    });
    root.innerHTML = "";
    const heading = el("p", "text-muted mb-4");
    heading.textContent = hits.length
      ? hits.length + " postagens com a tag " + wanted
      : "Nenhuma postagem com a tag " + wanted;
    root.appendChild(heading);

    hits.forEach(function (entry) {
      const article = el("article", "mb-4");
      const title = el("h2", "fs-5");
      const link = el("a", "", entry.title || entry.url);
      link.href = entry.url;
      title.appendChild(link);
      article.appendChild(title);
      if (entry.snippet) {
        article.appendChild(el("p", "text-muted mb-1", entry.snippet));
      }
      if (entry.categories) {
        article.appendChild(el("div", "small text-muted", entry.categories));
      }
      root.appendChild(article);
    });
  }

  function boot() {
    const root = document.getElementById("tag-archive");
    const cloud = document.getElementById("tags");
    if (!root && !cloud) return;
    const wanted = tagFromLocation();
    const title = document.querySelector(".dynamic-title, #tag-title");

    fetch("/assets/js/data/search.json")
      .then(function (res) {
        if (!res.ok) throw new Error("search.json " + res.status);
        return res.json();
      })
      .then(function (entries) {
        if (!Array.isArray(entries)) throw new Error("search.json inválido");
        if (wanted) {
          if (title) title.textContent = wanted;
          document.title = wanted + " | Tags | LAWFARE";
          if (cloud) cloud.hidden = true;
          const target = root || cloud.parentElement || document.body;
          if (!root) {
            const box = el("div");
            box.id = "tag-archive";
            target.insertBefore(box, cloud);
            renderList(box, wanted, entries);
          } else {
            renderList(root, wanted, entries);
          }
        } else if (root && !cloud) {
          renderCloud(root, entries);
        }
      })
      .catch(function (err) {
        const target = root || cloud || document.body;
        const p = el("p", "text-danger", "Não foi possível carregar as tags.");
        target.appendChild(p);
        console.error(err);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
