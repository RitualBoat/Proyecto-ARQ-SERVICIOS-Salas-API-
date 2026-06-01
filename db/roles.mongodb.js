use("SalasMantenimiento");

const DB_NAME = "SalasMantenimiento";

function recreateRole(roleName, privileges) {
  try {
    db.dropRole(roleName);
  } catch (e) {
    // Si el rol no existe, se ignora el error
  }

  db.createRole({
    role: roleName,
    privileges,
    roles: [],
  });
}

recreateRole("Administrador", [
  {
    resource: { db: DB_NAME, collection: "salas" },
    actions: ["find", "insert", "update", "remove"],
  },
  {
    resource: { db: DB_NAME, collection: "mantenimientos" },
    actions: ["find", "insert", "update"],
  },
  {
    resource: { db: DB_NAME, collection: "actividades" },
    actions: ["find", "insert", "update", "remove"],
  },
  {
    resource: { db: DB_NAME, collection: "materiales" },
    actions: ["find", "insert", "update", "remove"],
  },
  {
    resource: { db: DB_NAME, collection: "usuarios" },
    actions: ["find", "insert", "update", "remove"],
  },
  {
    resource: { db: DB_NAME, collection: "salasView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "mantenimientosView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "actividadesView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "materialesView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "usuariosView" },
    actions: ["find"],
  },
]);

recreateRole("Tecnico", [
  {
    resource: { db: DB_NAME, collection: "salas" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "mantenimientos" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "actividades" },
    actions: ["find", "insert", "update", "remove"],
  },
  {
    resource: { db: DB_NAME, collection: "materiales" },
    actions: ["find", "insert", "update", "remove"],
  },
  {
    resource: { db: DB_NAME, collection: "salasView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "mantenimientosView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "actividadesView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "materialesView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "usuariosView" },
    actions: ["find"],
  },
]);

recreateRole("Organizador", [
  {
    resource: { db: DB_NAME, collection: "salas" },
    actions: ["find", "update"],
  },
  {
    resource: { db: DB_NAME, collection: "mantenimientos" },
    actions: ["find", "insert", "update"],
  },
  {
    resource: { db: DB_NAME, collection: "actividades" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "materiales" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "salasView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "mantenimientosView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "actividadesView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "materialesView" },
    actions: ["find"],
  },
  {
    resource: { db: DB_NAME, collection: "usuariosView" },
    actions: ["find"],
  },
]);
