use("admin");

const DB_NAME = "SalasMantenimiento";

function ensureMongoUser(username, password, roleName) {
  const roleExists = db.getSiblingDB(DB_NAME).getRole(roleName);
  const resolvedRoleName = roleExists ? roleName : roleName.replace("rol", "").replace("BD", "");
  const userExists = db.getUser(username);
  const desiredRoles = [{ role: resolvedRoleName, db: DB_NAME }];

  if (!userExists) {
    db.createUser({
      user: username,
      pwd: password,
      roles: desiredRoles,
    });
    return;
  }

  db.updateUser(username, {
    pwd: password,
    roles: desiredRoles,
  });
}

ensureMongoUser("admin.salas", "admin123", "rolAdministradorBD");
ensureMongoUser("tecnico.salas", "tecnico123", "rolTecnicoBD");
ensureMongoUser("organizador.salas", "organizador123", "rolOrganizadorBD");

use(DB_NAME);

db.usuarios.createIndex({ username: 1 }, { unique: true });

db.usuarios.updateOne(
  { username: "admin.salas" },
  {
    $set: {
      username: "admin.salas",
      password: "admin123",
      rol: "Administrador",
      estatus: "ACTIVO",
    }
  },
  { upsert: true }
);

db.usuarios.updateOne(
  { username: "tecnico.salas" },
  {
    $set: {
      username: "tecnico.salas",
      password: "tecnico123",
      rol: "Tecnico",
      estatus: "ACTIVO",
    }
  },
  { upsert: true }
);

db.usuarios.updateOne(
  { username: "organizador.salas" },
  {
    $set: {
      username: "organizador.salas",
      password: "organizador123",
      rol: "Organizador",
      estatus: "ACTIVO",
    }
  },
  { upsert: true }
);
