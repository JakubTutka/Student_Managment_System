-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 13, 2022 at 07:58 PM
-- Server version: 8.0.26
-- PHP Version: 8.0.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `s402128`
--

DELIMITER $$
--
-- Functions
--
CREATE DEFINER=`s402128`@`localhost` FUNCTION `create_email` (`name` VARCHAR(45), `surname` VARCHAR(45), `type` VARCHAR(45)) RETURNS VARCHAR(103) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci BEGIN
	DECLARE user_email VARCHAR(103);
    DECLARE c INT;
    
   	SELECT count(*) INTO c FROM users WHERE first_name=name AND last_name=surname;
    IF c>0 THEN
    	SET user_email = CONCAT(name,'.',surname,c,'@',type,'.usos.edu.pl');
    ELSE
    	SET user_email = CONCAT(name,'.',surname,'@',type,'.usos.edu.pl');
    END IF;
    RETURN user_email;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `buildings`
--

CREATE TABLE `buildings` (
  `building_id` int NOT NULL,
  `number` varchar(4) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `faculty_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `buildings`
--

INSERT INTO `buildings` (`building_id`, `number`, `address`, `faculty_id`) VALUES
(1, 'A-1', 'Ul. Reymonta 22, Kraków', 10),
(3, 'A-2', 'Ul. Mickewicza 30, Kraków', 14),
(4, 'D17', 'ul. Kawiory 21', 10);

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `course_id` int NOT NULL,
  `name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `creator_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`course_id`, `name`, `description`, `creator_id`) VALUES
(36, 'przykładowy', 'amen', 10),
(37, 'Przyklad', 'przyklad\r\n', 10),
(38, 'Bazy Danych', 'Postgresik tak o', 32),
(39, 'TESTOWY KURSIK', 'AAA', 23),
(40, 'BAZY DANYCH TELEINFORMATYKA', 'aaaaaaaaaaaaaaaaaaaaaa', 16);

-- --------------------------------------------------------

--
-- Table structure for table `faculties`
--

CREATE TABLE `faculties` (
  `faculty_id` int NOT NULL,
  `name_short` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name_full` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `faculties`
--

INSERT INTO `faculties` (`faculty_id`, `name_short`, `name_full`, `description`) VALUES
(10, 'WI', 'Wydział Informatyki', 'Wydział ten oferuje nauke w zawodach związanych z ogólnie pojętą branżą IT. Dostępne są 2 kierunki: Informatyka oraz Teleinformatyka'),
(12, 'WH', 'Wydział Humanistyczny', 'Nauka na naszym wydziale związana jest z przedmiotami humanistycznymi. Znajdziesz tutaj kierunki takie jak kulturoznastwo, czy tez informatyka społeczna.'),
(13, 'WRiA', 'Wydział Robotyki i Automatyki', 'Wydział ten ma w swojej ofercie wiele ciekawych kierunków związanych z budowaniem robotów oraz tak zwaną automatyzacją.'),
(14, 'WZ', 'Wydział Zarządzania', 'Tutaj uczymy się zarządzać ludźmi, klubami piłkarskimi takimi jak Wielka Wisła Kraków i innymi ciekawymi zagadnieniami.'),
(15, 'WIMIR', 'Wydział Inżynierii Mechanicznej i Robotyki', 'Ten wydział nazywany jest często zmorą studentów, chociaż i tak każdy go kojarzy z pewną rymowanką. '),
(17, 'WO', 'Wydział Odlewnictwa', 'Na owym wydziale możesz nauczyć się odlewania armat czy też kilofów.'),
(18, 'WFIIS', 'Wydział Fizyki i Informatyki Stosowanej', 'Tutaj możesz nauczyć się fizyki lub też informatyki. Ciekawe doświadczenia fizyczne stoją przed tobą otworem.');

-- --------------------------------------------------------

--
-- Table structure for table `student_marks`
--

CREATE TABLE `student_marks` (
  `mark_id` int NOT NULL,
  `value` enum('2.0','3.0','3.5','4.0','4.5','5.0') COLLATE utf8mb4_unicode_ci NOT NULL,
  `value_number` decimal(10,0) NOT NULL,
  `date` datetime NOT NULL,
  `student_id` int NOT NULL,
  `course_id` int NOT NULL,
  `professor_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `student_marks`
--

INSERT INTO `student_marks` (`mark_id`, `value`, `value_number`, `date`, `student_id`, `course_id`, `professor_id`) VALUES
(52, '4.0', '4', '2022-02-10 09:46:19', 14, 36, 10),
(53, '4.5', '5', '2022-02-10 09:46:21', 14, 36, 10),
(54, '5.0', '5', '2022-02-10 09:46:23', 14, 36, 10),
(55, '5.0', '5', '2022-02-10 09:47:03', 15, 36, 10),
(56, '5.0', '5', '2022-02-10 09:47:05', 15, 36, 10),
(57, '5.0', '5', '2022-02-10 09:47:06', 15, 36, 10),
(58, '3.0', '3', '2022-02-10 09:47:12', 18, 36, 10),
(59, '3.0', '3', '2022-02-10 09:47:13', 18, 36, 10),
(60, '2.0', '2', '2022-02-10 09:47:14', 18, 36, 10),
(65, '3.0', '3', '2022-02-10 10:07:49', 22, 37, 10),
(66, '2.0', '2', '2022-02-10 10:17:00', 14, 38, 32),
(68, '5.0', '5', '2022-02-10 19:45:58', 21, 39, 23),
(69, '4.0', '4', '2022-02-11 15:44:50', 19, 40, 16);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `email` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `creation_date` datetime NOT NULL,
  `type_of_user` enum('Student','Pracownik','Student/Pracownik') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `degree` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_polish_ci NOT NULL,
  `faculty_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `email`, `password`, `first_name`, `last_name`, `creation_date`, `type_of_user`, `degree`, `faculty_id`) VALUES
(10, 'konrad.zaworski@usos.edu.pl', 'pbkdf2:sha256:260000$clBbaoN6ng4rT3lA$fc92922fad7461d2cc6971a3279bc7d6f1cd17bc3396869d25e8d571cba7118b', 'Konrad', 'Zaworski', '2022-02-07 13:09:28', 'Pracownik', 'Mgr. Inż', 10),
(12, 'jakub.tutka@usos.edu.pl', 'pbkdf2:sha256:260000$cwHNTP2AzmQNSTwU$3d32ff413662146ce2054c52e19e29c98be1b131542b0db47b08b76a7b921daa', 'Jakub', 'Tutka', '2022-02-07 15:35:51', 'Student', 'Brak', 12),
(13, 'mikołaj.sztaba@usos.edu.pl', 'pbkdf2:sha256:260000$wcE8wjmXqDWpuWtJ$0953e52a9a551a3c18beb346dc298137e78745c660d025235a58e619c66b0517', 'Mikołaj', 'Sztaba', '2022-02-07 15:36:07', 'Student', 'Brak', 14),
(14, 'piotr.węgrzyn@usos.edu.pl', 'pbkdf2:sha256:260000$yHKIbygBYSyf1HIO$ca5ce602eb61d43899eee7fa4250be9a4c13ac0a2f16f10983ec73b269458d6f', 'Piotr', 'Węgrzyn', '2022-02-07 15:36:26', 'Student', 'Brak', 10),
(15, 'piotr.kurasiewicz@usos.edu.pl', 'pbkdf2:sha256:260000$8E5pXpGpOhNluLsD$e2e58c34f2b6719d94d37fcc37977a26017951370b3341ab4d542829c779756d', 'Piotr', 'Kurasiewicz', '2022-02-07 15:38:36', 'Student', 'Brak', 10),
(16, 'marek.sikora@usos.edu.pl', 'pbkdf2:sha256:260000$DCd7Ge1j4vDgnOxs$f3b331b87ade158a5487666cd12819219436e527be76463fa7fda58f119813d8', 'Marek', 'Sikora', '2022-02-07 18:15:51', 'Pracownik', 'Dr. Inż', 13),
(18, 'pawel.baluszynski@usos.edu.pl', 'pbkdf2:sha256:260000$jOtyjPrwViQflz1D$fe273587a499e708d657389d56a86adc68eb8266f98ee94e4df76023c6c0b197', 'Pawel', 'Baluszynski', '2022-02-07 18:17:57', 'Student', 'Brak', 10),
(19, 'kamil.sobolak@usos.edu.pl', 'pbkdf2:sha256:260000$BZCnDVla8fJoCEJx$c18938089a6b8dd06fca048169830ef28bd017080d079e09fa8c7ca731f036af', 'Kamil', 'Sobolak', '2022-02-07 18:18:12', 'Student', 'Brak', 13),
(20, 'kacper.zemla@usos.edu.pl', 'pbkdf2:sha256:260000$W2TDFBaJhiuL8bd0$0650342b0a2c98d7d862d823d1ea7982f5a5f4d4a7f2c5cca3c863ad69007ee4', 'Kacper', 'Zemla', '2022-02-07 18:18:24', 'Student', 'Brak', 13),
(21, 'kacper.tutka@usos.edu.pl', 'pbkdf2:sha256:260000$JFoaKoqYvCtyHyhU$4a408a0d8e5c4e7af27b2e461eb43bd6e1c33886ff2236a23d259cc73d96f218', 'Kacper', 'Tutka', '2022-02-08 09:26:30', 'Student', 'Brak', 10),
(22, 'jakub.żelazko@usos.edu.pl', 'pbkdf2:sha256:260000$tdfCTmgAROW5adYp$40d12229fc96f40126b8111a21b8688aab3f4fcac6d977441bc219f8a0a100fe', 'Jakub', 'Żelazko', '2022-02-08 09:26:45', 'Student', 'Brak', 10),
(23, 'andrzej.matiolański@usos.edu.pl', 'pbkdf2:sha256:260000$7tkL3zhRAuJqhqJu$cdfff6bf81bffbc30ad954eae4f83695ffd96c416cd542418fd838973135a58c', 'Andrzej', 'Matiolański', '2022-02-08 12:30:00', 'Pracownik', 'Dr. Inż', 10),
(24, 'jakub.tutka1@student.usos.edu.pl', 'pbkdf2:sha256:260000$HqFtmdAgEGDlfKwn$a4ed6c06c2ff73d04652842f8fe31e906a4c28620588e44615e4f6c9b1d2ce53', 'Jakub', 'Tutka', '2022-02-08 14:30:53', 'Student', 'Brak', 13),
(25, 'stanisław.stoch@pracownik.usos.edu.pl', 'pbkdf2:sha256:260000$hNpF264LVQKBBxud$c71d32d877d02b9986f72b5712cb60027e7b758d2ef749df7d57858dee0d44b3', 'Stanisław', 'Stoch', '2022-02-08 14:31:20', 'Pracownik', 'Dr. Inż', 14),
(26, 'mikołaj.sztaba1@student.usos.edu.pl', 'pbkdf2:sha256:260000$tV9XJwCnuZkxWku5$50e6f966c645219fb354f02d1c4aeab774652a0c1f906d1d30f9c07b57ad0701', 'Mikołaj', 'Sztaba', '2022-02-08 18:49:32', 'Student', 'Brak', 12),
(27, 'andrzej.jajszczyk@pracownik.usos.edu.pl', 'pbkdf2:sha256:260000$N20MsE9iAM5Soc1e$738f1cfb5f4fbd18d72f490cd18d774a545b06ed4dcb6bd19ea15edab391dcac', 'Andrzej', 'Jajszczyk', '2022-02-09 09:36:21', 'Pracownik', 'Prof. Dr. Hab. Inż.', 10),
(29, 'marek.kwak@student.usos.edu.pl', 'pbkdf2:sha256:260000$H2jrklHz4RfbkXa2$b3c5f94a4a0491274f4d89b14d4f3f1831bc6a6b7e29c60ed63a3ad5d843b227', 'Marek', 'Kwak', '2022-02-09 22:25:14', 'Student', 'Brak', 10),
(30, 'mikołaj.sztaba2@student.usos.edu.pl', 'pbkdf2:sha256:260000$UsHhCEdcuCskuOYO$33a6454618ce3e436d7f2f256bbbb0f7f173b496ff8236d6beebdcfe612d4f1a', 'Mikołaj', 'Sztaba', '2022-02-09 22:26:01', 'Student', 'Brak', 13),
(31, 'ola.mardaus@student.usos.edu.pl', 'pbkdf2:sha256:260000$irM2vm1ktiA69SPf$c4246f754a964f7055bcf412bafd67c827bd531343296ff4de14e17a01ec2b6d', 'Ola', 'Mardaus', '2022-02-09 22:26:34', 'Student', 'Brak', 10),
(32, 'marek.sikora1@pracownik.usos.edu.pl', 'pbkdf2:sha256:260000$x4wKg1rpmZtLrWNE$c2c7e8d8be1409957a8298a8f8461c026e47af2f048cea2ae7e7a35e59ef9941', 'Marek', 'Sikora', '2022-02-10 10:13:39', 'Pracownik', 'Dr. Inż.', 10),
(33, 'mikołaj.aaa@student.usos.edu.pl', 'pbkdf2:sha256:260000$15Zr4rKGrYLMULSw$0dd149740d56a2b416b8fae9a8c5979622237fe962810e6bb4c9a34028fa163f', 'Mikołaj', 'aaa', '2022-02-10 19:03:55', 'Student', 'Brak', 10),
(34, 'aaaaaa.aaaaaa@student.usos.edu.pl', 'pbkdf2:sha256:260000$A3AMP8pcWcVizfYs$8478e157e56063a33fd15b4d237e916bf379b057ee1161a91cc2ad5c7a741b38', 'aaaaaa', 'aaaaaa', '2022-02-10 19:34:14', 'Student', 'Brak', 10),
(37, 'rokoko.rokoko@student.usos.edu.pl', 'pbkdf2:sha256:260000$wZQ2xS2YGt9eH6Ja$7e05513866ee302e182fc2a090dabb738b0062d534c494f0ef8300afc25afc44', 'ROKOKO', 'ROKOKO', '2022-02-11 14:38:56', 'Student', 'Brak', 10),
(38, 'adam.nowak@pracownik.usos.edu.pl', 'pbkdf2:sha256:260000$OsK2DtsUgNcQTVBw$8ec6018c8c8ca4f9bf67bff962cfd0c70608efdad44443a56acbc919e82c69c0', 'Adam', 'Nowak', '2022-02-11 14:40:29', 'Pracownik', 'Magister', 13);

-- --------------------------------------------------------

--
-- Table structure for table `user_courses`
--

CREATE TABLE `user_courses` (
  `course_id` int NOT NULL,
  `user_id` int NOT NULL,
  `role` enum('Student','Pracownik') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `user_courses`
--

INSERT INTO `user_courses` (`course_id`, `user_id`, `role`) VALUES
(36, 10, 'Pracownik'),
(36, 14, 'Student'),
(36, 15, 'Student'),
(36, 18, 'Student'),
(36, 27, 'Pracownik'),
(36, 29, 'Student'),
(37, 10, 'Pracownik'),
(37, 22, 'Student'),
(37, 27, 'Pracownik'),
(38, 14, 'Student'),
(38, 18, 'Student'),
(38, 32, 'Pracownik'),
(39, 10, 'Pracownik'),
(39, 21, 'Student'),
(39, 23, 'Pracownik'),
(39, 27, 'Pracownik'),
(39, 32, 'Pracownik'),
(40, 16, 'Pracownik'),
(40, 19, 'Student'),
(40, 24, 'Student'),
(40, 30, 'Student'),
(40, 38, 'Pracownik');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `buildings`
--
ALTER TABLE `buildings`
  ADD PRIMARY KEY (`building_id`),
  ADD KEY `fk_buildings_faculties1_idx` (`faculty_id`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`course_id`),
  ADD KEY `creator_id` (`creator_id`);

--
-- Indexes for table `faculties`
--
ALTER TABLE `faculties`
  ADD PRIMARY KEY (`faculty_id`),
  ADD UNIQUE KEY `faculty_id_UNIQUE` (`faculty_id`);

--
-- Indexes for table `student_marks`
--
ALTER TABLE `student_marks`
  ADD PRIMARY KEY (`mark_id`),
  ADD KEY `fk_student_marks_users1_idx` (`student_id`),
  ADD KEY `fk_student_marks_courses1_idx` (`course_id`),
  ADD KEY `fk_student_marks_users2_idx` (`professor_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email_UNIQUE` (`email`),
  ADD UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  ADD KEY `fk_users_faculties_idx` (`faculty_id`);

--
-- Indexes for table `user_courses`
--
ALTER TABLE `user_courses`
  ADD PRIMARY KEY (`course_id`,`user_id`),
  ADD KEY `fk_courses_has_users_users1_idx` (`user_id`),
  ADD KEY `fk_courses_has_users_courses1_idx` (`course_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `buildings`
--
ALTER TABLE `buildings`
  MODIFY `building_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `course_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `faculties`
--
ALTER TABLE `faculties`
  MODIFY `faculty_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `student_marks`
--
ALTER TABLE `student_marks`
  MODIFY `mark_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `buildings`
--
ALTER TABLE `buildings`
  ADD CONSTRAINT `fk_buildings_faculties1` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `student_marks`
--
ALTER TABLE `student_marks`
  ADD CONSTRAINT `fk_student_marks_courses1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_student_marks_users1` FOREIGN KEY (`student_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_student_marks_users2` FOREIGN KEY (`professor_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_faculties` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_courses`
--
ALTER TABLE `user_courses`
  ADD CONSTRAINT `fk_courses_has_users_courses1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_courses_has_users_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
