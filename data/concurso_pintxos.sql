
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
CREATE DATABASE IF NOT EXISTS `concurso_pintxos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
USE `concurso_pintxos`;


--
-- Procedimientos crear para cada usuario 1 voto por categoria
--
DELIMITER $$

DROP PROCEDURE IF EXISTS `generar_votos`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `generar_votos`()
BEGIN
    DECLARE uid INT DEFAULT 1;
    DECLARE cid INT;
    DECLARE pid INT;

    -- Recorremos los 20 usuarios
    WHILE uid <= 20 DO
        SET cid = 1;
        WHILE cid <= 5 DO

            -- Solo genera voto si no existe ya
            IF NOT EXISTS (
                SELECT 1
                FROM votos
                WHERE id_usuario = uid AND id_categoria = cid
            ) THEN
                -- Elegimos un pintxo aleatorio de esa categoría
                SELECT id_pintxo
                INTO pid
                FROM pintxos
                WHERE id_categoria = cid
                ORDER BY RAND()
                LIMIT 1;

                -- Insertamos el voto
                INSERT INTO votos (id_usuario, id_pintxo, id_categoria)
                VALUES (uid, pid, cid);
            END IF;

            SET cid = cid + 1;
        END WHILE;
        SET uid = uid + 1;
    END WHILE;
END$$

DELIMITER ;

--
-- Procedimientos crear 20 votos al azar
--
DELIMITER $$

DROP PROCEDURE IF EXISTS `generar_20_votos`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `generar_20_votos`()
BEGIN
    DECLARE votos_generados INT DEFAULT 0;
    DECLARE uid INT;
    DECLARE cid INT;
    DECLARE pid INT;

    -- Repetir hasta insertar 20 votos nuevos
    WHILE votos_generados < 20 DO
        -- Seleccionar un usuario aleatorio (1 a 20)
        SET uid = FLOOR(1 + (RAND() * 20));

        -- Seleccionar una categoría aleatoria (1 a 5)
        SET cid = FLOOR(1 + (RAND() * 5));

        -- Verificamos si ese usuario ya votó en esa categoría
        IF NOT EXISTS (
            SELECT 1
            FROM votos
            WHERE id_usuario = uid AND id_categoria = cid
        ) THEN
            -- Elegimos un pintxo aleatorio de esa categoría
            SELECT id_pintxo
            INTO pid
            FROM pintxos
            WHERE id_categoria = cid
            ORDER BY RAND()
            LIMIT 1;

            -- Insertamos el voto
            INSERT INTO votos (id_usuario, id_pintxo, id_categoria)
            VALUES (uid, pid, cid);

            -- Incrementamos el contador de votos
            SET votos_generados = votos_generados + 1;
        END IF;
    END WHILE;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bares`
--

