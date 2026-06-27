const NAV_LINKS = [
  { href: "dashboard.html", label: "Dashboard" },
  { href: "recurring-expenses.html", label: "Gastos recorrentes" },
  { href: "installment-purchases.html", label: "Compras parceladas" },
  { href: "categories.html", label: "Categorias" },
  { href: "calendar.html", label: "Calendário" },
  { href: "reports.html", label: "Relatórios" },
];

function renderSidebar(activeHref) {
  const sidebar = document.getElementById("sidebar");
  if (!sidebar) return;

  const nav = el("nav", {}, NAV_LINKS.map((link) =>
    el("a", {
      href: link.href,
      class: link.href === activeHref ? "active" : "",
      text: link.label,
    })
  ));

  const logoutBtn = el("button", { class: "btn logout-btn", text: "Sair" });
  logoutBtn.addEventListener("click", logout);

  sidebar.appendChild(el("h2", { text: "ParcelaFácil" }));
  sidebar.appendChild(nav);
  sidebar.appendChild(logoutBtn);
}
