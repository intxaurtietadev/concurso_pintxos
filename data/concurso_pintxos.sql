-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 15-05-2025 a las 09:33:05
-- Versión del servidor: 10.11.11-MariaDB-0ubuntu0.24.04.2
-- Versión de PHP: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `concurso_pintxos`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `generar_votos` ()   BEGIN
    DECLARE uid INT$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bares`
--

CREATE TABLE `bares` (
  `id_bar` int(11) NOT NULL,
  `nombre_bar` varchar(100) NOT NULL,
  `direccion` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `bares`
--

INSERT INTO `bares` (`id_bar`, `nombre_bar`, `direccion`) VALUES
(1, 'Bar Charly', 'Plaza Nueva, 8'),
(2, 'Restaurante Víctor Montes', 'Plaza Nueva, 8'),
(3, 'Txiriboga', 'Andra Maria, 13'),
(4, 'Gure Toki', 'Plaza Nueva, 12'),
(5, 'Sorginzulo', 'Plaza Nueva, 12'),
(6, 'La Olla', 'Plaza Nueva, 2'),
(7, 'Bar Fermín', 'Iturribide, 4'),
(8, 'Bar Urdiña', 'Plaza Nueva, 5'),
(9, 'Zaharra - Plaza Nueva', 'Barria, 4');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre_categoria` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre_categoria`) VALUES
(1, 'Tortilla'),
(2, 'Champiñón'),
(3, 'Atún'),
(4, 'Sándwich'),
(5, 'Vegano');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pintxos`
--