DROP TABLE IF EXISTS `bares`;
CREATE TABLE IF NOT EXISTS `bares` (
  `id_bar` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `nombre_bar` varchar(100) NOT NULL,
  `direccion` varchar(150) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `bares`
--

INSERT INTO `bares` (`id_bar`, `nombre_bar`, `direccion`) VALUES
(1, 'Bar Charly', 'Plaza Nueva, 8'),
(2, 'Restaurante Víctor Montes', 'Plaza Nueva, 12'),
(3, 'Txiriboga', 'Andra Maria, 13'),
(4, 'Gure Toki', 'Plaza Nueva, 12'),
(5, 'Sorginzulo', 'Plaza Nueva, 14'),
(6, 'La Olla', 'Plaza Nueva, 2'),
(7, 'Bar Fermín', 'Iturribide, 4'),
(8, 'Bar Urdiña', 'Plaza Nueva, 5'),
(9, 'Zaharra', 'Barria, 4'),
(10, 'GastroBar 42', 'Av. Gastronómica 42'),
(11, 'Zazpiak Bat Tavern', 'Calle Especias 3'),
(12, 'Paladar Urbano', 'Calle Gourmet 99');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

DROP TABLE IF EXISTS `categorias`;
CREATE TABLE IF NOT EXISTS `categorias` (
  `id_categoria` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre_categoria` varchar(50) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

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

DROP TABLE IF EXISTS `pintxos`;
CREATE TABLE IF NOT EXISTS `pintxos` (
  `id_pintxo` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre_pintxo` varchar(100) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `id_bar` int(11) NOT NULL,
  CONSTRAINT `fk_pintxos_categoria` FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
  CONSTRAINT `fk_pintxos_bar` FOREIGN KEY (id_bar) REFERENCES bares(id_bar) ON DELETE CASCADE 
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

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
-- Estructura de tabla para la tabla `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id_rol` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `rol` varchar(50) NOT NULL COMMENT 'Nombre del rol (ej: Administrador, Editor, Lector)',
  UNIQUE KEY `rol` (`rol`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

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

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nombre_usuario` varchar(100) NOT NULL,
  `email_usuario` varchar(100) NOT NULL,
  `pass_usuario` varchar(45) NOT NULL,
  `estado_usuario` enum('activo','inactivo','pendiente') DEFAULT 'activo',
  `id_rol` int(11) NOT NULL,
  UNIQUE KEY `email_usuario` (`email_usuario`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `fk_usuarios_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE RESTRICT 
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

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
(20, 'Víctor Peña', 'victor@example.com', 'victorpena', 'inactivo', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `votos`
--

DROP TABLE IF EXISTS `votos`;
CREATE TABLE IF NOT EXISTS `votos` (
  `id_voto` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `id_usuario` int(11) NOT NULL,
  `id_pintxo` int(11) NOT NULL,
  `fecha_voto` datetime NOT NULL DEFAULT current_timestamp(),
  `id_categoria` int(11) NOT NULL,
  UNIQUE KEY `id_usuario` (`id_usuario`,`id_categoria`),
  KEY `id_pintxo` (`id_pintxo`),
  KEY `id_categoria` (`id_categoria`),
  CONSTRAINT `fk_votos_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE, 
  CONSTRAINT `fk_votos_pintxo` FOREIGN KEY (`id_pintxo`) REFERENCES `pintxos` (`id_pintxo`) ON DELETE CASCADE, 
  CONSTRAINT `fk_votos_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE CASCADE 
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `votos`
--

INSERT INTO `votos` (`id_voto`, `id_usuario`, `id_pintxo`, `fecha_voto`, `id_categoria`) VALUES
(1, 1, 10, '2025-05-12 19:54:07', 1),
(2, 1, 14, '2025-05-12 19:54:07', 2),
(3, 1, 27, '2025-05-12 19:54:07', 3),
(4, 1, 43, '2025-05-12 19:54:07', 4),
(5, 1, 55, '2025-05-12 19:54:07', 5),
(6, 2, 6, '2025-05-12 19:54:07', 1),
(7, 2, 14, '2025-05-12 19:54:07', 2),
(8, 2, 35, '2025-05-12 19:54:07', 3),
(9, 2, 47, '2025-05-12 19:54:07', 4),
(10, 2, 59, '2025-05-12 19:54:07', 5),
(11, 3, 1, '2025-05-12 19:54:07', 1),
(12, 3, 17, '2025-05-12 19:54:07', 2),
(13, 3, 34, '2025-05-12 19:54:07', 3),
(14, 3, 43, '2025-05-12 19:54:07', 4),
(15, 3, 49, '2025-05-12 19:54:07', 5),
(16, 4, 4, '2025-05-12 19:54:07', 1),
(17, 4, 16, '2025-05-12 19:54:07', 2),
(18, 4, 36, '2025-05-12 19:54:07', 3),
(19, 4, 38, '2025-05-12 19:54:07', 4),
(20, 4, 59, '2025-05-12 19:54:07', 5),
(21, 5, 4, '2025-05-12 19:54:07', 1),
(22, 5, 22, '2025-05-12 19:54:07', 2),
(23, 5, 31, '2025-05-12 19:54:07', 3),
(24, 5, 43, '2025-05-12 19:54:07', 4),
(25, 5, 52, '2025-05-12 19:54:07', 5),
(26, 6, 1, '2025-05-12 19:54:07', 1),
(27, 6, 18, '2025-05-12 19:54:07', 2),
(28, 6, 27, '2025-05-12 19:54:07', 3),
(29, 6, 43, '2025-05-12 19:54:07', 4),
(30, 6, 51, '2025-05-12 19:54:07', 5),
(31, 7, 8, '2025-05-12 19:54:07', 1),
(32, 7, 13, '2025-05-12 19:54:07', 2),
(33, 7, 36, '2025-05-12 19:54:07', 3),
(34, 7, 46, '2025-05-12 19:54:07', 4),
(35, 7, 59, '2025-05-12 19:54:07', 5),
(36, 8, 8, '2025-05-12 19:54:07', 1),
(37, 8, 17, '2025-05-12 19:54:07', 2),
(38, 8, 25, '2025-05-12 19:54:07', 3),
(39, 8, 41, '2025-05-12 19:54:07', 4),
(40, 8, 51, '2025-05-12 19:54:07', 5),
(41, 9, 4, '2025-05-12 19:54:07', 1),
(42, 9, 23, '2025-05-12 19:54:07', 2),
(43, 9, 30, '2025-05-12 19:54:07', 3),
(44, 9, 43, '2025-05-12 19:54:07', 4),
(45, 9, 50, '2025-05-12 19:54:07', 5),
(46, 10, 9, '2025-05-12 19:54:07', 1),
(47, 10, 13, '2025-05-12 19:54:07', 2),
(48, 10, 27, '2025-05-12 19:54:07', 3),
(49, 10, 48, '2025-05-12 19:54:07', 4),
(50, 10, 50, '2025-05-12 19:54:07', 5),
(51, 11, 6, '2025-05-12 19:54:07', 1),
(52, 11, 14, '2025-05-12 19:54:07', 2),
(53, 11, 34, '2025-05-12 19:54:07', 3),
(54, 11, 37, '2025-05-12 19:54:07', 4),
(55, 11, 55, '2025-05-12 19:54:07', 5),
(56, 12, 7, '2025-05-12 19:54:07', 1),
(57, 12, 19, '2025-05-12 19:54:07', 2),
(58, 12, 26, '2025-05-12 19:54:07', 3),
(59, 12, 45, '2025-05-12 19:54:07', 4),
(60, 12, 59, '2025-05-12 19:54:07', 5),
(61, 13, 9, '2025-05-12 19:54:07', 1),
(62, 13, 16, '2025-05-12 19:54:07', 2),
(63, 13, 27, '2025-05-12 19:54:07', 3),
(64, 13, 48, '2025-05-12 19:54:07', 4),
(65, 13, 50, '2025-05-12 19:54:07', 5),
(66, 14, 12, '2025-05-12 19:54:07', 1),
(67, 14, 22, '2025-05-12 19:54:07', 2),
(68, 14, 31, '2025-05-12 19:54:07', 3),
(69, 14, 45, '2025-05-12 19:54:07', 4),
(70, 14, 50, '2025-05-12 19:54:07', 5),
(71, 15, 9, '2025-05-12 19:54:07', 1),
(72, 15, 21, '2025-05-12 19:54:07', 2),
(73, 15, 31, '2025-05-12 19:54:07', 3),
(74, 15, 44, '2025-05-12 19:54:07', 4),
(75, 15, 57, '2025-05-12 19:54:07', 5),
(76, 16, 8, '2025-05-12 19:54:07', 1),
(77, 16, 13, '2025-05-12 19:54:07', 2),
(78, 16, 25, '2025-05-12 19:54:07', 3),
(79, 16, 38, '2025-05-12 19:54:07', 4),
(80, 16, 59, '2025-05-12 19:54:07', 5),
(81, 17, 6, '2025-05-12 19:54:07', 1),
(82, 17, 20, '2025-05-12 19:54:07', 2),
(83, 17, 27, '2025-05-12 19:54:07', 3),
(84, 17, 39, '2025-05-12 19:54:07', 4),
(85, 17, 60, '2025-05-12 19:54:07', 5),
(86, 18, 2, '2025-05-12 19:54:07', 1),
(87, 18, 15, '2025-05-12 19:54:07', 2),
(88, 18, 26, '2025-05-12 19:54:07', 3),
(89, 18, 48, '2025-05-12 19:54:07', 4),
(90, 18, 55, '2025-05-12 19:54:07', 5),
(91, 19, 4, '2025-05-12 19:54:07', 1),
(92, 19, 21, '2025-05-12 19:54:07', 2),
(93, 19, 26, '2025-05-12 19:54:07', 3),
(94, 19, 46, '2025-05-12 19:54:07', 4),
(95, 19, 50, '2025-05-12 19:54:07', 5),
(96, 20, 11, '2025-05-12 19:54:07', 1),
(97, 20, 13, '2025-05-12 19:54:07', 2),
(98, 20, 32, '2025-05-12 19:54:07', 3),
(99, 20, 48, '2025-05-12 19:54:07', 4),
(100, 20, 52, '2025-05-12 19:54:07', 5);

-- --------------------------------------------------------

--
-- VISTAS REALES
--

--
-- Vista `vista_votos_detalle`
--
DROP VIEW IF EXISTS `vista_votos_detalle`;
CREATE OR REPLACE VIEW `vista_votos_detalle` AS
SELECT
    v.id_voto,  -- Agregamos identificador único
    u.nombre_usuario AS nombre,
    c.nombre_categoria AS categoria,
    p.nombre_pintxo AS pintxo,
    b.nombre_bar AS bar
FROM votos v
JOIN usuarios u ON v.id_usuario = u.id_usuario
JOIN pintxos p ON v.id_pintxo = p.id_pintxo
JOIN categorias c ON p.id_categoria = c.id_categoria
JOIN bares b ON p.id_bar = b.id_bar;

-- --------------------------------------------------------

--
-- Vista `ranking_pintxos_por_categoria` (antes llamada `ranking_por_categoria`)
--
DROP VIEW IF EXISTS `ranking_pintxos_por_categoria`;
CREATE OR REPLACE VIEW `ranking_pintxos_por_categoria` AS
SELECT
    c.nombre_categoria,
    p.nombre_pintxo,
    b.nombre_bar,
    COUNT(v.id_voto) AS total_votos
FROM votos v
JOIN pintxos p ON v.id_pintxo = p.id_pintxo
JOIN categorias c ON p.id_categoria = c.id_categoria
JOIN bares b ON p.id_bar = b.id_bar
GROUP BY p.id_pintxo, c.nombre_categoria, b.nombre_bar
ORDER BY c.nombre_categoria, total_votos DESC;

-- --------------------------------------------------------

--
-- Vista `ranking_bares_por_votos` (antes llamada `ranking_por_bar`)
--
DROP VIEW IF EXISTS `ranking_bares_por_votos`;
CREATE OR REPLACE VIEW `ranking_bares_por_votos` AS
SELECT
    b.nombre_bar,
    COUNT(v.id_voto) AS total_votos
FROM votos v
JOIN pintxos p ON v.id_pintxo = p.id_pintxo
JOIN bares b ON p.id_bar = b.id_bar
GROUP BY b.id_bar, b.nombre_bar
ORDER BY total_votos DESC;

-- --------------------------------------------------------


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;