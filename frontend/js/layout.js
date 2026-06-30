const NAV_LINKS = [
  { href: "dashboard.html", label: "Dashboard" },
  { href: "recurring-expenses.html", label: "Gastos recorrentes" },
  { href: "sporadic-expenses.html", label: "Gastos esporádicos" },
  { href: "installment-purchases.html", label: "Compras parceladas" },
  { href: "savings.html", label: "Caixinhas" },
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

  sidebar.appendChild(el("h2", { text: "ParcelaFácil" }));
  sidebar.appendChild(nav);
}