CREATE TABLE `pintxos` (
  `id_pintxo` int(11) NOT NULL,
  `nombre_pintxo` varchar(100) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `id_bar` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `pintxos`
--

INSERT INTO `pintxos` (`id_pintxo`, `nombre_pintxo`, `id_categoria`, `id_bar`) VALUES
(1, 'Tortilla Tradicional', 1, 1),
(2, 'Tortilla de Patata con Cebolla', 1, 2),
(3, 'Tortilla de Espinacas', 1, 3),
(4, 'Tortilla Francesa', 1, 4),
(5, 'Tortilla de Chorizo', 1, 5),
(6, 'Tortilla rellena', 1, 6),
(7, 'Tortilla de Queso', 1, 7),
(8, 'Tortilla de Bacalao', 1, 8),
(9, 'Tortilla de Calabacín', 1, 9),
(10, 'Tortilla Picante', 1, 10),
(11, 'Tortilla con Trufa', 1, 11),
(12, 'Tortilla Mediterránea', 1, 12),
(13, 'Champiñones al Ajillo', 2, 1),
(14, 'Champiñones rellenos de jamón y queso', 2, 2),
(15, 'Mini hamburguesas de champiñón', 2, 3),
(16, 'Brocheta de champiñones, gambas y bacon', 2, 4),
(17, 'Tosta de Champiñones', 2, 5),
(18, 'Champiñones al Curry', 2, 6),
(19, 'Champiñones Empanados', 2, 7),
(20, 'Champiñones con foie gras', 2, 8),
(21, 'Revuelto de champiñones', 2, 9),
(22, 'Champiñón Trufado', 2, 10),
(23, 'Champiñones a la Plancha', 2, 11),
(24, 'Volován de champiñones a la crema', 2, 12),
(25, 'Mini empanadillas de atún', 3, 1),
(26, 'Ensaladilla de Atún', 3, 2),
(27, 'Brocheta de atún, tomate y aceituna', 3, 3),
(28, 'Gilda de Atún', 3, 4),
(29, 'Atún con pimiento rojo', 3, 5),
(30, 'Atún con queso crema y pepinillos', 3, 6),
(31, 'Atún con cebolla caramelizada', 3, 7),
(32, 'Atún con tomate cherry y albahaca', 3, 8),
(33, 'Tosta de atún con tapenade', 3, 9),
(34, 'Atún con Sésamo', 3, 10),
(35, 'Atún Marinado', 3, 11),
(36, 'Bocadillo de Atún', 3, 12),
(37, 'Sándwich Club', 4, 1),
(38, 'Sándwich de Pollo', 4, 2),
(39, 'Sándwich Vegetal', 4, 3),
(40, 'Sándwich Mixto', 4, 4),
(41, 'Sándwich Caprese', 4, 5),
(42, 'Sándwich Cubano', 4, 6),
(43, 'Sándwich de Queso Azul', 4, 7),
(44, 'Sándwich de Salmón', 4, 8),
(45, 'Sándwich de Huevo', 4, 9),
(46, 'Sándwich Americano', 4, 10),
(47, 'Sándwich de Bacon', 4, 11),
(48, 'Sándwich Ranchero', 4, 12),
(49, 'Patatas bravas con salsa de tomate picante', 5, 1),
(50, 'Berenjenas con miel', 5, 2),
(51, 'Gazpacho', 5, 3),
(52, 'Tosta de pisto', 5, 4),
(53, 'Empanadillas de tofu y espinacas', 5, 5),
(54, 'Papas arrugadas con mojo', 5, 6),
(55, 'Gilda Vegana', 5, 7),
(56, 'Hummus con Crudités', 5, 8),
(57, 'Pintxo de Escalivada', 5, 9),
(58, 'Croquetas Veganas', 5, 10),
(59, 'Banderilla de Frutas', 5, 11),
(60, 'Rollitos de Pepino Rellenos', 5, 12);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `ranking_por_bar`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `ranking_por_bar` (
`nombre_bar` varchar(100)
,`total_votos` bigint(21)
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `ranking_por_categoria`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `ranking_por_categoria` (
`nombre_categoria` varchar(50)
,`nombre_pintxo` varchar(100)
,`nombre_bar` varchar(100)
,`total_votos` bigint(21)
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `rol` varchar(50) NOT NULL COMMENT 'Nombre del rol (ej: Administrador, Editor, Lector)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `rol`) VALUES
(1, 'Administrador'),
(2, 'Editor'),
(3, 'Lector');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `email_usuario` varchar(100) NOT NULL,
  `pass_usuario` varchar(45) NOT NULL,
  `estado_usuario` enum('activo','inactivo','pendiente') DEFAULT 'activo',
  `id_rol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre_usuario`, `email_usuario`, `pass_usuario`, `estado_usuario`, `id_rol`) VALUES
(1, 'Ana García', 'ana@example.com', 'anagarcia', 'activo', 3),
(2, 'Luis Fernández', 'luis@example.com', 'luisfernandez', 'activo', 3),
(3, 'María López', 'maria@example.com', 'marialopez', 'activo', 3),
(4, 'Carlos Ruiz', 'carlos@example.com', 'carlosruiz', 'activo', 3),
(5, 'Lucía Gómez', 'lucia@example.com', 'luciagomez', 'activo', 3),
(6, 'Jorge Pérez', 'jorge@example.com', 'jorgeperez', 'activo', 3),
(7, 'Sara Torres', 'sara@example.com', 'saratorres', 'activo', 3),
(8, 'David Molina', 'david@example.com', 'davidmolina', 'activo', 3),
(9, 'Carmen Romero', 'carmen@example.com', 'carmenromero', 'activo', 3),
(10, 'Pablo León', 'pablo@example.com', 'pabloleon', 'activo', 3),
(11, 'Isabel Díaz', 'isabel@example.com', 'isabeldiaz', 'activo', 3),
(12, 'Andrés Ortega', 'andres@example.com', 'andresortega', 'activo', 3),
(13, 'Natalia Vargas', 'natalia@example.com', 'nataliavargas', 'activo', 3),
(14, 'Hugo Navarro', 'hugo@example.com', 'hugonavarro', 'activo', 3),
(15, 'Clara Sáez', 'clara@example.com', 'clarasaez', 'activo', 3),
(16, 'Rafael Moreno', 'rafael@example.com', 'rafaelmoreno', 'activo', 3),
(17, 'Elena Ramos', 'elena@example.com', 'elenaramos', 'activo', 3),
(18, 'Mario Castro', 'mario@example.com', 'mariocastro', 'activo', 3),
(19, 'Irene Herrera', 'irene@example.com', 'ireneherrera', 'activo', 2),
(20, 'Víctor Peña', 'victor@example.com', 'victorpena', 'inactivo', 3),
(21, 'thais', 'thais@example.com', 'NOT_SET_ANONYMOUS_VOTE', 'activo', 3),
(22, 'Erika', 'erika@ejemplo.com', 'NOT_SET_ANONYMOUS_VOTE', 'activo', 3),
(23, 'lucia', 'lucia@ejemplo.com', 'NOT_SET_ANONYMOUS_VOTE', 'activo', 3),
(24, 'bebe', 'bebejefazo@ejemplo.com', 'NOT_SET_ANONYMOUS_VOTE', 'activo', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `votos`
--

CREATE TABLE `votos` (
  `id_voto` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_pintxo` int(11) NOT NULL,
  `fecha_voto` datetime NOT NULL DEFAULT current_timestamp(),
  `id_categoria` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `votos`
--

INSERT INTO `votos` (`id_voto`, `id_usuario`, `id_pintxo`, `fecha_voto`, `id_categoria`) VALUES
(101, 24, 15, '2025-05-15 11:23:18', 2);

-- --------------------------------------------------------

--
-- Estructura para la vista `ranking_por_bar`
--
DROP TABLE IF EXISTS `ranking_por_bar`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ranking_por_bar`  AS SELECT `r`.`nombre_bar` AS `nombre_bar`, count(`v`.`id_voto`) AS `total_votos` FROM ((`votos` `v` join `pintxos` `p` on(`v`.`id_pintxo` = `p`.`id_pintxo`)) join `bares` `r` on(`p`.`id_bar` = `r`.`id_bar`)) GROUP BY `r`.`id_bar` ORDER BY count(`v`.`id_voto`) DESC ;

-- --------------------------------------------------------

--
-- Estructura para la vista `ranking_por_categoria`
--
DROP TABLE IF EXISTS `ranking_por_categoria`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `ranking_por_categoria`  AS SELECT `c`.`nombre_categoria` AS `nombre_categoria`, `p`.`nombre_pintxo` AS `nombre_pintxo`, `r`.`nombre_bar` AS `nombre_bar`, count(`v`.`id_voto`) AS `total_votos` FROM (((`votos` `v` join `pintxos` `p` on(`v`.`id_pintxo` = `p`.`id_pintxo`)) join `categorias` `c` on(`p`.`id_categoria` = `c`.`id_categoria`)) join `bares` `r` on(`p`.`id_bar` = `r`.`id_bar`)) GROUP BY `c`.`nombre_categoria`, `p`.`id_pintxo` ORDER BY `c`.`nombre_categoria` ASC, count(`v`.`id_voto`) DESC ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `bares`
--
ALTER TABLE `bares`
  ADD PRIMARY KEY (`id_bar`);

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `pintxos`
--
ALTER TABLE `pintxos`
  ADD PRIMARY KEY (`id_pintxo`),
  ADD KEY `id_categoria` (`id_categoria`),
  ADD KEY `id_bar` (`id_bar`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`),
  ADD UNIQUE KEY `rol` (`rol`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email_usuario` (`email_usuario`),
  ADD KEY `id_rol` (`id_rol`);

--
-- Indices de la tabla `votos`
--
ALTER TABLE `votos`
  ADD PRIMARY KEY (`id_voto`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`,`id_categoria`),
  ADD UNIQUE KEY `unique_voto_por_categoria` (`id_usuario`,`id_categoria`),
  ADD KEY `id_pintxo` (`id_pintxo`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `bares`
--
ALTER TABLE `bares`
  MODIFY `id_bar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `pintxos`
--
ALTER TABLE `pintxos`
  MODIFY `id_pintxo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `votos`
--
ALTER TABLE `votos`
  MODIFY `id_voto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
