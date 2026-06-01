use("SalasMantenimiento");

db.createView("salasView", "salas", [
  {
    $project: {
      _id: 0,
      idSala: { $toString: "$_id" },
      nombre: 1,
      ubicacion: 1,
      capacidad: 1,
      estatus: 1,
      tipo: 1,
      idDepartamento: { $toString: "$idDepartamento" },
    },
  },
]);

db.createView("mantenimientosView", "mantenimientos", [
  {
    $project: {
      _id: 0,
      idMantenimiento: { $toString: "$_id" },
      estatus: 1,
      fechaInicio: 1,
      fechaFin: 1,
      idSala: { $toString: "$idSala" },
      actividades: {
        $map: {
          input: "$actividades",
          as: "idActividad",
          in: { $toString: "$$idActividad" },
        },
      },
    },
  },
]);

db.createView("actividadesView", "actividades", [
  {
    $project: {
      _id: 0,
      idActividad: { $toString: "$_id" },
      nombre: 1,
      descripcion: 1,
      completado: 1,
      observaciones: 1,
      idTecnico: { $toString: "$idTecnico" },
      materiales: {
        $map: {
          input: "$materiales",
          as: "material",
          in: {
            idMaterial: { $toString: "$$material.idMaterial" },
            cantidad: "$$material.cantidad",
          },
        },
      },
    },
  },
]);

db.createView("materialesView", "materiales", [
  {
    $project: {
      _id: 0,
      idMaterial: { $toString: "$_id" },
      nombre: 1,
      descripcion: 1,
      tipo: 1,
      unidadMedida: 1,
      cantidadUnidades: 1,
    },
  },
]);

db.createView("usuariosView", "usuarios", [
  {
    $project: {
      _id: 0,
      idUsuario: { $toString: "$_id" },
      username: 1,
      rol: 1,
      estatus: 1,
    },
  },
]);
