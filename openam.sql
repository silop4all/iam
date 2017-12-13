-- phpMyAdmin SQL Dump
-- version 4.2.7.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jul 25, 2016 at 03:09 PM
-- Server version: 5.6.20
-- PHP Version: 5.5.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `openam`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
`id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
`id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
`id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=58 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add content type', 4, 'add_contenttype'),
(11, 'Can change content type', 4, 'change_contenttype'),
(12, 'Can delete content type', 4, 'delete_contenttype'),
(13, 'Can add session', 5, 'add_session'),
(14, 'Can change session', 5, 'change_session'),
(15, 'Can delete session', 5, 'delete_session'),
(16, 'Can add site', 6, 'add_site'),
(17, 'Can change site', 6, 'change_site'),
(18, 'Can delete site', 6, 'delete_site'),
(19, 'Can add manager', 7, 'add_manager'),
(20, 'Can change manager', 7, 'change_manager'),
(21, 'Can delete manager', 7, 'delete_manager'),
(22, 'Can add profile', 8, 'add_profile'),
(23, 'Can change profile', 8, 'change_profile'),
(24, 'Can delete profile', 8, 'delete_profile'),
(25, 'Can add registration request', 9, 'add_registrationrequest'),
(26, 'Can change registration request', 9, 'change_registrationrequest'),
(27, 'Can delete registration request', 9, 'delete_registrationrequest'),
(28, 'Can add application', 10, 'add_application'),
(29, 'Can change application', 10, 'change_application'),
(30, 'Can delete application', 10, 'delete_application'),
(31, 'Can add application owner', 11, 'add_applicationowner'),
(32, 'Can change application owner', 11, 'change_applicationowner'),
(33, 'Can delete application owner', 11, 'delete_applicationowner'),
(34, 'Can add cors model', 12, 'add_corsmodel'),
(35, 'Can change cors model', 12, 'change_corsmodel'),
(36, 'Can delete cors model', 12, 'delete_corsmodel'),
(37, 'Can add role', 13, 'add_role'),
(38, 'Can change role', 13, 'change_role'),
(39, 'Can delete role', 13, 'delete_role'),
(40, 'Can add application role', 14, 'add_applicationrole'),
(41, 'Can change application role', 14, 'change_applicationrole'),
(42, 'Can delete application role', 14, 'delete_applicationrole'),
(52, 'Can add application membership', 18, 'add_applicationmembership'),
(53, 'Can change application membership', 18, 'change_applicationmembership'),
(54, 'Can delete application membership', 18, 'delete_applicationmembership'),
(55, 'Can add application member has role', 19, 'add_applicationmemberhasrole'),
(56, 'Can change application member has role', 19, 'change_applicationmemberhasrole'),
(57, 'Can delete application member has role', 19, 'delete_applicationmemberhasrole');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
`id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `corsheaders_corsmodel`
--

CREATE TABLE IF NOT EXISTS `corsheaders_corsmodel` (
`id` int(11) NOT NULL,
  `cors` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
`id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=20 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(10, 'app', 'application'),
(19, 'app', 'applicationmemberhasrole'),
(18, 'app', 'applicationmembership'),
(11, 'app', 'applicationowner'),
(14, 'app', 'applicationrole'),
(7, 'app', 'manager'),
(8, 'app', 'profile'),
(9, 'app', 'registrationrequest'),
(13, 'app', 'role'),
(2, 'auth', 'group'),
(1, 'auth', 'permission'),
(3, 'auth', 'user'),
(4, 'contenttypes', 'contenttype'),
(12, 'corsheaders', 'corsmodel'),
(5, 'sessions', 'session'),
(6, 'sites', 'site');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
`id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2016-06-24 08:10:02.734000'),
(2, 'contenttypes', '0002_remove_content_type_name', '2016-06-24 08:10:02.860000'),
(3, 'auth', '0001_initial', '2016-06-24 08:10:04.491000'),
(4, 'auth', '0002_alter_permission_name_max_length', '2016-06-24 08:10:04.575000'),
(5, 'auth', '0003_alter_user_email_max_length', '2016-06-24 08:10:04.666000'),
(6, 'auth', '0004_alter_user_username_opts', '2016-06-24 08:10:04.700000'),
(7, 'auth', '0005_alter_user_last_login_null', '2016-06-24 08:10:04.788000'),
(8, 'auth', '0006_require_contenttypes_0002', '2016-06-24 08:10:04.800000'),
(9, 'sessions', '0001_initial', '2016-06-24 08:10:05.276000'),
(10, 'sites', '0001_initial', '2016-06-24 08:10:05.414000');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

CREATE TABLE IF NOT EXISTS `django_site` (
`id` int(11) NOT NULL,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

-- --------------------------------------------------------

--
-- Table structure for table `iam_application`
--

CREATE TABLE IF NOT EXISTS `iam_application` (
`id` int(11) NOT NULL,
  `client_id` varchar(255) NOT NULL,
  `client_access_token` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(500) NOT NULL,
  `url` varchar(255) NOT NULL,
  `callback_url` varchar(500) NOT NULL,
  `callback_url2` varchar(500) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=18 ;

-- --------------------------------------------------------

--
-- Table structure for table `iam_application_membership`
--

CREATE TABLE IF NOT EXISTS `iam_application_membership` (
`id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=15 ;

-- --------------------------------------------------------

--
-- Table structure for table `iam_application_member_hasrole`
--

CREATE TABLE IF NOT EXISTS `iam_application_member_hasrole` (
`id` int(11) NOT NULL,
  `application_role_id` int(11) NOT NULL,
  `application_member_id` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=25 ;

-- --------------------------------------------------------

--
-- Table structure for table `iam_application_ownership`
--

CREATE TABLE IF NOT EXISTS `iam_application_ownership` (
`id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Table structure for table `iam_application_role`
--

CREATE TABLE IF NOT EXISTS `iam_application_role` (
`id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=315 ;

-- --------------------------------------------------------

--
-- Table structure for table `iam_manager`
--

CREATE TABLE IF NOT EXISTS `iam_manager` (
`id` int(11) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(128) NOT NULL,
  `token` varchar(255) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `iam_manager`
--

INSERT INTO `iam_manager` (`id`, `username`, `password`, `token`) VALUES
(1, 'amadmin', 'cm9vdHJvb3Q=', 'qweqkwldjqdu');

-- --------------------------------------------------------

--
-- Table structure for table `iam_profile`
--

CREATE TABLE IF NOT EXISTS `iam_profile` (
`id` int(11) NOT NULL,
  `name` varchar(127) NOT NULL,
  `surname` varchar(127) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `username` varchar(255) NOT NULL,
  `country` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `postcode` varchar(20) DEFAULT NULL,
  `mail` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `skills` varchar(10) NOT NULL,
  `activation` tinyint(1) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16 ;

-- --------------------------------------------------------

--
-- Table structure for table `iam_registration_request`
--

CREATE TABLE IF NOT EXISTS `iam_registration_request` (
`id` int(11) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `uuid` varchar(255) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=14 ;

-- --------------------------------------------------------

--
-- Table structure for table `iam_role`
--

CREATE TABLE IF NOT EXISTS `iam_role` (
`id` int(11) NOT NULL,
  `type` varchar(64) NOT NULL,
  `description` varchar(512) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=23 ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `group_id` (`group_id`,`permission_id`), ADD KEY `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `content_type_id` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `user_id` (`user_id`,`group_id`), ADD KEY `auth_user_groups_group_id_30a071c9_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `user_id` (`user_id`,`permission_id`), ADD KEY `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` (`permission_id`);

--
-- Indexes for table `corsheaders_corsmodel`
--
ALTER TABLE `corsheaders_corsmodel`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
 ADD PRIMARY KEY (`session_key`), ADD KEY `django_session_de54fa62` (`expire_date`);

--
-- Indexes for table `django_site`
--
ALTER TABLE `django_site`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `iam_application`
--
ALTER TABLE `iam_application`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `iam_application_membership`
--
ALTER TABLE `iam_application_membership`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `application_id` (`application_id`,`member_id`), ADD KEY `iam_application_membership_member_id_6b513b9_fk_iam_profile_id` (`member_id`);

--
-- Indexes for table `iam_application_member_hasrole`
--
ALTER TABLE `iam_application_member_hasrole`
 ADD PRIMARY KEY (`id`), ADD KEY `iam_appl_application_role_id_3126688d_fk_iam_application_role_id` (`application_role_id`), ADD KEY `application_member_id_351b3847_fk_iam_application_membership_id` (`application_member_id`);

--
-- Indexes for table `iam_application_ownership`
--
ALTER TABLE `iam_application_ownership`
 ADD PRIMARY KEY (`id`), ADD KEY `iam_application_ownership_user_id_3e017964_fk_iam_profile_id` (`user_id`), ADD KEY `iam_application_ow_application_id_639ff5bc_fk_iam_application_id` (`application_id`);

--
-- Indexes for table `iam_application_role`
--
ALTER TABLE `iam_application_role`
 ADD PRIMARY KEY (`id`), ADD KEY `iam_application_ro_application_id_4badcc28_fk_iam_application_id` (`application_id`), ADD KEY `iam_application_role_role_id_5c43f433_fk_iam_role_id` (`role_id`);

--
-- Indexes for table `iam_manager`
--
ALTER TABLE `iam_manager`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `username` (`username`), ADD UNIQUE KEY `password` (`password`);

--
-- Indexes for table `iam_profile`
--
ALTER TABLE `iam_profile`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `iam_registration_request`
--
ALTER TABLE `iam_registration_request`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `iam_role`
--
ALTER TABLE `iam_role`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `type` (`type`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=58;
--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `corsheaders_corsmodel`
--
ALTER TABLE `corsheaders_corsmodel`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `django_site`
--
ALTER TABLE `django_site`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `iam_application`
--
ALTER TABLE `iam_application`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT for table `iam_application_membership`
--
ALTER TABLE `iam_application_membership`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT for table `iam_application_member_hasrole`
--
ALTER TABLE `iam_application_member_hasrole`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=25;
--
-- AUTO_INCREMENT for table `iam_application_ownership`
--
ALTER TABLE `iam_application_ownership`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `iam_application_role`
--
ALTER TABLE `iam_application_role`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=315;
--
-- AUTO_INCREMENT for table `iam_manager`
--
ALTER TABLE `iam_manager`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `iam_profile`
--
ALTER TABLE `iam_profile`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `iam_registration_request`
--
ALTER TABLE `iam_registration_request`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT for table `iam_role`
--
ALTER TABLE `iam_role`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=23;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
ADD CONSTRAINT `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
ADD CONSTRAINT `auth_group_permissions_group_id_58c48ba9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
ADD CONSTRAINT `auth_permissi_content_type_id_51277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
ADD CONSTRAINT `auth_user_groups_group_id_30a071c9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
ADD CONSTRAINT `auth_user_groups_user_id_24702650_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
ADD CONSTRAINT `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
ADD CONSTRAINT `auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `iam_application_membership`
--
ALTER TABLE `iam_application_membership`
ADD CONSTRAINT `iam_application_me_application_id_27fd5b12_fk_iam_application_id` FOREIGN KEY (`application_id`) REFERENCES `iam_application` (`id`),
ADD CONSTRAINT `iam_application_membership_member_id_6b513b9_fk_iam_profile_id` FOREIGN KEY (`member_id`) REFERENCES `iam_profile` (`id`);

--
-- Constraints for table `iam_application_member_hasrole`
--
ALTER TABLE `iam_application_member_hasrole`
ADD CONSTRAINT `application_member_id_351b3847_fk_iam_application_membership_id` FOREIGN KEY (`application_member_id`) REFERENCES `iam_application_membership` (`id`),
ADD CONSTRAINT `iam_appl_application_role_id_3126688d_fk_iam_application_role_id` FOREIGN KEY (`application_role_id`) REFERENCES `iam_application_role` (`id`);

--
-- Constraints for table `iam_application_ownership`
--
ALTER TABLE `iam_application_ownership`
ADD CONSTRAINT `iam_application_ow_application_id_639ff5bc_fk_iam_application_id` FOREIGN KEY (`application_id`) REFERENCES `iam_application` (`id`),
ADD CONSTRAINT `iam_application_ownership_user_id_3e017964_fk_iam_profile_id` FOREIGN KEY (`user_id`) REFERENCES `iam_profile` (`id`);

--
-- Constraints for table `iam_application_role`
--
ALTER TABLE `iam_application_role`
ADD CONSTRAINT `iam_application_ro_application_id_4badcc28_fk_iam_application_id` FOREIGN KEY (`application_id`) REFERENCES `iam_application` (`id`),
ADD CONSTRAINT `iam_application_role_role_id_5c43f433_fk_iam_role_id` FOREIGN KEY (`role_id`) REFERENCES `iam_role` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
